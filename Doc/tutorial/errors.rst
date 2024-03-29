.. _tut-errors:

*********************
错误和异常
*********************

直到现在, 我们还没有更多的提及错误信息, 但是如果你真的尝试了前面的例子, 也许你会见到一些. 这里 (至少) 有两种错误很容易辨认: 语法错误和异常. 


.. _tut-syntaxerrors:

语法错误
============


语法错误, 或者称之为解析错, 是你在学习 Python 的过程中最无孔不入的一种了::

   >>> while True print('Hello world')
     File "<stdin>", line 1, in ?
       while True print('Hello world')
                      ^
   SyntaxError: invalid syntax

The parser repeats the offending line and displays a little 'arrow' pointing at
the earliest point in the line where the error was detected.  The error is
caused by (or at least detected at) the token *preceding* the arrow: in the
example, the error is detected at the function :func:`print`, since a colon
(``':'``) is missing before it.  File name and line number are printed so you
know where to look in case the input came from a script.

语法分析器指出了出错的一行, 并且在最先找到的错误的位置标记了一个小小的' 箭头' . 箭头靠前的位置, 就是错误发生 (或者至少是被发现) 的位置. 这个例子中, 函数 print() 被检查到有错误, 是它前面缺少了一个冒号 (``' :' ``) . 文件名和行号一并给出, 这样就方便的获知是哪一个脚本的问题了. 


.. _tut-exceptions:

异常
==========

Even if a statement or expression is syntactically correct, it may cause an
error when an attempt is made to execute it. Errors detected during execution
are called *exceptions* and are not unconditionally fatal: you will soon learn
how to handle them in Python programs.  Most exceptions are not handled by
programs, however, and result in error messages as shown here::

就算一个语句或表达式在语法上是正确的, 在运行它的时候, 也有可能发生错误. 运行期检测到的错误被称为*异常*, 程序并不会无条件的崩掉, 你很快就可以了解到在Python中如何处理它们了. 大多数的异常都不会被程序处理, 都以错误信息的形式展现在这里:

   >>> 10 * (1/0)
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   ZeroDivisionError: int division or modulo by zero
   >>> 4 + spam*3
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   NameError: name 'spam' is not defined
   >>> '2' + 2
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   TypeError: Can't convert 'int' object to str implicitly

The last line of the error message indicates what happened. Exceptions come in
different types, and the type is printed as part of the message: the types in
the example are :exc:`ZeroDivisionError`, :exc:`NameError` and :exc:`TypeError`.
The string printed as the exception type is the name of the built-in exception
that occurred.  This is true for all built-in exceptions, but need not be true
for user-defined exceptions (although it is a useful convention). Standard
exception names are built-in identifiers (not reserved keywords).

每个错误信息的最后一行或说明发生了什么. 异常会有很多的类型, 
而这个类型会作为消息的一部分打印出来: 在此处的例子中的类型有
:exc:`ZeroDivisionError`, :exc:`NameError` 和 :exc:`TypeError`.
作为异常类型被输出的字符串其实是发生内建异常的名称.
对于所有内建异常都是那样的, 但是对于用户自定义的异常, 则可能不是这样
(尽管有某些约定). 标准异常的名字是内建的标识符 (但并不是关键字).

The rest of the line provides detail based on the type of exception and what
caused it.

这一行最后一部分描述了异常的详细内容和发生的原因. 

The preceding part of the error message shows the context where the exception
happened, in the form of a stack traceback. In general it contains a stack
traceback listing source lines; however, it will not display lines read from
standard input.

错误信息的前面部分显示了异常发生的上下文, 并以调用栈的形式显示具体信息. 通常它包含调用栈里的每一个源代码行, 然而, 来自标准输入的源码不会显示出来. 

:ref:`bltin-exceptions` lists the built-in exceptions and their meanings.

:ref:`bltin-exceptions` 列出了内建的异常和它们的意义.

.. _tut-handling:

异常处理
============

