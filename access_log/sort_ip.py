#!/usr/bin/python

ip = {}
with open("access.log","r") as f:
    for i in f.readlines():
        j = i.strip().split()[0]
        if j in ip.keys():
            ip[j] = ip[j] + 1
        else:
            ip[j] = 1
sort_ip = sorted(ip.items(), key = lambda ip:ip[1], reverse = True)        
for x, y in sort_ip:
    print x, y


# shell: awk '{print $1}' access.log | sort | uniq -c | sort -nr
