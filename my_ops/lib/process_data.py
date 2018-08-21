#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import json

from read_redis import OperaRedis
from assets.models import PhysicalMachine, ValueMachine


class ProcessData(OperaRedis):
    def __init__(self, key):
        res = dict(status=True, data='')
        super(ProcessData, self).__init__(res)
        self.key = key

    def _read_redis(self):
        try:
            self.res = self._get_info(self.key)
            #print '_ret', self.res
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = '_read_redis failed...'
        return self.res

    def _format_data(self):
        try:
            _res = self._read_redis()
            #print '_res', _res
            _data = ''
            if _res['status']:
                _data = _res['data']
                _data = json.loads(_data)
                if len(_data['result']['contacted']) > 0:
                    _data = _data['result']['contacted']
                    #print '_data', type(_data), _data

            host_info = []
            for i in _data:
                item = dict()
                item[i] = _data[i][0]['ansible_facts']
                host_info.append(item)
            #print 'host_info: ', host_info
            self.res['data'] = host_info
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = '_format_data failed...'
        # #print self.res
        return self.res

    def _insert_db(self):
        try:
            _reco = self._format_data()
            #print '_reco', _reco
            for c in _reco['data']:
                #print 'c: ', c.keys()[0], c.values(), type(c.keys())
                if PhysicalMachine.objects.filter(is_del=False, ip=c.keys()[0]):
                    PhysicalMachine.objects.filter(is_del=False, ip=c.keys()[0]).update(cpu=c.values()[0]['cpu'],
                                                                                     mem=c.values()[0]['mem'], \
                                                                                     disk=c.values()[0]['disk'])
                elif ValueMachine.objects.filter(is_del=False, ip=c.keys()[0]):
                    ValueMachine.objects.filter(is_del=False, ip=c.keys()[0]).update(cpu=c.values()[0]['cpu'],
                                                                                  mem=c.values()[0]['mem'], \
                                                                                  disk=c.values()[0]['disk'])
            self.res['data'] = []
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = '_insert_db failed...'
        return self.res

    @staticmethod
    def _get_host_ip(id=None, type=None):
        _result = None
        if id and type == '1':
            _ip = PhysicalMachine.objects.filter(is_del=False, id=id).values('ip')
            _result = _ip
        elif id and type == '0':
            _ip = ValueMachine.objects.filter(is_del=False, id=id).values('ip')
            _result = _ip
        else:
            _result = False
        # print _result[0]['ip']
        return _result[0]['ip']