It is possible to write programs that handle selected exceptions. Look at the
following example, which asks the user for input until a valid integer has been
entered, but allows the user to interrupt the program (using :kbd:`Control-C` or
whatever the operating system supports); note that a user-generated interruption
is signalled by raising the :exc:`KeyboardInterrupt` exception. ::

可以通过编程来处理选中的异常. 下面的例子让用户输入一个合法的整数, 但是允许用户中断这个程序 (使用 Control-C 或者操作系统提供的方法) . 用户中断的信息会引发一个 KeyboardInterrupt 异常. 

   >>> while True:
   ...     try:
   ...         x = int(input("Please enter a number: "))
   ...         break
   ...     except ValueError:
   ...         print("Oops!  That was no valid number.  Try again...")
   ...

The :keyword:`try` statement works as follows.

:keyword:`try`语句按照如下方式工作. 

* First, the *try clause* (the statement(s) between the :keyword:`try` and
  :keyword:`except` keywords) is executed.

  首先, 执行try子句 (在关键字`try`和关键字`except`之间的语句) 

* If no exception occurs, the *except clause* is skipped and execution of the
  :keyword:`try` statement is finished.

  如果没有异常发生, 忽略except子句, try子句执行后结束. 

* If an exception occurs during execution of the try clause, the rest of the
  clause is skipped.  Then if its type matches the exception named after the
  :keyword:`except` keyword, the except clause is executed, and then execution
  continues after the :keyword:`try` statement.

  如果在执行try子句的过程中发生了异常, 那么try子句余下的部分将被忽略. 如果异常的类型
  和 except 之后的名称相符, 那么对应的except子句将被执行. 最后执行 try 语句之后的代码. 

* If an exception occurs which does not match the exception named in the except
  clause, it is passed on to outer :keyword:`try` statements; if no handler is
  found, it is an *unhandled exception* and execution stops with a message as
  shown above.

  如果一个异常没有与任何的except匹配, 那么这个异常将会传递给上层的`try`中. 

A :keyword:`try` statement may have more than one except clause, to specify
handlers for different exceptions.  At most one handler will be executed.
Handlers only handle exceptions that occur in the corresponding try clause, not
in other handlers of the same :keyword:`try` statement.  An except clause may
name multiple exceptions as a parenthesized tuple, for example::

一个 try 语句可能包含多个except子句, 分别来处理不同的特定的异常. 最多只有一个分支会被执行. 处理程序将只针对对应的try子句中的异常进行处理, 而不是其他的 `try` 的处理程序中的异常. 一个except子句可以同时处理多个异常, 这些异常将被放在一个括号里成为一个元组, 例如:

   ... except (RuntimeError, TypeError, NameError):
   ...     pass

The last except clause may omit the exception name(s), to serve as a wildcard.
Use this with extreme caution, since it is easy to mask a real programming error
in this way!  It can also be used to print an error message and then re-raise
the exception (allowing a caller to handle the exception as well)::

最后一个except子句可以忽略异常的名称, 它将被当作通配符使用. 这种方法要慎用! 搞不好你会把程序中真正的错误隐藏的无影无踪. 你可以使用这种方法打印一个错误信息, 然后再次把异常抛出 (就让调用者去处理这个烫手的山芋吧) ::

   import sys

   try:
       f = open('myfile.txt')
       s = f.readline()
       i = int(s.strip())
   except IOError as err:
       print("I/O error: {0}".format(err))
   except ValueError:
       print("Could not convert data to an integer.")
   except:
       print("Unexpected error:", sys.exc_info()[0])
       raise

The :keyword:`try` ... :keyword:`except` statement has an optional *else
clause*, which, when present, must follow all except clauses.  It is useful for
code that must be executed if the try clause does not raise an exception.  For
example:

try... except 语句还有一个可选的else子句, 如果使用这个子句, 那么必须放在所有的except子句之后. 这个子句将在try子句没有发生任何异常的时候执行. 例如::

   for arg in sys.argv[1:]:
       try:
           f = open(arg, 'r')
       except IOError:
           print('cannot open', arg)
       else:
           print(arg, 'has', len(f.readlines()), 'lines')
           f.close()

