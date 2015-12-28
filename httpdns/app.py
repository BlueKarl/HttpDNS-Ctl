#!/usr/bin/env python
# encoding: utf-8

import logging
import json

from flask import Flask, request, g, abort
from werkzeug.utils import import_string
from httpdns.config import HTTPDNS_USER_COOKIE, IS_ADMIN

blueprints = (
    'index',
    'login',
)


def create_app():
    app = Flask(__name__)
    app.config.from_object('httpdns.config')
    app.secret_key = 'xiaoliulaoshibobobo'

    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
                        level=logging.INFO)

    for bp in blueprints:
        import_name = '%s.views.%s:bp' % (__package__, bp)
        app.register_blueprint(import_string(import_name))

    @app.before_request
    def init_global_vars():
        user_dict = json.loads(request.cookies.get(HTTPDNS_USER_COOKIE, '{}'))
        user = user_dict.get('realname')
        admins = IS_ADMIN.split(',')
        if user and user in admins:
            g.user = user
        else:
            g.user = None
    
    return app
