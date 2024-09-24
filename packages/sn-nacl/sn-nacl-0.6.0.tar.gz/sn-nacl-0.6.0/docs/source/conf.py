# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sphinx_rtd_theme
import sphinx_gallery

project = 'NaCl'
copyright = '2023, Nicolas Regnault, Guy Augarde, Marc Betoule, Seb Bongard'
author = 'Nicolas Regnault, Guy Augarde, Marc Betoule, Seb Bongard'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.mathjax',
    'sphinxemoji.sphinxemoji',
    'm2r2',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# html_theme = 'alabaster'
# html_theme = "sphinx_book_theme"
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    # 'show_toc_level': 2,
    # 'repository_url': 'https://gitlab.in2p3.fr/cosmo/sn-nacl',
    # 'use_repository_button': True,     # add a "link to repository" button
}

html_static_path = ['_static']
