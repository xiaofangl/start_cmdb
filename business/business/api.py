#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from views import OperaBusinessLine
from views import OperaProject


@csrf_exempt
def get_business_line(request):
    all = request.GET.get('all', '')
    id = request.GET.get('id', '')
    name = request.GET.get('name', '')

    oper = OperaBusinessLine()
    res = oper._get_info(all, id, name)

    return JsonResponse(res)


@csrf_exempt
def add_business_line(request):
    json_data = json.loads(request.body)
    print json_data

    name = json_data.get('business_name', '')
    manager = json_data.get('business_manage', '')
    contact = json_data.get('manage_contact', '')
    business = json_data.get('business_scope', '')
    desc = json_data.get('business_disc', '')

    oper = OperaBusinessLine()
    res = oper._create_info(name, manager, contact, business, desc)

    return JsonResponse(res)


@csrf_exempt
def mod_business_line(request):
    json_data = json.loads(request.body)
    print json_data
    id = json_data.get('id', '')
    name = json_data.get('name', '')
    manager = json_data.get('manager', '')
    contact = json_data.get('contact', '')
    business = json_data.get('business', '')
    desc = json_data.get('desc', '')

    oper = OperaBusinessLine()
    res = oper._modify_info(id, name, manager, contact, business, desc)
    print res
    return JsonResponse(res)


@csrf_exempt
def del_business_line(request):
    json_data = json.loads(request.body)
    id = json_data.get('id', '')

    oper = OperaBusinessLine()
    res = oper._delete_info(id=id)

    return JsonResponse(res)


"""
    project 
    name=None, business_line=None, language=None, host_type=None, host=None, \
                     develop=None, develop_contact=None, ops_contact=None, desc=None
"""


@csrf_exempt
def add_project(request):
    json_data = json.loads(request.body)
    print json_data

    name = json_data.get('project_name', '')
    business_line = json_data.get('business', '')
    language = json_data.get('language', '')
    host_type = json_data.get('host_type', '')
    host = json_data.get('host', '')
    develop = json_data.get('development', '')
    develop_contact = json_data.get('development_contact', '')
    ops_contact = json_data.get('ops_contact', '')
    desc = json_data.get('project_disc', '')

    oper = OperaProject()
    res = oper._create_item(name, business_line, language, host_type, host, develop, develop_contact, ops_contact, desc)

    return JsonResponse(res)


@csrf_exempt
def init_project(request):
    all = request.GET.get('all', '')
    id = request.GET.get('id', '')
    name = request.GET.get('name', '')
    business_line = request.GET.get('business_line', '')
    print 20 * '+'
    print all, id, name, business_line
    oper = OperaProject()
    res = oper._get_item(all, id, name, business_line)

    return JsonResponse(res)


@csrf_exempt
def mod_project(request):
    json_data = json.loads(request.body)
    print json_data
    id = json_data.get('id', '')
    name = json_data.get('name', '')
    business_line = json_data.get('business_line', '')
    language = json_data.get('language', '')
    host_type = json_data.get('host_type', '')
    phy_host = json_data.get('phy_host', '')
    val_host = json_data.get('val_host', '')
    develop = json_data.get('develop', '')
    develop_contact = json_data.get('develop_contact', '')
    ops_contact = json_data.get('ops_contact', '')
    desc = json_data.get('desc', '')

    print id, name, business_line, language, host_type, phy_host, val_host, develop, develop_contact, ops_contact, desc

    oper = OperaProject()
    res = oper._modify_item(id, name, business_line, language, host_type, phy_host, val_host, develop, develop_contact,
                            ops_contact, desc)

    return JsonResponse(res)


@csrf_exempt
def del_project(request):
    json_data = json.loads(request.body)
    print json_data

    id = json_data.get('id', '')

    opera = OperaProject()
    res = opera._delete_item(id)

    return JsonResponse(res)
