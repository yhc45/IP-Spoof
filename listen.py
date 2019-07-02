#/usr/bin/python
import socket

def liste_port(src_port):
  print(str(src_port))
#  ETH_P_ALL = 3
#  s = socket.socket(socket.AF_INET, socket.SOCKET_RAW, htons(ETH_P_ALL))
#  s.bind(('0.0.0.0',src_port))
#  while(True):
#    packet = s.recvfrom(65535).decode()
#    print(packet)

liste_port(54000)
