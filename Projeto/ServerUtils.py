import base64
import json

class ServerUtils:
    @staticmethod
    def fileToStream(imagePath):
        stream = bytearray([])
        with open(imagePath, "rb") as image:
            f = image.read()
            stream = base64.b64encode(f).decode('ascii')
        
        return stream
    
    @staticmethod
    def streamToFile(stream, imagePath):
        with open(imagePath, "wb") as fh:
            fh.write(base64.decodebytes(stream))
    
    
    @staticmethod
    def recvTimeout(connection, address, timeout):
        connection.recv()
        
    @staticmethod
    def sendJson(socket, dest, message):
        socket.sendto(bytes(json.dumps(message), encoding='latin-1'), dest)
        
    @staticmethod
    def sendWithTimeout(connection, address, package, timeout=500, max_timeout=3000):
        ServerUtils.sendJson(connection, address, package)
        t = millis_now()
        t_total = millis_now()
        
        while millis_now() - t_total < max_timeout:
            while millis_now() - t < timeout:
                ans, addrs = connection.recvfrom(1024)
                if ans["type"] == "ACK":
                    return True
                if ans["type"] == "ERROR":
                    t = millis_now()
                    t_total = millis_now()
        
        # Failure streamming the file
        if millis_now() - t_total < max_timeout:
            return False
            
        return True