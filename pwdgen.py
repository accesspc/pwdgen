#!/usr/bin/python3
from itertools import islice
from pathlib import Path
import argparse
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
parser = argparse.ArgumentParser(description="Generate some passwords.")
parser.add_argument("-c", "--count", metavar="#", type=int, help="Password count (1..20)")
parser.add_argument("-l", "--length", metavar="#", type=int, help="Word count (1..20)")
parser.add_argument("-x", "--padding_sep_char", metavar="#", type=int, help="Padding separator character count (0..10)")
parser.add_argument("-y", "--padding_after_num", metavar="#", type=int, help="Padding after number count (0..10)")
parser.add_argument("-z", "--padding_after_char", metavar="#", type=int, help="Padding after character count (0..10)")
parser.add_argument("--capital_mode", choices=["first", "all", "none"], help="Capitalization mode")
parser.add_argument("--charlist", metavar="FILE", type=argparse.FileType('r'), help="Character list file")
parser.add_argument("--wordlist", metavar="FILE", type=argparse.FileType('r'), help="Wordlist list file")

args = parser.parse_args()

if args.count is not None:
    if args.count in range(1, 21):
        config["count"] = args.count
    else:
        parser.print_usage()
        parser.exit(status=1)

if args.length is not None:
    if args.length in range(1, 21):
        config["length"] = args.length
    else:
        parser.print_usage()
        parser.exit(status=1)

if args.capital_mode is not None:
    config["capital_mode"] = args.capital_mode

if args.padding_sep_char is not None:
    if args.padding_sep_char in range(0, 11):
        config["padding_sep_char"] = args.padding_sep_char
    else:
        parser.print_usage()
        parser.exit(status=1)

if args.padding_after_num is not None:
    if args.padding_after_num in range(0, 11):
        config["padding_after_num"] = args.padding_after_num
    else:
        parser.print_usage()
        parser.exit(status=1)

if args.padding_after_char is not None:
    if args.padding_after_char in range(0, 11):
        config["padding_after_char"] = args.padding_after_char
    else:
        parser.print_usage()
        parser.exit(status=1)

if args.charlist is not None:
    config["charlist"] = args.charlist

if args.wordlist is not None:
    config["wordlist"] = args.wordlist

# Generate the actual password
for i in range(0, config["count"]):
    pwd = generate_password()
    print(pwd)
