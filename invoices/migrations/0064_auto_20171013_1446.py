# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-13 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0063_weeklyreportcomments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weeklyreport',
            name='invoice_state',
        ),
        migrations.AddField(
            model_name='weeklyreport',
            name='weekly_report_state',
            field=models.CharField(choices=[('C', 'Created'), ('A', 'Approved')], default='C', max_length=1),
        ),
    ]
