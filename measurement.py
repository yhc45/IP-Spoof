#!/usr/bin/python2
from spoof_struct import send_packet
import dpkt, socket, subprocess
from collections import defaultdict
import time
import cPickle as pickle
import itertools

#will be changed when running the test
local_ip = '1.1.1.1'
local_port = 54024
pcap_name = "measure.pcap"

def parse_candidate(file_name):
  f = open(file_name,'rb')
  db = pickle.load(f)
  return db

def main():
  reflector_ip = parse_candidate("reflector.pickle")
  black_list_ip = parse_candidate("black_list.pickle")
  p = subprocess.Popen(['tcpdump', '-s','0', '-i', 'ens33',
       '-w', pcap_name, "port", str(src_port)], stdout=subprocess.PIPE)
  time.sleep(2)
  timestamps = []
  
  for r_ip, r_port in reflector_ip:
    for b_ip, b_port in black_list_ip:
      for i in range(3):
        send_packet(local_ip,local_port,r_ip,r_port,1,1)
        time.sleep(0.999925)
      for i in range(3): 
        send_packet(local_ip,local_port,r_ip,r_port,1,1)
        send_packet(b_ip,b_port,r_ip,r_port,1,1)
        send_packet(b_ip,b_port,r_ip,r_port,1,1)
        send_packet(b_ip,b_port,r_ip,r_port,1,1)
        send_packet(b_ip,b_port,r_ip,r_port,1,1)
        send_packet(b_ip,b_port,r_ip,r_port,1,1)
        time.sleep(0.9998061)
  p.send_signal(subprocess.signal.SIGTERM)
  time.sleep(1)

if __name__ == "__main__":
  main()
