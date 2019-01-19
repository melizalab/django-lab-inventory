# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('chem_formula', models.CharField(max_length=45, null=True, verbose_name='Chemical formula', blank=True)),
                ('catalog', models.CharField(max_length=45, null=True, verbose_name='Catalog number', blank=True)),
                ('manufacturer_number', models.CharField(max_length=45, null=True, blank=True)),
                ('size', models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Size of unit', blank=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('comments', models.TextField(blank=True)),
                ('category', models.ForeignKey(to='inventory.Category', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=64)),
                ('url', models.CharField(max_length=64, null=True, blank=True)),
                ('rep', models.CharField(max_length=45, null=True, blank=True)),
                ('rep_phone', models.CharField(max_length=16, null=True, blank=True)),
                ('support_phone', models.CharField(max_length=16, null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('units_purchased', models.IntegerField()),
                ('cost', models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Cost per unit', blank=True)),
                ('date_arrived', models.DateField(null=True, blank=True)),
                ('serial', models.CharField(max_length=45, null=True, verbose_name='Serial number', blank=True)),
                ('uva_equip', models.CharField(max_length=32, null=True, verbose_name='UVa equipment number', blank=True)),
                ('location', models.CharField(max_length=45, null=True, help_text='example: -80 freezer, refrigerator, Gilmer 283', blank=True)),
                ('expiry_years', models.DecimalField(max_digits=4, decimal_places=2, null=True, verbose_name='Warranty or Item expiration (y)', blank=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('code', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(max_length=128)),
                ('expires', models.DateField(null=True, blank=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=64)),
                ('url', models.CharField(max_length=64, null=True, blank=True)),
                ('phone', models.CharField(max_length=16, null=True, blank=True)),
                ('rep', models.CharField(max_length=45, null=True, blank=True)),
                ('rep_phone', models.CharField(max_length=16, null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='inventory.OrderItem', to='inventory.Item'),
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
