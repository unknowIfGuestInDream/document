> 主从同步

https://www.cnblogs.com/timingstarts/p/12563510.html

http://www.macrozheng.com/#/reference/mysql_master_slave?id=mysql%e4%b8%bb%e4%bb%8e%e5%a4%8d%e5%88%b6%ef%bc%8c%e4%bb%8e%e5%8e%9f%e7%90%86%e5%88%b0%e5%ae%9e%e8%b7%b5%ef%bc%81

slave端  
replicate-do-db    设定需要复制的数据库（多数据库使用逗号，隔开）  
replicate-ignore-db 设定需要忽略的复制数据库 （多数据库使用逗号，隔开）  
replicate-do-table  设定需要复制的表  
replicate-ignore-table 设定需要忽略的复制表   
replicate-wild-do-table 同replication-do-table功能一样，但是可以通配符  
replicate-wild-ignore-table 同replication-ignore-table功能一样，但是可以加通配符  
replicate-wild-do-table=db_name.%   只复制哪个库的哪个表  

HB1  
Mysql 主从同步与触发器的关系  
转自：mysql主从和触发器的关系  
binlog_format=row  
结论：  
1 主从都存在trigger时，主库会记录下所有的操作，包含trigger的操作，从库上数据和主库一致.  
2 主有trigger,从库上没有trigger时，依然不影响主从同步  
3 主上无trigger,从上有trigger时 ，主从数据依然一致，从库上的trigger没有被触发  
binlog_format=statement  

主库表锁！  
mysql>flush tables with read lock;  
主库解锁！  
mysql>unlock tables;  

分区：  
https://www.cnblogs.com/myvic/p/7711498.html