> 正则表达式具有强大、便捷、高效的文本处理功能。能够添加、删除、分析、叠加、插入和修整各种类型的文本和数据。Oracle从10g开始支持正则表达式
 
## 运算符
```markdown
POSIX 正则表达式由标准的元字符（metacharacters）所构成：
'^' 匹配输入字符串的开始位置，在方括号表达式中使用，此时它表示不接受该字符集合。
'$' 匹配输入字符串的结尾位置。如果设置了 RegExp 对象的 Multiline 属性，则 $ 也匹
配 '\n' 或 '\r'。
'.' 匹配除换行符之外的任何单字符。
'?' 匹配前面的子表达式零次或一次。
'+' 匹配前面的子表达式一次或多次。
'*' 匹配前面的子表达式零次或多次。
'|' 指明两项之间的一个选择。例子'^([a-z]+|[0-9]+)$'表示所有小写字母或数字组合成的
字符串。
'( )' 标记一个子表达式的开始和结束位置。
'[]' 标记一个中括号表达式。
'{m,n}' 一个精确地出现次数范围，m=<出现次数<=n，'{m}'表示出现m次，'{m,}'表示至少
出现m次。
\num 匹配 num，其中 num 是一个正整数。对所获取的匹配的引用。
字符簇：
[[:alpha:]] 任何字母。
[[:digit:]] 任何数字。
[[:alnum:]] 任何字母和数字。
[[:blank:]] 所有的空格字符。
[[:cntrl:]] 所有的控制字符(不会打印出来)。
[[:space:]] 任何白字符。
[[:upper:]] 任何大写字母。
[[:lower:]] 任何小写字母。
[[:punct:]] 任何标点符号。
[[:xdigit:]] 任何16进制的数字，相当于[0-9a-fA-F]。
[[:graph:]] 所有的[:punct:]、[:upper:]、[:lower:]和[:digit:]字符。
各种操作符的运算优先级
\转义符
(), (?:), (?=), [] 圆括号和方括号
*, +, ?, {n}, {n,}, {n,m} 限定符
^, $, anymetacharacter 位置和顺序
```

ORACLE中的支持正则表达式的函数主要有下面四个：
* REGEXP_LIKE ：与LIKE的功能相似
* REGEXP_INSTR ：与INSTR的功能相似
* REGEXP_SUBSTR ：与SUBSTR的功能相似
* REGEXP_REPLACE ：与REPLACE的功能相似

它们在用法上与Oracle SQL 函数LIKE、INSTR、SUBSTR 和REPLACE 用法相同，但是它们使用POSIX 正则表达式代替了老的百分号（%）和通配符（_）字符。

