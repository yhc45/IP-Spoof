#!/usr/bin/python
import socket, struct

src_ip = "9.9.9.9"

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
  def __init__(self,src_port,dst_port):
    self.order = "!HHLLBBHHH" #!=network(big-endian), H=short(2), L=long(4),B=char(1) 
    self.src_port = src_port #doesn't matter
    self.dst_port = dst_port #doesn't matter
    self.seqnum = 1000 #doesn't matter
    self.acknum = 0 #doesn't matter
    self.data_offset = 5 #size of tcp header; size is specified by 4-byte words; 5 words * 4 bytes is 20bytes minimum length of tcp header
    self.fin = 0 #doesn't matter
    self.syn = 1 #doesn't matter
    self.rst = 0 #doesn't matter
    self.psh = 0 #doesn't matter
    self.ack = 0 #doesn't matter
    self.urg = 0 #doesn't matter
    self.window = socket.htons(5840)
    self.check = 0
    self.urg_ptr = 0
  #to generate the flag field
  def flags(self):
    return self.fin + (self.syn << 1) + (self.rst << 2) + (self.psh <<3) + (self.ack << 4) + (self.urg << 5)
  def gen_struct(self, check=False):
    #if check != False: self.check = check
    if check:
      self.check = check
      return struct.pack('!HHLLBBH',self.src_port,self.dst_port,self.seqnum,self.acknum,self.data_offset,self.flags(),self.window)+struct.pack('H',self.check)+struct.pack('!H',self.urg_ptr)
    else:
      return struct.pack(self.order,self.src_port,self.dst_port,self.seqnum,self.acknum,self.data_offset,self.flags(),self.window,self.check,self.urg_ptr)

def tcp_checksum(source_ip,dest_ip,tcp_header,user_data=''):
  #Calculates the correct checksum for the tcp header
  tcp_length = len(tcp_header) + len(user_data)
  ip_header = struct.pack('!4s4sBBH',socket.inet_aton(source_ip),socket.inet_aton(dest_ip),0,socket.IPPROTO_TCP,tcp_length) #construct IP header with TCP protocol.
  packet = ip_header + tcp_header + user_data #Assemble the packet (IP Header + TCP Header + data, and then send it to checksum function)
  return checksum(packet)

def send_packet(dst_ip, dst_port):
  #open socket
  #Use raw sockets to send a SYN packet.
  #If you want, you could use the IP header assembled in the tcp_checksum function to have a fully custom TCP/IP stack
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP) #Using IPPROTO_TCP so the kernel will deal with the IP packet for us. Change to IPPROTO_IP if you want control of IP header as well
  except Exception as e:
    print("Error creating socket in send_raw_syn\n")
    print(e)
  src_addr = src_ip
  src_port = 54321
  make_tcpheader = TCPHeader(src_port,dst_port)
  tcp_header = make_tcpheader.gen_struct()
  packet = make_tcpheader.gen_struct(check=tcp_checksum(src_addr,dst_ip,tcp_header))
  print("SEND: SYN packet {} {}\n".format(dst_ip,dst_port))
  try: s.sendto(packet,(dst_ip,0))
  except Exception as e: 
    print("Error utilizing raw socket in send_raw_syn\n")
    print(e)

send_packet("1.1.1.1",80)
