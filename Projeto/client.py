import socket
import argparse

dnsIP = 3.85.163.101
dnsPort = 53

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	clientSocket.connect((serverName, serverPort))
except Exception:
	pass
	
