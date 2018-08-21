#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.conf.urls import url
from api import *

urlpatterns = [
    url(r'^get_business_line/', get_business_line, name='get_business_line'),
    url(r'^add_business_line/', add_business_line, name='add_business_line'),
    url(r'^mod_business_line/', mod_business_line, name='mod_business_line'),
    url(r'^del_business_line/', del_business_line, name='del_business_line'),

    url(r'^add_project/', add_project, name='add_project'),
    url(r'^init_project/', init_project, name='init_project'),
    url(r'^mod_project/', mod_project, name='mod_project'),
    url(r'^del_project/', del_project, name='del_project')
]