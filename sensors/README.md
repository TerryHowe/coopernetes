# Coopernetes Sensors

Coopernetes sensor code is written in Python because libraries for
the sensor device drivers is often available in Python. Flask is used
to create a web server and Prometheus client is used to gather the data.
The sensor code is loaded dynmaically depending on the configuration file.
Each sensor library derived from the BaseSensor class. See the
`sample_config.yaml` for an example of the configuration with the
example sensor. You can override the sample configuration by creating
a `config.yaml` in this directory.

This picture shows what the sensors web server looks like with one DHT22
temperature sensor:

![DHT22 Sensor](dht_sensor.png)

A metrics page is added to the Flask web server for the Prometheus client
that makes the sensor data available for Prometheus to scrape. The data
for a temperature sensor looks like:

    # HELP rpi128_dht22_18_temperature Temperature
    # TYPE rpi128_dht22_18_temperature gauge
    rpi128_dht22_18_temperature 24.4
    # HELP rpi128_dht22_18_humidity Humidity Percent
    # TYPE rpi128_dht22_18_humidity gauge
    rpi128_dht22_18_humidity 63.1

The metrics names are made up of host name, sensor type, optionally GPIO
pin and metric identifier. In this example, the host is rpi128, sensor
is dht22, GPIO pin 18, and metric is temperature and humidity.

# Development and Testing

Most of the sensors will probably not work on your development machine
unless you are developing on a Raspberry Pi. To make things easier for
development and testing, the pi_sensor server looks for a `config.yaml`
first and if that does not exist, it reads the `sample_config.yaml`. The
sample config loads the `example_sensor` so you can test the sensor server
on a machine that does not have special libraries or software.

# Adding a Sensor

A new sensor can be added as long as the class name is `Sensor` and it
derives from `BaseSensor`. It must define the `read_data` method:

    from prometheus_client import Gauge
    from base_sensor import BaseSensor
    
    class Sensor(BaseSensor):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.reading = Gauge('reading', 'Reading')
    
        def read_data(self):
            self.reading.set(4)

To load the sensor, just add the module name to your configuration file.
