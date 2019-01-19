# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('inventory', '0001_initial'), ('inventory', '0002_auto_20150626_1805'), ('inventory', '0003_auto_20150626_1807')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('chem_formula', models.CharField(blank=True, max_length=45, verbose_name='Chemical formula', null=True)),
                ('catalog', models.CharField(blank=True, max_length=45, verbose_name='Catalog number', null=True)),
                ('manufacturer_number', models.CharField(blank=True, max_length=45, null=True)),
                ('size', models.DecimalField(blank=True, null=True, verbose_name='Size of unit', decimal_places=2, max_digits=10)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('comments', models.TextField(blank=True)),
                ('category', models.ForeignKey(to='inventory.Category', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=64)),
                ('url', models.CharField(blank=True, max_length=64, null=True)),
                ('rep', models.CharField(blank=True, max_length=128, null=True)),
                ('rep_phone', models.CharField(blank=True, max_length=16, null=True)),
                ('support_phone', models.CharField(blank=True, max_length=16, null=True)),
                ('lookup_url', models.CharField(blank=True, max_length=64, help_text='url pattern to look up part number', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=64)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ordered', models.BooleanField()),
                ('order_date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'ordering': ['-order_date', 'name'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('units_purchased', models.IntegerField()),
                ('cost', models.DecimalField(blank=True, null=True, verbose_name='Cost per unit', decimal_places=2, max_digits=10)),
                ('date_arrived', models.DateField(blank=True, null=True)),
                ('serial', models.CharField(blank=True, max_length=45, verbose_name='Serial number', null=True)),
                ('uva_equip', models.CharField(blank=True, max_length=32, verbose_name='UVa equipment number', null=True)),
                ('location', models.CharField(blank=True, max_length=45, help_text='example: -80 freezer, refrigerator, Gilmer 283', null=True)),
                ('expiry_years', models.DecimalField(blank=True, null=True, verbose_name='Warranty or Item expiration (y)', decimal_places=2, max_digits=4)),
                ('reconciled', models.BooleanField()),
                ('item', models.ForeignKey(to='inventory.Item', on_delete=models.CASCADE)),
                ('order', models.ForeignKey(to='inventory.Order', on_delete=models.CASCADE)),
            ],
            options={
                'db_table': 'inventory_order_items',
            },
        ),
        migrations.CreateModel(
            name='PTAO',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(max_length=128)),
                ('expires', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ['code'],
                'verbose_name': 'PTAO',
                'verbose_name_plural': 'PTAOs',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=64)),
                ('url', models.CharField(blank=True, max_length=64, null=True)),
                ('phone', models.CharField(blank=True, max_length=16, null=True)),
                ('rep', models.CharField(blank=True, max_length=45, null=True)),
                ('rep_phone', models.CharField(blank=True, max_length=16, null=True)),
                ('lookup_url', models.CharField(blank=True, max_length=128, help_text='url pattern to look up catalog number', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='inventory.Item', through='inventory.OrderItem'),
        ),
        migrations.AddField(
            model_name='order',
            name='ordered_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='order',
            name='ptao',
            field=models.ForeignKey(blank=True, to='inventory.PTAO', null=True, on_delete=models.SET_NULL),
        ),
        migrations.AddField(
            model_name='item',
            name='manufacturer',
            field=models.ForeignKey(help_text='leave blank if unknown or same as vendor', blank=True,
                                    to='inventory.Manufacturer', null=True, on_delete=models.SET_NULL),
        ),
        migrations.AddField(
            model_name='item',
            name='parent_item',
            field=models.ForeignKey(help_text='example: for printer cartriges, select printer', blank=True,
                                    to='inventory.Item', null=True, on_delete=models.SET_NULL),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(to='inventory.Unit', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='item',
            name='vendor',
            field=models.ForeignKey(to='inventory.Vendor', on_delete=models.CASCADE),
        ),
    ]
