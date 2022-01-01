# config-argument-parser
A module for building command-line interface from configuration.

## Motivation
Configuration files are highly readable and useful for specifying options, but sometimes they are not convenient as command-line interface. However, it requires writing a lot of code to produce a CLI. This module automates the building process, by utilizing the Python standard libraries `configparser` and `argparse`. It has features below.

- The comments are parsed as help messages. (Most libraries do not preserve the comments.)
- Consistent format between configuration and script provides ease of use.
- Only a few lines are needed to build a CLI.

## Usage
Create an example script `example.py`:
```python
import args

parser = args.ConfigArgumentParser()
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
