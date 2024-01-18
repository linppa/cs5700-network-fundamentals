#!/usr/bin/env python3

'''
https://docs.python.org/3/library/socket.html
https://docs.python.org/3/library/argparse.html#the-parse-args-method
https://www.datacamp.com/tutorial/a-complete-guide-to-socket-programming-in-python
https://www.geeksforgeeks.org/open-a-file-in-python/#
https://docs.python.org/3/library/ssl.html
https://docs.python.org/3/library/json.html
https://www.geeksforgeeks.org/enumerate-in-python/
'''

import socket
import argparse
import ssl
import json
import random


def open_word_file(filename):
    word_list = []
    
    # read file, strip whitespaces into list
    with open(filename, 'r') as file:
        for line in file:
            word_list.append(line.strip())
    
    return word_list



def parse_commands():
    parser = argparse.ArgumentParser(description='Executes the client program command line.')
    
    # optional arguments
    parser.add_argument('-p', '--port', action='store', type=int, default=27993)
    parser.add_argument('-s', '--tls_encryption', action='store_true', default=False)
    # required arguments
    parser.add_argument('hostname', action='store', type=str)
    parser.add_argument('northeastern_username', action='store', type=str)
    
    arguments = parser.parse_args()
    
    # determine port depending on encryption status
    if arguments.tls_encryption == True:
        # port not supplied, & tls encryption is true
        if arguments.port == 27993:
            arguments.port = 27994
            
    print(f"{arguments}")
    return arguments
    
    
    
def matches_mark(word, letter, position, mark):
    # letter at marked position matches expected letter
    if mark == 2:
        if word[position] == letter:
            return True
        else:
            return False
    # word contains letter but not at marked position
    if mark == 1:
        if letter in word and word[position] != letter:
            return True
        else:
            return False
    # letter doesnt match any position
    if mark == 0:
        if letter not in word:
            return True
        else:
            return False



def filter_word_list(word_list, guesses):
    # copy original list & filtered list
    filtered_list = word_list[:]
    
    for guess in guesses:
        word = guess['word']
        marks = guess['marks']
        
        # initialize list & assume all words match
        new_filtered_list = []
        for current_word in filtered_list:
            match = True
            # loop each letter & position in guessed word
            for i, letter in enumerate(word):
                # mark for current position
                mark = marks[i]
                if not matches_mark(current_word, letter, i, mark):
                    match = False
                    break
            if match:
                # word matches marks, add to filtered list
                new_filtered_list.append(current_word)
        filtered_list = new_filtered_list
    
    return filtered_list

    
    
def run_client(port, tls_encryption, hostname, northeastern_username):
    try:
        # create TCP client socket to connect with server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # modify for encryption
        if tls_encryption == True:
            context = ssl.create_default_context()
            client = context.wrap_socket(client, server_hostname=hostname)
        client.connect((hostname, port))
        
        #'hello' send to server
        client_hello_message = json.dumps({"type": "hello", "northeastern_username": northeastern_username}) + "\n"
        client.sendall(client_hello_message.encode('utf-8'))
        
        # game setup
        word_list = open_word_file('project1-words.txt')
        #print(f"Word count: {len(word_list)}")
        guessed_words = []
        game_id = ""
        
        while True:
            # receive message, decode, & determine type
            full_json_message = ""
            while True:
                json_server_message = client.recv(4096).decode('utf-8')
                full_json_message += json_server_message
                if len(json_server_message) < 4096:
                    break

            server_message = json.loads(full_json_message)
            server_message_type = server_message.get('type')
            # print(f"Full server message: {server_message}") 

            # 'start' game & update game id
            if server_message_type == 'start':
                game_id = server_message.get('id')
                # print(f"Game id: {game_id})
                
                # random word first guess
                first_guess = 'audio' #random.choice(word_list)
                guessed_words.append(first_guess)
                
                # send guess to server
                client_guess_message = json.dumps({"type": "guess", "id": game_id, "word": first_guess}) + "\n"
                client.sendall(client_guess_message.encode('utf-8'))
            
            # 'retry' & iterate thru word list for next guess
            elif server_message_type == 'retry':
                guesses = server_message.get('guesses', [])
                filtered_list = filter_word_list(word_list, guesses)
                
                # Choose the next guess from the filtered list
                next_guess = filtered_list[0] if filtered_list else random.choice(word_list)
                guessed_words.append(next_guess)
                
                # 'guess' send to server
                client_guess_message = json.dumps({"type": "guess", "id": game_id, "word": next_guess}) + "\n"
                client.sendall(client_guess_message.encode('utf-8'))
                
            # 'bye' after correct word guessed; print flag
            elif server_message_type == 'bye':
                secret_flag = server_message.get('flag')
                print(f"\nSecret flag obtained: {secret_flag}\n")
                break
            
            # 'error' from server; print error
            elif server_message_type == 'error':
                error_message = server_message.get('message')
                print(f"An error occurred on the server: {error_message}")
                break
    
    # catch all other errors    
    except Exception as e:
        print(f"\nAn error occurred: {e}. Please try again.\n")
    
    # close the client
    finally:
        client.close()



def main():
    # begin script commands & run client
    arguments = parse_commands()
    run_client(arguments.port, arguments.tls_encryption, arguments.hostname, arguments.northeastern_username)
    
    
if __name__ == "__main__":
    main()