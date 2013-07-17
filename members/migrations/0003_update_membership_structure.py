# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ('finance', '0002_update_membership_structure'),
    )

    def forwards(self, orm):
        db.rename_table(u'members_membershipcost', u'members_legacymembershipcost')
        db.rename_table(u'members_membership', u'members_legacymembership')
        # Adding model 'Membership'
        db.create_table(u'members_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('membership_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('membership_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'members', ['Membership'])


    def backwards(self, orm):
        db.rename_table(u'members_legacymembershipcost', u'members_membershipcost')
        db.delete_table(u'members_membership')
        db.rename_table(u'members_legacymembership', u'members_membership')


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
        u'members.legacymembership': {
            'Meta': {'object_name': 'LegacyMembership'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'membership_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'members.legacymembershipcost': {
            'Meta': {'ordering': "['valid_from']", 'object_name': 'LegacyMembershipCost'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.LegacyMembership']"}),
            'monthly_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'valid_from': ('django.db.models.fields.DateField', [], {})
        },
        u'members.phone': {
            'Meta': {'object_name': 'Phone'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['members']