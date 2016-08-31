## Functional Tests Hosted on ovc_master

Two types of automated functional tests are available for OpenvCloud:
- Tests that run on **ovc_master**, discussed below
- Tests that run on a physical **compute node**, discussed [here](../compute_node_hosted/compute_node_hosted.md)

> Remember: **ovc_master** is the virtual machine in the master cloud space where the Cloud Broker Portal is running, and all other OpenvCloud portals

Following test suites are available:
- Access Control List API 
- OpenvCloud API
- End User Portal

In order to install them you have two options:
- Install and run them directly on ovc_master, using the `setup_run_tests_local.sh` script, as documented [here](local_setup.md)
- Install and run them from a remote machine, using the `run_tests_remote.sh` script, as documented [here](remote_setup.md)

All test suites are auto-documented with Sphinx. Do the following to access it:

- Make sure that *pip* and *virtualenv* are installed to your system:
  ```shell
  sudo apt-get install python-pip
  sudo pip install virtualenv
  ```
- Pull the G8_test repository:
  ```
  git clone https://github.com/0-complexity/G8_testing.git
  ```
- Run the build script:
  ```
  bash G8_testing/functional_testing/Openvcloud/tools/build_docs.sh
  ```
- Open the generated `index.html` in your browser of choice:
  ```
  firefox G8_testing/auto_generated_docs/_build/html/index.html
  ````
  
  ![](sphinx.png)