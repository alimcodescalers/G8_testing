## Node Maintenance Test

### Test case description

- Create an account
- Create a cloud space
- Create a virtual machine on a node x (type of virtual machine needs to be selectable in the test parameters) --> do a random read write action of files on that virtual machine
- During the read/write action go to the Cloud Broker Portal
- Select stacks
- Select one of the CPU node x
- Choose Action: **Put in Maintenance** (with option move VMs)

### Expected result
- All virtual machines on that node should be installed on another CPU node
- Virtual machine should not have experienced any downtime
- Virtual machine should not have data loss

### Run the test
- Connect to one of the cpun odes of the environment
```
git clone git@github.com:gig-projects/org_quality.git
```
- Go to performance testing directory:
```
cd org_quality/Environment_testing/performance\ testing/
```
- From inside that directory:
```
jspython Testsuite/8_node_maintenance_test/8_node_maintenance_test.py
```
- After the test has been completed, the test will clean itself