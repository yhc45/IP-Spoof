#!/usr/bin/python
from spoof_struct import send_packet
import socket, subprocess
import time

src_ip = '192.168.100.128'
spoof_ip = ''
src_port = 54002
pcap_name = "capture.pcap"


def parse_candidate(file_name):
  f = open(file_name,"r")
  content = f.readlines()
  f.close()
  black_list = [x.rstrip('\n') for x in content if x[0]!='#']
  return black_list

def main():
  parse_ip = parse_candidate("result_prob.txt")
  p = subprocess.Popen(['tcpdump', '-s','0', '-i', 'ens33',
       '-w', pcap_name, "port", str(src_port)], stdout=subprocess.PIPE)
  time.sleep(2)
  for i in range(30):
    for ip, port in rem_ip:
      send_packet(src_ip,src_port,ip,port,1,1)
      send_packet(spoof_ip,src_port,ip,port,1,1)
    time.sleep(2)

  p.send_signal(subprocess.signal.SIGTERM)

if __name__ == "__main__":
  main()
