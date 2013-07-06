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