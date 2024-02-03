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
import re
    
def parse_commands():
    parser = argparse.ArgumentParser(description='Executes the FTP client command line.')
    # required arguments
    parser.add_argument('operation', type=str, choices=['ls', 'mkdir', 'rm', 'rmdir', 'cp', 'mv'], help='Enter valid operation.')
    parser.add_argument('param1', type=str, nargs='?', default='', help='Enter valid path/URL to file/directory on local filesystem or FTP server.')
    parser.add_argument('param2', type=str, nargs='?', default='', help='Enter valid path/URL to file/directory on local filesystem or FTP server.')
    # optional arguments
    parser.add_argument('-v', '--verbose', action='store_true', help='Print all messages to & from FTP server.')
    
    # parse arguments
    arguments = parser.parse_args()
    
    # parse urls
    if arguments.param1 and arguments.param1.startswith('ftp://'):
        username, password, hostname, port, path = parse_urls(arguments)
    else:
        local_path = arguments.param1
        
    if arguments.param2 and arguments.param2.startswith('ftp://'):
        username, password, hostname, port, path = parse_urls(arguments)
    else:
        local_path = arguments.param2
    
        
    print(f"Args: {arguments}")
    return arguments, username, password, hostname, port, path, local_path


def parse_urls(arguments):
    # initialize default & variables
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
    
    # parse components from url
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


def run_client(port, hostname, username, password, arguments):
    try:
        # create client socket to connect with server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((hostname, port))
        
        # receive hello from server
        while True:
            print(client_socket.recv(4096).decode())
            break
        
        # send username to server
        client_socket.sendall(f"USER {username}\r\n".encode())
        print(f"USER {username}")
        while True:
            print(client_socket.recv(4096).decode())
            break
        
        # send pass to server
        client_socket.sendall(f"PASS {password}\r\n".encode())
        print(f"PASS {password}")
        while True:
            print(client_socket.recv(4096).decode())
            break
        
        # set type to 8-bit binary data mode
        client_socket.sendall("TYPE I\r\n".encode())
        print("TYPE I; 8-bit binary data mode")
        while True:
            print(client_socket.recv(4096).decode())
            break
        
        # set mode to stream mode
        client_socket.sendall("MODE S\r\n".encode())
        print("MODE; stream mode")
        while True:
            print(client_socket.recv(4096).decode())
            break
        
        # set stru to file-oriented mode
        client_socket.sendall("STRU F\r\n".encode())
        print("STRU; file-oriented mode")
        while True:
            print(client_socket.recv(4096).decode())
            break
        
        # handle operations from command line
        # ls
        if arguments.operation == 'ls':
            handle_ls(arguments, client_socket)
            
        
        
        # quit server
        client_socket.sendall("QUIT\r\n".encode())
        print("QUIT")
        while True:
            print(client_socket.recv(4096).decode())
            break
        
        # close connection
        client_socket.close()
        
    except Exception as e:
        print(f"Error: {e}")
        return None
        
def handle_ls(arguments, client_socket):
    # ask server for data socket
    data_socket = handle_pasv(client_socket)
    
    # send ls command to server
    client_socket.sendall(f"LIST {arguments.param1}\r\n".encode())
    print(f"LIST from {arguments.param1}")

    # receive data from server
    list = data_socket.recv(4096).decode()
    print(f"LIST Data: {list}")
    
    
    # close data socket
    data_socket.close()
        
        
def handle_pasv(client_socket):
    # send pasv command to server
    client_socket.sendall("PASV\r\n".encode())
    response = client_socket.recv(4096).decode()
    print(response)
    
    # parse response, '227 Entering Passive Mode (1,2,3,4,5,6).'
    # split first parenthesis, '1,2,3,4,5,6).'
    first_split = response.split('(')[1]
    # split second parenthesis, '1,2,3,4,5,6'
    second_split = first_split.split(')')[0]
    numbers = second_split.split(',')
    
    # ip; first 4 numbers
    ip = '.'.join(numbers[:4])
    # port; left shift 8 bits (mult by 256) & add next number
    port = (int(numbers[4]) * 256) + int(numbers[5])
        
    # create data socket to connect with server
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((ip, port))
    print(f"Data socket connected; {ip}:{port}")
    
    return data_socket


def main():
    # parse command line arguments
    arguments, username, password, hostname, port, path, local_path = parse_commands()
    
    # run client
    run_client(port, hostname, username, password, arguments)
    
if __name__ == '__main__':
    main()