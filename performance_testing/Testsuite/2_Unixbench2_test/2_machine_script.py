#!/usr/bin/env/python
import re
import os
import sys
import time

password = sys.argv[1]
cores = int(sys.argv[2])
runtime = int(sys.argv[3])
start = time.time()
while True:
    now = time.time()
    if now-start > runtime:
        break
    os.system(' cd /home/cloudscalers/UnixBench; echo %s | sudo -S ./Run -c %s -i 1 >> /home/cloudscalers/test_res.txt' %(password, cores))

file = open('/home/cloudscalers/test_res.txt', 'r')
f = file.read()
match = re.finditer(r'System Benchmarks Index Score\s+([\d.]+)', f)
matches = [float(m.group(1)) for m in match]
os.system('rm /home/cloudscalers/test_res.txt')
if(len(matches) != 0):
    print(sum(matches)/len(matches))
else:
    print('0')

