#!/usr/bin/python
import cPickle as pickle

def parse_black_list(file_name):
  f = open(file_name,"r")
  content = f.readlines()
  f.close()
  filter_list = dict((x,int(y))  for x,y in (tuple(x.rstrip('\n').split('/')) for x in content))
  #filter_list = dict((x,int(y)) for x, y in filter_list)
  return filter_list

def main():
  blist = parse_black_list("ip_block.netset")
  f = open( "black_list.p", "wb" )
  pickle.dump(blist, f)
  f.close()
  print(blist)

if __name__ == "__main__":
  main()
