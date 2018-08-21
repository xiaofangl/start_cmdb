#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class IpAddress(models.Model):
    ip = models.CharField(u'', max_length=124, default='0.0.0.0')
    # network = models.ForeignKey(NetworkSegment)
    is_del = models.BooleanField(default=False)

    created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-pk']


class MachineRoom(models.Model):
    room_name = models.CharField(u'机房名称', max_length=124, null=False, default=u'北京酒仙桥鹏博士')
    room_bandwidth = models.CharField(u'机房带宽', max_length=124, null=True)
    ip_address = models.CharField(u'IP地址段', max_length=124, null=True)
    isp = models.CharField(u'运营商', max_length=124, null=True)
    contact = models.CharField(u'联系人', max_length=124, null=True)
    contact_phone = models.CharField(u'联系电话', max_length=124, null=True)
    room_address = models.CharField(u'机房地址', max_length=124, null=True)
    room_telephone = models.CharField(u'机房电话', max_length=30, null=True)

    has_cabinet = models.BooleanField(default=True)
    is_del = models.BooleanField(default=False)
    created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-pk']


class NetworkSegment(models.Model):
    start = models.CharField(u'', max_length=124, default='0.0.0.0')
    end = models.CharField(u'', max_length=124, default='0.0.0.0')
    subnet_mask = models.CharField(u'', max_length=124, default='24')
    idc = models.ForeignKey(MachineRoom)
    desc = models.CharField(u'', max_length=256, null=True)

    is_del = models.BooleanField(default=False)
    created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-pk']


class Cabinet(models.Model):
    cabinet = models.CharField(u'机柜', max_length=30, null=True)
    machine_room = models.ForeignKey(MachineRoom)
    is_del = models.BooleanField(default=False)
    created = models.DateField(auto_now=True)


class PhysicalMachine(models.Model):
    MACHINE_TYPE = (
        ('0', u'虚拟机'),
        ('1', u'物理机')
    )
    SYSTEM_CHOICES = (
        ('0', u'centos7'),
        ('1', u'centos6.7'),
        ('2', u'ubuntu12'),
        ('3', u'server2012'),
        ('4', u'server2008'),
        ('5', u'其他'),
        ('6', u''),
    )
    ENVIRONMENT_CHOICES = (
        ('0', u'生产'),
        ('1', u'预发布'),
        ('2', u'测试'),
        ('3', u'开发'),
    )
    RAID_ARRAY_CHOICES = (
        ('1', u'raid0'),
        ('2', u'raid1'),
        ('3', u'raid5'),
        ('4', u'raid10'),
        ('5', u'raid5+热备'),
        ('6', u'other'),
    )
    ip = models.CharField(u'IP', max_length=30, null=False, default='0')
    type = models.CharField(u'类型', max_length=30, choices=MACHINE_TYPE, default='1')
    hostname = models.CharField(u'主机名', max_length=30, null=True)
    fqdn = models.CharField(u'完全合格域名', max_length=45, null=True)
    system = models.CharField(u'系统版本', max_length=30, null=True, choices=SYSTEM_CHOICES, default='6')
    env = models.CharField(u'运行环境', max_length=30, choices=ENVIRONMENT_CHOICES, default='0')
    run_service = models.CharField(u'运行服务', max_length=124, null=True)
    disk_array = models.CharField(u'磁盘阵列', max_length=30, choices=RAID_ARRAY_CHOICES, default='6')
    cpu = models.CharField(u'CPU', max_length=124, null=True)
    mem = models.CharField(u'内存', max_length=124, null=True)
    disk = models.CharField(u'硬盘', max_length=124, null=True)

    brand = models.CharField(u'品牌', max_length=45, null=True)
    machine_model = models.CharField(u'服务器型号', max_length=124, null=True)
    machine_room = models.ForeignKey(MachineRoom)
    cabinet = models.ForeignKey(Cabinet)
    sn = models.CharField(u'SN编号', max_length=30, null=True)
    quick_service = models.CharField(u'快速服务编码', max_length=30, null=True)
    remote_control = models.CharField(u'远控卡号', max_length=30, null=True)
    warranty = models.CharField(u'保修期', max_length=30, null=True)

    user = models.CharField(u'管理用户', max_length=30, null=True)
    pawd = models.CharField(u'密码', max_length=30, null=True)

    created = models.DateField(auto_now=True)
    is_del = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pk']


class ValueMachine(models.Model):
    MACHINE_TYPE = (
        ('0', u'虚拟机'),
        ('1', u'物理机')
    )
    SYSTEM_CHOICES = (
        ('0', u'centos7'),
        ('1', u'centos6.7'),
        ('2', u'ubuntu12'),
        ('3', u'server2012'),
        ('4', u'server2008'),
        ('5', u'其他'),
        ('6', u''),
    )
    ENVIRONMENT_CHOICES = (
        ('0', u'生产'),
        ('1', u'预发布'),
        ('2', u'测试'),
        ('3', u'开发'),
    )

    ip = models.CharField(u'IP', max_length=30, null=False, default='0')
    type = models.CharField(u'类型', max_length=30, choices=MACHINE_TYPE, default='0')
    hostname = models.CharField(u'主机名', max_length=30, null=True)
    fqdn = models.CharField(u'完全合格域名', max_length=45, null=True)
    system = models.CharField(u'系统版本', max_length=30, null=True, choices=SYSTEM_CHOICES, default='6')
    env = models.CharField(u'运行环境', max_length=30, choices=ENVIRONMENT_CHOICES, default='0')
    cpu = models.CharField(u'CPU', max_length=124, null=True)
    mem = models.CharField(u'内存', max_length=124, null=True)
    disk = models.CharField(u'硬盘', max_length=124, null=True)

    physical_machine = models.ForeignKey(PhysicalMachine)
    value_file = models.CharField(u'虚拟文件', max_length=124, null=True)
    run_service = models.CharField(u'运行服务', max_length=124, null=True)

    user = models.CharField(u'管理用户', max_length=30, null=True)
    pawd = models.CharField(u'密码', max_length=30, null=True)

    created = models.DateField(auto_now=True)
    is_del = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pk']


class OperationLog(models.Model):
    LOG_LEVEL = (
        ('0', 'SUCCESS'),
        ('1', 'WANTING'),
        ('2', 'FAILED')
    )
    action = models.CharField(u'', max_length=45, default='')
    status = models.BooleanField(default=False)
    level = models.CharField(u'', max_length=30, default='0', null=True)
    desc = models.CharField(u'', max_length=256, null=True)

    # user = models
    created = models.DateTimeField(auto_now=True)
    is_del = models.BooleanField(default=False)
