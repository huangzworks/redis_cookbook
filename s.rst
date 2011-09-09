s
**

.. _timeline:

时间线(timeline)
=================

**应用**

在有些应用程序中，数据通常带有一个时间值，程序以时间为单位操作数据(可以是一个时间范围，或者是单独的一个时间点)：比如求一个博客在6月至8月的所有日志，或者是今天写博客的文章数。

还有一些微博客，只显示最近两天的内容，等等。

**定义**

一个时间线对象最少有两个属性

1. 时间值
2. 数据内容

针对时间线对象的操作通常都是一些范围型的操作：比如求某个时间点起到另一个时间点内的所有数据，或者是统计某个时间点起到另一个时间点内的数据数目，等等。

**实现**

在Redis中我们可以用\ :ref:`sorted_set_struct`\ 表示时间线。

当增加一个新条目时，我们将条目内容作为有序集元素的\ ``member``\ 参数，使用当前时间的\ `UnixTime`_\ 格式，作为有序集元素的\ ``score``\ 值。

比如一条在2011年8月22日时47分7秒发出的信息，会被储存为：

\ ``ZADD tweet 1313981227.681918 "hello my friend"``\ 

其中\ ``tweet``\ 是时间线的\ ``key``\ ，\ ``1313981227.681918``\ 是\ `UnixTime`_\ 格式的\ `UTC`_\ 时间，而\ ``"hello my friend"``\ 则是条目内容。

这样一来，就可以用\ :ref:`ZREVRANGE`\ 进行按条目数读取(比如读出最新10条数据)，使用\ :ref:`ZREVRANGEBYSCORE`\ 进行时间范围型的读取操作(比如读出2011年8月20日到2011年8月22日的所有数据)，用\ :ref:`ZREM`\ 对单条数据进行删除，用\ :ref:`ZREMRANGEBYRANK`\ 和\ :ref:`ZREMRANGEBYSCORE`\ 进行时间范围型的删除操作。 

.. literalinclude:: source/s/timeline/sorted_set_implement.py

.. _UnixTime: http://en.wikipedia.org/wiki/Unix_time
.. _UTC: http://en.wikipedia.org/wiki/Coordinated_Universal_Time


锁(Lock)
=========

**应用**

**定义**

**实现**
