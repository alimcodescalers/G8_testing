#!/bin/bash

usage(){
	echo "This script to run itsyou.online api test suite on local environment"
	echo -e "\nUsage:\n$0 [options] [environment] \n"
	echo "Options:"
	echo "    -i    the application id"
	echo "    -p    the secret password"
	echo "    -u    the user"
	echo "    -b    the testsuite branch"
	echo "    -d    directory to install the testsuite"
}

if [[ ( $1 == "--help") ||  $1 == "-h" ]]
then
	usage
	exit 0
fi

OPTIND=1
while getopts ":i:p:u:d:" opt; do
  case $opt in
	i) id=="$OPTARG";;
	p) passwd=="$OPTARG";;
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
id=${id:-wyWj8JDYWSny2yOJ0wwsvaAyDAUH}
passwd=${passwd:-abmyA-0oYXRwOF5uIPewvktwX6em}
user=${user:-m_flip_flop}
branch=${branch:-master}
directory=${directory:-/opt}


mkdir -p $directory
cd $directory
rm -rf org_quality
ssh-add -l
echo -e "${GREEN}** Clone org_quality $branch branch ...${NC}"
ssh-add -l
git clone -b $branch git@github.com:gig-projects/org_quality.git
cd org_quality/Itsyouonline_testing/api_testing
echo -e "${GREEN}** Activating JumpScale virtual env ...${NC}"
virtualenv venv
source venv/bin/activate
echo -e "${GREEN}** Checking python-pip ...${NC}";
which pip || apt-get install -y python-pip
echo -e "${GREEN}** Installing org_quality requirements ...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}** Running tests ...${NC}"
nosetests testsuite --tc-file config.ini --tc=main.env_url:$environment --tc=main.applicationid:$id --tc=main.secret:$passwd --tc=main.user:$user  --with-xunit --xunit-file='testresults.xml' --with-progressive


# Collect result

