#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
import logging


def get_object_or_none(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    return obj


def get_logger(name=None):
    return logging.getLogger('opsserver.%s' % name)