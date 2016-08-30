## FIO Test

### Prerequisites
- Have a G8 running the latest version of OpenvCloud
- Clean the G8, so no virtual machines are running on it
- Have admin access to one of the physical compute nodes

### FIO settings
When running the test we are writing 3 GB of data per disk. This means if we have defined 5 disks we will write 5 x 3 GB iteration. The amount of data to be written is settable in the `Perf_parameters.cfg` file.

### Running the test
Prior to running the script we need to make sure that the environment is clean. To clean the environment we need to use the `tear_down.py` script:
```
cd G8_testing/Environment_testing/performance_testing
jspython scripts/tear_down.py --clean
```

Now we need to set up the required parameters:
```
vim Perf_parameters.cfg
```

Following paramenters are settable in the config file:
```
# Number of Iterations --> each iteration create one VM per cpunode(stack)
iterations: 1

# No of cloudspaces --> an account is created for each cloudspace and Number of cloudspaces should be
#less than or equal that of cpu nodes
No_of_cloudspaces: 1

# Number of cpu nodes which will be used for the test (must be less than environment_cpu_nodes-1 )
used_stacks: 2

no_of_vms_per_stack_per_iteration: 3

# Parameters required for VM
# RAM and cpu are coupled together,
# please choose between these values [RAM, vcpu] = [512,1] or [1024,1] or [4096,2] or [2048,2] or [8192,4] or [16384,8]
# RAM specifications
memory: 2048
#vcpu cores
cpu: 2

#Boot Disk size (in GB), please choose between these values [10, 20, 50, 100, 250, 500, 1000, 2000] -- default = 100G
Bdisksize: 100

# Number of data disks per VM
no_of_disks: 1

# Data disksize per vm
data_disksize: 60

# Parameters required for FIO
# Block size
bs:4k
#IO depth:is the number of I/O units to keep in flight against the file.
iodepth: 1
#Direct IO: If direct_io = 1, use non-buffered I/O. Default:0
direct_io:0
#rwmixwrite: is the Percentage of a mixed workload that should be writes. If rwmixwrite = 70
#then rwmixread will be equal 30 by default
rwmixwrite:50

# FIO starting time difference between virtual machines (in seconds)
vms_time_diff: 1

# Test-rum time per virtual machine  (in seconds)
testrun_time: 300

# Amount of data to be written per each data disk per VM (in MB)
data_size: 4000

# Type of I/O pattern -- what you will enter will be the same for all VMs (enter:
# 'write' for sequential write or 'randwrite' for random write
# 'read' for sequential read or 'randread' for random read
# 'rw' for mixed sequential reads and writes or 'randrw' for mixed random reads and writes
# if you enter nothing then half of the vms will be write and the other half will be randwrite
IO_type: write


# Results Directory : write absolute directory
Res_dir: /root/G8_testing/tests_results/FIO_test

# username
username: perftestuser
```

When the config file is set, there are two steps in order to actually run the test:
1. Create all virtual machines with `demo_create_vms.py`
2. Start the FIO tests on all virtual machines in parallel with `demo_run_fio.py`

So first you create all virtual machines, for instance in order to create 25 virtual machines:
```
cd G8_testing/Environment_testing/performance\ testing/ 
demo_create_vms.py 25
```

> Note: After creating the virtual machines make sure that the assigned IP addresses match the IP addresses you see in the Cloud Broker Portal.

This script will actually do the following:

-  Create a user
  - username: perftest
  - password: gig12345
- Create a cloud space, with a randomly generated name
- Create virtual machines
  - the virtual machines will we spread over the number of nodes you indicated in `Perf_parameters.cfg`
  - name in formatted like "nodex_y", where x = the node/stack where the VM is installed and y the number of the virtual machine
- Moint the disks

Next start the test using `demo_run_fio.py`, here with the parameter 10 to indicate that you want to use 10 virtual machines (needs to be between 1 and 25):
```
jspython scripts/demo_run_fio.py 10 (10 = number of vms need to run FIO on .. (bet (1-25))  
```

### Check the test results
If we want to check the results of the test we need to check the following file:
```
cd /G8_testing/tests_results/FIO_test/(date)_(cpu_name).(env_name)_testresults(run_number)/
vim (date)_(cpu_name).(env_name)_testresults(run_number).csv
```

In the test result file we can view the following information:
- Total IOPS per virtual machine per iteration
- Avergage CPU usage