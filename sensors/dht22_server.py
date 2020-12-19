#!/usr/bin/env python3

import os
import sys
import time
import datetime
import threading

import psutil
from flask import Flask
from healthcheck import HealthCheck, EnvironmentDump


app = Flask(__name__)


def pi_health():
    application = os.path.basename(sys.argv[0])
    version = "unknown"
    if len(sys.argv) > 1:
        version = sys.argv[1]

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory()[2]
    disk_usage = {}
    for disk_partition in psutil.disk_partitions():
        disk = disk_partition[1]
        disk_usage[disk] = psutil.disk_usage(disk)[3]
    return True, {
        "application": application,
        "version": version,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
    }


health = HealthCheck()
envdump = EnvironmentDump()
health.add_check(pi_health)

@app.route('/healthcheck')
def healthcheck():
    return health.run()

@app.route('/environment')
def environment():
    return envdump.run()

 


from flask import send_from_directory


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


app.run(host= '0.0.0.0')
