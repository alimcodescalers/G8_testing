#!/usr/local/bin/jspython
from JumpScale import j
import uuid
import sys
import os
import ConfigParser


def main():
    config = ConfigParser.ConfigParser()
    config.read("Testsuite/3_Env_Limit_test/parameters.cfg")
    cpu = int(config.get("parameters", "cpu"))
    memory = int(config.get("parameters", "memory"))
    Bdisksize = int(config.get("parameters", "Bdisksize"))
    no_of_disks=0; data_disksize=0;
    vm_specs = [no_of_disks, data_disksize, Bdisksize, memory, cpu]

    ccl = j.clients.osis.getNamespace('cloudbroker')
    pcl = j.clients.portal.getByInstance('main')
    scl = j.clients.osis.getNamespace('system')

    j.do.execute('mkdir -p /Env_limitation_results')
    j.do.execute('rm -rf /Env_limitation_results/*')

    USERNAME = 'envlimittestuser'
    email = "%s@test.com" % str(uuid.uuid4())[0:8]
    utils.create_user(USERNAME, email,  pcl, scl)
    ACCOUNTNAME = str(uuid.uuid4())[0:8]
    accountId = utils.create_account(USERNAME, email, ACCOUNTNAME, ccl, pcl)


    current_stack = ccl.stack.search({'referenceId': str(j.application.whoAmI.nid), 'gid': j.application.whoAmI.gid})[1]
    stacks=utils.get_stacks(ccl)

    cloudspace_publicport = 2000
    cloudspaces=[]
    for stackid in stacks:
        if stackid == current_stack['id']:
            continue
        print('creating cloudspace and corresponding vm ')
        loc = ccl.location.search({})[1]['locationCode']
        # change this to cloudbroker later, after api is fixed
        cloudspaceId = pcl.actors.cloudapi.cloudspaces.create(accountId=accountId,location=loc,name='CS%s'%stackid,access=USERNAME)
        pcl.actors.cloudbroker.cloudspace.deployVFW(cloudspaceId)
        cloudspace = ccl.cloudspace.get(cloudspaceId).dump()
        utils.create_machine_onStack(stackid, cloudspace, 0, ccl, pcl, scl, vm_specs, cloudspace_publicport, Res_dir='NoIP')
        cloudspaces.append([cloudspace, stackid])
        cloudspace_publicport += 1
    vms = 3
    iteration=1
    while(True):
        for cloudspace in cloudspaces:
            cs = cloudspace[0]
            stackid = cloudspace[1]
            try:
                print('creating VM No:%s' %(vms+1))
                utils.create_machine_onStack(stackid, cs, iteration, ccl, pcl, scl, vm_specs, cloudspace_publicport, Res_dir='NoIP')
                vms += 1
            except:
                print('   |--failed to create the machine')
                return [[cpu, memory, Bdisksize, vms]]
        iteration += 1
if __name__ == "__main__":
    if j.do.exists('/root/.ssh/known_hosts'):
        j.do.execute('rm /root/.ssh/known_hosts')
    sys.path.append(os.getcwd())
    from utils import utils
    try:
        results = main()
        titles = ['VM_CPU\'s', 'VM_Memory(MB)', 'HDD(GB)', 'Total VMs created']
        utils.collect_results(titles, results, '/Env_limitation_results')
    finally:
        j.do.execute('jspython scripts/tear_down.py envlimittestuser')



