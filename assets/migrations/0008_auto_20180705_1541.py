# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-07-05 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0007_auto_20180704_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabinet',
            name='created',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='machineroom',
            name='created',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='operationlog',
            name='created',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='physicalmachine',
            name='created',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='valuemachine',
            name='created',
            field=models.DateField(auto_now=True),
        ),
    ]
