# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-28 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0038_auto_20170424_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hourentry',
            name='date',
            field=models.DateField(db_index=True),
        ),
    ]
