#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
cd ${BASEDIR}
git pull 2>/dev/null || true
VERSION=v$(git describe --tags --long)
./dht22_server.py $VERSION
