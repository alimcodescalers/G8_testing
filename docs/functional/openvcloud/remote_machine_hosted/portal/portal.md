# OpenvCloud Portals Functional Tests
## 1. Introduction:
The goal of the portal test suit is testing the OpenvCloud portals. There are currently two sets of functional test suites for the OpenvCloud portals:

- One covering the **End User Portal**
- Another is covering the **Cloud Broker Portal**

The portal testing framework has been building depending on selenium framework to automate different browsers on different OS.

The documentation for these functional tests is embedded in the actual test code. For instructions on how to setup an **Read the Docs** site consolidating the embedded documentation see the section [Setup a Read the Docs site for your Testing Suite](../../sphinx.md) in this guide.

## 2. Portal Test Suit Architecture:
```
Portal
  | framework # This directory includes the implementation of the testing framework.
  | testcases # This directory includes the implementation of the test cases.
    | admin_portal # This directory includes the test cases which cover **Cloud Broker Portal**.
    | end_user # This directory includes the test cases which cover **End User Portal**.
  | config.ini # This configuration file includes the configuration parameters.
  | requirements.txt # This file include all the requirement python packages.
  | run_portal_tests.sh # This file includes the bash script to automatically execute the test suit.
```
## 3. Test Suit Execution:
This test suit can be executed from Ubuntu Desktop or Server operating systems. There are three modes of execution:
- Normal execution
- Grid execution
- Manual execution

### 3.1 Normal Execution:
In normal execution mode, The tester will execute the portal test suit on one linux machine.
#### 3.1.1 Execution Guide:

- After making sure your SSH private key is loaded by ssh-agent, clone the **G8_testing** repository:

  ```
  ssh-add -l
  git clone git@github.com:0-complexity/G8_testing.git
  ```

- Run the following command after replacing each <variable> with its value:

  ```
  cd G8_testing/
  sudo bash functional_testing/Openvcloud/ovc_master_hosted/Portal/run_portal_tests.sh -u <browser> -i <username> -p <password> -s <secret> -d <testcases directory> <environment_url> <location>
  ```
   - Browser : firefox or chrome
   - username : itsyou.online username
   - password : itsyou.online password
   - secret : itsyou.online secret key
   - testcase_directory : the directory of the test cases
   - environment_url : the environment url
   - location : the environment location
   Example:
   ```
  sudo bash functional_testing/Openvcloud/ovc_master_hosted/Portal/run_portal_tests.sh -u chrome -i username -p username123 -s BMDHEDMMGFZG7RBMDHEDMMGFZG7R -d testcases/admin_portal/cloud_broker/test01_accounts.py http://du-conv-2.demo.greenitglobe.com du-conv-2
   ```

The run_portal_tests.sh script will update the operating systems and install python, pip, virtualenv and all requirement package in requirement.txt then it will start a virtual environment, install latest chrome and firefox and finally execute the test cases in headless mode.

### 3.2 Grid Execution:
In grid execution, Tester is using a selenium server as hub, chrome node, firefox node and any other browser node. In this documentation, we will intro how to prepare a testing environment which has hub, chrome node and firefox node as a docker containers.

#### 3.2.1 Prepare The Grid:
After installing the docker service in the machine operating system, run the following commands:
```
docker run -d -p 4444:4444 --name selenium-hub selenium/hub
docker run -d --name chrome-node --link selenium-hub:hub selenium/node-chrome
docker run -d --name firefox-node --link selenium-hub:hub selenium/node-firefox
```
Now you can access this remote server via **http://localhost:4444** and you can execute test cases on firefox-node and chrome-node. If you wanna connect this hub from your machine, You have to do a port forward from the cloudspace to the hub machine and then the remote webdriver will be **http://< clocud_space_ip>:4444**

#### 3.2.2 Execution Guide:
- After making sure your SSH private key is loaded by ssh-agent, clone the **G8_testing** repository:

  ```
  ssh-add -l
  git clone git@github.com:0-complexity/G8_testing.git
  ```

