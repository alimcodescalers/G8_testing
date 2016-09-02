## OpenvCloud Portals Functional Tests

Currently only the **End User Portal** is covered.

### Requirements

- Supported browsers for Ubuntu:
  - Chrome
  - Firefox <= 46.0
- Current tests can only run from Ubuntu Desktop, not server
- Make sure Pythin 2.7 is installed:
  ```
  sudo apt-get update
  sudo apt-get install python2.7
  sudo apt-get install python-setuptools python-dev build-essential
  sudo easy_install pip
  ```
- Install **virtual env**, create a virtual environment and load the virtual environment:
  ```
  pip install virtualenv
  virtualenv venv
  source venv/bin/activate
  ```

- Install some other dependenies:
  ```
  git clone https://github.com/0-complexity/G8_testing.git
  cd G8_testing/functional_testing/Openvcloud/ovc_master_hosted/Portal
  pip install -r requirements.txt
  ```


### Running the tests

Change the necessary parameters in **config.ini** according to your environment:
```
[main]
env = http://du-conv-2.demo.greenitglobe.com
#url for the environment portal
location = du-conv-2
#location for the environment in the grid, ex.: du-conv-2, du-conv-1, du-conv-3
admin = gig
passwd = 
browser = firefox
```

Run the test using **nosetests** using the required parameters:
```
nosetests -v testsuite_name --tc-file=config.ini  2>testresults.log
```

Currently we have two test suites: **end\_user** ans **admin\_portal**.

So for running the **end\_user** test suite:
```
nosetests -v end_user --tc-file=config.ini  2>testresults.log
```

You can also overwrite the **config.ini** parameters:
```
nosetests -v testsuite --tc-file=config.ini --tc=main.url:http://be-conv-2.demo.greenitglobe.com/  --tc=main.admin:gig 2>testresults.log
```