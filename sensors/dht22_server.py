#!/usr/bin/env python3

import os

from flask import Flask
from flask import send_from_directory

from pi_health import get_healthcheck, get_environment


app = Flask(__name__)


@app.route('/healthcheck')
def healthcheck():
    result = app.make_response(get_healthcheck())
    result.mimetype = 'application/json'
    return result


@app.route('/environment')
def environment():
    result = app.make_response(get_environment())
    result.mimetype = 'application/json'
    return result


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


app.run(host= '0.0.0.0')
