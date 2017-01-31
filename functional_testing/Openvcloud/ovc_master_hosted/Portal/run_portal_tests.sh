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
	echo "    -d    directory contains testsuite"
	echo "    -r    remote webdriver url"
}

if [[ ( $1 == "--help") ||  $1 == "-h" ]]
then
	usage
	exit 0
fi


OPTIND=1
while getopts ":i:p:s:u:d:r:" opt; do
  case $opt in
	i) user_id="$OPTARG";;
	p) passwd="$OPTARG";;
	s) secret="$OPTARG";;
	u) browser="$OPTARG";;
  d) directory="$OPTARG";;
	r) remote_webdriver="$OPTARG";;
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
directory=${directory:-end_user}
remote_webdriver=${remote_webdriver}

echo -e "${GREEN}**  environment $environment ...${NC}"
echo -e "${GREEN}**  location $location ...${NC}"
echo -e "${GREEN}**  user_id $user_id ...${NC}"
echo -e "${GREEN}**  browser $browser ...${NC}"
echo -e "${GREEN}**  directory $directory ...${NC}"

cd functional_testing/Openvcloud/ovc_master_hosted/Portal
which pip2 || sudo apt-get install -y python-pip python-dev build-essential
sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv

echo -e "${GREEN}** Activating virtual env ...${NC}"
virtualenv env
source env/bin/activate

echo -e "${GREEN}** Installing the requirements ...${NC}"
pip2 install -r requirements.txt

if [[ -z "${remote_webdriver}" ]]; then
	echo -e "${GREEN}** Installing portal test suite requirements ...${NC}"

	echo -e "${GREEN}** Installing xvfv ...${NC}"
	sudo apt-get install -y xvfb

	echo -e "${GREEN}** Installing chromeium ...${NC}"
	sudo apt-get install -y chromium-chromedriver
	sudo ln -fs /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver
	sudo ln -fs /usr/lib/chromium-browser/chromedriver /usr/local/bin/chromedriver

	echo -e "${GREEN}** Installing firefox ...${NC}"
	sudo apt-get intstall -y firefox
	wget https://github.com/mozilla/geckodriver/releases/download/v0.13.0/geckodriver-v0.13.0-linux64.tar.gz -O /tmp/eckodriver.tar.gz
	tar -C /opt -xzf /tmp/eckodriver.tar.gz
	chmod 755 /opt/eckodriver
	ln -fs /opt/eckodriver /usr/bin/eckodriver

	echo -e "${GREEN}** Running tests ...${NC}"
		xvfb-run -a nosetests -v -s  --logging-level=WARNING $directory --tc-file=config.ini --tc=main.passwd:$passwd --tc=main.secret:$secret --tc=main.env:$environment --tc=main.location:$location --tc=main.admin:$user_id --with-xunit --xunit-file='testresults.xml' --with-progressive
fi

if [[ -n "${remote_webdriver}" ]]; then
	nosetests -v -s  --logging-level=WARNING $directory --tc-file=config.ini --tc=main.passwd:$passwd --tc=main.secret:$secret --tc=main.env:$environment --tc=main.location:$location --tc=main.admin:$user_id --tc=main.remote_webdriver:$remote_webdriver --with-xunit --xunit-file='testresults.xml' --with-progressive
fi

# Collect result
echo -e "${GREEN}** DONE ** ...${NC}"
