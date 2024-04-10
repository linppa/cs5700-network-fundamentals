#!/usr/bin/env python3

import argparse
import dnslib
import socket

# import geoip2 
# import urllib
# import curl
# import requests

'''
DNS server called using (both required):
$ ./dnsserver [-p port] [-n name]

Implementation notes:
    - my port range: 20380-20389

    - ssh into build server
        `ssh linppa@cs5700cdnproject.ccs.neu.edu`

    - ssh into the dns server
        `ssh -i ssh-ed25519-quach.l.priv quach.l@cdn-dns.khoury.northeastern.edu`

    - upload the dnsserver.py file to the server
        `scp -i ssh/ssh-ed25519-quach.l.priv dnsserver.py quach.l@cdn-dns.khoury.northeastern.edu:~/`
    
    - run dns server
        `python3 dnsserver.py -p 20380 -n cs5700cdn.example.com`

    - dig command to test the DNS server
        `dig @cdn-dns.khoury.northeastern.edu -p 20380 cs5700cdn.example.com`

    -
      '''


# server name & IP address of HTTP cache servers, TODO: check if correct IP
REPLICA_SERVERS = {
    'cdn-http3.khoury.northeastern.edu': '45.33.55.171',
    'cdn-http4.khoury.northeastern.edu': '170.187.142.220', 
    'cdn-http7.khoury.northeastern.edu': '213.168.249.157', 
    'cdn-http11.khoury.northeastern.edu': '139.162.82.207', 
    'cdn-http14.khoury.northeastern.edu': '45.79.124.209', 
    'cdn-http15.khoury.northeastern.edu': '192.53.123.145', 
    'cdn-http16.khoury.northeastern.edu': '192.46.221.203',
}
server_order = list(REPLICA_SERVERS.keys()) # ordering for round-robin implementation
current_index = 0 # counter to keep track of the current replica server


def parse_args():
    '''
    Parses command line arguments.
    '''
    parser = argparse.ArgumentParser(description='DNS Server')
    parser.add_argument('-p', '--port', required=True, type=int, help='Port number to bind DNS server to')
    parser.add_argument('-n', '--name', required=True, type=str, help='CDN-specific name to translate')
    return parser.parse_args()


def run_dns_server(port, cdn_name):
    '''
    Runs the DNS server.
    '''
    # create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))
    print(f' ** dns server running on port {port} ** ')

    try:
        while True:
            # receive data from client
            data, client_address = server_socket.recvfrom(1024)
            query = dnslib.DNSRecord.parse(data)
            print(f' ** received query from CLIENT ADDRESS: {client_address}, QUERY: {query} ** ')

            # respond to 'A Queries' for specified CDN name (cs5700cdn.example.com)
            if query.q.qtype == dnslib.QTYPE.A and query.q.qname == cdn_name:

                # get the best geographic replica for the client's IP address
                # TODO: implement get_closest_replica() INSTEAD of round-robin
                
                server_name, ip_address = get_next_replica() # NOTE: round-robin implementation
                response = query.reply()

                # create 'A record' with replica/cache IP & add to response to send to back to client
                response.add_answer(dnslib.RR(query.q.qname, # domain name in query
                                              dnslib.QTYPE.A, # query type (A record)
                                              rdata=dnslib.A(ip_address), # IP address of replica/cache, TODO: get replica's IP address
                                              ttl=120)) #time-to-live, how long record is cached, TODO: check if correct TTL?
                server_socket.sendto(response.pack(), client_address)
                print(f' ** sent response to CLIENT ADDRESS: {client_address}, & RESPONSE: {response} ** ')
                print(f' \n =============================== \n ')
    except Exception as e:
        print(f' ** error: {e} ** ')
    finally:
        server_socket.close()


def get_closest_replica(client_ip_address):
    '''
    Returns the best geographic replica for the client's IP address.
    '''
    pass
    # TODO: geoip2

def get_next_replica():
    '''
    Testing a round-robin implementation.
    '''
    global current_index
    # pick next server name based on current index counter
    current_server_name = server_order[current_index]
    # get IP address of current server name
    current_server_ip = REPLICA_SERVERS[current_server_name]
    # increment counter to update index for next call
    current_index = (current_index + 1) % len(server_order) # modulo to loop back to beginning of list
    return current_server_name, current_server_ip


def main():
    args = parse_args()
    run_dns_server(args.port, args.name)


if __name__ == "__main__":
    main()