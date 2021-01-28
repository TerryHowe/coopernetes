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
     a mounted Raspbian disk enabling ssh and copying ssh keys.

