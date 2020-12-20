#!/usr/bin/env python3

import random

from base_sensor import BaseSensor


class Sensor(BaseSensor):
    description = "Example Sensor"
    path = "example"
    image = "example_png"
    sample_rate = 10

    def read_data(self):
        return {
            "timestamp": self.get_timestamp(),
            "data": round(123.456 + random.random(), 1),
        }
