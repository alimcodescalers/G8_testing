#!/usr/bin/env/python3
import sys
import re
import os
from prettytable import PrettyTable
import itertools
import csv


def get_vm_ovs_node(vmid, ovc):
    # make sure vmid is int
    vm = ovc.api.cloudapi.machines.get(machineId=vmid)
    for disk in vm['disks']:
        if disk['type'] == 'D':
            ovs_ip = re.search('(\d+.){3}(\d+)', disk['referenceId'])
            break
    return ovs_ip.group()

#vm_ovsip_iops_list.append({'machineId': machineId, 'ovs_ip': ovs_ip, 'iops': total_iops})

def sum_iops_per_ovs(vm_ovsip_iops_list):
    ovs_list = []
    cross_iops_list = []
    final_iops_list = [[]]
    vm_dist_list = []
    for vm in vm_ovsip_iops_list:
        if vm['ovs_ip'] not in ovs_list:
            ovs_list.append(vm['ovs_ip'])
            cross_iops_list.append([vm['iops']])
            index = ovs_list.index(vm['ovs_ip'])
            vm_dist_list.insert(index,1)
        else:
            index = ovs_list.index(vm['ovs_ip'])
            cross_iops_list[index].append(vm['iops'])
            temp = vm_dist_list[index]
            vm_dist_list.remove(vm_dist_list[index])
            vm_dist_list.insert(index, temp+1)
    for ovs_iops in cross_iops_list:
        final_iops_list[0].append(sum(ovs_iops))
    ovs_list.insert(0,"OVS_NODES")
    final_iops_list[0].insert(0,"TOTAL_IOPS")
    vm_dist_list.insert(0,"VMs DISTRIBUTION")
    final_iops_list.append(vm_dist_list)
    return ovs_list, final_iops_list

def results_on_csvfile(csv_file_name, Res_dir, table_string):
    #s=s1.get_string()
    result=[]
    for line in table_string.splitlines():
        splitdata = line.split("|")
        if len(splitdata) == 1:
            continue  # skip lines with no separators
        linedata = []
        for field in splitdata:
            field = field.strip()
            if field:
                linedata.append(field)
        result.append(linedata)

    with open('%s/%s.csv'%(Res_dir, csv_file_name), 'a') as outcsv:
           writer = csv.writer(outcsv)
           writer.writerows(result)

def collect_results(titles, results, Res_dir):
    table = PrettyTable(titles)
    for i in results:
        table.add_row(i)
    table_txt = table.get_string()
    with open('%s/ovs_nodes_iops.table' %Res_dir,'a') as file:
        file.write('\n%s'%table_txt)
    results_on_csvfile('ovs_nodes_iops', Res_dir, table_txt)



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



def main():
    Res_dir = sys.argv[1]
    environment=sys.argv[2]
    username=sys.argv[3]
    password=sys.argv[4]
    from JumpScale import j
    ovc = j.clients.openvcloud.get(environment, username, password)
    #working from inside Res_dir
    #iterate on each machine results
    # Assuming RAID0 for calculating the total IOPS
    total_iops_list=[]
    vm_ovsip_iops_list=[]
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
                    disk_iops=[]
                    match = re.finditer(r'iops=([\S]+),', f)
                    # this for loop in case there are iops for write and read
                    for c in match:
                        if c.group(1).endswith('K'):
                            disk_iops.append(int(float(c.group(1).replace('K',''))*1000))
                        else:
                            disk_iops.append(int(c.group(1)))
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

            ovs_ip = get_vm_ovs_node(int(machineId), ovc)
            vm_ovsip_iops_list.append({'machineId': machineId, 'ovs_ip': ovs_ip, 'iops': total_iops})

            os.chdir('%s' %Res_dir)

    ovs_list, iops_list = sum_iops_per_ovs(vm_ovsip_iops_list)
    collect_results(ovs_list, iops_list, Res_dir)




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


if __name__ == "__main__":
    main()
