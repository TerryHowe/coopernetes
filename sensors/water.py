#!/usr/bin/env python3

import board
import analogio
from prometheus_client import Gauge

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
        self.thermistor = analogio.AnalogIn(board.A1)


    def read_data(self):
        try:
            self.water.set(self.thermistor.value)
        except Exception as e:
            import traceback
            traceback.print_exc()
        return
