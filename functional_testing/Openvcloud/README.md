## Goal
This directory is made to test full functionality of our OVC product

## Execute Automated Testing

### Run OpenvCloud Testsuite on remote environment

**Instructions**

1. Pull the OpenvCloud Testsuite repository:

  ```
  git clone https://github.com/0-complexity/G8_testing.git
  ```

2. Change directory to Openvcloud:

  ```
  $ cd G8_testing/Openvcloud/
  ```

3. Run the `run_tests_remote.sh` script with the required parameters:
  ```
  This remote script can be used to run the test suite from local machine to any remote environment.
      - first it will connect to the master node of the grid or the environment
      - clone the testing repo on this master node
      - then it will call the script `setup_run_tests_local.sh` and lanch the test suite
  ```
  ```
  $ bash tools/run_tests_remote.sh -b testsuite_branch grid_name env_name
  [Ex.: bash tools/run_tests_remote.sh -b master gig be-conv-2 ACL/a_basic_operations/acl_account_test.py:Read.test003_account_get_with_readonly_user]

  $ bash tools/run_tests_remote.sh -h

      This script to run OpenvCloud test suite on remote environment

      Usage: tools/run_tests_remote.sh [options] [environment]

      Options:
           -n    node on the environment
           -b    testsuite branch to run tests from

      Results will be found in *testresults.xml* and collected logs under *logs/*
   ```

### Run OpenvCloud Testsuite on local environment

**Instructions**

1. Pull the OpenvCloud Testsuite repository:

  ```
  git clone https://github.com/0-complexity/G8_testing.git
  ```

2. Change directory to Openvcloud:

  ```
  $ cd G8_testing/Openvcloud/
  ```
3. Run the `setup_run_tests_local.sh` script with the required parameters:
  ```
  This local script can be used to run the test suite on the master node of the environment directly
      - clone the testing repo on this master node
      - then it will call the script `setup_run_tests_local.sh` and lanch the test suite
  ```
  ```
  $ bash tools/setup_run_tests_local.sh testsuite_branch local_directory env_name test_path
  [Ex.: bash tools/setup_run_tests_local.sh master /opt/code/ be-conv-2 ACL/a_basic_operations/acl_account_test.py:Read.test003_account_get_with_readonly_user]

  $ bash tools/run_tests_remote.sh -h

      This script to run OpenvCloud test suite on remote environment

      Usage: tools/run_tests_remote.sh [options] [environment]

      Options:
           -n    node on the environment
           -b    testsuite branch to run tests from

      Results will be found in *testresults.xml* and collected logs under *logs/*
   ```

**Continues Integration**

OpenvCloud Testsuite runs continuously on [Jenkins CI](http://ci.codescalers.com/view/Integration%20Testing/)

**Prerequisites**

* This instruction works for UNIX-Like operating systems
* Make sure that *pip* and *virtualenv* are installed to your system

    ```shell
    $ sudo apt-get install python-pip
    $ sudo pip install virtualenv
    ```

**Instructions on how to update the coverage documentation**

1. Pull the testsuite repository:

  ```
  git clone https://github.com/gig-projects/org_quality.git
  ```

2. Change directory to Openvcloud:

  ```
  $ cd G8_testing/Openvcloud/
  ```

3. Run the build script to generate the documentation locally:

  ```
  $ bash tools/build_docs.sh
  ```

4. Open the documentation using any browser

  ```
  $ firefox docs/_build/html/index.html
  ```
