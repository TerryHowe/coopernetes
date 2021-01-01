#!/bin/bash -x

set -e 

git clone git@github.com:carlosedp/cluster-monitoring.git
cd cluster-monitoring

# Random SHA1 we have tested
git checkout a136833aaf364a8e76809a9dca789bb59e070677

git apply ../roles/cluster-monitoring/files/0001-Raspberry-changes.patch 

make deploy
cd ..
rm -rf cluster-monitoring
