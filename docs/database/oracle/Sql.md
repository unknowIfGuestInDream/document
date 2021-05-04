> oracle sql语句调优

## IN 操作符
用IN写出来的SQL的优点是比较容易写及清晰易懂，这比较适合现代软件开发的风格。但是用IN的SQL性能总是比较低的，从Oracle执行的步骤来分析用IN的SQL与不用IN的SQL有以下区别：

ORACLE试图将其转换成多个表的连接，如果转换不成功则先执行IN里面的子查询，再查询外层的表记录，如果转换成功则直接采用多个表的连接方式查询。由此可见用IN的SQL至少多了一个转换的过程。一般的SQL都可以转换成功，但对于含有分组统计等方面的SQL就不能转换了。

推荐方案：在业务密集的SQL当中尽量不采用IN操作符，用EXISTS 方案代替。

## NOT IN操作符
此操作是强列不推荐使用的，因为它不能应用表的索引。

推荐方案：用NOT EXISTS 方案代替

## IS NULL 或IS NOT NULL操作
判断字段是否为空一般是不会应用索引的，因为索引是不索引空值的。

推荐方案：用其它相同功能的操作运算代替，如：a is not null 改为 a>0 或a>’’等。不允许字段为空，而用一个缺省值代替空值，如申请中状态字段不允许为空，缺省为申请。

## > 及 < 操作符
大于或小于操作符一般情况下是不用调整的，因为它有索引就会采用索引查找，但有的情况下可以对它进行优化，如一个表有100万记录，一个数值型字段A，30万记录的A=0，30万记录的A=1，39万记录的A=2，1万记录的A=3。那么执行A>2与A>=3的效果就有很大的区别了，因为A>2时ORACLE会先找出为2的记录索引再进行比较，而A>=3时ORACLE则直接找到=3的记录索引。

## LIKE
LIKE操作符可以应用通配符查询，里面的通配符组合可能达到几乎是任意的查询，但是如果用得不好则会产生性能上的问题，如LIKE ‘%5400%’ 这种查询不会引用索引，而LIKE ‘X5400%’则会引用范围索引。

一个实际例子：用YW_YHJBQK表中营业编号后面的户标识号可来查询营业编号 YY_BH LIKE ‘%5400%’ 这个条件会产生全表扫描，如果改成YY_BH LIKE ’X5400%’ OR YY_BH LIKE ’B5400%’ 则会利用YY_BH的索引进行两个范围的查询，性能肯定大大提高。

## UNION
UNION在进行表链接后会筛选掉重复的记录，所以在表链接后会对所产生的结果集进行排序运算，删除重复的记录再返回结果。实际大部分应用中是不会产生重复的记录，最常见的是过程表与历史表UNION。如：
select * from gc_dfys
union
select * from ls_jg_dfys
这个SQL在运行时先取出两个表的结果，再用排序空间进行排序删除重复的记录，最后返回结果集，如果表数据量大的话可能会导致用磁盘进行排序。

推荐方案：采用UNION ALL操作符替代UNION，因为UNION ALL操作只是简单的将两个结果合并后就返回。

select * from gc_dfys
union all
select * from ls_jg_dfys

## WHERE后面的条件顺序影响
SQL条件的执行是从右到左的

## 选择最有效率的表名顺序
ORACLE的解析器按照从右到左的顺序处理FROM子句中的表名，因此FROM子句中写在最后的表(基础表 driving table)将被最先处理。  
只在基于规则的优化器中有效。

## 查询表顺序的影响
在FROM后面的表中的列表顺序会对SQL执行性能影响，在没有索引及ORACLE没有对表进行统计分析的情况下，ORACLE会按表出现的顺序进行链接，由此可见表的顺序不对时会产生十分耗服物器资源的数据交叉。（注：如果对表进行了统计分析，ORACLE会自动先进小表的链接，再进行大表的链接）

## 采用函数处理的字段不能利用索引
substr(hbs_bh,1,4)=’5400’，优化处理：hbs_bh like ‘5400%’

trunc(sk_rq)=trunc(sysdate)， 优化处理：sk_rq>=trunc(sysdate) and sk_rq<trunc(sysdate+1)

进行了显式或隐式的运算的字段不能进行索引，如：ss_df+20>50，优化处理：ss_df>30

‘X’ || hbs_bh>’X5400021452’，优化处理：hbs_bh>’5400021542’

sk_rq+5=sysdate，优化处理：sk_rq=sysdate-5

hbs_bh=5401002554，优化处理：hbs_bh=’ 5401002554’，注：此条件对hbs_bh 进行隐式的to_number转换，因为hbs_bh字段是字符型。

