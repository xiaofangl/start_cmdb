#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.conf.urls import url
from api import *

urlpatterns = [
    url(r'^add_machine_room/', add_machine_room, name='add_machine_room'),
    url(r'^get_item/', get_item, name='get_item'),
    url(r'^modify_item/', mod_machine_room, name='mod_machine_room'),
    url(r'^delete_item/?', del_machine_room, name='del_machine_room'),

    url(r'^init_machine/', init_machine, name='init_machine'),
    url(r'^init_machine_room/', init_machine_room, name='init_machine_room'),
    url(r'^init_physical_machine/', init_physical_machine, name='init_physical_machine'),
    url(r'^init_machine_room_cabinet/', init_machine_room_cabinet, name='init_machine_room_cabinet'),

    url(r'^add_physical_machine/', add_physical_machine, name='add_physical_machine'),
    url(r'^modify_phy_machine/', modify_phy_machine, name='modify_phy_machine'),
    url(r'^add_value_machine/', add_value_machine, name='add_value_machine'),
    url(r'^modify_val_machine/', modify_val_machine, name='modify_val_machine'),


    url(r'^del_machine/', del_machine, name='del_machine'),

    url(r'^add_network_segment/', add_network_segment, name='add_network_segment'),
    url(r'^init_network_segment/', init_network_segment, name='init_network_segment'),
    url(r'^mod_network_segment/', mod_network_segment, name='mod_network_segment'),
    url(r'^del_network_segment/', del_network_segment, name='del_network_segment')
]
