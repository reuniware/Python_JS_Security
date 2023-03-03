# PythonSecurity
Scripts to perform various security analysis

https://ntic974.blogspot.com

TCP Port Scanner

DNS Sniffer

TCP Sniffer

Experimental IP Rotation with TOR


# Netfilterqueue installation problems ? Follow this alternative procedure under the root account on Kali Linux :

git clone https://github.com/kti/python-netfilterqueue.git

cd python-netfilterqueue

python3 setup.py install


# How to use the sniffers with Bettercap

sudo bettercap

set arp.spoof.whitelist 192.168.10.11 (if you need to whitelist your IP address)

arp.spoof on

Then you need to launch the python script, eg. python3 udp_tcp_sniffer_4.py
