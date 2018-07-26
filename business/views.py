#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.shortcuts import render
from models import BusinessLine
from models import Project
from models import BusinessLog


# Create your views here.

class OperaBusinessLine(object):
    def __init__(self):
        self.res = {
            'status': True,
            'msg': ''
        }

    def _get_info(self, all=None, id=None, name=None):
        if all:
            print all, name
            try:
                businesses = BusinessLine.objects.filter(is_del=False).values('id', 'name', 'manager', 'contact', \
                                                                              'business', 'desc', 'created')
                _business_list = []
                for item in businesses:
                    _business_list.append(item)

                self.res['data'] = _business_list
            except Exception as e:
                print e
                self.res['status'] = False
                self.res['msg'] = e
        elif id:
            print id, name
            try:
                id_info = []
                items = BusinessLine.objects.filter(is_del=False, id=id).values('id', 'name', 'manager', 'contact',
                                                                                'business', 'desc')
                for i in items:
                    id_info.append(i)
                self.res['data'] = id_info
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
        elif name:
            print 'name', name
            try:
                name_info = []
                items = BusinessLine.objects.filter(is_del=False, name=name).values('id', 'name', 'manager', 'contact',
                                                                                    'business', 'desc')
                for i in items:
                    name_info.append(i)
                self.res['data'] = name_info
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
        print self.res
        BusinessLog.objects.create(action='OperaBusinessLine._get_info', status=self.res['status'], desc=self.res['msg'])
        return self.res

    def _create_info(self, name=None, manager=None, contact=None, business=None, desc=None):
        print 20 * '+'
        print name, manager, contact, business, desc
        try:
            BusinessLine.objects.create(name=name, manager=manager, contact=contact, business=business, desc=desc)
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        BusinessLog.objects.create(action='OperaBusinessLine._create_info', status=self.res['status'],
                                   desc=self.res['msg'])
        return self.res

    def _modify_info(self, id=None, name=None, manager=None, contact=None, business=None, desc=None):
        print id, name, manager, contact, business, desc
        try:
            business_line = BusinessLine(is_del=False, id=id)
            business_line.name = name
            business_line.manager = manager
            business_line.contact = contact
            business_line.business = business
            business_line.desc = desc
            business_line.save()
        except Exception as e:

            self.res['status'] = False
            self.res['msg'] = e
        BusinessLog.objects.create(action='OperaBusinessLine._modify_info', status=self.res['status'],
                                   desc=self.res['msg'])
        return self.res

    def _delete_info(self, id=None):
        try:
            BusinessLine.objects.filter(is_del=False, id=id).update(is_del=True)
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        BusinessLog.objects.create(action='OperaBusinessLine._delete_info', status=self.res['status'],
                                   desc=self.res['msg'])
        return self.res