The use of the :keyword:`else` clause is better than adding additional code to
the :keyword:`try` clause because it avoids accidentally catching an exception
that wasn't raised by the code being protected by the :keyword:`try` ...
:keyword:`except` statement.

使用 else 子句比把所有的语句都放在 try 子句里面要好, 这样可以避免一些意想不到的、而except又没有捕获的异常. 

When an exception occurs, it may have an associated value, also known as the
exception's *argument*. The presence and type of the argument depend on the
exception type.

当发生了一个异常, 可能伴随着会有相关数据, 也就是所谓的异常的*参数*. 是否有这个参数, 以及它的类型取决于异常的类型. 

The except clause may specify a variable after the exception name.  The
variable is bound to an exception instance with the arguments stored in
``instance.args``.  For convenience, the exception instance defines
:meth:`__str__` so the arguments can be printed directly without having to
reference ``.args``.  One may also instantiate an exception first before
raising it and add any attributes to it as desired. ::

except语句可以在异常名字 (或元组) 之后指定一个变量. 这个变量绑定异常实例, 异常的参数存放在 instance.args 里面. 为了方便使用, 这个实例定义了方法 __getitem__() 和 __str__`, 所以这个参数可以直接用于赋值或打印, 而不必麻烦的使用 `().args``. 但是并不推荐使用 .args``. 取而代之的是, 这里欢迎给异常传递一个单独的参数 (如果多个参数,  使用元组也可以) , 把它绑定到 ``message 属性上. 一旦发生异常, 它将在抛出前绑定所有指定的属性:权文博

   >>> try:
   ...    raise Exception('spam', 'eggs')
   ... except Exception as inst:
   ...    print(type(inst))    # the exception instance
   ...    print(inst.args)     # arguments stored in .args
   ...    print(inst)          # __str__ allows args to be printed directly,
   ...                         # but may be overridden in exception subclasses
   ...    x, y = inst.args     # unpack args
   ...    print('x =', x)
   ...    print('y =', y)
   ...
   <class 'Exception'>
   ('spam', 'eggs')
   ('spam', 'eggs')
   x = spam
   y = eggs

If an exception has arguments, they are printed as the last part ('detail') of
the message for unhandled exceptions.

对于未处理的异常, 如果他含有参数, 那么他就会被当作详细信息打印出来. 

Exception handlers don't just handle exceptions if they occur immediately in the
try clause, but also if they occur inside functions that are called (even
indirectly) in the try clause. For example::

异常处理并不仅仅处理那些直接发生在try子句中的异常, 而且还能处理子句中调用的函数 (甚至间接调用的函数) 里抛出的异常. 例如:

   >>> def this_fails():
   ...     x = 1/0
   ...
   >>> try:
   ...     this_fails()
   ... except ZeroDivisionError as err:
   ...     print('Handling run-time error:', err)
   ...
   Handling run-time error: int division or modulo by zero


.. _tut-raising:

抛出异常
============

The :keyword:`raise` statement allows the programmer to force a specified
exception to occur. For example::

:keyword:`raise` 语句允许程序员强制抛出一个指定的异常. 例如::

   >>> raise NameError('HiThere')
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   NameError: HiThere

The sole argument to :keyword:`raise` indicates the exception to be raised.
This must be either an exception instance or an exception class (a class that
derives from :class:`Exception`).

raise 唯一的一个参数指定了要被抛出的异常. 它必须是一个异常的实例或者是异常的类 (也就是 Exception 的子类) 

If you need to determine whether an exception was raised but don't intend to
handle it, a simpler form of the :keyword:`raise` statement allows you to
re-raise the exception::

