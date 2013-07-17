# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('members_expensecategory', 'finance_expensecategory')
        db.rename_table('members_expense', 'finance_expense')
        db.rename_table('members_recurringexpense', 'finance_recurringexpense')
        db.rename_table('members_incomecategory', 'finance_incomecategory')
        db.rename_table('members_income', 'finance_income')
        db.rename_table('members_memberpayment', 'finance_memberpayment')

    def backwards(self, orm):
        db.rename_table('finance_expensecategory', 'members_expensecategory')
        db.rename_table('finance_expense', 'members_expense')
        db.rename_table('finance_recurringexpense', 'members_recurringexpense')
        db.rename_table('finance_incomecategory', 'members_incomecategory')
        db.rename_table('finance_income', 'members_income')
        db.rename_table('finance_memberpayment', 'members_memberpayment')

    complete_apps = ['finance']

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
            'continues_membership': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'free_months': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_existing_upgrade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"}),
            'membership_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Membership']"}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'payment_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'finance.recurringexpense': {
            'Meta': {'ordering': "['-date']", 'object_name': 'RecurringExpense', '_ormbases': [u'finance.Expense']},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['finance.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'period': ('django.db.models.fields.IntegerField', [], {}),
            'period_unit': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }