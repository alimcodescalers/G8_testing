## VM Live Migration Test

### Prerequisites
- Have a G8 run the latest version of OpenvCloud
- Have admin access to one of the physical compute nodes

### Test case description
- Create an account
- Create a cloud space
- Create a virtual machine (type of virtual machine need to be selectable in the test parameters)
- Do a random read write action of files on that virtual machine
- During the read/write action go to the **Cloud Broker Portal**, and got to the **Virtual Machines** page
- Choose action: **Move to another CPU node**
  - Select new CPU node
  - Set force option to "no"

### Expected result
- Virtual machine should be installed on another CPU node
- Virtual machine should not have experienced any downtime
- Virtual machine should not have data loss  

When above is OK then the test is PASS
When one of the above actions failed then it's a FAIL

### Running the test
- Go to the `functional_testing/Openvcloud/compute_node_hosted/6_vm_live_migration_test/` directory:
  ```bash
  cd functional_testing/Openvcloud/compute_node_hosted/6_vm_live_migration_test/
  ```

- Run the rest:  
  ```
  jspython 6_vm_live_migration_test.py 
  ```

- After the test has been completed, the test will clean itself.

### Result sample

![livem](https://cloud.githubusercontent.com/assets/15011431/16177906/76a13782-3642-11e6-9986-209a8c807f5d.png)
