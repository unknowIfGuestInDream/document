> mysql性能调优

1.  
单表500w

2.
采用分表技术（大表分小表）

a)垂直分表：将部分字段分离出来，设计成分表，根据主表的主键关联
b)水平分表：将相同字段表中的记录按照某种Hash算法进行拆分多个分表

2，采用mysql分区技术（必须5.1版以上，此技术完全能够对抗Oracle），与水平分表有点类似，但是它是在逻辑层进行的水平分表

3.
主从   主库增删改 无索引   从库查询 索引

大表优化方案  https://mp.weixin.qq.com/s/cPHmWZaR8k_vXb4hAuGhhA

MyISAM引擎和InnoDB引擎介绍及应用场景  
https://blog.csdn.net/m0_37814112/article/details/78633136

**记录 sending data导致的cpu打满 sql卡死**

show variables like 'innodb_buffer_pool_size'

修改 innodb_buffer_pool_size值  如果服务器只有mysql的话 最大设置为总内存的75%左右

**查看执行的sql**

mysql -u用户 -p密码

show processlist;   或者    show full processlist;

**类似于日志之类的数据备份表**

引擎修改为MYISAM引擎 innodb事务影响插入效率