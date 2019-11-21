#scan ports from 0 to 65535 (very fast thanks to threading)
#ex: python scan_all_ports.py 192.168.1.1

import socket
import sys
from threading import Thread

ipAddressAndPort = (sys.argv[1], 80)
#ipAddressAndPort = ("192.168.1.1", 80)

def exec_scan(port):
    try:
        ipAddressAndPort = (sys.argv[1], port)
        s = socket.socket()
        s.settimeout(1)
        s.connect(ipAddressAndPort)
        print("Connected to ", ipAddressAndPort[0], " on port ", ipAddressAndPort[1])
        s.close()
    except socket.error as exc:
        pass

for port in range(0, 65535):
    t = Thread(target=exec_scan, args=(port,))
    t.start()
