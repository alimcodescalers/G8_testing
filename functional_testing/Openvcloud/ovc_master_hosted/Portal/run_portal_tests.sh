#!/bin/bash

usage(){
	echo "This script to run OVC Portal test suite on local environment"
	echo -e "\nUsage:\n$0 [options] [environment] \n"
	echo "Options:"
	echo "    -i    the admin id"
	echo "    -p    the secret password"
	echo "    -u    the user browser"
	echo "    -b    the testsuite branch"
	echo "    -d    directory contains testsuite"
}

if [[ ( $1 == "--help") ||  $1 == "-h" ]]
then
	usage
	exit 0
fi

OPTIND=1
while getopts ":i:p:u:b:d:" opt; do
  case $opt in
	i) id="$OPTARG";;
	p) passwd="$OPTARG";;
	u) user="$OPTARG";;
    b) branch="$OPTARG";;
    d) directory="$OPTARG";;
    \?) echo "Invalid option -$OPTARG" >&2 ; exit 1;;
  esac
done
shift $((OPTIND-1))
if [[ -z $1 ]]
then
    usage
    exit 1
fi
environment=$1
id=${id:-gig}
user=${user:-firefox}
branch=${branch:-master}
directory=${directory:-end_user}

rm -rf org_quality
ssh-add -l
echo -e "${GREEN}** Clone org_quality $branch branch ...${NC}"
ssh-add -l
git clone -b $branch git@github.com:gig-projects/org_quality.git
cd org_quality/Openvcloud/Portal
echo -e "${GREEN}** Checking python-pip ...${NC}";
which pip2 || apt-get install -y python-pip
echo -e "${GREEN}** Activating JumpScale virtual env ...${NC}"
sudo pip2 install virtualenv
virtualenv venv
source venv/bin/activate
echo -e "${GREEN}** Installing org_quality requirements ...${NC}"
sudo pip2 install -r requirements.txt
echo -e "${GREEN}** Running tests ...${NC}"
Xvfb :99 -ac
export DISPLAY=:99
nosetests -v $directory --tc-file config.ini --tc=main.url:$environment --tc=main.admin:$id --tc=main.passwd:$passwd --tc=main.browser:$user  --with-xunit --xunit-file='testresults.xml' --with-progressive


# Collect result

