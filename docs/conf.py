# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).parent.parent)]

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import configargparser

project = 'config-argument-parser'
copyright = '2021, Xiao Yuan'
author = 'Xiao Yuan'
release = configargparser.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

default_role = 'obj'
add_module_names = False
toc_object_entries_show_parents = 'hide'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

html_theme_options = {
    'top_of_page_button': None,
}
html_title = project

# MyST-Parser

myst_heading_anchors = 3

# Napoleon settings

napoleon_google_docstring = True
napoleon_numpy_docstring = False

# autodoc

autodoc_member_order = 'bysource'

# intersphinx

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}
