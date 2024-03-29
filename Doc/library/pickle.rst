:mod:`pickle` --- Python的对象序列化
=============================================

.. index::
   single: persistence
   pair: persistent; objects
   pair: serializing; objects
   pair: marshalling; objects
   pair: flattening; objects
   pair: pickling; objects

.. module:: pickle
   :synopsis: Convert Python objects to streams of bytes and back.
.. sectionauthor:: Jim Kerr <jbkerr@sr.hp.com>.
.. sectionauthor:: Barry Warsaw <barry@zope.com>


The :mod:`pickle` module implements a fundamental, but powerful algorithm for
serializing and de-serializing a Python object structure.  "Pickling" is the
process whereby a Python object hierarchy is converted into a byte stream, and
"unpickling" is the inverse operation, whereby a byte stream is converted back
into an object hierarchy.  Pickling (and unpickling) is alternatively known as
"serialization", "marshalling," [#]_ or "flattening", however, to avoid
confusion, the terms used here are "pickling" and "unpickling"..

.. warning::

   The :mod:`pickle` module is not intended to be secure against erroneous or
   maliciously constructed data.  Never unpickle data received from an untrusted
   or unauthenticated source.


Relationship to other Python modules
------------------------------------

The :mod:`pickle` module has an transparent optimizer (:mod:`_pickle`) written
in C.  It is used whenever available.  Otherwise the pure Python implementation is
used.

Python has a more primitive serialization module called :mod:`marshal`, but in
general :mod:`pickle` should always be the preferred way to serialize Python
objects.  :mod:`marshal` exists primarily to support Python's :file:`.pyc`
files.

The :mod:`pickle` module differs from :mod:`marshal` in several significant ways:

* The :mod:`pickle` module keeps track of the objects it has already serialized,
  so that later references to the same object won't be serialized again.
  :mod:`marshal` doesn't do this.

  This has implications both for recursive objects and object sharing.  Recursive
  objects are objects that contain references to themselves.  These are not
  handled by marshal, and in fact, attempting to marshal recursive objects will
  crash your Python interpreter.  Object sharing happens when there are multiple
  references to the same object in different places in the object hierarchy being
  serialized.  :mod:`pickle` stores such objects only once, and ensures that all
  other references point to the master copy.  Shared objects remain shared, which
  can be very important for mutable objects.

* :mod:`marshal` cannot be used to serialize user-defined classes and their
  instances.  :mod:`pickle` can save and restore class instances transparently,
  however the class definition must be importable and live in the same module as
  when the object was stored.

* The :mod:`marshal` serialization format is not guaranteed to be portable
  across Python versions.  Because its primary job in life is to support
  :file:`.pyc` files, the Python implementers reserve the right to change the
  serialization format in non-backwards compatible ways should the need arise.
  The :mod:`pickle` serialization format is guaranteed to be backwards compatible
  across Python releases.

Note that serialization is a more primitive notion than persistence; although
:mod:`pickle` reads and writes file objects, it does not handle the issue of
naming persistent objects, nor the (even more complicated) issue of concurrent
access to persistent objects.  The :mod:`pickle` module can transform a complex
object into a byte stream and it can transform the byte stream into an object
with the same internal structure.  Perhaps the most obvious thing to do with
these byte streams is to write them onto a file, but it is also conceivable to
send them across a network or store them in a database.  The module
:mod:`shelve` provides a simple interface to pickle and unpickle objects on
DBM-style database files.


Data stream format
------------------

.. index::
   single: XDR
   single: External Data Representation

The data format used by :mod:`pickle` is Python-specific.  This has the
advantage that there are no restrictions imposed by external standards such as
XDR (which can't represent pointer sharing); however it means that non-Python
programs may not be able to reconstruct pickled Python objects.

By default, the :mod:`pickle` data format uses a compact binary representation.
The module :mod:`pickletools` contains tools for analyzing data streams
generated by :mod:`pickle`.

There are currently 4 different protocols which can be used for pickling.

* Protocol version 0 is the original human-readable protocol and is
  backwards compatible with earlier versions of Python.

* Protocol version 1 is the old binary format which is also compatible with
  earlier versions of Python.

* Protocol version 2 was introduced in Python 2.3.  It provides much more
  efficient pickling of :term:`new-style class`\es.

* Protocol version 3 was added in Python 3.0.  It has explicit support for
  bytes and cannot be unpickled by Python 2.x pickle modules.  This is
  the current recommended protocol, use it whenever it is possible.

Refer to :pep:`307` for information about improvements brought by
protocol 2.  See :mod:`pickletools`'s source code for extensive
comments about opcodes used by pickle protocols.


Module Interface
----------------

To serialize an object hierarchy, you first create a pickler, then you call the
pickler's :meth:`dump` method.  To de-serialize a data stream, you first create
an unpickler, then you call the unpickler's :meth:`load` method.  The
:mod:`pickle` module provides the following constant:


.. data:: HIGHEST_PROTOCOL

   The highest protocol version available.  This value can be passed as a
   *protocol* value.

.. data:: DEFAULT_PROTOCOL

   The default protocol used for pickling.  May be less than HIGHEST_PROTOCOL.
   Currently the default protocol is 3; a backward-incompatible protocol
   designed for Python 3.0.


The :mod:`pickle` module provides the following functions to make the pickling
process more convenient:

.. function:: dump(obj, file, protocol=None, \*, fix_imports=True)

   Write a pickled representation of *obj* to the open :term:`file object` *file*.
   This is equivalent to ``Pickler(file, protocol).dump(obj)``.

   The optional *protocol* argument tells the pickler to use the given protocol;
   supported protocols are 0, 1, 2, 3.  The default protocol is 3; a
   backward-incompatible protocol designed for Python 3.0.

   Specifying a negative protocol version selects the highest protocol version
   supported.  The higher the protocol used, the more recent the version of
   Python needed to read the pickle produced.

   The *file* argument must have a write() method that accepts a single bytes
   argument.  It can thus be an on-disk file opened for binary writing, a
   :class:`io.BytesIO` instance, or any other custom object that meets this
   interface.

   If *fix_imports* is True and *protocol* is less than 3, pickle will try to
   map the new Python 3.x names to the old module names used in Python 2.x,
   so that the pickle data stream is readable with Python 2.x.

.. function:: dumps(obj, protocol=None, \*, fix_imports=True)

   Return the pickled representation of the object as a :class:`bytes`
   object, instead of writing it to a file.

   The optional *protocol* argument tells the pickler to use the given protocol;
   supported protocols are 0, 1, 2, 3.  The default protocol is 3; a
   backward-incompatible protocol designed for Python 3.0.

   Specifying a negative protocol version selects the highest protocol version
   supported.  The higher the protocol used, the more recent the version of
   Python needed to read the pickle produced.

   If *fix_imports* is True and *protocol* is less than 3, pickle will try to
   map the new Python 3.x names to the old module names used in Python 2.x,
   so that the pickle data stream is readable with Python 2.x.

.. function:: load(file, \*, fix_imports=True, encoding="ASCII", errors="strict")

   Read a pickled object representation from the open :term:`file object` *file*
   and return the reconstituted object hierarchy specified therein.  This is
   equivalent to ``Unpickler(file).load()``.

   The protocol version of the pickle is detected automatically, so no protocol
   argument is needed.  Bytes past the pickled object's representation are
   ignored.

   The argument *file* must have two methods, a read() method that takes an
   integer argument, and a readline() method that requires no arguments.  Both
   methods should return bytes.  Thus *file* can be an on-disk file opened
   for binary reading, a :class:`io.BytesIO` object, or any other custom object
   that meets this interface.

   Optional keyword arguments are *fix_imports*, *encoding* and *errors*,
   which are used to control compatibility support for pickle stream generated
   by Python 2.x.  If *fix_imports* is True, pickle will try to map the old
   Python 2.x names to the new names used in Python 3.x.  The *encoding* and
   *errors* tell pickle how to decode 8-bit string instances pickled by Python
   2.x; these default to 'ASCII' and 'strict', respectively.

.. function:: loads(bytes_object, \*, fix_imports=True, encoding="ASCII", errors="strict")

   Read a pickled object hierarchy from a :class:`bytes` object and return the
   reconstituted object hierarchy specified therein

   The protocol version of the pickle is detected automatically, so no protocol
   argument is needed.  Bytes past the pickled object's representation are
   ignored.

   Optional keyword arguments are *fix_imports*, *encoding* and *errors*,
   which are used to control compatibility support for pickle stream generated
   by Python 2.x.  If *fix_imports* is True, pickle will try to map the old
   Python 2.x names to the new names used in Python 3.x.  The *encoding* and
   *errors* tell pickle how to decode 8-bit string instances pickled by Python
   2.x; these default to 'ASCII' and 'strict', respectively.


The :mod:`pickle` module defines three exceptions:

.. exception:: PickleError

   Common base class for the other pickling exceptions.  It inherits
   :exc:`Exception`.

.. exception:: PicklingError

   Error raised when an unpicklable object is encountered by :class:`Pickler`.
   It inherits :exc:`PickleError`.

   Refer to :ref:`pickle-picklable` to learn what kinds of objects can be
   pickled.

.. exception:: UnpicklingError

   Error raised when there a problem unpickling an object, such as a data
   corruption or a security violation.  It inherits :exc:`PickleError`.

   Note that other exceptions may also be raised during unpickling, including
   (but not necessarily limited to) AttributeError, EOFError, ImportError, and
   IndexError.


The :mod:`pickle` module exports two classes, :class:`Pickler` and
:class:`Unpickler`:

.. class:: Pickler(file, protocol=None, \*, fix_imports=True)

   This takes a binary file for writing a pickle data stream.

   The optional *protocol* argument tells the pickler to use the given protocol;
   supported protocols are 0, 1, 2, 3.  The default protocol is 3; a
   backward-incompatible protocol designed for Python 3.0.

   Specifying a negative protocol version selects the highest protocol version
   supported.  The higher the protocol used, the more recent the version of
   Python needed to read the pickle produced.

   The *file* argument must have a write() method that accepts a single bytes
   argument.  It can thus be an on-disk file opened for binary writing, a
   :class:`io.BytesIO` instance, or any other custom object that meets this interface.

   If *fix_imports* is True and *protocol* is less than 3, pickle will try to
   map the new Python 3.x names to the old module names used in Python 2.x,
   so that the pickle data stream is readable with Python 2.x.

   .. method:: dump(obj)

      Write a pickled representation of *obj* to the open file object given in
      the constructor.

   .. method:: persistent_id(obj)

      Do nothing by default.  This exists so a subclass can override it.

      If :meth:`persistent_id` returns ``None``, *obj* is pickled as usual.  Any
      other value causes :class:`Pickler` to emit the returned value as a
      persistent ID for *obj*.  The meaning of this persistent ID should be
      defined by :meth:`Unpickler.persistent_load`.  Note that the value
      returned by :meth:`persistent_id` cannot itself have a persistent ID.

      See :ref:`pickle-persistent` for details and examples of uses.

   .. attribute:: fast

      Deprecated. Enable fast mode if set to a true value.  The fast mode
      disables the usage of memo, therefore speeding the pickling process by not
      generating superfluous PUT opcodes.  It should not be used with
      self-referential objects, doing otherwise will cause :class:`Pickler` to
      recurse infinitely.

      Use :func:`pickletools.optimize` if you need more compact pickles.


.. class:: Unpickler(file, \*, fix_imports=True, encoding="ASCII", errors="strict")

   This takes a binary file for reading a pickle data stream.

   The protocol version of the pickle is detected automatically, so no
   protocol argument is needed.

   The argument *file* must have two methods, a read() method that takes an
   integer argument, and a readline() method that requires no arguments.  Both
   methods should return bytes.  Thus *file* can be an on-disk file object opened
   for binary reading, a :class:`io.BytesIO` object, or any other custom object
   that meets this interface.

   Optional keyword arguments are *fix_imports*, *encoding* and *errors*,
   which are used to control compatibility support for pickle stream generated
   by Python 2.x.  If *fix_imports* is True, pickle will try to map the old
   Python 2.x names to the new names used in Python 3.x.  The *encoding* and
   *errors* tell pickle how to decode 8-bit string instances pickled by Python
   2.x; these default to 'ASCII' and 'strict', respectively.

   .. method:: load()

      Read a pickled object representation from the open file object given in
      the constructor, and return the reconstituted object hierarchy specified
      therein.  Bytes past the pickled object's representation are ignored.

   .. method:: persistent_load(pid)

      Raise an :exc:`UnpickingError` by default.

      If defined, :meth:`persistent_load` should return the object specified by
      the persistent ID *pid*.  If an invalid persistent ID is encountered, an
      :exc:`UnpickingError` should be raised.

      See :ref:`pickle-persistent` for details and examples of uses.

   .. method:: find_class(module, name)

      Import *module* if necessary and return the object called *name* from it,
      where the *module* and *name* arguments are :class:`str` objects.  Note,
      unlike its name suggests, :meth:`find_class` is also used for finding
      functions.

      Subclasses may override this to gain control over what type of objects and
      how they can be loaded, potentially reducing security risks. Refer to
      :ref:`pickle-restrict` for details.


.. _pickle-picklable:

What can be pickled and unpickled?
----------------------------------

The following types can be pickled:

* ``None``, ``True``, and ``False``

* integers, floating point numbers, complex numbers

* strings, bytes, bytearrays

* tuples, lists, sets, and dictionaries containing only picklable objects

* functions defined at the top level of a module

* built-in functions defined at the top level of a module

* classes that are defined at the top level of a module

* instances of such classes whose :attr:`__dict__` or :meth:`__setstate__` is
  picklable  (see section :ref:`pickle-inst` for details)

Attempts to pickle unpicklable objects will raise the :exc:`PicklingError`
exception; when this happens, an unspecified number of bytes may have already
been written to the underlying file.  Trying to pickle a highly recursive data
structure may exceed the maximum recursion depth, a :exc:`RuntimeError` will be
raised in this case.  You can carefully raise this limit with
:func:`sys.setrecursionlimit`.

Note that functions (built-in and user-defined) are pickled by "fully qualified"
name reference, not by value.  This means that only the function name is
pickled, along with the name of module the function is defined in.  Neither the
function's code, nor any of its function attributes are pickled.  Thus the
defining module must be importable in the unpickling environment, and the module
must contain the named object, otherwise an exception will be raised. [#]_

Similarly, classes are pickled by named reference, so the same restrictions in
the unpickling environment apply.  Note that none of the class's code or data is
pickled, so in the following example the class attribute ``attr`` is not
restored in the unpickling environment::

   class Foo:
       attr = 'A class attribute'

   picklestring = pickle.dumps(Foo)

These restrictions are why picklable functions and classes must be defined in
the top level of a module.

Similarly, when class instances are pickled, their class's code and data are not
pickled along with them.  Only the instance data are pickled.  This is done on
purpose, so you can fix bugs in a class or add methods to the class and still
load objects that were created with an earlier version of the class.  If you
plan to have long-lived objects that will see many versions of a class, it may
be worthwhile to put a version number in the objects so that suitable
conversions can be made by the class's :meth:`__setstate__` method.


.. _pickle-inst:

Pickling Class Instances
------------------------

In this section, we describe the general mechanisms available to you to define,
customize, and control how class instances are pickled and unpickled.

In most cases, no additional code is needed to make instances picklable.  By
default, pickle will retrieve the class and the attributes of an instance via
introspection. When a class instance is unpickled, its :meth:`__init__` method
is usually *not* invoked.  The default behaviour first creates an uninitialized
instance and then restores the saved attributes.  The following code shows an
implementation of this behaviour::

   def save(obj):
       return (obj.__class__, obj.__dict__)

   def load(cls, attributes):
       obj = cls.__new__(cls)
       obj.__dict__.update(attributes)
       return obj

Classes can alter the default behaviour by providing one or several special
methods:

.. method:: object.__getnewargs__()

   In protocol 2 and newer, classes that implements the :meth:`__getnewargs__`
   method can dictate the values passed to the :meth:`__new__` method upon
   unpickling.  This is often needed for classes whose :meth:`__new__` method
   requires arguments.


.. method:: object.__getstate__()

   Classes can further influence how their instances are pickled; if the class
   defines the method :meth:`__getstate__`, it is called and the returned object
   is pickled as the contents for the instance, instead of the contents of the
   instance's dictionary.  If the :meth:`__getstate__` method is absent, the
   instance's :attr:`__dict__` is pickled as usual.


.. method:: object.__setstate__(state)

   Upon unpickling, if the class defines :meth:`__setstate__`, it is called with
   the unpickled state.  In that case, there is no requirement for the state
   object to be a dictionary.  Otherwise, the pickled state must be a dictionary
   and its items are assigned to the new instance's dictionary.

   .. note::

      If :meth:`__getstate__` returns a false value, the :meth:`__setstate__`
      method will not be called upon unpickling.


Refer to the section :ref:`pickle-state` for more information about how to use
the methods :meth:`__getstate__` and :meth:`__setstate__`.

.. note::

   At unpickling time, some methods like :meth:`__getattr__`,
   :meth:`__getattribute__`, or :meth:`__setattr__` may be called upon the
   instance.  In case those methods rely on some internal invariant being true,
   the type should implement :meth:`__getnewargs__` to establish such an
   invariant; otherwise, neither :meth:`__new__` nor :meth:`__init__` will be
   called.

.. index:: pair: copy; protocol

As we shall see, pickle does not use directly the methods described above.  In
fact, these methods are part of the copy protocol which implements the
:meth:`__reduce__` special method.  The copy protocol provides a unified
interface for retrieving the data necessary for pickling and copying
objects. [#]_

Although powerful, implementing :meth:`__reduce__` directly in your classes is
error prone.  For this reason, class designers should use the high-level
interface (i.e., :meth:`__getnewargs__`, :meth:`__getstate__` and
:meth:`__setstate__`) whenever possible.  We will show, however, cases where
using :meth:`__reduce__` is the only option or leads to more efficient pickling
or both.

.. method:: object.__reduce__()

   The interface is currently defined as follows.  The :meth:`__reduce__` method
   takes no argument and shall return either a string or preferably a tuple (the
   returned object is often referred to as the "reduce value").

   If a string is returned, the string should be interpreted as the name of a
   global variable.  It should be the object's local name relative to its
   module; the pickle module searches the module namespace to determine the
   object's module.  This behaviour is typically useful for singletons.

   When a tuple is returned, it must be between two and five items long.
   Optional items can either be omitted, or ``None`` can be provided as their
   value.  The semantics of each item are in order:

   .. XXX Mention __newobj__ special-case?

   * A callable object that will be called to create the initial version of the
     object.

   * A tuple of arguments for the callable object.  An empty tuple must be given
     if the callable does not accept any argument.

   * Optionally, the object's state, which will be passed to the object's
     :meth:`__setstate__` method as previously described.  If the object has no
     such method then, the value must be a dictionary and it will be added to
     the object's :attr:`__dict__` attribute.

   * Optionally, an iterator (and not a sequence) yielding successive items.
     These items will be appended to the object either using
     ``obj.append(item)`` or, in batch, using ``obj.extend(list_of_items)``.
     This is primarily used for list subclasses, but may be used by other
     classes as long as they have :meth:`append` and :meth:`extend` methods with
     the appropriate signature.  (Whether :meth:`append` or :meth:`extend` is
     used depends on which pickle protocol version is used as well as the number
     of items to append, so both must be supported.)

   * Optionally, an iterator (not a sequence) yielding successive key-value
     pairs.  These items will be stored to the object using ``obj[key] =
     value``.  This is primarily used for dictionary subclasses, but may be used
     by other classes as long as they implement :meth:`__setitem__`.


.. method:: object.__reduce_ex__(protocol)

   Alternatively, a :meth:`__reduce_ex__` method may be defined.  The only
   difference is this method should take a single integer argument, the protocol
   version.  When defined, pickle will prefer it over the :meth:`__reduce__`
   method.  In addition, :meth:`__reduce__` automatically becomes a synonym for
   the extended version.  The main use for this method is to provide
   backwards-compatible reduce values for older Python releases.

.. _pickle-persistent:

Persistence of External Objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   single: persistent_id (pickle protocol)
   single: persistent_load (pickle protocol)

For the benefit of object persistence, the :mod:`pickle` module supports the
notion of a reference to an object outside the pickled data stream.  Such
objects are referenced by a persistent ID, which should be either a string of
alphanumeric characters (for protocol 0) [#]_ or just an arbitrary object (for
any newer protocol).

The resolution of such persistent IDs is not defined by the :mod:`pickle`
module; it will delegate this resolution to the user defined methods on the
pickler and unpickler, :meth:`persistent_id` and :meth:`persistent_load`
respectively.

To pickle objects that have an external persistent id, the pickler must have a
custom :meth:`persistent_id` method that takes an object as an argument and
returns either ``None`` or the persistent id for that object.  When ``None`` is
returned, the pickler simply pickles the object as normal.  When a persistent ID
string is returned, the pickler will pickle that object, along with a marker so
that the unpickler will recognize it as a persistent ID.

To unpickle external objects, the unpickler must have a custom
:meth:`persistent_load` method that takes a persistent ID object and returns the
referenced object.

Here is a comprehensive example presenting how persistent ID can be used to
pickle external objects by reference.

.. literalinclude:: ../includes/dbpickle.py


.. _pickle-state:

Handling Stateful Objects
^^^^^^^^^^^^^^^^^^^^^^^^^

.. index::
   single: __getstate__() (copy protocol)
   single: __setstate__() (copy protocol)

Here's an example that shows how to modify pickling behavior for a class.
The :class:`TextReader` class opens a text file, and returns the line number and
line contents each time its :meth:`readline` method is called. If a
:class:`TextReader` instance is pickled, all attributes *except* the file object
member are saved. When the instance is unpickled, the file is reopened, and
reading resumes from the last location. The :meth:`__setstate__` and
:meth:`__getstate__` methods are used to implement this behavior. ::

   class TextReader:
       """Print and number lines in a text file."""

       def __init__(self, filename):
           self.filename = filename
           self.file = open(filename)
           self.lineno = 0

       def readline(self):
           self.lineno += 1
           line = self.file.readline()
           if not line:
               return None
           if line.endswith('\n'):
               line = line[:-1]
           return "%i: %s" % (self.lineno, line)

       def __getstate__(self):
           # Copy the object's state from self.__dict__ which contains
           # all our instance attributes. Always use the dict.copy()
           # method to avoid modifying the original state.
           state = self.__dict__.copy()
           # Remove the unpicklable entries.
           del state['file']
           return state

       def __setstate__(self, state):
           # Restore instance attributes (i.e., filename and lineno).
           self.__dict__.update(state)
           # Restore the previously opened file's state. To do so, we need to
           # reopen it and read from it until the line count is restored.
           file = open(self.filename)
           for _ in range(self.lineno):
               file.readline()
           # Finally, save the file.
           self.file = file


A sample usage might be something like this::

   >>> reader = TextReader("hello.txt")
   >>> reader.readline()
   '1: Hello world!'
   >>> reader.readline()
   '2: I am line number two.'
   >>> new_reader = pickle.loads(pickle.dumps(reader))
   >>> new_reader.readline()
   '3: Goodbye!'


.. _pickle-restrict:

Restricting Globals
-------------------

.. index::
   single: find_class() (pickle protocol)

By default, unpickling will import any class or function that it finds in the
pickle data.  For many applications, this behaviour is unacceptable as it
permits the unpickler to import and invoke arbitrary code.  Just consider what
this hand-crafted pickle data stream does when loaded::

    >>> import pickle
    >>> pickle.loads(b"cos\nsystem\n(S'echo hello world'\ntR.")
    hello world
    0

In this example, the unpickler imports the :func:`os.system` function and then
apply the string argument "echo hello world".  Although this example is
inoffensive, it is not difficult to imagine one that could damage your system.

For this reason, you may want to control what gets unpickled by customizing
:meth:`Unpickler.find_class`.  Unlike its name suggests, :meth:`find_class` is
called whenever a global (i.e., a class or a function) is requested.  Thus it is
possible to either forbid completely globals or restrict them to a safe subset.

Here is an example of an unpickler allowing only few safe classes from the
:mod:`builtins` module to be loaded::

   import builtins
   import io
   import pickle

   safe_builtins = {
       'range',
       'complex',
       'set',
       'frozenset',
       'slice',
   }

   class RestrictedUnpickler(pickle.Unpickler):

       def find_class(self, module, name):
           # Only allow safe classes from builtins.
           if module == "builtins" and name in safe_builtins:
               return getattr(builtins, name)
           # Forbid everything else.
           raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                        (module, name))

   def restricted_loads(s):
       """Helper function analogous to pickle.loads()."""
       return RestrictedUnpickler(io.BytesIO(s)).load()

A sample usage of our unpickler working has intended::

    >>> restricted_loads(pickle.dumps([1, 2, range(15)]))
    [1, 2, range(0, 15)]
    >>> restricted_loads(b"cos\nsystem\n(S'echo hello world'\ntR.")
    Traceback (most recent call last):
      ...
    pickle.UnpicklingError: global 'os.system' is forbidden
    >>> restricted_loads(b'cbuiltins\neval\n'
    ...                  b'(S\'getattr(__import__("os"), "system")'
    ...                  b'("echo hello world")\'\ntR.')
    Traceback (most recent call last):
      ...
    pickle.UnpicklingError: global 'builtins.eval' is forbidden


.. XXX Add note about how extension codes could evade our protection
   mechanism (e.g. cached classes do not invokes find_class()).

As our examples shows, you have to be careful with what you allow to be
unpickled.  Therefore if security is a concern, you may want to consider
alternatives such as the marshalling API in :mod:`xmlrpc.client` or
third-party solutions.


.. _pickle-example:

Examples
--------

For the simplest code, use the :func:`dump` and :func:`load` functions. ::

   import pickle

   # An arbitrary collection of objects supported by pickle.
   data = {
       'a': [1, 2.0, 3, 4+6j],
       'b': ("character string", b"byte string"),
       'c': set([None, True, False])
   }

   with open('data.pickle', 'wb') as f:
       # Pickle the 'data' dictionary using the highest protocol available.
       pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


The following example reads the resulting pickled data. ::

   import pickle

   with open('data.pickle', 'rb') as f:
       # The protocol version used is detected automatically, so we do not
       # have to specify it.
       data = pickle.load(f)


.. XXX: Add examples showing how to optimize pickles for size (like using
.. pickletools.optimize() or the gzip module).


.. seealso::

   Module :mod:`copyreg`
      Pickle interface constructor registration for extension types.

   Module :mod:`pickletools`
      Tools for working with and analyzing pickled data.

   Module :mod:`shelve`
      Indexed databases of objects; uses :mod:`pickle`.

   Module :mod:`copy`
      Shallow and deep object copying.

   Module :mod:`marshal`
      High-performance serialization of built-in types.


.. rubric:: Footnotes

.. [#] Don't confuse this with the :mod:`marshal` module

.. [#] The exception raised will likely be an :exc:`ImportError` or an
   :exc:`AttributeError` but it could be something else.

.. [#] The :mod:`copy` module uses this protocol for shallow and deep copying
   operations.

.. [#] The limitation on alphanumeric characters is due to the fact
   the persistent IDs, in protocol 0, are delimited by the newline
   character.  Therefore if any kind of newline characters occurs in
   persistent IDs, the resulting pickle will become unreadable.

