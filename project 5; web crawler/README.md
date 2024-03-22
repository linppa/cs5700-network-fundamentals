# Project 5; Web Crawler

## Authors:
- [Linda Quach](https://github.com/linppa)

- Starter code provided by Professor Christo Wilson at Northeastern University.

## Description:
- This project was intended to help us understand how web crawlers work and how
  to implement one. The goal was to create a web crawler that would traverse a
  given site and find the secret flags hidden within the site. The site was
  Fakebook, a mock social media site that required a login to access the
  content. The site can be found here: [Fakebook](https://www.3700.network/fakebook/).


## How to install & run:
- The command line syntax for the running the program is given below:
> `$ ./crawler <-s server> <-p port> <username> <password>`

- The `-s` and `-p` arguments are each optional and they represent the server and
  port your code should crawl, respectively. If either or both are not provided,
  use `www.3700.network` for the server and `443` for the port.

- The `username` and `password` arguments are required and are used to login to
  Fakebook.
  
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

- Then, I implemented the initial login, which required me to parse the csrf
  middleware token from the HTML content and send it back to the server along
  with the required form information such as username and password. Once the
  POST request, I recevied the redirect URL to the root page.

- From the inital login redirect, I utilized the HTML parser to find the links
  as well as the secret flags. The data structures selected for the links were
  sets, becuase I wanted to avoid duplicates links. 

- In a loop, the program continues to crawl each link until either the frontier
  is empty or the 5 secret flags had been found, handling status codes and error
  codes as it traverses. 
  
- Since I did not implement multi-threading, the program was quite slow in
  traversing the links, taking upwards to 10-30 minutes to find all the secret
  flags. This could be improved upon in the future.

- At the very end, the program prints out the secret flags in the order they were
  found.


## Challenges:
- It took quite a bit of time to fiddle with the POST request formatting to
  figure out exactly what was needed for the formatting. Several resources were
  consulted in the links below this document.

- Since the crawler was not multi-threaded, it was initially difficult to figure
  out if the traversal logic was correct and not accidentally caught in a loop.
  Using print statements to see the frontier and history helped me debug the
  potential issues.

## Testing:
- Numerous print statements were utilized throughout the code to debug and
  visually observe how the code was behaving. 

- A testing file was used to test the parsing of the HTML content and the
  extraction of the links and secret flags without having to traverse the entire
  site.

## Resources:
> https://www.jmarshall.com/easy/http/
> https://fasterthanli.me/articles/the-http-crash-course-nobody-asked-for
> https://docs.python.org/3/library/urllib.parse.html
> https://docs.python.org/3/library/html.parser.html#module-html.parser
> https://stackoverflow.com/questions/79780/parsing-http-headers
> 

