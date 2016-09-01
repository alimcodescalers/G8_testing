## UnixBench Test

### Prerequisites
- Have a G8 running the latest version of OpenvCloud
- Clean the G8, so no virtual machines are running on it
- Have admin access to one of the physical compute nodes

### Test case description
- Create an account
- Create a cloud space for all nodes
- Create the number of vms you want to run unixbench on
- Install unixbench on the created virtual machines then run unixbench on them
- Run unixbench on the first VM only and store its score
- Run unixbench on all VMs , then store all VMs unixbench scores


### Expected result
- Create a result table providing the average UnixBench score per virtual machine  

|vm name  | CPU's  | Memory | HDD | Iteration 1 | Iteration 2 | ... | iteration x | Avg Unixbench score|

### Running the test
- Go to performance testing directory: 
  ```
  cd /root/G8_testing/performance_testing
  ```
  
- For changing the test parameters:
  ```
  vim Testsuite/2_Unixbench2_test/parameters.cfg 
  ```
- Following parameters can be configured:
```  
# Results Directory: write absolute directory
Res_dir: /root/G8_testing/tests_results/2_unixbench2

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
- Results can be found in /G8_testing/tests_results/Unixbench_results/(date)_(cpu_name).(env_name)_testresults(run_number)/
vim (date)_(cpu_name).(env_name)_testresults(run_number).csv


![unixbench](https://cloud.githubusercontent.com/assets/15011431/14142022/b3a054de-f68b-11e5-8996-259aca0fba93.png)

