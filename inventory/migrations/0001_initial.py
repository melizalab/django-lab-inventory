# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table(u'inventory_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('chem_formula', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Vendor'])),
            ('catalog', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Manufacturer'], null=True, blank=True)),
            ('manufacturer_number', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Unit'])),
            ('units_purchased', self.gf('django.db.models.fields.IntegerField')()),
            ('cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Category'])),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_arrived', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('serial', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('uva_equip', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('parent_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'], null=True, blank=True)),
            ('expiry_years', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Item'])

        # Adding model 'Category'
        db.create_table(u'inventory_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal(u'inventory', ['Category'])

        # Adding model 'Unit'
        db.create_table(u'inventory_unit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal(u'inventory', ['Unit'])

        # Adding model 'Manufacturer'
        db.create_table(u'inventory_manufacturer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('rep', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('rep_phone', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('support_phone', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Manufacturer'])

        # Adding model 'Vendor'
        db.create_table(u'inventory_vendor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('rep', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('rep_phone', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Vendor'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table(u'inventory_item')

        # Deleting model 'Category'
        db.delete_table(u'inventory_category')

        # Deleting model 'Unit'
        db.delete_table(u'inventory_unit')

        # Deleting model 'Manufacturer'
        db.delete_table(u'inventory_manufacturer')

        # Deleting model 'Vendor'
        db.delete_table(u'inventory_vendor')


    models = {
        u'inventory.category': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'catalog': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Category']"}),
            'chem_formula': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_arrived': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'expiry_years': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Manufacturer']", 'null': 'True', 'blank': 'True'}),
            'manufacturer_number': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent_item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']", 'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Unit']"}),
            'units_purchased': ('django.db.models.fields.IntegerField', [], {}),
            'uva_equip': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Vendor']"})
        },
        u'inventory.manufacturer': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Manufacturer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'rep': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'rep_phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'support_phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'inventory.unit': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Unit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'inventory.vendor': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Vendor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'rep': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'rep_phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['inventory']