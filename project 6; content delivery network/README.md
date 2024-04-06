# Project 6; Content  Delivery Network

## Authors:
- [Linda Quach](https://github.com/linppa)


## Description:
- 


## How to install & run:
- `pip install dnslib`
- `pip install pycurl`
- `pip install requests`


## Design & Implementation:
- Before starting the project, we needed to review CDN's and what the goals of
  the project were. Initially we were a bit confused at what parts of the CDN
  we needed to build and which parts were already provided to us. 
  
- After figuring out how to ssh into the DNS server, I began to brainstorm how
  to implement the DNS server. Although still slightly confused about the
  bigger picture, I felt I needed to build a DNS server that is able to
  return the IP address of the HTTP cache server with the lowest latency
  (closest to the client?). Then, I need to check if that cache server (? `https://cdn-http4.khoury.northeastern.edu/`) has the
  requested webpage. If the cache server has the webpage stored, then the DNS
  server should send the webpage to the client via the HTTP cache server. If
  the cache server doesn't have the webpage, then the DNS server should send
  the request to the origin server, `http://cs5700cdnorigin.ccs.neu.edu:8080`,
  and then send the webpage to the client via the HTTP cache server.


## Challenges:
- At the start of imlementing the project, we needed to review our basic
  understanding of CDN's and the big picture of what the project wanted us to
  accomplish. On top of that, we were given ssh private & public keys
  the professor provided in an email, which I had no clue what to do with them,
  initially. After some help, I was able to ssh into the DNS server to start.

- There was a lot of confusing on my part about how to deploy my code on my
  local machine to the DNS server. I was able to figure out the scp command to
  copy my files over.

## Testing:
- 

## Resources:
> https://pythonbasics.org/webserver/
> https://docs.python.org/3/library/http.server.html
> https://pypi.org/project/dnslib/
> https://github.com/paulc/dnslib
> https://www.geeksforgeeks.org/designing-content-delivery-network-cdn-system-design/#
> 
> 

