#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from views import ServerTree
from views import HomeChart
from views import ToDoList


@csrf_exempt
def init_tree(request):
    business_line = request.GET.get('business_line', '')
    init = request.GET.get('init', '')
    all = request.GET.get('all', '')
    # business_line = '3' if not business_line else business_line

    opera = ServerTree()
    res = opera._get_tree(all=all, init=init, business_line=business_line)
    # print res
    return JsonResponse(res)


@csrf_exempt
def init_chart(request):
    init = request.GET.get('init', '')

    print init
    opera = HomeChart()
    res = opera._get_info(init)

    return JsonResponse(res)


@csrf_exempt
def init_do_list(request):
    opera = ToDoList()
    res = opera._get_info()
    print res
    return JsonResponse(res)


@csrf_exempt
def add_do_list(request):
    print request.body
    json_data = request.body

    opera = ToDoList()
    res = opera._add_info(json_data)

    return JsonResponse(res)


@csrf_exempt
def mod_do_list(request):
    print request.body
    json_data = request.body

    opera = ToDoList()
    res = opera._mod_info(json_data)

    return JsonResponse(res)
