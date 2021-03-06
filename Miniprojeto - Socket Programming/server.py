#!/usr/bin/env python3

import sys
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
                # receive --command and --content
                message = connection_socket.recv(1024).decode()
                print("I receive " + message)

                command = message.split('-')[0]
                
                if command == "GET" or command == "GETPROG":
                    idx = len(command) + 1
                    request = message[idx:]
                elif command ==  "POST":
                    toFile = message.split('-')[1]
                    idx = len(command) + len(toFile) + 2
                    request = message[idx:]
                    print("File to save: " + toFile)

                print("Command: " + command)
                print("Request: " + request)

                if command == "GET" or command == "GETPROG":
                    reply = http_handle(request) # read archive and returns its content
                    connection_socket.send(reply) # send message
                    print("Success")
                elif command == "POST":
                    path = "filesPOST/" + toFile
                    
                    with open(path, "wb") as f: # save contents in output files
                        f.write(request.encode())

                        while request:
                            request = connection_socket.recv(1024)
                            f.write(request)

                    print("Success")
                else:
                    print("Command not supported")

    return 0

def http_handle(request_string):
    # if string "file.txt" isn't a binary
    assert not isinstance(request_string, bytes)

    contents = ''
    with open(request_string, 'rb') as file:
        contents = file.read()

    print(contents)
    return contents

if __name__ == "__main__":
    sys.exit(main())