## 条件内包括了多个本表的字段运算时不能进行索引
ys_df>cx_df，无法进行优化

qc_bh || kh_bh=’5400250000’，优化处理：qc_bh=’5400’ and kh_bh=’250000’

## 使用DECODE函数来减少处理时间： 
 使用DECODE函数可以避免重复扫描相同记录或重复连接相同的表. （DECODE函数的作用：它可以将输入数值与函数中的参数列表相比较，根据输入值返回一个对应值。函数的参数列表是由若干数值及其对应结果值组成的若干序偶形式。当然，如果未能与任何一个实参序偶匹配成功，则函数也有默认的返回值。  
    select decode( x , 1 , ‘x is 1 ’, 2 , ‘x is 2 ’, ‘others’) from dual  
　　当x等于1时，则返回‘x is 1’。  
　　当x等于2时，则返回‘x is 2’。  
　　否则，返回others）  

## 删除重复记录
DELETE FROM EMP E WHERE E.ROWID > (SELECT MIN(X.ROWID) FROM EMP X WHERE X.EMP_NO = E.EMP_NO); 

## 用TRUNCATE替代DELETE
当删除表中的记录时,在通常情况下, 回滚段(rollback segments ) 用来存放可以被恢复的信息. 如果你没有COMMIT事务,ORACLE会将数据恢复到删除之前的状态(准确地说是恢复到执行删除命令之前的状况) 而当运用TRUNCATE时, 回滚段不再存放任何可被恢复的信息.当命令运行后,数据不能被恢复.因此很少的资源被调用,执行时间也会很短. (译者按: TRUNCATE只在删除全表适用,TRUNCATE是DDL不是DML)

