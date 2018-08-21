#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import redis
from redis.sentinel import Sentinel


def conn_redis():
    sentinel = Sentinel([('192.168.99.37', 6402),
                         ('192.168.99.39', 6403),
                         ('192.168.99.43', 6401)], socket_timeout=0.1)
    master = sentinel.discover_master('sentinel-192.168.99.43-6400')
    print 'master', master

    # slave = sentinel.discover_master('sentinel-192.168.99.43-6400')
    # print 'slave', slave

    master = sentinel.master_for('sentinel-192.168.99.43-6400', socket_timeout=0.1)
    w_ret = master.set('foo', 'bar')

    print w_ret
    r_ret = master.get('foo')
    print 20 * 'x'
    print r_ret


if __name__ == '__main__':
    conn_redis()