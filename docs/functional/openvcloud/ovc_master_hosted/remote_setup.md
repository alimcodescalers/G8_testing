## Remote Setup of the OpenvCloud Functional Tests

For setting up the functional tests, you have two options:
- Install directly on **ovc\_master**, so locally from the perspective of where the tests will run
- Install from your local machine, so remotely from the perspective of where the tests will run

Here we discuss the second option.

There are two steps:
1. Clone the **G8_testing** repository to the remote machine, probably your local machine
2. Run the **run\_tests\_remote.sh** script with the required parameters:
  - [grid_name] specifies the name of the grid
  - [env_name] specifies the name of the environment
  - [test_suite] specifies the test suite to execute, optionally indicating that you only want to run a specific vest case of the test suite, all formatted as:
    - [python\_script\_name]:[class\_name].[test\_case\_name]
  - Use the `-b` option to specify the branch of the test suite

> **Note**: Make sure that your private SSH key is stored in the **.ssh** directory on the remote machine, since the **run\_tests\_remote.sh** script will look for it there, ignoring the private key that has been loaded in the memory of **ssh-agent**. So using the -A option when connecting over SSH to a remote machine where your SSH keys are not in the **.ssh** directory will result in **run\_tests\_remote.sh** not being able to get to access your private SSH key, and not being able to connect to GitHub.

So first, clone the **G8_testing** repository:
```
git clone git@github.com:0-complexity/G8_testing.git
```

Then go to the **Openvcloud** directory:
```
cd G8_testing/functional_testing/Openvcloud/
```

And finally execute the **run_tests_remote.sh** script with the required parameters, for instance:
```
bash tools/run_tests_remote.sh -b master gig be-g8-3 ovc_master_hosted/ACL/a_basic_operations/acl_account_test.py:Read.test003_account_get_with_readonly_user
```

In the above example:
- **Branch**: "master"
- **Grid**: "gig"
- **Environment**: "be-conv-2"
- **Python script**: "ovc_master_hosted/ACL/a_basic_operations/acl_account_test.py"
- **Class**: "Read()"
- **Test case**: "test003\_account\_get\_with\_readonly\_user()"

What actually will happen:
- It will connect to **ovc\_master** where it will clone the **G8_testing** repository
  - As the script will lookup to SSH key from the environment repository, make sure that you have access to it
- It will call the **setup_run_tests_local.sh** which is discussed [here](local_setup.md) passing the test case parameters
- The result will be fed back in the file **testresults.xml** and all collected log information in the **logs** directory