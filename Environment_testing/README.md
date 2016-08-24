# Goal
This repo will be used for testing our Gener8
- Installation test --> Auto Installation testing should be added in this repo
- Performance testing --> All testing that result in providing Performance information of an environment
- Upgrade testing --> Automated upgrade script tests should be added into this repo
- Automated tests --> Automated test currently performed through Jenkins. In the near furure all test will run using AYS & Cockpit.


## usefull info

To start the performance test we should connect to one of the physical nodes of the environment that needs to be tested. To connect to a physical node, follow the steps as described in the [connect documentation](https://gig.gitbooks.io/ovcdoc_public/content/Sysadmin/Connect/connect.html).


First we need to get the latest test scripts on the physical machine in the root directory by pulling the G8_testing repo to the node where we want to test
```
git clone git@github.com:0-complexity/G8_testing.git
```

As from now all tests need to be executed from the CPU node where the G8_testing repo is cloned.
