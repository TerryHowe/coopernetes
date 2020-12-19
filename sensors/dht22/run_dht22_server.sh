#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
cd ${BASEDIR}
VERSION=v$(git describe --tags --long)
dht22_server.py $VERSION
