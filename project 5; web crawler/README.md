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

- Next, after implementing TLS encryption, I was able to see the HTTP headers
  along with the HTML content of the root page. It took me quite a while to try
  to understand the information that I needed from the given headers and HTML; I
  pulled out the basic information I could see including the initial set-cookies
  and status code from the header, and the csrf token in the HTML.

- Then, I implemented the actual login using the POST request.


## Challenges:
- 


## Testing:
- 


## Resources:
> https://www.jmarshall.com/easy/http/
> https://fasterthanli.me/articles/the-http-crash-course-nobody-asked-for
> https://docs.python.org/3/library/urllib.parse.html
> https://docs.python.org/3/library/html.parser.html#module-html.parser
> https://stackoverflow.com/questions/79780/parsing-http-headers
> 

