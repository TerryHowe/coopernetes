#!/usr/bin/env python3

import os
import sys
import time
import datetime
import threading

import psutil
import Adafruit_DHT
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
app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())

 

class Dht22(object):
    sensor = Adafruit_DHT.DHT22
    pin = 18

    def get_data(self):
        try:
            humidity, temperature_c = Adafruit_DHT.read_retry(self.sensor, self.pin)
            temperature_f = temperature_c * (9 / 5) + 32
            result = '"timestamp": "{}", "temperature": {:.1f}, "humidity": {:.1f}'.format(
                    datetime.datetime.now(),
                    temperature_f,
                    humidity)
            return("{" + result + "}")
        except Exception as e:
            # import traceback 
            # traceback.print_exc()
            return('{"error": "' + str(e) + '"}')
 
    @staticmethod
    def collect_data():
        dht22 = Dht22()
        result = dht22.get_data()
        print(result)
        t = threading.Timer(30.0, Dht22.collect_data)
        t.start() 



Dht22.collect_data()

app.run(host= '0.0.0.0')
