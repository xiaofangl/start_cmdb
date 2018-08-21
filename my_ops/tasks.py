#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
import time
from ops_api.celery import app
from my_ops.ansible.works import run_setup
from my_ops.lib.process_data import ProcessData
from my_ops.models import OperationLog
# from django.conf import settings


@app.task
def test_celery(x, y):
    logger = get_task_logger(__name__)
    logger.info('func start  ----------------->')
    logger.info('application:%s', "TEST_APP")
    logger.info('func end -------------------->')
    return x + y


@app.task
def run_ansible_setup(host_data=None, task_tuple=None, pattern=None, play_name=None):
    print 'this run_ansible_setup...'
    ret = run_setup()
    return ret


@app.task
def single_host_setup(host_data=None, task_tuple=None, pattern=None, play_name=None):
    """

    :param host_data: [{
            "hostname": "",
            "ip": "",
            "port": "",
            "username": "",
            "password": "",
            "private_key": "",
            "become": {
                "method": "",
                "user": "",
                "pass": "",
            },
            "groups": [],
            "vars": {},
          },
        ]
    :param task_tuple:
    :param pattern:
    :param play_name:
    :return:
    """
    task_tuple = (('setup', ''),) if not task_tuple else task_tuple
    pattern = 'all' if not pattern else pattern
    play_name = 'Ansible Ad-hoc' if not play_name else play_name
    ret = run_setup(host_data=host_data, task_tuple=task_tuple, pattern=pattern, play_name=play_name)

    return ret


@app.task
def schedule_hardware_info(host_data=None, task_tuple=None, pattern=None, play_name=None):
    # 运行ansible task
    data = run_ansible_setup.delay()

    # print 'data', data.get('contacted'), data.id, data.status
    key = data.id
    # key = 'celery-task-meta-b457e287-d085-452f-bf51-c3759e4aba14'
    if data.status and key and data.get('contacted'):
        # if key:
        key = "celery-task-meta-" + str(data.id)
        # print 'key', key
        _proc = ProcessData(key)
        ret = _proc._insert_db()
        # print ret
        OperationLog.objects.create(action='schedule_hardware_info', status=True, desc=ret)
    else:
        OperationLog.objects.create(action='schedule_hardware_info', desc=data, level='2')