# Project 5; Web Crawler

## Authors:
- [Linda Quach](https://github.com/linppa)

- Starter code provided by Professor Christo Wilson at Northeastern University.

## Description:
- 


## How to install & run:
- The command line syntax for the sending program is given below:

> `$ ./crawler <-s server> <-p port> <username> <password>`

- The `-s` and `-p` arguments are each optional and they represent the server and
  port your code should crawl, respectively. If either or both are not provided,
  use `www.3700.network` for the server and `443` for the port. 
  
- The arguments username and password are used by the crawler to login to Fakebook.
  Assume that the root page for Fakebook is available at
  `https://<server>:<port>/fakebook/`. 
  Also assume that the login form for Fakebook is available at
  `https://<server>:<port>/accounts/login/?next=/fakebook/`.


## Design & Implementation:
- The first step was to dissect the given starter code to understand what I was
  working with. The code was a simple implementation of a client that simply
  fetches the root page of the site using HTTP 1.0. But it does not implement
  TLS so it receives an error message from the server.


## Challenges:
- 


## Testing:
- 


## Resources:
> https://www.jmarshall.com/easy/http/

