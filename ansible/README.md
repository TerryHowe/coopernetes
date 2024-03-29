# Coopernetes Deployment

Coopernetes deployment uses Ansible to automate deployment. Just like chickens,
our Raspberry Pis should be livestock, not pets. Make deployment to them easy
so we are not so attached when they get killed by a bear.

## Development Setup

The ansible configuration resides in `ansible.cfg` in the root of the repository.

1.  Create a password file containing the Ansible vault password in text on a
    single line at:

   ```
   echo 'yourpassword' >~/.ansiblevault
   chmod 600 ~/.ansiblevault
   ```

1. Make sure you have an ssh key at `~/.ssh/id_rsa`

1. Create a Python virtualenv
   ```
   pip install virtualenvwrapper
   export WORKON_HOME=~/.virtualenvs
   mkdir -p $WORKON_HOME
   virtualenv -p /usr/local/bin/python3 ${WORKON_HOME}/coop
   ```

1. Add to your shell rc script:
   ```
   if command -v pyenv 1>/dev/null 2>&1; then
     eval "$(pyenv init -)"
   fi
   export WORKON_HOME=~/.virtualenvs
   source ~/.pyenv/versions/3.7.3/bin/virtualenvwrapper.sh
   workon coop
   ```

1. Install the required software:
   ```
   pip install -r requirements.txt
   ```

1. Copy your ssh public key to the targets. The `sshable` role will prepare
   a mounted Raspbian disk enabling ssh and copying ssh keys. You need to
   copy your public key into the `sshable` vars so it will be available on
   the raspberries.

## Playbooks

Several different playbooks have been created to fully automate the deployment
of Coopernetes. Many of these playbooks are generic and not strictly related to
this project.

The first step in deploying Coopernetes to a Raspberry is burning a disk. This
playbook assumes you already have a Raspberry setup to run the playbook, so
there is a bit of a chicken or the egg situation. You will need to first
create a disk with the Raspberry Pi Imager, enable ssh, wifi and set your
public key in the authorized keys for the user pi. These are exactly the
steps that this playbook automates. There is currently support for
`arch=arm32` and `arch=arm64`:
```
ansible-playbook -v -e arch=arm32 playbooks/disk_burn.yml
```
It is expected that you are burning disks on you `k8sprimary` host. See the
`host.ini` file and update it with your IP address for that node.  The next
step is putting the disk in a Raspberry Pi you want to configure, booting it
and running the playbook on it associated with the desired function.

### Sensors

Sensor playbooks are named after the shorthand name of the associated sensor.
For example, if you had a US-100 distance sensor, you would run:
```
ansible-playbook -v playbooks/us100.yml
```

### Kubernetes

If you are creating a node for the Kubernetes cluster, start by running the
k8sinstall playbook. This playbook is for control plane and worker nodes. It
will make changes to the operating system required to run Kubernetes, it
will install containerd and it will install Kubernetes. This example targets
one host:

```
ansible-playbook -v -e target=172.27.27.159 playbooks/k8sinstall.yml
```

After install Kubernetes, you can either configure a node to be a control
plane or a worker with the `k8sprimary.yml` or `k8sworker.yml` playbooks.

```
ansible-playbook -v playbooks/k8sworker.yml
```

### Ingress

I suspected that a conflict between the Ingress controller and Flannel
was causing both of them to fail, so I broke out the Ingress controller
into another playbook:

```
ansible-playbook -v playbooks/ingress-nginx.yml
```

### Prometheus, Grafana, and Alert Manager

Once you have your Kubernetes cluster running, you need to start the monitoring
software Prometheus, Grafana and Alert Manager.

```
ansible-playbook -v playbooks/prometheus.yml
```
