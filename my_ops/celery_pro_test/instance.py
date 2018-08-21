#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery_redis_sentinel import register
from django.conf import settings

print os.getcwd()
# print '3' * 20
os.environ['DJANGO_SETTINGS_MODULE'] = '.ops_api.settings'
register()
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ops_api.settings.settings')

app = Celery('celery_pro_test')
print '1' * 20

# app.config_from_object('celery_pro_test.celeryconfig')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
print '2' * 20


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
print '3' * 20
