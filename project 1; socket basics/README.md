# Project 1: Socket Basics

## Description
This assignment was intended to help familiarize us to writing simpler network
code. A client program is implemented to play a variation of the game "Wordle".
The client makes guesses for the secret word and receives feedback information
about how close the guess is. When the client guesses the word, the server
returns a "secret flag" message.

The program utilizes Python language, and the following libraries that are a
part of the python standard library: socket,
argparse, ssl, json, and random.

As an Align MSCS student with no background knowledge in network programming, the biggest challenges encountered during this project
was self-teaching and reading over the documentation to learn about socket
basics.

As such, the following resources were referenced during the implementation of
this project:

> https://docs.python.org/3/library/socket.html
> https://docs.python.org/3/library/argparse.html#the-parse-args-method
> https://www.datacamp.com/tutorial/a-complete-guide-to-socket-programming-in-python
> https://www.geeksforgeeks.org/open-a-file-in-python/#
> https://docs.python.org/3/library/ssl.html
> https://docs.python.org/3/library/json.html
> https://www.geeksforgeeks.org/enumerate-in-python/
> https://stackoverflow.com/questions/46645755/makefile-to-do-nothing

## How to Install & Run Program
Ensure that the following files are in the same directory: `client`,
`project1-words.txt`.

The following files are included for the sake of submission requirements. One
contains the expected secret flags obtained, The other is a Makefile, however, does not have a significant impact on the program since we are using Python:
`Makefile`, `secret_flags`. 

The script command to run the client program executes in this format:
> `$ ./client <-p port> <-s> <hostname> <Northeastern-username>``

## How to Use the Program
The client program is designed to pull from a provided list of words to use as
word guesses. After running the script to start the program and connecting to
the server at `proj1.3700.network`, the program will play out the game without
any user input.


## Design Strategies
In attempt to improve the performance of the word guessing logic, there are a
couple helper functions that observe the feedback marks given by the server
after a word guess is made and filter out remaining words in the list that do
not match the marks. 

The initial guess made by the client server is the word `swing` since it
contains a good mix of consenants to help us filter out words initially. Originally, I was
using the random library to pick a randomized word from the word list, however,
the results were, as expected, too random.

Unfortunately, it is still not the most efficient design, however, it was an
improvement from just randomizing the word list, and iterating throught the
first 500 guesses until the server times out.

## Secret Flags
> 06dc810e9499f7b63a1ce1c8a7710ed4683f85076df41dc813b99f828accd58d
> 047c0e7ead18d62e0d186b6d35808892f72d5da2cc8c5ef2f759b46273f5f15a
