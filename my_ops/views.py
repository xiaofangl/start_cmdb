#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from lib.process_data import ProcessData
from tasks import run_ansible_setup
from tasks import single_host_setup
from django.conf import settings

# Create your views here.
"""
    执行 ansible_setup task;
    获取 ansible_setup task 的result;
    将result写入MySQL；
    host_data=None, task_tuple=None, pattern=None, play_name=None
"""


# from multiprocessing import process

def get_hardware_info(request):
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
        return JsonResponse(ret)
    else:
        ret = dict(status=False, msg=data)
        return JsonResponse(ret)


def get_single_hardware(request):
    # host_data = [{
    #     "ip": "172.16.1.50",
    #     "port": 22,
    #     "username": "root",
    #     "password": "",
    #     "private_key": "/Users/xiaofangl/tmp/id_rsa.ansible",
    #     "become": {
    #         "method": "sudo",
    #         "user": "root",
    #         "pass": "",
    #     },
    #     "groups": ['all'],
    #     "vars": {},
    # },
    # ]
    id = request.GET.get('id', '')
    type = request.GET.get('type', '')
    print 'get: ', id, type
    _reco = ProcessData._get_host_ip(id, type)
    #print 'ip: ', _reco
    if _reco:
        host_data = [{
            "ip": str(_reco),
            "port": settings.ANSIBLE_CONN.get('port'),
            "username": settings.ANSIBLE_CONN.get('username'),
            "password": settings.ANSIBLE_CONN.get('password'),
            "private_key": settings.ANSIBLE_CONN.get('private_key'),
            "become": {
                "method": settings.ANSIBLE_CONN.get('method'),
                "user": settings.ANSIBLE_CONN.get('user'),
                "pass": settings.ANSIBLE_CONN.get('pass'),
            },
            "groups": settings.ANSIBLE_CONN.get('groups'),
            "vars": settings.ANSIBLE_CONN.get('vars'),
        }]
        if host_data:
            #print 'host_data', host_data
            data = single_host_setup.delay(host_data=host_data)

            # #print 'data', data.get(), data.id, data.status
            key = data.id
            # key = 'celery-task-meta-b457e287-d085-452f-bf51-c3759e4aba14'
            if data.status and key and data.get('contacted'):
                # if key:
                key = "celery-task-meta-" + str(data.id)
                # #print 'key', key
                _proc = ProcessData(key)
                ret = _proc._insert_db()

                return JsonResponse(ret)
            else:
                ret = dict(status=False, msg=data)
                return JsonResponse(ret)
    else:
        ret = dict(status=False, msg=_reco)
        return JsonResponse(ret)