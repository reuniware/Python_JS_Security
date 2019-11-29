# coding: utf-8

# This script can be a good starting point for implementing your own firewall :)
# And don't spy your colleagues !
# apt-get install build-essential python-dev libnetfilter-queue-dev
# pip install NetfilterQueue
# sudo apt-get install python-netfilterqueue
# iptables -F
# iptables -F -t nat
# iptables -I FORWARD -j NFQUEUE --queue-num 0
# arpspoof -i eth0 192.168.1.200 -t 192.168.1.1     +      arpspoof -i eth0 192.168.1.1 -t 192.168.1.200
# arpspoof -i eth0 192.168.1.201 -> intercepte les requêtes dont la destination est 192.168.1.201

from netfilterqueue import NetfilterQueue
import scapy.all as scapy
import re
import os
import logging
import dns.resolver
import dns.reversename

from scapy.layers.inet import IP, TCP, UDP
from scapy.modules.winpcapy import pcap

from datetime import datetime

# LOG_FILENAME = datetime.now().strftime('logfile_%H_%M_%S_%d_%m_%Y.log')
LOG_FILENAME = datetime.now().strftime('logfile_%d_%m_%Y.log')

os.system("rm " + LOG_FILENAME)

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format='%(asctime)s :: %(message)s')

# logging.info('Forecastiong Job Started...')
# logging.debug('abc method started...')

os.system("echo '1' > /proc/sys/net/ipv4/ip_forward")
os.system("iptables -F")
os.system("iptables -F -t nat")
os.system("iptables -A FORWARD -j NFQUEUE --queue-num 0")

resolve_dns = False
ip_src = ""
ip_dst = ""
src_port = 0
dst_port = 0


def print_and_accept(input_packet):
    global ip_src, ip_dst, dst_port, src_port
    packet = scapy.IP(input_packet.get_payload())

    if UDP in packet:
        packet_type = "UDP"

    if TCP in packet:
        packet_type = "TCP"

    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        src_port = packet[IP].sport
        dst_port = packet[IP].dport

        dns_names_src = ""
        if resolve_dns:
            answers = ""
            try:
                no = dns.reversename.from_address(ip_src)
                answers = dns.resolver.query(no, 'PTR')
            except dns.resolver.NXDOMAIN:
                pass
            except dns.resolver.NoNameservers:
                pass

            for r_data in answers:
                dns_names_src = dns_names_src + str(r_data.target) + "/"

        dns_names_dst = ""
        if resolve_dns:
            answers = ""
            try:
                no = dns.reversename.from_address(ip_dst)
                answers = dns.resolver.query(no, 'PTR')
            except dns.resolver.NXDOMAIN:
                pass
            except dns.resolver.NoNameservers:
                pass

            for r_data in answers:
                dns_names_dst = dns_names_dst + str(r_data.target) + "/"

        packet_len = input_packet.get_payload_len()
        log_str = "(" + packet_type + ")" + " " + ip_src + ":" + str(
            src_port) + " (" + dns_names_src + ") -> " + ip_dst + ":" + str(
            dst_port) + " (" + dns_names_dst + ")" + " size = " + str(packet_len)
        print(log_str)
        logging.info(log_str)

    input_packet.accept()
    # packet.drop()


nf_queue = NetfilterQueue()
nf_queue.bind(0, print_and_accept)
try:
    nf_queue.run()
except KeyboardInterrupt:
    os.system("iptables -F")
    os.system("iptables -F -t nat")
    print("Gettin' out")

nf_queue.unbind()
