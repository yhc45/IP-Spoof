#!/usr/bin/python
import socket

def listen_port(src_port):
  ETH_P_ALL = 3
  #s = socket.socket(socket.AF_INET, socket.SOCK_RAW,socket.IPPROTO_RAW) 
  s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

  #device name is 
  s.bind(('192.168.100.135',src_port))
  #s.listen(0)
  while(True):
    packet = s.recvfrom(65535)
    print(packet)

listen_port(54000)