## 用EXISTS替换DISTINCT
* (低效): SELECT DISTINCT DEPT_NO,DEPT_NAME FROM DEPT D , EMP E WHERE D.DEPT_NO = E.DEPT_NO 
* (高效): SELECT DEPT_NO,DEPT_NAME FROM DEPT D WHERE EXISTS ( SELECT ‘X' FROM EMP E WHERE E.DEPT_NO = D.DEPT_NO);  

## 用UNION替换OR (适用于索引列) 
通常情况下, 用UNION替换WHERE子句中的OR将会起到较好的效果. 对索引列使用OR将造成全表扫描. 注意, 以上规则只针对多个索引列有效. 如果有column没有被索引, 查询效率可能会因为你没有选择OR而降低  
如果你坚持要用OR, 那就需要返回记录最少的索引列写在最前面. 

## SQL语句优化技巧
1. 对查询进行优化，应尽量避免全表扫描，首先应考虑在 where 及 order by 涉及的列上建立索引。
2. 应尽量避免在 where 子句中对字段进行 null 值判断，否则将导致引擎放弃使用索引而进行全表扫描，如：  
   select id from t where num is null  
   可以在num上设置默认值0，确保表中num列没有null值，然后这样查询：  
   select id from t where num=0  
3. 应尽量避免在 where 子句中使用!=或<>操作符，否则将引擎放弃使用索引而进行全表扫描。
4. 应尽量避免在 where 子句中使用 or 来连接条件，否则将导致引擎放弃使用索引而进行全表扫描，如：  
   select id from t where num=10 or num=20  
   可以这样查询：  
   select id from t where num=10  
   union all  
   select id from t where num=20  
5. in 和 not in 也要慎用，否则会导致全表扫描，如：  
   select id from t where num in(1,2,3)  
   对于连续的数值，能用 between 就不要用 in 了：  
   select id from t where num between 1 and 3  
6. 下面的查询也将导致全表扫描：  
   select id from t where name like '%abc%'  
   若要提高效率，可以考虑全文检索。  
7. 如果在 where 子句中使用参数，也会导致全表扫描。因为SQL只有在运行时才会解析局部变量，但优化程序不能将访问计划的选择推迟到运行时；它必须在编译时进行选择。然而，如果在编译时建立访问计划，变量的值还是未知的，因而无法作为索引选择的输入项。如下面语句将进行全表扫描：  
   select id from t where num=@num  
   可以改为强制查询使用索引：  
   select id from t with(index(索引名)) where num=@num  
8. 应尽量避免在 where 子句中对字段进行表达式操作，这将导致引擎放弃使用索引而进行全表扫描。如：  
   select id from t where num/2=100  
   应改为:  
   select id from t where num=100*2  
9. 应尽量避免在where子句中对字段进行函数操作，这将导致引擎放弃使用索引而进行全表扫描。如：  
   select id from t where substring(name,1,3)='abc' // oracle总有的是substr函数。  
   select id from t where datediff(day,createdate,'2005-11-30')=0 //查过了确实没有datediff函数。  
   应改为:  
   select id from t where name like 'abc%'  
   select id from t where createdate>='2005-11-30' and createdate<'2005-12-1' //   
   oracle 中时间应该把char 转换成 date 如： createdate >= to_date('2005-11-30','yyyy-mm-dd')  
10. 不要在 where 子句中的“=”左边进行函数、算术运算或其他表达式运算，否则系统将可能无法正确使用索引。
11. 在使用索引字段作为条件时，如果该索引是复合索引，那么必须使用到该索引中的第一个字段作为条件时才能保证系统使用该索引，否则该索引将不会被使用，并且应尽可能的让字段顺序与索引顺序相一致。
12. 不要写一些没有意义的查询，如需要生成一个空表结构：  
    select col1,col2 into #t from t where 1=0  
    这类代码不会返回任何结果集，但是会消耗系统资源的，应改成这样：  
    create table #t(...)  
13. 很多时候用 exists 代替 in 是一个好的选择：  
    select num from a where num in(select num from b)  
    用下面的语句替换：  
    select num from a where exists(select 1 from b where num=a.num)  
14. 并不是所有索引对查询都有效，SQL是根据表中数据来进行查询优化的，当索引列有大量数据重复时，SQL查询可能不会去利用索引，如一表中有字段sex，male、female几乎各一半，那么即使在sex上建了索引也对查询效率起不了作用。
15. 索引并不是越多越好，索引固然可以提高相应的 select 的效率，但同时也降低了 insert 及 update 的效率，因为 insert 或 update 时有可能会重建索引，所以怎样建索引需要慎重考虑，视具体情况而定。一个表的索引数最好不要超过6个，若太多则应考虑一些不常使用到的列上建的索引是否有必要。
16. 应尽可能的避免更新 clustered 索引数据列，因为 clustered 索引数据列的顺序就是表记录的物理存储顺序，一旦该列值改变将导致整个表记录的顺序的调整，会耗费相当大的资源。若应用系统需要频繁更新 clustered 索引数据列，那么需要考虑是否应将该索引建为 clustered 索引。
17. 尽量使用数字型字段，若只含数值信息的字段尽量不要设计为字符型，这会降低查询和连接的性能，并会增加存储开销。这是因为引擎在处理查询和连接时会逐个比较字符串中每一个字符，而对于数字型而言只需要比较一次就够了。
18. 尽可能的使用 varchar/nvarchar 代替 char/nchar ，因为首先变长字段存储空间小，可以节省存储空间，其次对于查询来说，在一个相对较小的字段内搜索效率显然要高些。
19. 任何地方都不要使用 select * from t ，用具体的字段列表代替“*”，不要返回用不到的任何字段。
20. 尽量使用表变量来代替临时表。如果表变量包含大量数据，请注意索引非常有限（只有主键索引）。
21. 避免频繁创建和删除临时表，以减少系统表资源的消耗。
22. 临时表并不是不可使用，适当地使用它们可以使某些例程更有效，例如，当需要重复引用大型表或常用表中的某个数据集时。但是，对于一次性事件，最好使用导出表。
23. 在新建临时表时，如果一次性插入数据量很大，那么可以使用 select into 代替 create table，避免造成大量 log ，以提高速度；如果数据量不大，为了缓和系统表的资源，应先create table，然后insert。
24. 如果使用到了临时表，在存储过程的最后务必将所有的临时表显式删除，先 truncate table ，然后 drop table ，这样可以避免系统表的较长时间锁定。
25. 尽量避免使用游标，因为游标的效率较差，如果游标操作的数据超过1万行，那么就应该考虑改写。
26. 使用基于游标的方法或临时表方法之前，应先寻找基于集的解决方案来解决问题，基于集的方法通常更有效。
27. 与临时表一样，游标并不是不可使用。对小型数据集使用 FAST_FORWARD 游标通常要优于其他逐行处理方法，尤其是在必须引用几个表才能获得所需的数据时。在结果集中包括“合计”的例程通常要比使用游标执行的速度快。如果开发时间允许，基于游标的方法和基于集的方法都可以尝试一下，看哪一种方法的效果更好。
28. 在所有的存储过程和触发器的开始处设置 SET NOCOUNT ON ，在结束时设置 SET NOCOUNT OFF 。无需在执行存储过程和触发器的每个语句后向客户端发送 DONE_IN_PROC 消息。
29. 尽量避免大事务操作，提高系统并发能力。
30. 尽量避免向客户端返回大数据量，若数据量过大，应该考虑相应需求是否合理。

