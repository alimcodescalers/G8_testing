#!/usr/bin/python3
from gevent import monkey
monkey.patch_all()
from libtest import run_cmd_via_gevent, wait_until_remote_is_listening, safe_get_vm, check_package, push_results_to_repo
import gevent
from gevent.lock import BoundedSemaphore
import signal
from optparse import OptionParser
import os
import datetime

machines_running = set()
machines_complete = set()


def mount_disks(ovc, machine_id, publicip, publicport):
    # only one data disk for this test
    machine = safe_get_vm(ovc, concurrency, machine_id)
    account = machine['accounts'][0]
    templ = 'sshpass -p "{}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p {} {}@{} '
    templ += ' bash mount_disk.sh {} b'
    cmd = templ.format(account['password'], publicport, account['login'], publicip,
                       account['password'])
    print('mounting disks for machine:%s' % machine_id)
    run_cmd_via_gevent(cmd)


def prepare_fio_test(ovc, options, machine_id, publicip, publicport):
    print("Preparing fio test on machine {}".format(machine_id))
    machine = safe_get_vm(ovc, concurrency, machine_id)
    account = machine['accounts'][0]

    wait_until_remote_is_listening(publicip, int(publicport), True, machine_id)

    templ = 'sshpass -p{} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
    templ += '-P {} {}/1_fio_vms/Machine_script.py  {}@{}:'
    cmd = templ.format(account['password'], publicport, options.testsuite, account['login'], publicip)
    run_cmd_via_gevent(cmd)

    return machine_id, publicip, publicport, account


def fio_test(options, machine_id, publicip, publicport, account):
    machines_running.add(machine_id)
    # only one data disk for this test
    disks_num = 1
    templ = 'sshpass -p "{}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p {} {}@{} '
    templ += ' python Machine_script.py {} {} {} {} {} {} {} {} {} {} {} {} {} {}'
    cmd = templ.format(account['password'], publicport, account['login'], publicip,
                       options.testrun_time, machine_id, account['password'], 1, disks_num,
                       options.data_size, options.write_type, options.block_size, options.iodepth,
                       options.direct_io, options.rwmixwrite, options.rate_iops, options.numjobs, options.filesystem)
    print('FIO testing has been started on machine: {}'.format(machine_id))
    run_cmd_via_gevent(cmd)
    machines_complete.add(machine_id)
    running = machines_running.difference(machines_complete)
    complete = (len(machines_running) - len(running)) / len(machines_running) * 100.0
    print('Testing completed for {:.2f}%'.format(complete))
    if complete >= 90.0:
        print('Waiting for machines {} to complete their test ...'.format(' '.join(str(x) for x in running)))

    return account, publicport, publicip, machine_id


def assemble_fio_test_results(results_dir, account, publicport, cloudspace_publicip, machine_id):
    print('Collecting results from machine: {}'.format(machine_id))
    templ = 'sshpass -p{} scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
    templ += '-P {}  {}@{}:machine{}_iter{}_{}_results {}/'
    cmd = templ.format(account['password'], publicport, account['login'], cloudspace_publicip,
                       machine_id, 1, options.write_type, results_dir)
    run_cmd_via_gevent(cmd)


