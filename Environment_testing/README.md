# Goal
This repo will be used for testing following items
- Installation test --> Auto Installation testing should be added in this repo
- Performance testing --> All testing that result in Performance of an environment should be added into this repo
- Upgrade testing --> Automated upgrade script tests should be added into this repo


## Openvcloud Quality Performance Test   
The repo contains all test scripts used for testing our Gener8 

When performance test are ran on an environment the result is pushed to the environment it selve in the following folder on the repo:  
$Environment_reponame/Environment_testing/test_results/$name_of_the_performance_test_executed/

## Prerequisites

# General Set up of the Gener8 prior to start testing  

To start the performance test we should connect to one of the physical nodes of the environment that needs to be tested. To connect to a physical node, follow the steps as described in the [connect documentation](https://gig.gitbooks.io/ovcdoc_public/content/Sysadmin/Connect/connect.html).

When connecting to a physical node the node will not be used during the stress test. e.g. When you connect to node 1, tests will run on node 2 and other available nodes. (we can run the tests from any node)

First we need to get the test scripts on the physical machine on the root directory by pulling the G8_testing repo to the node where we want to test
```
git clone git@github.com:0-complexity/G8_testing.git
```
