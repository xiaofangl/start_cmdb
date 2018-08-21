#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from __future__ import absolute_import, unicode_literals

from celery.schedules import crontab
from kombu import Exchange, Queue
from celery import platforms

platforms.C_FORCE_ROOT = True
print 'this celeryconfig....'

"""
    celery broker and backend use Redis-sentinel
"""
REDIS_SERVER = '192.168.99.43'
REDIS_PORT = 6400
REDIS_DB = 1
BROKER_URL = 'redis://192.168.99.43:6400/0'
CELERY_RESULT_BACKEND = 'redis://192.168.99.43:6400/1'

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# celery时区设置，使用settings中TIME_ZONE同样的时区
CELERY_TIMEZONE = 'Asia/Shanghai'
# BROKER_URL = 'redis-sentinel://redis-sentinel:6401/0'
# BROKER_TRANSPORT_OPTIONS = {
#     'sentinels': [('192.168.99.37', 6402),
#                   ('192.168.99.39', 6403),
#                   ('192.168.99.43', 6401)],
#     'service_name': 'sentinel-192.168.99.43-6400',
#     'socket_timeout': 0.1,
# }
#
# CELERY_RESULT_BACKEND = 'redis-sentinel://redis-sentinel:6401/1'
# CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = BROKER_TRANSPORT_OPTIONS

# CELERYBEAT_SCHEDULE = {
#     'add-everyday-run': {
#         'task': '',
#         'schedule': crontab(hour=24, minute=30, day_of_week=all),
#         'args': ''
#     }
# }


"""
    celery beat 
    celery schedule application 
"""
from datetime import timedelta

# 每天的凌晨12:30分，执行任务

CELERYBEAT_SCHEDULE = {
    'add-every-3-seconds': {
        'task': 'my_ops.tasks.schedule_hardware_info',
        'schedule': crontab(minute=30, hour=0),
        # 'schedule': timedelta(seconds=3),
        'args': ()
    },
}
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # 数据库调度
"""
    celery manage queue
"""
# CELERY_QUEUES = (
#     Queue("default", Exchange("default"), routing_key="default"),
#     Queue("for_task_A", Exchange("for_task_A"), routing_key="for_task_A"),
#     Queue("for_task_B", Exchange("for_task_B"), routing_key="for_task_B")
# )
#
# CELERY_ROUTES = {
#     'tasks.taskA': {"queue": "for_task_A", "routing_key": "for_task_A"},
#     'tasks.taskB': {"queue": "for_task_B", "routing_key": "for_task_B"}
# }