def main(options):
    from JumpScale import j

    # Check dependencies
    if not os.path.exists(options.results_dir):
        print("Not all dependencies are met. Make sure the result directory exists.")
        return

    if not check_package('sshpass') or not check_package('python3-prettytable'):
        return

    # Prepare test run
    hostname = run_cmd_via_gevent('hostname').replace("\n", "")
    test_num = len(os.listdir('{}'.format(options.results_dir))) + 1
    test_dir = "/" + datetime.datetime.today().strftime('%Y-%m-%d')
    test_dir += "_" + hostname + "_testresults_{}".format(test_num)
    results_dir = options.results_dir + test_dir
    run_cmd_via_gevent('mkdir -p {}'.format(results_dir))

    # list virtual and deployed cloudspaces
    vms = []
    vms_index = set()
    ovc = j.clients.openvcloud.get(options.environment, options.username, options.password)
    cloudspaces_per_user = ovc.api.cloudapi.cloudspaces.list()
    for cs in cloudspaces_per_user:
        portforwards = ovc.api.cloudapi.portforwarding.list(cloudspaceId=cs['id'])
        for pi in portforwards:
            if 'machineId' not in pi or pi['machineId'] in vms_index:
                continue
            vms.append([pi['machineId'], pi['publicIp'], pi['publicPort']])
            vms_index.add(pi['machineId'])

    if len(vms) < options.required_vms:
        print("Not enough vms available to run this test. {} < {}".format(len(vms), options.required_vms))
        return
    vms = vms[:options.required_vms]

    # prepare fio tests
    pjobs = [gevent.spawn(prepare_fio_test, ovc, options, *vm) for vm in vms]
    gevent.joinall(pjobs)

    # mount disks if the filesystem will be used
    mjobs = [gevent.spawn(mount_disks, ovc, *vm) for vm in vms]
    gevent.joinall(mjobs)

    # run fio tests
    rjobs = [gevent.spawn(fio_test, options, *job.value) for job in pjobs if job.value is not None]
    gevent.joinall(rjobs)

    # collect results from machines
    rjobs = [gevent.spawn(assemble_fio_test_results, results_dir, *job.value) for job in rjobs if job.value is not None]
    gevent.joinall(rjobs)

    # collecting results in csv file
    cwd = os.getcwd()
    j.do.copyFile('{}/1_fio_vms/collect_results.py'.format(options.testsuite), results_dir)
    os.chdir(results_dir)
    j.do.execute('python3 collect_results.py {} {} {} {}'.format(results_dir, options.environment,
                                                                 options.username, options.password))

    # pushing results to env_repo
    os.chdir(cwd)
    location = options.environment.split('.')[0]
    push_results_to_repo(results_dir, location)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--user", dest="username", type="string",
                      help="username to login on the OVC api")
    parser.add_option("-p", "--pwd", dest="password", type="string",
                      help="password to login on the OVC api")
    parser.add_option("-e", "--env", dest="environment", type="string",
                      help="environment to login on the OVC api")
    parser.add_option("-d", "--ds", dest="data_size", type="int",
                      default=1000, help="Amount of data to be written per each data disk per VM (in MB)")
    parser.add_option("-t", "--run_time", dest="testrun_time", type="int",
                      default=300, help=" Test-rum time per virtual machine  (in seconds)")
    parser.add_option("-w", "--IO_type", dest="write_type", type="string",
                      default="randrw", help="Type of I/O pattern")
    parser.add_option("-m", "--mixwrite", dest="rwmixwrite", type="int",
                      default=20, help=" Percentage of a mixed workload that should be writes")
    parser.add_option("-b", "--bs", dest="block_size", type="string",
                      default='4k', help="Block size")
    parser.add_option("-i", "--iodp", dest="iodepth", type="int",
                      default=128, help="number of I/O units to keep in flight against the file")
    parser.add_option("-o", "--dio", dest="direct_io", type="int",
                      default=1, help="If direct_io = 1, use non-buffered I/O.")
    parser.add_option("-x", "--max_iops", dest="rate_iops", type="int",
                      default=8000, help="Cap the bandwidth to this number of IOPS")
    parser.add_option("-j", "--numjobs", dest="numjobs", type="int",
                      default=1, help=" Number of clones (processes/threads performing the same workload) of this job")
    parser.add_option("-j", "--fs", dest="filesystem", type="int",
                      default=1, help="Equate filesystem to 1 if the disks will use the filesytem and equate it to 0 if you will use the disks as block devices")
    parser.add_option("-v", "--vms", dest="required_vms", type="int",
                      default=2, help=" selected number of virtual machines to run fio on")
    parser.add_option("-r", "--rdir", dest="results_dir", type="string",
                      default="/root/G8_testing/tests_results/FIO_test", help="absolute path fot results directory")
    parser.add_option("-n", "--con", dest="concurrency", default=2, type="int",
                      help="amount of concurrency to execute the job")
    parser.add_option("-s", "--ts", dest="testsuite", default="../Testsuite", type="string",
                      help="location to find Testsuite directory")

    (options, args) = parser.parse_args()
    if not options.username or not options.password or not options.environment:
        parser.print_usage()
    else:
        gevent.signal(signal.SIGQUIT, gevent.kill)
        concurrency = BoundedSemaphore(options.concurrency)
        main(options)
