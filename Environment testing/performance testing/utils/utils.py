from JumpScale import j
import netaddr
import time
from JumpScale.portal.portal.PortalClient2 import ApiError
from prettytable import PrettyTable


def get_stacks(ccl):
    return ccl.stack.list()

def create_user(USERNAME, email, pcl, scl):
    print "Creating User with username %s" %USERNAME
    pcl.actors.cloudbroker.user.create(USERNAME, email, 'gig12345')
    user = scl.user.get(USERNAME)
    user.groups.extend([u'level1', u'level2', u'level3', u'admin',u'finance',u'ovs_admin',u'user'])
    scl.user.set(user)

def create_account_cloudspace(USERNAME, email, ACCOUNTNAME, ccl, pcl, scl):

    loc = ccl.location.search({})[1]['locationCode']

    print 'Creating Account with accountname %s' % ACCOUNTNAME
    accountId = pcl.actors.cloudbroker.account.create(ACCOUNTNAME, USERNAME, email, loc)
    #Refactor the cloudspace part
    cloudspaces = ccl.cloudspace.search({'accountId': accountId,
                                        'status': {'$in': ['VIRTUAL', 'DEPLOYED']}})[1:]
    if not cloudspaces:
        msg = "Not cloudspace available for account %s, disabling test" % ACCOUNTNAME
        return [{'message': msg, 'category': 'Storage Test', 'state': 'OK'}]
    else:
        cloudspace = cloudspaces[0]
    if cloudspace['status'] == 'VIRTUAL':
        print 'Deploying CloudSpace'
        pcl.actors.cloudbroker.cloudspace.deployVFW(cloudspace['id'])
        # retreive cloudspace with Public IP set
        cloudspace = ccl.cloudspace.get(cloudspace['id']).dump()
    return cloudspace

def create_machine_onStack(stackid, cloudspace, iteration, ccl, pcl, scl, vm_specs, cs_publicport=0,  Res_dir=None, queue=None):

    images = ccl.image.search({'name': 'Ubuntu 14.04 x64'})[1:]
    if not images:
        return [{'message': "Image not available (yet)", 'category': 'Storage Test', 'state': "ERROR"}]
    imageId = images[0]['id']

    size = ccl.size.search({'memory': vm_specs[3], 'vcpus': vm_specs[4]})
    if size[0] == 0:
        size = ccl.size.search({'memory': 2048, 'vcpus': 2})[1]
    else:
        size = ccl.size.search({'memory': vm_specs[3], 'vcpus': vm_specs[4]})[1]

    sizeId = size['id']

    if vm_specs[2] in [10, 20, 50, 100, 250, 500, 1000, 2000]:
        boot_diskSize = vm_specs[2]
    else:
        boot_diskSize = size['disks'][3]

    datadisks_list = [vm_specs[1] for x in range(vm_specs[0])]

    cloudspace_publicip = str(netaddr.IPNetwork(cloudspace['publicipaddress']).ip)
    print('Creating new machine...')
    t1 = time.time()

    try:
        machineId = pcl.actors.cloudbroker.machine.createOnStack(cloudspaceId=cloudspace['id'],
                                                             name='node%s%s' % (stackid, iteration), imageId=imageId, sizeId=sizeId,
                                                             disksize=boot_diskSize, stackid=stackid, datadisks=datadisks_list)
    except ApiError as e:
        print('   |--failed to create the machine with error: %s' %e.message)
        vm = ccl.vmachine.search({'name': 'node%s%s'% (stackid, iteration), 'cloudspaceId': cloudspace['id']})
        if vm[0] != 0:
            ccl.vmachine.delete(vm[1]['id'])
        print('   |--trying to create the machine once more')
        machineId = pcl.actors.cloudbroker.machine.createOnStack(cloudspaceId=cloudspace['id'],
                                                             name='node%s%s' % (stackid, iteration), imageId=imageId, sizeId=sizeId,
                                                             disksize=boot_diskSize, stackid=stackid, datadisks=datadisks_list)

    print('   |--finished creating machine: %s' % machineId)
    if queue:
        #needed for 4_unixbench for parallel execution
        queue.put([machineId, cloudspace_publicip, cs_publicport, cloudspace])
    if Res_dir != 'NoIP':
        now = time.time()
        ip = 'Undefined'
        print '   |--Waiting for IP for VM: node%s%s' % (stackid, iteration)
        while now + 100 > time.time() and ip == 'Undefined':
            time.sleep(1)
            machine = pcl.actors.cloudapi.machines.get(machineId)
            ip = machine['interfaces'][0]['ipAddress']
        pcl.actors.cloudapi.portforwarding.create(cloudspace['id'], cloudspace_publicip, cs_publicport, machineId, 22, 'tcp')

        if not j.system.net.waitConnectionTest(cloudspace_publicip, cs_publicport, 60):
            print 'Could not connect to VM over public interface'
    if not Res_dir or Res_dir=='NoIP':
        return machineId
    elif Res_dir=='test_res':
        return [machineId, cloudspace_publicip]
    else:
        t2 = time.time()
        time_creating_vm = round(t2-t1, 2)
        j.do.execute('echo \'VM: %s  - creation time: %s sec\' >> %s/VMs_creation_time.txt' %(machineId, time_creating_vm, Res_dir))
        cloudspace_publicip = setup_machine(cloudspace, machineId, cs_publicport, pcl, vm_specs[0])
        return [machineId, cloudspace_publicip]

