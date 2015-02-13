#!/usr/bin/python

import StringIO
import socket
import urllib2, sys

import socks  # SocksiPy module
import stem.process

#'http://craftmusic.ru/cs_go/16750'
# sudo docker run -d -i -v ~/Documents/Projects/torconnect:/src/app michael/ubuntu /src/app/main.py http://15free-steam-games.ru/index.php?code=7502299 100

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="url to connect")
parser.add_argument("amount", type=int, help="amount of times to connect")

args = parser.parse_args()

url = args.url
amount = args.amount

SOCKS_PORT = 7000

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo


def query(url):
  """
  Uses urllib to fetch a site using SocksiPy for Tor over the SOCKS_PORT.
  """

  try:
    return urllib2.urlopen(url).read()
  except:
    return "Unable to reach %s" % url


def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print line


for x in range(1, amount + 1):

        print "\n________  %d\n" % x

        print "Starting Tor:\n"

        tor_process = stem.process.launch_tor_with_config(
          config = {
            'SocksPort': str(SOCKS_PORT),
            # 'ExitNodes': '{ru}',
          },
          init_msg_handler = print_bootstrap_lines,
        )

        # print "\nChecking our endpoint:\n"
        # print query("https://www.atagar.com/echo.php")
        print "\nConnecting to ", url
        urllib2.urlopen(url)

        print "\nStopping Tor\n"

        tor_process.kill()


exit(0)
