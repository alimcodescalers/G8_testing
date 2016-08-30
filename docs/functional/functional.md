## Functional Testing

This section describes the tests to be executed in order validate the basic functionality of a G8 installation. It lists the tests and expected test results.

Functional testing requires that the system was installed properly, as documented in the [OpenvCloud Operator's Guide](https://www.gitbook.com/book/gig/ovcdoc_public/details), more specifically in the section [Installation of an OpenvCloud Environment](https://gig.gitbooks.io/ovcdoc_public/content/Installation/Installation.html).

Two types of automated functional tests are available:
- Tests that run on ovc_master, that is the virtual machine in the master cloud space where Cloud Broker Portal is running, and all other OpenvCloud portals
- Tests that run on a physical compute node 

### Functional tests hosted on ovc_master

Following test suites are available:
- Access Control List API 
- OpenvCloud API
- End User Portal

All test suites are auto-documented with Sphinx. In order to access the documentation, you need to do the following:
- Pull the G8_test repository:
  ```
  git clone https://github.com/0-complexity/G8_testing.git
  ```
- Run the build script:
  ```
  bash G8_testing/Openvcloud/tools/build_docs.sh
  ```
- Open the generated `index.html` in your browser of choice:
  ```
  firefox /auto_generated_docs/_build/html/index.html
  ````

![](documentation.png)


In order to install them you have two options:
- Install and run them directly on the master cloud spaces, using the `setup_run_tests_local.sh` script, as documented [here](local_setup.md)
- Install and run them from a remote machine, using the `run_tests_remote.sh` script, as documented [here](remote_setup.md)


### Functional tests hosted on a compute node

The differences with these tests is that they have been designed to run on a physical compute node.

Following tests require access to the physical compute nodes:

* [Network Configuration Test](1_network_config_test/1_network_config_test.md)
* [Virtual Machines Limit Test](3_Env_Limit_test/3_Env_Limit_test.md)
* [Cloud Spaces Limit Test](5_cloudspace_limits_test/5_cloudspace_limits_test.md)
* [VM Live Migration Test](6_vm_live_migration_test/6_vm_live_migration_test.md)
* [Node Maintenance Test](8_node_maintenance_test/8_node_maintenance_test.md)
* [Snapshots Limit Test](9_vm_unlimited _snapshots/9_vm_unlimited _snapshots.md)

How to get access to a physical compute node is documented in the [OpenvCloud Operator's Guide](https://www.gitbook.com/book/gig/ovcdoc_public/details), see the [Connect to an Environement](https://gig.gitbooks.io/ovcdoc_public/content/Sysadmin/Connect/connect.html) section for all details.