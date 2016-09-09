## Auto-documentation with Sphinx

For following tests auto-documentation generated with **Sphinx** is available:
- [OpenvCloud API Functional Tests](ovc_master_hosted/API/API.md)
- [OpenvCloud Portal Functional Testing](remote_machine_hosted//portal/portal.md)

Click [here](http://85.255.197.106:8888/) to see an online version.

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