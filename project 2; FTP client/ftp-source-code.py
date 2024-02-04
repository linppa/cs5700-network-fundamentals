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
    parser.add_argument('source_url', type=str, help='Enter valid path/URL to file/directory.')
    # optional arguments
    parser.add_argument('destination_url', type=str, nargs='?', help='Enter valid path/URL to file/directory.')

    # parse arguments
    arguments = parser.parse_args()

    # # cp & mv require destination_url
    # if arguments.operation in ['cp', 'mv']:
    #     if not arguments.destination_url:
    #         parser.error(f"{arguments.operation} needs source & destination path.")

    return arguments

    
def parse_ftp_url(url):
    parsed_url = urllib.parse.urlparse(url)
    
    if not url.startswith('ftp://'):
        return None, None, None, None, url

    # if username provided
    if parsed_url.username:
        username = parsed_url.username
    else:
        username = 'anonymous'
        
    # if password provided
    if parsed_url.password:
        password = parsed_url.password
    else:
        password = ''
        
    # if hostname provided
    if parsed_url.hostname:
        hostname = parsed_url.hostname
    else:
        hostname = 'ftp.4700.network'
        
    # if port provided
    if parsed_url.port:
        port = parsed_url.port
    else:
        port = 21
        
    # if path provided
    if parsed_url.path:
        path = parsed_url.path
    else:
        path = '/'
    
    return port, hostname, username, password, path
    


def run_client(arguments):
    # remote_path = ''
    # local_path = ''
    # path = ''
        
    # if arguments.operation in ['cp', 'mv']:
    #     if arguments.source_url.startswith('ftp://'):
    #         port, hostname, username, password, remote_path = parse_ftp_url(arguments.source_url)
    #         local_path = arguments.destination_url
    #     elif arguments.destination_url.startswith('ftp://'):
    #         port, hostname, username, password, remote_path = parse_ftp_url(arguments.destination_url)
    #         local_path = arguments.source_url        
        
    # if arguments.operation in ['cp', 'mv']:
    #     if 'ftp://' in arguments.source_url or 'ftp://' in arguments.destination_url:
    #         handle_cp(arguments)
    #     else:
    #         print(f"Error: {arguments.operation} needs source & destination path.")
    
    # if arguments.operation in ['ls', 'mkdir', 'rm', 'rmdir']:
    #     port, hostname, username, password, path = parse_ftp_url(arguments.source_url)
    # else:
    #     if arguments.source_url.startswith('ftp://'):
    #         port, hostname, username, password, remote_path = parse_ftp_url(arguments.source_url)
    #         local_path = arguments.destination_url
    #     elif arguments.destination_url.startswith('ftp://'):
    #         port, hostname, username, password, remote_path = parse_ftp_url(arguments.destination_url)
    #         local_path = arguments.source_url
    #     else:
    #         print(f"Error: {arguments.operation} needs source & destination path.")
    #         return None
    
    port, hostname, username, password, path = parse_ftp_url(arguments.source_url)
    local_path = ''
    remote_path = ''
    
    if arguments.operation in ['cp', 'mv']:
        if arguments.source_url.startswith('ftp://'):
            remote_path = path
            local_path = arguments.destination_url
        elif arguments.destination_url and arguments.destination_url.startswith('ftp://'):
            port, hostname, username, password, remote_path = parse_ftp_url(arguments.destination_url)
            local_path = arguments.source_url
        else:
            print(f"Error: {arguments.operation} needs source & destination path.")
            return None
    
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
        
        # ----- handle operations -----
        # ls
        if arguments.operation == 'ls':
            handle_ls(client_socket, path)
            
        # mkdir
        elif arguments.operation == 'mkdir':
            handle_mkdir(client_socket, path)
            
        # rmdir
        elif arguments.operation == 'rmdir':
            handle_rmdir(client_socket, path)
            
        # cp
        elif arguments.operation == 'cp':
            handle_cp(arguments, client_socket, local_path, remote_path)
            
        # mv
        elif arguments.operation == 'mv':
            pass
        
        # rm
        elif arguments.operation == 'rm':
            pass
        
        
        
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

       
def handle_ls(client_socket, path):
    # send pasv command to server
    data_socket = handle_pasv(client_socket)
    
    # send ls command to server
    client_socket.sendall(f"LIST {path}\r\n".encode())
    print(client_socket.recv(4096).decode())

    # receive data from server data socket
    data_list = data_socket.recv(4096).decode()
    print(f"LIST Data: \n{data_list}")
    
    # close data socket
    data_socket.close()
    

def handle_mkdir(client_socket, path):
    # send mkdir command to server
    client_socket.sendall(f"MKD {path}\r\n".encode())
    print(client_socket.recv(4096).decode())


def handle_rmdir(client_socket, path):
    # send rmdir command to server
    client_socket.sendall(f"RMD {path}\r\n".encode())
    print(client_socket.recv(4096).decode())
    
    
def handle_cp(arguments, client_socket, local_path, remote_path):
    if arguments.source_url.startswith('ftp://'):
        handle_stor(client_socket, local_path, remote_path)
    elif arguments.destination_url.startswith('ftp://'):
        handle_retr(client_socket, remote_path, local_path)
    else:
        print(f"Error: {arguments.operation} needs source & destination path.")
        
        

            

def handle_stor(client_socket, local_path, remote_path):
    # send pasv command to server
    data_socket = handle_pasv(client_socket)
    
    # send stor/upload command to server
    client_socket.sendall(f"STOR {remote_path}\r\n".encode())
    print(client_socket.recv(4096).decode())
    
    # send file to server data socket
    with open(local_path, 'rb') as file:
        data = file.read(4096)
        while data:
            data_socket.sendall(data)
            data = file.read(4096)
    
    # close data socket
    data_socket.close()
    print(f"File {local_path} sent to {remote_path}")
    

def handle_retr(client_socket, remote_path, local_path):
    # send pasv command to server
    data_socket = handle_pasv(client_socket)
    
    # send retr/download command to server
    client_socket.sendall(f"RETR {remote_path}\r\n".encode())
    print(client_socket.recv(4096).decode())
    
    # receive file from server data socket
    with open(local_path, 'wb') as file:
        while True:
            data = data_socket.recv(4096)
            if not data:
                break
            file.write(data)
    
    # close data socket
    data_socket.close()
    print(f"File {remote_path} received to {local_path}")
    

def handle_mv():
    pass

def handle_rm():
    pass

    
def main():
    # parse command line arguments
    arguments = parse_commands()

    # run client
    run_client(arguments)
    
if __name__ == '__main__':
    main()