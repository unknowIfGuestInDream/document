> 工作过程中常用的方法

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