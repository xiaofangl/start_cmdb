# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-07-04 04:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_auto_20180704_1146'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(default='', max_length=45, verbose_name='')),
                ('level', models.CharField(default='0', max_length=30, verbose_name='')),
                ('desc', models.CharField(max_length=256, null=True, verbose_name='')),
                ('created', models.DateField(auto_now_add=True)),
                ('is_del', models.BooleanField(verbose_name=False)),
            ],
        ),
    ]
