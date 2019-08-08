#!/usr/bin/python
from spoof_struct import send_packet
import dpkt, socket, subprocess
import time

common_ports = [1,5,7,18,20,21,22,233,25,29,37,42,43,49,53,69,70,79,80,103,\
             108,109,110,115,118,119,137,139,143,150,156,161,179,190,194,197,\
             389,396,443,444,445,458,546,547,563,569,1080]
src_ip = '192.168.100.128'
src_port = 54024
pcap_name = "capture.pcap"


def parse_pcap(file_n,port):
  f = open(file_n)
  pcap = dpkt.pcap.Reader(f)
  result = []

  for ts, buf in pcap:
    eth = dpkt.ethernet.Ethernet(buf)
    ip = eth.data
    tcp = ip.data
    if eth.type == dpkt.ethernet.ETH_TYPE_IP and tcp.dport == src_port and tcp.sport == port:
      result.append(socket.inet_ntoa(ip.src))
    elif socket.inet_ntoa(ip.src) != src_ip:
      print("*************potential abnormal behavior*********")
      print(socket.inet_ntoa(ip.src))
      print(tcp.sport)
  f.close()
  return result

def parse_blacklist(file_name):
  f = open(file_name,"r")
  content = f.readlines()
  f.close()
  black_list = [x.rstrip('\n') for x in content if x[0]!='#']
  return black_list

def main():
  #generate the 1000 reflector, given in the result list, has port
  blacklist_ip = parse_blacklist("black_list.txt")
  result = []
  #genertate black list 20:
  #ports = iter(common_ports)
  #ports are included in the ip list

  while rem_ip:
    curr_port = next(ports,None)
    if curr_port != None:
      p = subprocess.Popen(['tcpdump', '-s','0', '-i', 'ens33',
                  '-w', pcap_name, "port", str(src_port)], stdout=subprocess.PIPE)
      time.sleep(2)
      for ip in rem_ip:
        send_packet(src_ip,src_port,ip,curr_port,1,1)
      #TODO parse cpk package and remove ip from list_b
      time.sleep(1)
      p.send_signal(subprocess.signal.SIGTERM)
      time.sleep(1)
      ip_res = parse_pcap(pcap_name,curr_port)
      print(ip_res)
      rem_ip = [x for x in rem_ip if x not in ip_res]
      result_temp = [(x,curr_port) for x in ip_res]
      result += result_temp
    else:
      result_temp = [(x,None) for x in rem_ip]
      result += result_temp
      rem_ip=[]
  f = open("result_prob.txt","w+")
  for ip, port in result:
    f.write(str(ip)+":"+str(port)+"\n")
  f.close()

if __name__ == "__main__":
  main()
