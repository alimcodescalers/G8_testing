## Node Maintenance Test

### Test Case description

- create an account
- create a cloudspace
- create a vm on a node x (type of vm's need to be selectable in the test parameters) --> do a random read write action of files on that vm.
- during the read/write action go to the cloudbroker portal
- select stacks
- select one of the CPU node x
- Choose Action: Put in Maintenance (with option move VMs)

### Expected result

- all vm's on that node should be installed on another CPU node
- vm should not have experienced any downtime
- vm should not have data loss

### Steps to run the script
- connect to one of the cpunodes of the environment
- git clone git@github.com:gig-projects/org_quality.git
- Go to performance testing directory: cd org_quality/Environment_testing/performance\ testing/
- From inside that directory: jspython Testsuite/8_node_maintenance_test/8_node_maintenance_test.py
- After the test has been completed, the test will clean itself.