#!/usr/bin/env python3

import datetime
import threading


class ExampleSensor(object):
    mutex = threading.Lock()
    sample = '{"error": "No data collected yet"}'
    sample_rate = 10

    def get_data(self):
        self.mutex.acquire()
        result = str(self.sample)
        self.mutex.release()
        return result

    def _read_data(self):
        data = '"timestamp": "{}", "data": 123'.format(datetime.datetime.now())
        self.mutex.acquire()
        self.sample = '{' + data + '}'
        self.mutex.release()
 
    @staticmethod
    def collect_data(sensor):
        sensor._read_data()
        print(sensor.get_data())
        t = threading.Timer(sensor.sample_rate,
                            ExampleSensor.collect_data, (sensor,))
        t.start() 
