#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from __future__ import unicode_literals

from django.db import models


# Create your models here.

class ToDoList(models.Model):
    # user =
    title = models.CharField(u'', max_length=256, default='welcome come...')
    is_del = models.BooleanField(default=False)

    created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-pk']