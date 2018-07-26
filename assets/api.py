#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from views import OperaMachineRoom
from views import MachineInit
from views import OperaMachine
from views import OperaNetworkSegment


@csrf_exempt
def get_item(request):
    if request.method == 'GET':
        all = request.GET.get('all', '')
        id = request.GET.get('id', '')
        isp = request.GET.get('isp', '')
        room_name = request.GET.get('room_name', '')

        print all, id, room_name, isp
        oper = OperaMachineRoom()
        res = oper._get_info(all, id, room_name, isp)
    # print res
    return JsonResponse(res)


@csrf_exempt
def add_machine_room(request):
    json_data = json.loads(request.body)
    room_name = json_data.get('room_name', '')
    room_bandwidth = json_data.get('room_bandwidth', '')
    ip_address = json_data.get('ip_address', '')
    isp = json_data.get('isp', '')
    contact = json_data.get('contact', '')
    contact_phone = json_data.get('contact_phone', '')
    room_address = json_data.get('room_address', '')
    room_telephone = json_data.get('room_telephone', '')
    cabinet = json_data.get('cabinet', '')
    print room_name, room_bandwidth, 'ip_address', ip_address, isp, contact, contact_phone, room_address, room_telephone, cabinet
    oper = OperaMachineRoom()
    res = oper._create_info(room_name=room_name, room_bandwidth=room_bandwidth, ip_address=ip_address, isp=isp,
                            contact=contact,
                            contact_phone=contact_phone, room_address=room_address, room_telephone=room_telephone,
                            cabinet=cabinet)

    return JsonResponse(res)


@csrf_exempt
def mod_machine_room(request):
    json_data = json.loads(request.body)
    room_name = json_data.get('room_name', '')
    room_bandwidth = json_data.get('room_bandwidth', '')
    ip_address = json_data.get('ip_address', '')
    isp = json_data.get('isp', '')
    contact = json_data.get('contact', '')
    contact_phone = json_data.get('contact_phone', '')
    room_address = json_data.get('room_address', '')
    room_telephone = json_data.get('room_telephone', '')
    cabinet = json_data.get('cabinet', '')
    id = json_data.get('id', '')
    if type(cabinet) == list:
        cabinet = ','.join(cabinet)
    print id, room_name, room_bandwidth, ip_address, isp, contact, contact_phone, room_address, room_telephone, cabinet
    oper = OperaMachineRoom()
    res = oper._modify_info(id, room_name, room_bandwidth, ip_address, isp, contact, contact_phone, room_address,
                            room_telephone, cabinet)
    print res
    return JsonResponse(res)


@csrf_exempt
def del_machine_room(request):
    json_data = json.loads(request.body)
    print json_data, type(json_data)

    oper = OperaMachineRoom()
    res = oper._delete_info(json_data)
    print res
    return JsonResponse(res)


"""all=False, type=None, id=None, env=None, system=None"""


@csrf_exempt
def init_machine(request):
    all = request.GET.get('all', '')
    id = request.GET.get('id', '')
    type = request.GET.get('type', '')
    env = request.GET.get('env', '')
    system = request.GET.get('system', '')
    ip = request.GET.get('ip', 'ip')
    print all, type, id, env, system
    oper = OperaMachine()
    res = oper._get_info(all, type, id, env, system, ip)
    print 20 * '*'
    print res
    return JsonResponse(res)


@csrf_exempt
def init_machine_room(request):
    machine_init = MachineInit()
    res = machine_init._get_machine_room()
    print 20 * '-'
    print res
    return JsonResponse(res)


@csrf_exempt
def init_machine_room_cabinet(request):
    print 20 * '+'
    machine_room_id = request.GET.get('0', '')
    print machine_room_id
    machine_init = MachineInit()
    res = machine_init._get_machine_room_cabinet(machine_room_id)
    print res

    return JsonResponse(res)


@csrf_exempt
def init_physical_machine(request):
    oper = MachineInit()
    res = oper.get_physical_machine()
    print res

    return JsonResponse(res)


@csrf_exempt
def add_physical_machine(request):
    json_data = json.loads(request.body)
    print json_data
    ip = json_data.get('ip', '')
    hostname = json_data.get('hostname', '')
    fqdn = json_data.get('fqdn', '')
    system = json_data.get('system', '')
    env = json_data.get('env', '')
    brand = json_data.get('brand', '')
    server_model = json_data.get('server_model', '')
    machine_room = json_data.get('machine_room', '')
    cabinet = json_data.get('cabinet', '')
    disk_array = json_data.get('disk_array', '')
    sn = json_data.get('sn', '')
    quick_service = json_data.get('quick_service', '')
    warranty = json_data.get('warranty', '')
    remote_control = json_data.get('remote_control', '')
    user = json_data.get('user', '')
    pawd = json_data.get('pawd', '')
    cpu = json_data.get('cpu', '')
    mem = json_data.get('mem', '')
    disk = json_data.get('disk', '')
    run_service = json_data.get('run_service', '')

    # print ip, hostname, fqdn, system, env, brand, server_model, machine_room, cabinet, disk_array, sn, quick_service, warranty, remote_control, user, pawd, cpu, mem, disk, run_service
    oper = OperaMachine()
    res = oper._create_physical(ip, hostname, fqdn, system, env, brand, server_model, machine_room, cabinet, disk_array,
                                sn, quick_service, warranty, remote_control, user, pawd, cpu, mem, disk, run_service)

    return JsonResponse(res)


