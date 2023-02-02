"""A module for building command-line interface from file."""

import argparse
import configparser
import inspect
import re
from ast import literal_eval


class ConfigArgumentParser:
    """Wrapper combining ConfigParser and ArgumentParser.

    Attributes:
        config: A configparser.ConfigParser.
        parser: A argparse.ArgumentParser.
        defaults: A dict contains the default arguments.
        namespace: An object returned by `parser.parse_args`.
        args: A dict contains the parsed arguments.
        help: A dict contains the help messages.
    """

    def __init__(self):
        """Initialize ConfigArgumentParser."""
        self._init_config()
        self._init_parser()
        self.defaults = {}
        self.namespace = object()
        self.args = {}
        self.help = {}
        self._comment_prefix = "#"
        self._sect_header_default = self.config.SECTCRE
        self._sect_header_py = re.compile(r"# \[(?P<header>.+)\]")

    def _init_config(self):
        self.config = configparser.ConfigParser(
            allow_no_value=True, delimiters="=", comment_prefixes=";", strict=False
        )
        self.config.optionxform = lambda x: x  # override the default

    def _convert_defaults(self):
        """Convert configuration to `self.defaults` and parse the comments into `self.help`."""
        msg_lst = []
        for key, value in self.config.defaults().items():
            if key.startswith(self._comment_prefix):
                msg = key.lstrip(self._comment_prefix)
                msg = msg.strip()
                msg_lst.append(msg)
            else:
                self.defaults[key] = literal_eval(value)
                self.help[key] = self._join_msg(msg_lst)
                msg_lst = []

    @staticmethod
    def _join_msg(msg_lst):
        if msg_lst:
            return " ".join(msg_lst)
        # A non-empty string is needed to show the default in help.
        return " "

    def read(self, filenames):
        """Read and parse a filename or an iterable of filenames.

        Return list of successfully read files.
        """
        f_lst = self.config.read(filenames)
        self._convert_defaults()
        return f_lst

    def read_string(self, string):
        """Read configuration from a given string."""
        self.config.read_string(string)
        self._convert_defaults()

    def read_py(self, filename):
        """Read and parse a filename of Python script."""
        self.config.SECTCRE = self._sect_header_py
        self.config.read(filename)
        self._convert_defaults()
        self.config.SECTCRE = self._sect_header_default

    def _add_arguments(self, shorts=""):
        """Add arguments to parser according to the configuration.

        Args:
            shorts: A sequence of short option letters for the leading options.
        """
        boolean_to_action = {True: "store_false", False: "store_true"}
        for i, (option, value) in enumerate(self.defaults.items()):
            flags = [f"--{option.replace('_', '-')}"]
            if i < len(shorts):
                flags.insert(0, f"-{shorts[i]}")
            if isinstance(value, bool):
                self.parser.add_argument(
                    *flags,
                    action=boolean_to_action[value],
                    help=self.help[option],
                )
            else:
                self.parser.add_argument(
                    *flags, default=value, type=type(value), help=self.help[option]
                )

    def _init_parser(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    def _parse_args(self, args=None):
        """Convert argument strings to dictionary `self.args`.

        Return a dictionary containing arguments.
        """
        self.namespace = self.parser.parse_args(args)
        self.args = vars(self.namespace)
        return self.args

    def parse_args(self, args=None, *, shorts=""):
        """Add arguments to parser and parse arguments.

        Args:
            args: A list of strings to parse. The default is taken from `sys.argv`.
            shorts: A sequence of short option letters for the leading options.

        Returns:
            A dictionary containing arguments.
        """
        self._add_arguments(shorts=shorts)
        self._parse_args(args=args)
        return self.args

    def _read_obj(self, obj):
        """Read and parse the attributes of an object."""
        source_lines, _ = inspect.getsourcelines(type(obj))
        source_lines[0] = "[DEFAULT]\n"
        self.config.read_string("".join(source_lines))
        self._convert_defaults()

    def _change_obj(self, obj):
        """Update object attributes."""
        obj.__dict__.update(self.args)

    def parse_obj(self, obj, args=None, *, shorts=""):
        """Parse arguments and update object attributes.

        Args:
            obj: An object with attributes as default arguments.
            args: A list of strings to parse. The default is taken from `sys.argv`.
            shorts: A sequence of short option letters for the leading options.

        Returns:
            A dictionary containing updated arguments.
        """
        self._read_obj(obj)
        self._add_arguments(shorts=shorts)
        self._parse_args(args=args)
        self._change_obj(obj)
        return self.args
