#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.conf.urls import url
from ansible.tests import *
from my_ops.views import get_hardware_info, get_single_hardware

urlpatterns = [
    url(r'test_adhoc_runner/', test_adhoc_runner, name='test_adhoc_runner'),
    url(r'get_hardware_info/', get_hardware_info, name='get_hardware_info'),
    url(r'get_single_hardware/', get_single_hardware, name='get_single_hardware')
]
