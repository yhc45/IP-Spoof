#!/usr/bin/python
import json, gzip
import os
import sqlite3
from datetime import datetime
import cPickle as pickle

drop_prev = set([])
drop_next =  set([])
drop_end_date = ""
edrop_prev = set([])
edrop_next =  set([])
edrop_end_date = ""

def parse_drop(file_name,date_i):
  global drop_prev
  global drop_next
  global drop_end_date

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
            '.format(tn='\''+removed+'\'',date='\''+drop_end_date+'\''))

    cursor.execute('\
      INSERT INTO ip_table(ip_address,edrop,ddrop)\
      SELECT {tn}, \'\', {date}\
      WHERE (Select Changes() = 0)\
            '.format(tn='\''+removed+'\'',date='\''+drop_end_date+'\''))

  new_to_list = drop_next - drop_prev
  for new in new_to_list:
    cursor.execute('\
      UPDATE ip_table\
      SET ddrop= (SELECT ddrop FROM ip_table WHERE ip_address={tn}) || {date}\
      WHERE ip_address={tn}\
            '.format(tn='\''+new+'\'',date='\'S'+date_i+'-\''))

    cursor.execute('\
      INSERT INTO ip_table(ip_address,edrop,ddrop)\
      SELECT {tn}, \'\', {date}\
      WHERE (SELECT Changes()=0) \
            '.format(tn='\''+new+'\'',date='\'S'+date_i+'-\''))
  drop_prev=drop_next
  drop_end_date = date_i

def parse_edrop(file_name,date_i):
  global edrop_prev
  global edrop_next
  global edrop_end_date

  parsed = json.load(file_name)
  edrop_next = set([])
  for x in parsed['records']:
    edrop_next.add(x['ioc'])
  removed_from_list = edrop_prev - edrop_next
  for removed in removed_from_list:
    cursor.execute('\
      UPDATE ip_table\
      SET edrop= (SELECT edrop FROM ip_table WHERE ip_address={tn}) || {date}\
      WHERE ip_address={tn}\
            '.format(tn='\''+removed+'\'',date='\''+edrop_end_date+'\''))

    cursor.execute('\
      INSERT INTO ip_table(ip_address,edrop,ddrop)\
      SELECT {tn}, {date}, \'\'\
      WHERE (Select Changes() = 0)\
            '.format(tn='\''+removed+'\'',date='\''+edrop_end_date+'\''))

  new_to_list = edrop_next - edrop_prev
  for new in new_to_list:
    cursor.execute('\
      UPDATE ip_table\
      SET edrop= (SELECT edrop FROM ip_table WHERE ip_address={tn}) || {date}\
      WHERE ip_address={tn}\
            '.format(tn='\''+new+'\'',date='\'S'+date_i+'-\''))

    cursor.execute('\
      INSERT INTO ip_table(ip_address,edrop,ddrop)\
      SELECT {tn}, {date}, \'\'\
      WHERE (Select Changes() = 0)\
            '.format(tn='\''+new+'\'',date='\'S'+date_i+'-\''))
  edrop_prev=edrop_next
  edrop_end_date = date_i

db = sqlite3.connect('mydb',isolation_level=None)

cursor = db.cursor()
cursor.execute('\
  CREATE TABLE IF NOT EXISTS ip_table (id INTEGER PRIMARY KEY, \
  ip_address TEXT UNIQUE, edrop TEXT DEFAULT \'\', ddrop TEXT DEFAULT \'\')\
  ')

#iterate through files
for root, dirs, files in os.walk('json_file/',topdown=True):
  dirs.sort()
  for stuff in sorted(files):
    date, _, _, cat, _, _ = stuff.split('_')

   json_file = gzip.open(os.path.join(root,stuff))
    if cat == 'DROP':
      parse_drop(json_file,date)
    elif cat == 'EDROP':
      parse_edrop(json_file,date)
    json_file.close()

days_counter = {}
cursor.execute('SELECT * FROM ip_table')
for row in cursor:
  e_delta = 0
  d_delta = 0
  if row[2] != "" and row[2][-1] == "-":
    edrop_range = row[2].split("S")
    time = datetime.strptime(edrop_range[-1],"%Y%m%d-")
    today = datetime.today()
    e_delta = (today - time).days
  if row[3] != "" and row[3][-1] == "-":
    ddrop_range = row[3].split("S")
    time = datetime.strptime(ddrop_range[-1],"%Y%m%d-")
    today = datetime.today()
    d_delta = (today - time).days
  if e_delta != 0 or d_delta != 0:
    days_counter[row[1]]=(e_delta,d_delta)

pickle.dump(days_counter, open( "days_counter.pickle", "wb" ))
db.close()
