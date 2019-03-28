#!/usr/bin/env python3

import sys
import itertools
import socket
from socket import socket as Socket


def main():    
    
    # create
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    
        # connect
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # connect to localhost port 2080
        server_socket.bind(('', 2080))
        server_socket.listen(1)

        print("server ready")

        while True:
            # connection, client_address = server_socket.accept()
            with server_socket.accept()[0] as connection_socket:
                print("test")
                message = connection_socket.recv(1024).decode('ascii') # receive --command and --content
                print("I receive " + message)
                
                command = message.split('-')[0]
                
                idx = len(command) + 1
                request = message[idx:]
                
                print("Command:" + command)
                print("Request:" + request)
                
                if command == "GET":
                    reply = http_handle(request) # read archive and returns its content
                    connection_socket.send(reply) # send message
                    print("Success")
                elif command == "POST":
                    connection_socket.send(request.encode()) # send message
                    print("Success")

    return 0


def http_handle(request_string):
    assert not isinstance(request_string, bytes) # if string "file.txt" isn't a binary

    contents = ''
    with open(request_string, 'rb') as file:
        contents = file.read()

    return contents

if __name__ == "__main__":
    sys.exit(main())