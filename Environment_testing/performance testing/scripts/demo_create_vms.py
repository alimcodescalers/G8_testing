#!/usr/local/bin/jspython
import sys
import os
from JumpScale import j
import ConfigParser
import uuid


def main():
    ccl = j.clients.osis.getNamespace('cloudbroker')
    pcl = j.clients.portal.getByInstance('main')
    scl = j.clients.osis.getNamespace('system')

    No_of_vms=20

    #run the setup_test from inside the repo so the file could be parsed
    config = ConfigParser.ConfigParser()
    config.read("Perf_parameters.cfg")
    used_stacks = int(config.get("perf_parameters", "used_stacks"))
    memory = int(config.get("perf_parameters", "memory"))
    cpu = int(config.get("perf_parameters", "cpu"))
    Bdisksize = int(config.get("perf_parameters", "Bdisksize"))
    no_of_disks = int(config.get("perf_parameters", "no_of_disks"))
    data_disksize = int(config.get("perf_parameters", "data_disksize"))
    USERNAME = config.get("perf_parameters", "username")
    ACCOUNTNAME = str(uuid.uuid4())[0:8]
    Res_dir = config.get("perf_parameters", "Res_dir")
    j.do.execute('mkdir -p %s' % Res_dir)


    sys.path.append(os.getcwd())

    from utils import utils
    stacks = utils.get_stacks(ccl)
    current_stack = ccl.stack.search({'referenceId': str(j.application.whoAmI.nid), 'gid': j.application.whoAmI.gid})[1]
    stacks.remove(current_stack['id'])
    vm_specs = [no_of_disks, data_disksize, Bdisksize, memory, cpu]
    cloudspace_publicport = 1999
    vms_list = [] #list of vms

    email = "%s@test.com" % str(uuid.uuid4())[0:8]
    utils.create_user(USERNAME, email,  pcl, scl)
    cloudspace = utils.create_account_cloudspace(USERNAME, email, ACCOUNTNAME, ccl, pcl, scl)

    vms_list = []
    i=0
    while i < No_of_vms:
        for stackId in stacks:
            cloudspace_publicport += 1
            machineId, cloudspace_publicip = utils.create_machine_onStack(stackId, cloudspace, '_%s' %i, ccl, pcl, scl, vm_specs, cloudspace_publicport, Res_dir)
            vms_list.append({machineId: [cloudspace_publicip, cloudspace_publicport]})
            i += 1
            if i == No_of_vms:
                break

if __name__ == "__main__":
    main()
