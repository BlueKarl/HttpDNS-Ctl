#!/usr/bin/env python
# encoding: utf-8

import sys
import os
sys.path.append(os.path.abspath('.'))

import yaml
from httpdns.model import DomainName


def read_yaml(filename):
    data = yaml.load(open(filename))
    return data


def dump_yaml_to_redis(src_data):
    for dn, dn_dict in src_data.iteritems():
        domain_name = DomainName(dn)
        apis = dn_dict.get('api') or []
        dns = dn_dict.get('dns') or {}
        failure = dn_dict.get('failure')
        for api in apis:
            domain_name.add_api(api)
        for sp, ips in dns.iteritems():
            for ip in ips:
                print dn, sp, ip
                domain_name.add(ip, sp=sp)
        if not failure:
            domain_name.set_failure()
        else:
            domain_name.set_failure(failure['minute'], failure['times'])

if __name__ == '__main__':
    data = read_yaml('dn.yaml')
    dump_yaml_to_redis(data)
