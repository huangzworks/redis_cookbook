z
**

.. _auid:

自增唯一id(autoincrementing unique identifier)
================================================

**应用**

自增唯一id最常见的应用就是作为关系型数据库的主键，因为主键必须确保每个数据项都有唯一id。

它也可以在不支持自增唯一id的数据库中(比如MongoDB)用来替代唯一id(uniqueidentifier，通常是一个哈希值)，为用户提供更好的URL：比如将\ ``/topic/4e491e229f328b0cd900010d``\ 修改为\ ``/topic/10086``\ 。

**定义**

一个自增唯一id对象最重要的是保证\ *值的唯一性*\ ，要做到这一点，自增id的自增\ ``incr``\ 操作必须是一个\ *原子操作*\ ，它应该能在一个原子时间内完成以下两件事:

1. 增加id值
2. 返回当前id值

并且它也没有减法\ ``decr``\ 和清零\ ``reset``\ 等操作，因为这些操作破坏了唯一性。

\ ``get``\ 操作一般只用于内部检查，比如观察值是否溢出，但在一般情况下，自增唯一id对象应该只有一个\ ``incr``\ 操作。

.. seealso:: 如果你需要一个\ *非唯一*\ 的，带\ ``incr``\ 、\ ``reset``\ 和\ ``decr``\ 等操作的计数对象，请参考\ :ref:`counter`\ 。

**实现**

自增唯一id可以用以下两种方式实现：

1. String类函数： \ :ref:`INCR`\ 和\ :ref:`GET`\ 。
2. Hash类函数：\ :ref:`HINCRBY`\ 和\ :ref:`HGET`\ 。

String实现
----------

.. literalinclude:: source/z/auid/string_implement.py

Hash实现
--------
.. literalinclude:: source/z/auid/hash_implement.py
