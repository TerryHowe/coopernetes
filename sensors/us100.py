#!/usr/bin/env python3

import adafruit_us100
from prometheus_client import Gauge
import serial

from base_sensor import BaseSensor


class Sensor(BaseSensor):
    description = "US-100 Sensor"
    path = "us100"
    image = "us100_jpg"
    sample_rate = 30

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        name_prefix = self.hostname + '_us100'
        self.distance = Gauge(name_prefix + '_distance', 'Distance inches')
        self.temperature = Gauge(name_prefix + '_temperature', 'Temperature')
        self.uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3)
        self.us100 = adafruit_us100.US100(self.uart)


    def read_data(self):
        try:
            self.temperature.set(round((((self.us100.temperature * 9.0) / 5.0) + 32), 1))
            self.distance.set(round((self.us100.distance / 2.54), 1))
        except Exception as e:
            import traceback
            traceback.print_exc()
        return
