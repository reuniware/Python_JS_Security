from pip._vendor.distlib.compat import raw_input
from scapy.all import *
import sys

from scapy.layers.dns import DNS
from scapy.layers.inet import IP

import netifaces as ni

default_interface = "eth0"
ip_exclude = "192.168.1.201"

if default_interface != "":
    interface = default_interface

if default_interface == "":
    try:
        interface = raw_input("[*] Enter desired Interface : ")
    except KeyboardInterrupt:
        print("[*] User Requests Shutdown")
        print("[*] Exiting")
        sys.exit(1)

# get local ip address
ni.ifaddresses(interface)
ip_local = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']

# une première IP à exclure est notre ip locale
print("1st IP to exclude from src = Local IP = ", ip_local)
# on peut aussi exclure une deuxième adresse ip
if ip_exclude != "":
    print("2nd IP to exclude from src = ", ip_exclude)

skipPacket = False


def query_sniff(pkt):
    global skipPacket
    if IP in pkt:
        ip_src = pkt[IP].src
        ip_dst = pkt[IP].dst
        if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
            if (ip_src != ip_local) and (ip_src != ip_exclude):
                if not skipPacket:
                    print(ip_src, " -> ", ip_dst, " : ", "(", pkt.getlayer(DNS).qd.qname, ")")
                    skipPacket = True
                else:
                    skipPacket = False


sniff(iface=interface, filter="port 53", prn=query_sniff, store=0)
# sniff(iface=interface, filter="", prn=query_sniff, store=0)
print("\n[*] Shutting Down...")
