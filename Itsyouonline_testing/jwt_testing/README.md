
## Goal of this repo:
This repo is used to execute our automated tests for the itsyouonline JWT (JSON Web Token) testsuite.

Tests are performed using the descriptions in the Folders

**testsuite**
In this folder we have automated test testsuite for the itsyouonline jwt

# Requirements:

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
pip install -r requirements.txt
```

Run the tests
---------------
change the necessary parameters in config.ini according to your environment
```
(venv)$> nosetests -xv testsuite --tc-file config.ini  2>testresults.log
```

or overwrite it using the following command
```
(venv)$> nosetests -xv testsuite --tc-file config.ini --tc=main.url:https://itsyou.online/  --tc=main.user:alim 2>testresults.log
```