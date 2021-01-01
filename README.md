# coopernetes

Coopernetes chicken coop monitoring system. There are applications that run
on Pi Zeros for sensors and an array of RP4s for monitoring and alarms.

![DHT22 Sensor](dht_sensor.png)

The [sensor directory](sensor/README.md) contains code that runs on the
Pis for collecting data and putting into a format so it can be gatered
by Prometheus.

The [ansible directory](ansible/README.md) contains Ansible code to
install all the necessary code to get sensors and Kubernetes running.
