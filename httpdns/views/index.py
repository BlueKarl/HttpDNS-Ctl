# encoding: utf-8

import sys 
import json
from flask import url_for, redirect, g, render_template, Blueprint, request, abort
from collections import defaultdict

from httpdns.db import rds
from httpdns.model import DomainName, Service_IP
from httpdns.config import DEFAULT_CACHE_TIME
from httpdns.consts import HTTPDNS_IP_DEFAULT, HTTPDNS_DOMAIN_PREFIX, DEFAULT_SP_NUM, SP_NUM_MAP

bp = Blueprint('index', __name__)
reload(sys) 
sys.setdefaultencoding('utf-8')

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain = ''.join(request.form.get('host', default='').split())
        ip = ''.join(request.form.get('ip', default='').split())
        domain_name = DomainName(domain)
        if len(domain) != 0 and len(ip) != 0:
            domain_name.add(ip)
    domains = rds.smembers(HTTPDNS_DOMAIN_PREFIX)
    default_ip = rds.hget(HTTPDNS_IP_DEFAULT, 'ip')
    TTL = DEFAULT_CACHE_TIME
    if not domains:
        domains = "0"
    if not default_ip:
        default_ip = 'not set'
    count = {}
    for domain in domains:
        domain_name = DomainName(domain)
        count[domain] = domain_name.get_all_counts()
    return render_template('index.html', ttl=TTL, count=count, results=domains, default_ip=default_ip)
@bp.route('/default/', methods=['GET', 'POST'])
def default():
    if request.method == 'POST':
        ip = ''.join(request.form.get('defaultip', default='').split())
        default_ip = Service_IP(ip)
        if len(ip) != 0:
            default_ip.set_default_ip(ip)
    domains = rds.smembers(HTTPDNS_DOMAIN_PREFIX)
    default_ip = rds.hget(HTTPDNS_IP_DEFAULT, 'ip')
    TTL = DEFAULT_CACHE_TIME
    if not domains:
        domains = "0"
    if not default_ip:
        default_ip = 'not set'
    count = {}
    for domain in domains:
        domain_name = DomainName(domain)
        count[domain] = domain_name.get_all_counts()
    return render_template('index.html', ttl=TTL, count=count, results=domains, default_ip=default_ip)
@bp.route('/<domain>/', methods=['GET', 'POST'])
def show_info(domain):
    domain_name = DomainName(domain)
    if request.method == 'POST':
        isp = ''.join(request.form.get('local', default='').split())
        ip = ''.join(request.form.get('ip', default='').split())
        if len(ip) != 0 and len(isp) != 0:
            domain_name.add(ip, isp)
    count = domain_name.get_counts()
    result = defaultdict(list)
    for sp in domain_name.all_sps():
        for host in domain_name.sp_ips(sp):
            result[sp].append(host)
    if not result:
        return render_template('404.html')
    return render_template('domaininfo.html', count=count, results=result, domain=domain, spnummap=SP_NUM_MAP)

@bp.route('/delete/<domain>/<isp>/<ip>', methods=['POST'])
def delete_info(domain, isp, ip):
    domain_name = DomainName(domain)
    if rds.scard(('%s:%s:%s')%(HTTPDNS_DOMAIN_PREFIX, domain, isp)) == 1:
        domain_name.delete_sp(isp)
    domain_name.delete_sp_ip(ip, isp)
    result = defaultdict(list)
    for sp in domain_name.all_sps():
        for host in domain_name.sp_ips(sp):
            result[sp].append(host)
    return render_template('domaininfo.html', result=result, domain=domain)

@bp.route('/delete/<domain>', methods=['POST'])
def delete_domain(domain):
    domain_name = DomainName(domain)
    domain_name.delete_domain()
    result = defaultdict(list)
    for sp in domain_name.all_sps():
        for host in domain_name.sp_ips(sp):
            result[sp].append(host)
    return render_template('index.html', result=result)

@bp.errorhandler(403)
@bp.errorhandler(404)
def errorhandler(error):
    return render_template('{}.html'.format(error.code))

@bp.before_request
def login_or_not():
    if not g.user:
        abort(403)
