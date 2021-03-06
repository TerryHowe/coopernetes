#!/usr/bin/env python3

import threading

from base_sensor import BaseSensor


class LoadSensors(object):

    def __init__(self, sensor_names):
        self.sensors = []
        for sensor in sensor_names:
            module = __import__(sensor['module'])
            sensor_class = getattr(module, 'Sensor')
            sensor_instance = sensor_class()
            LoadSensors.collect_data(sensor_instance)
            self.sensors.append(sensor_instance)
            print('Enabled sensor: {}'.format(sensor_instance.description))

    def get_sensor(self, path):
        for sensor in self.get_sensors():
            if '/' + sensor.path == path:
                return sensor
        return BaseSensor()

    def get_sensors(self):
        return self.sensors


    @staticmethod
    def collect_data(sensor):
        sensor.read_data()
        t = threading.Timer(sensor.sample_rate,
                            LoadSensors.collect_data, (sensor,))
        t.start()
