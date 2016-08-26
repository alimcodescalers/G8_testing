## Cloud Space Limit Test

> Note: In a public setup the number of created cloud spaces or VDCs are limited to the number of available public IP adresses.

### Prerequisites

- Have a G8 run the latest version of OpenvCloud
- Have admin rights as a user

### Test case description
- Create an account
- Create a cloud space
- Create a virtual machine with minimum specs on the new cloud space
- Create another cloud space
- Create a new virtual machine with minimum specs on the new cloud space
- Repeat above iterations until the system provides a message stating that there are no more resources available to deploy a new cloudspace

### Expected result

A file should be created with all created cloud spaces. The number of created cloud spaces should be equal to the number of free public IP addresses.  

### Running the test
- Go to performance testing directory:  
```
cd G8_testing/Environment_testing/performance_testing
```
- From inside that directory:  
```
jspython Testsuite/5_cloudspace_limits_test/5_cs_limits_test.py
```
- After the test has been completed, the test will clean itself

### Result sample

@todo