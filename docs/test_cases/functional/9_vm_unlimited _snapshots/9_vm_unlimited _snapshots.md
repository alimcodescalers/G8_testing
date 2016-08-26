## Snapshots Limit Test

### Test case description
- Create a virtual machine in a cloud space 
  - virtual machine name: unlimited_snapshotvm
  - Package: 512 MB
  - Disk size: 10 GB
  - Create disk: 10GB
- Create a new directory "snapshots" on the new virtual machine
- Create a new text file called "snapshot"
- In actions menu: Take snapshot called "snapshot x"
- Add a new text file in the snapshot directory called "snapshot x"
- From to snapshots menu: Take "Snapshot x+1"  
- Add a new text file in the snapshot directory called snapshot x+1
- Repeat above steps depending on the variable chosen
- Stop machine
- Revert to the latest snapshot -1
- Start machine  

### Expected behavior
- Data of the latest snapshot -1 should be on the virtual machine
- All later snapshots than the one selected should be removed from the portal...

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
- Any number of snapshots can be provided to figure out the max number of snapshots that can be created for a virtual machine
- After the test has been completed, the test will clean itself
