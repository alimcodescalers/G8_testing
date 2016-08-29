## Node Maintenance Test

### Prerequisites
- Have a G8 running the latest version of OpenvCloud
- Clean the G8, so no virtual machines are running on it
- Have admin access to one of the physical compute nodes

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
- Go to the `functional_testing` directory:
  ```bash
  cd G8_testing/functional_testing
  ```
  
- Run the test:
  ```
  jspython Testsuite/8_node_maintenance_test/8_node_maintenance_test.py
  ```

- After the test has been completed, the test will clean itself