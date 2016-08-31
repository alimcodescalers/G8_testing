#!/bin/bash

usage(){
	echo "This script to run OpenVCloud test suite on remote grid"
	echo -e "\nUsage:\n$0 [options] [grid] \n"
	echo "Options:"
	echo "    -n    node on the grid"
	echo "    -b    testsuite branch to run tests from"
	echo "    -d    directory to install the testsuite"
}

if [[ ( $1 == "--help") ||  $1 == "-h" ]]
then
	usage
	exit 0
fi

OPTIND=1
while getopts ":n:b:d:" opt; do
  case $opt in
    n) node="$OPTARG";;
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
grid=$1
environment=$2
testsuite=$3
node=${node:-ovc_master}
branch=${branch:-master}
directory=${directory:-/opt/code}

su jenkins
eval $(ssh-agent -s)
private_key="$HOME/.ssh/id_awesomo"
if [ ! -e $private_key ]; then
    private_key="$HOME/.ssh/id_rsa"
fi 
echo $private_key
ssh-add $private_key
ssh-add -l

python3 Openvcloud/tools/sshconfigen.py -r $grid >> .ssh/config
eval $(bash Openvcloud/tools/gen_connection_params.sh $grid $node) # This script returns SSHKEY, PROXY and HOST


script="'bash -s' < Openvcloud/tools/setup_run_tests_local.sh $branch $directory $environment $testsuite "
eval "ssh -A -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -M -l root -i $SSHKEY -o ProxyCommand=\"$PROXY\" $HOST $script"

# Collect result
rm -rf logs/
mkdir logs/
eval "scp -r -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i $SSHKEY -o ProxyCommand=\"$PROXY\" root@$HOST:$directory/org_quality/logs/* logs/"

# Copy test results
eval "scp -r -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i $SSHKEY -o ProxyCommand=\"$PROXY\" root@$HOST:$directory/org_quality/testresults.xml ."
