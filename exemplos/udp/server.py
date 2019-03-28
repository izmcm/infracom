import socket

serverPort = 12000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverSocket.bind(("", serverPort))

print ("The server is ready to receive")

while (True):
    message, clientAddress = serverSocket.recvfrom(2048)
    
    print('m: ' + message.decode())
    print(clientAddress)

    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    