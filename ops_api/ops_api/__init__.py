#coding=utf-8


from __future__ import absolute_import, unicode_literals

# 这将保证celery app总能在django应用启动时启动
# from .celery import app as celery_app
from ops_api.celery import app as celery_app