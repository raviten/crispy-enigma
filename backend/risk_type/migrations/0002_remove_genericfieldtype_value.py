# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-04 12:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('risk_type', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genericfieldtype',
            name='value',
        ),
    ]
