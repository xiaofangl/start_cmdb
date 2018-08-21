#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from assets.models import PhysicalMachine, ValueMachine
from django.http import JsonResponse
import time
import sys
import os

from my_ops.ansible.inventory import BaseInventory
from django.conf import settings

"""
host_data:  {
                   "hostname": "",
                   "ip": "",
                   "port": "",
                   # behind is not must be required
                   "username": "",
                   "password": "",
                   "private_key": "",
                   "become": {
                       "method": "",
                       "user": "",
                       "pass": "",
                   }
                   "groups": [],
                   "vars": {},
               }
"""


def readData():
    _phy_ip = PhysicalMachine.objects.filter(is_del=False).values('ip')
    total_host = []
    for i in _phy_ip:
        i['port'] = settings.ANSIBLE_CONN.get('port')
        i['username'] = settings.ANSIBLE_CONN.get('username')
        i['password'] = settings.ANSIBLE_CONN.get('password')
        i['private_key'] = settings.ANSIBLE_CONN.get('private_key')
        i['become'] = {
            "method": settings.ANSIBLE_CONN.get('method'),
            "user": settings.ANSIBLE_CONN.get('user'),
            "pass": settings.ANSIBLE_CONN.get('pass'),
        }
        i['groups'] = settings.ANSIBLE_CONN.get('groups')
        i['vars'] = settings.ANSIBLE_CONN.get('vars')
        total_host.append(i)
    _val_ip = ValueMachine.objects.filter(is_del=False).values('ip')
    for c in _val_ip:
        c['port'] = settings.ANSIBLE_CONN.get('port')
        c['username'] = settings.ANSIBLE_CONN.get('username')
        c['password'] = settings.ANSIBLE_CONN.get('password')
        c['private_key'] = settings.ANSIBLE_CONN.get('private_key')
        c['become'] = {
            "method": settings.ANSIBLE_CONN.get('method'),
            "user": settings.ANSIBLE_CONN.get('user'),
            "pass": settings.ANSIBLE_CONN.get('pass'),
        }
        c['groups'] = settings.ANSIBLE_CONN.get('groups')
        c['vars'] = settings.ANSIBLE_CONN.get('vars')
        total_host.append(c)

    # print 'all_host', total_host
    # res = {'data': total_host}
    # inventory = BaseInventory(host_list=total_host)
    # print 'host', 20 * '#'
    # for host in inventory.hosts:
    #     print host
    # return JsonResponse(res)
    # print 'total_host', total_host
    return total_host


if __name__ == '__main__':
    res = readData()
