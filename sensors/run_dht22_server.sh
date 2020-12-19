#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
cd ${BASEDIR}
git pull || true
VERSION=v$(git describe --tags --long)
./dht22_server.py $VERSION
