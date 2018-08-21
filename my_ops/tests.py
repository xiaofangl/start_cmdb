#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

# from django.test import TestCase

# Create your tests here.
from __future__ import absolute_import, unicode_literals
from ops_api.celery import app


@app.task
def tashA(x, y):
    return x * y


@app.task
def taskB(x, y, z):
    return x + y + z


@app.task
def add(x, y):
    return x + y