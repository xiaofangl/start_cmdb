#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import sys
from my_ops.ansible.inventory import BaseInventory
from my_ops.ansible.runner import CommandRunner, AdHocRunner
from my_ops.lib.sync_data import readData
from django.http import JsonResponse, HttpResponse


def test_command_runner(data):
    inventory = BaseInventory(data)
    print 'test_command_runner:', inventory
    runner = CommandRunner(inventory)
    print 20 * '8'
    print 'runner:', runner
    res = runner.execute('ls', 'all')
    print res.results_command
    print res.results_raw


def test(request):
    host_data = readData()
    print 20 * 'e'
    print 'host_data:', host_data
    res = test_command_runner(host_data)
    return JsonResponse(res)


# this runner callback is OK
"""
通过setup 收集每台主机的 cpu mem disk信息
"ansible_memtotal_mb", "ansible_processor_vcpus", "ansible_devices"
disk_total = sum([int(data["ansible_devices"][i]["sectors"]) * \
                          int(data["ansible_devices"][i]["sectorsize"]) / 1024 / 1024 / 1024 \
                          for i in data["ansible_devices"] if i[0:2] in ("sd", "ss")])
"""


def test_adhoc_runner(request):
    host_data = readData()
    print host_data
    inventory = BaseInventory(host_data)
    runner = AdHocRunner(inventory)
    # tasks = [
    #     {"action": {"module": "shell", "args": "ls"}, "name": "run_cmd"},
    #     {"action": {"module": "shell", "args": "whoami"}, "name": "run_whoami"},
    # ]
    task_tuple = (('setup', ''),)

    ret = runner.run(task_tuple=task_tuple, pattern='all', play_name='Ansible Ad-hoc')
    print 'this result...'
    print ret
    return JsonResponse(ret)

if __name__ == '__main__':
    # test_command_runner(data='')
    test_adhoc_runner()
