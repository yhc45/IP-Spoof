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
  f = open(file_name,'rb')
  db = pickle.load(f)
  return db

def main():
  #parse_ip = parse_candidate("ip_port_record.pickle")
  #ip = subprocess.Popen(['tcpdump', '-s','0', '-i', 'ens33',
  #     '-w', pcap_name, "port", str(src_port)], stdout=subprocess.PIPE)
  #time.sleep(2)
  beg_ind = 0 
  end_ind = 6300
  start = 0
  #for p in range (131):
  timestamps = []
  for i in range(30):
    timestamps.append(time.time())
    send_packet(spoof_ip,src_port,"1.1.1.1",500,1,1)
    
    #send_packet(spoof_ip,src_port,"1.1.1.1",500,1,1)
    #send_packet(spoof_ip,src_port,"1.1.1.1",500,1,1)
    #send_packet(spoof_ip,src_port,"1.1.1.1",500,1,1)
    #send_packet(spoof_ip,src_port,"1.1.1.1",500,1,1)
    #send_packet(spoof_ip,src_port,"1.1.1.1",500,1,1)
    #time.sleep(0.9998061)
    time.sleep(0.999925)
    timestamps.append(time.time())

    print(timestamps[1]-timestamps[0])
    return
    if p == 130:
      time.sleep(0.136)
  print(str(sum(result)/29))
  beg_ind = end_ind
  end_ind += 6300

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
