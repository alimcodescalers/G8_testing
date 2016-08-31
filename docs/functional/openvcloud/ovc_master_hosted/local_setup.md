## Local Setup of the OpenvCloud Functional Tests

For setting up the OpenvCloud functional tests, you have two options:
- Install everything directly on the master cloud space, so locally from the perspecitive where the tests will actually run
- Install everything on your local machine, so remotely from the perspective of where the tests will actually run

Here we discuss the first option.

There are three simple steps:
- Clone the G8_testing repository to the remote machine, which will most probably actually be your local machine:
  ```
  git clone git@github.com:0-complexity/G8_testing.git
  ```
- Run the `setup_run_tests_local.sh` script with the required pareameters