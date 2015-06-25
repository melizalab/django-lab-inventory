# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('chem_formula', models.CharField(max_length=45, blank=True, null=True, verbose_name='Chemical formula')),
                ('catalog', models.CharField(max_length=45, blank=True, null=True, verbose_name='Catalog number')),
                ('manufacturer_number', models.CharField(max_length=45, blank=True, null=True)),
                ('size', models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2, verbose_name='Size of unit')),
                ('units_purchased', models.IntegerField()),
                ('cost', models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2, verbose_name='Cost per unit')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_arrived', models.DateField(blank=True, null=True)),
                ('serial', models.CharField(max_length=45, blank=True, null=True, verbose_name='Serial number')),
                ('uva_equip', models.CharField(max_length=32, blank=True, null=True, verbose_name='UVa equipment number')),
                ('location', models.CharField(max_length=45, blank=True, null=True)),
                ('expiry_years', models.DecimalField(max_digits=4, blank=True, null=True, decimal_places=2, verbose_name='Warranty or Item expiration (y)')),
                ('comments', models.TextField(blank=True)),
                ('category', models.ForeignKey(to='inventory.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('url', models.CharField(max_length=64, blank=True, null=True)),
                ('rep', models.CharField(max_length=45, blank=True, null=True)),
                ('rep_phone', models.CharField(max_length=16, blank=True, null=True)),
                ('support_phone', models.CharField(max_length=16, blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ordered', models.BooleanField()),
                ('order_date', models.DateField(default=datetime.date.today)),
                ('reconciled', models.BooleanField()),
                ('items', models.ManyToManyField(to='inventory.Item', blank=True)),
                ('ordered_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-order_date', 'name'],
            },
        ),
        migrations.CreateModel(
            name='PTAO',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(unique=True, max_length=64)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('url', models.CharField(max_length=64, blank=True, null=True)),
                ('phone', models.CharField(max_length=16, blank=True, null=True)),
                ('rep', models.CharField(max_length=45, blank=True, null=True)),
                ('rep_phone', models.CharField(max_length=16, blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='ptao',
            field=models.ForeignKey(to='inventory.PTAO', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='manufacturer',
            field=models.ForeignKey(to='inventory.Manufacturer', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='parent_item',
            field=models.ForeignKey(to='inventory.Item', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(to='inventory.Unit'),
        ),
        migrations.AddField(
            model_name='item',
            name='vendor',
            field=models.ForeignKey(to='inventory.Vendor'),
        ),
    ]
