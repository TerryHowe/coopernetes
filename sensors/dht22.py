#!/usr/bin/env python3

import Adafruit_DHT
 

class Dht22(object):

    sensor = Adafruit_DHT.DHT22
    pin = 18

    def get_data(self):
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
            # import traceback 
            # traceback.print_exc()
            return('{"error": "' + str(e) + '"}')
 
    @staticmethod
    def collect_data():
        dht22 = Dht22()
        result = dht22.get_data()
        print(result)
        t = threading.Timer(30.0, Dht22.collect_data)
        t.start() 

# Dht22.collect_data()
# @app.route('/environment')
# def environment():
#     return envdump.run()

