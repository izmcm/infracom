import socket
from ArchiveList import ArchiveList
from ServerUtils import ServerUtils
import json
import time

millis_now = lambda: int(round(time.time() * 1000))

class Server():
    archiveList = ArchiveList()

    def __init__(self):
        self.notifyDNS("infra.com", "172.31.91.59")

    def connectClient(self):
        HOST = ''
        PORT = 5001
        counter = 0
        
        t = millis_now()
        waitTimeout = 60000
            
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setblocking(False)
        
        orig = (HOST, PORT)
        udp.bind(orig)
        
        while True:
            try:
                msg, adrss = udp.recvfrom(1024)
                msgJSON = json.loads(msg)
                print("Mensagem recebida:")
                print(msg)
                print()
                
                if msgJSON["type"] == "connect":
                    print("Iniciando envio de arquivos para o cliente...")
                    self.serveData(udp, adrss, "archives", ",".join(self.archiveList.getAllArchives()))
                    print()

                elif msgJSON["type"] == "request":
                    self.serveFile(udp, adrss, msgJSON["value"])
                
                elif msgJSON["type"] == "ENDCONNECTION":
                    break
            
                else:
                    error = {
                    	"type": "ERROR",
                    	"ord": 0,
                    	"ordn": 0,
                    	"value": "unordered messages"
                    }
                    
                    ServerUtils.sendJson(udp, adrss, error)
                
                t = millis_now()
            except:
                if millis_now() - t > waitTimeout:
                    break
                pass
            
        print("connection finished")
        udp.close()
    
    
    ##################################
    ## Stream Service
    ##################################
    def serveFile(self, connection, address, filename):
        stream = ServerUtils.fileToStream(self.archiveList.solictArchive(filename))
        
        # print(stream)
        print(filename)
        
        res = self.serveData(connection, address, "archives", stream)
        return res
        
    def serveData(self, connection, address, msgtype, stream, timeout=3000, max_timeout=500):
        n = 0
        oldn = 0
        
        countTry = 0

        while n < len(stream):
            package = {
        	    "type": msgtype, 
        	    "ord": n,
        	    "ordn": oldn,
        	    "value": stream[n:n+512]
            }
            
            print("sending:", package)
            
            sent = self.sendWithTimeout(connection, address, package, timeout, max_timeout)
            print("n", n, len(stream))
            if not sent:
                countTry += 1
                if countTry >= 5:
                    return False
                
                pass
            else:
                countTry = 0
                oldn = n
                n += min(512, len(stream) - n)
                print("*n", n, len(stream))
        
        package = {
            "type": "END", 
    	    "ord": n,
    	    "ordn": oldn,
    	    "value": ""
        }
        
        sent = self.sendWithTimeout(connection, address, package, timeout, max_timeout)
        
        # if not sent:
        #     return False
        
        return True
    
    def sendWithTimeout(self, connection, address, package, timeout=500, max_timeout=3000):
        ServerUtils.sendJson(connection, address, package)
        t = millis_now()
        t_total = millis_now()
        res = dict()
        
        while millis_now() - t_total < max_timeout:
            while millis_now() - t < timeout:
                try:
                    ans, addrs = connection.recvfrom(1024)
                    ans = json.loads(ans)
                    print("ans:", ans)
                    if ans["type"] == "ACK":
                        return True
                    if ans["type"] == "ERROR":
                        t = millis_now()
                        t_total = millis_now()
                except:
                    pass
        
        # Failure streamming the file

        if millis_now() - t_total > max_timeout:
            return False
        
        return True
    ##################################
    
    ##################################
    ## DNS Zone
    ##################################
    def notifyDNS(self, hostname, dnsip="127.0.0.1"):
        HOST = socket.gethostbyname("localhost")  # Endereco IP do Servidor
        try:
            HOST = socket.gethostbyname(socket.gethostname())
        except:
            HOST = socket.gethostbyname("localhost")

        help = HOST
        if dnsip != "127.0.0.1":
            HOST = dnsip
        
        PORT = 53
        dest = (HOST, PORT)
        command = "UPDATE"
        message = bytes("<>".join([command, hostname, help]), encoding="latin-1")
        
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
            udp.sendto(message, dest)
            print("Update no DNS...")


server = Server()
while True:
    server.connectClient()
