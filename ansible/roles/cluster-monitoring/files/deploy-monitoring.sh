#!/bin/bash -x

set -e 

git clone git@github.com:carlosedp/cluster-monitoring.git
cd cluster-monitoring

# Random SHA1 we have tested
git checkout bf9342e95c8211ebbda6b357ea0048d5283a1bf2

git apply ../roles/cluster-monitoring/files/0001-Raspberry-changes.patch 

make deploy
cd ..
rm -rf cluster-monitoring
