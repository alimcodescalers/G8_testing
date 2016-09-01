## OpenvCloud Portals Functional Tests

Currently only the **End User Portal** is covered.


### Requirements

- Current tests can only run from Ubuntu desktop, not server
- Make sure Pythin 2.7 us installed:
  ```
  sudo apt-get update
  sudo apt-get install python2.7
  sudo apt-get install python-setuptools python-dev build-essential
  sudo easy_install pip
  ```
- **virtual env** and some other additional packages are required:
  ```
  pip install virtualenv
  virtualenv venv
  source venv/bin/activate
  git clone https://github.com/0-complexity/G8_testing.git
  cd G8_testing/functional_testing/Openvcloud/ovc_master_hosted/Portal
  pip install -r requirements.txt
  ```
- Supported browsers for Ubuntu:
  - Chrome
  - Firefox <= 46.0

### Running the tests

Change the necessary parameters in config.ini according to your environment:
```
(venv)portal_quality_testsuite$> nosetests -v testsuite_name --tc-file=config.ini  2>testresults.log
* currently we have two testsuites [end_user & admin_portal]
* Ex.: [nosetests -v end_user --tc-file=config.ini  2>testresults.log]
```

Or overwrite it using the following command
```
(venv)portal_quality_testsuite$> nosetests -v testsuite --tc-file=config.ini --tc=main.url:http://be-conv-2.demo.greenitglobe.com/  --tc=main.admin:gig 2>testresults.log
```