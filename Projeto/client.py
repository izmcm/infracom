# https://codebeautify.org/base64-to-image-converter
import base64
import socket
import json
import sys
import select
import time
from random import randint
from DNSMessageManager import DNSMessageManager
from ServerUtils import ServerUtils

millis_now = lambda: int(round(time.time() * 1000))

def printMenu():
	print()
	print("***** MENU *****")
	print("1. Ver lista de arquivos disponíveis no server")
	print("2. Download de arquivo")
	print("3. Encerrar")
	print()
	
	
def printArchives(localArchives):
	print()
	print("***** ARQUIVOS DISPONIVEIS *****")
	for i in localArchives:
		print(i)
	print()


def sendRequest(connection, dest, localArchives):
	'''
	Envia requisição de arquivo desejado para o server
	
	param localArchives      Lista de arquivos disponíveis no server
	param dest               Informações sobre o host de destino
	'''
	while 1:
		print("Nome do arquivo?")
		arqName = input()
		try:
			isNum = (int(arqName) >= 0 and int(arqName) < len(localArchives))
		except:
			pass
	
		if arqName in localArchives:
			requestMessage = {
				"type": "request", 
				"ord": 0,
				"ordn": 0,
				"value": arqName
			}

			
			# TODO: Adicionar uma espera para a resposta do server com mensagens fragmentadas
			packs = getPartsWithTimeout(connection, dest, requestMessage)
			filedata = "".join(packs)
			with open("./clientArchives/" + arqName + ".jpg", "wb") as fh:
				fh.write(base64.decodebytes(bytes(filedata, encoding="latin-1")))
				
			print("Arquivo salvo com sucesso em clientArchives!")
			
			break
			
		else:
			print("Arquivo não encontrado :(")

def connect_to_server(clientSocket, dest):
	'''
	Configura o inicio da conexão com uma
	lista de arquivos disponíveis no servidor
	no momento da conexão
	
	param clientSocket       Socket aberto para trafego UDP
	param dest               Informações sobre o host de destino
	'''
	MAX_TIMEOUT = 20000
	TIMEOUT = 1000
	begin = millis_now()
	time = millis_now()
	recv = False
	localArchives = []
	
	connectMessage = {
		"type": "connect",
		"ord": 0,
		"ordn": 0,
		"value": ""
	}
	
	localArchives = getPartsWithTimeout(clientSocket, dest, connectMessage)
	ans = localArchives[0].split(',')

	return recv, ans

def getPartsWithTimeout(connection, address, package, timeout=500, max_timeout=3000):
	ServerUtils.sendJson(connection, address, package)
	t = millis_now()
	t_total = millis_now()
	parts = []
	
	ack = {
		"type": "ACK",
		"ord": 0,
		"ordn": 0,
		"value": ""
	}
	
	error = {
		"type": "ERROR",
		"ord": 0,
		"ordn": 0,
		"value": ""
	}
	
	shouldBreak = False
	
	print("Recendo mensagem...")
	
	# TODO: Implement package numbering 
	while millis_now() - t_total < max_timeout and not shouldBreak:
		while millis_now() - t < timeout and not shouldBreak:
			try:
				ans, addrs = connection.recvfrom(1024)
				ans = json.loads(ans)

				if ans["type"] == "END":
					parts += [ans]
					shouldBreak = True
				elif ans["type"] != "ERROR":
					parts += [ans]
					t = millis_now()
					t_total = millis_now()
				
				ServerUtils.sendJson(connection, address, ack)
			except:
				pass
			
	ServerUtils.sendJson(connection, address, ack)
	return [p["value"] for p in parts]
	
def setup_connection(serverIP):
	'''
	Configura dados de conexão socket udp
	'''
	clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	clientSocket.setblocking(False)
	
	serverPort = 5001
	dest = (serverIP, serverPort)
	
	return clientSocket, dest


def buildDNSMessage(host):
	message = bytearray([])
	transactionID = bytearray([randint(0, 0xff), randint(0, 0xff)])
	
	# Build the header properly
	data = transactionID + bytearray([0,0])
	flags = DNSMessageManager.getFlags(data)
	flags["RD"] = 1
	data = DNSMessageManager.modifyHeader(data, flags)
	
	# build the QD and so on
	QDCOUNT = bytearray([0,1])
	ANCOUNT = bytearray([0,0])
	NSCOUNT = bytearray([0,0])
	ARCOUNT = bytearray([0,0])
	data = data + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT
	
	# build the host query
	parts = host.split(".")
	hostFormat = bytearray([])
	for pt in parts:
		p1 = bytearray([len(pt)])
		p2 = bytes(pt, encoding='utf-8')
		hostFormat = hostFormat + p1 + p2
	hostFormat += bytearray([0])
	data += hostFormat
	
	# set the type of the message
	rrtype = bytearray([0,1])
	qclass = bytearray([0,1])
	data += rrtype + qclass
	
	return bytes(data)


def serverIPFromDNS(hostname):
	ip = ""

	HOST = socket.gethostbyname("localhost")  # Endereco IP do Servidor
	try:
		HOST = socket.gethostbyname(socket.gethostname())
	except:
		HOST = socket.gethostbyname("localhost")
	
	PORT = 53            # Porta que o Servidor esta
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
		dest = (HOST, PORT)
		udp.bind(('', 0))
		message = buildDNSMessage(hostname)
		x = udp.sendto(message, dest)
		ans, address = udp.recvfrom(512)
		ip = getIp(ans)
	
	return ip


def serverIPFromDNSByIp(hostname, dnsip="127.0.0.1"):
	ip = ""

	HOST = socket.gethostbyname("localhost")  # Endereco IP do Servidor
	try:
		HOST = socket.gethostbyname(socket.gethostname())
	except:
		HOST = socket.gethostbyname("localhost")

	if dnsip != "127.0.0.1":
		HOST = dnsip
	
	PORT = 53            # Porta que o Servidor esta
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
		dest = (HOST, PORT)
		udp.bind(('', 0))
		message = buildDNSMessage(hostname)
		x = udp.sendto(message, dest)
		ans, address = udp.recvfrom(512)
		ip = getIp(ans)
	
	return ip
	

def getIp(data):
	address = []
	dt = bytearray(data)
	
	for pt in dt[-4:]:
		address += [str(int(pt))]
	
	return ".".join(address)

## main
if __name__ == "__main__":
	lastCounter = -1
	localArchives = []
	
	# dnsip = input("Digite o ip do DNS que deseja utilizar: ")
	# ip = serverIPFromDNSByIp("www.google.com.br", "8.8.8.8")
	host = input("Digite o endereço do servidor que deseja acessar: ")
	ip = serverIPFromDNSByIp(host)
	
	print("IP do servidor: " + str(ip))

	clientSocket, dest = setup_connection(ip)
	clientSocket.bind(('', 0))
	
	status, localArchives = connect_to_server(clientSocket, dest)
	
	printMenu()

	while True:
		while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
			command = sys.stdin.readline()

			if command:
				if command == "1\n":
					printArchives(localArchives)
					printMenu()
					
				elif command == "2\n":
					sendRequest(clientSocket, dest, localArchives)
					printMenu()

				elif command == "3\n":
					END = {
						"type": "ENDCONNECTION",
						"ord": 0,
						"ordn": 0,
						"value": ""
					}
					
					# clientSocket.sendto(END, dest)
					ServerUtils.sendJson(clientSocket, dest, END)
					
					clientSocket.close()
					print("Bye Bye ;)")
					
					exit(0)
			else: 
				print('eof')
				exit(0)

			