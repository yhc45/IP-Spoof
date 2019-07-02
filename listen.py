#!/usr/bin/python
import socket,struct

def listen_port(src_ip,src_port):
  ETH_P_ALL = 3
  #s = socket.socket(socket.AF_INET, socket.SOCK_RAW,socket.IPPROTO_RAW) 
  s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
  ip_order = "!BBHHHBBH4s4s"
  tcp_order = "HHLLBBHHH"
  order = ip_order + tcp_order
  #device name is 
  s.bind((src_ip,src_port))
  #s.listen(0)
  #while(True):
  s.settimeout(3)
  #raw_packet = 0
  try:
    raw_packet = s.recvfrom(65535)
  except socket.timeout:
    return False
  ip_packet = raw_packet [0]
  src_ip = raw_packet [1]
  #can only print RST packet right now
  if (len(ip_packet) == 40):
    res = struct.unpack(order,ip_packet)
    ip_id = res [3]
    tcp_flag =res [15]
    packet_type = ""
    #rst = 4, syn = 2, ack = 16, syn ack = 18
    if(tcp_flag == 2):
      packet_type = "SYN"
    elif(tcp_flag == 4):
      packet_type = "RST"
    elif(tcp_flag == 16):
      packet_type = "ACK"
    elif(tcp_flag == 18):
      packet_type = "SYN ACK"
    else:
      packet_type = "Unknown"
    print("recieving {}:\nip_id:{}     ip:{}".format(packet_type,ip_id,src_ip))
  else:
    print("recieve from {}".format(src_ip))
    print(raw_packet)
  return True


