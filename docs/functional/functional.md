## Functional Testing

This section describes the tests to be executed in order to validate the basic functionality of a G8 installation.

Functional testing requires that the system was installed properly, as documented in the [OpenvCloud Operator's Guide](https://www.gitbook.com/book/gig/ovcdoc_public/details), more specifically in the section [Installation of an OpenvCloud Environment](https://gig.gitbooks.io/ovcdoc_public/content/Installation/Installation.html).

The functional tests can be categorized into three categories:

- [Hosted on ovc_master](openvcloud/ovc_master_hosted/ovc_master_hosted.md)
- [Hosted on a compute node](openvcloud/compute_node_hosted/compute_node_hosted.md)
- [Hosted on any remote machine](openvcloud/remote_machine_hosted/remote_machine_hosted.md)

Only the Portal tests can be run from both the master node or any remote node, that's why it appears under both categories:

| Section                                        | master node | compute node | remote node |
|:-----------------------------------------------|:-----------:|:------------:|:-----------:|
|[Portal testing](#portal)                       | X           |              | X           |
|[API testing](#api)                             | X           |              |             |
|[Network configuration test](#network-config)   |             | X            |             |
|[Virtual machines limit test](#vm-limit)        |             | X            |             |
|[Cloud Spaces limit test](#cloudspace-limit)    |             | X            |             |
|[VM Live migration test](#vm-migration)         |             | X            |             |
|[Node maintenance test](#node-maintenance)      |             | X            |             |
|[Snapshots limit test](#snapshots-limit)        |             | X            |             |


<a id="portal"></a>
### Portal tests

- End User Portal
- Admin Portal

See [Portal Testing](openvcloud/remote_machine_hosted//portal/portal.md)


<a id="api"></a>
### API tests

- Access Control List (ACL) APIs
- OpenvCloud API, covering all non-ACL APIs

See [API Testing](openvcloud/ovc_master_hosted/API/API.md)


<a id="network-config"></a>
### Network configuration test

See [Network Configuration Test](openvcloud/compute_node_hosted/1_network_config_test/1_network_config_test.md)


<a id="vm-limit"></a>
### Virtual machines limit test

See [Virtual Machines Limit Test](openvcloud/compute_node_hosted/3_Env_Limit_test/3_Env_Limit_test.md)


<a id="cloudspace-limit"></a>
### Cloud spaces limit test

See [Cloud Spaces Limit Test](/openvcloud/compute_node_hosted/5_cloudspace_limits_test/5_cloudspace_limits_test.md)


<a id="vm-migration"></a>
### VM Live migration test

See [VM Live Migration Test](openvcloud/compute_node_hosted/6_vm_live_migration_test/6_vm_live_migration_test.md)


<a id="node-maintenance"></a>
### Node Maintenance Test

See [Node Maintenance Test](openvcloud/compute_node_hosted/8_node_maintenance_test/8_node_maintenance_test.md)


<a id="snapshots-limit"></a>
### Snapshots Limit Test

See [Snapshots Limit Test](openvcloud/compute_node_hosted/9_vm_unlimited_snapshots/9_vm_unlimited snapshots.md)
