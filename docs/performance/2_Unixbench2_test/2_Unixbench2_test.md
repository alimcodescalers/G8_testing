## UnixBench Test

### Prerequisites
- Have a G8 running the latest version of OpenvCloud
- Clean the G8, so no virtual machines are running on it
- Have admin access to one of the physical compute nodes

### Test case description
- Create an account
- Create a cloud space for all nodes
- Create a virtual machine running UnixBench
- When the test is done store the UnixBench score
- Create a second virtual machine in the same cloud space and run UnixBench with a random time interval on both virtual machines
- When the test is done store the UnixBench score of both virtual machines
- Create a third virtual machine in the same cloud space and run UnixBench with a random time interval on all virtual machines
- When the test is done store the UnixBech score of all virtual machines
- Repeat above until the UnixBench score of the first virtual machines is devided by 2

### Expected result
- Create a result table providing the average UnixBench score per virtual machine  

|vm name  | CPU's  | Memory | HDD | Iteration 1 | Iteration 2 | ... | iteration x | Avg Unixbench score|

### Running the test
- Go to performance testing directory: 
  ```
  cd org_quality/performance_testing
  ```
  
- For changing the test parameters:
  ```
  vim Testsuite/2_Unixbench2_test/parameters.cfg 
  ```
  - Following parameters can be configured:
```  
# Results Directory : write absolute directory
Res_dir: /root/org_quality/Environment_testing/tests_results/2_unixbench2

#Number of VMS to run unixbench on
VMs:2

#Numbers of unixbench_running_times on the created vms
unixbench_run_times:1

# Time difference (in secs) between starting running unixbench on VMs
vms_time_diff: 1

# please choose between these values [RAM, vcpu] = [512,1] or [1024,1] or [4096,2] or [2048,2] or [8192,4] or [16384,8]
# RAM specifications
memory: 8192
#vcpu cores
cpus: 4
#Boot Disk size(in GB), please choose between these values [10, 20, 50, 100, 250, 500, 1000, 2000]
Bdisksize: 100
```
- From inside that directory:
  ```
  jspython Testsuite/2_Unixbench2_test/2_unixbench2.0_test.py 
  ```
- After the test has been completed, the test will clean itself.

### Result sample
- Results can be found in /Unixbench_results/results.table
- This sample is only for 2 iterations:

![unixbench](https://cloud.githubusercontent.com/assets/15011431/14142022/b3a054de-f68b-11e5-8996-259aca0fba93.png)

