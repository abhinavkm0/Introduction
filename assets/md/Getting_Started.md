# Environment Setup

We will be working inside WSL

First, install wsl

```
wsl --install
```

Install the Ubuntu distro

```
wsl --install -d Ubuntu
```

Set the default version to WSL2

```
wsl --set-default-version 2
```

### WSL2

Now you can enter wsl to open a shell

![alt text](../images/wsl2_shell.png)

### Docker Desktop

Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

Now, enable WSL2 integration 
![alt text](../images/docker_wsl2.png)

### Create SSH Key

Create an SSH Key 

```
ssh-keygen -t rsa -b 4096 -C "email@thoughtminds.io"
```

Add to identity

```
  237  ssh-add ~/.ssh/file_name
```

Now copy contents of the `.pub` file to GitHub SSH Keys

![alt text](../images/ssh_key.png)


### Install pyenv

```
curl -fsSL https://pyenv.run | bash
```

Refer [this](https://github.com/pyenv/pyenv?tab=readme-ov-file#b-set-up-your-shell-environment-for-pyenv) for setup

Zsh users can do this

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc
```

Now you can install a python version using pyenv

```
pyenv install 3.10.5
```

If this throws an error install gcc

```
sudo apt install -y software-properties-common
```

I recommend setting a python version to be the default

```
pyenv global 3.10.5
```

### Install pipenv

```
python -m pip install pipenv
```

To initialize simply run

```
pipenv install
```

Once you have a Pipfile, start installing packages

Eg:

```
pipenv install tqdm
```