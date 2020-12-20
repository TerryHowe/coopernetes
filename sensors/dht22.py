#!/usr/bin/env python3

import datetime

import Adafruit_DHT

from base_sensor import BaseSensor


class Sensor(BaseSensor):
    description = "DHT22 Sensor"
    path = "dht22"
    image = "dht22_png"
    sample_rate = 30
    sensor = Adafruit_DHT.DHT22
    pin = 18

    def read_data(self):
        data = '"timestamp": "{}", "data": 123'.format(datetime.datetime.now())
        return '{' + data + '}'
        try:
            humidity, temperature_c = Adafruit_DHT.read_retry(self.sensor, self.pin)
            if temperature_c is None:
                return('{"error": "Error collecting data"}')
            if humidity is None:
                humidity = 0.0

            temperature_f = temperature_c * (9 / 5) + 32
            result = '"timestamp": "{}", "temperature": {:.1f}, "humidity": {:.1f}'.format(
                    datetime.datetime.now(),
                    temperature_f,
                    humidity)
            return("{" + result + "}")
        except Exception as e:
            import traceback 
            traceback.print_exc()
            return('{"error": "' + str(e) + '"}')
