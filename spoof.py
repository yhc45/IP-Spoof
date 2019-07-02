#!/usr/bin/python
import socket, struct

NO_FRAG = 2

#IPHeader for spoofing and checksum calculation
class IPHeader():
  def __init__(self,src_ip,dst_ip,payload_len,flag, fragment = 0,  protocol = 6, TTL = 64, iden = 54321 ,ihl_ver=((4 << 4) | 5)):
    self.src_ip = socket.inet_aton(src_ip)
    self.dst_ip = socket.inet_aton(dst_ip)
    self.pseudo_order = "!4s4sBBH"
    self.order = "!BBHHHBBH4s4s"
    self.flag_off = (flag << 13) | fragment
    self.pseudo_header = struct.pack(self.pseudo_order,self.src_ip,self.dst_ip,0,protocol,payload_len)
    self.header = struct.pack('!BBHHHBBH4s4s',ihl_ver, 0, payload_len, iden, self.flag_off, TTL, protocol, 0, self.src_ip, self.dst_ip)


#TCPHeader class
class TCPHeader():
  def __init__(self,src_port,dst_port,syn,ack,rst,fin):
    #notes sample header:src_port=47123,dst_port=80,seqnum=1000,acknum=0,data_offset=80,fin=0,syn=1,rst=0,psh=0,ack=0,urg=0,window=5840,check=0,urg_ptr=0

    #!=network(big-endian), H=short(2), L=long(4),B=char(1) 
    self.order = "!HHLLBBHHH" 
    #size of tcp header; size is specified by 4-byte words; 
    #5 words * 4 bytes is 20bytes minimum length of tcp header
    self.data_offset = 0x50
    #following fields doesn't matter
    self.src_port = src_port 
    self.dst_port = dst_port
    self.seqnum = 23453
    self.acknum = 0
    self.window = 29200 #socket.htons(5840) #server's window size is 5840  
    self.fin = 0 
    self.syn = syn
    self.rst = rst
    self.psh = 0 
    self.ack = ack
    self.urg = 0
    self.check = False
    self.urg_ptr = 0
    self.packet = ""
  # to generate tcp_header assign flags
  def flags(self):
    return self.fin + (self.syn << 1) + (self.rst << 2) + (self.psh <<3) + (self.ack << 4) + (self.urg << 5)
  # generate the struc for TCP
  # 2 cases, first being checksum is calculated, latter being it hasn't
  def gen_struct(self, check=False):
    if self.check:
      self.packet = struct.pack('!HHLLBBH',self.src_port,self.dst_port,self.seqnum,self.acknum,self.data_offset,self.flags(),self.window)+struct.pack('H',self.check)+struct.pack('!H',self.urg_ptr)
    else:
      self.packet = struct.pack(self.order,self.src_port,self.dst_port,self.seqnum,self.acknum,self.data_offset,self.flags(),self.window,self.check,self.urg_ptr)
  #generate checksum for tcp, alg is found @ Silver Moon, binarytides
  def checksum(self):
    msg = self.packet
    sum = 0
    for i in range(0,len(msg),2):
      w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
      sum = sum + w

    sum = (sum>>16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    sum = ~sum & 0xffff
    self.check = sum


def send_packet(src_ip, src_port, dst_ip, dst_port,syn = 1,ack = 0):
  #open socket
  #Use raw sockets to send a SYN packet.
  #PRTOCOL_RAW allows customize IP header
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW,socket.IPPROTO_RAW) 
    #s = socket.socket(socket.AF_INET, socket.SOCK_RAW,socket.IPPROTO_TCP) 
  except Exception as e:
    print("Error creating socket in send_raw_syn\n")
    print(e)
  #test for bind device, doesn't need it after changing socket type to PROTO_RAW
  #s.bind(('ens33',0x800))
  tcpheader = TCPHeader(src_port,dst_port,syn,ack,0,0)
  #generate initial TCP header
  tcpheader.gen_struct()
  ipheader = IPHeader(src_ip,dst_ip,len(tcpheader.packet),NO_FRAG) 
  tcpheader.packet = ipheader.pseudo_header + tcpheader.packet
  tcpheader.checksum()
  #generate header with correct checksum
  tcpheader.gen_struct()

  #finalize packet
  #append optional part for server to reply (mimiced from browser)
  packet = ipheader.header + tcpheader.packet
  print("SEND: SYN packet from {}:{} to {}:{}\n".format(src_ip,src_port,dst_ip,dst_port))
  try: 
    s.sendto(packet,(dst_ip,dst_port))
  except Exception as e: 
    print("Error utilizing raw socket in send_raw_syn\n")
    print(e)
  
send_packet("192.168.100.135",54001,"216.58.193.196",443,1,1)
