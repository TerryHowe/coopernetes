#!/usr/bin/env python3

from datetime import datetime, timezone

import Adafruit_DHT
from prometheus_client import Gauge

from base_sensor import BaseSensor


class Sensor(BaseSensor):
    description = "DHT22 Sensor"
    path = "dht22"
    image = "dht22_png"
    sample_rate = 30
    sensor = Adafruit_DHT.DHT22
    pin = 18

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = self.get_timestamp()
        name_prefix = self.hostname + '_dht22_' + str(self.pin)
        self.temperature = Gauge(name_prefix + '_temperature', 'Temperature')
        self.humidity = Gauge(name_prefix + '_humidity', 'Humidity Percent')
        self.last_result = Gauge(name_prefix + '_last_result', 'Last successful read')

    def read_data(self):
        try:
            humidity, temperature_c = Adafruit_DHT.read_retry(self.sensor, self.pin)
            if temperature_c is None:
                timestamp = self.get_timestamp()
                last_result_seconds = (timestamp - self.timestamp).total_seconds()
                self.last_result.set(round((float(last_result_seconds) / 60.0), 1))
                return
            if humidity is None:
                humidity = 0.0

            self.timestamp = self.get_timestamp()
            self.temperature.set(round((temperature_c * (9 / 5) + 32), 1))
            self.humidity.set(round(humidity, 1))
            self.last_result.set(0.0)
            return
        except Exception as e:
            import traceback 
            traceback.print_exc()
            return
