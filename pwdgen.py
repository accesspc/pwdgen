#!/usr/bin/python3
from itertools import islice
from pathlib import Path
import os.path
import subprocess
import yaml

# Default config options
config = {
    "charlist": "/usr/local/lib/pwdgen/character-lists/ascii.lst",
    "wordlist": "/usr/local/lib/pwdgen/wordlists/crr.lst",
    "capital_mode": "first",
    #"padding_before_char": 0,
    #"padding_before_num": 0,
    "padding_sep_char": 1,
    "padding_after_num": 2,
    "padding_after_char": 2,
    "length": 2,
    "count": 5
}

def capitalize(word):
    if config["capital_mode"] == "first":
        return word.capitalize()
    elif config["capital_mode"] == "all":
        return word.upper()
    return word

def generate_from_list(flist):
    num = generate_num(wccount(flist))
    with open(flist) as f:
        try:
            if num > 0:
                line = next(islice(f, num - 1, num))
            else:
                line = f.readline()
        except StopIteration:
            print('File %s has less than %s lines' % (flist, num))
    return line.strip()

def generate_num(max):
    out = subprocess.Popen([
            'od', 
            '--address-radix=n', 
            '--read-bytes=3', 
            '-i', 
            '/dev/urandom'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    ).communicate()[0].decode("utf-8")
    return int(out) % (max + 1)

def generate_password():
    sep = ""
    if config["length"] > 1:
        sep = generate_from_list(config["charlist"])

    pwd = ""
    for i in range(1, config["length"] + 1):
        pwd+= capitalize(generate_from_list(config["wordlist"]))
        if i < config["length"]:
            pwd+= sep * config["padding_sep_char"]

    if config["padding_after_num"] > 0:
        for i in range(0, config["padding_after_num"]):
            pwd+= str(generate_num(9))

    if config["padding_after_char"] > 0:
        pwd+= generate_from_list(config["charlist"]) * config["padding_after_char"]
    
    return pwd

def wccount(filename):
    out = subprocess.Popen(['wc', '-l', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT).communicate()[0]
    return int(out.partition(b' ')[0])

# Read it from ~/.pwdgen.yml if exists
homedir = os.path.expanduser("~")
config_file = Path("%s/.pwdgen.yml" % homedir)

if config_file.is_file():
    cfg = yaml.safe_load(open(config_file)) or {}
    for k, v in cfg.items():
        config[k] = v

# Parse command line arguments
## TBD

# Do config checks
## TBD

# Generate the actual password
for i in range(0, config["count"]):
    pwd = generate_password()
    print(pwd)
