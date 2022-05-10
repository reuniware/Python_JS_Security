# coding: utf-8

# apt-get install build-essential python-dev libnetfilter-queue-dev
# pip install NetfilterQueue
# sudo apt-get install python-netfilterqueue
# pip3 install -U git+https://github.com/kti/python-netfilterqueue
# iptables -F
# iptables -F -t nat
# iptables -I FORWARD -j NFQUEUE --queue-num 0
# arpspoof -i eth0 192.168.1.200 -t 192.168.1.1     +      arpspoof -i eth0 192.168.1.1 -t 192.168.1.200
# arpspoof -i eth0 192.168.1.201 -> intercepte les requêtes dont la destination est 192.168.1.201
from subprocess import Popen, PIPE
from threading import Thread

from netfilterqueue import NetfilterQueue
import scapy.all as scapy
import re
import os
import logging
# import dns.resolver
# import dns.reversename
import socket

from scapy.layers.dns import DNS
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import ARP
# from scapy.modules.winpcapy import pcap
from scapy.libs.winpcapy import pcap

from datetime import datetime

import netifaces as ni

# LOG_FILENAME = datetime.now().strftime('logfile_%H_%M_%S_%d_%m_%Y.log')
LOG_FILENAME = datetime.now().strftime('logfile_%d_%m_%Y.log')
delete_log_file_before_go = False

if delete_log_file_before_go:
    os.system("rm " + LOG_FILENAME)

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format='%(asctime)s :: %(message)s')

os.system("echo '1' > /proc/sys/net/ipv4/ip_forward")
os.system("iptables -F")
os.system("iptables -F -t nat")
os.system("iptables -A FORWARD -j NFQUEUE --queue-num 0")

LOG_TO_FILE = False
LOG_TO_SCREEN = True

dns_table = {}
netbios_table = {}

interface = "eth0"
resolve_dns = False
resolve_netbios = False
ip_src = ""
ip_dst = ""
src_port = 0
dst_port = 0
nb_packets = 0

# resolver = dns.resolver.Resolver()
# resolver.timeout = 0.250

# get local ip address
ni.ifaddresses(interface)
ip_local = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']

#83.136.163.31 = k3yy0 telephonie
whitelist_ips = {ip_local, "192.168.10.33", "83.136.163.31"}
blacklist_ips = {"52.109.88.10"}
log_only_str = {""}  # If nothing to log then {""}       # string is compared to log_str variable
blacklist_str = {"8.247.", "8.248."}  # If no blacklist string then {}    # string is compared to log_str variable
whitelist_str = {}  # If no whitelist string then {}    # string is compared to log_str variable

if len(blacklist_ips) == 0:
    blacklist_ips = {}

if len(log_only_str) == 0:
    log_only_str = {""}


def exit_script():
    os.system("iptables -F")
    os.system("iptables -F -t nat")
    print("Gettin' out")
    exit(0)


def get_netbios_name(ip_address):
    DN = open(os.devnull, 'w')
    nbt = Popen(['nbtscan', ip_address], stdout=PIPE, stderr=DN)
    nbt = nbt.communicate()[0]
    nbt = nbt.splitlines()
    for l in nbt:
        # print("l=" + str(l))
        if str(l).endswith(ip_address):
            netbios = l.split('    ')
            # print(netbios[1])
            nb_name = netbios[1]
            nb_name = nb_name.replace('<server>', '')
            nb_name = nb_name.replace('<unknown>', '')
            nb_name = nb_name.replace(' ', '')
            return nb_name


def log_to_screen(str_to_log):
    print(str_to_log)


def log_to_file(str_to_log):
    logging.info(str_to_log)


def drop_packet(input_packet):
    input_packet.drop()


def accept_packet(input_packet):
    input_packet.accept()


def process_packet(input_packet):
    global LOG_TO_FILE, LOG_TO_SCREEN
    global ip_src, ip_dst, dst_port, src_port, nb_packets
    packet = scapy.IP(input_packet.get_payload())

    packet_type = "???"

    if UDP in packet:
        packet_type = "UDP "

    if TCP in packet:
        packet_type = "TCP "

    if ICMP in packet:
        packet_type = "ICMP"

    packet_processed = False

    if IP in packet:

        ip_src = packet[IP].src
        ip_dst = packet[IP].dst

        if ICMP not in packet:
            src_port = packet[IP].sport
            dst_port = packet[IP].dport

        if ip_src in whitelist_ips or ip_dst in whitelist_ips:
            input_packet.accept()
            # When packet automatically accepted because IP is in whitelist then nothing is logged (in this version)
            return

        nb_packets = nb_packets + 1
        nb_packets_str = "{:0>9d}".format(nb_packets)

        packet_len = input_packet.get_payload_len()
        log_str = str(datetime.now()) + " " + nb_packets_str + " (" + packet_type + ")" + " " + ip_src + ":" + str(
            src_port) + " -> " + ip_dst + ":" + str(
            dst_port) + " size = " + str(packet_len)

        if UDP in packet and dst_port == 53: #src_port == 443 or dst_port == 443:
            #print(log_str)
            print(ip_src, " asking for ", packet[DNS].qd.qname)
            #print(str(input_packet.get_payload()))
            # if not packet_processed:
            #     t = Thread(target=drop_packet, args=(input_packet,))
            #     t.start()
            #     log_str_bi = "Blacklisted IP : Dropping [" + ip_src + "]"
            #     print(log_str_bi)
            #     packet_processed = True

        if len(blacklist_ips) > 0:
            if ip_src in blacklist_ips or ip_dst in blacklist_ips:
                if not packet_processed:
                    t = Thread(target=drop_packet, args=(input_packet,))
                    t.start()
                    log_str_bi = "Blacklisted IP : Dropping [" + ip_src + "]"
                    print(log_str_bi)
                    packet_processed = True

        nb_packets = nb_packets + 1
        nb_packets_str = "{:0>9d}".format(nb_packets)

        packet_len = input_packet.get_payload_len()

    if not packet_processed:
        input_packet.accept()


nf_queue = NetfilterQueue()
nf_queue.bind(0, process_packet)
try:
    nf_queue.run()
except KeyboardInterrupt:
    exit_script()
except UnboundLocalError:
    pass
except AttributeError:
    pass

nf_queue.unbind()
