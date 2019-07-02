#!/usr/bin/python
from listen import listen_port
from spoof_struct import send_packet

common_ports = [1,5,7,18,20,21,22,233,25,29,37,42,43,49,53,69,70,79,80,103,\
             108,109,110,115,118,119,137,139,143,150,156,161,179,190,194,197,\
             389,396,443,444,445,458,546,547,563,569,1080] 
src_ip = '192.168.100.135'
src_port = 54002

def parse_file(file_name):
  f = open(file_name,"r")
  content = f.readlines()
  f.close()
  black_list = [x.rstrip('\n') for x in content if x[0]!='#']
  return black_list

def main():
  list_b = parse_file("black_list.txt")
  result = set([])
  for ip in list_b:
    for port in common_ports:
      send_packet(src_ip,src_port,ip,port,1,1)
      if(listen_port(src_ip,src_port)):
        try:
          result.remove((ip,"none"))
        except:
          pass
        result.add((ip,port)) 
        break
      else:
        result.add((ip,"none"))
  f = open("result.txt","w+")
  for pair in result:
    f.write(str(pair)+"\n")
  f.close()

if __name__ == "__main__":
  main()
