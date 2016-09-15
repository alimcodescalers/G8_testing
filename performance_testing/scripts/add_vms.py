#!/usr/bin/python3
from gevent import monkey
monkey.patch_all()
from JumpScale import j
from optparse import OptionParser
import gevent
import signal
import time
from gevent.coros import BoundedSemaphore
_cloudspace_semaphores = dict()


def get_publicport_semaphore(cloudspace_id):
    if cloudspace_id not in _cloudspace_semaphores:
        _cloudspace_semaphores[cloudspace_id] = BoundedSemaphore()
    return _cloudspace_semaphores[cloudspace_id]


def install_req(ovc, vm_id, cloudspace, public_port, name):
    with concurrency:
        vm = ovc.api.cloudapi.machines.get(machineId=vm_id)
    account = vm['accounts'][0]
    exc = j.tools.executor.getSSHBased(cloudspace['publicipaddress'], port=public_port,
                                       passwd=account['password'], login=account['login'])
    connection = j.tools.cuisine.get(exc)
    print("Installing performance test packages on {}".format(name))
    connection.core.sudo('apt-get update')
    connection.core.sudo('echo "Y" | sudo apt-get install fio libx11-dev ' +
                         'libgl1-mesa-dev libxext-dev perl perl-modules make')
    print("Downloading and compiling unixbench-5 on {}".format(name))
    connection.core.sudo('wget http://byte-unixbench.googlecode.com/files/unixbench-5.1.3.tgz')
    connection.core.sudo('tar xvf unixbench-5.1.3.tgz')
    connection.core.sudo('mv unixbench-5.1.3 unixbench')


def deploy_vm(options, ovc, account_id, gid, name, cloudspace_id, image_id):
    # Listing sizes
    with concurrency:
        sizes = ovc.api.cloudapi.sizes.list(cloudspaceId=cloudspace_id)
    size_id = next((s['id'] for s in sizes if (options.bootdisk in s['disks'] and
                                               options.memory == s['memory'] and
                                               options.cpu == s['vcpus'])), None)
    if size_id is None:
        raise ValueError("No matching size for vm found.")

    # Create vm
    print("Creating {}".format(name))
    with concurrency:
        vm_id = ovc.api.cloudapi.machines.create(cloudspaceId=cloudspace_id,
                                                 name=name,
                                                 description=name,
                                                 sizeId=size_id,
                                                 imageId=image_id,
                                                 disksize=options.bootdisk,
                                                 datadisks=[int(options.datadisk)])

    # Wait until vm has ip address
    start = time.time()
    while True:
        gevent.sleep(2)
        with concurrency:
            machine = ovc.api.cloudapi.machines.get(machineId=vm_id)
        ip = machine['interfaces'][0]['ipAddress']
        if ip != 'Undefined':
            break
        now = time.time()
        if now > start + 300:
            raise RuntimeError("Machine {} did not get an ip within 300 seconds".format(vm_id))
        print("Waiting {} seconds for an IP for VM {}".format(int(now - start), name))

    # Configure portforward to ssh port of vm
    print("Configuring portforward for machine {}".format(name))
    with concurrency:
        cloudspace = ovc.api.cloudapi.cloudspaces.get(cloudspaceId=cloudspace_id)
    with get_publicport_semaphore(cloudspace_id):
        public_ports = [pf['publicPort'] for pf in ovc.api.cloudapi.portforwarding.list(cloudspaceId=cloudspace_id)]
        public_ports.append(19999)
        public_port = max(public_ports) + 1
        ovc.api.cloudapi.portforwarding.create(cloudspaceId=cloudspace_id,
                                               publicIp=cloudspace['publicipaddress'],
                                               publicPort=public_port,
                                               machineId=vm_id,
                                               localPort=22,
                                               protocol='tcp')

    # Install fio & unixbench via cuisine on the vm
    install_req(ovc, vm_id, cloudspace, public_port, name)
    print("Machine {} deployed succesfully.".format(name))


