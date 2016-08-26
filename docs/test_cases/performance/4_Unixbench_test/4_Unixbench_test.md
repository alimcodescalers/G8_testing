## Standard Unixbech Test

### Prerequisites
- Have a G8 run the latest version of OpenvCloud
- Clean the G8 so no virtual machines are running on it

### Test case description
- Create an account
- Create 2 cloud spaces per node
- Create 7 virtual machines per cloud space (4GB RAM, 2 Core), so 14 virtual machines per node
- Install Unixbench on 2 virtual nachines per cloud space (4x UnixBench per node)
- Start UnixBench with a random time interval on all virtual machines using all available cores
- Run this UnixBench test in loop per virtual machine for a variable amount of iterations --> Run unixbench --> Finish, store result --> Run UnixBench --> Finish, store result --> Run unixbench --> Finish, store result ...

### Expected result
- Create a result table providing the average unixbench score per virtual machine:

|vm name  | CPU's  | Memory | HDD | Iteration 1 | Iteration 2 | ... | iteration x | Avg Unixbench score|

- Result needs to be compared to other similar vm scores in the market
http://serverbear.com/benchmarks/cloud

### Running the test
- Go to performance testing directory: 
```
cd G8_testing/Environment_testing/performance_testing
```
- From inside that directory:
```
jspython Testsuite/4_Unixbench_test/4_Unixbench_test.py 
```
- After the test has been completed, the test will clean itself.

### Result sample
- Results can be found in `/Unixbench1_resultss/results.table`
- Test output (for 2 iterations):
![4unixbench](https://cloud.githubusercontent.com/assets/15011431/14319591/6de39fe8-fc1a-11e5-8f7e-aa41378273ce.png)
