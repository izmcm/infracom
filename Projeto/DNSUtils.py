from DNSManager import DNSManager

def printf(message):
    print(str(message))
    with open('log.txt', 'a+') as f:
        f.write(str(message) + "\n")  # Python 3.x
        
def printAscii(data):
        string = ""
        for d in data:
            string += str(chr(d))
        
        printf(string)