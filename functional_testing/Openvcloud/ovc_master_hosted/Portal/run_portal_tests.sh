#!/bin/bash

GREEN='\033[0;32m' # Green color
NC='\033[0m'       # No color

usage(){
	echo "This script to run OVC Portal test suite on local environment"
	echo -e "\nUsage:\n$0 ${GREEN}[options] [environment_url] [location]${NC} \n"
	echo "Options:"
	echo "    -i    the admin user id"
	echo "    -p    the secret password"
	echo "    -u    the browser name"
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
	i) user_id="$OPTARG";;
	p) passwd="$OPTARG";;
	u) browser="$OPTARG";;
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

if [[ -z $2 ]]
then
    usage
    exit 1
fi

environment=$1
location=$2
browser=${browser:-firefox}
branch=${branch:-master}
directory=${directory:-end_user}


echo -e "${GREEN}**  environment $environment ...${NC}"
echo -e "${GREEN}**  location $location ...${NC}"
echo -e "${GREEN}**  user_id $user_id ...${NC}"
echo -e "${GREEN}**  passwd $passwd ...${NC}"
echo -e "${GREEN}**  browser $browser ...${NC}"
echo -e "${GREEN}**  branch $branch ...${NC}"
echo -e "${GREEN}**  directory $directory ...${NC}"

#cd functional_testing/Openvcloud/ovc_master_hosted/Portal
#which pip2 || sudo apt-get install -y python-pip
#echo -e "${GREEN}** Activating virtual env ...${NC}"
#virtualenv venv
#source venv/bin/activate
#echo -e "${GREEN}** Installing portal test suite requirements ...${NC}"
#pip2 install -r requirements.txt
#echo -e "${GREEN}** Running tests ...${NC}"
#Xvfb :99 -ac
#export DISPLAY=:99

#echo -e "${GREEN}** Start nose for $directory browser $browser...${NC}"
#xvfb-run -a nosetests -v admin_portal/admin/test01_create_account_user_cs_vm.py --tc-file=config.ini --tc=main.env:$environment --tc=main.location:$location --tc=main.admin:$user_id --tc=main.browser:$browser  --with-xunit --xunit-file='testresults.xml' --with-progressive


sudo apt-get install xvfb
xvfb-run -a nosetests -v $directory --tc-file=config.ini --tc=main.passwd:KrOe6gE9K5nCQdmretfXnj --tc=main.env:$environment --tc=main.location:$location --tc=main.admin:$user_id --tc=main.browser:$browser  --with-xunit --xunit-file='testresults.xml' --with-progressive

# Collect result
echo -e "${GREEN}** DONE ** ...${NC}"
