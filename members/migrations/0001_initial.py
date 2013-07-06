# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Member'
        db.create_table(u'members_member', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('join_date', self.gf('django.db.models.fields.DateField')()),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('emergency_contact_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('emergency_contact_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('medical_info', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'members', ['Member'])

        # Adding model 'Email'
        db.create_table(u'members_email', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('is_preferred', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'members', ['Email'])

        # Adding model 'ExpenseCategory'
        db.create_table(u'members_expensecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'members', ['ExpenseCategory'])

        # Adding model 'Expense'
        db.create_table(u'members_expense', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('via_member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('payment_value', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.ExpenseCategory'])),
        ))
        db.send_create_signal(u'members', ['Expense'])

        # Adding model 'RecurringExpense'
        db.create_table(u'members_recurringexpense', (
            (u'expense_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['members.Expense'], unique=True, primary_key=True)),
            ('period_unit', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('period', self.gf('django.db.models.fields.IntegerField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'members', ['RecurringExpense'])

        # Adding model 'Membership'
        db.create_table(u'members_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('membership_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('membership_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'members', ['Membership'])

        # Adding model 'IncomeCategory'
        db.create_table(u'members_incomecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'members', ['IncomeCategory'])

        # Adding model 'Income'
        db.create_table(u'members_income', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('payment_value', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.IncomeCategory'])),
        ))
        db.send_create_signal(u'members', ['Income'])

        # Adding model 'MemberPayment'
        db.create_table(u'members_memberpayment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('payment_value', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('membership_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Membership'])),
            ('free_months', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('continues_membership', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_existing_upgrade', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'members', ['MemberPayment'])

        # Adding model 'MembershipCost'
        db.create_table(u'members_membershipcost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('membership', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Membership'])),
            ('monthly_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('valid_from', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'members', ['MembershipCost'])

        # Adding model 'Phone'
        db.create_table(u'members_phone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
        ))
        db.send_create_signal(u'members', ['Phone'])


    def backwards(self, orm):
        # Deleting model 'Member'
        db.delete_table(u'members_member')

        # Deleting model 'Email'
        db.delete_table(u'members_email')

        # Deleting model 'ExpenseCategory'
        db.delete_table(u'members_expensecategory')

        # Deleting model 'Expense'
        db.delete_table(u'members_expense')

        # Deleting model 'RecurringExpense'
        db.delete_table(u'members_recurringexpense')

        # Deleting model 'Membership'
        db.delete_table(u'members_membership')

        # Deleting model 'IncomeCategory'
        db.delete_table(u'members_incomecategory')

        # Deleting model 'Income'
        db.delete_table(u'members_income')

        # Deleting model 'MemberPayment'
        db.delete_table(u'members_memberpayment')

        # Deleting model 'MembershipCost'
        db.delete_table(u'members_membershipcost')

        # Deleting model 'Phone'
        db.delete_table(u'members_phone')


    models = {
        u'members.email': {
            'Meta': {'object_name': 'Email'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_preferred': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"})
        },
        u'members.expense': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Expense'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.ExpenseCategory']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'payment_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'via_member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']", 'null': 'True', 'blank': 'True'})
        },
        u'members.expensecategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'ExpenseCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'members.income': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Income'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.IncomeCategory']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'payment_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'members.incomecategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'IncomeCategory'},
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
        u'members.memberpayment': {
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
        u'members.membership': {
            'Meta': {'object_name': 'Membership'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'membership_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'members.membershipcost': {
            'Meta': {'ordering': "['valid_from']", 'object_name': 'MembershipCost'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Membership']"}),
            'monthly_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'valid_from': ('django.db.models.fields.DateField', [], {})
        },
        u'members.phone': {
            'Meta': {'object_name': 'Phone'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'members.recurringexpense': {
            'Meta': {'ordering': "['-date']", 'object_name': 'RecurringExpense', '_ormbases': [u'members.Expense']},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'expense_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['members.Expense']", 'unique': 'True', 'primary_key': 'True'}),
            'period': ('django.db.models.fields.IntegerField', [], {}),
            'period_unit': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['members']