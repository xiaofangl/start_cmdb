#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.conf.urls import url
from api import *

urlpatterns = [
    url(r'^init_tree/', init_tree, name='init_tree'),
    url(r'^init_chart/', init_chart, name='init_chart'),
    url(r'^init_do_list/', init_do_list, name='init_do_list'),
    url(r'^add_do_list/', add_do_list, name='add_do_list'),
    url(r'^mod_do_list/', mod_do_list, name='mod_do_list')
]