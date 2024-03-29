:mod:`fnmatch` --- Unix文件名正则匹配
=================================================

.. module:: fnmatch
   :synopsis: Unix shell style filename pattern matching.


.. index:: single: filenames; wildcard expansion

.. index:: module: re

**Source code:** :source:`Lib/fnmatch.py`

--------------

This module provides support for Unix shell-style wildcards, which are *not* the
same as regular expressions (which are documented in the :mod:`re` module).  The
special characters used in shell-style wildcards are:

fnmatch 实现了 shell patterns 表匹配字符串或文件名. 


+------------+------------------------------------+
| Pattern    | Meaning                            |
+============+====================================+
| ``*``      | matches everything                 |
+------------+------------------------------------+
| ``?``      | matches any single character       |
+------------+------------------------------------+
| ``[seq]``  | matches any character in *seq*     |
+------------+------------------------------------+
| ``[!seq]`` | matches any character not in *seq* |
+------------+------------------------------------+

.. index:: module: glob

Note that the filename separator (``'/'`` on Unix) is *not* special to this
module.  See module :mod:`glob` for pathname expansion (:mod:`glob` uses
:func:`fnmatch` to match pathname segments).  Similarly, filenames starting with
a period are not special for this module, and are matched by the ``*`` and ``?``
patterns.


.. function:: fnmatch(filename, pattern)

   Test whether the *filename* string matches the *pattern* string, returning
   :const:`True` or :const:`False`.  If the operating system is case-insensitive,
   then both parameters will be normalized to all lower- or upper-case before
   the comparison is performed.  :func:`fnmatchcase` can be used to perform a
   case-sensitive comparison, regardless of whether that's standard for the
   operating system.

   This example will print all file names in the current directory with the
   extension ``.txt``::

      import fnmatch
      import os

      for file in os.listdir('.'):
          if fnmatch.fnmatch(file, '*.txt'):
              print(file)


.. function:: fnmatchcase(filename, pattern)

   Test whether *filename* matches *pattern*, returning :const:`True` or
   :const:`False`; the comparison is case-sensitive.


.. function:: filter(names, pattern)

   Return the subset of the list of *names* that match *pattern*. It is the same as
   ``[n for n in names if fnmatch(n, pattern)]``, but implemented more efficiently.


.. function:: translate(pattern)

   Return the shell-style *pattern* converted to a regular expression.

   Be aware there is no way to quote meta-characters.

   Example:

      >>> import fnmatch, re
      >>>
      >>> regex = fnmatch.translate('*.txt')
      >>> regex
      '.*\\.txt$'
      >>> reobj = re.compile(regex)
      >>> reobj.match('foobar.txt')
      <_sre.SRE_Match object at 0x...>


.. seealso::

   Module :mod:`glob`
      Unix shell-style path expansion.

