#!/usr/bin/env python
#coding: utf-8
#date: 2015-09-24
#配合Zabbix Low-level discovery功能自动采集jvm信息

import subprocess
import sys
import re

#jps 路径
jps = ''

#jstat路径
jstat = ''

#根据你的环境修改java进程name与pid的获取方式
def getprocpid(procname):
    jpsout0 = subprocess.Popen(["sudo", jps, "-v"], stdout=subprocess.PIPE)
    jpsout = subprocess.Popen(["grep", "-v", "Jps"], stdin=jpsout0.stdout,stdout=subprocess.PIPE)
    jpsout.wait()

    for line in jpsout.stdout:
        result = re.split(' |/',line)
        if len(result) > 6:
            pid, name  = result[0], result[6]
            if name == procname:
                return pid

def gccapacity_jstats(procpid):
    jstatout = subprocess.Popen(["sudo", jstat, "-gccapacity", procpid], stdout=subprocess.PIPE)
    stdout, stderr = jstatout.communicate()
    legend, data = stdout.split('\n',1)
    gc_status = dict(zip(legend.split(), data.split()))
    return gc_status
    
def gc_jstats(procpid):
    jstatout = subprocess.Popen(["sudo", jstat, "-gc", procpid], stdout=subprocess.PIPE)
    stdout, stderr = jstatout.communicate()
    legend, data = stdout.split('\n',1)
    gccapacity_status = dict(zip(legend.split(), data.split()))
    return gccapacity_status

def heap_percent(gc_status,gccapacity_status):
    heap_used = float(gc_status["EU"]) + float(gc_status["OU"]) + float(gc_status["S0U"]) + float(gc_status["S1U"])
    heap_max = float(gccapacity_status["NGCMX"]) + float(gccapacity_status["OGCMX"])
    heap_percentage = round((heap_used / heap_max),2) * 100
    print heap_percentage

def fgc_frequent(gc_status):
    fgc = float(gc_status["FGC"])
    fgct = float(gc_status["FGCT"])
    if fgct == 0:
        print 0
    else:
        fgc_frequency = round(fgc / fgct,1)
        print fgc_frequency

def ygc_frequent(gc_status):
    ygc = float(gc_status["YGC"])
    ygct = float(gc_status["YGCT"])
    if ygct == 0:
        print 0
    else:
        ygc_frequency = round(ygc / ygct,1)
        print ygc_frequency
    
if len(sys.argv) == 3:
    procname = sys.argv[1]
    procpid = getprocpid(procname)
    gccapacity = gccapacity_jstats(procpid)
    gc=gc_jstats(procpid)
    if sys.argv[2] == "heap_percentage":
        heap_percent(gc,gccapacity)
    elif sys.argv[2] == "fgc_frequent":
        fgc_frequent(gc)
    elif sys.argv[2] == "ygc_frequent":
        ygc_frequent(gc)
else:
    print "Usage: " + sys.argv[0] + " process_name [heap_percentage |fgc_frequent | ygc_frequent] "
    print "Example:" + sys.argv[0] + " sms heap_percentage "
