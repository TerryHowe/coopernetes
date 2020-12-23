#!/usr/bin/env python3

from datetime import datetime, timezone
import socket


class BaseSensor(object):
    description = "BaseSensor"
    path = "sensor"
    image = "example_png"
    sample_rate = 10

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
        self.hostname = socket.gethostname()
        if self.hostname.startswith('rpi-'):
            self.hostname = self.hostname.replace('-', '')
        else:
            self.hostname = 'coop'

    def get_timestamp(self):
        return datetime.now(tz=timezone.utc)

    def read_data(self):
        raise Exception("Not implemented")

