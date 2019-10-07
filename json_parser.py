#!/usr/bin/python
import json, gzip
import os
import sqlite3

drop_prev = set([])
drop_next =  set([])
edrop_prev = set([])
edrop_next =  set([])

def parse_drop(file_name,date_i):
  global drop_prev
  global drop_next

  parsed = json.load(file_name)
  drop_next = set([])
  for x in parsed['records']:
    drop_next.add(x['ioc'])
  removed_from_list = drop_prev - drop_next
  for removed in removed_from_list:
    cursor.execute('\
      UPDATE ip_table\
      SET ddrop= (SELECT ddrop FROM ip_table WHERE ip_address={tn}) || {date}\
      WHERE ip_address={tn}\
            '.format(tn='\''+removed+'\'',date='\'-'+date_i+'\''))

    cursor.execute('\
      INSERT INTO ip_table(ip_address,edrop,ddrop)\
      SELECT {tn}, \'\', {date}\
      WHERE (Select Changes() = 0)\
            '.format(tn='\''+removed+'\'',date='\'-'+date_i+'\''))

  new_to_list = drop_next - drop_prev
  for new in new_to_list:
    cursor.execute('\
      UPDATE ip_table\
      SET ddrop= (SELECT ddrop FROM ip_table WHERE ip_address={tn}) || {date}\
      WHERE ip_address={tn}\
            '.format(tn='\''+new+'\'',date='\'S'+date_i+'\''))

    cursor.execute('\
      INSERT INTO ip_table(ip_address,edrop,ddrop)\
      SELECT {tn}, \'\', {date}\
      WHERE (SELECT Changes()=0) \
            '.format(tn='\''+new+'\'',date='\'S'+date_i+'\''))
  drop_prev=drop_next

def parse_edrop(file_name,date_i):
  global edrop_prev
  global edrop_next

  parsed = json.load(file_name)
  edrop_next = set([])
  for x in parsed['records']:
    edrop_next.add(x['ioc'])
  removed_from_list = edrop_prev - edrop_next
  for removed in removed_from_list:
    cursor.execute('\
      UPDATE ip_table\
      SET edrop= (SELECT ddrop FROM ip_table WHERE ip_address={tn}) || {date}\
      WHERE ip_address={tn}\
            '.format(tn='\''+removed+'\'',date='\'-'+date_i+'\''))

    cursor.execute('\
      INSERT INTO ip_table(ip_address,edrop,ddrop)\
      SELECT {tn}, {date}, \'\'\
      WHERE (Select Changes() = 0)\
            '.format(tn='\''+removed+'\'',date='\'-'+date_i+'\''))

  new_to_list = edrop_next - edrop_prev
  for new in new_to_list:
    cursor.execute('\
      UPDATE ip_table\
      SET edrop= (SELECT ddrop FROM ip_table WHERE ip_address={tn}) || {date}\
      WHERE ip_address={tn}\
            '.format(tn='\''+new+'\'',date='\'S'+date_i+'\''))

    cursor.execute('\
      INSERT INTO ip_table(ip_address,edrop,ddrop)\
      SELECT {tn}, {date}, \'\'\
      WHERE (Select Changes() = 0)\
            '.format(tn='\''+new+'\'',date='\'S'+date_i+'\''))
  edrop_prev=edrop_next

db = sqlite3.connect('mydb',isolation_level=None)

cursor = db.cursor()
cursor.execute('\
  CREATE TABLE IF NOT EXISTS ip_table (id INTEGER PRIMARY KEY, \
  ip_address TEXT UNIQUE, edrop TEXT DEFAULT \'\', ddrop TEXT DEFAULT \'\')\
  ')

#iterate through files
for root, dirs, files in os.walk('json_data/',topdown=True):
  dirs.sort()
  for stuff in sorted(files):
    date, _, _, cat, _, _ = stuff.split('_')

    json_file = gzip.open(os.path.join(root,stuff))
    if cat == 'DROP':
      parse_drop(json_file,date)
    elif cat == 'EDROP':
      parse_edrop(json_file,date)
    json_file.close()

db.close()
