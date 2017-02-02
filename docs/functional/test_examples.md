## Test Examples


### While running the test from a remote Locations...

opt/code/2c3e834f-8491-4827-ad78-233267709010/G8_testing/functional_testing/Openvcloud#

```
tailf logs/openvcloud_testsuite.log
```


sudo apt-get install libxml2-utils

<a id="acl-apis"></a>
### Basic ACL API tests

<a id="account-basic"></a>
Running the **Account** basic ACL API tests:

```
bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/a_basic_operations/acl_account_test.py
xmllint --format testresults.xml
```

<a id="cloudspace-basic"></a>
Running the **Cloud Space** basic ACL API tests:

```
bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/a_basic_operations/acl_cloudspace_test.py
xmllint --format testresults.xml
```

<a id="vm-basic"></a>
Running the **Virtual Machines** basic ACL API tests:

```
bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/a_basic_operations/acl_machine_test.py
xmllint --format testresults.xml
```

<a id="acl-basic-all"></a>
Or running **All** basic ACL API tests:

```
bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/a_basic_operations
xmllint --format testresults.xml
```

<a id="acl-extended"></a>
### Extended ACL API tests


<a id="account-extended"></a>
Running the **Account** extended ACL API tests:

```
bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/b_try_operations/acl_account_test.py
xmllint --format testresults.xml
```

<a id="cloudspace-extended"></a>
Running the **Cloud Space** extended ACL API tests:

```
bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/b_try_operations/acl_cloudspace_test.py
xmllint --format testresults.xml
```

<a id="vm-extended"></a>
Running the **Virtual Machines** extended ACL API tests:

```
bash tools/run_tests_remote.sh -c 34022 -b master ma-g8-1 ma-g8-1 ovc_master_hosted/ACL/b_try_operations/acl_machine_test.py
xmllint --format testresults.xml
```
