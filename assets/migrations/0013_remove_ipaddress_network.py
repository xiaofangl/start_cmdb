# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-07-23 09:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0012_auto_20180723_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ipaddress',
            name='network',
        ),
    ]
