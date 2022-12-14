> 工作过程中常用的方法

## 分页查询
```oracle
select * from (select ROW_NUMBER() OVER(order by T.ID asc) R, T.* from DATABASE_INFO T) where R between 1 and 5
```

```oracle
select * from (select FULLTABLE.*, ROWNUM RN from (select * from DATABASE_INFO order by id) FULLTABLE where ROWNUM <= 5) where RN >= 1
```

## 递归查询

```oracle
select MENU_ID_ from MENU connect by prior MENU_ID_ = PARENT_MENU_ID_ start with MENU_ID_ = ?;
select MENU_ID_ from MENU where MENU_STATUS_ = 1 connect by prior MENU_ID_ = PARENT_MENU_ID_ start with MENU_ID_ = ?; -- 查询后过滤
select MENU_ID_ from (select * from MENU where MENU_STATUS_ = 1) connect by prior MENU_ID_ = PARENT_MENU_ID_ start with MENU_ID_ = ?; -- 查询前过滤
```

## 自增id实现

```oracle
-- Create sequence 
create sequence 序列名
minvalue 1
maxvalue 9999999999999999999999
start with 1
increment by 1
nocache;


CREATE OR REPLACE TRIGGER 触发器名
  BEFORE INSERT ON 表名
  REFERENCING OLD AS OLD NEW AS NEW
  FOR EACH ROW
BEGIN
  SELECT 序列名.NEXTVAL INTO :NEW.自增id FROM DUAL;
END 触发器名;
```

## 修改时间字段的触发器
```oracle
create or replace trigger TRI_DAILY_DINGROBOT_UPD
before
update on DAILY_DINGROBOT
for each row
begin
  select sysdate into :NEW.UPDATE_DATE from dual;
end;
```

## 查询过去7天

```oracle
select to_char(sysdate-level+1,'YYYY-MM-DD')today from dual connect by level <=7
```

## 逗号分隔字符串

```oracle
    SELECT regexp_substr('3,4,5', '[^,]+', 1, LEVEL) FROM DUAL CONNECT BY LEVEL <= length('3,4,5') + 1 -length(REPLACE('3,4,5', ',', ''));
```

## 查看连接

```oracle
select count(*) from v$process;   --当前的连接数
select value from v$parameter where name = 'processes'; --数据库允许的最大连接数
SELECT osuser, a.username,cpu_time/executions/1000000||'s', sql_fulltext,machine 
from v$session a, v$sqlarea b
where a.sql_address =b.address order by cpu_time/executions desc;   --查看当前有哪些用户正在使用数据
--修改最大连接数:
alter system set processes = 300 scope = spfile;
--重启数据库:
shutdown immediate;
startup;
```

## 根据条件分组拼接

```oracle
SELECT 分组字段（如id）,LISTAGG(合并字段, ',') WITHIN GROUP (ORDER BY 分组字段)  FROM 表 GROUP BY 分组字段; 
```

## 账户死锁

```oracle
alter user USERNAME account unlock;
commit;
```

## 大小写转换

```oracle
SELECT INITCAP('hello world') as "首字母大写"  FROM DUAL;

SELECT UPPER('hello world')   as "全部转为大写" FROM dual;

SELECT LOWER('HELLO WORLD')   as "全部转为小写" FROM DUAL;
```

## 查询数据库的存储过程

```oracle
select distinct name From user_source where type = 'PROCEDURE'
```

## 查询存储过程等参数信息

```oracle
select * from SYS.ALL_ARGUMENTS t where t.OWNER = '' and t.OBJECT_NAME = ''
```

## 查询表的字段跟注释
```oracle
select * from user_col_comments; -- 当前用户下的表的字段跟注释
select * from dba_col_comments; -- 包括系统表的字段跟注释
select * from all_col_comments; -- 所有用户的表的字段跟注释
```

## 获取表，视图的注释
```oracle
select * from user_tab_comments; -- 当前用户下的表的注释
```

## 获取表
```oracle
select * from user_tables; -- 当前用户拥有的表
select * from dba_tables; -- 包括系统表
select * from all_tables; -- 所有用户的表
```

