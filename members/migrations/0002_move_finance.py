# -*- coding: utf-8 -*-
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    depends_on = (
        ('finance', '0001_move_finance'),
    )

    def forwards(self, orm):
        pass

    def backwards(self, orm):
        pass

    complete_apps = ['members']