#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, platforms
# from celery_redis_sentinel import register
from django.conf import settings
from ops_api import celeryconfig

print os.getcwd()
# print '3' * 20
platforms.C_FORCE_ROOT = True
os.environ['DJANGO_SETTINGS_MODULE'] = 'ops_api.settings'
# register()

app = Celery('ops_api')
# app.conf.update(
#     CELERY_ACKS_LATE=True,
#     CELERY_ACCEPT_CONTENT=['pickle', 'json'],
#     CELERYD_FORCE_EXECV=True,
#     CELERYD_MAX_TASKS_PER_CHILD=500,
#     BROKER_HEARTBEAT=0,
# )
# app.config_from_object('django.conf:settings')
app.config_from_object(celeryconfig)
# 从所有已注册的app中加载任务模块
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
