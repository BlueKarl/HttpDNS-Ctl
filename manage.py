#!/usr/bin/env python
# encoding: utf-8

from flask.ext.script import Shell, Manager
from httpdns.app import create_app
from httpdns.model import IP, DomainName

app = create_app()
manager = Manager(app)


def make_shell_context():
    return dict(app=app, IP=IP, DomainName=DomainName)
manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def run():
    app.run('0.0.0.0', 5000, debug=True)

if __name__ == '__main__':
    manager.run()
