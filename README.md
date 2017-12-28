This is a simple application that processes self-admin data.

To use, create a virtual environment and install `requirements.txt` (needed fox XLSX writing).

Then, simply run:

`$ python3 main.py <absolute_path_to_root>`

Your output will then be in the supplied root.

To create a virtual env:

- `$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
- `$ brew install python3`
- `$ virtualenv -p python3 ~/.virtualenvs/testenv`
- `$ source ~/.virtualenvs/testenv/bin/activate`
- `$ pip3 install -r requirements.txt`