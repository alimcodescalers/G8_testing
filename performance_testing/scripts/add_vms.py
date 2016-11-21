#!/usr/bin/python3
from gevent import monkey
monkey.patch_all()
from libtest import run_cmd_via_gevent, wait_until_remote_is_listening, safe_get_vm, get_logger
from argparse import ArgumentParser
import gevent
import signal
import time
import os
import sys
from gevent.lock import BoundedSemaphore
from JumpScale import j
_cloudspace_semaphores = dict()
_stats = dict(deployed_vms=0, deployed_cloudspaces=0)
_vmnamecache = dict()

TEMPLATE_NAME = 'performance_testing'

logger = get_logger('add_vms')


def get_publicport_semaphore(cloudspace_id):
    if cloudspace_id not in _cloudspace_semaphores:
        _cloudspace_semaphores[cloudspace_id] = BoundedSemaphore()
    return _cloudspace_semaphores[cloudspace_id]


def get_vm_name(cloudspace_id, counter):
    return "vm-{0}-{1:0>3}".format(cloudspace_id, counter)


class Deployer(object):
    def __init__(self, options):
        self.options = options
        self.ovc = j.clients.openvcloud.get(options.environment,
                                            options.username,
                                            options.password)

        # Get account id
        print('Getting account id')
        tmp = self.ovc.api.cloudapi.accounts.list()
        if len(tmp) != 1:
            print('FAILURE: Expected to only find 1 account and found {}'.format(len(tmp)))
            return
        self.account_id = tmp[0]['id']

        # Get location gid
        print('Getting location gid')
        self.gid = next((loc['gid'] for loc in self.ovc.api.cloudapi.locations.list() if loc['locationCode'] == options.location), None)
        if self.gid is None:
            print('FAILURE: Could not determine gid')
            sys.exit(1)

    def create_performance_test_image(self):
        image_id = next((img['id'] for img in self.ovc.api.cloudapi.images.list(accountId=self.account_id) if img['name'] == TEMPLATE_NAME), None)
        if image_id:
            print('Found template for performance_testing')
            return image_id
        print('Checking if source image is available')
        image_id = next((img['id'] for img in self.ovc.api.cloudapi.images.list() if img['name'] == options.image), None)
        if image_id is None:
            print('FAILURE: Could not find image.')
            sys.exit(1)

        print('Creating template_space')
        cloudspace_id = self.deploy_cloudspace('template_space')
        machine = self.safe_deploy_vm('template_vm', cloudspace_id, image_id)
        cloudspace = self.ovc.api.cloudapi.cloudspaces.get(cloudspaceId=cloudspace_id)
        print('Installing requirements')
        self.install_req(machine, cloudspace)
        print('Stopping template vm')
        self.ovc.api.cloudapi.machines.stop(machineId=machine['id'])
        print('Making template')
        templateid = self.ovc.api.cloudapi.machines.createTemplate(machineId=machine['id'], templatename=TEMPLATE_NAME)
        print('Remove portforwarding from templatevm')
        self.ovc.api.cloudapi.portforwarding.deleteByPort(cloudspaceId=cloudspace_id,
                                                          publicIp=cloudspace['externalnetworkip'],
                                                          publicPort=machine['public_port'],
                                                          proto='tcp')
        return templateid

    def install_req(self, machine, cloudspace):
        account = machine['accounts'][0]

        # Wait until vm accepts connections
        wait_until_remote_is_listening(cloudspace['publicipaddress'], machine['public_port'])

        # Copy install_deps.sh to vm
        templ = 'sshpass -p "{0}" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
        templ += ' -P {1} install_deps.sh {2}@{3}:/home/{2}'
        cmd = templ.format(account['password'], machine['public_port'], account['login'], cloudspace['externalnetworkip'])
        run_cmd_via_gevent(cmd)

        # Run bash script on vm
        templ = 'sshpass -p "{0}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p {1} {2}@{3} '
        templ += '\'echo "{0}" | sudo -S bash /home/{2}/install_deps.sh\''
        cmd = templ.format(account['password'], machine['public_port'], account['login'], cloudspace['externalnetworkip'])
        run_cmd_via_gevent(cmd)

    def safe_deploy_vm(self, name, cloudspace_id, image_id, datadisk=None, iops=None):
        while True:
            try:
                return self.deploy_vm(name, cloudspace_id, image_id, datadisk, iops)
            except Exception as e:
                templ = "Failed creating machine {} in cloudspace {}, \nError: {}\nretrying ..."
                logger.error(templ.format(name, cloudspace_id, str(e)))
                gevent.sleep(10)
                while True:
                    try:
                        machines = self.ovc.api.cloudapi.machines.list(cloudspaceId=cloudspace_id)
                        machine_id = next((m['id'] for m in machines if m['name'] == name), None)
                        if machine_id is None:
                            break
                        self.ovc.api.cloudapi.machines.delete(machineId=machine_id)
                        break
                    except Exception as e:
                        templ = "Failed cleaning up machine {} in cloudspace {}, \nError: {}\nretrying ..."
                        logger.error(templ.format(name, cloudspace_id, str(e)))
                        gevent.sleep(10)

    def deploy_vm(self, name, cloudspace_id, image_id, datadisk=None, iops=None):
        # Listing sizes
        sizes = self.ovc.api.cloudapi.sizes.list(cloudspaceId=cloudspace_id)
        size_id = next((s['id'] for s in sizes if (self.options.bootdisk in s['disks'] and
                                                   self.options.memory == s['memory'] and
                                                   self.options.cpu == s['vcpus'])), None)
        if size_id is None:
            raise ValueError("No matching size for vm found.")

        if options.iops < 0:
            raise ValueError("Maximum iops can't be a negative value")

        # Create vm
        with concurrency:
            print("Creating {}".format(name))
            datadisks = [int(datadisk)] if datadisk else []
            vm_id = self.ovc.api.cloudapi.machines.create(cloudspaceId=cloudspace_id,
                                                          name=name,
                                                          description=name,
                                                          sizeId=size_id,
                                                          imageId=image_id,
                                                          disksize=options.bootdisk,
                                                          datadisks=datadisks)

        # limit the IOPS on all the disks of the vm
        machine = safe_get_vm(self.ovc, concurrency, vm_id)
        if iops is not None:
            for disk in machine['disks']:
                if disk['type'] != 'D':
                    continue
                with concurrency:
                    print("Set limit of iops to {} on disk {}({}) for machine {}".format(options.iops,
                                                                                         disk['name'],
                                                                                         disk['id'],
                                                                                         name))
                    self.ovc.api.cloudapi.disks.limitIO(diskId=disk['id'], iops=iops)

        # Wait until vm has ip address
        start = time.time()
        while True:
            gevent.sleep(5)
            machine = safe_get_vm(self.ovc, concurrency, vm_id)
            ip = machine['interfaces'][0]['ipAddress']
            if ip != 'Undefined':
                break
            now = time.time()
            if now > start + 600:
                raise RuntimeError("Machine {} did not get an ip within 600 seconds".format(vm_id))
            print("Waiting {} seconds for an IP for VM {}".format(int(now - start), name))

        # Configure portforward to ssh port of vm
        print("Configuring portforward for machine {}".format(name))
        cloudspace = self.ovc.api.cloudapi.cloudspaces.get(cloudspaceId=cloudspace_id)
        with get_publicport_semaphore(cloudspace_id):
            public_ports = [int(pf['publicPort']) for pf in self.ovc.api.cloudapi.portforwarding.list(cloudspaceId=cloudspace_id)]
            public_ports.append(19999)
            public_port = max(public_ports) + 1
            with concurrency:
                self.ovc.api.cloudapi.portforwarding.create(cloudspaceId=cloudspace_id,
                                                            publicIp=cloudspace['publicipaddress'],
                                                            publicPort=public_port,
                                                            machineId=vm_id,
                                                            localPort=22,
                                                            protocol='tcp')
        machine['public_port'] = public_port
        print("Machine {} deployed succesfully.".format(name))
        _stats['deployed_vms'] += 1
        return machine

    def deploy_cloudspace(self, name):
        # Create cloudspace
        with concurrency:
            print("Creating cloudspace {}".format(name))
            cloudspace_id = self.ovc.api.cloudapi.cloudspaces.create(accountId=self.account_id,
                                                                     location=options.location,
                                                                     name=name,
                                                                     access=options.username)

            print("Deploying cloudspace {}".format(name))
            self.ovc.api.cloudapi.cloudspaces.deploy(cloudspaceId=cloudspace_id)
            _stats['deployed_cloudspaces'] += 1
            return cloudspace_id


