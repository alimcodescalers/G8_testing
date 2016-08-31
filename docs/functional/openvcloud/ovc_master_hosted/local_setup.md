## Local Setup of the OpenvCloud Functional Tests

For setting up the OpenvCloud functional tests, you have two options:
- Install everything directly on the master cloud space, so locally from the perspecitive where the tests will actually run
- Install everything on your local machine, so remotely from the perspective of where the tests will actually run

Here we discuss the first option.

There are three simple steps:
1. Clone the G8_testing repository to the environment master node (ovc_master):

  ```
  git clone git@github.com:0-complexity/G8_testing.git
  ```

2. Change directory to Openvcloud:

  ```
  $ cd G8_testing/functional_testing/Openvcloud/
  ```
3. Run the `setup_run_tests_local.sh` script with the required parameters:

  ```
  $ bash tools/setup_run_tests_local.sh testsuite_branch local_directory env_name test_path
  ```
  ```
  [Ex.: bash tools/setup_run_tests_local.sh master /opt/code/ be-conv-2 ovc_master_hosted/ACL/a_basic_operations/acl_account_test.py:Read.test003_account_get_with_readonly_user]
  ```
