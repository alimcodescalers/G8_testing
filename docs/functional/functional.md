## Functional Testing

This section describes the tests to be executed in order validate the basic functionality of a G8 installation. It lists the tests and expected test results.

Functional testing requires that the system was installed properly, as documented in the [OpenvCloud Operator's Guide](https://www.gitbook.com/book/gig/ovcdoc_public/details), more specifically in the section [Installation of an OpenvCloud Environment](https://gig.gitbooks.io/ovcdoc_public/content/Installation/Installation.html).


### Automated testing with Jenkins

- ACL
- OVC
- Portal


#### Other functional tests

Following tests require access to the physical compute nodes:

* [Network Configuration Test](1_network_config_test/1_network_config_test.md)
* [Virtual Machines Limit Test](3_Env_Limit_test/3_Env_Limit_test.md)
* [Cloud Spaces Limit Test](5_cloudspace_limits_test/5_cloudspace_limits_test.md)
* [VM Live Migration Test](6_vm_live_migration_test/6_vm_live_migration_test.md)
* [Node Maintenance Test](8_node_maintenance_test/8_node_maintenance_test.md)
* [Snapshots Limit Test](9_vm_unlimited _snapshots/9_vm_unlimited _snapshots.md)

How to get access to a physical compute node is documented in the [OpenvCloud Operator's Guide](https://www.gitbook.com/book/gig/ovcdoc_public/details), see the [Connect to an Environement](https://gig.gitbooks.io/ovcdoc_public/content/Sysadmin/Connect/connect.html) section for all details.