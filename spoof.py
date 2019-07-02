#!/usr/bin/python
import socket, struct

src_ip = "192.168.100.135" #my ip address
src_lport = 34980
#src_ip = "127.0.0.1"
dst_ip = "216.58.193.196"
ip_header = ""

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

#TCPHeader class
class TCPHeader():
  def __init__(self,src_port,dst_port):
    #notes sample header:src_port=47123,dst_port=80,seqnum=1000,acknum=0,data_offset=80,fin=0,syn=1,rst=0,psh=0,ack=0,urg=0,window=5840,check=0,urg_ptr=0

    #!=network(big-endian), H=short(2), L=long(4),B=char(1) 
    self.order = "!HHLLBBHHH" 
    #size of tcp header; size is specified by 4-byte words; 
    #5 words * 4 bytes is 20bytes minimum length of tcp header
    self.data_offset = 0xa0
    #following fields doesn't matter
    self.src_port = src_port 
    self.dst_port = dst_port
    self.seqnum = 23453
    self.acknum = 0
    self.window = 29200 #socket.htons(5840) #server's window size is 5840  
    self.fin = 0 
    self.syn = 1
    self.rst = 0 
    self.psh = 0 
    self.ack = 0 
    self.urg = 0
    self.check = 0
    self.urg_ptr = 0
  # to generate tcp_header assign flags
  def flags(self):
    return self.fin + (self.syn << 1) + (self.rst << 2) + (self.psh <<3) + (self.ack << 4) + (self.urg << 5)
  # generate the struc for TCP
  # 2 cases, first being checksum is calculated, latter being it hasn't
  def gen_struct(self, check=False):
    if check:
      self.check = check
      return struct.pack('!HHLLBBH',self.src_port,self.dst_port,self.seqnum,self.acknum,self.data_offset,self.flags(),self.window)+struct.pack('H',self.check)+struct.pack('!H',self.urg_ptr)
    else:
      return struct.pack(self.order,self.src_port,self.dst_port,self.seqnum,self.acknum,self.data_offset,self.flags(),self.window,self.check,self.urg_ptr)

#calculate tcp checksum
def tcp_checksum(source_ip,dest_ip,tcp_header,user_data=''):
  #Calculates the correct checksum for the tcp header
  global ip_header
  #populate the field for TCP header
  tcp_length = len(tcp_header) + len(user_data)
  print(tcp_length)
  saddr = socket.inet_aton(source_ip)
  daddr = socket.inet_aton(dest_ip)
  ihl_ver = (4 << 4) | 5
  ident = 54321
  ip_header = struct.pack('!BBHHHBBH4s4s',ihl_ver, 0, tcp_length, ident, 0x4000, 64, 6, 0, saddr, daddr)
  #Assemble the packet (IP Header + TCP Header + data, and then send it to checksum function)
  packet = ip_header + tcp_header + user_data 
  return checksum(packet)

def send_packet(dst_ip, dst_port):
  global ip_header
  #open socket
  #Use raw sockets to send a SYN packet.
  #PRTOCOL_RAW allows customize IP header
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW,socket.IPPROTO_RAW) 
    #s = socket.socket(socket.AF_INET, socket.SOCK_RAW,socket.IPPROTO_TCP) 
  except Exception as e:
    print("Error creating socket in send_raw_syn\n")
    print(e)
  src_addr = src_ip
  src_port = src_lport
  #test for bind device, doesn't need it after changing socket type to PROTO_RAW
  #s.bind(('ens33',0x800))
  make_tcpheader = TCPHeader(src_port,dst_port)
  #generate initial TCP header
  tcp_header = make_tcpheader.gen_struct()
  #generate TCP header that has checksum
  packet = make_tcpheader.gen_struct(check=tcp_checksum(src_addr,dst_ip,tcp_header))

  #finalize packet
  #append optional part for server to reply (mimiced from browser)
  packet = ip_header + packet + "\x02\x04\x05\xb4\x04\x02\x08\x0a\x4f\xa7\xbe\x47\x00\x00\x00\x00\x01\x03\x03\x07"
  print("SEND: SYN packet from {}:{} to {}:{}\n".format(src_ip,src_port,dst_ip,dst_port))
  try: 
    s.sendto(packet,(dst_ip,dst_port))
  except Exception as e: 
    print("Error utilizing raw socket in send_raw_syn\n")
    print(e)

  

send_packet(dst_ip,443)
