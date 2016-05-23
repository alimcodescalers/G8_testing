#!/usr/local/bin/jspython
from JumpScale import j
import uuid
import os
import time
import sys


def main(snapshots_number):
    cpu = 1; memory = 512; Bdisksize = 10
    no_of_disks=0; data_disksize=0;
    vm_specs = [no_of_disks, data_disksize, Bdisksize, memory, cpu]

    ccl = j.clients.osis.getNamespace('cloudbroker')
    pcl = j.clients.portal.getByInstance('main')
    scl = j.clients.osis.getNamespace('system')

    if j.do.exists('/root/.ssh/known_hosts'):
        j.do.execute('rm /root/.ssh/known_hosts')
    sys.path.append(os.getcwd())
    from utils import utils
    USERNAME = 'vmsnapshotsuser'
    email = "%s@test.com" % str(uuid.uuid4())[0:8]
    utils.create_user(USERNAME, email,  pcl, scl)
    ACCOUNTNAME = str(uuid.uuid4())[0:8]
    accountId = utils.create_account(USERNAME, email, ACCOUNTNAME, ccl, pcl)
    cloudspace = utils.create_cloudspace(accountId, ccl, pcl)
    cloudspace_publicport = 2000

    current_stack = ccl.stack.search({'referenceId': str(j.application.whoAmI.nid), 'gid': j.application.whoAmI.gid})[1]
    stacks=utils.get_stacks(ccl)
    stacks.remove(current_stack['id'])
    stackid = stacks[0]

    print('A new machine will be created on the node with stackId:%s' %stackid) #################################################################3 name of the vm
    [machineId, cloudspace_publicip] = utils.create_machine_onStack(stackid, cloudspace, '_unlimited_snapshotvm', ccl, pcl, scl,
                                                                    vm_specs, cloudspace_publicport, Res_dir='test_res')
    machine = pcl.actors.cloudapi.machines.get(machineId)
    account = machine['accounts'][0]

    for i in range(snapshots_number):
        utils.wirtefile_on_vm(account, cloudspace_publicip, cloudspace_publicport, 'snapshot%s.txt' %(i+1))
        pcl.actors.cloudapi.machines.stop(machineId=machineId)
        print('   |--creating snapshot No.%s ...' %(i+1))
        pcl.actors.cloudapi.machines.snapshot(machineId=machineId, name='snapshot%s'%(i+1))
        pcl.actors.cloudapi.machines.start(machineId=machineId)
        time.sleep(20)

    print('Rolling back to snapshot No.%s ...' %(snapshots_number-1))
    pcl.actors.cloudapi.machines.stop(machineId=machineId)
    snapshots = pcl.actors.cloudapi.machines.listSnapshots(machineId=machineId)
    snapshots.sort()
    pcl.actors.cloudapi.machines.rollbackSnapshot(machineId=machineId,
                                                              epoch=snapshots[snapshots_number-2]['epoch'])
    pcl.actors.cloudapi.machines.start(machineId=machineId)
    time.sleep(20)

    connection = j.remote.cuisine.connect(cloudspace_publicip, cloudspace_publicport, account['password'], account['login'])
    count_snapshots = connection.run('ls -1 | wc -l')
    return count_snapshots[0]



if __name__ == "__main__":
    try:
        snapshots_number = int(sys.argv[1])
        count = main(snapshots_number)
    finally:
        compare = str(snapshots_number-1)
        if count == compare:
            print ('################ \n# Test succeed #\n################')
        else:
            print ('############### \n# Test Failed # \n###############')
        j.do.execute('jspython scripts/tear_down.py vmsnapshotsuser')