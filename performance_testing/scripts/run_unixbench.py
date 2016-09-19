#!/usr/bin/python3
import gevent
from gevent.coros import BoundedSemaphore
import signal
from optparse import OptionParser
import os
from JumpScale import j
import datetime
from libtest import run_cmd_via_gevent, check_remote_is_listening, safe_get_vm, check_package
import csv
import re



def results_on_csvfile(csv_file_name, Res_dir, table_string):
    result=[]
    for line in table_string.splitlines():
        splitdata = line.split("|")
        if len(splitdata) == 1:
            continue  # skip lines with no separators
        linedata = []
        for field in splitdata:
            field = field.strip()
            if field:
                linedata.append(field)
        result.append(linedata)

    with open('%s/%s.csv'%(Res_dir, csv_file_name), 'a') as outcsv:
           writer = csv.writer(outcsv)
           writer.writerows(result)

#collects results in a table
def collect_results(titles, results, Res_dir):
    from prettytable import PrettyTable
    table = PrettyTable(titles)
    for i in results:
        table.add_row(i)
    table_txt = table.get_string()
    with open('%s/results.table' %Res_dir,'a') as file:
        file.write('\n%s'%table_txt)
    match = re.search('/(201.+)', Res_dir)
    results_on_csvfile(match.group(1), Res_dir, table_txt)


def prepare_unixbench_test(options, ovc, cpu_cores, machine_id, publicip, publicport):
    print("Preparing unixbench test on machine {}".format(machine_id))
    machine = safe_get_vm(ovc, concurrency, machine_id)
    account = machine['accounts'][0]

    check_remote_is_listening(publicip, int(publicport))

    templ = 'sshpass -p{} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '
    templ += '-P {} {}/2_Unixbench2_test/2_machine_script.py  {}@{}:'
    cmd = templ.format(account['password'], publicport, options.testsuite, account['login'], publicip)
    run_cmd_via_gevent(cmd)

    return machine_id, publicip, publicport, account, cpu_cores


def unixbench_test(options, machine_id, publicip, publicport, account, cpu_cores):
    print('unixbench testing has been started on machine: {}'.format(machine_id))

    templ = 'sshpass -p "{}" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p {} {}@{} '
    templ += ' python 2_machine_script.py {} {} {}'
    cmd = templ.format(account['password'], publicport, account['login'], publicip,
                       account['password'], cpu_cores, options.test_runtime)
    score = run_cmd_via_gevent(cmd)

    return [machine_id, float(score)]


def main(options):
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
    j.do.execute('mkdir -p %s' % results_dir)

    # list virtual and deployed cloudspaces
    vms = []
    ovc = j.clients.openvcloud.get(options.environment, options.username, options.password)
    cloudspaces_per_user = ovc.api.cloudapi.cloudspaces.list()
    for cs in cloudspaces_per_user:
        portforwards = ovc.api.cloudapi.portforwarding.list(cloudspaceId=cs['id'])
        for pi in portforwards:
            vms.append([pi['machineId'], pi['publicIp'], pi['publicPort']])

    # getting bootdisk size, cpu and memory used during vms creatian (for any vm)
    machine = safe_get_vm(ovc, concurrency, pi['machineId'])
    bootdisk = machine['disks'][0]['sizeMax']
    size_id = machine['sizeid']
    sizes = ovc.api.cloudapi.sizes.list(cloudspaceId=cs['id'])
    memory = next((i for i in sizes if i['id'] == size_id), False)['memory']
    cpu = next((i for i in sizes if i['id'] == size_id), False)['vcpus']

    # prepare unixbench tests
    prepare_jobs = [gevent.spawn(prepare_unixbench_test, options, ovc, cpu, *vms[c])
                    for c in range(len(vms)) if c < options.required_vms]
    gevent.joinall(prepare_jobs)

    # run unixbench tests
    run_jobs = [gevent.spawn(unixbench_test, options, *job.value) for job in prepare_jobs if job.value is not None]
    gevent.joinall(run_jobs)

    raw_results = [job.value for job in run_jobs]
    raw_results.sort()
    results = []
    index = 0
    for s in raw_results:
        index += 1
        results.append([index, s[0], cpu, memory, bootdisk, s[1]])
    titles = ['Index', 'VM', 'CPU\'s', 'Memory(MB)', 'HDD(GB)', 'Avg. Unixbench Score']
    collect_results(titles, results, '%s' % results_dir)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--user", dest="username", type="string",
                      help="username to login on the OVC api")
    parser.add_option("-p", "--pwd", dest="password", type="string",
                      help="password to login on the OVC api")
    parser.add_option("-e", "--env", dest="environment", type="string",
                      help="environment to login on the OVC api")
    parser.add_option("-v", "--vms", dest="required_vms", type="int",
                      default=2, help=" selected number of virtual machines to run unixbench on")
    parser.add_option("-t", "--runtime", dest="test_runtime", type="int",
                      default=100, help="duration for running unixbecnh (in secs)")
    parser.add_option("-r", "--rdir", dest="results_dir", type="string",
                      default="/root/G8_testing/tests_results/unixbench", help="absolute path for results directory")
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
