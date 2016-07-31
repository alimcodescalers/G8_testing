#!/usr/local/bin/jspython
from JumpScale import j
import uuid
import sys
import os
import time
import multiprocessing
import ConfigParser
import datetime
import netaddr


def main():
    config = ConfigParser.ConfigParser()
    config.read("Testsuite/4_Unixbench_test/parameters.cfg")
    unixbench_run_times = int(config.get("parameters", "unixbench_run_times"))
    cpus = int(config.get("parameters", "cpus"))
    memory = int(config.get("parameters", "memory"))
    Bdisksize = int(config.get("parameters", "Bdisksize"))
    vms_time_diff = int(config.get("parameters", "vms_time_diff"))
    no_of_disks=0; data_disksize=0;
    vm_specs = [no_of_disks, data_disksize, Bdisksize, memory, cpus]
    vms_per_cs = 7; unixb_vms_per_cs = 2 ; cs_per_stack = 2
    Res_dir = config.get("parameters", "Res_dir")

    j.do.execute("mkdir -p %s" %Res_dir)
    hostname = j.do.execute('hostname')[1].replace("\n","")
    test_num = len(os.listdir('%s'%Res_dir))+1
    test_folder = "/"+datetime.datetime.today().strftime('%Y-%m-%d')+"_"+hostname+"_testresults_%s"%test_num
    Res_dir = Res_dir + test_folder

    try:

        if not j.do.exists('%s' % Res_dir):
            j.do.execute('mkdir -p %s' % Res_dir)

        sys.path.append(os.getcwd())
        from utils import utils

        ccl = j.clients.osis.getNamespace('cloudbroker')
        pcl = j.clients.portal.getByInstance('main')
        scl = j.clients.osis.getNamespace('system')

        USERNAME = 'unixbenchuser'
        email = "%s@test.com" % str(uuid.uuid4())[0:8]
        utils.create_user(USERNAME, email,  pcl, scl)
        ACCOUNTNAME = str(uuid.uuid4())[0:8]
        accountId = utils.create_account(USERNAME, email, ACCOUNTNAME, ccl, pcl)

        current_stack = ccl.stack.search({'referenceId': str(j.application.whoAmI.nid), 'gid': j.application.whoAmI.gid})[1]
        stacks=utils.get_stacks(ccl)

        loc = ccl.location.search({})[1]['locationCode']
        cloudspaces=[]
        for stackid in stacks:
            if stackid == current_stack['id']:
                continue
            print('creating %s cloudspaces for stackId:%s' %(cs_per_stack, stackid))
            for i in range(cs_per_stack):
                print('   |--creating cloudspace No.%s'%(i+1))
                cloudspaceId = pcl.actors.cloudapi.cloudspaces.create(accountId=accountId,location=loc,name='CS%s%s'%(i,stackid),access=USERNAME)
                pcl.actors.cloudbroker.cloudspace.deployVFW(cloudspaceId)
                cloudspace = ccl.cloudspace.get(cloudspaceId).dump()
                cloudspaces.append([cloudspace, stackid])

        cloudspace_publicport=4000
        q= multiprocessing.Queue()
        unixbench_machines=[]
        processes = []
        for cs in cloudspaces:
            cloudspace = cs[0]
            stackid = cs[1]
            for i in range(vms_per_cs):
                if(i < unixb_vms_per_cs):
                    p = multiprocessing.Process(target=utils.create_machine_onStack, args=(stackid, cloudspace, i, ccl, pcl, scl, vm_specs, cloudspace_publicport, 'test_res', q))
                    cloudspace_publicport += 1
                else:
                    p = multiprocessing.Process(target=utils.create_machine_onStack, args=(stackid, cloudspace, i, ccl, pcl, scl, vm_specs, 0, 'wait_for_VMIP', None))
                processes.append(p)

        for l in range(len(processes)):
            processes[l].start()
            time.sleep(0.5)
        for k in range(len(processes)):
            processes[k].join()
        for h in range(unixb_vms_per_cs*cs_per_stack*(len(stacks)-1)):
            unixbench_machines.append(q.get())

        # installing unixbench on machines
        print('Installing Unixbench on required machines')
        processes = []
        for vm in unixbench_machines:
            vmid = vm[0]; cs = vm[3]; cs_pp = vm[2]
            p = multiprocessing.Process(target=utils.Install_unixbench, args=(vmid, cs, cs_pp, pcl, 'Testsuite/2_Unixbench2_test/2_machine_script.py'))
            processes.append(p)
        for l in range(len(processes)):
            processes[l].start()
            time.sleep(0.5)
        for k in range(len(processes)):
            processes[k].join()

        # Running unixbench on machines
        print('Running Unixbench on required machines')
        titles = ['Index', 'VM', 'CPU\'s', 'Memory(MB)', 'HDD(GB)', 'Avg. Unixbench Score']
        final_results=[]
        for t in range(unixbench_run_times):
            print('Running Unixbench for iteration No.%s'%(t+1))
            processes = []
            res_arr=[]
            q= multiprocessing.Queue()
            for vm in unixbench_machines:
                p = multiprocessing.Process(target=utils.Run_unixbench, args=(vm, cpus, pcl, q))
                processes.append(p)
            for l in range(len(processes)):
                processes[l].start()
                time.sleep(vms_time_diff)
            for k in range(len(processes)):
                processes[k].join()
            for n in range(len(processes)):
                res_arr.append(q.get())
            res_arr.sort()

            results=[]
            for s in res_arr:
                results.append([res_arr.index(s)+1, s[0], cpus, memory, Bdisksize, s[1]])
            utils.collect_results(titles, results, '%s' %Res_dir)

            for i in range(len(res_arr)):
                if final_results == []:
                    final_results = res_arr
                else:
                    final_results[i].append(res_arr[i][1])

        results = []
        for s in final_results:
            avg = round(sum([float(i) for i in s[1:]])/len(s[1:]), 1)
            results.append([final_results.index(s)+1, s[0], cpus, memory, Bdisksize, avg])
        utils.collect_results(titles, results, '%s' %Res_dir)

	#Removing vms fingerprints from known hosts
        for vm in unixbench_machines:
            cs = vm[3]; cs_pp = vm[2]
            cloudspace_publicip = str(netaddr.IPNetwork(cs['publicipaddress']).ip)
            j.do.execute('ssh-keygen -f "/root/.ssh/known_hosts" -R [%s]:%s'%(cloudspace_publicip, cs_pp))

        utils.push_results_to_repo(Res_dir)
    except:
        print('Found problems during running the test.. removing results directory..')
        for vm in unixbench_machines:
            cs = vm[3]; cs_pp = vm[2]
            cloudspace_publicip = str(netaddr.IPNetwork(cs['publicipaddress']).ip)
            j.do.execute('ssh-keygen -f "/root/.ssh/known_hosts" -R [%s]:%s'%(cloudspace_publicip, cs_pp))
        j.do.execute('rm -rf %s' %Res_dir)
        raise


if __name__ == "__main__":
    try:
        main()
    finally:
        j.do.execute('jspython scripts/tear_down.py unixbenchuser')


