# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Coopernetes is a chicken coop monitoring system using Raspberry Pis and Kubernetes. It consists of:
- **Sensor applications** that run on Raspberry Pis to collect environmental data (temperature, humidity, distance, water levels)
- **Kubernetes cluster** running on Pi 4s for monitoring and alerting via Prometheus, Grafana, and AlertManager

The philosophy is "livestock, not pets" - all Raspberry Pis should be easily deployable and replaceable through automation.

## Architecture

### Sensors (`sensors/`)
- Python-based Flask web server (`pi_server.py`) that dynamically loads sensor modules
- Each sensor extends `BaseSensor` class and implements a `read_data()` method
- Sensors expose metrics via Prometheus client at `/metrics` endpoint
- Configuration via YAML file loaded by `PiConfig` class - looks for `config.yaml` first, falls back to `sample_config.yaml`
- Metric naming: `{hostname}_{sensor_type}_{gpio_pin}_{metric_name}` (e.g., `rpi128_dht22_18_temperature`)
- Available sensors: DHT22 (temp/humidity), US-100 (distance), water level sensors, Milone eTape
- Sensors run on a timer thread (default 10s sample rate) via `LoadSensors` class in `load_sensors.py`
- Web UI includes index page showing all sensors, `/healthcheck` and `/environment` endpoints
- Server runs via uwsgi on port 5000 in production (deployed as systemd service `pi_server`)

### Ansible Deployment (`ansible/`)
- All infrastructure automation is Ansible-based with idempotent playbooks and roles
- Inventory in `hosts.ini` - update with your Pi IP addresses
- Uses Ansible vault for secrets (password file at `~/.ansiblevault`)
- Requires SSH key at `~/.ssh/id_rsa`

### Kubernetes Stack
- Uses containerd as container runtime (converted from Docker)
- Flannel for pod networking
- nginx-ingress for ingress controller
- Prometheus + Grafana + AlertManager for monitoring (cluster-monitoring stack)

## Common Commands

### Development Setup
```bash
# Create Python virtualenv for Ansible
pip install virtualenvwrapper
export WORKON_HOME=~/.virtualenvs
mkdir -p $WORKON_HOME
virtualenv -p /usr/local/bin/python3 ${WORKON_HOME}/coop
workon coop
pip install -r ansible/requirements.txt
```

### Ansible Deployment Workflow

**Important:** All ansible commands should be run from the `ansible/` directory.

**1. Burn a new SD card for Raspberry Pi:**
```bash
cd ansible
ansible-playbook -v -e arch=arm64 playbooks/disk_burn.yml
```
Note: First Pi must be set up manually with Raspberry Pi Imager (enable SSH, WiFi, set authorized keys). The disk burn playbook runs on the `k8sprimary` host, so that node must already exist.

**2. Deploy a sensor application:**
```bash
# Examples for different sensor types (run from ansible/ directory)
ansible-playbook -v playbooks/dht22.yml      # Temperature/humidity sensor
ansible-playbook -v playbooks/us100.yml      # Distance sensor
```
Sensor playbooks clone the coopernetes repo to `/home/pi/coopernetes` on the target, install Python dependencies, create a `config.yaml` from template, and set up the `pi_server` systemd service.

**3. Set up a Kubernetes node:**
```bash
# Step 1: Install Kubernetes prerequisites and binaries
ansible-playbook -v -e target=172.27.27.159 playbooks/k8sinstall.yml

# Step 2a: Configure as control plane node
ansible-playbook -v playbooks/k8sprimary.yml

# Step 2b: Or configure as worker node
ansible-playbook -v playbooks/k8sworker.yml
```

**4. Deploy monitoring stack:**
```bash
# Deploy Prometheus, Grafana, and AlertManager to k8s cluster
ansible-playbook -v playbooks/prometheus.yml

# Deploy ingress controller (separate due to potential Flannel conflicts)
ansible-playbook -v playbooks/ingress-nginx.yml
```

### Sensor Development

**Run sensor server locally:**
```bash
cd sensors
./run_server.sh
# Uses sample_config.yaml with example_sensor for testing without real hardware
# Runs uwsgi on http://0.0.0.0:5000
# Access UI at http://localhost:5000
# Access metrics at http://localhost:5000/metrics
```

**Add a new sensor:**
1. Create a new Python module in `sensors/`
2. Define a `Sensor` class that extends `BaseSensor`
3. Implement `read_data()` method using Prometheus client gauges
4. Add module name to `config.yaml` sensors list

Example:
```python
from prometheus_client import Gauge
from base_sensor import BaseSensor

class Sensor(BaseSensor):
    description = "My Sensor"
    path = "mysensor"
    sample_rate = 10  # seconds

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reading = Gauge(f'{self.hostname}_mysensor_reading', 'Reading')

    def read_data(self):
        value = # ... read from hardware
        self.reading.set(value)
```

## Important Notes

- The `target` variable in k8s playbooks allows running against specific hosts instead of inventory groups
- Sensors use dynamic imports via `load_sensors.py` - sensor class must be named `Sensor`
- Hostname normalization: `rpi-XXX` becomes `rpiXXX` in metrics (see `base_sensor.py:16-20`)
- Ansible roles should be idempotent for repeatability
- Sensor data is collected on a background timer thread that calls `read_data()` at the configured `sample_rate` interval
- Each sensor can define custom attributes: `description`, `path`, `image`, and `sample_rate` (default 10s)
- The `pi_server` role targets hosts based on playbook inventory groups (e.g., `thermometers`, `food`) defined in `hosts.ini`
