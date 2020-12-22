#!/usr/bin/env python3

import random

from prometheus_client import Gauge

from base_sensor import BaseSensor


class Sensor(BaseSensor):
    description = "Example Sensor"
    path = "example"
    image = "example_png"
    sample_rate = 10
    example_data = Gauge('coopernetes_example_data', 'Coopernetes example data')

    def read_data(self):
        value = round(123.456 + (random.random()*10), 1)
        self.example_data.set(value)
        return {
            "timestamp": str(self.get_timestamp()),
            "data": value,
        }
