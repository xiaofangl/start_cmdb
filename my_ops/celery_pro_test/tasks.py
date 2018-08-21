#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from celery.utils.log import get_task_logger
from celery import shared_task
from instance import app

print 'this tasks...'

@app.task
def test_celery(x, y):
    logger = get_task_logger(__name__)
    logger.info('func start  ----------------->')
    logger.info('application:%s', "TEST_APP")
    logger.info('func end -------------------->')
    return x + y


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


if __name__ == '__main__':
    res = add.delay(228, 24)
    print("start running task")
    print("async task res", res.get())
