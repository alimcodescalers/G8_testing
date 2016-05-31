#!/bin/bash

branch=$1
directory=$2
testsuite=$3
GREEN='\033[0;32m' # Green color
NC='\033[0m'       # No color

mkdir -p $directory
cd $directory
rm -rf org_quality
ssh-add -l
#chmod g-r /root/.ssh/id_awesomo
echo -e "${GREEN}** Clone org_quality $branch branch ...${NC}"
ssh-add -l
git clone -b $branch git@github.com:gig-projects/org_quality.git
cd org_quality
echo -e "${GREEN}** Activating JumpScale virtual env ...${NC}"
source /opt/jumpscale7/env.sh
echo -e "${GREEN}** Checking python-pip ...${NC}";
which pip || apt-get install -y python-pip
echo -e "${GREEN}** Installing org_quality requirements ...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}** Running tests ...${NC}"
nosetests $testsuite --with-xunit --xunit-file='testresults.xml' --with-progressive