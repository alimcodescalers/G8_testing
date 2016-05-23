#!/bin/bash

set -xe

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cd docs/
make clean
make html