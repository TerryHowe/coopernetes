#!/usr/bin/env python3

from datetime import datetime, timezone

import Adafruit_DHT
from prometheus_client import Gauge

from base_sensor import BaseSensor


class Sensor(BaseSensor):
    description = "DHT22 Sensor"
    path = "dht22"
    image = "dht22_png"
    sample_rate = 30
    sensor = Adafruit_DHT.DHT22
    pin = 18
    timestamp = datetime.now(tz=timezone.utc)
    result = {'error': 'No data collected yet'}
    temperature = Gauge('coopernetes_dht22_temperature', 'Temperature')
    humidity = Gauge('coopernetes_dht22_humidity', 'Humidity Percent')
    last_result = Gauge('coopernetes_dht22_last_result', 'Last successful read')

    def read_data(self):
        try:
            humidity, temperature_c = Adafruit_DHT.read_retry(self.sensor, self.pin)
            if temperature_c is None:
                timestamp = self.get_timestamp()
                last_result_seconds = (timestamp - self.timestamp).total_seconds()
                last_result = round((float(last_result_seconds) / 60.0), 1)
                self.result['timestamp'] = str(timestamp)
                self.result['last_result'] = last_result
                self.last_result.set(last_result)
                return self.result
            if humidity is None:
                humidity = 0.0

            temperature_f = round((temperature_c * (9 / 5) + 32), 1)
            humidity = round(humidity, 1)
            self.temperature.set(temperature_f)
            self.humidity.set(humidity)
            self.timestamp = self.get_timestamp()
            self.last_result.set(0.0)
            self.result = {
                'timestamp': str(self.timestamp),
                'temperature': temperature_f,
                'humidity': humidity,
                'last_result': 0.0,
            }
            return self.result
        except Exception as e:
            import traceback 
            traceback.print_exc()
            return {'error': str(e)}
