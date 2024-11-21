"""A module for building command-line interface from globals."""

import argparse
import inspect


class GlobalArgumentParser:
    """Parser parsing and updating global variables.

    Attributes:
        parser: An `~argparse.ArgumentParser`.
        defaults: A `dict` contains the default arguments.
        args: A `dict` contains the parsed arguments.
    """

    def __init__(self):
        """Initialize GlobalArgumentParser."""
        self._init_parser()
        self.defaults = {}
        self.args = {}
        self.help = {}
        self._globals = {}

    def _init_parser(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    def _read_globals(self, stack=2):
        """Read and parse the attributes of global variables.

        Convert attributes to :attr:`defaults`.
        """
        self._globals = dict(inspect.getmembers(inspect.stack()[stack][0]))["f_globals"]
        self.defaults = {
            k: v
            for k, v in self._globals.items()
            if not k.startswith("_")
            and not inspect.ismodule(v)
            and not inspect.isclass(v)
            and not inspect.isfunction(v)
            and not isinstance(v, GlobalArgumentParser)
        }
        self.help = {k: str(k) for k in self.defaults}

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
        """Convert argument strings to dictionary :attr:`args`.

        Return a `dict` containing arguments.
        """
        namespace = self.parser.parse_args(args)
        self.args = vars(namespace)
        return self.args

    def _change_globals(self):
        """Update global variables."""
        self._globals.update(self.args)

    def parse_globals(self, args=None, *, shorts=""):
        """Parse arguments and update global variables.

        Args:
            args: A list of strings to parse. The default is taken from `sys.argv`.
            shorts: A sequence of short option letters for the leading options.

        Returns:
            A `dict` containing updated arguments.
        """
        self._read_globals()
        self._add_arguments(shorts=shorts)
        self._parse_args(args=args)
        self._change_globals()
        return self.args
