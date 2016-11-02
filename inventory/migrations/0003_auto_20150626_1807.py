# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20150626_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='rep',
            field=models.CharField(null=True, max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='lookup_url',
            field=models.CharField(null=True, help_text='url pattern to look up catalog number', max_length=128, blank=True),
        ),
    ]
