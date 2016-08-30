
# Portal testsuite:
This section of the repo is used to execute our automated tests for the cloud portal.

Tests are performed using the descriptions in the Folders

Following test are currently done on the Portal testsuite:

This is a [link](https://docs.google.com/spreadsheets/d/1VgEoIUxZdCQEglwN2VUe3sDY-Jn-nnrEWWNcGQq7dPU/edit#gid=0) to all available automated test that are done

In the case of the Portal automated test we need to check the Portal tab in the Test_ID doc.

## To Do
Get auto generation test descriptions for the Portal automated tests done

| test ID | Prerequisites | test description | expected results |
|---|---|---|---|

Testresults should be pushed to the environment repo under automated test

**end_user**
In this folder we have automated test for the enduser portal

## Requirements:

Supported browsers for Ubuntu:
-------------------
```
chrome
firefox <= 46.0
```

If you don't have python 2.7 use this commands to install:
-----------------------------------------------------------
```
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python2.7
sudo apt-get install python-setuptools python-dev build-essential
sudo easy_install pip
```

Install Python Packages:
------------------------
Note That: you may use virtual env for this step
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
git clone https://github.com/0-complexity/G8_testing.git
cd G8_testing/Openvcloud/Portal/
pip install -r requirements.txt
```

## Run the tests:
--------------
change the necessary parameters in config.ini according to your environment
```
(venv)portal_quality_testsuite$> nosetests -xv testsuite_name --tc-file config.ini  2>testresults.log
* currently we have two testsuites [end_user & admin_portal]
* Ex.: [nosetests -xv end_user --tc-file config.ini  2>testresults.log]
```

or overwrite it using the following command
```
(venv)portal_quality_testsuite$> nosetests -xv testsuite --tc-file config.ini --tc=main.url:http://be-conv-2.demo.greenitglobe.com/  --tc=main.admin:gig 2>testresults.log
```

Continues Integration:
----------------------

OpenvCloud Testsuite runs continuously on [Jenkins CI](http://ci.codescalers.com/view/Integration%20Testing/)


