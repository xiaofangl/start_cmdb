# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-07-04 04:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_operationlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationlog',
            name='status',
            field=models.BooleanField(default=2, verbose_name=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='operationlog',
            name='level',
            field=models.CharField(default='0', max_length=30, null=True, verbose_name=''),
        ),
    ]
