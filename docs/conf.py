# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:

# -- Project information -----------------------------------------------------
import os
import sys

current_dir = os.path.dirname(__file__)
target_dir = os.path.abspath(os.path.join(current_dir, "../entsopy"))
sys.path.insert(0, target_dir)


project = "entsopy"
copyright = "2023, lorenzoxi"
author = "lorenzoxi"
release = "0.1"

# -- General configuration ---------------------------------------------------

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.viewcode"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_static_path = ["_static"]
