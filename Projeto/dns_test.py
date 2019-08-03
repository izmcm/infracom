import socket
HOST = socket.gethostbyname("localhost")  # Endereco IP do Servidor
try:
    HOST = socket.gethostbyname(socket.gethostname())
except:
    HOST = socket.gethostbyname("localhost")

PORT = 53            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

print(HOST)

udp.sendto (b'UPDATE<>infra.com<>2.2.4.16', dest)
print("sent message!")
    
udp.close()
