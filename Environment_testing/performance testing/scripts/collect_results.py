#!/usr/bin/env/python
import sys
import re
import os
from prettytable import PrettyTable
import itertools
import csv

Res_dir = sys.argv[1]
#working from inside Res_dir
#iterate on each machine results
# Assuming RAID0 for calculating the total IOPS
total_iops_list=[]
for j in os.listdir(os.getcwd()):

    if j.startswith('machine'):
        os.chdir(j)

        file = open('cpuload.txt', 'r')
        f=file.read()
        cpuload = re.finditer(r'all\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+'
                              r'\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+([\d.]+)', f)
        total_cpuload = [100-float(s.group(1)) for s in cpuload]
        avg_total_cpuload = round(sum(total_cpuload)/len(total_cpuload), 1)

        iops_list=[]
        disks_runtime=[]
        #iterate on disks_results per machine
        for i in os.listdir(os.getcwd()):
            if i.startswith("result"):
                file = open( i, 'r')
                f=file.read()
                match = re.finditer(r'iops=([\d]+),', f)
                disk_iops = [int(c.group(1)) for c in match]
                iops_list.append(sum(disk_iops))
                runt = re.search(r'runt=\s*([\d]+)msec', f)
                disks_runtime.append(int(runt.group(1)))
        total_iops = sum(iops_list)

        total_iops_list.append(total_iops)

        runtime = max(disks_runtime)
        vm_info = re.search('machine([\d.]+)_iter([\d]+)_([\w]+)_', j)
        machineId = vm_info.group(1)
        iteration = vm_info.group(2)
        write_type = vm_info.group(3)

        with open('%s/total_results' %Res_dir, 'a') as newfile:
            newfile.write('\n VM: %s \n Iteration: %s \n Test_type: %s' %(machineId, iteration, write_type))
            newfile.write('\n IOPS(%s): %s \n Avg_cpuload(%s): %s%% \n test_runtime(%s): %s msec'
                    %(iteration,total_iops, iteration, avg_total_cpuload, iteration, runtime))
            newfile.write('\n --------------------:-------------------- \n')

        os.chdir('%s' %Res_dir)


def group_separator(line):
    return line=='\n'


def table_print(iter, arrays):
    titles = ["VM_index", "Machine", "Test_type"]
    titles.append('IOPS(%s)'%iter); titles.append('cpuload(%s)'%iter); titles.append('Testruntime(%s)'%iter)
    table = PrettyTable(titles)
    index = 0
    for c in arrays:
        index += 1
        c.pop(1)
        c.insert(0, index)
        table.add_row(c)
    table_txt = table.get_string()
    with open('%s/total_results.table' %Res_dir,'a') as file:
        file.write('\n%s'%table_txt)

    result=[]
    for line in table_txt.splitlines():
        splitdata = line.split("|")
        if len(splitdata) == 1:
            continue  # skip lines with no separators
        linedata = []
        for field in splitdata:
            field = field.strip()
            if field:
                linedata.append(field)
        result.append(linedata)
    match = re.search('/(201.+)', Res_dir)
    with open('%s/%s.csv'%(Res_dir, match.group(1)), 'a') as outcsv:
           writer = csv.writer(outcsv)
           writer.writerows(result)


arr=[]
with open('%s/total_results' %Res_dir) as f:
    for key,group in itertools.groupby(f, group_separator):
        row=[]
        if not key:
            for item in list(group):
                field,value=item.split(':')
                match = re.search('[\d]+', field)
                value= value.strip()
                if field == ' Iteration':
                    row.append(int(value))
                else:
                    row.append(value)
            row.pop(6)
            arr.append(row)

arr.sort(key=lambda x: x[1])
b = []
iter = 1
for a in arr:
    if a[1] == iter:
        b.append(a)
    else:
        b.sort()
        table_print(iter, b)
        iter += 1
        b = []; b.append(a)
    if a == arr[len(arr)-1]:
        b.sort()
        table_print(iter, b)
print ('##################### \n TOTAL_IOPS = %s \n#####################' %sum(total_iops_list))
