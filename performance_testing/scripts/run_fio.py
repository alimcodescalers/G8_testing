#!/usr/local/bin/jspython
import gevent
import signal
from optparse import OptionParser
import os
from JumpScale import j
import datetime


def fio_test(vm_pubip_pubport, Res_dir,ovc, options):
    iteration=1
    machineId = vm_pubip_pubport.keys()[0]
    cloudspace_publicip = vm_pubip_pubport.values()[0][0]
    cs_publicport = vm_pubip_pubport.values()[0][1]

    machine = ovc.api.cloudapi.machines.get(machineId)
    account = machine['accounts'][0]

    if not j.system.net.waitConnectionTest(cloudspace_publicip, cs_publicport, 20):
        print 'Could not connect to VM over public interface'
    else:
        exc = j.tools.executor.getSSHBased(cloudspace_publicip, port=cs_publicport,
                                           passwd=account['password'], login=account['login'])
        connection = j.tools.cuisine.get(exc)
        j.do.execute('sshpass -p%s scp -o \'StrictHostKeyChecking=no\' -P %s Testsuite/1_fio_vms/Machine_script.py  %s@%s:'
                     %(account['password'], cs_publicport, account['login'], cloudspace_publicip))

        print('FIO testing has been started on machine: %s' %machineId)

        connection.core.run('python Machine_script.py %s %s %s %s %s %s %s %s %s %s %s %s %s'
                            %(options.testrun_time, machineId, account['password'], iteration, options.no_of_disks,
                              options.data_size, options.write_type, options.block_size, options.iodepth,
                              options.direct_io, options.rwmixwrite, options.rate_iops, options.numjobs))

        print('FIO testing has been ended on machine: %s' %machineId)

        j.do.execute('sshpass -p%s scp -r -o \'StrictHostKeyChecking=no \' -P %s  %s@%s:machine%s_iter%s_%s_results %s/'
                     %(account['password'], cs_publicport, account['login'], cloudspace_publicip,
                       machineId, iteration, options.write_type, Res_dir))


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

    vms_list = []
    #list virtual and deployed cloudspaces
    cloudspaces_per_user =  ovc.api.cloudapi.cloudspaces.list()
    for cs in cloudspaces_per_user:
        portforwards = ovc.api.cloudapi.portforwarding.list(cloudspaceId=cs['id'])
        for pi in portforwards:
            vms_list.append({pi['machineId']: [pi['publicIp'], pi['publicPort']]})


    # running fio in parallel
    jobs.extend([gevent.spawn(fio_test, Res_dir, iter_on_vms, ovc, options) for iter_on_vms in vms_list])
    gevent.joinall(jobs)

    #collecting results in csv file
    j.do.execute('cp Testsuite/1_fio_vms/collect_results.py %s' % Res_dir)
    j.do.chdir('%s' % Res_dir)
    j.do.execute('python collect_results.py %s' % Res_dir)


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
    parser.add_option("-n", "--dn", dest="no_of_disks", type="int",
                      default=1, help="Number of data disks per VM")
    parser.add_option("-t", "--IO_type", dest="write_type", type="string",
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
    parser.add_option("-r", "--rdir", dest="Res_dir", type="string",
                      default="/root/G8_testing/tests_results/FIO_test", help="absolute path fot results directory")

    (options, args) = parser.parse_args()
    if not options.username or not options.password or not options.environment:
        parser.print_usage()
    else:
        jobs = list()
        gevent.signal(signal.SIGQUIT, gevent.kill)
        main(options)