## VM Unlimited Snapshots Test

### Test description:

 - Create a vm in a cloudspace 
–> vm name: unlimited_snapshotvm
–> Package, 512 MB
–> disk size = from 10 GB
–> create disk 10GB
–> Make directory snapshots on the new vm
–> create a text file called "snapshot"

- Different places to perform the snapshot test:  

1. In actions menu
–> Take snapshot called "snapshot x"  

2. add a new text file in the snapshot directory called snapshot x  

3. go to snapshots menu  
–> Take snapshot x+1  

4. add a new text file in the snapshot directory called snapshot x+1  

5. repeat above steps depending on the variable chosen  

6. stop machine  

7. revert to the latest snapshot -1  

8. start machine  

### Expected behavior

Data of the latest snapshot -1 should be on the vm
all later snapshots than the one selected should be removed from the portal...

### Running the Test

- Go to performance testing directory: 
```
cd G8_testing/Environment_testing/performance_testing
```
- From inside that directory:  
```
jspython Testsuite/9_vm_unlimited_snapshots/9_vm_snapshots_test.py **6**
```
-  '**6**' is the number of snapshots to be created
- Any number of snapshots can be provided to figure out the max number of snapshots that can be created for VM.
- After the test has been completed, the test will clean itself.
