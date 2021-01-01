# Coopernetes Sensors

Coopernetes sensor code is written in Python. There is a Flask server
that uses the prometheus client to present sensor data gathered. The
sensor code is loaded dynmaically depending on the configuration file.
Each sensor library derived from the BaseSensor class.

