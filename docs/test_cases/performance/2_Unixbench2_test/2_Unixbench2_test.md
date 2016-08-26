
## UnixBench 2 Test

### Prerequisites
- Have a G8 running the latest version of OpenvCloud
- Clean the G8 so no vm's are running on it

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
- For changing the test parameters:
  ```
  vim Testsuite/2_Unixbench2_test/parameters.cfg 
  ```
- Go to performance testing directory: 
  ```
  cd org_quality/Environment_testing/performance_testing
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

