#!/usr/bin/env python
# encoding: utf-8
from httpdns.db import rds
from httpdns.consts import HTTPDNS_IP_PREFIX, HTTPDNS_DOMAIN_PREFIX, HTTPDNS_SERVICE_PREFIX, DEFAULT_SP_NUM
from httpdns.utils import ip2long


class IP(object):
    '''
    IP have three properties:
    sp -- service provider
    ip_addr -- ip address
    location -- location the ip belongs to
    '''
    @classmethod
    def list_ips(cls):
        return rds.smembers(HTTPDNS_IP_PREFIX)

    def __init__(self, ip_addr):
        self.ip_key = 'httpdns:ip:{0}'.format(ip_addr)
        self.ip_ranges_key = 'httpdns:ip:ranges'
        self.ip_provider_key = 'httpdns:ip:provider:{0}'
        self.address = ip_addr

    @property
    def sp(self):
        long_ip = ip2long(self.address)
        ip_range_id = rds.zrangebyscore(self.ip_ranges_key, long_ip, float('inf'), 0, 1)
        if ip_range_id:
            provider_key = self.ip_provider_key.format(ip_range_id.pop())
            return rds.hget(provider_key, 'isp')
        return None

    @property
    def location(self):
        long_ip = ip2long(self.address)
        ip_range_id = rds.zrangebyscore(self.ip_ranges_key, long_ip, float('inf'), 0, 1)
        if ip_range_id:
            provider_key = self.ip_provider_key.format(ip_range_id.pop())
            return rds.hget(provider_key, 'location')
        return None


class DomainName(object):

    def __init__(self, domain_name):
        self.domain_name = domain_name
        self.key = 'httpdns:domain:{0}'.format(domain_name)
        self.sp_key_pattern = "httpdns:domain:{0}:{1}"    # {0} domain {1} sp
        self.sp_count_key_pattern = "httpdns:domain:{0}:sp:{1}:count"  # value
        self.location_key = "httpdns:domain:{0}:location".format(domain_name)

    def add(self, ip_addr, sp=DEFAULT_SP_NUM):
        ''' add ip_addr to a sp, if sp or domain is not exist, create it'''
        if not rds.sismember(HTTPDNS_DOMAIN_PREFIX, self.domain_name):
            self.add_domain()
        if not rds.sismember(self.key, sp):
            self.add_sp(sp)
        return self.add_sp_ip(ip_addr, sp)

    def clear(self):
        for sp in list(rds.smembers(self.key)):
            sp_ips_key = self.sp_key_pattern.format(self.domain_name, sp)
            rds.delete(sp_ips_key)
        rds.delete(self.key)
        rds.srem(HTTPDNS_DOMAIN_PREFIX, self.domain_name)

    def add_domain(self):
        return rds.sadd(HTTPDNS_DOMAIN_PREFIX, self.domain_name)

    def delete_domain(self):
        self.clear()

    def add_sp(self, sp):
        return rds.sadd(self.key, sp)

    def delete_sp(self, sp):
        '''delete a specific sp on this domain'''
        if sp == DEFAULT_SP_NUM:
            return False
        sp_ips_key = self.sp_key_pattern.format(self.domain_name, sp)
        rds.srem(self.key, sp)
        rds.delete(sp_ips_key)

    def add_sp_ip(self, ip_addr, sp):
        sp_ips_key = self.sp_key_pattern.format(self.domain_name, sp)
        return rds.sadd(sp_ips_key, ip_addr)

    def delete_sp_ip(self, ip_addr, sp=DEFAULT_SP_NUM):
        ''' if is defualt sp and only have 1 item, you cant remove it'''
        ips_key = self.sp_key_pattern.format(self.domain_name, sp)
        if sp == DEFAULT_SP_NUM and rds.scard(ips_key) <= 1:
            return False
        return self.delete_ip_from_sp(ip_addr, sp)

    def delete_ip_from_sp(self, ip_addr, sp):
        sp_ips_key = self.sp_key_pattern.format(self.domain_name, sp)
        return rds.srem(sp_ips_key, ip_addr)

    def all_sps(self):
        ''' return all domain's service providers'''
        return rds.smembers(self.key)

    def sp_ips(self, sp=DEFAULT_SP_NUM):
        ''' return ips of a specific service provider '''
        ips_key = self.sp_key_pattern.format(self.domain_name, sp)
        return rds.smembers(ips_key)

    def sp_rand_ip(self, sp=DEFAULT_SP_NUM):
        ips_key = self.sp_key_pattern.format(self.domain_name, sp)
        return rds.srandmember(ips_key)

    def sp_count_incr(self, sp):
        key = self.sp_count_key_pattern.format(self.domain_name, sp)
        rds.incr(key)

    def get_count(self, sp):
        ''' get count by sp '''
        key = self.sp_count_key_pattern.format(self.domain_name, sp)
        return rds.get(key) or '0'

    def get_counts(self):
        result = {}
        for sp in self.all_sps():
            key = self.sp_count_key_pattern.format(self.domain_name, sp)
            result[sp] = rds.get(key) or '0'
        return result

    def get_all_counts(self):
        result = 0
        all_counts = map(lambda x: int(x), self.get_counts().values())
        if all_counts:
            result = reduce(lambda x, y: x + y, all_counts)
        return result


class Service_TTL(object):

    def __init__(self, service_num):
        self.service_key = 'httpdns:service:{0}'.format(service_num)

    def set_ttl(self, ttl):
        return rds.hset(self.service_key, 'ttl', ttl)

    def get_ttl(self):
        return rds.hget(self.service_key, 'ttl')

class Service_IP(object):
    def __init__(self, ip):
        self.service_ip = 'httpdns:default'

    def set_default_ip(self, default):
        return rds.hset(self.service_ip, 'ip', default)

    def get_default_ip(self):
        return rds.hget(self.service_ip, 'ip')

