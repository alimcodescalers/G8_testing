
## Goal of this repo:
This repo is used to execute our automated tests for the itsyouonline api testsuite.

Tests are performed using the descriptions in the Folders

**testsuite**
In this folder we have automated test testsuite for the itsyouonline api

** Installation **
Steps to install itsyouonline locally:  
1. sudo apt-get update  
2. sudo apt-get -y upgrade  
3. sudo apt-get install docker.io  
4. sudo usermod -G docker -a cloudscalers  
5. sudo docker run -it -p 27017:27017 -name=mongo mongo  
6. sudo curl -O https://storage.googleapis.com/golang/go1.6.linux-amd64.tar.gz  
7. sudo tar -xvf go1.6.linux-amd64.tar.gz  
8. sudo mv go /usr/local  
9. echo "export PATH=\$PATH:/usr/local/go/bin" » .profile  
10. source ~/.profile  
11. mkdir $HOME/gopath  
12. export GOPATH=$HOME/gopath  
13. go get -u github.com/itsyouonline/identityserver  
14. cd gopath/src/github.com/itsyouonline/identityserver  
15. go build  
16. ./identityserver  


# Pre-Requirements:
Create user on the target environment using sign-up and create api key under this user and use this info in the config file [config.ini]
steps:
1. Register with valid authenticator application  
2. Sign-in with valid authenticator application  
3. Fill the user data company/organization etc.  
4. Generate api-key and use it in the config file [config.ini]  

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
