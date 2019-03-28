import socket
import argparse

serverName = "localhost"
serverPort = 2080

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

parser = argparse.ArgumentParser()
parser.add_argument('--command', '-c', type=str, help='Command to execute: GET or POST')
parser.add_argument('--file', '-f', type=str, help='File to read or content to save in file')
parser.add_argument('--tofile', '-t', type=str, help='File to save')
args = parser.parse_args()

print(args.file) # file in
print(args.tofile) # file out

try:
	clientSocket.connect((serverName, serverPort))
except Exception:
	pass

try:
	command = args.command
	contents = args.file
	toFile = args.tofile

	message = command + "-" + contents
	clientSocket.send(message.encode()) # send command and contents to server
	print("I send " + message)

	# change path according command
	if command == "POST":
		path = "files/" + toFile
	elif command == "GET":
		path = toFile

	# save contents in output files
	with open(path, "wb") as f:
		data = clientSocket.recv(1024) # receive from server
		while data:
			f.write(data)
			data = clientSocket.recv(1024)

	clientSocket.close()

except KeyboardInterrupt:
	escape = True
except Exception:
	clientSocket.close()

clientSocket.close()
print("\nBye bye :)")
