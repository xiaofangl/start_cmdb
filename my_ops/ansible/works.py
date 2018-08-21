#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.http import JsonResponse
from my_ops.lib.sync_data import readData
from my_ops.ansible.inventory import BaseInventory
from my_ops.ansible.runner import AdHocRunner
from my_ops.ansible.callback import AdHocResultCallback
from my_ops.ansible.runner import CommandRunner


def run_setup(host_data=None, task_tuple=None, pattern=None, play_name=None):

    host_data = readData() if not host_data else host_data
    pattern = 'all' if not pattern else pattern
    play_name = 'Ansible Ad-hoc' if not play_name else play_name
    task_tuple = (('setup', ''),) if not task_tuple else task_tuple
        # host_data = _host_data if not host_data else host_data

    print 'task' * 20
    # print host_data

    inventory = BaseInventory(host_data)
    runner = AdHocRunner(inventory)
    # runner.results_callback = AdHocResultCallback()
    # task_tuple = (('setup', ''),)

    ret = runner.run(task_tuple=task_tuple, pattern=pattern, play_name=play_name)
    print '_' * 20
    # print ret

    # return JsonResponse(ret)
    return ret