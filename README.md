# Live Company Data

### Deployment Instructions (single Ubuntu VPS instance)
Note: this deployment is designed to be self-recovering in case of server failure. This has been tested on a 1 vcpu 1 gb ram 25 gb ssd Digital Ocean Ubunutu 24.0.4 LTS droplet.
- get VPS instance
- ssh in
- create new user w/ sudo privileges
  - run `sudo adduser <username>` to add user
  - run `sudo usermod -aG sudo <username>` to give user sudoer privileges
  - login as the new user    
    - Two options:
      - generate key pair + put public key in authorized key files on remote host (you can do it manually or via `ssh-copy-id`, but you want that public key to end up in `~/.ssh/authorized_keys`
      - enabled password authentication by setting `PasswordAuthentication` to `yes` in your `sshd_config` file (usually located somewhere like `/etc/ssh/sshd_config`)
- disable ssh root login
  - set `PermitRootLogin` to `no` in your `sshd_config` file (usually in a location like `/etc/ssh/sshd_config`
  - also doesn't hurt to set `PermitEmptyPasswords` to `no` in your `sshd_config`
  - restart ssh service (`sudo systemctl restart <service name>`)
    - service is usually named `ssh` or `sshd`, you can easily check by running `systemctl -l --type service --all` and piping that into grep
- install pyenv
  - run `curl https://pyenv.run | bash`
  - add the following to the end of your `.bashrc` file:
    ```
    export PYENV_ROOT="$HOME/.pyenv"
    [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
    # export PYENV_VIRTUALENV_DISABLE_PROMPT=1
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    ```
  - run `source ~/.bashrc`
- install build-essential
  - run `sudo apt-get install build-essential`
- install dependencies to build python from source
  - run `sudo apt install libssl-dev libffi-dev libncurses5-dev zlib1g zlib1g-dev libreadline-dev libbz2-dev libsqlite3-dev make gcc`
- install python 3.10.0
  - run `pyenv install 3.10.0`
  - if you run into errors when installing python versions w/ pyenv, a couple notes:
    - pyenv builds versions from source, which is why we installed `build-essential` and the long list of dependencies
    - you shouldn't run into actual major build issues with all the right dependencies installed, but if you do, pyenv will dump log files and patches to `/tmp` so make sure to keep that directory clear because it will fill up fast and you may run out of space
- set python 3.10.0 as the global python version
  - run `pyenv global 3.10.0`
- copy this repo to the VPS instance, you can do whatever works for you (git clone, scp, rsync, whatever)
- create and activate a python virtual environment
  - run `python3 -m venv ~/envs/live_company_data`
  - run `source ~/envs/live_company_data/bin/activate`
- install requirements
  - run `cd ~/live_company_data && pip3 install -r requirements.txt` 
- copy the service files to `/etc/systemd/system/`
  - run `sudo cp services/* /etc/systemd/system/`
- reload the systemd daemon
  - run `sudo systemctl daemon-reload`
- enable and start the services
  - run `sudo systemctl enable live0.service`
  - run `sudo systemctl start live0.service`
  - run `sudo systemctl enable live1.service`
  - run `sudo systemctl start live1.service`
- check the status of the services
  - run `sudo systemctl status live0.service`
  - run `sudo systemctl status live1.service`
- install nginx
  - run `sudo apt install nginx`
- copy the nginx config file (`nginx/live.conf`) to `/etc/nginx/sites-available/`
- create symbolic link to the config file in `/etc/nginx/sites-enabled/`
  - run `sudo ln -s /etc/nginx/sites-available/live.conf /etc/nginx/sites-enabled/`
- remove the default nginx config file
  - run `sudo rm /etc/nginx/sites-enabled/default`
- verify the config file
  - run `sudo nginx -t`
- restart nginx
  - run `sudo systemctl daemon-reload`
  - run `sudo systemctl restart nginx`
- enable and start ufw
  - run `sudo ufw enable`
  - run `sudo ufw allow 'Nginx Full'`
  - run `sudo ufw allow ssh`
  - run `sudo ufw status verbose` to see what ports are open
- make sure `sudo su` requires a password
  - run `sudo vim /etc/pam.d/su`
  - comment out `auth required pam_wheel.so` and `auth sufficient pam_rootok.so`
  - uncomment `auth required pam_wheel.so use_uid`
