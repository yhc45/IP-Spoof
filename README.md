# Files

update\_list.sh: fetch the blocked list from ransomeware tracker
spoof\_struct.py: send tcp handshake packet based on the input
listen.py: listen to the tcp response
scan.py: main program to do the scan

run the following
```
./update_list.sh
sudo ./scan.py
```

"result.txt" will be generated with (*ip*,*port*)