def main(options):
    # Check dependencies
    if not (os.path.exists('install_deps.sh') and os.path.exists('/usr/bin/sshpass')):
        print("Not all dependencies are met. Make sure the install_deps.sh script" +
              " is in the current directory and sshpass is installed.")
        return

    deployer = Deployer(options)
    # Can we find the image we need ?
    templateimage_id = deployer.create_performance_test_image()

    jobs = list()
    print('Checking if we need more cloudspaces')
    cloudspaces = list(filter(lambda space: space['name'].startswith('space-'), deployer.ovc.api.cloudapi.cloudspaces.list()))
    if len(cloudspaces) < options.cloudspaces:
        jobs.extend([gevent.spawn(deployer.deploy_cloudspace, 'space-{0:0>3}'.format(x))
                     for x in range(len(cloudspaces) + 1, int(options.cloudspaces) + 1)])

    gevent.joinall(jobs)
    jobs = list()
    # Add vms in existing cloudspaces
    cloudspaces = list(filter(lambda space: space['name'].startswith('space-'), deployer.ovc.api.cloudapi.cloudspaces.list()))
    print('Checking if we need more vms in existing cloudspaces')
    for cloudspace in cloudspaces:
        cloudspace_id = cloudspace['id']
        expected_vms = [get_vm_name(cloudspace_id, x) for x in range(1, options.vmachines + 1)]
        for vm in deployer.ovc.api.cloudapi.machines.list(cloudspaceId=cloudspace_id):
            if vm['name'] in expected_vms:
                expected_vms.remove(vm['name'])
        jobs.extend([gevent.spawn(deployer.safe_deploy_vm, vm_name, cloudspace_id, templateimage_id, options.datadisk, options.iops)
                     for vm_name in expected_vms])
    gevent.joinall(jobs)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-u", "--user", dest="username",
                        help="username to login on the OVC api", required=True)
    parser.add_argument("-p", "--pwd", dest="password",
                        help="password to login on the OVC api", required=True)
    parser.add_argument("-e", "--env", dest="environment",
                        help="environment to login on the OVC api", required=True)
    parser.add_argument("-l", "--loc", dest="location",
                        help="location to create cloudspaces")
    parser.add_argument("-c", "--clspcs", dest="cloudspaces", type=int,
                        default=5, help="minimum number of cloudspaces")
    parser.add_argument("-v", "--vms", dest="vmachines", type=int,
                        default=5, help="minimum number of vmachines per cloudspace")
    parser.add_argument("-i", "--img", dest="image", default='Ubuntu 16.04 x64',
                        help="image to use for creating vmachines")
    parser.add_argument("-b", "--boot", dest="bootdisk", type=int,
                        help="bootdisk size", default=10)
    parser.add_argument("-d", "--data", dest="datadisk", type=int,
                        help="datadisk size", default=20)
    parser.add_argument("-m", "--mem", dest="memory", default=1024, type=int,
                        help="amount of memory for the virtual machines")
    parser.add_argument("-k", "--cpu", dest="cpu", default=1, type=int,
                        help="amount of vcpus for the virtual machines")
    parser.add_argument("-o", "--iops", dest="iops", default=600, type=int,
                        help="maximum of iops of the disks for the virtual machines")
    parser.add_argument("-n", "--con", dest="concurrency", default=2, type=int,
                        help="amount of concurrency to execute the job")

    options = parser.parse_args()
    concurrency = BoundedSemaphore(options.concurrency)
    gevent.signal(signal.SIGQUIT, gevent.kill)
    start = time.time()
    main(options)
    end = time.time()
    elapsed = int(end - start)
    minutes = int(elapsed / 60)
    seconds = elapsed % 60
    tmpl = "Deployed {} cloudspace(s) and {} machine(s) in {} minutes and {} seconds"
    print(tmpl.format(_stats['deployed_cloudspaces'], _stats['deployed_vms'],
          minutes, seconds))
