# Coopernetes Sensors

Coopernetes sensor code is written in Python because libraries for
the sensor device drivers is often available in Python. Flask is used
to create a web server and Prometheus Client is used to gather the data.
The sensor code is loaded dynmaically depending on the configuration file.
Each sensor library derived from the BaseSensor class.

This picture shows what the sensors web server looks like with one DHT22
temperature sensor:

![DHT22 Sensor](dht_sensor.png)
