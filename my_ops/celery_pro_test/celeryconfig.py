#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
BROKER_URL = 'redis-sentinel://redis-sentinel:6401/0'
BROKER_TRANSPORT_OPTIONS = {
    'sentinels': [('192.168.99.37', 6402),
                  ('192.168.99.39', 6403),
                  ('192.168.99.43', 6401)],
    'service_name': 'sentinel-192.168.99.43-6400',
    'socket_timeout': 0.1,
}

CELERY_RESULT_BACKEND = 'redis-sentinel://redis-sentinel:6401/1'
CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = BROKER_TRANSPORT_OPTIONS

# CELERYBEAT_SCHEDULE = {
#     'add-everyday-run': {
#         'task': '',
#         'schedule': crontab(hour=24, minute=30, day_of_week=all),
#         'args': ''
#     }
# }

from datetime import timedelta


CELERYBEAT_SCHEDULE = {
    'add-every-3-seconds': {
        'task': 'appdemo.tasks.test_celery',
        # 'schedule': crontab(minute=u'40', hour=u'17',),
        'schedule': timedelta(seconds=3),
        'args': (16, 16)
    },
}