@csrf_exempt
def add_value_machine(request):
    json_data = json.loads(request.body)
    print json_data
    ip = json_data.get('ip', '')
    hostname = json_data.get('hostname', '')
    fqdn = json_data.get('fqdn', '')
    system = json_data.get('system', '')
    env = json_data.get('env', '')
    value_file = json_data.get('value_file', '')
    physical_machine = json_data.get('physical_machine', '')
    run_service = json_data.get('run_service', '')
    user = json_data.get('user', '')
    pawd = json_data.get('pawd', '')
    cpu = json_data.get('cpu', '')
    mem = json_data.get('mem', '')
    disk = json_data.get('disk', '')

    oper = OperaMachine()
    res = oper._create_value(ip, hostname, fqdn, system, env, value_file, physical_machine, run_service, user, pawd,
                             cpu, mem, disk)
    return JsonResponse(res)


@csrf_exempt
def modify_phy_machine(request):
    json_data = json.loads(request.body)
    print json_data
    id = json_data.get('id', '')
    ip = json_data.get('ip', '')
    hostname = json_data.get('hostname', '')
    fqdn = json_data.get('fqdn', '')
    system = json_data.get('system', '')
    env = json_data.get('env', '')
    brand = json_data.get('brand', '')
    server_model = json_data.get('server_model', '')
    machine_room = json_data.get('machine_room', '')
    cabinet = json_data.get('cabinet', '')
    disk_array = json_data.get('disk_array', '')
    sn = json_data.get('sn', '')
    quick_service = json_data.get('quick_service', '')
    warranty = json_data.get('warranty', '')
    remote_control = json_data.get('remote_control', '')
    user = json_data.get('user', '')
    pawd = json_data.get('pawd', '')
    cpu = json_data.get('cpu', '')
    mem = json_data.get('mem', '')
    disk = json_data.get('disk', '')
    run_service = json_data.get('run_service', '')

    oper = OperaMachine()
    res = oper._modify_physical(id, ip, hostname, fqdn, system, env, brand, server_model, machine_room, cabinet,
                                disk_array,
                                sn, quick_service, warranty, remote_control, user, pawd, cpu, mem, disk, run_service)

    return JsonResponse(res)


@csrf_exempt
def modify_val_machine(request):
    json_data = json.loads(request.body)
    print json_data
    id = json_data.get('id', '')
    ip = json_data.get('ip', '')
    hostname = json_data.get('hostname', '')
    fqdn = json_data.get('fqdn', '')
    system = json_data.get('system', '')
    env = json_data.get('env', '')
    value_file = json_data.get('value_file', '')
    physical_machine = json_data.get('physical_machine', '')
    run_service = json_data.get('run_service', '')
    user = json_data.get('user', '')
    pawd = json_data.get('pawd', '')
    cpu = json_data.get('cpu', '')
    mem = json_data.get('mem', '')
    disk = json_data.get('disk', '')

    oper = OperaMachine()
    res = oper._modify_value(id, ip, hostname, fqdn, system, env, value_file, physical_machine, run_service, user, pawd,
                             cpu, mem, disk)
    return JsonResponse(res)


@csrf_exempt
def del_machine(request):
    json_data = json.loads(request.body)
    print json_data
    type = json_data.get('type', '')
    id = json_data.get('id', '')
    all = json_data.get('all', '')
    oper = OperaMachine()
    res = oper._delete_machine(all, id, type)
    print res
    return JsonResponse(res)


@csrf_exempt
def add_network_segment(request):
    json_data = json.loads(request.body)
    start = json_data.get('start', '')
    end = json_data.get('end', '')
    subnet_mask = json_data.get('subnet_mask', '')
    desc = json_data.get('desc', '')
    idc = json_data.get('idc', '')

    print json_data
    # start=None, end=None, subnet_mask=None, desc=None, idc=None

    opera = OperaNetworkSegment()
    res = opera._add_item(start, end, subnet_mask, desc, idc)

    return JsonResponse(res)


@csrf_exempt
def init_network_segment(request):
    all = request.GET.get('all', '')
    id = request.GET.get('id', '')

    opera = OperaNetworkSegment()
    res = opera._get_item(all, id)

    return JsonResponse(res)


@csrf_exempt
def mod_network_segment(request):
    json_data = json.loads(request.body)
    id = json_data.get('id', '')
    start = json_data.get('start', '')
    end = json_data.get('end', '')
    subnet_mask = json_data.get('subnet_mask', '')
    desc = json_data.get('desc', '')
    idc = json_data.get('idc', '')

    print json_data
    opera = OperaNetworkSegment()
    res = opera._mod_item(id, start, end, subnet_mask, desc, idc)

    return JsonResponse(res)


@csrf_exempt
def del_network_segment(request):
    json_data = json.loads(request.body)
    id = json_data.get('id', '')

    opera = OperaNetworkSegment()
    res = opera._del_item(id)

    return JsonResponse(res)