class OperaProject(object):
    def __init__(self):
        self.res = {
            'status': True,
            'msg': ''
        }

    def _get_item(self, all=None, id=None, name=None, business_line=None):
        if all:
            try:
                _total_list = []
                _total = Project.objects.filter(is_del=False).values('id', 'name', 'language', 'develop', 'ops_contact', \
                                                                     'desc', 'created', 'business_line__name')

                for _i in _total:
                    _total_list.append(_i)
                self.res['data'] = _total_list
            # print '---', _total_list
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
        elif id:
            try:
                _total_list = []
                _total = Project.objects.filter(is_del=False, id=id).values('id', 'name', 'language', 'develop',
                                                                            'ops_contact', 'develop_contact', \
                                                                            'desc', 'created', 'business_line')

                _obj = Project(is_del=False, id=id)
                # print _obj
                _physical_machine = _obj.physical_machine.all().values('project__physical_machine',
                                                                       'project__physical_machine__ip',
                                                                       'project__physical_machine__hostname')
                _value_machine = _obj.value_machine.all().values('project__value_machine', 'project__value_machine__ip',
                                                                 'project__value_machine__hostname')

                value_machine = []
                isValue = False
                physical_machine = []
                isPhysical = False
                if len(_value_machine) > 0:
                    isValue = True
                    for i in _value_machine:
                        if i not in value_machine:
                            value_machine.append(i)

                if len(_physical_machine) > 0:
                    isPhysical = True
                    for _p in _physical_machine:
                        if _p not in physical_machine:
                            physical_machine.append(_p)
                # print 20 * '1'
                for _i in _total:
                    # _i = _i.push(isValue, set(value_machine), isPhysical, set(physical_machine))
                    _i['isValue'] = isValue
                    _i['value_machine'] = value_machine
                    _i['isPhysical'] = isPhysical
                    _i['physical_machine'] = physical_machine
                    _total_list.append(_i)
                self.res['data'] = _total_list
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
            print '---', self.res
        elif name:
            try:
                _total_list = []
                _total = Project.objects.filter(is_del=False, name=name).values('id', 'name', 'language', 'develop',
                                                                                'ops_contact', \
                                                                                'desc', 'created', 'business_line__name')
                for _i in _total:
                    _total_list.append(_i)
                self.res['data'] = _total_list
                print self.res
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
        elif business_line:
            print 'busineline', business_line
            try:
                ids = BusinessLine.objects.filter(is_del=False, name=business_line).values('id')[0].get('id')
                # print 'ids', ids
                _total_list = []
                _total = Project.objects.filter(is_del=False,
                                                business_line=ids) \
                    .values('id', 'name', 'language', 'develop', 'ops_contact', 'desc', 'created', \
                            'business_line__name')
                for _i in _total:
                    _total_list.append(_i)
                self.res['data'] = _total_list
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
        BusinessLog.objects.create(action='OperaProject._get_item', status=self.res['status'],
                                   desc=self.res['msg'])
        return self.res

    def _create_item(self, name=None, business_line=None, language=None, host_type=None, host=None, \
                     develop=None, develop_contact=None, ops_contact=None, desc=None):
        try:
            project = Project()
            project.name = name
            project.business_line = BusinessLine.objects.get(is_del=False, id=business_line)
            project.language = language
            project.develop = develop
            project.develop_contact = develop_contact
            project.ops_contact = ops_contact
            project.desc = desc
            project.save()
            if host_type == 'physical':
                if len(host) > 1:
                    for _host in host:
                        project.physical_machine.add(_host)
                else:
                    project.physical_machine.add(host[0])
            elif host_type == 'value':
                if len(host) > 1:
                    for _host in host:
                        project.value_machine.add(_host)
                else:
                    project.value_machine.add(host[0])
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        BusinessLog.objects.create(action='OperaProject._create_item', status=self.res['status'],
                                   desc=self.res['msg'])
        return self.res

        return self.res

    def _modify_item(self, id=None, name=None, business_line=None, language=None, host_type=None, phy_host=None, \
                     val_host=None, develop=None, develop_contact=None, ops_contact=None, desc=None):
        print 20 * 'x'
        print id, name, business_line, language, host_type, phy_host, val_host, develop, develop_contact, ops_contact, desc
        try:
            _obj = Project(is_del=False, id=id)
            _obj.name = name
            _obj.business_line = BusinessLine.objects.get(is_del=False, id=business_line)
            _obj.language = language
            _obj.develop = develop
            _obj.develop_contact = develop_contact
            _obj.ops_contact = ops_contact
            _obj.desc = desc
            _obj.save()

            is_phy_list = []
            is_val_list = []
            is_phy_host = _obj.physical_machine.all().values('project__physical_machine')
            is_val_host = _obj.value_machine.all().values('project__value_machine')

            if is_phy_host:
                for i in is_phy_host:
                    if i['project__physical_machine'] not in is_phy_list:
                        is_phy_list.append(i['project__physical_machine'])
            if is_val_host:
                for c in is_val_host:
                    if c['project__value_machine'] not in is_val_list:
                        is_val_list.append(c['project__value_machine'])
            print is_val_list, is_phy_list
            if phy_host:
                if is_phy_list:
                    for _isin in is_phy_list:
                        print 'isin', _isin, phy_host
                        if _isin not in phy_host:
                            _obj.physical_machine.remove(_isin)

                if len(phy_host) > 1:
                    for _host in phy_host:
                        _obj.physical_machine.add(_host)
                else:
                    _obj.physical_machine.add(phy_host[0])
            else:
                if is_phy_list:
                    for _isin in is_phy_list:
                        print 'no phy', _isin
                        _obj.physical_machine.remove(_isin)
            if val_host:
                if is_val_list:
                    for _isin in is_val_list:
                        print 'isin', _isin, val_host
                        if _isin not in val_host:
                            print _isin
                            _obj.value_machine.remove(_isin)

                if len(val_host) > 1:
                    for _host in val_host:
                        print '_hostxxx', _host, is_val_list, val_host
                        _obj.value_machine.add(_host)
                        # if _host in is_val_list:
                        #     print _host
                        #     pass
                        # else:
                        #     _obj.value_machine.add(_host)

                else:
                    _obj.value_machine.add(val_host[0])
            else:
                if is_val_list:
                    for _isin in is_val_list:
                        _obj.value_machine.remove(_isin)
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        BusinessLog.objects.create(action='OperaProject._modify_item', status=self.res['status'],
                                   desc=self.res['msg'])
        return self.res

    def _delete_item(self, id=None):
        try:
            Project.objects.filter(is_del=False, id=id).update(is_del=True)
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        BusinessLog.objects.create(action='OperaProject._delete_item', status=self.res['status'],
                                   desc=self.res['msg'])
        return self.res