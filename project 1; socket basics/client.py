#!/usr/bin/env python3

'''
Linda Quach
Spring 2024
CS5700 Network Fundamentals
Project 1: Socket Basics
'''

import socket
import argparse
import ssl
import json
import random

def open_word_file(filename):
    """
    Opens a text file containing list of words to append them into a list.

    Parameters:
    filename (file): .txt file containing valid words

    Returns:
    list: A list of words found in the text file.
    """
    
    word_list = []
    # read file, strip whitespaces into list
    with open(filename, 'r') as file:
        for line in file:
            word_list.append(line.strip())
    return word_list



def parse_commands():
    """
    Takes the command script, and parses them into arguments.

    Returns:
    Namespace: Contains the parsed arguments.
    """
    
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
            
    # print(f"{arguments}")
    return arguments
    
    
    
def matches_mark(word, letter, position, mark):
    """
    Helper function that takes the word guess and checks if the letter matches
    the mark at the given position.

    Parameters:
    word (string): Guessed word.
    letter (string): Letter in the guessed word.
    position (int): Given position.
    mark (int): Mark feedback from the server; 0, 1, 2.

    Returns:
    boolean: True if the marked position matches the expected letter. False otherwise.
    """
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
    """
    Filters out the words based on guessed word, and whether the mark feedback
    from the server matches the word.

    Parameters:
    word_list (list): List of original words.
    guesses (list): List of guessed words, with their feedback marks.

    Returns:
    list: New list of words filtering out the incompatible words.
    """
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
    """
    Runs the client program based on the information parsed from the given
    script commands.

    Parameters:
    port (int): Port number parsed from script.
    tls_encryption (boolean): True if TLS encryption used. False otherwise.
    hostname (string): Name or IP address of the host.
    northeastern_username (string): Username of the student, to obtain their
    unique flags.
    """
    
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
                first_guess = 'swing' #random.choice(word_list)
                guessed_words.append(first_guess)
                
                # send guess to server
                client_guess_message = json.dumps({"type": "guess", "id": game_id, "word": first_guess}) + "\n"
                client.sendall(client_guess_message.encode('utf-8'))
            
            # 'retry' & iterate thru word list for next guess
            elif server_message_type == 'retry':
                guesses = server_message.get('guesses', [])
                filtered_list = filter_word_list(word_list, guesses)
                
                # choose next guess from filtered list
                if filtered_list:
                    next_guess = filtered_list[0]
                # if filtered list empty
                else:
                    next_guess = random.choice(word_list)
                guessed_words.append(next_guess)
                
                # 'guess' send to server
                client_guess_message = json.dumps({"type": "guess", "id": game_id, "word": next_guess}) + "\n"
                client.sendall(client_guess_message.encode('utf-8'))
                
            # 'bye' after correct word guessed; print flag
            elif server_message_type == 'bye':
                secret_flag = server_message.get('flag')
                print(f"{secret_flag}")
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
    """
    Main function to execute the client program.
    """
    
    # begin script commands & run client
    arguments = parse_commands()
    run_client(arguments.port, arguments.tls_encryption, arguments.hostname, arguments.northeastern_username)
    
    
if __name__ == "__main__":
    main()