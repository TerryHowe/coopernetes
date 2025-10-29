# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Coopernetes is a chicken coop monitoring system using Raspberry Pis and Kubernetes. It consists of:
- **Sensor applications** that run on Raspberry Pis to collect environmental data (temperature, humidity, distance, water levels)
- **Kubernetes cluster** running on Pi 4s for monitoring and alerting via Prometheus, Grafana, and AlertManager

The philosophy is "livestock, not pets" - all Raspberry Pis should be easily deployable and replaceable through automation.

**Repository Structure:**
- `sensors/` - Python sensor server and sensor modules
- `ansible/` - All deployment automation (playbooks and roles)
- `prometheus/` - Kubernetes monitoring stack manifests
- `simulator/` - Sensor simulation tools

## Architecture

### Sensors (`sensors/`)
- Python-based Flask web server (`pi_server.py`) that dynamically loads sensor modules
- Each sensor extends `BaseSensor` class and implements a `read_data()` method
- Sensors expose metrics via Prometheus client at `/metrics` endpoint
- Configuration via YAML file loaded by `PiConfig` class - looks for `config.yaml` first, falls back to `sample_config.yaml`
  - Config structure: `sensors: [{ module: sensor_name }]` - list of sensor module names to load
- Metric naming: `{hostname}_{sensor_type}_{gpio_pin}_{metric_name}` (e.g., `rpi128_dht22_18_temperature`)
- Available sensors: DHT22 (temp/humidity), US-100 (distance), water level sensors, Milone eTape
- Sensors run on a timer thread (default 10s sample rate) via `LoadSensors` class in `load_sensors.py`
  - Timer starts immediately on sensor initialization via `LoadSensors.collect_data()` static method
  - Each sensor can override `sample_rate` attribute to change collection frequency
- Web UI includes index page showing all sensors, `/healthcheck` and `/environment` endpoints
- Server runs via uwsgi on port 5000 in production (deployed as systemd service `pi_server`)

### Ansible Deployment (`ansible/`)
- All infrastructure automation is Ansible-based with idempotent playbooks and roles
- Inventory in `hosts.ini` - defines host groups (`thermometers`, `food`, `k8sprimary`, `k8sworkers`)
  - Update with your Pi IP addresses for each functional group
- Uses Ansible vault for secrets (password file at `~/.ansiblevault`)
  - To encrypt: `ansible-vault encrypt <file>`
  - To edit: `ansible-vault edit <file>`
- Requires SSH key at `~/.ssh/id_rsa`
- Key roles:
  - `pi_server` - Deploys sensor server and systemd service
  - `k8s/install` - Installs containerd and Kubernetes binaries
  - `k8s/configuration` - Configures OS for Kubernetes (cgroups, modules, sysctl)
  - `k8s/primary` - Initializes control plane with `kubeadm init`
  - `k8s/worker` - Joins worker nodes to cluster
  - `k8s/users/{root,pi,localhost}` - Copies kubeconfig to different users
  - `flannel` - Deploys Flannel CNI for pod networking
  - `cluster-monitoring` - Deploys Prometheus, Grafana, AlertManager stack

### Kubernetes Stack
- Uses containerd as container runtime (converted from Docker)
- Flannel for pod networking
- nginx-ingress for ingress controller
- Prometheus + Grafana + AlertManager for monitoring (cluster-monitoring stack)

## Common Commands

### Development Setup

**Prerequisites:**
- SSH key at `~/.ssh/id_rsa`
- Ansible vault password file at `~/.ansiblevault` (single line with password, chmod 600)

**Python environment for Ansible:**
```bash
pip install virtualenvwrapper
export WORKON_HOME=~/.virtualenvs
mkdir -p $WORKON_HOME
virtualenv -p /usr/local/bin/python3 ${WORKON_HOME}/coop
workon coop
pip install -r ansible/requirements.txt
```

**Optional: Add to shell rc for persistent activation:**
```bash
export WORKON_HOME=~/.virtualenvs
source $(which virtualenvwrapper.sh)
workon coop
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
# The target variable allows targeting specific IPs instead of inventory groups
# Default: Kubernetes 1.31 (latest stable)
ansible-playbook -v -e target=172.27.27.159 playbooks/k8sinstall.yml

# To install a different version, override k8s_major_minor and k8s_version:
ansible-playbook -v -e target=172.27.27.159 -e k8s_major_minor=1.30 -e k8s_version=1.30.8-1.1 playbooks/k8sinstall.yml

# Step 2a: Configure as control plane node
# Runs k8s/configuration, k8s/primary, k8s/users/*, and flannel roles
ansible-playbook -v playbooks/k8sprimary.yml

# Step 2b: Or configure as worker node
# Runs k8s/configuration and k8s/worker roles
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
1. Create a new Python module in `sensors/` (e.g., `my_sensor.py`)
2. Define a `Sensor` class that extends `BaseSensor` (class MUST be named `Sensor`)
3. Set class attributes: `description`, `path`, `sample_rate` (optional, defaults to 10s)
4. Implement `__init__()` to create Prometheus Gauge metrics
5. Implement `read_data()` method to read hardware and update gauges
6. Add module name (without .py) to `config.yaml` sensors list: `sensors: [{ module: my_sensor }]`

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
        # Metric naming: {hostname}_{sensor}_{metric}
        self.reading = Gauge(f'{self.hostname}_mysensor_reading', 'Reading')

    def read_data(self):
        value = # ... read from hardware
        self.reading.set(value)
```

**Test sensor locally:**
```bash
cd sensors
# Add your sensor module to sample_config.yaml
./run_server.sh
# Access http://localhost:5000 for UI
# Access http://localhost:5000/metrics for Prometheus metrics
```

## Important Notes

**Ansible:**
- All playbook commands should be run from the `ansible/` directory
- The `target` variable in k8s playbooks allows targeting specific IP addresses instead of inventory groups
- Sensor playbooks target hosts by functional group in `hosts.ini` (e.g., `thermometers`, `food`)
- All roles should be idempotent for repeatability
- First Pi must be bootstrapped manually using Raspberry Pi Imager (enable SSH, WiFi, set authorized keys)
- The `disk_burn.yml` playbook runs on `k8sprimary` host, so that node must already exist

**Sensors:**
- Sensor class must be named `Sensor` for dynamic loading via `load_sensors.py:14`
- Hostname normalization: `rpi-XXX` → `rpiXXX` in metrics (see `base_sensor.py:16-20`)
- Non-rpi hostnames default to `coop` in metrics
- Data collection runs on background timer thread that calls `read_data()` at the configured `sample_rate`
- Available sensor attributes: `description`, `path`, `image`, `sample_rate` (default 10s)
- Server version is set from git tags via `run_server.sh:6`

**Kubernetes:**
- Default version: v1.31.4 (latest stable as of configuration)
- Version is configurable via `k8s_major_minor` (e.g., "1.31") and `k8s_version` (e.g., "1.31.4-1.1")
- Repository URL uses `k8s_major_minor` to determine package source
- Ingress controller deployed separately from main stack due to potential Flannel conflicts
- Control plane initialized with `kubeadm init` using command-line options (not config file)
- Bootstrap token from encrypted `roles/k8s/configuration/vars/main.yml` used for worker joins
- kubeconfig copied to root, pi, and localhost users via respective k8s/users roles
