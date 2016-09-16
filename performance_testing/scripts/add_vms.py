#!/usr/bin/python3
from optparse import OptionParser
import gevent
import signal
import time
import os
from libtest import run_cmd_via_gevent, wait_until_remote_is_listening, safe_get_vm
from gevent.coros import BoundedSemaphore
from gevent import monkey
monkey.patch_all()
_cloudspace_semaphores = dict()
_stats = dict(deployed_vms=0, deployed_cloudspaces=0)


def get_publicport_semaphore(cloudspace_id):
    if cloudspace_id not in _cloudspace_semaphores:
        _cloudspace_semaphores[cloudspace_id] = BoundedSemaphore()
    return _cloudspace_semaphores[cloudspace_id]


def install_req(ovc, machine, cloudspace, public_port, name):
    account = machine['accounts'][0]

    # Wait until vm accepts connections
    wait_until_remote_is_listening(cloudspace['publicipaddress'], public_port)

    # Copy install_deps.sh to vm
    templ = 'sshpass -p "{0}" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
    templ += ' -P {1} install_deps.sh {2}@{3}:/home/{2}'
    cmd = templ.format(account['password'], public_port, account['login'], cloudspace['publicipaddress'])
    run_cmd_via_gevent(cmd)

    # Run bash script on vm
    templ = 'sshpass -p "{0}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p {1} {2}@{3} '
    templ += '\'echo "{0}" | sudo -S bash /home/{2}/install_deps.sh\''
    cmd = templ.format(account['password'], public_port, account['login'], cloudspace['publicipaddress'])
    run_cmd_via_gevent(cmd)


def safe_deploy_vm(options, ovc, account_id, gid, name, cloudspace_id, image_id):
    while True:
        try:
            deploy_vm(options, ovc, account_id, gid, name, cloudspace_id, image_id)
            return
        except Exception as e:
            templ = "Failed creating machine {} in cloudspace {}, \nError: {}\nretrying ..."
            print(templ.format(name, cloudspace_id, str(e)))
            gevent.sleep(10)
            while True:
                try:
                    machines = ovc.api.cloudapi.machines.list(cloudspaceId=cloudspace_id)
                    machine_id = next((m['id'] for m in machines if m['name'] == name), None)
                    if machine_id is None:
                        break
                    ovc.api.cloudapi.machines.delete(machineId=machine_id)
                    break
                except Exception as e:
                    templ = "Failed cleaning up machine {} in cloudspace {}, \nError: {}\nretrying ..."
                    print(templ.format(name, cloudspace_id, str(e)))
                    gevent.sleep(10)


def deploy_vm(options, ovc, account_id, gid, name, cloudspace_id, image_id):
    # Listing sizes
    sizes = ovc.api.cloudapi.sizes.list(cloudspaceId=cloudspace_id)
    size_id = next((s['id'] for s in sizes if (options.bootdisk in s['disks'] and
                                               options.memory == s['memory'] and
                                               options.cpu == s['vcpus'])), None)
    if size_id is None:
        raise ValueError("No matching size for vm found.")

    if options.iops < 0:
        raise ValueError("Maximum iops can't be a negative value")

    # Create vm
    with concurrency:
        print("Creating {}".format(name))
        vm_id = ovc.api.cloudapi.machines.create(cloudspaceId=cloudspace_id,
                                                 name=name,
                                                 description=name,
                                                 sizeId=size_id,
                                                 imageId=image_id,
                                                 disksize=options.bootdisk,
                                                 datadisks=[int(options.datadisk)])

        # limit the IOPS on all the disks of the vm
        machine = ovc.api.cloudapi.machines.get(machineId=vm_id)
        for disk in machine['disks']:
            print("Set limit of iops to {} on disk {}({}) for machine {}".format(options.iops, disk['name'], disk['id'], name))
            ovc.api.cloudapi.disks.limitIO(diskId=disk['id'], iops=options.iops)

    # Wait until vm has ip address
    start = time.time()
    while True:
        gevent.sleep(5)
        machine = safe_get_vm(ovc, concurrency, vm_id)
        ip = machine['interfaces'][0]['ipAddress']
        if ip != 'Undefined':
            break
        now = time.time()
        if now > start + 300:
            raise RuntimeError("Machine {} did not get an ip within 300 seconds".format(vm_id))
        print("Waiting {} seconds for an IP for VM {}".format(int(now - start), name))

    # Configure portforward to ssh port of vm
    print("Configuring portforward for machine {}".format(name))
    cloudspace = ovc.api.cloudapi.cloudspaces.get(cloudspaceId=cloudspace_id)
    with get_publicport_semaphore(cloudspace_id):
        public_ports = [int(pf['publicPort']) for pf in ovc.api.cloudapi.portforwarding.list(cloudspaceId=cloudspace_id)]
        public_ports.append(19999)
        public_port = max(public_ports) + 1
        with concurrency:
            ovc.api.cloudapi.portforwarding.create(cloudspaceId=cloudspace_id,
                                                   publicIp=cloudspace['publicipaddress'],
                                                   publicPort=public_port,
                                                   machineId=vm_id,
                                                   localPort=22,
                                                   protocol='tcp')

    # Install fio & unixbench via cuisine on the vm
    install_req(ovc, machine, cloudspace, public_port, name)
    print("Machine {} deployed succesfully.".format(name))

    _stats['deployed_vms'] += 1


