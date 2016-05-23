#!/bin/bash

branch=$1
directory=$2
testsuite=$3
GREEN='\033[0;32m' # Green color
NC='\033[0m'       # No color

mkdir -p $directory
cd $directory
rm -rf openvcloud_quality_testsuite
ssh-add -l
#chmod g-r /root/.ssh/id_awesomo
echo -e "${GREEN}** Clone openvcloud_quality_testsuite $branch branch ...${NC}"
ssh-add -l
git clone -b $branch git@github.com:0-complexity/openvcloud_quality_testsuite.git
cd openvcloud_quality_testsuite
echo -e "${GREEN}** Activating JumpScale virtual env ...${NC}"
source /opt/jumpscale7/env.sh
echo -e "${GREEN}** Checking python-pip ...${NC}";
which pip || apt-get install -y python-pip
echo -e "${GREEN}** Installing openvcloud_quality_testsuite requirements ...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}** Running tests ...${NC}"
nosetests $testsuite --with-xunit --xunit-file='testresults.xml' --with-progressive