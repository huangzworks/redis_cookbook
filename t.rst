t
**

TAG系统
========

tag在互联网应用里尤其多见，如果以传统的关系型数据库来设计有点不伦不类。我们以查找书的例子来看看redis在这方面的优势。

关系型数据库的设计
------------------

两张表，一张\ ``book``\ 的明细，一张\ ``tag``\ 表，表示每本书的\ ``tag`` ，一本书可以有多个\ ``tag``\ 。

.. code-block:: sql

    mysql> select * from book;
    +------+-------------------------------+----------------+
    | id   | name                          | author         |
    +------+-------------------------------+----------------+
    |    1 | The Ruby Programming Language | Mark Pilgrim   |
    |    1 | Ruby on rail                  | David Flanagan |
    |    1 | Programming Erlang            | Joe Armstrong  |
    +------+-------------------------------+----------------+

.. code-block:: sql

    mysql> select * from tag;
    +---------+---------+
    | tagname | book_id |
    +---------+---------+
    | ruby    |       1 |
    | ruby    |       2 |
    | web     |       2 |
    | erlang  |       3 |
    +---------+---------+

假如有如此需求，查找即是ruby又是web方面的书籍，如果以关系型数据库会怎么处理？

.. code-block:: sql

    select b.name, b.author  from tag t1, tag t2, book b
    where t1.tagname = 'web' and t2.tagname = 'ruby' and t1.book_id = t2.book_id and b.id = t1.book_id

\ ``tag``\ 表自关联2次再与\ ``book``\ 关联，这个sql还是比较复杂的，如果要求即ruby，但不是web方面的书籍呢？

关系型数据其实并不太适合这些集合操作。

REDIS的设计
------------

首先book的数据肯定要存储的，和上面一样。

::

    SET book:1:name     ”The Ruby Programming Language”
    SET book:2:name     ”Ruby on rail”
    SET book:3:name     ”Programming Erlang”
    
    SET book:1:author     ”Mark Pilgrim”
    SET book:2:author     ”David Flanagan”
    SET book:3:author     ”Joe Armstrong”

\ ``tag``\ 表我们使用集合来存储数据，因为集合擅长求交集、并集

::

    SADD tag:ruby 1
    SADD tag:ruby 2
    SADD tag:web 2
    SADD tag:erlang 3

那么，即属于ruby又属于web的书？

.. code-block:: python

    inter_list = redis.sinter("tag.web", "tag:ruby")

即属于ruby，但不属于web的书？

.. code-block:: python

    inter_list = redis.sdiff("tag.ruby", "tag:web")

属于ruby和属于web的书的合集？

.. code-block:: python

    inter_list = redis.sunion("tag.ruby", "tag:web")

简单到不行阿。

从以上2个例子可以看出在某些场景里，关系型数据库是不太适合的，你可能能够设计出满足需求的系统，但总是感觉的怪怪的，有种生搬硬套的感觉。

尤其登录系统这个例子，频繁的为业务建立索引。放在一个复杂的系统里，ddl（创建索引）有可能改变执行计划。导致其它的sql采用不同的执行计划，业务复杂的老系统，这个问题是很难预估的，sql千奇百怪。要求DBA对这个系统里所有的sql都了解，这点太难了。这个问题在oracle里尤其严重，每个DBA估计都碰到过。对于MySQL这类系统，ddl又不方便（虽然现在有online ddl的方法）。碰到大表，DBA凌晨爬起来在业务低峰期操作，这事我没少干过。而这种需求放到redis里就很好处理，DBA仅仅对容量进行预估即可。

未来的OLTP系统应该是kv和关系型的紧密结合。
