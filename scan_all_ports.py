# scan ports from 0 to 65535 (very fast thanks to threading)
# ex: python scan_all_ports.py 192.168.1.1

import socket
import sys
from threading import Thread

ip = sys.argv[1]
ip = "192.168.1.15"


def exec_scan(port_to_scan):
    try:
        ip_address_and_port = (ip, port_to_scan)
        s = socket.socket()
        s.settimeout(1)
        s.connect(ip_address_and_port)
        print("Connected to ", ip_address_and_port[0], " on port ", ip_address_and_port[1])
        s.close()
    except socket.error as exc:
        pass


for port in range(0, 65535):
    t = Thread(target=exec_scan, args=(port,))
    t.start()
