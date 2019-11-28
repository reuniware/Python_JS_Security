# apt-get install build-essential python-dev libnetfilter-queue-dev
# pip install NetfilterQueue
# sudo apt-get install python-netfilterqueue
# iptables -F
# iptables -F -t nat
# iptables -I FORWARD -j NFQUEUE --queue-num 0

from netfilterqueue import NetfilterQueue
import scapy.all as scapy
import re
import os

from scapy.layers.inet import IP, TCP

os.system("echo '1' > /proc/sys/net/ipv4/ip_forward")
os.system("iptables -F")
os.system("iptables -F -t nat")
os.system("iptables -I FORWARD -j NFQUEUE --queue-num 0")

ip_src = ""
ip_dst = ""
dst_port = 0


def print_and_accept(packet):
    global ip_src, ip_dst, dst_port
    http_packet = scapy.IP(packet.get_payload())
    # print(http_packet)

    if http_packet.haslayer(scapy.Raw) and http_packet.haslayer(TCP):
        if IP in http_packet:
            ip_src = http_packet[IP].src
            ip_dst = http_packet[IP].dst
            dst_port = http_packet[TCP].dport
        if dst_port == 80:
            print(ip_src + " -> " + ip_dst + ":" + str(dst_port))
            if http_packet.haslayer(scapy.Raw):
                load = http_packet[scapy.Raw].load
                print(load)

    packet.accept()


nf_queue = NetfilterQueue()
nf_queue.bind(0, print_and_accept)
try:
    nf_queue.run()
except KeyboardInterrupt:
    print('')

nf_queue.unbind()