def deploy_cloudspace(options, ovc, account_id, name, image_id, gid):
    # Create cloudspace
    print("Creating cloudspace {}".format(name))
    with concurrency:
        cloudspace_id = ovc.api.cloudapi.cloudspaces.create(accountId=account_id,
                                                            location=options.location,
                                                            name=name,
                                                            access=options.username)
    # Create first vm to force the routeros deployment
    print("Deploying first vm in cloudspace {}".format(name))
    deploy_vm(options, ovc, account_id, gid, "vm-{0}-{1:0>3}".format(cloudspace_id, 0),
              cloudspace_id, image_id)

    # Deploy the remaining vms
    jobs.extend([gevent.spawn(deploy_vm, options, ovc, account_id, gid,
                              "vm-{0}-{1:0>3}".format(cloudspace_id, x),
                              cloudspace_id, image_id) for x in range(1, options.vmachines)])


def main(options):
    ovc = j.clients.openvcloud.get(options.environment,
                                   options.username,
                                   options.password)
    # Can we find the image we need ?
    print('Checking if image is available')
    image_id = next((img['id'] for img in ovc.api.cloudapi.images.list() if img['name'] == options.image), None)
    if image_id is None:
        print('FAILURE: Could not find image.')
        return

    # Get account id
    print('Getting account id')
    tmp = ovc.api.cloudapi.accounts.list()
    if len(tmp) != 1:
        print('FAILURE: Expected to only find 1 account and found {}'.format(len(tmp)))
        return
    account_id = tmp[0]['id']

    # Get location gid
    print('Getting location gid')
    gid = next((loc['gid'] for loc in ovc.api.cloudapi.locations.list() if loc['locationCode'] == options.location),
               None)
    if gid is None:
        print('FAILURE: Could not determine gid')
        return

    # Create cloudspaces if needed
    print('Checking if we need more cloudspaces')
    cloudspaces = ovc.api.cloudapi.cloudspaces.list()
    if len(cloudspaces) < options.cloudspaces:
        jobs.extend([gevent.spawn(deploy_cloudspace, options, ovc, account_id,
                                  'space-{0:0>3}'.format(x), image_id,
                                  gid) for x in range(len(tmp) + 1, int(options.cloudspaces) + 1)])

    # Add vms in existing cloudspaces
    print('Checking if we need more vms in existing cloudspaces')
    for cloudspace in cloudspaces:
        cloudspace_id = cloudspace['id']
        with concurrency:
            vm_count = len(ovc.api.cloudapi.machines.list(cloudspaceId=cloudspace_id))
        jobs.extend([gevent.spawn(deploy_vm, options, ovc, account_id, gid,
                                  "vm-{0}-{1:0>3}".format(cloudspace_id, x),
                                  cloudspace_id, image_id) for x in range(vm_count, options.vmachines)])

    gevent.joinall(jobs)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--user", dest="username", type="string",
                      help="username to login on the OVC api")
    parser.add_option("-p", "--pwd", dest="password", type="string",
                      help="password to login on the OVC api")
    parser.add_option("-e", "--env", dest="environment", type="string",
                      help="environment to login on the OVC api")
    parser.add_option("-l", "--loc", dest="location", type="string",
                      help="location to create cloudspaces")
    parser.add_option("-c", "--clspcs", dest="cloudspaces", type="int",
                      default=5, help="minimum number of cloudspaces")
    parser.add_option("-v", "--vms", dest="vmachines", type="int",
                      default=5, help="minimum number of vmachines per cloudspace")
    parser.add_option("-i", "--img", dest="image", default='Ubuntu 16.04 x64', type="string",
                      help="image to use for creating vmachines")
    parser.add_option("-b", "--boot", dest="bootdisk", type="int",
                      help="bootdisk size", default=10)
    parser.add_option("-d", "--data", dest="datadisk", type="int",
                      help="datadisk size", default=20)
    parser.add_option("-m", "--mem", dest="memory", default=1024, type="int",
                      help="amount of memory for the virtual machines")
    parser.add_option("-k", "--cpu", dest="cpu", default=1, type="int",
                      help="amount of vcpus for the virtual machines")
    parser.add_option("-n", "--con", dest="concurrency", default=5, type="int",
                      help="amount of concurrency to execute the job")

    (options, args) = parser.parse_args()
    if not options.username or not options.password or not options.environment:
        parser.print_usage()
    else:
        concurrency = BoundedSemaphore(options.concurrency)
        jobs = list()
        gevent.signal(signal.SIGQUIT, gevent.kill)
        main(options)

