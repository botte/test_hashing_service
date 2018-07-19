# test_hash_service

Python2 / PyTest tests for 'ACME Password Hash Service.'

## Getting Started
```
The service executable must available to the local file system.
It is highly recommended installing the test suite into a Python virtual environment.
```

## NOTE
```
Test suite was ONLY run and tested on Ubuntu 6.04.1.
Tests only verified using python2.
```

### Prerequisites
```
4G RAM

Python2.7.x

NOTE: Tests will NOT run correctly with python3.
```

### Installing, running, and test results output
```
1. Edit the file 'config.ini,' located in base of the cloned test project.

   server = 'file system location of the executable service'
   port = 'service port' 


2. In base project directory, run

     python2 setup.py -q test

3. A results file, 'results.html,' will be created in the base of the test project.

```

### Errors found during testing
```
These five errors are repeatable running the automated test suite.

    - POST /hash did not return immediately, took 5.0
    - GET /stats should not accept data
    - Average time hash request 112559 > assumed max milliseconds 50000
    - New request (GET /stats) accepted when shutdown pending
    - Password request accepted when shutdown pending


Rarely, the following error occurs -
likely a test script and/or timing error - and requires further investigation.

    - Expected requests: 100, reported requests: 99

