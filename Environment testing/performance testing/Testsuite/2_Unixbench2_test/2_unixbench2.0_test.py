#!/usr/local/bin/jspython
from JumpScale import j
import uuid
import sys
import os
from fabric import network
import time
import multiprocessing
import ConfigParser


def main():
    config = ConfigParser.ConfigParser()
    config.read("Testsuite/2_Unixbench2_test/parameters.cfg")
    vms_time_diff = int(config.get("parameters", "vms_time_diff"))
    cpus = int(config.get("parameters", "cpus"))
    memory = int(config.get("parameters", "memory"))
    Bdisksize = int(config.get("parameters", "Bdisksize"))
    no_of_disks=0; data_disksize=0;
    vm_specs = [no_of_disks, data_disksize, Bdisksize, memory, cpus]

    j.do.execute('mkdir -p /Unixbench_results')
    j.do.execute('rm -rf /Unixbench_results/*')
    if j.do.exists('/root/.ssh/known_hosts'):
        j.do.execute('rm /root/.ssh/known_hosts')
    sys.path.append(os.getcwd())
    from utils import utils

    ccl = j.clients.osis.getNamespace('cloudbroker')
    pcl = j.clients.portal.getByInstance('main')
    scl = j.clients.osis.getNamespace('system')

    USERNAME = 'unixbench2testuser'
    email = "%s@test.com" % str(uuid.uuid4())[0:8]
    utils.create_user(USERNAME, email,  pcl, scl)
    ACCOUNTNAME = str(uuid.uuid4())[0:8]
    accountId = utils.create_account(USERNAME, email, ACCOUNTNAME, ccl, pcl)
    cloudspace = utils.create_cloudspace(accountId, ccl, pcl)
    cloudspace_publicport = 2000

    current_stack = ccl.stack.search({'referenceId': str(j.application.whoAmI.nid), 'gid': j.application.whoAmI.gid})[1]
    stacks=utils.get_stacks(ccl)
    stacks.remove(current_stack['id'])
    stacks_temp = []

    def select_stackid():
        global stacks_temp
        ns = list(set(stacks) - set(stacks_temp))
        stacks_temp.append(ns[0])
        if (len(stacks_temp) == len(stacks)):
            stacks_temp=[]
        return ns[0]

    machines=[]
    iteration=1
    [machineId, cloudspace_ip] = utils.create_machine_onStack(select_stackid(), cloudspace, iteration, ccl, pcl, scl, vm_specs, cloudspace_publicport, Res_dir='test_res')
    utils.Install_unixbench(machineId, cloudspace, cloudspace_publicport, pcl, sendscript='Testsuite/2_Unixbench2_test/2_machine_script.py')
    machines.append([machineId, cloudspace_ip, cloudspace_publicport])
    VM1_score = utils.Run_unixbench(machines[0], cpus, pcl)
    print('VM1_score = %s' %VM1_score) # for checking.. remove it later
    titles = ['Index', 'VM', 'CPU\'s', 'Memory(MB)', 'HDD(GB)', 'Avg. Unixbench Score']
    results=[[1, machineId, cpus, memory, Bdisksize, VM1_score]]
    utils.collect_results(titles, results, '/Unixbench_results')
    network.disconnect_all()

    cloudspace_publicport = 2001
    iteration=2
    score=10000 # just fake number for intializations
    while(score >= 0.5*VM1_score):
        #make sure to implement which stackid
        [machineId, cloudspace_ip] = utils.create_machine_onStack(select_stackid(), cloudspace, iteration, ccl, pcl, scl, vm_specs, cloudspace_publicport, Res_dir='test_res')
        connection = utils.Install_unixbench(machineId, cloudspace, cloudspace_publicport, pcl, sendscript='Testsuite/2_Unixbench2_test/2_machine_script.py')
        machines.append([machineId, cloudspace_ip ,cloudspace_publicport])
        q= multiprocessing.Queue()
        processes = []
        res_arr=[]
        network.disconnect_all()
        for vm in machines:
            p = multiprocessing.Process(target=utils.Run_unixbench, args=(vm, cpus, pcl, q))
            processes.append(p)
        for l in range(len(machines)):
            processes[l].start()
            time.sleep(vms_time_diff)
        for k in range(len(machines)):
            processes[k].join()
        for n in range(len(machines)):
            res_arr.append(q.get())

        res_arr.sort()
        #first machine unixbench score for iteration i
        score = res_arr[0][1]
        results=[]
        for s in res_arr:
            results.append([res_arr.index(s)+1, s[0], cpus, memory, Bdisksize, s[1]])
        utils.collect_results(titles, results, '/Unixbench_results')
        iteration += 1
        cloudspace_publicport += 1


if __name__ == "__main__":
    stacks_temp = []
    try:
        main()
    finally:
        j.do.execute('jspython scripts/tear_down.py unixbench2testuser')











