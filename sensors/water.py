#!/usr/bin/env python3

import adafruit_us100
from prometheus_client import Gauge
import serial

from base_sensor import BaseSensor


class Sensor(BaseSensor):
    description = "Water Sensor"
    path = "water"
    image = "water_jpg"
    sample_rate = 30

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        name_prefix = self.hostname + '_water'
        self.water = Gauge(name_prefix + '_water', 'Temperature')
        self.uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3)
        self.water = adafruit_water.US100(self.uart)


    def read_data(self):
        try:
            self.water.set(self.water.level)
        except Exception as e:
            import traceback
            traceback.print_exc()
        return