[更多oracle表信息查看](https://docs.oracle.com/en/database/oracle/oracle-database/12.2/refrn/ALL_TABLES.html#GUID-6823CD28-0681-468E-950B-966C6F71325D  ':target=_blank')

<details>
  <summary>user_tables表各字段意思</summary>
  
* table_name : 表名
* tablespace_name : 表空间名
* cluster_name : 群集名称
* iot_name : IOT（Index Organized Table）索引组织表的名称
* status : 状态
* pct_free : 为一个块保留的空间百分比
* pct_used : 一个块的使用水位的百分比
* ini_trans : 初始交易的数量
* max_trans : 交易的最大数量
* initial_extent : 初始扩展数
* next_extent : 下一次扩展数
* min_extents : 最小扩展数
* max_extents : 最大扩展数
* pct_increase : 表在做了第一次extent后，下次再扩展时的增量，它是一个百分比值
* freelists : 可用列表是e799bee5baa6e79fa5e98193e59b9ee7ad9431333365643533表中的一组可插入数据的可用块
* freelist_groups : 列表所属组
* logging : 是否记录日志
* backed_up : 指示自上次修改表是否已备份（Y）或否（N）的
* num_rows : 表中的行数
* blocks : 所使用的数据块数量
* empty_blocks : 空数据块的数量
* avg_space : 自由空间的平均量
* chain_cnt : 从一个数据块，或迁移到一个新块链接表中的行数
* avg_row_len : 行表中的平均长度
* avg_space_freelist_blocks : 一个freelist上的所有块的平均可用空间
* num_freelist_blocks : 空闲列表上的块数量
* degree : 每个实例的线程数量扫描表
* instances : 跨表进行扫描的实例数量
* cache : 是否是要在缓冲区高速缓存
* table_lock : 是否启用表锁
* sample_size : 分析这个表所使用的样本大小
* last_analyzed : 最近分析的日期
* partitioned : 表是否已分区
* iot_type : 表是否是索引组织表
* temporary : 表是否是暂时的
* secondary : 表是否是次要的对象
* nested : 是否是一个嵌套表
* buffer_pool : 缓冲池的表
* flash_cache : 智能闪存缓存提示可用于表块
* cell_flash_cache : 细胞闪存缓存提示可用于表块
* row_movement : 是否启用分区行运动
* global_stats : 作为一个整体（全球统计）表的统计的是否准确
* user_stats : 是否有统计
* duration : 临时表的时间
* skip_corrupt : 是否忽略损坏的块标记在表和索引扫描（ENABLED）状态的或将引发一个错误（已禁用）。
* monitoring : 是否有监测属性集
* cluster_owner : 群集的所有者
* dependencies : 行依赖性跟踪是否已启用
* compression : 是否启用表压缩
* compress_for : 什么样的操作的默认压缩
* dropped : 是否已经删除并在回收站
* read_only : 表是否是只读
* segment_created : 是否创建表段
* result_cache : 结果缓存表的模式注释
  
</details>  

## 获取表字段
```oracle
select * from user_tab_columns; -- 当前用户下的表的字段
select * from dba_tab_columns; -- 包括系统表的字段
select * from all_tab_columns; -- 所有用户的表的字段
```

## 字段前填充0

固定8位 不足填充0

```oracle
update 表 t set t.字段 = lpad(t.字段,8,0)
```

## 存在修改，不存在新增

```oracle
MERGE <hint> INTO <table_name> -- 表名称
USING <table_view_or_query> -- 表查询信息
ON (<condition>) -- 条件
WHEN MATCHED THEN <update_clause> -- 更新操作
DELETE <where_clause> -- 删除操作
WHEN NOT MATCHED THEN <insert_clause> -- 插入操作
[LOG ERRORS <log_errors_clause> <reject limit <integer | unlimited>]; 
```

示例:
```oracle
MERGE INTO BUD_DATAYEAR_PRODUCTION a
USING (
    SELECT '6d31d8406db423d848534147cc70901z' as UNAME
    FROM dual
) b
ON (a.DATAYEAR_PRODUCTION_ID_ = b.UNAME)
WHEN MATCHED THEN
    UPDATE SET a.YEAR_ = 2022
WHEN NOT MATCHED THEN
    INSERT (a.DATAYEAR_PRODUCTION_ID_,a.YEAR_) VALUES ('6d31d8406db423d848534147cc70901z',2033);
```

## 查询某一字段重复的数据
```oracle
select a.*  from ASSET_MAINTAIN a inner join ASSET_MAINTAIN b on a.asset_id=b.asset_id and a.rowid!=b.rowid
```

## 去除字段中的空串
```oracle
update BASE_DEPT set I_ID = REGEXP_REPLACE(I_ID, '\s')
```

## 去重
```oracle

--方法1：
--常用的关键字：distinct
--缺点：方法局限性很大，因为它只能对全部查询的列做去重。如果我想对col_2,col3去重，那我的结果集中就只能有col_2,col_3列，而不能有col_1列。
select distinct t.user_name, t.user_age from TEST_USER t;
 
--方法2：
--思路：给重复的数据建立有序下标，然后只查询下标为：1的数据即可
select f.user_name, f.user_age
  from (select t.*,
               row_number() over(partition by user_name order by user_name) as group_idx
          from TEST_USER t) f
 where f.group_idx = 1;

--方法3：
select *
  from (select t1.*,
               count(1) over(partition by t1.col_2, t1.col_3) rn
          from nayi224_180824 t1) t1
 where t1.rn > 1;
```
