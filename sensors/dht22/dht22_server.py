#!/usr/bin/env python3

import os
import sys
import psutil
from flask import Flask
from healthcheck import HealthCheck, EnvironmentDump

app = Flask(__name__)

health = HealthCheck()
envdump = EnvironmentDump()

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

health.add_check(pi_health)

# Add a flask route to expose information
app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())
app.run()
