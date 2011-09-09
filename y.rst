y
***

用户登录系统
=============

记录用户登录信息的一个系统， 我们简化业务后只留下一张表。

关系型数据库的设计
------------------

.. code-block:: sql

    mysql> select * from login;
    +---------+----------------+-------------+---------------------+
    | user_id | name           | login_times | last_login_time     |
    +---------+----------------+-------------+---------------------+
    |       1 | ken thompson   |           5 | 2011-01-01 00:00:00 |
    |       2 | dennis ritchie |           1 | 2011-02-01 00:00:00 |
    |       3 | Joe Armstrong  |           2 | 2011-03-01 00:00:00 |
    +---------+----------------+-------------+---------------------+

\ ``user_id``\ 表的主键，\ ``name``\ 表示用户名，\ ``login_times``\ 表示该用户的登录次数，每次用户登录后，\ ``login_times``\ 会自增，而\ ``last_login_time``\ 更新为当前时间。

REDIS的设计
------------

关系型数据转化为KV数据库，我的方法如下：

\ ``key 表名：主键值：列名``\ 

\ ``value 列值``\ 

一般使用冒号做分割符，这是不成文的规矩。比如在php-admin for redis系统里，就是默认以冒号分割，于是\ ``user:1``\ \ ``user:2``\ 等key会分成一组。于是以上的关系数据转化成kv数据后记录如下：

::

    SET login:1:login_times 5
    SET login:2:login_times 1
    SET login:3:login_times 2
    
    SET login:1:last_login_time 2011-1-1
    SET login:2:last_login_time 2011-2-1
    SET login:3:last_login_time 2011-3-1
    
    SET login:1:name ”ken thompson“
    SET login:2:name “dennis ritchie”
    SET login:3:name ”Joe Armstrong“

这样在已知主键的情况下，通过\ :ref:`GET`\ 、\ :ref:`set`\ 就可以获得或者修改用户的登录次数和最后登录时间和姓名。

一般用户是无法知道自己的\ ``id``\ 的，只知道自己的用户名，所以还必须有一个从\ ``name``\ 到\ ``id``\ 的映射关系，这里的设计与上面的有所不同。

::

    SET "login:ken thompson:id"      1
    SET "login:dennis ritchie:id"    2
    SET "login: Joe Armstrong:id"    3

这样每次用户登录的时候业务逻辑如下（python版），r是redis对象，name是已经获知的用户名。

.. code-block:: python

    #获得用户的id
    uid = r.get("login:%s:id" % name)

    #自增用户的登录次数
    ret = r.incr("login:%s:login_times" % uid)

    #更新该用户的最后登录时间
    ret = r.set("login:%s:last_login_time" % uid, datetime.datetime.now())

如果需求仅仅是已知\ ``id``\ ，更新或者获取某个用户的最后登录时间，登录次数，关系型和kv数据库无啥区别：一个通过btree pk，一个通过hash，效果都很好。

假设有如下需求，查找最近登录的N个用户。开发人员看看，还是比较简单的，一个sql搞定：

.. code-block:: sql

    select * from login order by last_login_time desc limit N

DBA了解需求后，考虑到以后表如果比较大，所以在\ ``last_login_time``\ 上建个索引。执行计划从索引leafblock 的最右边开始访问N条记录，再回表N次，效果很好。

过了两天，又来一个需求，需要知道登录次数最多的人是谁。同样的关系型如何处理？DEV说简单：

.. code-block:: sql

    select * from login order by login_times desc limit N

DBA一看，又要在\ ``login_time``\ 上建立一个索引。有没有觉得有点问题呢，表上每个字段上都有素引。

关系型数据库的数据存储的的不灵活是问题的源头，数据仅有一种储存方法，那就是按行排列的堆表。统一的数据结构意味着你必须使用索引来改变sql的访问路径来快速访问某个列的，而访问路径的增加又意味着你必须使用统计信息来辅助，于是一大堆的问题就出现了。

没有索引，没有统计计划，没有执行计划，这就是kv数据库。

redis里如何满足以上的需求呢？对于求最新的N条数据的需求，链表的后进后出的特点非常适合。我们在上面的登录代码之后添加一段代码，维护一个登录的链表，控制他的长度，使得里面永远保存的是最近的N个登录用户。

.. code-block:: python

    #把当前登录人添加到链表里
    ret = r.lpush("login:last_login_times", uid)

    #保持链表只有N位
    ret = redis.ltrim("login:last_login_times", 0, N-1)

这样需要获得最新登录人的\ ``id``\ ，如下的代码即可：

.. code-block:: python

    last_login_list = r.lrange("login:last_login_times", 0, N-1)

另外，求登录次数最多的人，对于排序，积分榜这类需求，\ :ref:`sorted_set_struct`\ 非常的适合，我们把用户和登录次数统一存储在一个\ :ref:`sorted_set_struct`\ 里。

::

    ZADD login:login_times 5 1
    ZADD login:login_times 1 2
    ZADD login:login_times 2 3

这样假如某个用户登录，额外维护一个\ :ref:`sorted_set_struct`\ ，代码如下：

.. code-block:: python

    #对该用户的登录次数自增1
    ret = r.zincrby("login:login_times", 1, uid)

那么如何获得登录次数最多的用户呢？逆序排列取的排名第N的用户即可：

.. code-block:: python

    ret = r.zrevrange("login:login_times", 0, N-1)

可以看出，DEV需要添加2行代码，而DBA不需要考虑索引什么的。
