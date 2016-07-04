#!/usr/local/bin/jspython
import sys
import os
from JumpScale import j
import ConfigParser
import uuid
import multiprocessing
import time
import datetime
from fabric import network
import re


def main():
    ccl = j.clients.osis.getNamespace('cloudbroker')
    pcl = j.clients.portal.getByInstance('main')
    scl = j.clients.osis.getNamespace('system')

    #run the setup_test from inside the repo so the file could be parsed
    config = ConfigParser.ConfigParser()
    config.read("Perf_parameters.cfg")
    iterations = int(config.get("perf_parameters", "iterations"))
    No_of_cloudspaces = int(config.get("perf_parameters", "No_of_cloudspaces"))
    used_stacks = int(config.get("perf_parameters", "used_stacks"))
    memory = int(config.get("perf_parameters", "memory"))
    cpu = int(config.get("perf_parameters", "cpu"))
    Bdisksize = int(config.get("perf_parameters", "Bdisksize"))
    no_of_disks = int(config.get("perf_parameters", "no_of_disks"))
    data_disksize = int(config.get("perf_parameters", "data_disksize"))
    vms_time_diff = int(config.get("perf_parameters", "vms_time_diff"))
    testrun_time = int(config.get("perf_parameters", "testrun_time"))
    data_size = int(config.get("perf_parameters", "data_size"))
    IO_type = config.get("perf_parameters", "IO_type")
    bs=config.get("perf_parameters", "bs")
    iodepth=int(config.get("perf_parameters", "iodepth"))
    direct_io=int(config.get("perf_parameters", "direct_io"))
    rwmixwrite=int(config.get("perf_parameters", "direct_io"))
    USERNAME = config.get("perf_parameters", "username")
    Res_dir = config.get("perf_parameters", "Res_dir")
    j.do.execute("mkdir -p %s" %Res_dir)
    hostname = j.do.execute('hostname')[1].replace("\n","")
    test_num = len(os.listdir('%s'%Res_dir))+1
    test_folder = "/"+datetime.datetime.today().strftime('%Y-%m-%d')+"_"+hostname+"_testresults_%s"%test_num
    Res_dir = Res_dir + test_folder

    try:
        if not j.do.exists('%s' % Res_dir):
            j.do.execute('mkdir -p %s' % Res_dir)
        if j.do.exists('/root/.ssh/known_hosts'):
            j.do.execute('rm /root/.ssh/known_hosts')
        sys.path.append(os.getcwd())

        from utils import utils
        j.do.execute('cp Perf_parameters.cfg %s' %Res_dir)
        stacks = utils.get_stacks(ccl)
        stack = ccl.stack.search({'referenceId': str(j.application.whoAmI.nid), 'gid': j.application.whoAmI.gid})[1]
        vm_specs = [no_of_disks, data_disksize, Bdisksize, memory, cpu]
        cloudspace_publicport = 1999
        vms_list = [] #list of vms
        cloudspace_of_stacks= {} # indicate the stack's cloudspace
        cloudspaces_cre = 0 # keep track of created cloudspaces
        cs_count = 0 # passes on created cloudscpaces
        cloudspaces_created = []

        email = "%s@test.com" % str(uuid.uuid4())[0:8]
        utils.create_user(USERNAME, email,  pcl, scl)

        i = 1 # keep track of iterations
        while i <= iterations:
            print ('###################### \n Starting Iteration(%s) \n######################'%i)
            used_stacks = int(config.get("perf_parameters", "used_stacks"))
            for stackid in stacks:
                if used_stacks == 0:
                    used_stacks = int(config.get("perf_parameters", "used_stacks"))
                    break
                if stackid == stack['id']:
                    continue
                if i == 1 and cloudspaces_cre == No_of_cloudspaces:
                    if cs_count == len(cloudspaces_created):
                        cs_count = 0
                    cloudspace = cloudspaces_created[cs_count]
                    cloudspace_of_stacks['stack %s' % stackid] = cloudspace
                    cs_count += 1
                if i == 1 and cloudspaces_cre < No_of_cloudspaces:
                    ACCOUNTNAME = str(uuid.uuid4())[0:8]
                    cloudspace = utils.create_account_cloudspace(USERNAME, email, ACCOUNTNAME, ccl, pcl, scl)
                    cloudspace_of_stacks['stack %s' % stackid] = cloudspace
                    cloudspaces_created.append(cloudspace)
                    cloudspaces_cre += 1

                cs = cloudspace_of_stacks['stack %s' % stackid]
                cloudspace_publicport += 1
                [machineId, cloudspace_publicip] = utils.create_machine_onStack(stackid, cs, i, ccl, pcl, scl, vm_specs, cloudspace_publicport, Res_dir)
                if IO_type:
                    vms_list.append({machineId: [cloudspace_publicip, cloudspace_publicport, IO_type]})
                elif cloudspace_publicport%2 == 0:
                    vms_list.append({machineId: [cloudspace_publicip, cloudspace_publicport, 'write']})
                else:
                    vms_list.append({machineId: [cloudspace_publicip, cloudspace_publicport, 'randwrite']})

                used_stacks -= 1

            # make ur tests and collect ur resutls before going to the next iteration
            network.disconnect_all()
            #terminate all connections before setting up them again
            processes = []
            for iter_on_vms in vms_list:
                p = multiprocessing.Process(target=utils.FIO_test, args=(iter_on_vms, pcl, data_size,
                                                                         testrun_time, Res_dir, i, no_of_disks,
                                                                         rwmixwrite, bs, iodepth, direct_io))
                processes.append(p)
            for l in range(len(vms_list)):
                dict = vms_list[l]
                processes[l].start()
                print('FIO testing has been started on machine: %s' % dict.keys()[0])
                time.sleep(vms_time_diff)
            for k in range(len(vms_list)):
                dict = vms_list[k]
                processes[k].join()
                print('FIO testing has been ended on machine: %s' % dict.keys()[0])
            i += 1
        match = re.search('/(201.+)', Res_dir)
        utils.write_onecsv_to_another('VMs_creation_time.csv', match.group(1), Res_dir)
        return Res_dir
    except:
        print('Found problems during running the test.. removing results directory..')
        j.do.execute('rm -rf %s' %Res_dir)
        raise


if __name__ == "__main__":
    sys.path.append(os.getcwd())
    from utils import utils

    try:
        Res_dir = main()
    finally:
        j.do.execute('cp scripts/collect_results.py %s' %Res_dir)
        j.do.chdir('%s' %Res_dir)
        j.do.execute('python collect_results.py %s' %Res_dir)
        j.do.execute('rm -rf collect_results.py')
    utils.push_results_to_repo(Res_dir, test_type='FIO_test')