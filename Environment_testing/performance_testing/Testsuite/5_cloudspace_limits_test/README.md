# Cloudspace limitation test

note: In a public setup the number of created cloudspaces or VDC's are limited to the number of available public IP adresses.

## Prerequisite

Have a gener8 run the latest version of openvcloud.
Have admin rights as a user

## Test Scenario

create an account
create a clouspace
create a vm with minimum specs on the cloudspace made
create another cloudspace
create a new vm with minimum specs on the new cloudspace made

repeat above iterations untill the system provides a message stating that there are no more recourses available to deploy a new cloudspace.

## Expected result

a file should be created with all cloudspaces made. The number of created cloudspaces should be equal to the number of free public IP addresses.  

## Running the Test

Go to performance testing directory:  
```
cd G8_testing/Environment testing/performance testing
```

From inside that directory:  
```
jspython Testsuite/5_cloudspace_limits_test/5_cs_limits_test.py
```
After the test has been completed, the test will clean itself.
