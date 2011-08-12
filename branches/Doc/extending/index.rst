.. _extending-index:

###########################################################################
  Extending and Embedding the Python Interpreter ��չ��Ƕ�� Python ������
###########################################################################

:Release: |version|
:Date: |today|

:Release: |version|
:Date: |today|

This document describes how to write modules in C or C++ to extend the Python
interpreter with new modules.  Those modules can define new functions but also
new object types and their methods.  The document also describes how to embed
the Python interpreter in another application, for use as an extension language.
Finally, it shows how to compile and link extension modules so that they can be
loaded dynamically (at run time) into the interpreter, if the underlying
operating system supports this feature.

����ĵ����������ʹ�� C �� C++ Ϊ Python ������д��չģ��. ��Щģ�鲻�����Զ����µĺ���,
���������µĶ��������Լ����ǵķ���.  ����ĵ�Ҳ�������Ƕ�� Python ����������һ��Ӧ����,
����Ϊһ����չ����. ���, ����������α����������չģ����ʹ�����ǿ��Զ�̬�� (������ʱ��)
���뵽��������, ����Ҫ�ײ�Ĳ���ϵͳ֧���������.

This document assumes basic knowledge about Python.  For an informal
introduction to the language, see :ref:`tutorial-index`.  :ref:`reference-index`
gives a more formal definition of the language.  :ref:`library-index` documents
the existing object types, functions and modules (both built-in and written in
Python) that give the language its wide application range.

����ĵ���Ҫ����ӵ�� Python �Ļ���֪ʶ. ��õ��������Եķ���ʽ����,
���� :ref:`tutorial-index`. :ref:`library-index` �������������Ե�һ����Ϊ��ʽ�Ķ���.
:ref:`library-index` ���������еĶ�������, ������ģ�� (�ڽ��ĺ�ʹ�� Python д��),
���Ǹ����������Կ���ʹ�÷�Χ.

For a detailed description of the whole Python/C API, see the separate
:ref:`c-api-index`.

��Ҫ���� Python/C API ����ϸ����, ���ĵ����� :ref:`c-api-index`.

.. toctree::
   :maxdepth: 2
   :numbered:

   extending.rst
   newtypes.rst
   building.rst
   windows.rst
   embedding.rst
