# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-03 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('client', models.CharField(max_length=100)),
                ('project', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together=set([('year', 'month', 'client', 'project')]),
        ),
    ]
