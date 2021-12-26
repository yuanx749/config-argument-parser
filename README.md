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
parser.add_arguments(shorts="snb")  # or parser.add_arguments()
parser.parse_args()

print("Configs:", parser.defaults)
print("Args:", parser.args)
```
Create a configuration file `config.ini` in the same directory:
```ini
[DEFAULT]
# Help message before argument. Optional.
a_string = 'abc'
a_number = 1.23  # inline comments are omitted
# Help can span multiple lines.
# This is another line.
a_boolean = False
```
Show help, `python example.py -h`:
```
usage: example.py [-h] [-s A_STRING] [-n A_NUMBER] [-b]

optional arguments:
  -h, --help            show this help message and exit
  -s A_STRING, --a_string A_STRING
                        Help message before argument. Optional. (default: abc)
  -n A_NUMBER, --a_number A_NUMBER
  -b, --a_boolean       Help can span multiple lines, this is another line.
                        (default: False)
```
Regular run, `python example.py`:
```
Configs: {'a_string': 'abc', 'a_number': 1.23, 'a_boolean': False}
Args: {'a_string': 'abc', 'a_number': 1.23, 'a_boolean': True}
```
Run with options, such as `python example.py -b -n 1`:
```
Configs: {'a_string': 'abc', 'a_number': 1.23, 'a_boolean': False}
Args: {'a_string': 'abc', 'a_number': 1.0, 'a_boolean': True}
```

## Installation
After `git clone` and `cd` into this repo, install:
```bash
python -m pip install --upgrade pip
pip install .
```
Install in development mode:
```bash
pip install -e .[dev]
pre-commit install
```
Uninstall:
```bash
pip uninstall config-argument-parser
```
