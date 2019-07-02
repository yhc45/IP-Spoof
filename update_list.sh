#!/bin/sh

URL=https://ransomwaretracker.abuse.ch/downloads/RW_IPBL.txt
FILE="black_list.txt"
LOG=wget.log

wget $URL -O $FILE -o $LOG
