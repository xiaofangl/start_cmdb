#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.shortcuts import render

# Create your views here.
from models import ToDoList as todolist
from business.models import BusinessLine
from business.models import Project
from assets.models import PhysicalMachine, ValueMachine


class ServerTree(object):
    def __init__(self):
        self.res = {
            'status': True,
            'msg': ''
        }

    def _get_tree(self, all=None, init=None, business_line=None):
        if all:
            _total_tree = []

        elif init:
            print 'init', init
            _business_line = []
            _total_business_line = BusinessLine.objects.filter(is_del=False).values('id', 'name')
            _projec_count = BusinessLine.objects.filter(is_del=False).values('id', 'project').count()
            print '_projec_count', _projec_count

            for _line in _total_business_line:
                if _line not in _business_line:
                    # print _line, type(_line), _line.get('id')
                    _count = Project.objects.filter(is_del=False, business_line=BusinessLine.objects.get(is_del=False,
                                                                                                         id=_line.get(
                                                                                                             'id'))).count()
                    _line['count'] = _count
                    print _count, _line
                    _business_line.append(_line)

            self.res['data'] = _business_line
            print self.res
        elif business_line:
            # business_line = '3' if business_line else business_line
            print 'business_line', business_line
            """
            business_dic = [

                {'project_name1': [{
                    'dev': [
                        {'host1': 'server'},
                        {'host2': 'server2'}
                    ],
                    'st': [],
                    'pre': [],
                    'pro': []
                }]
                },

                {'project_name2': []}
            ]
            """

            _tree = []
            _one_line = BusinessLine.objects.filter(is_del=False, id=business_line).values('id', 'name', 'project', \
                                                                                           'project__physical_machine__is_del', \
                                                                                           'project__value_machine__is_del', \
                                                                                           'project__name', \
                                                                                           'project__physical_machine', \
                                                                                           'project__physical_machine__ip',
                                                                                           'project__physical_machine__env', \
                                                                                           'project__value_machine',
                                                                                           'project__value_machine__ip', \
                                                                                           'project__value_machine__env')
            _projects = BusinessLine.objects.filter(is_del=False, id=business_line).values('project')
            project_list = []
            for i in _projects:
                if i not in project_list:
                    project_list.append(i['project'])

            print 20 * 'x'
            print project_list
            # project_name_list
            tmp = {}
            for i in _one_line:
                print 'i: ', i
                if i not in _tree:
                    # if i['project__value_machine__is_del'] == False or i['project__physical_machine__is_del'] == False:
                    _tree.append(i)

            res = []
            for c in project_list:
                tmp = {}
                _tmp = {}
                dev = []
                st = []
                pre = []
                pro = []
                for i in _tree:
                    if c == i['project']:
                        # print 'c - i', c, i['project']
                        # print '--=', i['project__value_machine__env'], i['project__value_machine__ip']
                        if i['project__value_machine__env'] == u'测试':
                            _c = i['project__value_machine__ip'] + '_' + 'val' + '_' + 'service'
                            print i['project__value_machine__ip']
                            if _c not in st:
                                print i['project__value_machine__ip']
                                print 'i', _c
                                st.append(_c)
                                print 'st', st
                        elif i['project__value_machine__env'] == u'开发':
                            _c = i['project__value_machine__ip'] + '_' + 'val' + '_' + 'service'
                            if _c not in dev:
                                dev.append(_c)
                                print 'dev', dev
                        elif i['project__value_machine__env'] == u'预发布':
                            _c = i['project__value_machine__ip'] + '_' + 'val' + '_' + 'service'
                            if _c not in pre:
                                pre.append(_c)
                                print 'pre', pre
                        elif i['project__value_machine__env'] == u'生产':
                            _c = i['project__value_machine__ip'] + '_' + 'val' + '_' + 'service'
                            if _c not in pro:
                                pro.append(_c)
                                print 'pro', pro
                        # print 30 * '9'
                        # print 'phy', i['project__physical_machine__env']
                        if i['project__physical_machine__env'] == u'测试':
                            print 'phy', i['project__physical_machine__env']
                            _n = i['project__physical_machine__ip'] + '_' + 'phy' + '_' + 'service'
                            if _n not in st:
                                st.append(_n)
                                print st
                        elif i['project__physical_machine__env'] == u'开发':
                            _n = i['project__physical_machine__ip'] + '_' + 'phy' + '_' + 'service'
                            if _n not in dev:
                                dev.append(_n)
                                print dev
                        elif i['project__physical_machine__env'] == u'预发布':
                            _n = i['project__physical_machine__ip'] + '_' + 'phy' + '_' + 'service'
                            if _n not in pre:
                                pre.append(_n)
                                print pre
                        elif i['project__physical_machine__env'] == u'生产':
                            _n = i['project__physical_machine__ip'] + '_' + 'phy' + '_' + 'service'
                            if _n not in pro:
                                pro.append(_n)
                                print pro
                        _tmp['dev'] = dev
                        _tmp['st'] = st
                        _tmp['pre'] = pre
                        _tmp['pro'] = pro
                        _tmp['env'] = [u'开发', u'测试', u'预发布', u'生产']
                        print '_tmp--', _tmp
                        print
                        tmp['details'] = _tmp
                        tmp['id'] = c
                        tmp['name'] = i['project__name']
                    print '+++++++'
                    print tmp
                res.append(tmp)

            self.res['data'] = res

        print self.res
        return self.res


class HomeChart(object):
    def __init__(self):
        self.res = {
            'status': True,
            'msg': ''
        }

    def _get_info(self, init=None):
        if init:
            try:
                business_count = BusinessLine.objects.filter(is_del=False).count()
                project_count = Project.objects.filter(is_del=False).count()
                physical_server = PhysicalMachine.objects.filter(is_del=False).count()
                value_server = ValueMachine.objects.filter(is_del=False).count()

                print 20 * '6'
                data = {
                    'business_count': business_count,
                    'project_count': project_count,
                    'physical_server': physical_server,
                    'value_server': value_server
                }

                self.res['data'] = data
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
        return self.res


class ToDoList(object):
    def __init__(self):
        self.res = {
            'status': True,
            'msg': ''
        }

    def _add_info(self, info=None):
        try:
            todolist.objects.create(title=info)
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
            print e
        return self.res

    def _get_info(self):
        try:
            total = todolist.objects.filter(is_del=False).values('title', 'is_del', 'id')
            did_total = todolist.objects.filter(is_del=True).values('title', 'is_del', 'id')
            _list = []
            for i in total:
                if i not in _list:
                    _list.append(i)
            print _list
            did_list = []
            for c in did_total:
                if c not in did_list:
                    did_list.append(c)
            self.res['data'] = _list
            self.res['did_data'] = did_list

        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        return self.res

    def _mod_info(self, id=None):
        if id:
            try:
                todolist.objects.filter(is_del=False, id=id).update(is_del=True)
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = e
                print e
            return self.res
