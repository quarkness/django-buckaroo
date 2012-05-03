from django.db import models


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models


class PaymentMethodType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sysname = models.CharField(max_length=96, blank=True)

    def __unicode__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sysname = models.CharField(max_length=96, blank=True)
    payment_method_type = models.ForeignKey(PaymentMethodType, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Transaction(models.Model):
    remote_id = models.CharField(max_length=192, blank=True)
    invoice = models.CharField(max_length=48, unique=True)
    reference = models.CharField(max_length=48, unique=True)
    price = models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)
    description = models.CharField(max_length=765, blank=True)
    return_url = models.CharField(max_length=765, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TransactionState(models.Model):
    payment_method = models.ForeignKey(PaymentMethod, null=True, blank=True)
    transaction = models.ForeignKey(Transaction, null=True, blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    response_message = models.TextField(null=True, blank=True)

    # machtiging
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    account_name = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=32, blank=True)

    #ideal
    idealurl = models.CharField(max_length=765, blank=True, null=True)
    transactionkey = models.CharField(max_length=128, blank=True, null=True)
    responsestatusdescription = models.CharField(max_length=128, blank=True, null=True)
    idealtransactionid = models.CharField(max_length=128, blank=True, null=True)
    responsestatus = models.CharField(max_length=16, blank=True, null=True)
    additionalmessage = models.CharField(max_length=128, blank=True, null=True)
    # state = models.ForeignKey(State, null=True, blank=True)



