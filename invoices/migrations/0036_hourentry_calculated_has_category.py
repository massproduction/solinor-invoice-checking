# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-24 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0035_auto_20170420_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='hourentry',
            name='calculated_has_category',
            field=models.BooleanField(default=True),
        ),
    ]
