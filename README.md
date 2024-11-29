# Live Company Data

### Deployment Instructions (single VPS instance)
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
    eval "$(pyenv init -)"
    ```
  - run `source ~/.bashrc`

