#!/usr/bin/python
from spoof_struct import send_packet
import socket, subprocess
import time

src_ip = '192.168.100.128'
spoof_ip = ''
src_port = 54024
pcap_name = "filter.pcap"
ipid_map={}


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
  return filter_list

def main():
  parse_ip = parse_candidate("result_prob.txt")
  p = subprocess.Popen(['tcpdump', '-s','0', '-i', 'ens33',
       '-w', pcap_name, "port", str(src_port)], stdout=subprocess.PIPE)
  time.sleep(2)
  for ip, port in parse_ip:
    for i in range(5):
      send_packet(src_ip,src_port,ip,port,1,1)
      send_packet(spoof_ip,src_port,ip,port,1,1)

  time.sleep(2)
  p.send_signal(subprocess.signal.SIGTERM)
  time.sleep(2)
  parse_pcap(pcap_name)
  f = open("result_measure.txt","w+")
  for ip, id_list in ipid_map.iteritems():
    f.write("ip: "+ip+" id: "+str(id_list)+"\n")
  f.close()


if __name__ == "__main__":
  main()
