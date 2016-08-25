## VM Live Migration Test

### Prerequisite
Have a gener8 run the latest version of openvcloud.
Have admin rights as a user

### Test Case description
- create an account
- create a cloudspace
- create a vm (type of vm's need to be selectable in the test parameters)
- do a random read write action of files on that vm.
- during the read/write action go to the cloudbroker portal
- select Virtual Machines
- Choose Action: Move to another CPU node
--> Select new CPU node
--> force option "no"

### Expected result
- vm should be installed on another CPU node
- vm should not have experienced any downtime
- vm should not have data loss  

When above is ok then the test is PASS
When one of the above actions fail then its a FAIL


### Running the Test
- Go to performance testing directory: 
```
cd G8_testing/Environment_testing/performance_testing
```

- From inside that directory:  
```
jspython Testsuite/6_vm_live_migration_test/6_vm_live_migration_test.py 
```
- After the test has been completed, the test will clean itself.

### Result Sample
![livem](https://cloud.githubusercontent.com/assets/15011431/16177906/76a13782-3642-11e6-9986-209a8c807f5d.png)
