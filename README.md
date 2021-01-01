# Coopernetes

Coopernetes is a chicken coop monitoring system using Raspberry Pis and
Kubernetes. There are applications that run on Pis that collect data
and a Kubernetes cluster using Pi 4s for monitoring and alarms.

## Sensors

The [sensors directory](sensors/) contains code that runs on the
Pis for collecting data and putting it into a format so it can be gathered
by Prometheus.

## DevOps

The [ansible directory](ansible/) contains Ansible code to install
all the necessary code to get sensors and Kubernetes running. The
idea is to make creating new sensors and Kubernetes clusters easy
so that they can be created and destroyed quickly and with no thought.
The playbooks and roles should be idempotent.
