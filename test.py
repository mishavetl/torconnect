#!/usr/bin/python

import socks
import socket

from stem import Signal
from stem.control import Controller
import urllib, sys

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 7000)
socket.socket = socks.socksocket

for _ in range(2):
    with Controller.from_port(port = 7000) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
    urllib.urlopen("atagar.com/echo.php")

sys.exit()
