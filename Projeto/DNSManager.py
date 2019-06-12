class DNSManager():
    # [String:String]
    servers = dict() 
    
    def __init__(self):
        print("works!")

    def registerIp(self, hostname, ip):
        self.servers[hostname] = ip
    
    def getIp(self, hostname):
        return self.servers.get(hostname, "nil")