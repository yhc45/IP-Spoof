#!/usr/bin/python3
from ipdata import ipdata
import json, gzip
import os
import pickle
ip_address = {}
geo_mapping = {}
ipdata = ipdata.IPData('API-Key')
ip_address = pickle.load(open( "b.pickle", "rb" ))
for ip_list in ip_address.values():
  for ip in ip_list:
    response = ipdata.lookup(ip)
    val = response['country_name']
    if val == "United States":
      val += ", " + str(response['city'])
    geo_mapping[ip] = val

pickle.dump(geo_mapping, open( "geo_map.pickle", "wb" ))
print(geo_mapping)

