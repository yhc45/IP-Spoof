import socket, struct

#generate checksum for tcp, alg is found online
def checksum(msg):
  s = 0
  #loop take 2 char at a time
  for i in range(0, len(msg), 2):
    w = (ord(msg[i]) << 8) + ord(msg[i+1])
    s = s+w


