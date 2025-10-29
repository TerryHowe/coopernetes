set -e
echo "${1?First argument is password}" >~/.ansiblevault
chmod 600 ~/.ansiblevault

export WORKON_HOME=~/.virtualenvs
mkdir -p $WORKON_HOME
# pip install virtualenvwrapper
# virtualenv -p `which python3` ${WORKON_HOME}/coop
python3 -m venv $WORKON_HOME/coop
source $WORKON_HOME/coop/bin/activate
pip install -r requirements.txt

  git config --global user.email "terrylhowe@gmail.com"
  git config --global user.name "Terry Howe"
