#!/usr/bin/env python3

#from datetime import datetime, timezone

import time
import board
import adafruit_hcsr04
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)
while True:
    try:
        print((sonar.distance,))
    except RuntimeError:
        print("Retrying!")
    time.sleep(0.1)

#from prometheus_client import Gauge
#
#from base_sensor import BaseSensor

#class Sensor(BaseSensor):
#    description = "DHT22 Sensor"
#    path = "dht22"
#    image = "dht22_png"
#    sample_rate = 30
#    sensor = Adafruit_DHT.DHT22
#    pin = 18
#
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#        self.timestamp = self.get_timestamp()
#        name_prefix = self.hostname + '_dht22_' + str(self.pin)
#        self.temperature = Gauge(name_prefix + '_temperature', 'Temperature')
#        self.humidity = Gauge(name_prefix + '_humidity', 'Humidity Percent')
#        self.last_result = Gauge(name_prefix + '_last_result', 'Last successful read')
#
#    def read_data(self):
#        return
