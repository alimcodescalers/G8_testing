## FIO Performance Testing

### Prerequisites  
- Have a funtional G8 up and running

### FIO settings
When running the test we are writing 3GB of data per disk. This means if we have defined 5 disks we will write 3GB x 5 per iteration. The amount of data to be written is settable in the Perf_parameters.cfg file.


### Running the test script
Prior to running the script we need to make sure that the environment is clean. To clean the environment we need to use the tear down script.

Connect as root to the physical environment, go to the Performance_test script directory. and run the tear_down.py script.

```
cd Performance_test
jspython scripts/tear_down.py --clean
```
Now we need to set up the required parameters.

Run a vim command to change the performance test parameters.
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
Res_dir: /root/org_quality/Environment_testing/tests_results/FIO_test

# username
username: perftestuser

```

When the configfile is set you can run the FIO test script using
```
jspython scripts/setup_test.py
```
When the complete set up is done following actions are performed:  
1. user creation
2. cloudspace is made
3. vm's are created
4. disks are mounted
5. Start of FIO test
6. Test results are posted to the repo

*user information*  
username: perftest  
PW: gig12345

*vm information*  
during the testscript vm's are created following the naming convention  

"nodexy"   
x = the stack where the vm is installed

y = the iteration number  

Each deployed vm also gets his own ID during the set up.  

The more iterations we have selected the more vm's are created per node or stack. This means if you have 3 iterations selected and we use 1 stack in the set up we have the following process:

Iteration 1:
- vm created on stack 1 and FIO test is done.

Iteration 2:
- a new vm is created on stack 1 and FIO tests are now performed on vm1 and vm2

Iteration 3:
- a new vm is created on stack 1 and FIO tests are now performed on vm1, vm2 and vm3.


## Check the test results.
If we want to view the results of the test we need to go to the following file:  
```
cd /perftest/
vim total_results
```
In the test result file we can view the following information
- Total IOPS per vm per Iteration
- Avergage cpu

A more advanced test result is added to the environment repo on the following path:  

$environment_repo/Testreport/Fio_test/YYMMDD_$CPU_nodename_$iterationnumber_of_the_day