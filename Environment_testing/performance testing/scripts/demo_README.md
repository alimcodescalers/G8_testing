# Demo scripts
  1- demo_create_vms.py: create all vms on the environment
  2- demo_run_fio.py: runs FIO tests on all vms inn parallel

# This demo is assuming that:
  1- All machines are created on one cloudspace
  2- We are running the test from an ovs node

# Precautions
  1- After creating the vms please make sure that the assigned ip for the machines
     matches the ip on the portal

# To Run the scripts
  1- Make sure you are on the demo branch (git checkout demo)
  2- cd org_quality/Environment_testing/performance\ testing/
  3- jspython scripts/demo_create_vms.py 25 (25= number of vms need to be created)
  4- jspython scripts/demo_run_fio.py 10 (10 = number of vms need to run FIO on .. (bet (1-25))
