#!/bin/bash

usage(){
	echo "This script to run OpenVCloud test suite on remote environment"
	echo -e "\nUsage:\n$0 [options] [environment] \n"
	echo "Options:"
	echo "    -n    node on the environment"
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
environment=$1
testsuite=$2
node=${node:-ovc_master}
branch=${branch:-master}
directory=${directory:-/opt/code}

eval $(bash tools/gen_connection_params.sh $environment $node) # This script returns SSHKEY, PROXY and HOST

eval $(ssh-agent -s)
private_key="$HOME/.ssh/id_awesomo"
if [ ! -e $private_key ]; then
    private_key="$HOME/.ssh/id_rsa"
fi 
echo $private_key
ssh-add $private_key
ssh-add -l

script="'bash -s' < tools/setup_run_tests_local.sh $branch $directory $testsuite"
eval "ssh -A -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -M -l root -i $SSHKEY -o ProxyCommand=\"$PROXY\" $HOST $script"

# Collect result
rm -rf logs/
mkdir logs/
eval "scp -r -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i $SSHKEY -o ProxyCommand=\"$PROXY\" root@$HOST:$directory/openvcloud_quality_testsuite/logs/* logs/"

# Copy test results
eval "scp -r -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i $SSHKEY -o ProxyCommand=\"$PROXY\" root@$HOST:$directory/openvcloud_quality_testsuite/testresults.xml ."
