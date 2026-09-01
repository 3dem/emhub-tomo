# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'EMhub-Tomo'
copyright = '2026, Jose Miguel De la Rosa Trevin, Daniel Marchan'
author = 'Jose Miguel De la Rosa Trevin, Daniel Marchan'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

extensions = [
    'myst_parser'
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['custom.css']

# Show only the logo in the sidebar, not the "<project> documentation"
# text next to/below it (the logo already carries the project name).
html_theme_options = {
    'sidebar_hide_name': True,
}

# Displayed at the top of the Furo sidebar (above the search box). The
# "-top" image is the tall/stacked variant of the logo (icon over
# "EMhub Tomo"), which fits the narrow sidebar much better than the wide
# horizontal banner variant used for other purposes.
html_logo = 'images/emhub-tomo-logo-top.png'
