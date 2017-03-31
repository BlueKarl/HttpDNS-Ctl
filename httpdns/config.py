#!/usr/bin/env python
# encoding: utf-8

import os

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_POOL_SIZE = int(os.getenv('REDIS_POOL_SIZE', '1000'))

DEFAULT_CACHE_TIME = int(os.getenv('DEFAULT_CACHE_TIME', 300))

OPENID_SERVER_LOGIN = os.getenv('OPENID_SERVER_LOGIN', 'http://openids-web.intra.hunantv.com/oauth/login/')
OPENID_SERVER_PRO = os.getenv('OPENID_SERVER_PRO', 'http://openids-web.intra.hunantv.com/oauth/profile/')

HTTPDNS_USER_COOKIE = os.getenv('HTTPDNS_USER_COOKIE', 'e45af773ghttpdns_cookies')

IS_ADMIN = os.getenv('IS_ADMIN', 'aaaaa')

DEFAULT_HOST_PRIORITY = os.getenv('DEFAULT_HOST_PRIORITY', 0)
MATCHED_HOST_PRIORITY = os.getenv('MATCHED_HOST_PRIORITY', 30)
