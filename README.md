# Live Company Data

### Deployment Instructions (single Ubuntu VPS instance) (WIP)
- get VPS instance
- ssh in
- create new user w/ sudo privileges
  - run `adduser <username>` to add user
  - run `usermod -aG sudo <username>` to give user sudoer privileges
  - make sure new user can login
    - Two options:
      - generate key pair + put public key in authorized key files on remote host (you can do it manually or via `ssh-copy-id`, but you want that public key to end up in `~/.ssh/authorized_keys`
      - enabled password authentication by setting `PasswordAuthentication` to `yes` in your `sshd_config` file (usually located somewhere like `/etc/ssh/sshd_config`)
- disable ssh root login
  - set `PermitRootLogin` to `no` in your `sshd_config` file (usually in a location like `/etc/ssh/sshd_config`
  - restart ssh service (`systemctl restart <service name>`)
    - service is usually named `ssh` or `sshd`, you can easily check by running `systemctl -l --type service --all` and piping that into grep
- install pyenv
  - run `curl https://pyenv.run | bash`
  - add the following to the end of your `.bashrc` file:
    ```
    export PYENV_ROOT="$HOME/.pyenv"
    [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init --path)"
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
- copy this repo to the VPS instance, you can do whatever works for you (git clone, scp, rsync, whatever)
- create and activate a python virtual environment w/ pyenv
  - run `pyenv virtualenv 3.10.0 <env name>`
  - run `pyenv activate <env name>`
