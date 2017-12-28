This is a simple application that processes self-admin data.

To use, create a virtual environment and install `requirements.txt` (needed fox XLSX writing).

Then, simply run:

- `$ python3 main.py <absolute_path_to_root>`

Your output will then be in the supplied root.

To create a virtual env:

- `$ cd ~/Desktop`
- `$ git clone https://github.com/timoneal91/msn-dreadd.git`
- `$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
- `$ echo 'export PATH="$PATH:/usr/local/bin"' >> ~/.bash_profile`
- `$ brew install python3`
- `$ brew postinstall python3`
- `$ pip3 install -r requirements.txt`