如果你只想知道这是否抛出了一个异常, 并不想去处理它, 那么一个简单的 raise 语句就可以再次把它抛出. 

   >>> try:
   ...     raise NameError('HiThere')
   ... except NameError:
   ...     print('An exception flew by!')
   ...     raise
   ...
   An exception flew by!
   Traceback (most recent call last):
     File "<stdin>", line 2, in ?
   NameError: HiThere


.. _tut-userexceptions:

用户定义异常
===============

Programs may name their own exceptions by creating a new exception class (see
:ref:`tut-classes` for more about Python classes).  Exceptions should typically
be derived from the :exc:`Exception` class, either directly or indirectly.  For
example::

创建一个新的exception类, 你就拥有了一个自己的异常. 异常应该继承自 Exception 类, 或者直接继承, 或者间接继承. 例如:

   >>> class MyError(Exception):
   ...     def __init__(self, value):
   ...         self.value = value
   ...     def __str__(self):
   ...         return repr(self.value)
   ...
   >>> try:
   ...     raise MyError(2*2)
   ... except MyError as e:
   ...     print('My exception occurred, value:', e.value)
   ...
   My exception occurred, value: 4
   >>> raise MyError('oops!')
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
   __main__.MyError: 'oops!'

In this example, the default :meth:`__init__` of :class:`Exception` has been
overridden.  The new behavior simply creates the *value* attribute.  This
replaces the default behavior of creating the *args* attribute.

在这个例子中, 类 Exception 默认的 __init__() 被覆盖, 被替换为只是简单的创建一个*value*属性. 替换了原先的需要创建*args*属性的行为. 

Exception classes can be defined which do anything any other class can do, but
are usually kept simple, often only offering a number of attributes that allow
information about the error to be extracted by handlers for the exception.  When
creating a module that can raise several distinct errors, a common practice is
to create a base class for exceptions defined by that module, and subclass that
to create specific exception classes for different error conditions::

异常的类可以像其他的类一样做任何事情, 但是通常都会比较简单, 只提供一些错误相关的属性, 并且允许处理异常的代码方便的获取这些信息. 当创建一个模块有可能抛出多种不同的异常时, 一种通常的做法是为这个包建立一个基础异常类, 然后基于这个基础类为不同的错误情况创建不同的子类::

   class Error(Exception):
       """Base class for exceptions in this module."""
       pass

   class InputError(Error):
       """Exception raised for errors in the input.

       Attributes:
           expression -- input expression in which the error occurred
           message -- explanation of the error
       """

       def __init__(self, expression, message):
           self.expression = expression
           self.message = message

   class TransitionError(Error):
       """Raised when an operation attempts a state transition that's not
       allowed.

       Attributes:
           previous -- state at beginning of transition
           next -- attempted new state
           message -- explanation of why the specific transition is not allowed
       """

       def __init__(self, previous, next, message):
           self.previous = previous
           self.next = next
           self.message = message

Most exceptions are defined with names that end in "Error," similar to the
naming of the standard exceptions.

大多数的异常的名字都以 "Error" 结尾, 就跟标准的异常命名一样. 

Many standard modules define their own exceptions to report errors that may
occur in functions they define.  More information on classes is presented in
chapter :ref:`tut-classes`.

大多数的标准包为了描述自己的错误, 都为自己的方法定义了自己的异常. 更多的关于类的描述请参阅:ref:`tut-classes`章节. 


.. _tut-cleanup:

定义清理行为
===============

The :keyword:`try` statement has another optional clause which is intended to
define clean-up actions that must be executed under all circumstances.  For
example::

try 语句还有另外一个可选的子句, 它定义了无论在任何情况下都会执行的清理行为.  例如::

   >>> try:
   ...     raise KeyboardInterrupt
   ... finally:
   ...     print('Goodbye, world!')
   ...
   Goodbye, world!
   Traceback (most recent call last):
     File "<stdin>", line 2, in ?
   KeyboardInterrupt

