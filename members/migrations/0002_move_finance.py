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

    models = {
        u'members.email': {
            'Meta': {'object_name': 'Email'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_preferred': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"})
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
    }