- Run the following command after replacing each <variable> with its value:

  ```
  cd G8_testing/
  sudo bash functional_testing/Openvcloud/ovc_master_hosted/Portal/run_portal_tests.sh -r <remote_webdriver> -u <browser> -i <username> -p <password> -s <secret> -d <testcases directory> <environment_url> <location>
  ```
   - remote_webdriver : remote server ip:port
   - Browser : firefox or chrome
   - username : itsyou.online username
   - password : itsyou.online password
   - secret : itsyou.online secret key
   - testcase_directory : the directory of the test cases
   - environment_url : the environment url
   - location : the environment location
   Example:
   ```
  sudo bash functional_testing/Openvcloud/ovc_master_hosted/Portal/run_portal_tests.sh -r http://localhost:4444 -u chrome -i username -p username123 -s BMDHEDMMGFZG7RBMDHEDMMGFZG7R -d testcases/admin_portal/cloud_broker/test01_accounts.py http://du-conv-2.demo.greenitglobe.com du-conv-2
   ```

The run_portal_tests.sh script will update the operating systems and install python, pip, virtualenv and all requirement package in requirement.txt then it will execute the test cases in through the remote server.


### 3.3 Manual Execution:
In manual execution, Tester will install all dependencies and run the execution command manually on his machine.
- To install the requirements, run:
```
pip install -r requirement.txt
```
#### 3.3.1 Prepare The Machine:
To execute this test suit, the machine should has chrome and firefox, so run the following commands to isnallt them in the right way.

```
echo -e "${GREEN}** Installing xvfb ...${NC}"
sudo apt-get update
sudo apt-get install -y xvfb

echo -e "${GREEN}** Installing chromium ...${NC}"
sudo apt-get install -y chromium-chromedriver
sudo ln -fs /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver
sudo ln -fs /usr/lib/chromium-browser/chromedriver /usr/local/bin/chromedriver

echo -e "${GREEN}** Installing firefox ...${NC}"
which firefox && firefox_version=(firefox -v)
if [[ $firefox_version != 'Mozilla Firefox 46.0' ]]; then
	apt-get -y purge firefox
	wget 'https://ftp.mozilla.org/pub/firefox/releases/46.0/linux-x86_64/en-US/firefox-46.0.tar.bz2' -O /tmp/firefox.tar.gz
	tar -C /opt/ -xf /tmp/firefox.tar.gz
	chmod 775 /opt/firefox/firefox
	ln -fs /opt/firefox/firefox /usr/bin/firefox
	ln -fs /opt/firefox/firefox /usr/local/bin/firefox
fi

```
#### 3.3.2 Execution Guide:
- After making sure your SSH private key is loaded by ssh-agent, clone the **G8_testing** repository:

  ```
  ssh-add -l
  git clone git@github.com:0-complexity/G8_testing.git
  ```
- Change the necessary parameters in **config.ini** according to your environment:
  ```
  [main]
  env = <environment_url>
  location = <locations>
  #location for the environment in the grid, ex.: du-conv-2,du-conv-1,du-conv-3
  admin = <username>
  passwd = <password>
  browser = <browser>
  secret = <secret>
  remote_webdriver = <remote_webdriver>
  ```
  - Browser : firefox or chrome
  - username : itsyou.online username
  - password : itsyou.online password
  - secret : itsyou.online secret key
  - environment_url : the environment url
  - location : the environment location
  - remote_webdriver : remote server ip:port

- Desktop OS: Run the testcase using **nosetests**:

```
nosetests -v -s  --logging-level=WARNING <testsuite_directory> --tc-file=config.ini  2>testresults.log
```

- Server OS : Use the **xfvb-run** package to run the testcases on Ubuntu Server:
```
xvfb-run -a nosetests -v -s  --logging-level=WARNING <testsuite_directory> --tc-file=config.ini  2>testresults.log
```

You can also overwrite the **config.ini** parameters:

```
nosetests -v testsuite --tc-file=config.ini --tc=main.url:http://be-conv-2.demo.greenitglobe.com/  --tc=main.admin:gig 2>testresults.log
```

## 4. Appendix:
### 4.1 How to get itsyouonline secret?
- During registering a new itsyou.online account, scan the QR code using any QR scanner or you can use **right-click QRcode reader** it is a free **google chrome extension**, and you will find the secret code after secret parameter in the message.
