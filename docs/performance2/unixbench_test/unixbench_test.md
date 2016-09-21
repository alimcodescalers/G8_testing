## UnixBench Test

### Prerequisites
- Have a G8 running the latest version of OpenvCloud
- Clean the G8, so no virtual machines are running on it
- Have an admin user with only one corresponding account
- Make sure you Jumpscale8 is installed on your personal machine
  (https://github.com/Jumpscale/jumpscale_core8/blob/master/docs/GettingStarted/Installation.md)


### Test case description
- Create one user with corresponding account 
- Create a number of cloud spaces that will be used for the test
- Create a number of virtual machines you want to run the UnixBench on
- Install UnixBench on the created virtual machines
- Run UnixBench on the required number of virtual machines, then store all UnixBench scores

### Expected result
- Create a result table providing the average UnixBench score per virtual machine:

  |VM name  | CPUs  | Memory | HDD | Iteration 1 | Iteration 2 | ... | Iteration x | Avg UnixBench Score|

### Running the test
- The test is divided into 2 scripts:

    - **add_vms.py** creates all virtual machines and installs UnixBench on them
      - - This test is also used to install fio on the virtual machines
    - **run_unixbench.py** runs UnixBench on the specified number of virtual machines in parallel


- Go to the scripts testing directory:

  ```
  cd G8_testing/performance_testing/scripts
  ```

- Following parameters can be configured:

  ```  
-u USERNAME, --user=USERNAME
                        username to login on the OVC api
  -p PASSWORD, --pwd=PASSWORD
                        password to login on the OVC api
  -e ENVIRONMENT, --env=ENVIRONMENT
                        environment to login on the OVC api
  -v REQUIRED_VMS, --vms=REQUIRED_VMS
                         selected number of virtual machines to run unixbench
                        on
  -t TEST_RUNTIME, --runtime=TEST_RUNTIME
                        duration for running unixbecnh (in secs)
  -d TIME_INTERVAL, --interval=TIME_INTERVAL
                        time interval between starting unixbench on 2
                        successive machines   (in secs)
  -r RESULTS_DIR, --rdir=RESULTS_DIR
                        absolute path for results directory
  -n CONCURRENCY, --con=CONCURRENCY
                        amount of concurrency to execute the job
  -s TESTSUITE, --ts=TESTSUITE
                        location to find Testsuite directory
```

- Finally start creating virtual machines:

  ```
  see ....
  ```

- Then run UnixBench on a specified number of virtual machines:

  ```
  cd G8_testing/performance_testing/scripts
  python3 run_unixbench.py --{provide needed parameters}
  ```


### Result sample
- The results of the tests will on the results directory specified during the test
  ```
  cd (results_directory)/(date)_(cpu_name).(env_name)_testresults(run_number)/
  vim (date)_(cpu_name).(pc_hostname)_testresults(run_number).csv
  ```

- Also results will be pushed on the environment repo under testresults directory
  - please make sure to identify who you are
  ```
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
  ```



