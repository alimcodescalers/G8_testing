## Local Setup of the OpenvCloud Functional Tests

For setting up the OpenvCloud functional tests, you have two options:
- Install directly on **ovc\_master**, so locally from the perspective where the tests will actually run
- Install on your local machine, so remotely from the perspective of where the tests will actually run

Here we discuss the first option.

There are three steps:
1. Get access to **ovc\_master**, see the [How to Connect to an OpenvCloud Environment](https://gig.gitbooks.io/ovcdoc_public/content/Sysadmin/Connect/connect.html) documentation in the [OpenvCloud Operator's Guide](https://www.gitbook.com/book/gig/ovcdoc_public/details)
2. Clone the **G8_testing** repository on **ovc\_master** in the directory `/opt/code/github/0-complexity`:
3. Run the `setup_run_tests_local.sh` script with the required pareameters:
  - [test_suite branch] specifies the branch of the test suite to be used
  - [local\_directory] speficies the directory on ovc_master where you want the specified branch be cloned
  - [env_name] specifies the name of the environment
  - [test_path] specifies the actual test to be used, this path is formatted as [full path of the Python script]:[Class of the test suite][test case]

So first, clone the G8_testing repository:
```
cd /opt/code/github/0-complexity
git clone git@github.com:0-complexity/G8_testing.git
```

Then go to the `Openvcloud` directory:
```
cd cd G8_testing/functional_testing/Openvcloud/
```

And finally run the test, for instance:
```
bash setup_run_tests_local.sh master /opt/code/github/0-complexity be-g8-3 ovc_master_hosted/ACL/a_basic_operations/acl_account_test.py:Read.test003_account_get_with_readonly_user
```

This will run the **test003\_account\_get\_with\_readonly\_user()** test case of the **Read()** class that is implemented in the **acl_account_test.py**, located in the directory **ovc\_master\_hosted/ACL/a\_basic\_operations/**.

The result will be fed back in the file `testresults.xml` and all collected log information in the `logs/` directory.

You might want to install and use **tidy** in order to nicely formatted `testresults.xml`:
```
apt-get install tidy
tidy -xml -i testresults.xml > output.xml
cat output.xml
<?xml version="1.0" encoding="utf-8"?>
<testsuite name="nosetests" tests="1" errors="0" failures="0" skip="0">
  <testcase classname="functional_testing.Openvcloud.ovc_master_hosted.ACL.a_basic_operations.acl_account_test.Read" name="test003_account_get_with_readonly_user" time="4.151">
  </testcase>
</testsuite>
```