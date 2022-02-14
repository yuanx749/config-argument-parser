[![PyPI version](https://badge.fury.io/py/config-argument-parser.svg)](https://badge.fury.io/py/config-argument-parser)
[![Downloads](https://static.pepy.tech/badge/config-argument-parser/month)](https://pepy.tech/project/config-argument-parser)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/yuanx749/config-argument-parser.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/yuanx749/config-argument-parser/context:python)
[![Maintainability](https://api.codeclimate.com/v1/badges/288bbabbf406afe66e37/maintainability)](https://codeclimate.com/github/yuanx749/config-argument-parser/maintainability)
[![codecov](https://codecov.io/gh/yuanx749/config-argument-parser/branch/dev/graph/badge.svg?token=W34MFRGVMY)](https://codecov.io/gh/yuanx749/config-argument-parser)

# config-argument-parser
A package help automatically create command-line interface from configuration or code.

## Motivation
Configuration files are highly readable and useful for specifying options, but sometimes they are not convenient as command-line interface. However, it requires writing a lot of code to produce a CLI. This module automates the building process, by utilizing the Python standard libraries `configparser` and `argparse`.

The design is to minimize the changes to your original scripts, so as to facilitate maintenance.

## Features
- Only a few extra lines are needed to build a CLI from an existing script.
- The comments are parsed as help messages. (Most libraries do not preserve the comments.)
- Consistent format between configuration and script provides ease of use.

## Usage

### Case 1: create CLI from an object
If you used class to store arguments, create a script `example.py` as below. Default arguments are defined as class attributes, and parsed arguments are stored as instance attributes. The good is that auto-completion can be triggered in editors.
```Python
import configargparser

class Args:
    # Help message of the first argument. Help is optional.
    a_string = "abc"
    a_float = 1.23  # inline comments are omitted
    # Help can span multiple lines.
    # This is another line.
    a_boolean = False
    an_integer = 0

args = Args()

parser = configargparser.ConfigArgumentParser()
parser.parse_obj(args, shorts="sfb")

print(args.a_string)
print(args.a_float)
print(args.a_boolean)
print(args.an_integer)
```
In fact, only the snippet below is added to the original script. Moreover, removing this minimal modification does not affect the original script.
```Python
import configargparser
parser = configargparser.ConfigArgumentParser()
parser.parse_obj(args)
```
Show help, `python example.py -h`:
```
usage: example.py [-h] [-s A_STRING] [-f A_FLOAT] [-b]
                  [--an_integer AN_INTEGER]

optional arguments:
  -h, --help            show this help message and exit
  -s A_STRING, --a_string A_STRING
                        Help message of the first argument. Help is optional.
                        (default: abc)
  -f A_FLOAT, --a_float A_FLOAT
                        (default: 1.23)
  -b, --a_boolean       Help can span multiple lines. This is another line.
                        (default: False)
  --an_integer AN_INTEGER
                        (default: 0)
```
Run with options, for example, `python example.py -b -f 1`:
```
abc
1.0
True
0
```
Note that the values are changed.

### Case 2: create CLI from configuration
If you used configuration file, create an example script `example.py`:
```Python
import configargparser

parser = configargparser.ConfigArgumentParser()
parser.read("config.ini")
# add short options for the first few arguments in order
# default is parser.add_arguments()
parser.add_arguments(shorts="sfb")
parser.parse_args()

print("Configs:", parser.defaults)
print("Args:   ", parser.args)
```
Create a configuration file `config.ini` in the same directory:
```ini
[DEFAULT]
# Help message of the first argument. Help is optional.
a_string = 'abc'
a_float = 1.23  # inline comments are omitted
# Help can span multiple lines.
# This is another line.
a_boolean = False
an_integer = 0
```
Regular run, `python example.py`:
```
Configs: {'a_string': 'abc', 'a_float': 1.23, 'a_boolean': False, 'an_integer': 0}
Args:    {'a_string': 'abc', 'a_float': 1.23, 'a_boolean': False, 'an_integer': 0}
```
Run with options, such as `python example.py -b -f 1`:
```
Configs: {'a_string': 'abc', 'a_float': 1.23, 'a_boolean': False, 'an_integer': 0}
Args:    {'a_string': 'abc', 'a_float': 1.0, 'a_boolean': True, 'an_integer': 0}
```

### Case 3: create CLI from script itself
If you used global variables, create a script `example.py`, with the variables defined at top of file as below:
```Python
# [DEFAULT]
# Help message of the first argument. Help is optional.
a_string = "abc"
a_float = 1.23  # inline comments are omitted
# Help can span multiple lines.
# This is another line.
a_boolean = False
an_integer = 0
# [END]

import configargparser

parser = configargparser.ConfigArgumentParser()
parser.read_py("example.py")
parser.add_arguments(shorts="sfb")
parser.parse_args()

# update global variables
globals().update(parser.args)
print(a_string)
print(a_float)
print(a_boolean)
print(an_integer)
```
Use it as in case 1. For example, `python example.py -b -f 1`:
```
abc
1.0
True
0
```

## Installation
Install from PyPI:
```bash
python -m pip install --upgrade pip
pip install config-argument-parser
```
Alternatively, install from source:
```bash
git clone https://github.com/yuanx749/config-argument-parser.git
cd config-argument-parser
```
then install in development mode:
```bash
git checkout main
python -m pip install --upgrade pip
pip install -e .
```
or:
```bash
git checkout dev
python -m pip install --upgrade pip
pip install -e .[dev]
pre-commit install
```
Uninstall:
```bash
pip uninstall config-argument-parser
```

## Notes
This package uses [Semantic Versioning](https://semver.org/).
