# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-14 19:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0052_auto_20170513_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='billable_percentage',
            field=models.FloatField(default=0),
        ),
    ]
