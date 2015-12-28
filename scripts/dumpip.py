#!/usr/bin/env python
# encoding: utf-8

import sys
import os
sys.path.append(os.path.abspath('.'))

from httpdns.db import rds

sp_dict = {
    '电信': '1',
    '联通': '2',
    '铁通': '3',
    '移动': '4',
    '教育网': '5',
    '广电网': '6',
    '方正宽带': '7',
    '鹏博士': '8',
    '中企通信': '9',
    '天威视讯': '10',
    '阿里云': '11',
    '歌华有线': '12',
    '有线通': '13',
    '京宽网络': '14',
    '科技网': '15',
    '珠江宽频': '16',
    '中电飞华': '17',
    '华数': '18',
    'baidu.com': '19',
    '*': '0'
}

ip_ranges_key = 'httpdns:ip:ranges'
ip_provider_key = 'httpdns:ip:provider:{0}'


def dump_data(filename):
    with open(filename) as f:
        for line in f.readlines():
            columns = line.split()
            c_id = columns[0]
            long_ip_min = columns[3]
            long_ip_max = columns[4]
            province = columns[6]
            isp = columns[8]
            sp_num = sp_dict.get(isp) or 7
            if '电信' in isp:
                sp_num = sp_dict['电信']
            elif '联通' in isp:
                sp_num = sp_dict['联通']
            elif '铁通' in isp:
                sp_num = sp_dict['铁通']
            rds.hmset(ip_provider_key.format(c_id),
                      {'name': isp, 'min': long_ip_min, 'max': long_ip_max,
                       'province': province, 'isp': sp_num})
            print c_id, isp, long_ip_max, province, sp_num

            rds.zadd(ip_ranges_key, c_id, long_ip_max)


if __name__ == '__main__':
    dump_data('ip_range.example')
