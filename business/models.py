#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from __future__ import unicode_literals

from django.db import models
from assets.models import PhysicalMachine
from assets.models import ValueMachine


# Create your models here.

class BusinessLine(models.Model):
    name = models.CharField(u'业务线名', max_length=30, null=False, default='test')
    manager = models.CharField(u'业务对接人', max_length=30, null=True, default='shawna')
    contact = models.CharField(u'联系方式', max_length=30, null=True)
    business = models.CharField(u'业务范围', max_length=45, null=True)
    desc = models.CharField(u'描述', max_length=256, null=True)

    is_del = models.BooleanField(default=False)
    created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-pk']


class Project(models.Model):

    CHOICES_LANGUAGE = (
        ('0', u'Java'),
        ('1', u'Python'),
        ('2', u'Other'),
        ('3', u'PhP'),
    )

    name = models.CharField(u'项目名', max_length=30, default='web', null=False)
    business_line = models.ForeignKey(BusinessLine)
    language = models.CharField(u'语言', choices=CHOICES_LANGUAGE, max_length=30, default='1')

    physical_machine = models.ManyToManyField(PhysicalMachine)
    value_machine = models.ManyToManyField(ValueMachine)

    develop = models.CharField(u'开发人员', max_length=45, null=True)
    develop_contact = models.CharField(u'开发联系方式', max_length=45, null=True)

    ops_contact = models.CharField(u'运维联系方式', max_length=45, null=True)
    desc = models.CharField(u'描述', max_length=256, null=True)

    is_del = models.BooleanField(default=False)
    created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-pk']


class BusinessLog(models.Model):
    action = models.CharField(u'', max_length=45, default='')
    status = models.BooleanField(default=False)
    level = models.CharField(u'', max_length=30, default='0', null=True)
    desc = models.CharField(u'', max_length=256, null=True)

    # user = models
    created = models.DateTimeField(auto_now=True)
    is_del = models.BooleanField(default=False)