#!/usr/bin/python
from spoof_struct import send_packet
import dpkt, socket, subprocess
from collections import defaultdict
import time

src_ip = ''
spoof_ip = '192.168.0.221'
src_port = 54024
pcap_name = "filter.pcap"
ipid_map=defaultdict(lambda:[])


def parse_pcap(file_n):
  f = open(file_n)
  pcap = dpkt.pcap.Reader(f)

  for ts, buf in pcap:
    eth = dpkt.ethernet.Ethernet(buf)
    ip = eth.data
    tcp = ip.data
    #src_addr = socket.inet_ntoa(ip.src)
    if eth.type == dpkt.ethernet.ETH_TYPE_IP and tcp.dport == src_port: # and tcp.sport == port
      ipid_map[socket.inet_ntoa(ip.src)].append(ip.id)
  f.close()
  return

def parse_candidate(file_name):
  f = open(file_name,"r")
  content = f.readlines()
  f.close()
  filter_list = [tuple(x.rstrip('\n').split(':')) for x in content]
  filter_list = [ (x[0],int(x[1])) for x in filter_list if x[1] != 'None']
  return filter_list

def main():
  parse_pcap(pcap_name)
  f = open("target_measure.txt","w+")
  for ip, id_list in ipid_map.iteritems():
    f.write("ip: "+ip+" id: "+str(id_list)+"\n")
  f.close()


if __name__ == "__main__":
  main()

