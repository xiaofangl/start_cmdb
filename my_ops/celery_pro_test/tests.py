#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
# from django.conf import settings

from celery import Celery

app = Celery('tests', broker='redis://192.168.99.61:6379/0', backend='redis://192.168.99.61:6379/1',)


@app.task
def add(x, y):
    return x + y

if __name__ == '__main__':
    add.delay(2, 3)