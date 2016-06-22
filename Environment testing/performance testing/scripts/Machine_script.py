#!/usr/bin/env/python
import sys
import os
import multiprocessing


def FIO_test(disk, testrun_time, machineId, account_pass, iteration, datasize_process, write_type,rwmixwrite, bs, iodepth, direct_io):
    os.system('echo %s | sudo -S fio --bs=%s --iodepth=%s --direct=%s --ioengine=libaio  --gtod_reduce=1 --name=test_iter%s_%s --size=%sM --readwrite=%s --rwmixread=%s'
              ' --numjobs=3 --group_reporting --directory=/mnt/%s --runtime=%s --output=machine%s_iter%s_%s_results/result%s_iter%s_%s.txt'
              %(account_pass, bs, iodepth, direct_io, iteration, disk, datasize_process, write_type, rwmixwrite ,disk, testrun_time, machineId,iteration, write_type, machineId, iteration, disk))


if __name__ == "__main__":
    testrun_time = sys.argv[1]
    machineId = sys.argv[2]
    account_pass = sys.argv[3]
    iteration = sys.argv[4]
    no_of_disks = int(sys.argv[5])
    data_size = int(sys.argv[6])
    write_type = sys.argv[7]
    datasize_process = data_size/3
    bs=sys.arg[8]
    iodepth=sys.arg[9]
    direct_io=sys.arg[10]
    rwmixwrite=sys.arg[11]

    disk_list = ['disk_b', 'disk_c', 'disk_d', 'disk_e', 'disk_f', 'disk_g', 'disk_h', 'disk_i', 'disk_j', 'disk_k']
    os.system('mkdir machine%s_iter%s_%s_results' % (machineId, iteration, write_type))
    processes = []
    for iter_on_disks in range(no_of_disks):
        p = multiprocessing.Process(target=FIO_test, args=(disk_list[iter_on_disks], testrun_time, machineId,
                                                           account_pass, iteration, datasize_process, write_type,
                                                           rwmixwrite, bs, iodepth, direct_io))
        processes.append(p)
    for j in range(no_of_disks):
        processes[j].start()
        print('FIO testing has been started on machine: %s and on disk: %s'% (machineId, disk_list[j]))
    while (any(p.is_alive()==True for p in processes)):
        os.system('sar -r 1 1 >> machine%s_iter%s_%s_results/memory_usage.txt' %(machineId, iteration, write_type))
        os.system('mpstat -P ALL >> machine%s_iter%s_%s_results/cpuload.txt' %(machineId, iteration, write_type))
    for k in range(no_of_disks):
        processes[k].join()
        print('FIO testing has been ended on machine: %s and on disk: %s'% (machineId, disk_list[k]))
