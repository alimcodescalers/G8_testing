#!/usr/bin/env/python
import re
file = open('/home/cloudscalers/test_res.txt', 'r')
f = file.read()
match = re.search(r'System Benchmarks Index Score\s+([\d.]+)', f)
print(match.group(1))

