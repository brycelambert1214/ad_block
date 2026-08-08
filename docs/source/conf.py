# Configuration file for the Sphinx documentation builder.

import os
import sys


# Add project root to Python path
sys.path.insert(
    0,
    os.path.abspath("../..")
)


# -----------------------------------------------------------------------------
# Project information
# -----------------------------------------------------------------------------

project = "ad_block"
copyright = "2026, Bryce Lambert"
author = "Bryce Lambert"

release = "0.1.0"


# -----------------------------------------------------------------------------
# Extensions
# -----------------------------------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]


# -----------------------------------------------------------------------------
# General configuration
# -----------------------------------------------------------------------------

templates_path = ["_templates"]

exclude_patterns = []


# NumPy-style docstrings
napoleon_numpy_docstring = True
napoleon_google_docstring = False


# -----------------------------------------------------------------------------
# Autodoc behavior
# -----------------------------------------------------------------------------

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "show-inheritance": True,
}


autodoc_typehints = "description"


# -----------------------------------------------------------------------------
# HTML
# -----------------------------------------------------------------------------

html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]