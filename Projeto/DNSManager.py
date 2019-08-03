import socket
import os

class DNSManager():
    # [String:String]
    servers = dict() 
    
    def __init__(self):
        print("works!")

    def registerIp(self, hostname, ip):
        self.servers[hostname] = ip
    
    def getIp(self, hostname):
        return self.servers.get(hostname, "nil")
    
    @staticmethod
    def registerHost(hostname, ip):
        os.system("touch hosts.txt")
        out = ""
        didupdate = False
        
        with open("hosts.txt", "r") as f:
            for l in f:
                if l in ["", "\n"]: 
                    continue

                host, lip = l.split(" ")
                if hostname.lower() == host.lower():
                    out += hostname + " " + ip + "\n"
                    didupdate = True
                else:
                    out += l
            
            if not didupdate:
                out += hostname + " " + ip + "\n"
        
        os.system("echo '' > hosts.txt")    
        
        with open("hosts.txt", "w") as f:
            f.write(out)
            
        pass
        
    @staticmethod
    def getHostByName(hostname):
        # Look in internal hosts
        os.system("touch hosts.txt")
        name = ""
        with open("hosts.txt", "r") as f:
            for l in f:
                host, ip = l.split(" ")
                if hostname.lower() == host.lower():
                    name = ip
                    break
        
        # otherwise search for external DNS
        if name == "":
            try:
                name = socket.gethostbyname(hostname)
            except:
                name = "0.0.0.0"
            
        return name