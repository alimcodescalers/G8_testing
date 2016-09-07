## Functional Tests Hosted on ovc_master

Three types of automated functional tests are available for OpenvCloud:
- Tests that run on **ovc_master**, discussed here below
- Tests that run on a physical **compute node**, discussed [elsewhere in this guide](../compute_node_hosted/compute_node_hosted.md)
- Tests that can run on any **remote machine**, discussed [elsewhere in this guide](../remote_machine_hosted/remote_machine_hosted.md)

> Remember: **ovc_master** is the virtual machine in the master cloud space where the **Cloud Broker Portal** is running, and all other OpenvCloud portals

Currently all API test suites are designed to be installed (hosted) on and run from **ovc_master**. There are two tests suites for the OpenvCloud API, Access Control List APIs and OpenvCloud APIs, both documented [here](API/API.md).

All API test suites are auto-documented with **Sphinx**, [click here](http://85.255.197.106:8888/) to see an online version.

Do the following to install a local version and keep it up to date:

- Make sure that **pip** and **virtualenv** are installed to your system:

  ```shell
  sudo apt-get install python-pip
  sudo pip install virtualenv
  ```

- Clone the **G8_testing** repository:

  ```
  git clone git@github.com:0-complexity/G8_testing.git
  ```

- Run the build script:

  ```
  bash G8_testing/functional_testing/Openvcloud/tools/build_docs.sh
  ```

- Open the generated **index.html** in your browser of choice:

  ```
  firefox G8_testing/auto_generated_docs/_build/html/index.html
  ```

  ![](sphinx.png)
