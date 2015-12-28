#!/usr/bin/env python
# encoding: utf-8
import requests
import urllib
import urllib2
import json
from urlparse import urljoin
import flask
from flask import make_response, Blueprint, url_for, redirect, request, abort, jsonify, render_template
from httpdns.config import OPENID_SERVER_LOGIN, OPENID_SERVER_PRO, HTTPDNS_USER_COOKIE

bp = Blueprint('login', __name__,)

@bp.route('/login/')
def login():
    req_url = urllib.urlencode({
              'return_to': urljoin(request.url, url_for('login.verify')),
              'days': '14',
                              })
    url = "{0}?{1}".format(OPENID_SERVER_LOGIN, req_url)
    return redirect(url)

@bp.route('/verify/')
def verify():
    req_url = OPENID_SERVER_PRO + '?'
    token = request.args.get('token')
    params = {'token' : token}
    r = requests.get(req_url, params=params)
    resp = make_response(redirect(url_for('index.index')))
    if r.status_code == 200:
        try:
            profile = r.json()
        except ContentDecodingError:
            pass
        else:
            cookies = {'username': profile['username'], 'uid': profile['uid'],\
                    'email': profile['email'], 'realname':profile['realname']}
            resp.set_cookie(HTTPDNS_USER_COOKIE, json.dumps(cookies))
    return resp

@bp.route('/logout/')
def logout():
    resp = make_response(redirect(url_for('index.index')))
    if request.cookies.get(HTTPDNS_USER_COOKIE):
        resp.set_cookie(HTTPDNS_USER_COOKIE, '', expires=0)
    return resp 
