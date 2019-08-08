#!/usr/bin/python2
from spoof_struct import send_packet
import dpkt, socket, subprocess
from collections import defaultdict
import time
import cPickle as pickle
import itertools

src_ip = '192.168.100.128'
spoof_ip = '192.168.22.21'
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
  f = open(file_name,'rb')
  db = pickle.load(f)
  f.close()
  return db

def main():
  parse_ip = parse_candidate("ip_port_record.pickle")
  ipid_map = parse_candidate("save.p")
  f1 = open("not_found","w+")
  f2 = open("diff_port","w+")
  for ip,port in parse_ip.items():
    if ip not in ipid_map:
      f1.write(ip+"\n")
    elif port != ipid_map[ip][0]:
      f2.write("request to ip: "+ip+ " port: "+str(port)+"\n")
      f2.write("respond to ip: "+ip+ " port: "+str(ipid_map[ip][0])+"\n")
  f1.close()
  f2.close()
  reflector_candidate = {}
  f3 = open("increment","w+")
  for ip,lists in ipid_map.items():
    result = [j-i for j, i in zip(lists[3::2],lists[1:-2:2])]
    timestamp = [j-i for j, i in zip(lists[4::2],lists[2:-1:2])]
    if sum(result)/29>0 and sum(result)/29 < 6:
      f3.write("ip is: "+ip+"\n"+str(result)+"\n")
  f3.close()



  #for i in range(30):
  #  for ip, port in parse_ip.items():
      #send_packet(src_ip,src_port,ip,port,1,1)
  #    send_packet(spoof_ip,src_port,ip,port,1,1)
  #    print("ip: "+ip+" id: "+str(port)+"\n")
  #  exit(1)
  #  time.sleep(1)

  #p.send_signal(subprocess.signal.SIGTERM)
  #time.sleep(1)
  #parse_pcap(pcap_name)
  #f = open("result_measure.txt","w+")
  #for ip, id_list in ipid_map.iteritems():
  #  f.write("ip: "+ip+" id: "+str(id_list)+"\n")
  #f.close()


if __name__ == "__main__":
  main()
