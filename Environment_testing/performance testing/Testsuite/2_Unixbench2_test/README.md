# Unixbench 2 test description

## Prerequisite
Have a gener8 run the latest version of openvcloud
Clean the Gener8 so no vm's are running on it.

## Test Case description
- create an account
- create 1 cloudspace for all nodes
- create 1vm running Unixbench
- When the test is done store the unixbench score
- create a second vm in the same cloudspace and run Unixbench with a random time interval on both vm's
- When the test is done store the unixbech score of both vm's
- create a third vm in the same cloudspace and run Unixbench with a random time interval on all vm's
- When the test is done store the unixbech score of all vm's
- Repeat above untill the unixbench score of the first vm is devided by 2

## Expected result
- Create a result table providing the average unixbench score per vm  

|vm name  | CPU's  | Memory | HDD | Iteration 1 | Iteration 2 | ... | iteration x | Avg Unixbench score|

## Running the Test
- For changing the test parameters: vim Testsuite/2_Unixbench2_test/parameters.cfg 
- Go to performance testing directory: cd org_quality/Environment testing/performance testing
- From inside that directory:  jspython Testsuite/2_Unixbench2_test/2_unixbench2.0_test.py 
- After the test has been completed, the test will clean itself.

## Results Sample
- Results can be found in /Unixbench_results/results.table
- This sample is only for 2 iterations
![unixbench](https://cloud.githubusercontent.com/assets/15011431/14142022/b3a054de-f68b-11e5-8996-259aca0fba93.png)

