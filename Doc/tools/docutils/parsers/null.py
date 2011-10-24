# $Id: null.py 78909 2010-03-13 10:49:23Z georg.brandl $
# Author: Martin Blais <blais@furius.ca>
# Copyright: This module has been placed in the public domain.

"""A do-nothing parser."""

from docutils import parsers


class Parser(parsers.Parser):

    """A do-nothing parser."""

    supported = ('null',)

    config_section = 'null parser'
    config_section_dependencies = ('parsers',)

    def parse(self, inputstring, document):
        pass
