"""A package to help automatically create command-line interface from configuration or code."""

__version__ = "1.5.0"

from .cap import ConfigArgumentParser
from .gap import GlobalArgumentParser
from .tap import TypeArgumentParser

__all__ = ["ConfigArgumentParser", "TypeArgumentParser", "GlobalArgumentParser"]
