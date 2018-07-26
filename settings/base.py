#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from settings import *
from os.path import join, abspath, dirname

# make root path
here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..", "..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)

DEBUG = False

TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-hans'

ALLOWED_HOSTS = [
]
INTERNAL_IPS = ['127.0.0.1']
INSTALLED_APPS += [
    'assets',
    'business',
    'home'
]

SMS = {
}

WEIXIN = {
}

WEIXIN_ADM = {

}

WX_CONF = {

}

API_SRV = {
    'erp': {
        'host': "http://.com",
        'authorization': '',
        'api': {
            "pdnames": "/api/v1/intapi/products/",
        },
    },
}

IMG_UPLOAD_URL = "http://img..com"

LOGGING_MIXIN_CONFIG = {
    "logging_methods": ['POST', 'PUT', 'PATCH', 'DELETE'],
}

AUTH = {
    "app_name": "deal",
    "app_key": "",
    "auth_login": "",
    "auth_info": "",
    "auth_mobile": "",
    "api_grouprole": "",
    "api_member": "",
    "api_groups": "",
}

CAPTCHA_BACKGROUND_COLOR = "#eee"
CAPTCHA_CHALLENGE_FUNCT = 'tools.helper.random_digit_challenge'

