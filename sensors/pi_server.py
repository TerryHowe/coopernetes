#!/usr/bin/env python3

import os

from flask import Flask
from flask import send_from_directory
from flask import render_template

from pi_health import get_hostname, get_healthcheck, get_environment
from pi_config import PiConfig

from load_sensors import LoadSensors


app = Flask(__name__)
pi_config = PiConfig()
load_sensors = LoadSensors(pi_config.get_sensors())


@app.route('/')
def index():
    parameters = {
        "title": get_hostname(),
        "hostname": get_hostname(),
        "sensors": load_sensors.get_sensors(),
    }
    return render_template('index.html', **parameters)


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


@app.route('/apple-touch-icon.png')
def favicon_apple_touch():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'apple-touch-icon.png', mimetype='image/png')


@app.route('/android-chrome-192x192.png')
def favicon_192x192():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'android-chrome-192x192.png', mimetype='image/png')


@app.route('/android-chrome-512x512.png')
def favicon_512x512():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'android-chrome-512x512.png', mimetype='image/png')


@app.route('/favicon-32x32.png')
def favicon_32x32():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon-32x32.png', mimetype='image/png')


@app.route('/favicon-16x16.png')
def favicon_16x16():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon-16x16.png', mimetype='image/png')


@app.route('/site.webmanifest')
def webmanifest():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'site.webmanifest', mimetype=' application/manifest+json')


@app.route('/style.css')
def style_css():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'style.css', mimetype='text/css')


@app.route('/example')
def example():
    result = app.make_response("bogus")
    result.mimetype = 'application/json'
    return result


app.run(host= '0.0.0.0')
