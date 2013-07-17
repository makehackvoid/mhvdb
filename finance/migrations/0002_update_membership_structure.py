# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExpiringProduct'
        db.create_table(u'finance_expiringproduct', (
            (u'product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['finance.Product'], unique=True, primary_key=True)),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('duration_type', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'finance', ['ExpiringProduct'])

        # Adding model 'Product'
        db.create_table(u'finance_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'finance', ['Product'])

        db.rename_table(u'finance_memberpayment', u'finance_legacymemberpayment')

        db.create_table(u'finance_memberpayment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('payment_value', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['finance.Product'])),
        ))
        db.send_create_signal(u'finance', ['MemberPayment'])

        db.create_table(u'finance_membershipproduct', (
            (u'expiringproduct_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['finance.ExpiringProduct'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'finance', ['MembershipProduct'])


    def backwards(self, orm):
        # Deleting model 'ExpiringProduct'
        db.delete_table(u'finance_expiringproduct')

        # Deleting model 'Product'
        db.delete_table(u'finance_product')

        db.delete_table(u'finance_memberpayment')

        db.rename_table(u'finance_legacymemberpayment', u'finance_memberpaymenst')

        # Deleting model 'MembershipProduct'
        db.delete_table(u'finance_membershipproduct')

    models = {
        u'finance.expense': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Expense'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.ExpenseCategory']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'payment_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'via_member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']", 'null': 'True', 'blank': 'True'})
        },
        u'finance.expensecategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'ExpenseCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'finance.expiringproduct': {
            'Meta': {'object_name': 'ExpiringProduct', '_ormbases': [u'finance.Product']},
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'duration_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['finance.Product']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'finance.income': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Income'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.IncomeCategory']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'payment_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'finance.incomecategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'IncomeCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'finance.memberpayment': {
            'Meta': {'ordering': "['-date']", 'object_name': 'MemberPayment'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'payment_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Product']"})
        },
        u'finance.legacymemberpayment': {
            'Meta': {'ordering': "['-date']", 'object_name': 'LegacyMemberPayment'},
            'continues_membership': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'free_months': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_existing_upgrade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"}),
            'membership_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.LegacyMembership']"}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'payment_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'finance.product': {
            'Meta': {'object_name': 'Product'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'finance.recurringexpense': {
            'Meta': {'ordering': "['-date']", 'object_name': 'RecurringExpense', '_ormbases': [u'finance.Expense']},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['finance.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'period': ('django.db.models.fields.IntegerField', [], {}),
            'period_unit': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'members.member': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Member'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'emergency_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'emergency_contact_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateField', [], {}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'medical_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'members.membership': {
            'Meta': {'object_name': 'Membership'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'membership_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'members.legacymembership': {
            'Meta': {'object_name': 'LegacyMembership'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'membership_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'finance.membershipproduct': {
            'Meta': {'object_name': 'MembershipProduct', '_ormbases': [u'finance.ExpiringProduct']},
            u'expiringproduct_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['finance.ExpiringProduct']", 'unique': 'True', 'primary_key': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Membership']"})
        },
    }

    complete_apps = ['finance']