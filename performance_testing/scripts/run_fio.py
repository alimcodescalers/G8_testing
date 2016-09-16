#!/usr/bin/python3
import gevent
from gevent.coros import BoundedSemaphore
import signal
from optparse import OptionParser
import os
from JumpScale import j
import datetime
from libtest import run_cmd_via_gevent, check_remote_is_listening, safe_get_vm, check_package


def prepare_fio_test(ovc, options, machine_id, publicip, publicport):
    print("Preparing fio test on machine {}".format(machine_id))
    machine = safe_get_vm(ovc, concurrency, machine_id)
    account = machine['accounts'][0]

    check_remote_is_listening(publicip, int(publicport))

    templ = 'sshpass -p{} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
    templ += '-P {} {}/1_fio_vms/Machine_script.py  {}@{}:'
    cmd = templ.format(account['password'], publicport, options.testsuite, account['login'], publicip)
    run_cmd_via_gevent(cmd)

    return machine_id, publicip, publicport, account


def fio_test(options, machine_id, publicip, publicport, account):
    print('FIO testing has been started on machine: {}'.format(machine_id))

    templ = 'sshpass -p "{}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p {} {}@{} '
    templ += ' python Machine_script.py {} {} {} {} {} {} {} {} {} {} {} {} {}'
    cmd = templ.format(account['password'], publicport, account['login'], publicip,
                       options.testrun_time, machine_id, account['password'], 1, options.no_of_disks,
                       options.data_size, options.write_type, options.block_size, options.iodepth,
                       options.direct_io, options.rwmixwrite, options.rate_iops, options.numjobs)
    run_cmd_via_gevent(cmd)

    return account, publicport, publicip, machine_id


def assemble_fio_test_results(account, publicport, cloudspace_publicip, machine_id, results_dir):
    print('Collecting results from machine: {}'.format(machine_id))
    templ = 'sshpass -p{} scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
    templ += '-P {}  {}@{}:machine{}_iter{}_{}_results {}/'
    cmd = templ.format(account['password'], publicport, account['login'], cloudspace_publicip,
                       machine_id, 1, options.write_type, results_dir)
    run_cmd_via_gevent(cmd)


def main(options):
    # Check dependencies
    if not os.path.exists(options.results_dir):
        print("Not all dependencies are met. Make sure the result directory exists.")
        return

    if not check_package('sshpass') or not check_package('python-prettytable'):
        return

    # Prepare test run
    hostname = run_cmd_via_gevent('hostname').replace("\n", "")
    test_num = len(os.listdir('{}'.format(options.results_dir))) + 1
    test_dir = "/" + datetime.datetime.today().strftime('%Y-%m-%d')
    test_dir += "_" + hostname + "_testresults_{}".format(test_num)
    results_dir = options.results_dir + test_dir

    # list virtual and deployed cloudspaces
    vms = []
    ovc = j.clients.openvcloud.get(options.environment, options.username, options.password)
    cloudspaces_per_user = ovc.api.cloudapi.cloudspaces.list()
    for cs in cloudspaces_per_user:
        portforwards = ovc.api.cloudapi.portforwarding.list(cloudspaceId=cs['id'])
        for pi in portforwards:
            vms.append([pi['machineId'], pi['publicIp'], pi['publicPort']])

    # prepare fio tests
    prepare_jobs = [gevent.spawn(prepare_fio_test, ovc, options, *vm) for vm in vms]
    gevent.joinall(prepare_jobs)

    # run fio tests
    run_jobs = [gevent.spawn(fio_test, options, *job.value) for job in prepare_jobs if job.value is not None]
    gevent.joinall(run_jobs)

    # collect results from machines
    run_jobs = [gevent.spawn(assemble_fio_test_results, *job.value, results_dir) for job in run_jobs if job.value]
    gevent.joinall(run_jobs)

    # collecting results in csv file
    # j.do.copyFile('{}/1_fio_vms/collect_results.py'.format(options.testsuite), results_dir)
    # j.do.chdir(results_dir)
    # j.do.execute('python2 collect_results.py {}'.format(results_dir))


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
    parser.add_option("-c", "--nod", dest="no_of_disks", type="int",
                      default=1, help="Number of data disks per VM")
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