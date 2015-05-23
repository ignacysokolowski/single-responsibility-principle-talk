# -*- coding: utf-8 -*-
"""SRP talk slides build configuration file.

This file is execfile()d with the current directory set to its containing dir.

"""
import sphinx_readable_theme


# -- General configuration ----------------------------------------------------

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Single Responsibility Principle'
copyright = u'2015, Ignacy Sokołowski'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output --------------------------------------------------

extensions = ['hieroglyph']
slide_theme_path = ['_themes']
slide_theme = 'readable'
# autoslides = False

# Output file base name for HTML help builder.
html_theme_path = [sphinx_readable_theme.get_html_theme_path()]
html_theme = 'readable'
htmlhelp_basename = 'srpdoc'


# -- Options for manual page output -------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(
    'index',
    project,
    project,
    [u'Ignacy Sokołowski'],
    1
)]
