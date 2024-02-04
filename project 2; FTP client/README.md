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
> https://stackoverflow.com/questions/20165843/argparse-how-to-handle-variable-number-of-arguments-nargs
> https://docs.python.org/3/library/urllib.parse.html
> https://setapp.com/how-to/ftp-on-mac#



## How to Install & Run Program
Ensure that the following files are in the same directory: `ftp-source-code.py`.

The following files are included for the sake of submission requirements. One
is a Makefile, however, does not have a significant impact on the program since we are using Python:
`Makefile`. 

The script command to run the client program executes in this format:
> `$ ./4700ftp [operation] [param1] [param2]`

Remote files & directories are specified in the following URL format:
`ftp://[USER[:PASSWORD]@]HOST[:PORT]/PATH`

For example, to list the files in the FTP server, you would
execute the following script to the command line depending on the location of
the directory:
`$ ./4700ftp ls ftp://bob:s3cr3t@ftp.example.com/`
`$ ./4700ftp ls ftp://bob:s3cr3t@ftp.example.com/documents/homeworks`

Another example, to copy a file from the local machine to the FTP server (and
vice versa), you would execute the following script to the command line
depending on the location of the directory:
`$ ./4700ftp cp other-hw/essay.pdf ftp://bob:s3cr3t@ftp.example.com/documents/homeworks-v2/essay.pdf`
`$ ./4700ftp cp ftp://bob:s3cr3t@ftp.example.com/documents/todo-list.txt other-hw/todo-list.txt`


## How to Use the Program
This FTP client supports the following operations:

`ls <URL>`                 Print out the directory listing from the FTP server at the given URL
`mkdir <URL>`              Create a new directory on the FTP server at the given URL
`rm <URL> `                Delete the file on the FTP server at the given URL
`rmdir <URL> `             Delete the directory on the FTP server at the given URL
`cp <ARG1> <ARG2>   `      Copy the file given by ARG1 to the file given by
                          ARG2. If ARG1 is a local file, then ARG2 must be a URL, and vice-versa.
`mv <ARG1> <ARG2> `        Move the file given by ARG1 to the file given by
                          ARG2. If ARG1 is a local file, then ARG2 must be a URL, and vice-versa.


## Design Strategies
The project was implemented in the following order, as suggested by the
"suggested implementation approach" section:
- [x] command line parsing
- [x] connection establishment
    - [x] login with USER & PASS commands
    - [x] set TYPE, MODE, & STRU commands
- [ ] PASV & LIST command (requires data channel)
    - [x] parse PASV response to get IP & port
    - [x] establish data channel connection
- [x] MKD & RMD commands (don't require data channel)
- [ ] STORE, RETR & DELE commands
    - [ ] STORE (upload)
    - [ ] RETR (download)
    - [ ] DELE (delete)

- [ ] double check client works successfully on a CCIS linux machine (login.ccs.neu.edu)


