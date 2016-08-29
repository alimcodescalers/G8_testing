## Environment Testing

This directory contains all tests that require physical access to the physical compute nodes.

How to get access to a physical compute node is documented in the [OpenvCloud Operator's Guide](https://www.gitbook.com/book/gig/ovcdoc_public/details), see the [Connect to an Environement](https://gig.gitbooks.io/ovcdoc_public/content/Sysadmin/Connect/connect.html) section.

Following subdirectories exist:

- [functional_testing](./functional_testing), documented [here](/docs/test_cases/functional/functional.md)
- [installation_testing](./installation_testing), documented [here]()
- [performance_testing](./performance_testing), documented [here](/docs/test_cases/performance)
- [tests_results](./tests_results)
- [upgrade_testing](./upgrade_testing)




First we need to get the latest test scripts on the physical machine in the root directory by pulling the G8_testing repo to the node where we want to test
```
git clone git@github.com:0-complexity/G8_testing.git
```

As from now all tests need to be executed from the CPU node where the G8_testing repo is cloned.
