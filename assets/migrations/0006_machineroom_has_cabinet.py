# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-07-04 04:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_auto_20180704_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='machineroom',
            name='has_cabinet',
            field=models.BooleanField(default=2, verbose_name=True),
            preserve_default=False,
        ),
    ]
