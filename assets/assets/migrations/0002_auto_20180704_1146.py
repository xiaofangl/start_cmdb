# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-07-04 03:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cabinet',
            old_name='contact',
            new_name='Cabinet',
        ),
    ]
