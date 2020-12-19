#!/usr/bin/env python3

from flask import Flask
from healthcheck import HealthCheck, EnvironmentDump
import sys

app = Flask(__name__)

health = HealthCheck()
envdump = EnvironmentDump()

def redis_available():
    return True, "redis ok"

health.add_check(redis_available)

# add your own data to the environment dump
def application_data():
    application = sys.argv[0]
    sha1 = sys.argv[1]
    return {"application": application, "sha1": sha1}

envdump.add_section("application", application_data)

# Add a flask route to expose information
app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())
app.run()
