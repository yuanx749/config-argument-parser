"""A module for building command-line interface from dataclass."""

import argparse
import inspect


class TypeArgumentParser:
    """Parser parsing and updating a dataclass object.

    Attributes:
        parser: A argparse.ArgumentParser.
        defaults: A dict contains the default arguments.
        args: A dict contains the parsed arguments.
        help: A dict contains the help messages.
    """

    def __init__(self):
        """Initialize TypeArgumentParser."""
        self._init_parser()
        self.defaults = {}
        self.args = {}
        self.help = {}

    def _init_parser(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    def _read_obj(self, obj: object):
        """Read and parse the attributes of a dataclass object.

        Convert attributes to `self.defaults` and parse the comments into `self.help`.
        """
        source_lines, _ = inspect.getsourcelines(type(obj))
        self.defaults = obj.__dict__.copy()
        msg_lst = []
        args_iter = iter(self.defaults.keys())
        for line in source_lines[1:]:
            if line.strip().startswith("#"):
                msg = line.lstrip(" #").strip()
                msg_lst.append(msg)
            else:
                self.help[next(args_iter)] = self._join_msg(msg_lst)
                msg_lst = []

    @staticmethod
    def _join_msg(msg_lst):
        if msg_lst:
            return " ".join(msg_lst)
        # A non-empty string is needed to show the default in help.
        return " "

    def _add_arguments(self, shorts=""):
        """Add arguments to parser according to the default.

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

    def _parse_args(self, args=None):
        """Convert argument strings to dictionary `self.args`.

        Return a dictionary containing arguments.
        """
        namespace = self.parser.parse_args(args)
        self.args = vars(namespace)
        return self.args

    def _change_obj(self, obj):
        """Update object attributes."""
        obj.__dict__.update(self.args)

    def parse_obj(self, obj, args=None, *, shorts=""):
        """Parse arguments and update object attributes.

        Args:
            obj: A dataclass object with attributes as default arguments.
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
