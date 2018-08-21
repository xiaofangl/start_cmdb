#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
from django.shortcuts import render
from models import MachineRoom
from models import Cabinet
from models import PhysicalMachine
from models import ValueMachine
from models import OperationLog
from models import IpAddress
from models import NetworkSegment
from utils.pag import paging


# Create your views here.

class OperaMachineRoom(object):
    def __init__(self):
        self.res = {
            'msg': '',
            'status': True
        }

    def _get_info(self, all=False, id=None, room_name=None, isp=None):
        if all:
            machine_list = []
            try:
                all_machine = MachineRoom.objects.filter(is_del=False).values('id', 'room_name', 'room_bandwidth',
                                                                              'ip_address', 'room_telephone',
                                                                              'contact_phone', \
                                                                              'isp', 'contact', 'room_address',
                                                                              'created')
                for item in all_machine:
                    machine_list.append(item)

                self.res['data'] = machine_list
                # #print machine_list
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
        elif id:
            try:
                _detail_info = []
                detailed = MachineRoom.objects.filter(is_del=False, id=id).values('id', 'room_name', 'room_bandwidth',
                                                                                  'ip_address', 'room_telephone', \
                                                                                  'isp', 'contact', 'room_address',
                                                                                  'contact_phone',
                                                                                  'created')
                machine = MachineRoom.objects.get(is_del=False, id=id)
                # #print machine
                cabinet = machine.cabinet_set.filter(machine_room_id=id, is_del=False)
                _cabinet_list = []
                for i in cabinet:
                    # print i.cabinet, i.machine_room_id
                    _cabinet_list.append(i.cabinet)
                # #print 'cabinet', cabinet
                for item in detailed:
                    item['cabinet'] = _cabinet_list
                    _detail_info.append(item)
                self.res['data'] = _detail_info
                # #print self.res['data']
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e

        elif room_name:
            try:
                _detail_info = []
                detailed = MachineRoom.objects.filter(is_del=False, room_name=room_name).values('id', 'room_name',
                                                                                                'room_bandwidth',
                                                                                                'ip_address',
                                                                                                'room_telephone',
                                                                                                'contact_phone', \
                                                                                                'isp', 'contact',
                                                                                                'room_address',
                                                                                                'created')
                for item in detailed:
                    _detail_info.append(item)
                self.res['data'] = _detail_info
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
        elif isp:
            try:
                _detail_info = []
                detailed = MachineRoom.objects.filter(is_del=False, isp=isp).values('id', 'room_name', 'room_bandwidth',
                                                                                    'ip_address', 'room_telephone',
                                                                                    'contact_phone', \
                                                                                    'isp', 'contact', 'room_address',
                                                                                    'created')
                for item in detailed:
                    _detail_info.append(item)
                self.res['data'] = _detail_info
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
        OperationLog.objects.create(action='OperaMachineRoom._create_info', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res

    def _create_info(self, room_name='', room_bandwidth='', ip_address='', isp='', contact='',
                     contact_phone='', room_address='', room_telephone='', cabinet=''):
        try:
            if cabinet:
                MachineRoom.objects.create(room_name=room_name, room_bandwidth=room_bandwidth,
                                           ip_address=ip_address, isp=isp, contact=contact,
                                           contact_phone=contact_phone, \
                                           room_address=room_address, room_telephone=room_telephone)
                if ',' in cabinet:
                    _cabinet_list = cabinet.split(',')
                    for i in _cabinet_list:
                        if i:
                            try:
                                Cabinet.objects.create(cabinet=i, machine_room=MachineRoom.objects.get(is_del=False, \
                                                                                                       room_name=room_name))
                            except Exception as e:
                                self.res['status'] = False
                                self.res['msg'] = e

                else:
                    cabinet = cabinet.strip()
                    try:
                        Cabinet.objects.create(cabinet=cabinet, machine_room=MachineRoom.objects.get(is_del=False, \
                                                                                                     room_name=room_name))
                    except Exception as e:
                        self.res['status'] = False
                        self.res['msg'] = e
            else:
                MachineRoom.objects.create(room_name=room_name, room_bandwidth=room_bandwidth,
                                           ip_address=ip_address, isp=isp, contact=contact,
                                           contact_phone=contact_phone, \
                                           room_address=room_address, room_telephone=room_telephone, has_cabinet=False)

                self.res['msg'] = room_name
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        OperationLog.objects.create(action='OperaMachineRoom._create_info', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res

    def _modify_info(self, id, room_name, room_bandwidth, ip_address, isp, contact,
                     contact_phone, room_address, room_telephone, cabinet):
        # print id, room_name, room_bandwidth, ip_address, isp, contact, contact_phone, room_address, room_telephone, cabinet

        try:
            # print '_machine_room'
            # cabinet = str(cabinet)
            # Cabinet.objects.filter(ma=id).update(is_del=True)
            # Cabinet.objects.filter(machine_room=id).update(is_del=True)
            if cabinet:
                _machine_room = MachineRoom(is_del=False, id=id)
                _machine_room.room_name = room_name
                _machine_room.room_bandwidth = room_bandwidth
                _machine_room.ip_address = ip_address
                _machine_room.isp = isp
                _machine_room.contact = contact
                _machine_room.contact_phone = contact_phone
                _machine_room.room_address = room_address
                _machine_room.room_telephone = room_telephone
                _machine_room.has_cabinet = True
                _machine_room.save()
                if ',' in cabinet:
                    # print 20 * '_', type(cabinet), cabinet
                    _cabinet_list = cabinet.split(',')
                    # print '_cabinet_list', _cabinet_list
                    cabinets_list = []
                    cabinets = Cabinet.objects.filter(is_del=False, machine_room=id).values('cabinet')
                    for s in cabinets:
                        # print s.get('cabinet')
                        cabinets_list.append(s.get('cabinet'))
                    # print 'cabinets_list', cabinets_list

                    for i in _cabinet_list:
                        # print i, _cabinet_list

                        if i and i not in cabinets_list:
                            # print i
                            try:
                                Cabinet.objects.create(cabinet=i,
                                                       machine_room=MachineRoom.objects.get(is_del=False, id=id))
                            except Exception as e:
                                self.res['status'] = False
                                self.res['msg'] = e
                                # elif i and i in cabinets_list:
                                #     Cabinet.objects.filter(cabinet=i).update(is_del=True)
                    for cc in cabinets_list:
                        # print 'cc', cc, _cabinet_list
                        if cc and cc not in _cabinet_list:
                            Cabinet.objects.filter(cabinet=cc).update(is_del=True)
                else:
                    # print 'cabinet', cabinet
                    # cabinet = cabinet.strip()
                    try:
                        Cabinet.objects.create(cabinet=cabinet,
                                               machine_room=MachineRoom.objects.get(is_del=False, id=id))
                        # print 20 * '+'
                    except Exception as e:
                        self.res['status'] = False
                        self.res['msg'] = e
            else:

                _machine_room = MachineRoom(is_del=False, id=id)
                _machine_room.room_name = room_name
                _machine_room.room_bandwidth = room_bandwidth
                _machine_room.ip_address = ip_address
                _machine_room.isp = isp
                _machine_room.contact = contact
                _machine_room.contact_phone = contact_phone
                _machine_room.room_address = room_address
                _machine_room.room_telephone = room_telephone
                _machine_room.has_cabinet = False
                _machine_room.save()

                Cabinet.objects.filter(machine_room=id).update(is_del=True)
            self.res['msg'] = room_name
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        # print self.res
        OperationLog.objects.create(action='OperaMachineRoom._modify_info', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res

    def _delete_info(self, id=''):
        try:
            MachineRoom.objects.filter(is_del=False, id=id).update(is_del=True)
            Cabinet.objects.filter(machine_room=id).update(is_del=True)
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        OperationLog.objects.create(action='OperaMachineRoom._create_info', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res


class OperaMachine(object):
    def __init__(self):
        self.res = {
            'msg': '',
            'status': True
        }

    def _get_info(self, all=False, type=None, id=None, env=None, system=None, ip=None, phy_page=1, val_page=1):
        if all and not type:
            _machine_list = []
            try:
                _phy_machine = PhysicalMachine.objects.filter(is_del=False).values('id', 'ip', 'type', 'env', 'system',
                                                                                   'cpu', 'hostname',
                                                                                   'mem', 'disk', 'run_service',
                                                                                   'brand', 'machine_model', 'warranty',
                                                                                   'disk_array',
                                                                                   'created')

                for _item in _phy_machine:
                    _machine_list.append(_item)

                phy_count, phy_list = paging(_machine_list, phy_page)
                self.res['phy_data'] = phy_list
                self.res['phy_count'] = phy_count
                # self.res['phy_data'] = _machine_list
                # print '_phy_machine', self.res['phy_data']
                _val_machine = ValueMachine.objects.filter(is_del=False).values('id', 'ip', 'type', 'env', 'system',
                                                                                'cpu',
                                                                                'mem', 'disk', 'run_service', 'user',
                                                                                'hostname',
                                                                                'value_file',
                                                                                'created')
                _machine_list = []
                for _item in _val_machine:
                    _machine_list.append(_item)

                val_count, val_list = paging(_machine_list, val_page)
                self.res['val_count'] = val_count
                self.res['val_data'] = val_list
                # print '_val_machine', self.res['val_data']
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
            OperationLog.objects.create(action='OperaMachine._get_info', status=self.res['status'],
                                        desc=self.res['msg'])
            return self.res

        elif not all and type == '1':
            if id:
                try:
                    details = []
                    _physical_info = PhysicalMachine.objects.filter(is_del=False, id=id).values('id', 'ip', 'hostname',
                                                                                                'fqdn', 'system', 'env', \
                                                                                                'brand',
                                                                                                'machine_model',
                                                                                                'machine_room',
                                                                                                'cabinet', \
                                                                                                'disk_array', 'sn',
                                                                                                'quick_service',
                                                                                                'warranty', \
                                                                                                'remote_control',
                                                                                                'user', 'pawd', 'cpu',
                                                                                                'mem', \
                                                                                                'disk', 'run_service')
                    for _i in _physical_info:
                        details.append(_i)

                    # phy_count, phy_list = paging(details, phy_page)
                    self.res['data'] = details
                    self.res['count'] = 1
                    # self.res['data'] = details
                except Exception as e:
                    # print e
                    self.res['status'] = False
                    self.res['msg'] = 'search id failed...'
                OperationLog.objects.create(action='OperaMachine._get_info.id', status=self.res['status'],
                                            desc=self.res['msg'])
                return self.res

            elif env:
                try:
                    details = []
                    _physical_info = PhysicalMachine.objects.filter(is_del=False, env=env).values('id', 'ip', 'type',
                                                                                                  'env', 'system',
                                                                                                  'cpu', 'hostname',
                                                                                                  'mem', 'disk',
                                                                                                  'run_service',
                                                                                                  'brand',
                                                                                                  'machine_model',
                                                                                                  'warranty',
                                                                                                  'disk_array',
                                                                                                  'created')
                    for _i in _physical_info:
                        details.append(_i)
                    # self.res['data'] = details
                    phy_count, phy_list = paging(details, phy_page)
                    self.res['data'] = phy_list
                    self.res['count'] = phy_count
                    # self.res['data'] = details
                except Exception as e:
                    # print e
                    self.res['status'] = False
                    self.res['msg'] = 'search id failed...'
                OperationLog.objects.create(action='OperaMachine._get_info.id', status=self.res['status'],
                                            desc=self.res['msg'])
                return self.res
            elif system:
                try:
                    details = []
                    _physical_info = PhysicalMachine.objects.filter(is_del=False, system=system).values('id', 'ip',
                                                                                                        'type',
                                                                                                        'env', 'system',
                                                                                                        'cpu',
                                                                                                        'hostname',
                                                                                                        'mem', 'disk',
                                                                                                        'run_service',
                                                                                                        'brand',
                                                                                                        'machine_model',
                                                                                                        'warranty',
                                                                                                        'disk_array',
                                                                                                        'created')
                    for _i in _physical_info:
                        details.append(_i)
                    # self.res['data'] = details
                    phy_count, phy_list = paging(details, phy_page)
                    self.res['data'] = phy_list
                    self.res['count'] = phy_count
                    # self.res['data'] = details
                except Exception as e:
                    # print e
                    self.res['status'] = False
                    self.res['msg'] = 'search id failed...'
                OperationLog.objects.create(action='OperaMachine._get_info.id', status=self.res['status'],
                                            desc=self.res['msg'])
                return self.res
            elif ip:
                try:
                    details = []
                    _physical_info = PhysicalMachine.objects.filter(is_del=False, ip=ip).values('id', 'ip', 'hostname',
                                                                                                'fqdn', 'system', 'env', \
                                                                                                'brand',
                                                                                                'machine_model',
                                                                                                'machine_room',
                                                                                                'cabinet', \
                                                                                                'disk_array', 'sn',
                                                                                                'quick_service',
                                                                                                'warranty', \
                                                                                                'remote_control',
                                                                                                'user', 'pawd', 'cpu',
                                                                                                'mem', \
                                                                                                'disk', 'run_service')
                    for _i in _physical_info:
                        details.append(_i)
                    # self.res['data'] = details
                    # phy_count, phy_list = paging(details, phy_page)
                    self.res['data'] = details
                    self.res['count'] = 1
                    # self.res['data'] = details
                except Exception as e:
                    # print e
                    self.res['status'] = False
                    self.res['msg'] = 'search id failed...'
                OperationLog.objects.create(action='OperaMachine._get_info.id', status=self.res['status'],
                                            desc=self.res['msg'])
                return self.res

        elif not all and type == '0':
            if id:
                try:
                    details = []
                    _value_info = ValueMachine.objects.filter(is_del=False, id=id).values('id', 'ip', 'hostname',
                                                                                          'fqdn', 'system', 'env', \
                                                                                          'value_file',
                                                                                          'physical_machine',
                                                                                          'run_service',
                                                                                          'user', 'pawd', 'cpu',
                                                                                          'mem', \
                                                                                          'disk')
                    for _i in _value_info:
                        details.append(_i)
                    # val_count, val_list = paging(details, val_page)
                    self.res['data'] = details
                    self.res['count'] = 1
                    # self.res['data'] = details
                except Exception as e:
                    # print e
                    self.res['status'] = False
                    self.res['msg'] = 'search id failed...'
                OperationLog.objects.create(action='OperaMachine._get_info.id', status=self.res['status'],
                                            desc=self.res['msg'])
                return self.res
            elif env:
                try:
                    details = []
                    _value_info = ValueMachine.objects.filter(is_del=False, env=env).values('id', 'ip', 'type', 'env',
                                                                                            'system',
                                                                                            'cpu',
                                                                                            'mem', 'disk',
                                                                                            'run_service', 'user',
                                                                                            'hostname',
                                                                                            'value_file',
                                                                                            'created')
                    for _i in _value_info:
                        details.append(_i)
                    val_count, val_list = paging(details, val_page)
                    self.res['data'] = val_list
                    self.res['count'] = val_count
                    # self.res['data'] = details
                except Exception as e:
                    # print e
                    self.res['status'] = False
                    self.res['msg'] = 'search id failed...'
                OperationLog.objects.create(action='OperaMachine._get_info.id', status=self.res['status'],
                                            desc=self.res['msg'])
                return self.res
            elif system:
                try:
                    details = []
                    _value_info = ValueMachine.objects.filter(is_del=False, system=system).values('id', 'ip', 'type',
                                                                                                  'env',
                                                                                                  'system',
                                                                                                  'cpu',
                                                                                                  'mem', 'disk',
                                                                                                  'run_service', 'user',
                                                                                                  'hostname',
                                                                                                  'value_file',
                                                                                                  'created')
                    for _i in _value_info:
                        details.append(_i)
                    val_count, val_list = paging(details, val_page)
                    self.res['data'] = val_list
                    self.res['count'] = val_count
                    # self.res['data'] = details
                except Exception as e:
                    # print e
                    self.res['status'] = False
                    self.res['msg'] = 'search id failed...'
                OperationLog.objects.create(action='OperaMachine._get_info.id', status=self.res['status'],
                                            desc=self.res['msg'])
                return self.res
            elif ip:
                try:
                    details = []
                    _value_info = ValueMachine.objects.filter(is_del=False, ip=ip).values('id', 'ip', 'hostname',
                                                                                          'fqdn', 'system', 'env', \
                                                                                          'value_file',
                                                                                          'physical_machine',
                                                                                          'run_service',
                                                                                          'user', 'pawd', 'cpu',
                                                                                          'mem', \
                                                                                          'disk')
                    for _i in _value_info:
                        details.append(_i)
                    # val_count, val_list = paging(details, val_page)
                    self.res['data'] = details
                    self.res['count'] = 1
                    # self.res['data'] = details
                except Exception as e:
                    # print e
                    self.res['status'] = False
                    self.res['msg'] = 'search id failed...'
                OperationLog.objects.create(action='OperaMachine._get_info.id', status=self.res['status'],
                                            desc=self.res['msg'])
                return self.res

        elif all and type == '1':
            try:
                details = []
                _physical_info = PhysicalMachine.objects.filter(is_del=False).values('id', 'ip', 'type', 'env',
                                                                                     'system',
                                                                                     'cpu', 'hostname',
                                                                                     'mem', 'disk', 'run_service',
                                                                                     'brand', 'machine_model',
                                                                                     'warranty',
                                                                                     'disk_array',
                                                                                     'created')
                for _i in _physical_info:
                    details.append(_i)
                # self.res['data'] = details
                phy_count, phy_list = paging(details, phy_page)
                self.res['data'] = phy_list
                self.res['count'] = phy_count
            except Exception as e:
                # print e
                self.res['status'] = False
                self.res['msg'] = 'search id failed...'
            OperationLog.objects.create(action='OperaMachine._get_info.id', status=self.res['status'],
                                        desc=self.res['msg'])
            return self.res
        elif all and type == '0':
            try:
                details = []
                _val_machine = ValueMachine.objects.filter(is_del=False).values('id', 'ip', 'type', 'env', 'system',
                                                                                'cpu',
                                                                                'mem', 'disk', 'run_service', 'user',
                                                                                'hostname',
                                                                                'value_file',
                                                                                'created')
                for _i in _val_machine:
                    details.append(_i)
                val_count, val_list = paging(details, val_page)
                self.res['data'] = val_list
                self.res['count'] = val_count
                # self.res['data'] = details
            except Exception as e:
                # print e
                self.res['status'] = False
                self.res['msg'] = 'search id failed...'
            OperationLog.objects.create(action='OperaMachine._get_info.id', status=self.res['status'],
                                        desc=self.res['msg'])
            return self.res

    def _create_physical(self, ip=None, hostname=None, fqdn=None, system=None, env=None, brand=None, server_model=None, \
                         machine_room=None, cabinet=None, disk_array=None, sn=None, quick_service=None, warranty=None, \
                         remote_control=None, user=None, pawd=None, cpu=None, mem=None, disk=None, run_service=None):

        try:
            if machine_room and cabinet:
                PhysicalMachine.objects.create(ip=ip, hostname=hostname, fqdn=fqdn, system=system, env=env, brand=brand, \
                                               machine_room=MachineRoom.objects.get(is_del=False, id=machine_room),
                                               machine_model=server_model, run_service=run_service,
                                               cabinet=Cabinet.objects.get(is_del=False, id=cabinet),
                                               disk_array=disk_array,
                                               sn=sn,
                                               quick_service=quick_service, warranty=warranty, \
                                               remote_control=remote_control, user=user, pawd=pawd, cpu=cpu, mem=mem,
                                               disk=disk)
            elif machine_room:
                PhysicalMachine.objects.create(ip=ip, hostname=hostname, fqdn=fqdn, system=system, env=env, brand=brand, \
                                               machine_room=MachineRoom.objects.get(is_del=False, id=machine_room),
                                               machine_model=server_model, run_service=run_service,
                                               disk_array=disk_array,
                                               sn=sn,
                                               quick_service=quick_service, warranty=warranty, \
                                               remote_control=remote_control, user=user, pawd=pawd, cpu=cpu, mem=mem,
                                               disk=disk)
            else:
                PhysicalMachine.objects.create(ip=ip, hostname=hostname, fqdn=fqdn, system=system, env=env, brand=brand, \
                                               machine_model=server_model, run_service=run_service,
                                               disk_array=disk_array,
                                               sn=sn,
                                               quick_service=quick_service, warranty=warranty, \
                                               remote_control=remote_control, user=user, pawd=pawd, cpu=cpu, mem=mem,
                                               disk=disk)

        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        OperationLog.objects.create(action='OperaMachine._create_physical', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res

    def _create_value(self, ip, hostname, fqdn, system, env, value_file, physical_machine, run_service, user, pawd,
                      cpu, mem, disk):
        try:
            if physical_machine:
                ValueMachine.objects.create(ip=ip, hostname=hostname, fqdn=fqdn, system=system, env=env,
                                            value_file=value_file, \
                                            physical_machine=PhysicalMachine.objects.get(is_del=False,
                                                                                         id=physical_machine), \
                                            run_service=run_service, user=user, pawd=pawd, \
                                            cpu=cpu, mem=mem, disk=disk)
            else:
                ValueMachine.objects.create(ip=ip, hostname=hostname, fqdn=fqdn, system=system, env=env,
                                            value_file=value_file, \
                                            run_service=run_service, user=user, pawd=pawd, \
                                            cpu=cpu, mem=mem, disk=disk)
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        OperationLog.objects.create(action='OperaMachine._create_value', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res

    def _modify_physical(self, id, ip, hostname, fqdn, system, env, brand,
                         machine_model, \
                         machine_room, cabinet, disk_array, sn, quick_service, warranty, \
                         remote_control, user, pawd, cpu, mem, disk, run_service):
        try:
            _physical_machine = PhysicalMachine(is_del=False, id=id)
            _physical_machine.hostname = hostname
            _physical_machine.fqdn = fqdn
            _physical_machine.system = system
            _physical_machine.ip = ip
            _physical_machine.env = env
            _physical_machine.brand = brand
            _physical_machine.machine_model = machine_model
            _physical_machine.machine_room_id = machine_room
            _physical_machine.cabinet_id = cabinet
            _physical_machine.disk_array = disk_array
            _physical_machine.sn = sn
            _physical_machine.quick_service = quick_service
            _physical_machine.warranty = warranty
            _physical_machine.remote_control = remote_control
            _physical_machine.user = user
            _physical_machine.pawd = pawd
            _physical_machine.cpu = cpu
            _physical_machine.mem = mem
            _physical_machine.disk = disk
            _physical_machine.run_service = run_service
            _physical_machine.save()

        except Exception as e:
            # print 20 * '0'
            # print e
            self.res['status'] = False
            self.res['msg'] = e
        OperationLog.objects.create(action='OperaMachine._modify_physical', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res

    def _modify_value(self, id, ip, hostname, fqdn, system, env, value_file, physical_machine, run_service, user, pawd,
                      cpu, mem, disk):
        try:
            _values_machine = ValueMachine(is_del=False, id=id)
            _values_machine.ip = ip
            _values_machine.hostname = hostname
            _values_machine.fqdn = fqdn
            _values_machine.system = system
            _values_machine.env = env
            _values_machine.value_file = value_file
            _values_machine.physical_machine_id = physical_machine
            _values_machine.run_service = run_service
            _values_machine.user = user
            _values_machine.pawd = pawd
            _values_machine.cpu = cpu
            _values_machine.mem = mem
            _values_machine.disk = disk
            _values_machine.save()
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        OperationLog.objects.create(action='OperaMachine._modify_value', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res

    def _delete_machine(self, all=None, id=None, type=None):
        if not all and type == '1':
            if id:
                try:
                    PhysicalMachine.objects.filter(is_del=False, id=id).update(is_del=True)
                except Exception as e:
                    self.res['status'] = False
                    self.res['msg'] = e
                OperationLog.objects.create(action='OperaMachine._delete_machine', status=self.res['status'],
                                            desc=self.res['msg'])
                return self.res
        elif not all and type == '0':
            if id:
                try:
                    ValueMachine.objects.filter(is_del=False, id=id).update(is_del=True)
                except Exception as e:
                    self.res['status'] = False
                    self.res['msg'] = e
                OperationLog.objects.create(action='OperaMachine._delete_machineval', status=self.res['status'],
                                            desc=self.res['msg'])
                return self.res


class MachineInit(object):
    def __init__(self):
        self.res = {
            'msg': '',
            'status': True
        }

    def _get_machine_room(self):
        try:
            _name_list = []
            _names = MachineRoom.objects.filter(is_del=False).values('id', 'room_name')
            for _i in _names:
                _name_list.append(_i)
            self.res['data'] = _name_list
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        OperationLog.objects.create(action='MachineInit._get_machine_room', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res

    def _get_machine_room_cabinet(self, machine_room_id=''):
        if machine_room_id:
            try:
                _cabinets = Cabinet.objects.filter(is_del=False,
                                                   machine_room=MachineRoom.objects.filter(is_del=False,
                                                                                           id=machine_room_id)).values(
                    'id', 'cabinet')
                _cabinets_list = []
                for n in _cabinets:
                    _cabinets_list.append(n)

                self.res['msg'] = machine_room_id
                self.res['data'] = _cabinets_list
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
            OperationLog.objects.create(action='MachineInit._get_machine_room_cabinet', status=self.res['status'],
                                        desc=self.res['msg'])
            return self.res
        else:
            pass

    def get_physical_machine(self):
        try:
            _name_list = []
            _names = PhysicalMachine.objects.filter(is_del=False).values('id', 'hostname')
            for _i in _names:
                _name_list.append(_i)
            self.res['data'] = _name_list
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        OperationLog.objects.create(action='MachineInit.get_physical_machine', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res


class OperaNetworkSegment(object):
    def __init__(self):
        self.res = {
            'msg': '',
            'status': True
        }

    def _add_item(self, start=None, end=None, subnet_mask=None, desc=None, idc=None):
        try:
            NetworkSegment.objects.create(start=start, end=end, subnet_mask=subnet_mask, desc=desc,
                                          idc=MachineRoom.objects.get(is_del=False, id=idc))
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        OperationLog.objects.create(action='OperaNetworkSegment._add_item', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res

    def _get_item(self, all=None, id=None):
        if all:
            try:
                _total = NetworkSegment.objects.filter(is_del=False).values('id', 'start', 'end', 'subnet_mask', 'desc',
                                                                            'created', 'idc__room_name')

                total_list = []

                for i in _total:
                    total_list.append(i)
                self.res['data'] = total_list

            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
        elif id:
            try:
                _total = NetworkSegment.objects.filter(is_del=False, id=id).values('id', 'start', 'end', 'subnet_mask',
                                                                                   'desc', 'idc', 'created')

                total_list = []

                for i in _total:
                    total_list.append(i)
                self.res['data'] = total_list

            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
        OperationLog.objects.create(action='OperaNetworkSegment._get_item', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res

    def _mod_item(self, id=id, start=None, end=None, subnet_mask=None, desc=None, idc=None):
        try:
            _obj = NetworkSegment(is_del=False, id=id)
            _obj.start = start
            _obj.end = end
            _obj.subnet_mask = subnet_mask
            _obj.desc = desc
            _obj.idc = MachineRoom.objects.get(is_del=False, id=idc)

            _obj.save()
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        OperationLog.objects.create(action='OperaNetworkSegment._mod_item', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res

    def _del_item(self, id=None):
        try:
            NetworkSegment.objects.filter(is_del=False, id=id).update(is_del=True)

        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        OperationLog.objects.create(action='OperaNetworkSegment._del_item', status=self.res['status'],
                                    desc=self.res['msg'])
        return self.res
