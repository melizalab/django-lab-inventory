# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='lookup_url',
            field=models.CharField(blank=True, max_length=64, null=True, help_text='url pattern to look up part number'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='lookup_url',
            field=models.CharField(blank=True, max_length=64, null=True, help_text='url pattern to look up catalog number'),
        ),
    ]
