import socket, struct

src_ip = ""

#generate checksum for tcp, alg is found @ Silver Moon, binarytides
def checksum(msg):
  sum = 0
  for i in range(0,len(msg),2):
    w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
    sum = sum + w

  sum = (sum>>16) + (sum & 0xffff)
  sum = sum + (sum >> 16)
  sum = ~sum & 0xffff
  return sum

#
#src_port=47123,dst_port=80,seqnum=1000,acknum=0,data_offset=80,fin=0,syn=1,rst=0,psh=0,ack=0,urg=0,window=5840,check=0,urg_ptr=0
class TCPHeader():
  def __init__(self):
    self.order = "!HHLLBBHHH" #!=network(big-endian), H=short(2), L=long(4),B=char(1) 
    self.src_port = 47123
    self.dst_port = 80
    self.seqnum = 1000
    self.acknum = 0
    self.data_offset = data_offset #size of tcp header; size is specified by 4-byte words; This is 80 decimal, which is 0x50, which is 20bytes (5words*4bytes).
    self.fin = 0
    self.syn = 1
    self.rst = 0
    self.psh = 0
    self.ack = 0
    self.urg = 0
    self.window = socket.htons(5840)
    self.check = 0
    self.urg_ptr = 0
