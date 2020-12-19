#!/usr/bin/env python3



class LoadSensors(object):

    def __init__(self, sensors):
        for sensor in sensors:
            module = __import__(sensor['module'])
            sensor_class = getattr(module, sensor['class_name'])
            sensor_instance = sensor_class()
            sensor_instance.collect_data(sensor_instance)
