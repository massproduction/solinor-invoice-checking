# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 08:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0065_project_enable_weekly_notifications'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='weeklyreport',
            unique_together=set([('year', 'week', 'project_m')]),
        ),
        migrations.AlterModelOptions(
            name='weeklyreport',
            options={'ordering': ('-year', '-week', 'project_m')},
        ),
        migrations.RemoveField(
            model_name='weeklyreport',
            name='client',
        ),
        migrations.RemoveField(
            model_name='weeklyreport',
            name='project',
        ),
    ]