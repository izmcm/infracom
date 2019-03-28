#!/usr/bin/env python3

import sys
import itertools
import socket
from socket import socket as Socket


def main():    

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind(('', 2080))
        server_socket.listen(1)

        print("server ready")

        while True:
            
            with server_socket.accept()[0] as connection_socket:
                request = connection_socket.recv(1024).decode('ascii')
                reply = http_handle(request)
                connection_socket.send(reply.encode('ascii'))


            print("\n\nReceived request")
            print("======================")
            print(request.rstrip())
            print("======================")


            print("\n\nReplied with")
            print("======================")
            print(reply.rstrip())
            print("======================")


    return 0


def http_handle(request_string):
    """Given a http requst return a response
    Both request and response are unicode strings with platform standard
    line endings.
    """
    print('request: ' + request_string)
    assert not isinstance(request_string, bytes)

    contents = ''
    with open(request_string, 'r') as file:
        contents = file.read()

    print('contents: ' + contents)

    
    return contents

if __name__ == "__main__":
    sys.exit(main())