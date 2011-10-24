# $Id: null.py 78909 2010-03-13 10:49:23Z georg.brandl $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
A do-nothing Writer.
"""

from docutils import writers


class Writer(writers.UnfilteredWriter):

    supported = ('null',)
    """Formats this writer supports."""

    config_section = 'null writer'
    config_section_dependencies = ('writers',)

    def translate(self):
        pass
