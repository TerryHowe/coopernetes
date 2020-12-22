#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
cd ${BASEDIR}
git pull 2>/dev/null || true
VERSION=v$(git describe --tags --long)
uwsgi --http 0.0.0.0:5000 --wsgi-file pi_server.py --pyarg "${VERSION}" --callable app
