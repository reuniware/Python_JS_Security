***PLEASE READ THAT BEFORE GOING FURTHER :***<br.>
https://github.com/reuniware/Clean-Windows-Tracks-Script/blob/7d1fd8110a2ca88240aa06ef3f3716aa9fac1e45/ATTENTION-WARNING.md


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


# How to use the sniffers with Bettercap ?

sudo bettercap

set arp.spoof.whitelist 192.168.10.11 (if you need to whitelist your IP address)

set arp.spoof.fullduplex true (if you want to view bi-directional flows, not only from LAN to WAN but also from WAN to LAN)

arp.spoof on

Then you need to launch the python script, eg. python3 udp_tcp_sniffer_4.py in another terminal and under the root account


# What can you do with these sniffers ?

You can be the global firewall for all your network (whitelist IPs, blacklist IPs...)

You can sniff UDP packets, TCP packets, DNS packets, HTTP packets, HTTPS packets (without decryption...)


