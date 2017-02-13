#!/usr/bin/env python
# encoding: utf-8

HTTPDNS_IP_PREFIX = 'httpdns:ip'
HTTPDNS_DOMAIN_PREFIX = 'httpdns:domain'
HTTPDNS_SERVICE_PREFIX = 'httpdns:service'
HTTPDNS_IP_DEFAULT = 'httpdns:default'

DEFAULT_SP_NUM = '0'

REDIS_CACHE_KEY = 'httpdns:cache:{0}'
SP_NUM_MAP = {
    '0': '缺省',
    '1': '电信',
    '2': '联通',
    '3': '铁通',
    '4': '移动',
    '5': '教育网',
    '6': '广电网',
    '7': '方正宽带',
    '8': '鹏博士',
    '9': '中企通信',
    '10': '天威视讯',
    '11': '阿里云',
    '12': '歌华有线',
    '13': '有线通',
    '14': '京宽网络',
    '15': '科技网',
    '16': '珠江宽频',
    '17': '中电飞华',
    '18': '华数',
    '19': 'baidu.com',
    '20': '海外'
}