def setup_machine(cloudspace, machineId, cs_publicport, pcl, no_of_disks, fio=None):
    print ('   |--setup machine:%s' %machineId)
    cloudspace_publicip = str(netaddr.IPNetwork(cloudspace['publicipaddress']).ip)

    machine = pcl.actors.cloudapi.machines.get(machineId)
    account = machine['accounts'][0]

    if not j.system.net.waitConnectionTest(cloudspace_publicip, cs_publicport, 40):
        print 'Could not connect to VM over public interface'
    else:
        connection = j.remote.cuisine.connect(cloudspace_publicip, cs_publicport, account['password'], account['login'])
        connection.fabric.state.output["running"]=False
        connection.fabric.state.output["stdout"]=False
        connection.user(account['login'])
        connection.apt_get('update')
        connection.apt_get('install fio')
        if fio != 'onlyfio':
            connection.apt_get('install sysstat')
            machine_mount_disks(connection, account, machineId, no_of_disks)
    return cloudspace_publicip

def machine_mount_disks(connection, account, machineId, no_of_disks=6):
    list=['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
    print('   |--mounting disks for machine:%s' %machineId)

    for i in range(no_of_disks):
        connection.run('echo %s | sudo -S echo -n ; echo n; echo p; echo 1; echo -ne \'\n\'; echo -ne \'\n\'; echo w | sudo fdisk /dev/vd%s' %(account['password'],list[i]))
        connection.run('echo %s | sudo -S mkfs.ext4 /dev/vd%s' %(account['password'],list[i]))
        connection.run('echo %s | sudo -S mkdir -p /mnt/disk_%s' %(account['password'],list[i]))
        connection.run('echo %s | sudo -S mount /dev/vd%s /mnt/disk_%s' %(account['password'],list[i], list[i]))
    print('   |--finished mounting')

def FIO_test(vm_pubip_pubport, pcl, data_size, testrun_time, Res_dir, iteration, no_of_disks):
    machineId = vm_pubip_pubport.keys()[0]
    cloudspace_publicip = vm_pubip_pubport.values()[0][0]
    cs_publicport = vm_pubip_pubport.values()[0][1]
    write_type = vm_pubip_pubport.values()[0][2]

    machine = pcl.actors.cloudapi.machines.get(machineId)
    account = machine['accounts'][0]

    if not j.system.net.waitConnectionTest(cloudspace_publicip, cs_publicport, 20):
        print 'Could not connect to VM over public interface'
    else:
        connection = j.remote.cuisine.connect(cloudspace_publicip, cs_publicport, account['password'], account['login'])
        connection.user(account['login'])
        j.do.execute('sshpass -p%s scp -o \'StrictHostKeyChecking=no\' -P %s scripts/Machine_script.py  %s@%s:'
                     %(account['password'], cs_publicport, account['login'], cloudspace_publicip))
        connection.run('python Machine_script.py %s %s %s %s %s %s %s' %(testrun_time, machineId, account['password'], iteration, no_of_disks, data_size, write_type))
        j.do.execute('sshpass -p%s scp -r -o \'StrictHostKeyChecking=no \' -P %s  %s@%s:machine%s_iter%s_%s_results %s/'
                     %(account['password'], cs_publicport, account['login'], cloudspace_publicip, machineId, iteration, write_type, Res_dir))



# These utils is used for the testsuite

def create_account(USERNAME, email, ACCOUNTNAME, ccl, pcl):

    loc = ccl.location.search({})[1]['locationCode']
    print 'Creating Account with accountname %s' % ACCOUNTNAME
    accountId = pcl.actors.cloudbroker.account.create(ACCOUNTNAME, USERNAME, email, loc)
    return accountId

def create_cloudspace(accountId, username, ccl, pcl, cs_name=''):
        loc = ccl.location.search({})[1]['locationCode']
        cloudspace_id = pcl.actors.cloudapi.cloudspaces.create(accountId=accountId, location=loc,
                                                              name=cs_name or 'default', access=username)
        print 'Deploying CloudSpace'
        pcl.actors.cloudbroker.cloudspace.deployVFW(cloudspace_id)
        # retreive cloudspace with Public IP set
        cloudspace = ccl.cloudspace.get(cloudspace_id).dump()
        return cloudspace

#install unixbench on a given machine
def Install_unixbench(machineId, cloudspace, cs_publicport, pcl, sendscript=None):
    print ('   |--installing Unixbench on machine:%s' %machineId)
    cloudspace_publicip = str(netaddr.IPNetwork(cloudspace['publicipaddress']).ip)
    machine = pcl.actors.cloudapi.machines.get(machineId)
    account = machine['accounts'][0]

    if not j.system.net.waitConnectionTest(cloudspace_publicip, cs_publicport, 40):
        print 'Could not connect to VM over public interface'
    else:
        connection = j.remote.cuisine.connect(cloudspace_publicip, cs_publicport, account['password'], account['login'])
        connection.fabric.state.output["running"]=False
        connection.fabric.state.output["stdout"]=False
        connection.user(account['login'])
        connection.apt_get('update')
        connection.apt_get('install build-essential libx11-dev libgl1-mesa-dev libxext-dev')
        connection.run('echo %s | sudo -S wget http://byte-unixbench.googlecode.com/files/UnixBench5.1.3.tgz' %account['password'])
        connection.run('echo %s | sudo -S tar xvfz UnixBench5.1.3.tgz' %account['password'])
        if sendscript:
            j.do.execute('sshpass -p%s scp -o \'StrictHostKeyChecking=no\' -P %s %s  %s@%s:'
                         %(account['password'], cs_publicport, sendscript, account['login'], cloudspace_publicip))
	print('   |--finished installation on machine:%s' %machineId)
        return connection

def Run_unixbench(VM, cpu_cores, pcl, queue=None):
        machineId = VM[0]
        cloudspace_ip = VM[1]
        cloudspace_publicport = VM[2]
        machine = pcl.actors.cloudapi.machines.get(machineId)
        account = machine['accounts'][0]
        connection = j.remote.cuisine.connect(cloudspace_ip, cloudspace_publicport, account['password'], account['login'])
        connection.fabric.state.output["running"]=False
        connection.fabric.state.output["stdout"]=False
        #change cloudscalers to account login
        print('   |--Running UnixBench on machine:%s' %machineId)
        connection.run('cd /home/cloudscalers/UnixBench; echo %s | sudo -S ./Run -c %s -i 3 > /home/cloudscalers/test_res.txt' %(account['password'],cpu_cores))
        score = connection.run('python 2_machine_script.py')
        print('   |--finished running UnixBench on machine:%s' %machineId)
        #connection.run('rm /test_res.txt')
        if queue:
            queue.put([machineId, score])
        score = float(score)
        return score

#collects results in a table
def collect_results(titles, results, Res_dir, iteration=0):
    table = PrettyTable(titles)
    for i in results:
        table.add_row(i)
    table_txt = table.get_string()
    with open('%s/results.table' %Res_dir,'a') as file:
        file.write('\n%s'%table_txt)

#utils for VM live migration test

def run_script(account, cloudspace_publicip, cloudspace_publicport, testname):
    connection = j.remote.cuisine.connect(cloudspace_publicip, cloudspace_publicport, account['password'], account['login'])
    connection.fabric.state.output["running"]=False
    connection.fabric.state.output["stdout"]=False
    connection.user(account['login'])
    connection.run('python machine_script.py %s  ' %(testname))


def check_script(account, cloudspace_publicip, cloudspace_publicport, file1, file2):
    connection = j.remote.cuisine.connect(cloudspace_publicip, cloudspace_publicport, account['password'], account['login'])
    connection.fabric.state.output["running"]=False
    connection.fabric.state.output["stdout"]=False
    connection.user(account['login'])
    return connection.run('python check_script.py %s %s ' %(file1, file2))

def wirtefile_on_vm(account, cloudspace_publicip, cloudspace_publicport, filename):
    connection = j.remote.cuisine.connect(cloudspace_publicip, cloudspace_publicport, account['password'], account['login'])
    connection.fabric.state.output["running"]=False
    connection.fabric.state.output["stdout"]=False
    connection.run('touch %s' %filename)
    return connection
