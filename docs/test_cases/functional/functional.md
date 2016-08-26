## Functional Testing

This section describes the tests to be executed to validate the basic functionality of the G8 Solution. It lists the tests and expected test results.

### Clean installation of a full system

First test case is to do a clean installation.  This can be done through the instructions provided here:
https://gig.gitbooks.io/ovcdoc_public/content/Installation/Installation.html

| Input  | Tests Executed  | Expected Output  |
|---|---|---|
| System racked / stacked for clean install with the right IP configurations for each of the nodes done | Clean install as described in https://gig.gitbooks.io/ovcdoc_public/content/Installation/Installation.html
| Functioning system that is ready for Automated Test run  |   


### Automated testing
Once installed - the first task is to executed the automated testing of the basic functionality of OpenvCloud, the G8 Cockpit and Itsyou.Online.


#### Automated testing for OpenvCloud

* [Network Configuration Test](1_network_config_test/1_network_config_test.md)
* [Virtual Machines Limit Test](3_Env_Limit_test/3_Env_Limit_test.md)
* [Cloud Spaces Limit Test](5_cloudspace_limits_test/5_cloudspace_limits_test.md)
* [VM Live Migration Test](6_vm_live_migration_test/6_vm_live_migration_test.md)
* [Node Maintenance Test](8_node_maintenance_test/8_node_maintenance_test.md)
* [Snapshots Limit Test](9_vm_unlimited _snapshots/9_vm_unlimited _snapshots.md)

#### Automated testing for G8 Cockpit
@TODO


#### Automated testing for Itsyou.Online
@TODO


### Manual testing
@TODO