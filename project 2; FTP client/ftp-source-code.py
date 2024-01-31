'''
    ssh linppa@login.khoury.northeastern.edu
    [linppa@login-students ~]$ 4700-ftp-password 002613766
    Your password is: b4da98eadabe2ce0801f46a20b35f587a70128969ec5cba5e0535f1f4ad7b076
'''

import socket
import re
import argparse
import os


def parse_command():
    parser = argparse.ArgumentParser(description='Executes the FTP client command line.')
    # required arguments
    parser.add_argument('operation', type=str, choices=['ls', 'mkdir', 'rm', 'rmdir', 'cp', 'mv'], help='Enter valid operation.')
    parser.add_argument('param1', type=str, help='Enter valid path/URL to file/directory on local filesystem or FTP server.')
    parser.add_argument('param2', type=str, nargs='?', help='Enter valid path/URL to file/directory on local filesystem or FTP server.')
    # optional arguments
    parser.add_argument('-v', '--verbose', action='store_true', help='Print all messages to & from FTP server.')
    
    arguments = parser.parse_args()
    return arguments


def connect_server(hostname, port):
    try:
        # connect to server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((hostname, port))
        
        # receive hello
        response = server.recv(4096).decode()
        return server, response
    
    # handle errors
    except Exception as e:
        print(e)
        return None, None
    
    
def send_command(server, command):
    try:
        # send command
        server.sendall(command.encode() + b'\r\n')
        
        # receive response
        response = server.recv(4096).decode()
        return response
    
    # handle errors
    except Exception as e:
        print(e)
        return None


def main():
    # parse command line arguments
    arguments = parse_command()
    operation = arguments.operation
    param1 = arguments.param1
    param2 = arguments.param2
    verbose = arguments.verbose
    
    # default hostname and port
    hostname = 'ftp://ftp.4700.network'
    port = 21
        
    # connect to FTP server
    server, response = connect_server(hostname, port)
    if server is None:
        return
    elif verbose:
        print(response)
    else:
        print('Connected to FTP server.')
        
    # send username
    username_response = send_command(server, 'USER linppa')
    print(username_response)
    
    # send password
    pass_response = send_command(server, 'PASS b4da98eadabe2ce0801f46a20b35f587a70128969ec5cba5e0535f1f4ad7b076')
    print(pass_response)
    
    
    
        
    