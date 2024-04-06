#!/usr/bin/env python3

import argparse
import dnslib
import socket

# import urllib
# import curl
# import requests

'''
DNS server called using (both required):
$ ./dnsserver [-p port] [-n name]
    TODO: parse port as the port number to bind DNS server to
    TODO: parse name as the CDN-specific name that our server translates to an IP
    address
    TODO: The DNS server only needs to respond to A queries for the site specified
    in the project description.

Implementation idea:
    - port range: 20380-20389

    - ssh into the dns server
        `ssh -i ssh-ed25519-quach.l.priv quach.l@cdn-dns.khoury.northeastern.edu`
    
    - build a DNS server that is able to return the IP address of the HTTP cache
      server with the lowest latency (closest to the client?).
    - check if that cache server (?
      `https://cdn-http4.khoury.northeastern.edu/`) has the requested webpage.
      If the cache server has the webpage stored, then the DNS server should
      send the webpage to the client via the HTTP cache server. If the cache
      server doesn't have the webpage, then the DNS server should send the
      request to the origin server, `http://cs5700cdnorigin.ccs.neu.edu:8080`,
      and then send the webpage to the client via the HTTP cache server. 

    - upload the dnsserver.py file to the server
        `scp -i ssh/ssh-ed25519-quach.l.priv dnsserver.py quach.l@cdn-dns.khoury.northeastern.edu:~/`
        
    - run it
        `quach.l@cdn-dns:~$ python3 dnsserver.py `
        `python3 dnsserver.py -p 20380 -n cs5700cdn.example.com`

    - dig command to test the DNS server
        `dig @cdn-dns.khoury.northeastern.edu -p 20380 cs5700cdn.example.com`
      '''


def parse_args():
    '''
    Parses command line arguments.
    '''
    parser = argparse.ArgumentParser(description='DNS Server')
    parser.add_argument('-p', '--port', required=True, type=int, help='Port number to bind DNS server to')
    parser.add_argument('-n', '--name', required=True, type=str, help='CDN-specific name to translate')
    return parser.parse_args()

