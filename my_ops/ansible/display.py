#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import sys


class TeeObj(object):
    origin_stdout = sys.stdout

    def __init__(self, file_obj):
        self.file_obj = file_obj

    def write(self, msg):
        self.origin_stdout.write(msg)
        self.file_obj.write(msg.replace('*', ''))

    def flush(self):
        self.origin_stdout.flush()
        self.file_obj.flush()
