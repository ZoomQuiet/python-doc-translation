.. highlightlang:: c

.. _bytearrayobjects:

字节数组对象
------------------

.. index:: object: bytearray


.. c:type:: PyByteArrayObject

   This subtype of :c:type:`PyObject` represents a Python bytearray object.


.. c:var:: PyTypeObject PyByteArray_Type

   This instance of :c:type:`PyTypeObject` represents the Python bytearray type;
   it is the same object as :class:`bytearray` in the Python layer.


类型检查宏
^^^^^^^^^^^^^^^^^

.. c:function:: int PyByteArray_Check(PyObject *o)

   Return true if the object *o* is a bytearray object or an instance of a
   subtype of the bytearray type.


.. c:function:: int PyByteArray_CheckExact(PyObject *o)

   Return true if the object *o* is a bytearray object, but not an instance of a
   subtype of the bytearray type.


Direct API 函数
^^^^^^^^^^^^^^^^^^^^

.. c:function:: PyObject* PyByteArray_FromObject(PyObject *o)

   Return a new bytearray object from any object, *o*, that implements the
   buffer protocol.

   .. XXX expand about the buffer protocol, at least somewhere


.. c:function:: PyObject* PyByteArray_FromStringAndSize(const char *string, Py_ssize_t len)

   Create a new bytearray object from *string* and its length, *len*.  On
   failure, *NULL* is returned.


.. c:function:: PyObject* PyByteArray_Concat(PyObject *a, PyObject *b)

   Concat bytearrays *a* and *b* and return a new bytearray with the result.


.. c:function:: Py_ssize_t PyByteArray_Size(PyObject *bytearray)

   Return the size of *bytearray* after checking for a *NULL* pointer.


.. c:function:: char* PyByteArray_AsString(PyObject *bytearray)

   Return the contents of *bytearray* as a char array after checking for a
   *NULL* pointer.


.. c:function:: int PyByteArray_Resize(PyObject *bytearray, Py_ssize_t len)

   Resize the internal buffer of *bytearray* to *len*.

宏
^^^^^^

These macros trade safety for speed and they don't check pointers.

.. c:function:: char* PyByteArray_AS_STRING(PyObject *bytearray)

   Macro version of :c:func:`PyByteArray_AsString`.


.. c:function:: Py_ssize_t PyByteArray_GET_SIZE(PyObject *bytearray)

   Macro version of :c:func:`PyByteArray_Size`.

