#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import proxy

msg1 = b"GET http://info.cern.ch/ HTTP/1.1\r\nHost: info.cern.ch\r\n\r\n"
msg2 = b"GET /9.html HTTP/1.1\r\nHost: localhost:6456\r\n\r\n"

host1 = proxy.extract_hostname(msg1)
host2 = proxy.extract_hostname(msg2)

assert host1 == (b"info.cern.ch", 80)
assert host2 == (b"localhost", 6456)
