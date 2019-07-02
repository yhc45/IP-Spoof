#!/usr/bin/python
import socket

def liste_port(src_port):
  ETH_P_ALL = 3
  s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
  #device name is ens33
  s.bind(('ens33',src_port))
  while(True):
    packet = s.recvfrom(65535).decode()
    print(packet)

liste_port(54000)
