#!/usr/bin/env python3

import datetime

from base_sensor import BaseSensor


class Sensor(BaseSensor):
    description = "Example Sensor"
    path = "example"
    sample_rate = 10
    image = "example_png"

    def read_data(self):
        data = '"timestamp": "{}", "data": 123'.format(datetime.datetime.now())
        return '{' + data + '}'
