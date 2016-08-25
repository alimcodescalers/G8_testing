## Virtual Machines Performance Test

All required files to setup and run the virtual mmachines performance test are available in the [0-complexity/G8_testing](https://github.com/0-complexity/G8_testing) GitHub repository.

In order to setup the virtual machines performance test you need to connect to one of the physical compute nodes of the G8 environment that needs to be tested. To connect to a physical compute node, follow the steps as described in the [How to Connect to an OpenvCloud Environment](https://gig.gitbooks.io/ovcdoc_public/content/Sysadmin/Connect/connect.html) documentation.

The physical compute node used for the performance test will not be tested during the performance test. So when using node 1, tests will run on node 2 and other available nodes.

Once connected to the compute node where you want to setup the performance test, you need to clone the [0-complexity/G8_testing](https://github.com/0-complexity/G8_testing) GitHub repository:
```
git clone https://github.com/0-complexity/G8_testing.git
```

All performance test files are in the `Environment_testing\performance_testing` directory:
- With the `Perf_parameters.cfg` file you set the performance test parameters, details below
- The `scripts` directory contains the actual scripts
  - `collect_results.py` collects all the results of the virtual machines
  - `Machine_script.py` is the actual script that runs on each virtual machine
  - `setup_test.py` sets up the test environment and executes the test script
  - `tear_down.py` tears down the environment, meaning deleting everything you created including user, accounts, cloudspaces and VMs.


### Running the test script

Prior to running the script we need to make sure that the environment is clean. To clean the environment we need to use the tear down script.

Connect as root to the physical environment, go to the `Environment_testing/performance_testing/scripts` directory and run the `tear_down.py` script:

```
cd Performance_test
jspython scripts/tear_down.py --clean
```

Note: the `--clean` option will delete all users except gig and admin users and will remove all accounts except the test_storage account which is responsible for checking environment health periodically

Now you need to set up the required parameters. To change the performance test parameters we need to run a vim command.

```
vim Perf_parameters.cfg
```

Following paramenters are available in the file:
```
[perf_parameters]

# Number of Iterations --> each iteration creates one VM per CPU node (stack)
iterations: 1

# Number of cloud spaces --> an account is created for each cloudspace and Number of cloudspaces should be less than or equal that of cpu nodes
No_of_cloudspaces: 2

# Number of CPU nodes which will be used for the test (must be less than environment_cpu_nodes-1 )
used_stacks: 3

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
no_of_disks: 5

# Data disksize per vm
data_disksize: 30

# Parameters required for FIO
# FIO starting time difference between virtual machines (in seconds)
vms_time_diff: 10

# Test-rum time per virtual machine  (in seconds)
testrun_time: 300

# Amount of data to be written per each data disk per VM (in MB)
data_size: 3000

# Type of I/O pattern -- what you will enter will be the same for all VMs (enter:
# 'write' for sequential write or 'randwrite' for random write
# 'read' for sequential read or 'randread' for random read
# 'rw' for mixed sequential reads and writes or 'randrw' for mixed random reads and writes
# if you enter nothing then half of the vms will be write and the other half will be randwrite
IO_type: write

# Results Directory : write absolute directory
Res_dir: /perftest

# username
username: perftestuser

# should run all scripts from inside the repo
```

Now from inside the repositorie run the test script:
```
jspython scripts/setup_test.py
```

Note: after running the `setup_test.py` and investigating the environment (if needed), please make sure to tear down the environment

When `setup_test.py` is completed, a user is created, a cloud space is made, vms are created, disks are mounted and FIO testing is done.

*User information*
username: perftestuser (can be changed in the Perf_parameters.cfg)
PW: gig12345

*Cloud space information*
For each cloudspace, an account is created
Name of the deployed cloud space = default

*VM information*  
During the test script vms are created following the naming convention  

"nodexy"   
x = the stack where the vm is installed

y = the iteration number  

Each deployed vm also gets his own ID during the set up.  

The more iterations we have selected the more vm's are created per node or stack. This means if you have 3 iterations selected and we use 1 stack in the set up we have the following process:

Iteration 1:
- A vm created on stack 1 and FIO test is done, let's call it vm1.

Iteration 2:
- A new vm is created on stack 1 and FIO tests are now performed on vm1 and vm2

Iteration 3:
- A new vm is created on stack 1 and FIO tests are now performed on vm1, vm2 and vm3.


### Check the test results

If we want to check the results of the test we need to open `total_results`:  
```
cd /perftest/
vim total_results
```

In the `total_results` file results are shown per VM and per iteration:
- total IOPS
- Avg_cpuload
- test runtime: time taken to run the test

Also you can find the sum up of all these informations printed in a pretty table, in a file called `total_results.table`.

Concerning the VMs creation time (the time from creating a VM till it gets an IP address and we have SSH access), the results for all VMs can be found in a file called `VMs_creation_time.txt`:
```
cd /perftest/
VMs_creation_time.txt
```