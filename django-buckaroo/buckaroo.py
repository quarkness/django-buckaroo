from django.template.loader import render_to_string
from datetime import datetime
from lxml import etree
import re
import random 
import hashlib 
import requests

SOAP_URL = 'https://payment.buckaroo.nl/soap/soap.asmx'

def md5(to_hash):
    m = hashlib.md5()
    m.update(to_hash)
    return m.hexdigest()


def signature_payload(payload, soap_secret_key):
    return md5(payload.replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '') + soap_secret_key)


class BuckarooException(Exception):
    def __init__(self, error):
        self.error = error
    def __str__(self):
        return self.error


class Buckaroo(object):
    def __init__(self, merchant_key=None, soap_fingerprint=None, soap_secret_key=None):
        self.language = 'NL'
        self.test = 'TRUE'
        self.teststatus = '800'
        self.sendersessionid = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # "yyyy-mm-dd hh:mm:ss"

        self.merchantid = merchant_key
        self.soap_fingerprint = soap_fingerprint
        self.soap_secret_key = soap_secret_key

        self.currency = 'EUR'
        self.amount = None
        self.invoice = None
        self.reference = None
        self.description = None

        self.calculatemethod = '100'

        self.method = type(self).__name__

    def get_global_template_vars(self):
        template_vars = {
            'method':self.method
        }
        control = {
            'language': self.language,
            'test': self.test,
            'teststatus': self.teststatus,
            'sendersessionid': self.sendersessionid,
            'timestamp': self.timestamp,
            'merchantid': self.merchantid,
        }

        invoice = {
            'currency': self.currency,
            'amount': self.amount,
            'invoice': self.invoice,
            'reference': self.reference,
            'description': self.description,
        }
        template_vars.update(**control)
        template_vars.update(**invoice)
        return template_vars

    def send(self):
        payload = self.payload()
        request_xml = self.request(payload)
        headers = {
            'Content-Type': 'application/soap+xml;charset=UTF-8;action="https://payment.buckaroo.nl/%s"' % self.method
        }
        r = requests.post(SOAP_URL, data=request_xml, headers=headers)
        print r.status_code
        print r.content
        m = re.match('.*<XMLMessage>(.*)</XMLMessage>.*', r.content, re.MULTILINE)
        x = re.match('.*<soap:Body>(.*)</soap:Body>.*', r.content, re.MULTILINE) # lelijke hack om "Unicode strings with encoding declaration are not supported." te voorkomen. 
        # tostring

        response = etree.fromstring(x.group(1))


        error = response.find(".//Error")
        print error
        if error is not None:
            raise BuckarooException(error.text)

        signaturevalue = response.find(".//SignatureValue").text

        print 'signaturevalue: %s' % signaturevalue
        transactions = response.findall(".//Transaction")

        response = {}
        
        transaction = transactions[0]
        for element in transaction.iter():
            if element.tag in self.transaction_tags:
                response[element.tag.lower()] = element.text
                # print("%s - %s" % (element.tag, element.text))

        print 'payload response: %s' % m.group(1)
        signaturevalue = signature_payload(m.group(1), self.soap_secret_key)


        if signaturevalue != signature_payload(m.group(1), self.soap_secret_key):
            pass
            # raise Exception('Invalid signature')
        print response
        return response

    def request(self, payload):

        template_vars = {}

        signaturevalue = signature_payload(payload)
        # print 'payload: %s' % payload
        # print 'signature_payload: %s' % signature_payload
        signature = {
            'fingerprint': self.soap_fingerprint,
            'digestmethod': 'MD5',
            'calculatemethod': self.calculatemethod,
            'signaturevalue': signaturevalue,
        }
        
        template_vars.update(**signature)
        template_vars.update(method=self.method)
        template_vars.update(payload=payload)
        request_xml = render_to_string('buckaroo/soap.xml', template_vars)
        print request_xml
        return request_xml


class EenmaligeMachtiging(Buckaroo):
    def __init__(self):
        super(EenmaligeMachtiging, self).__init__()
        self.counter = '1'
        self.gender = '0'
        self.teststatus = '600'
        self.firstname = None
        self.lastname = None
        self.mail = None
        self.accountnumber = None
        self.accountname = None
        self.collectdate = datetime.now().strftime('%Y-%m-%d')  # "yyyy-mm-dd hh:mm:ss"
        self.collecttype = 'single' #  'recurring' TODO uitzoek


    def payload(self):
        template_vars = {
            'counter': self.counter,
            'gender': self.gender,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'mail': self.mail,
            'accountnumber': self.accountnumber,
            'accountname': self.accountname,
            'method': 'EenmaligeMachtiging'
        }
 
        template_vars.update(**self.get_global_template_vars())
        return render_to_string('buckaroo/EenmaligeMachtiging.xml', template_vars)


class IDeal(Buckaroo):
    def __init__(self):
        super(IDeal, self).__init__()
        self.issuers = ['ABNAMRO', 'ASNBANK', 'FRIESLAND', 'INGBANK', 'RABOBANK', 'SNSBANK', 'SNSREGIO', 'TRIODOS', 'LANSCHOT']
        self.issuer = None
        self.transaction_tags = ['TransactionKey', 'IdealUrl', 'IdealTransactionId', 'Amount', 'Invoice', 'Reference', 'Description', 'ResponseStatus', 'ResponseStatusDescription', 'AdditionalMessage']
        self.returnurl = 'http://localhost:8000/demo/ivo'

    def payload(self):
        if not self.issuer or self.issuer not in self.issuers:
            raise Exception('geen geldige issuer')

        template_vars = {
            'returnurl': self.returnurl,
            'issuer': self.issuer,
            'method': 'IDeal'
        }
 
        template_vars.update(**self.get_global_template_vars())
        return render_to_string('buckaroo/IDeal.xml', template_vars)


class StatusRequest(Buckaroo):
    def __init__(self):
        super(StatusRequest, self).__init__()
        self.transactionkey = None
        self.invoice = None


    def payload(self):
        if not self.transactionkey or not self.invoice:
            raise Exception('transactionkey or invoice missing')
        template_vars = self.get_global_template_vars()
        print template_vars
        return render_to_string('buckaroo/StatusRequest.xml', template_vars)

