# The header contains the following fields:
#     MSB                                           LSB
#
#                                     1  1  1  1  1  1
#       0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#     |                      ID                       |
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#     |QR|   Opcode  |AA|TC|RD|RA| Z|  AD |   RCODE   |
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#     |                    QDCOUNT                    |
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#     |                    ANCOUNT                    |
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#     |                    NSCOUNT                    |
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#     |                    ARCOUNT                    |
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

# where:

# ID              A 16 bit identifier assigned by the program that
#                 generates any kind of query.  This identifier is copied
#                 the corresponding reply and can be used by the requester
#                 to match up replies to outstanding queries.

# QR              A one bit field that specifies whether this message is a
#                 query (0), or a response (1).

# OPCODE          A four bit field that specifies kind of query in this
#                 message.  This value is set by the originator of a query
#                 and copied into the response.  The values are:

#                 0               a standard query (QUERY)

#                 1               an inverse query (IQUERY)

#                 2               a server status request (STATUS)

#                 3-15            reserved for future use

# AA              Authoritative Answer - this bit is valid in responses,
#                 and specifies that the responding name server is an
#                 authority for the domain name in question section.

#                 Note that the contents of the answer section may have
#                 multiple owner names because of aliases.  The AA bit


class DNSMessageReader:
    def __init__(self):
        pass
    
    @staticmethod
    def getId(data):
        id = (data[0] << 8) + data[1]
        return int(id)
        
    @staticmethod
    def getFlags(data):
        flags = dict()
        flags["QR"] = data[2] >> 7
        flags["Opcode"] = (data[2] >> 3) & 0b1111
        flags["AA"] = (data[2] >> 2) & 0b1
        flags["TC"] = (data[2] >> 1) & 0b1
        flags["RD"] = data[2] & 0b1
        flags["RA"] = data[3] >> 7
        
        flags["Z"] = (data[3] >> 6) & 0b1
        flags["AD"] = (data[3] >> 4) & 0b11
        flags["RCODE"] = data[3] & 0b1111
        
        print(data[2])
        print(data[3])
        
        return flags
        
    @staticmethod
    def getQDCount(data):
        QDCount = (data[4] << 8) + data[5]
        return QDCount
    
    @staticmethod
    def getANCount(data):
        QDCount = (data[6] << 8) + data[7]
        return QDCount
        
    @staticmethod
    def getNSCount(data):
        NSCount = (data[8] << 8) + data[9]
        return NSCount
        
    @staticmethod
    def getARCount(data):
        ARCount = (data[10] << 8) + data[11]
        return ARCount