def deploy_cloudspace(options, ovc, account_id, name, image_id, gid):
    # Create cloudspace
    print("Creating cloudspace {}".format(name))
    cloudspace_id = ovc.api.cloudapi.cloudspaces.create(accountId=account_id,
                                                        location=options.location,
                                                        name=name,
                                                        access=options.username)
    # Create first vm to force the routeros deployment
    print("Deploying first vm in cloudspace {}".format(name))
    deploy_vm(options, ovc, account_id, gid, "vm-{0}-{1:0>3}".format(cloudspace_id, 0),
              cloudspace_id, image_id)

    # Deploy the remaining vms
    jobs = [gevent.spawn(safe_deploy_vm, options, ovc, account_id, gid,
                         "vm-{0}-{1:0>3}".format(cloudspace_id, x),
                         cloudspace_id, image_id) for x in range(1, options.vmachines)]
    gevent.joinall(jobs)

    _stats['deployed_cloudspaces'] += 1


def main(options):
    # Check dependencies
    if not (os.path.exists('install_deps.sh') and os.path.exists('/usr/bin/sshpass')):
        print("Not all dependencies are met. Make sure the install_deps.sh script" +
              " is in the current directory and sshpass is installed.")
        return

    from JumpScale import j
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
    jobs = list()
    print('Checking if we need more cloudspaces')
    cloudspaces = ovc.api.cloudapi.cloudspaces.list()
    if len(cloudspaces) < options.cloudspaces:
        jobs.extend([gevent.spawn(deploy_cloudspace, options, ovc, account_id,
                                  'space-{0:0>3}'.format(x), image_id,
                                  gid) for x in range(len(tmp), int(options.cloudspaces) + 1)])

    # Add vms in existing cloudspaces
    print('Checking if we need more vms in existing cloudspaces')
    for cloudspace in cloudspaces:
        cloudspace_id = cloudspace['id']
        with concurrency:
            vm_count = len(ovc.api.cloudapi.machines.list(cloudspaceId=cloudspace_id))
        jobs.extend([gevent.spawn(safe_deploy_vm, options, ovc, account_id, gid,
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
    parser.add_option("-o", "--iops", dest="iops", default=600, type="int",
                      help="maximum of iops of the disks for the virtual machines")
    parser.add_option("-n", "--con", dest="concurrency", default=2, type="int",
                      help="amount of concurrency to execute the job")

    (options, args) = parser.parse_args()
    if not options.username or not options.password or not options.environment:
        parser.print_usage()
    else:
        concurrency = BoundedSemaphore(options.concurrency)
        gevent.signal(signal.SIGQUIT, gevent.kill)
        start = time.time()
        main(options)
        end = time.time()
        elapsed = int(end - start)
        minutes = elapsed / 60
        seconds = elapsed % 60
        tmpl = "Deployed {} cloudspace(s) and {} machine(s) in {} minutes and {} seconds"
        print(tmpl.format(_stats['deployed_cloudspaces'], _stats['deployed_vms'],
              minutes, seconds))