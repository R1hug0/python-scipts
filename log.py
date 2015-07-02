#!/usr/bin/python

dic = {}
with open('log.txt','r') as f:
    for i in f.readlines():
        ip = i.strip().split()[0]
        if ip in dic.keys():
            dic[ip] = dic[ip] + 1
        else:
            dic[ip] = 1

for x, y in dic.items():
    print x, y

