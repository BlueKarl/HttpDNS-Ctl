#!/usr/bin/env python
# encoding: utf-8

import socket
import struct
import re
from consts import HTTPDNS_DOMAIN_PREFIX
domain_pattern = re.compile('{0}:([^:]+)$'.format(HTTPDNS_DOMAIN_PREFIX))


def ip2long(ip):
    """
    Convert an IP string to long
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]


def long2ip(ip_long):
    return socket.inet_ntoa(struct.pack('!L', ip_long))
