# Standard Unixbech test
## Prerequisite
Have a gener8 run the latest version of openvcloud
Clean the Gener8 so no vm's are running on it.

## Test Case description
- create an account
- create 2 cloudspaces per node
- create 7 vm's per cloudspace (4GB RAM, 2 Core) so 14 vm's per node
- install unixbench on 2 vm's per cloudspace (4x Unixbench per node)
- Start unixbench with a random time interval on all vm's using all available cores
- Run this Unixbench test in loop per vm for a variable amount of iterations --> Run unixbench --> Finish, store result --> Run unixbench --> Finish, store result --> Run unixbench --> Finish, store result ...

## Expected result
- Create a result table providing the average unixbench score per vm  

|vm name  | CPU's  | Memory | HDD | Iteration 1 | Iteration 2 | ... | iteration x | Avg Unixbench score|

- Result needs to be compared to other similar vm scores in the market
http://serverbear.com/benchmarks/cloud

## Running the Test
- Go to performance testing directory: cd G8_testing/Environment testing/performance testing
- From inside that directory:  jspython  Testsuite/4_Unixbench_test/4_Unixbench_test.py 
- After the test has been completed, the test will clean itself.

## Result Sample
- Results can be found in /Unixbench1_resultss/results.table
- Test output (for 2 iterations)  
![4unixbench](https://cloud.githubusercontent.com/assets/15011431/14319591/6de39fe8-fc1a-11e5-8f7e-aa41378273ce.png)
