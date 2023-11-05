"""A package help automatically create command-line interface from configuration or code."""

__version__ = "1.2.2"

from .cap import ConfigArgumentParser
from .tap import TypeArgumentParser

__all__ = ["ConfigArgumentParser", "TypeArgumentParser"]
