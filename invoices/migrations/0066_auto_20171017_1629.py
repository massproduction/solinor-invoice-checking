# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0065_project_enable_weekly_notifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weeklyreport',
            name='has_comments',
        ),
        migrations.AddField(
            model_name='weeklyreport',
            name='change_of_scope',
            field=models.TextField(blank=True, null=True),
        ),
    ]