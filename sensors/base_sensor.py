#!/usr/bin/env python3


class BaseSensor(object):
    description = "BaseSensor"
    path = "sensor"
    sample = '{"error": "No data collected yet"}'
    sample_rate = 10

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def get_data(self):
        return self.sample

    def set_data(self, data):
        self.sample = data

    def read_data(self):
        raise Exception("Not implemented")