## 范例
### regexp_like
语法：
```oracle
REGEXP_LIKE (source_string, pattern[, match_parameter])
```
* source_string：源字符串
* Pattern：正则表达式
* match_parameter：匹配模式(i:不区分大小写；c:区分大小写；n:允许使用可以匹配任意字符串的操作符；m:将x作为一个包含多行的字符串。

查询value中以1开头60结束的记录并且长度是7位
```oracle
select * from fzq where value like '1____60';
select * from fzq where regexp_like(value,'1....60');
```
查询value中以1开头60结束的记录并且长度是7位并且全部是数字的记录。
使用like就不是很好实现了。
```oracle
select * from fzq where regexp_like(value,'1[0-9]{4}60');
```
也可以这样实现，使用字符集
```oracle
select * from fzq where regexp_like(value,'1[[:digit:]]{4}60');
```
查询value中不是纯数字的记录
```oracle
select * from fzq where not regexp_like(value,'^[[:digit:]]+$');
```
查询value中不包含任何数字的记录
```oracle
select * from fzq where regexp_like(value,'^[^[:digit:]]+$');
```
查询以12或者1b开头的记录.不区分大小写。
```oracle
select * from fzq where regexp_like(value,'^1[2b]','i');
```
查询以12或者1b开头的记录.区分大小写
```oracle
select * from fzq where regexp_like(value,'^1[2B]');
```
查询数据中包含空白的记录
```oracle
select * from fzq where regexp_like(value,'[[:space:]]');
```
查询所有包含小写字母或者数字的记录
```oracle
select * from fzq where regexp_like(value,'^([a-z]+|[0-9]+)$');
```
查询任何包含标点符号的记录
```oracle
select * from fzq where regexp_like(value,'[[:punct:]]');
```

!> 函数中pattern为正则表达式，最多可以包含512个字节。

### REGEXP_SUBSTR
REGEXP_SUBSTR函数使用正则表达式来指定返回串的起点和终点。  
语法：
```oracle
regexp_substr(source_string,pattern[,position[,occurrence[,match_parameter]]])
```
* source_string：源串，可以是常量，也可以是某个值类型为串的列。
* position：从源串开始搜索的位置。默认为1。
* occurrence：指定源串中的第几次出现。默认值1.
* match_parameter：文本量，进一步订制搜索，取值如下：
  * 'i'     用于不区分大小写的匹配。
  * 'c'    用于区分大小写的匹配。
  * 'n'    允许将句点“.”作为通配符来匹配换行符。如果省略改参数，句点将不匹配换行符。
  * 'm'   将源串视为多行。即将“^”和“$”分别看做源串中任意位置任意行的开始和结束，而不是看作整个源串的开始或结束。如果省略该参数，源串将被看作一行来处理。
  * 如果取值不属于上述中的某个，将会报错。如果指定了多个互相矛盾的值，将使用最后一个值。如'ic'会被当做'c'处理。
  * 省略该参数时：默认区分大小写、句点不匹配换行符、源串被看作一行。
  

从字符串中截取子字符串
```oracle
SELECT regexp_substr('1PSN/231_3253/ABc', '[[:alnum:]]+') FROM dual;   -- Output: 1PSN
SELECT regexp_substr('1PSN/231_3253/ABc', '[[:alnum:]]+', 1, 2) FROM dual; -- Output: 231
select regexp_substr('@@/231_3253/ABc','@*[[:alnum:]]+') from dual; -- Output: 231 
select regexp_substr('The zip code 80831 is for falcon, co', '[[:alpha:]]{3,}', 1, 3) from dual; -- 结果选择的是code而非The或zip
```
查找网页地址信息
```oracle
SELECT regexp_substr('Go to http://www.oracle.com/products and click on database', 'http://([[:alnum:]]+\.?){3,4}/?') RESULT FROM dual; -- Output: http://www.oracle.com
```
提取csv字符串中的第三个值
```oracle
SELECT regexp_substr('1101,Yokohama,Japan,1.5.105', '[^,]+', 1, 3) AS output FROM dual; -- Output: Japan
```
字符串的列传行
```oracle
SELECT regexp_substr('1101,Yokohama,Japan,1.5.105', '[^,]+', 1, LEVEL) AS output FROM dual 
CONNECT BY LEVEL <= length '1101,Yokohama,Japan,1.5.105') - length(REPLACE('1101,Yokohama,Japan,1.5.105', ',')) + 1; 
-- 1101 
--Yokohama
--Japan
--1.5.105
```
查找源字符串中是否包含 kid 、kids或者kidding 这三个字符串  
其中： kid 表示字符串kid (s|ding)* 表示匹配0次或者多次字符“s”或者“ding” i 表示不区分大小写
```oracle
SELECT CASE WHEN regexp_like('Why does a kid enjoy kidding with kids only?', 'kid(s|ding)*', 'i') 
THEN 'Match Found' ELSE 'No Match Found' END AS utput 
FROM dual;
Output: Match Found 
```

### REGEXP_INSTR
REGEXP_INSTR函数使用正则表达式返回搜索模式的起点和终点（整数）。如果没有发现匹配的值，将返回0。REGEXP_INSTR函数常常会被用到where子句中。    
语法：
```oracle
regexp_instr(source_string,pattern[,position[,occurrence[,return_option[,match_parameter]]]])
```

* start_position：开始搜索位置
* Occurrence：第n次出现pattern，默认为1
* return_option 的作用，它允许用户告诉Oracle，模式出现的时候，要返回什么内容

如果return_option 为0 则，Oracle 返回第一个字符出现的位置。这是默认值，与INSTR的作用相同 
```oracle
SELECT regexp_instr('abc1def', '[[:digit:]]') output FROM dual; --Output: 4 
```
如果return_option 为1，则Oracle 返回跟在所搜索字符出现以后下一个字符的位置
```oracle
SELECT regexp_instr('abc1def', '[[:digit:]]',1,1,1) output FROM dual; --Output: 5
```

### REGEXP_REPLACE
REPLACE函数用于替换串中的某个值。  
```oracle
REGEXP_REPLACE(source_string,pattern[,replace_string][,position][,occurtence],match_parameter])
```
* replace_string：用于替换的字符串
* Position：开始搜索的起始位置
* occurtence:指定替换第n次出现字符串
* 其他同上。

把名字 aa bb cc 变成 cc, bb, aa.
```oracle
Select REGEXP_REPLACE('aa bb cc','(.*) (.*) (.*)', '3, 2, 1') FROM dual;
```
去掉两个空格
```oracle
Select REGEXP_REPLACE('Joe Smith','( ){2,}', ',') AS RX_REPLACE FROM dual; 
```
正则表达式匹配中文的方法
```oracle
-- 方法1
select regexp_replace('abc秋歌def','['||chr(128)||'-'||chr(255)||']','-') from dual;
-- 方法2（替换中文字符和“\”）
SELECT regexp_replace(ASCIISTR('abc秋-''"",.。!@#$%^&^*()_+=歌def、\'),'\\[[:alnum:]]{4}','X') FROM DUAL;
--  测试例子
select regexp_replace('abc秋-''"",.。!@#$%^&^*()_+=歌def、\','['||chr(128)||'-'||chr(255)||']','X') from dual
union all
SELECT regexp_replace(ASCIISTR('abc秋-''"",.。!@#$%^&^*()_+=歌def、\'),'\\[[:alnum:]]{4}','X') FROM DUAL;
```

### REGEXP_COUNT
11g新增的函数，REGEXP_COUNT函数返回在源串中出现的模式的次数，作为对REGEXP_INSTR函数的补充。如果未找到匹配，函数返回0。 虽然COUNT是一个集合函数，操作的是行组，但是REGEXP_COUNT是单行函数，分别计算每一行。  
语法：
```oracle
regexp_count(source_char,pattern[,start_position[,match_param]])
```
* start_position 开始搜索的位置
* metch_param参数，相对于前面介绍的match_parameter参数多一个取值“x”。 'x'：忽略空格字符。默认情况下，空格与自身想匹配。 metch_param如果指定了多个互相矛盾的值，将使用最后一个值。

统计A出现次数，大小写敏感c，不敏感i
```oracle
select regexp_count ('c means Case insensitive matching','A','1','c')  "count(A)" from dual
select regexp_count ('c means Case insensitive matching','A','1','i')  "count(A)" from dual
-- 结果分别为0,3
```
查询/36.0或者/00.4或者/88/5在字段zb出现的次数
```oracle
REGEXP_COUNT(zb,'/36\.0|/00\.4|/88\.5','1','c')
```
统计除了;,以外其他的
```oracle
regexp_count(whole,'[^;,]+') as cnt
```

