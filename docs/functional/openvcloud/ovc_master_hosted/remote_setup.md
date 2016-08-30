## Remote Setup of the OpenvCloud Functional Tests

For setting up the functional tests, you have two options:
- Install everything directly on the master cloud space, so locally from the perspecitive where the tests will actually run
- Install everything on your local machine, so remotely from the perspective of where the tests will actually run

Here we discuss the second option.

There are two simple steps:
- Clone the G8_testing repository to the remote machine, which will most probably actually be your local machine
- Run the `run_tests_remote.sh` script with the required parameters:
  - [grid_name] specifies the name of the grid
  - [env_name] specifies the name of the environment
  - [test_suite] specifies the test suite to execute, optionally indicating that you only want to run a specific vest case of the test suite, all formatted as:
    - [python\_script\_name]:[class\_name].[test\_case\_name]
  - Use the `-b` option to specify the test suite branch
  - Use the `-n` option to specify the environment


So first we clone the G8_testing repository:
```
git clone https://github.com/0-complexity/G8_testing.git
```

And then we execute the `run_tests_remote.sh` script, for instance:
```
bash tools/run_tests_remote.sh -b master gig be-conv-2 ACL/a_basic_operations/acl_account_test.py:Read.test003_account_get_with_readonly_user
```

In the above example:
- **Branch**: "master"
- **Grid**: "gig"
- **Environment**: "be-conv-2""
- **Python script**: "ACL/a_basic_operations/acl_account_test.py"
- **Class**: "Read"
- **Test case**: "test003_account_get_with_readonly_user"

What actually will happen:
- It will connect to the master cloud space where it will clone the G8_testing repository
  - As the script will lookup to SSH key from the environment repository, make sure that you have access to it
- It will call the `setup_run_tests_local.sh` which is discussed [here](local_setup.md) passing the test case parameters
- The result will be fed back in the file `testresults.xml` and all collected log information in the `logs/` directory