#!/usr/bin/env python3
'''
    ssh linppa@login.khoury.northeastern.edu
    [linppa@login-students ~]$ 4700-ftp-password 002613766
    Your password is:
    b4da98eadabe2ce0801f46a20b35f587a70128969ec5cba5e0535f1f4ad7b076
    
    ./ftp-source-code.py ls
    ftp://linppa:b4da98eadabe2ce0801f46a20b35f587a70128969ec5cba5e0535f1f4ad7b076@ftp.4700.network
    -verbose  
    
'''

import socket
import argparse
import urllib.parse
    
def parse_commands():
    parser = argparse.ArgumentParser(description='Executes the FTP client command line.')
    # required arguments
    parser.add_argument('operation', type=str, choices=['ls', 'mkdir', 'rm', 'rmdir', 'cp', 'mv'], help='Enter valid operation.')
    parser.add_argument('param1', type=str, nargs='?', default='', help='Enter valid path/URL to file/directory on local filesystem or FTP server.')
    parser.add_argument('param2', type=str, nargs='?', default='', help='Enter valid path/URL to file/directory on local filesystem or FTP server.')
    # optional arguments
    parser.add_argument('-verbose', action='store_true', help='Print all messages to & from FTP server.')
    
    # parse arguments
    arguments = parser.parse_args()
    
    # parse urls
    if arguments.param1 and arguments.param1.startswith('ftp://'):
        username, password, hostname, port, path = parse_urls(arguments.param1, arguments)
    else:
        local_path = arguments.param1
        
    if arguments.param2 and arguments.param2.startswith('ftp://'):
        username, password, hostname, port, path = parse_urls(arguments.param2, arguments)
    else:
        local_path = arguments.param2
    
        
    print(f"Args: {arguments}")
    return arguments, username, password, hostname, port, path, local_path


def parse_urls(url, arguments):
    # initialize variables
    default_hostname = 'ftp.4700.network'
    default_port = 21
    default_username = 'anonymous'
    default_password = None
    default_path = '/'
    
    username = default_username
    password = default_password
    hostname = default_hostname
    port = default_port
    path = default_path
    
    # parse user, pass, hostname, port, path from param1
    # ftp://[USER[:PASSWORD]@]HOST[:PORT]/PATH
    # $ ./4700ftp ls ftp://bob:s3cr3t@ftp.example.com/
    
    if arguments.param1 and arguments.param1.startswith('ftp://'):
        parsed_url = urllib.parse.urlparse(arguments.param1)
        
        # if username provided
        if parsed_url.username:
            username = parsed_url.username
        else:
            username = default_username
            
        # if password provided
        if parsed_url.password:
            password = parsed_url.password
        else:
            password = default_password
            
        # if hostname provided
        if parsed_url.hostname:
            hostname = parsed_url.hostname
        else:
            hostname = default_hostname
            
        # if port provided
        if parsed_url.port:
            port = parsed_url.port
        else:
            port = default_port
            
        # if path provided
        if parsed_url.path:
            path = parsed_url.path
        else:
            path = default_path
            
    return username, password, hostname, port, path


def run_client(port, hostname, username, password):
    try:
        # create socket to connect with server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((hostname, port))
        
        # receive hello from server
        while True:
            print(client.recv(4096).decode())
            break
        
        # send username to server
        client.sendall(f"USER {username}\r\n".encode())
        print(f"USER {username}")
        while True:
            print(client.recv(4096).decode())
            break
        
        # send pass to server
        client.sendall(f"PASS {password}\r\n".encode())
        print(f"PASS {password}")
        while True:
            print(client.recv(4096).decode())
            break
        
        # quit server
        client.sendall("QUIT\r\n".encode())
        print("QUIT")
        while True:
            print(client.recv(4096).decode())
            break
        
        # close connection
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        return None
        
        
def main():
    # parse command line arguments
    arguments, username, password, hostname, port, path, local_path = parse_commands()
    # operation = arguments.operation
    # param1 = arguments.param1
    # param2 = arguments.param2
    # verbose = arguments.verbose
    
    # run client
    run_client(port, hostname, username, password)
    
if __name__ == '__main__':
    main()