A *finally clause* is always executed before leaving the :keyword:`try`
statement, whether an exception has occurred or not. When an exception has
occurred in the :keyword:`try` clause and has not been handled by an
:keyword:`except` clause (or it has occurred in a :keyword:`except` or
:keyword:`else` clause), it is re-raised after the :keyword:`finally` clause has
been executed.  The :keyword:`finally` clause is also executed "on the way out"
when any other clause of the :keyword:`try` statement is left via a
:keyword:`break`, :keyword:`continue` or :keyword:`return` statement.  A more
complicated example::

无论怎样离开的 try , *finally子句*都会执行, 而不管*try子句*里面有没有发生异常. 如果一个异常在 try 子句里 (或者在 except 和 else 子句里) 被抛出, 而又没有任何的 except 把它截住, 那么这个异常会在 finally 子句执行后再次被抛出. :keyword:finally 子句总是挡在程序要跑路的路中间, 因为离开 try 语句的时候一定会执行, 甚至 break`,  :keyword:`continue 和 return 也逃不出他的手掌心. 下面是一个更加复杂的例子 (在同一个 try 语句里包含 except 和 finally 子句) :

   >>> def divide(x, y):
   ...     try:
   ...         result = x / y
   ...     except ZeroDivisionError:
   ...         print("division by zero!")
   ...     else:
   ...         print("result is", result)
   ...     finally:
   ...         print("executing finally clause")
   ...
   >>> divide(2, 1)
   result is 2.0
   executing finally clause
   >>> divide(2, 0)
   division by zero!
   executing finally clause
   >>> divide("2", "1")
   executing finally clause
   Traceback (most recent call last):
     File "<stdin>", line 1, in ?
     File "<stdin>", line 3, in divide
   TypeError: unsupported operand type(s) for /: 'str' and 'str'

As you can see, the :keyword:`finally` clause is executed in any event.  The
:exc:`TypeError` raised by dividing two strings is not handled by the
:keyword:`except` clause and therefore re-raised after the :keyword:`finally`
clause has been executed.

正如你所见, :keyword:finally 子句在任何情况下都运行. 异常 TypeError 在做两个字符创除法的时候并没有被任何的 except 截获, 但是它也是在 finally 子句执行后才再次被抛出的. 

In real world applications, the :keyword:`finally` clause is useful for
releasing external resources (such as files or network connections), regardless
of whether the use of the resource was successful.

在真实的应用中, :keyword:finally 子句通常用来释放外部资源 (比如文件或者网络连接) , 无论这些资源是否被成功的使用. 


.. _tut-cleanup-with:

预定义的清理行为
===================

Some objects define standard clean-up actions to be undertaken when the object
is no longer needed, regardless of whether or not the operation using the object
succeeded or failed. Look at the following example, which tries to open a file
and print its contents to the screen. ::

一些对象定义了标准的清理行为, 无论系统是否成功的使用了它, 一旦不需要它了, 那么这个标准的清理行为就会执行. 这面这个例子展示了尝试打开一个文件, 然后把内容打印到屏幕上::

   for line in open("myfile.txt"):
       print(line)

The problem with this code is that it leaves the file open for an indeterminate
amount of time after this part of the code has finished executing.
This is not an issue in simple scripts, but can be a problem for larger
applications. The :keyword:`with` statement allows objects like files to be
used in a way that ensures they are always cleaned up promptly and correctly. ::

这段代码的问题是, 当执行完毕后, 文件会保持打开状态, 并没有被关闭. 在一些简单的脚本里面这不是问题, 但是在大型的应用中问题可就大了. :keyword:with 语句就可以保证诸如文件之类的对象在使用完之后一定会正确的执行他的清理方法::

   with open("myfile.txt") as f:
       for line in f:
           print(line)

After the statement is executed, the file *f* is always closed, even if a
problem was encountered while processing the lines. Objects which, like files,
provide predefined clean-up actions will indicate this in their documentation.

这段代码执行完毕后, 文件*f*总是会关闭, 就算在处理过程中出问题了, 它也保证会管理. 凡是像文件这样的对象, 它都会在自己的文档中注明是否提供了预定义的清理对象. 



