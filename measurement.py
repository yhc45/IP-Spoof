#!/usr/bin/python2
from spoof_struct import send_packet
import dpkt, socket, subprocess
from collections import defaultdict
import time
import cPickle as pickle
import itertools

#will be changed when running the test
local_ip = '1.1.1.1'
local_port = 56577
pcap_name = "measure.pcap"

def parse_candidate(file_name):
  f = open(file_name,'rb')
  db = pickle.load(f)
  return db

def main():
  reflector_ip = parse_candidate("reflector_candidate.pickle")
  black_list_ip = parse_candidate("black_list.p")
  ref_1000 = list(itertools.islice(reflector_ip.iteritems(),1000))
  b_50 = list(itertools.islice(black_list_ip.iteritems(),50))
  p = subprocess.Popen(['tcpdump', '-s','0', '-i', 'eno2',
       '-w', pcap_name, "port", str(local_port)], stdout=subprocess.PIPE)
  time.sleep(2)
  timestamps = []
  for i in range(3):
    for r_ip, r_port in ref_1000:
      send_packet(local_ip,local_port,r_ip,r_port,1,1)
    time.sleep(0.98)
  for b_ip, b_port in b_50:
    for i in range(3):
      for r_ip, r_port in ref_1000:
        send_packet(local_ip,local_port,r_ip,r_port,1,1)
        send_packet(b_ip,b_port,r_ip,r_port,1,1)
        send_packet(b_ip,b_port,r_ip,r_port,1,1)
        send_packet(b_ip,b_port,r_ip,r_port,1,1)
        send_packet(b_ip,b_port,r_ip,r_port,1,1)
        send_packet(b_ip,b_port,r_ip,r_port,1,1)
      time.sleep(0.912758)
  p.send_signal(subprocess.signal.SIGTERM)
  time.sleep(2)

if __name__ == "__main__":
  main()
