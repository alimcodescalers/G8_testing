#!/bin/bash

apt-get update
echo "Y" | apt-get install fio libx11-dev libgl1-mesa-dev libxext-dev perl perl-modules make
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/byte-unixbench/UnixBench5.1.3.tgz
tar xvf UnixBench5.1.3.tgz
