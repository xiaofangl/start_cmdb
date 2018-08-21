# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-07-03 08:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=30, null=True, verbose_name='\u673a\u67dc')),
                ('is_del', models.BooleanField(verbose_name=False)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MachineRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(default='\u5317\u4eac\u9152\u4ed9\u6865\u9e4f\u535a\u58eb', max_length=124, verbose_name='\u673a\u623f\u540d\u79f0')),
                ('room_bandwidth', models.CharField(max_length=124, null=True, verbose_name='\u673a\u623f\u5e26\u5bbd')),
                ('ip_address', models.CharField(max_length=124, null=True, verbose_name='IP\u5730\u5740\u6bb5')),
                ('isp', models.CharField(max_length=124, null=True, verbose_name='\u8fd0\u8425\u5546')),
                ('contact', models.CharField(max_length=124, null=True, verbose_name='\u8054\u7cfb\u4eba')),
                ('contact_phone', models.CharField(max_length=124, null=True, verbose_name='\u8054\u7cfb\u7535\u8bdd')),
                ('room_address', models.CharField(max_length=124, null=True, verbose_name='\u673a\u623f\u5730\u5740')),
                ('room_telephone', models.CharField(max_length=30, null=True, verbose_name='\u673a\u623f\u7535\u8bdd')),
                ('is_del', models.BooleanField(verbose_name=False)),
                ('created', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='PhysicalMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(default='0', max_length=30, verbose_name='IP')),
                ('type', models.CharField(choices=[('0', '\u865a\u62df\u673a'), ('1', '\u7269\u7406\u673a')], default='1', max_length=30, verbose_name='\u7c7b\u578b')),
                ('hostname', models.CharField(max_length=30, null=True, verbose_name='\u4e3b\u673a\u540d')),
                ('fqdn', models.CharField(max_length=45, null=True, verbose_name='\u5b8c\u5168\u5408\u683c\u57df\u540d')),
                ('system', models.CharField(choices=[('0', 'centos7'), ('1', 'centos6.7'), ('2', 'ubuntu12'), ('3', 'server2012'), ('4', 'server2008'), ('5', '\u5176\u4ed6'), ('6', '')], default='6', max_length=30, null=True, verbose_name='\u7cfb\u7edf\u7248\u672c')),
                ('env', models.CharField(choices=[('0', '\u751f\u4ea7'), ('1', '\u9884\u53d1\u5e03'), ('2', '\u6d4b\u8bd5'), ('3', '\u5f00\u53d1')], default='0', max_length=30, verbose_name='\u8fd0\u884c\u73af\u5883')),
                ('disk_array', models.CharField(choices=[('1', 'raid 0'), ('2', 'raid 1'), ('3', 'raid 5'), ('4', 'raid 10'), ('5', 'raid 5+\u70ed\u5907'), ('6', 'other')], default='6', max_length=30, verbose_name='\u78c1\u76d8\u9635\u5217')),
                ('cpu', models.CharField(max_length=124, null=True, verbose_name='CPU')),
                ('mem', models.CharField(max_length=124, null=True, verbose_name='\u5185\u5b58')),
                ('disk', models.CharField(max_length=124, null=True, verbose_name='\u786c\u76d8')),
                ('machine_model', models.CharField(max_length=124, null=True, verbose_name='\u670d\u52a1\u5668\u578b\u53f7')),
                ('sn', models.CharField(max_length=30, null=True, verbose_name='SN\u7f16\u53f7')),
                ('quick_service', models.CharField(max_length=30, null=True, verbose_name='\u5feb\u901f\u670d\u52a1\u7f16\u7801')),
                ('remote_control', models.CharField(max_length=30, null=True, verbose_name='\u8fdc\u63a7\u5361\u53f7')),
                ('warranty', models.CharField(max_length=30, null=True, verbose_name='\u4fdd\u4fee\u671f')),
                ('user', models.CharField(max_length=30, null=True, verbose_name='\u7ba1\u7406\u7528\u6237')),
                ('pawd', models.CharField(max_length=30, null=True, verbose_name='\u5bc6\u7801')),
                ('created', models.DateField(auto_now_add=True)),
                ('is_del', models.BooleanField(verbose_name=False)),
                ('cabinet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Cabinet')),
                ('machine_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.MachineRoom')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='ValueMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(default='0', max_length=30, verbose_name='IP')),
                ('type', models.CharField(choices=[('0', '\u865a\u62df\u673a'), ('1', '\u7269\u7406\u673a')], default='0', max_length=30, verbose_name='\u7c7b\u578b')),
                ('hostname', models.CharField(max_length=30, null=True, verbose_name='\u4e3b\u673a\u540d')),
                ('fqdn', models.CharField(max_length=45, null=True, verbose_name='\u5b8c\u5168\u5408\u683c\u57df\u540d')),
                ('system', models.CharField(choices=[('0', 'centos7'), ('1', 'centos6.7'), ('2', 'ubuntu12'), ('3', 'server2012'), ('4', 'server2008'), ('5', '\u5176\u4ed6'), ('6', '')], default='6', max_length=30, null=True, verbose_name='\u7cfb\u7edf\u7248\u672c')),
                ('env', models.CharField(choices=[('0', '\u751f\u4ea7'), ('1', '\u9884\u53d1\u5e03'), ('2', '\u6d4b\u8bd5'), ('3', '\u5f00\u53d1')], default='0', max_length=30, verbose_name='\u8fd0\u884c\u73af\u5883')),
                ('cpu', models.CharField(max_length=124, null=True, verbose_name='CPU')),
                ('mem', models.CharField(max_length=124, null=True, verbose_name='\u5185\u5b58')),
                ('disk', models.CharField(max_length=124, null=True, verbose_name='\u786c\u76d8')),
                ('value_file', models.CharField(max_length=124, null=True, verbose_name='\u865a\u62df\u6587\u4ef6')),
                ('run_server', models.CharField(max_length=124, null=True, verbose_name='\u8fd0\u884c\u670d\u52a1')),
                ('user', models.CharField(max_length=30, null=True, verbose_name='\u7ba1\u7406\u7528\u6237')),
                ('pawd', models.CharField(max_length=30, null=True, verbose_name='\u5bc6\u7801')),
                ('created', models.DateField(auto_now_add=True)),
                ('is_del', models.BooleanField(verbose_name=False)),
                ('physical_machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.PhysicalMachine')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.AddField(
            model_name='cabinet',
            name='machine_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.MachineRoom'),
        ),
    ]
