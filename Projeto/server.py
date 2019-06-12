import socket

class server():
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 5000
        self.sock = socket.socket()
        self.sock = socket.connect((self.ip,self.port))
    
    def connectDns(self):
        message = input(" -> ")
        while message != 'q':
            mySocket.send(message.encode())
            data = mySocket.recv(1024).decode()
            print ('Received from server: ' + data)
            message = input(" -> ")
            mySocket.close()