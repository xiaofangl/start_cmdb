#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import redis
from ops_api.celeryconfig import REDIS_SERVER, REDIS_PORT, REDIS_DB


class OperaRedis(object):
    def __init__(self, res):
        print REDIS_SERVER, REDIS_PORT, REDIS_DB
        self.host = REDIS_SERVER
        self.port = REDIS_PORT
        self.db = REDIS_DB
        self.res = res
        self.conn = redis.Redis(host=self.host, port=self.port, db=self.db)
        print self.host, self.port, self.db

    def _get_info(self, key=None):
        if not key:
            self.res['status'] = False
            self.res['msg'] = 'not redis key...'
        else:
            try:
                print 'key', key, type(key)
                data = self.conn.get(key)
                self.res['data'] = data
                # print self.res
            except Exception as e:
                self.res['status'] = False
                self.res['msg'] = 'redis  get data failed ...'

        return self.res
