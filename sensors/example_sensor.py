#!/usr/bin/env python3

import random

from prometheus_client import Gauge

from base_sensor import BaseSensor


class Sensor(BaseSensor):
    description = "Example Sensor"
    path = "example"
    image = "example_png"
    sample_rate = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        example_data_name = self.hostname + '_example_data'
        self.example_data = Gauge(example_data_name, 'Coopernetes example data')

    def read_data(self):
        value = round(123.456 + (random.random()*10), 1)
        self.example_data.set(value)
        return
