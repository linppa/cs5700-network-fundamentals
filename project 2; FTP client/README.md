# Project 1: Socket Basics

## Description
The goal of this project is to deepen our ability to write network code. Since
we learned to open a socket and send & receive simple messages, in the first
project, we will now implement a client for a more complex protocol. This
project will have more features and use two sockets instead of one.

In this project, I develop a client for the File Transfer Protocol (FTP). The
server has been setup for us to use for development and testing. The server is
available at `ftp://ftp.4700.network`.

The client runs on the command line and supports the following operations:
directory listing, making directories, file deletion, directory deletion,
copying files to and from the FTP server, and moving files on the FTP server.


## Resources
The following resources were referenced during the implementation of
this project:

> https://stackoverflow.com/questions/46645755/makefile-to-do-nothing


## How to Install & Run Program
Ensure that the following files are in the same directory: `ftp-source-code.py`.

The following files are included for the sake of submission requirements. One
is a Makefile, however, does not have a significant impact on the program since we are using Python:
`Makefile`. 

The script command to run the client program executes in this format:
> `$ ./4700ftp [operation] [param1] [param2]`


## How to Use the Program



## Design Strategies
The project was implemented in the following order, as suggested by the
"suggested implementaiton approach" section:
- [x] command line parsing
- [ ] connection establishment
- [ ] MKD & RMD commands
- [ ] PASV & LIST command
- [ ] STORE, RETR & DELE commands
- [ ] double check client works successfully on a CCIS linux machine (login.ccs.neu.edu)


