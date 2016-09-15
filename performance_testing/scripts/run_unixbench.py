#!/usr/local/bin/jspython
import gevent
import signal
from optparse import OptionParser
from gevent.queue import Queue
import os
from JumpScale import j
import datetime
from utils import utils


def run_unixbench(vm, cpu_cores, ovc, queue=None):
    machineId = vm[0]
    cloudspace_ip = vm[1]
    publicport = vm[2]
    machine = ovc.api.cloudapi.machines.get(machineId=machineId)
    account = machine['accounts'][0]

    if not j.system.net.waitConnectionTest(cloudspace_ip, publicport, 20):
        print 'Could not connect to VM over public interface'
    else:
        sendscript = 'Testsuite/2_Unixbench2_test/2_machine_script.py'
        j.do.execute('sshpass -p%s scp -o \'StrictHostKeyChecking=no\' -P %s %s  %s@%s:'
                     % (account['password'], publicport, sendscript, account['login'], cloudspace_ip))

        exc = j.tools.executor.getSSHBased(cloudspace_ip, port=publicport,
                                           passwd=account['password'], login=account['login'])
        connection = j.tools.cuisine.get(exc)
        print('   |--Running UnixBench on machine:%s' % machineId)
        connection.core.run('cd /home/cloudscalers/UnixBench; echo %s | sudo -S ./Run -c %s -i 3 '
                            '> /home/cloudscalers/test_res.txt' %(account['password'], cpu_cores))
        score = connection.core.run('python 2_machine_script.py')
        print('   |--finished running UnixBench on machine:%s' % machineId)
        if queue:
            queue.put([machineId, score])
        score = float(score)
        return score




def main(options):
    ovc = j.clients.openvcloud.get(options.environment,
                                   options.username,
                                   options.password)

    if not j.do.exists('%s' % options.Res_dir):
        j.do.execute('mkdir -p %s' % options.Res_dir)

    hostname = j.do.execute('hostname')[1].replace("\n", "")
    test_num = len(os.listdir('%s' % options.Res_dir)) + 1
    test_folder = "/" + datetime.datetime.today().strftime('%Y-%m-%d') + "_" + hostname + "_testresults_%s" % test_num
    Res_dir = options.Res_dir + test_folder

    #make sure sshpass is installed
    j.do.execute('apt-get install sshpass')

    #getting portforwards
    machines = []
    cloudspaces_per_user = ovc.api.cloudapi.cloudspaces.list()
    for cs in cloudspaces_per_user:
        portforwards = ovc.api.cloudapi.portforwarding.list(cloudspaceId=cs['id'])
        for pi in portforwards:
            machines.append([pi['machineId'], pi['publicIp'], pi['publicPort']])

    # getting bootdisk size, cpu and memory used during vms creatian (for any vm)
    machine = ovc.api.cloudapi.machines.get(machineId=pi['machineId'])
    bootdisk = machine['disks'][0]['sizeMax']
    size_id = machine['sizeid']
    sizes = ovc.api.cloudapi.sizes.list(cloudspaceId=cs['id'])
    memory = next((i for i in sizes if i['id'] == size_id), False)['memory']
    cpu = next((i for i in sizes if i['id'] == size_id), False)['vcpus']

    # post results for first machine
    print('running unixbench on the first machine only')
    VM1_score = run_unixbench(machines[0], cpu, ovc)
    first_machineId = machines[0][0]
    titles = ['Index', 'VM', 'CPU\'s', 'Memory(MB)', 'HDD(GB)', 'Avg. Unixbench Score']
    results = [[1, first_machineId, cpu, memory, bootdisk, VM1_score]]
    utils.collect_results(titles, results, '%s' % Res_dir)


    # running unixbench in parallel
    queue = Queue()
    jobs.extend([gevent.spawn(run_unixbench, vm, cpu, ovc, queue) for vm in machines])
    gevent.joinall(jobs)

    res_arr = []
    while not queue.empty():
        res_arr.append(queue.get())

    res_arr.sort()
    results = []
    for s in res_arr:
        results.append([res_arr.index(s) + 1, s[0], cpu, memory, bootdisk, s[1]])
    utils.collect_results(titles, results, '%s' % Res_dir)


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
    parser.add_option("-r", "--rdir", dest="Res_dir", type="string",
                      default="/root/G8_testing/tests_results/unixbench", help="absolute path fot results directory")

    (options, args) = parser.parse_args()
    if not options.username or not options.password or not options.environment:
        parser.print_usage()
    else:
        jobs = list()
        gevent.signal(signal.SIGQUIT, gevent.kill)
        main(options)