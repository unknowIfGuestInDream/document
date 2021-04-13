> 生成500w测试数据

```mysql
-- 建表
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `uname` varchar(20) DEFAULT NULL COMMENT '账号',
  `pwd` varchar(20) DEFAULT NULL COMMENT '密码',
  `addr` varchar(80) DEFAULT NULL COMMENT '地址',
  `tel` varchar(20) DEFAULT NULL COMMENT '电话',
  `regtime` char(30) DEFAULT NULL COMMENT '注册时间',
  `age` int(11) DEFAULT NULL COMMENT '年龄',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
-- 生成数据过程
delimiter $$
SET AUTOCOMMIT = 0$$
 
create  procedure test()
begin
declare v_cnt decimal (10)  default 0 ;
dd:loop
    insert  into user values
        (null,rand()*10,now(),rand()*50,rand()*10,rand()*10,rand()*10),
        (null,rand()*10,now(),rand()*50,rand()*10,rand()*10,rand()*10),
        (null,rand()*10,now(),rand()*50,rand()*10,rand()*10,rand()*10),
        (null,rand()*10,now(),rand()*50,rand()*10,rand()*10,rand()*10),
        (null,rand()*10,now(),rand()*50,rand()*10,rand()*10,rand()*10),
        (null,rand()*10,now(),rand()*50,rand()*10,rand()*10,rand()*10),
        (null,rand()*10,now(),rand()*50,rand()*10,rand()*10,rand()*10),
        (null,rand()*10,now(),rand()*50,rand()*10,rand()*10,rand()*10),
        (null,rand()*10,now(),rand()*50,rand()*10,rand()*10,rand()*10),
        (null,rand()*10,now(),rand()*50,rand()*10,rand()*10,rand()*10);
    commit;
        set v_cnt = v_cnt+10 ;
            if  v_cnt = 5000000 then leave dd;
            end if;
        end loop dd ;
end;$$
 
delimiter ;

-- 过程调用
call test();
```