# Project 4: Reliable Transport Protocol

## Authors:
- [Linda Quach](https://github.com/linppa)

- Starter code provided by Professor Christo Wilson at Northeastern University.
- CS 5700 - Network Fundamentals - Spring 2024

## Description:
- In this project we designed a simple transport protocol that provides reliable
  datagram service. The protocol is responsible for ensuring that all packets
  are delivered in order, without duplicates, missing packets, or errors. The
  protocol is implemented with a virtual environment that emulates an unreliable
  network.


## How to install & run:
- The command line syntax for the sending program is given below. The sender
  program takes command line arguments of the remote IP address and UDP port
  number. The syntax for launching your sending program is therefore:

> `$ ./4700send <recv_host> <recv_port>`
- recv_host (Required) The domain name (e.g., “foo.com”) or IP address (e.g.,
  “1.2.3.4”) of the remote host.
- recv_port (Required) The UDP port of the remote host.

The command line syntax for the receiving program is given below.
> `$ ./4700recv`

- Rather than testing our on a real network, we are testing it in a simulator
  implemented in a script named `run`. The simulator comes with a suite of
  configuration files in the `configs` directory that our router is able to
  handle. To run the simulator, the following command is used:

> `$ ./run <config-file>`

- Otherwise, the router can be test with the entire test suite by running the
  following command to run the `test` file:

> `$ ./test`


## Design & Implementation:
- Before implementation of the TCP protocol on top of UDP, I reviewed the major
  differences between the two protocols. I also needed to understand the basic
  structure of the TCP header and the fields that are used to ensure reliable
  data transfer. That way, I could implement a similar simple protocol to mimic.

- Utilizing the test suite, I tackled the project in a step-by-step manner, and
  following the tips & hints provided by the professor in the "implementation
  strategy" section of the assignment description.

- After completing the basics of the project, I attempted to look at the struct
  module, to attempts to minimize the byte size of data being sent. I also tried
  to shave off bytes from the packet size by using smaller variable names and
  attempted to increase the cwnd size up to 10.

- Since the deadline was extended, I was able to play with zlib and base64 with
  the struct module to encode and decode the packet to even further minimize the
  byte size of the packet. It was a good learning experience to play around with
  these modules, but I'm not sure if I fully implemented it correctly. After
  discussing with the professor, I realized that I was so focused on trying to
  accomadate the JSON encoded packet headers, that I didn't realize that I could
  just use Struct to create a fixed-size binary encoded packet instead.
  Therefore, I made some minor changes in the packet format to send it as a
  binary encoded packet instead of a JSON encoded packet.



## Challenges:
- The biggest challenge was figuring out how to design a packet format that
  would be flexible enough to handle the future tests in the configuration
  suite. I learned from the last project that it was important to have a good
  foundation/adequate data structure to build upon, otherwise we would have to
  scrap the design and start over. Luckily I found a nice guide from MIT that
  helped me highlight fields that I needed to keep in mind, such as the window
  size, sequence number, and checksum.

- Another major challenge was deciphering the test suite and what the intented
  output/behavior of what the unreliable network was doing. At first it was
  difficult to debug because I didn't realize that print statements affected the
  output. After struggling for some time, I realized that the log function
  existed as a part of the starter code.

- That highlights another challenge, which is initially figuring out what
  someone else's code is doing. This ultimately also led my original partner and
  I to split up and work on the project separately. I think that was a good
  mutal situation since it was difficult for us to fully learn about the
  protocol without implementing the project from start to finish.

- Trying to figure out how to compress the data was a challenge since Struct
  only works with fixed-size data, such as the sequence number, time, and
  checksum. The actual data block was a variable size, so I had to figure out
  how to compress it. After discussing with the professor, I realized that I was
  so focused on trying to accomadate the JSON encoded packet headers, that I
  didn't realize that I could just use Struct to create a fixed-size binary
  encoded packet instead.


## Testing:
- The protocol was tested by utilizing the test suite provided by the professor,
  along with debugging using log/print statements. Since the test suite help to
  implement the protocol in a step-by-step manner, it was helpful to build the
  protocol with each test.

- Log statements were heavily used to visualize the behavior of the protocol
  at each step, and decipher what each test in the unrilable network was doing.


## Resources:
> https://educatedguesswork.org/posts/transport-protocols-intro/
> https://web.mit.edu/6.033/2018/wwwdocs/assignments/rtp_guide.pdf
> https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
> https://docs.python.org/3/library/struct.html#struct-format-strings
> https://docs.python.org/3/library/base64.html
> https://stackoverflow.com/questions/52081331/trying-to-print-out-json-from-a-decoded-base64-python
> https://docs.python.org/3/library/zlib.html


