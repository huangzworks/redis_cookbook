J
**
.. _counter:

计数器(counter)
================

**应用**

计数器一般用于访问量、下载量、投票数等各种计数用途，和\ :ref:`auid`\ 不同的是，计数器的值不但可以被增加，还可以被清零(比如发现有作弊行为)，或者被减少(比如部分计数无效)，所以计数器生成的值也\ *不是唯一*\ 的。

**定义**

一个计数器，至少应该拥有以下四个操作：

1. 增加数值
2. 减少数值
3. 清零
4. 查看当前数值

**实现**

计数器可以用以下两种方式实现：

1. String类函数，\ :ref:`INCR`\ ，\ :ref:`INCRBY`\ ，\ :ref:`DECR`\ ，\ :ref:`DECRBY`\ ，还有\ :ref:`GET`\ 和\ :ref:`SET`\ 。
2. Hash类函数，\ :ref:`HINCRBY`\ ，\ :ref:`HSET`\ 和\ :ref:`HGET`\ 。

String实现
-----------

.. literalinclude:: source/j/counter/string_implement.py

Hash实现
--------
Hash实现和String实现稍有不同，Hash实现还需提供一个\ ``key``\ 作Hash的键。另外，Hash只有\ :ref:`HINCRBY`\ 而没有HDECRBY命令，但是我们可以通过代码\ ``0-decrement``\ 将负数作为“增量”，传入\ :ref:`HINCRBY`\ 命令，来达到做减法的效果。

.. literalinclude:: source/j/counter/hash_implement.py
