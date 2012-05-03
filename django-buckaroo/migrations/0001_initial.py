# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PaymentMethodType'
        db.create_table('buckaroo_paymentmethodtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('sysname', self.gf('django.db.models.fields.CharField')(max_length=96, blank=True)),
        ))
        db.send_create_signal('buckaroo', ['PaymentMethodType'])

        # Adding model 'PaymentMethod'
        db.create_table('buckaroo_paymentmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('sysname', self.gf('django.db.models.fields.CharField')(max_length=96, blank=True)),
            ('payment_method_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['buckaroo.PaymentMethodType'], null=True, blank=True)),
        ))
        db.send_create_signal('buckaroo', ['PaymentMethod'])

        # Adding model 'Transaction'
        db.create_table('buckaroo_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=192, blank=True)),
            ('invoice', self.gf('django.db.models.fields.CharField')(unique=True, max_length=48)),
            ('reference', self.gf('django.db.models.fields.CharField')(unique=True, max_length=48)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('return_url', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('buckaroo', ['Transaction'])

        # Adding model 'TransactionState'
        db.create_table('buckaroo_transactionstate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['buckaroo.PaymentMethod'], null=True, blank=True)),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['buckaroo.Transaction'], null=True, blank=True)),
            ('valid_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('valid_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('response_message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('account_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('idealurl', self.gf('django.db.models.fields.CharField')(max_length=765, null=True, blank=True)),
            ('transactionkey', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('responsestatusdescription', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('idealtransactionid', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('responsestatus', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('additionalmessage', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('buckaroo', ['TransactionState'])

    def backwards(self, orm):
        # Deleting model 'PaymentMethodType'
        db.delete_table('buckaroo_paymentmethodtype')

        # Deleting model 'PaymentMethod'
        db.delete_table('buckaroo_paymentmethod')

        # Deleting model 'Transaction'
        db.delete_table('buckaroo_transaction')

        # Deleting model 'TransactionState'
        db.delete_table('buckaroo_transactionstate')

    models = {
        'buckaroo.paymentmethod': {
            'Meta': {'object_name': 'PaymentMethod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'payment_method_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buckaroo.PaymentMethodType']", 'null': 'True', 'blank': 'True'}),
            'sysname': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'})
        },
        'buckaroo.paymentmethodtype': {
            'Meta': {'object_name': 'PaymentMethodType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'sysname': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'})
        },
        'buckaroo.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '192', 'blank': 'True'}),
            'return_url': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'})
        },
        'buckaroo.transactionstate': {
            'Meta': {'object_name': 'TransactionState'},
            'account_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'additionalmessage': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idealtransactionid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'idealurl': ('django.db.models.fields.CharField', [], {'max_length': '765', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'payment_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buckaroo.PaymentMethod']", 'null': 'True', 'blank': 'True'}),
            'response_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'responsestatus': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'responsestatusdescription': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buckaroo.Transaction']", 'null': 'True', 'blank': 'True'}),
            'transactionkey': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'valid_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['buckaroo']