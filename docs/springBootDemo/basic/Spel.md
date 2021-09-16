> Spring表达式语言（简称SpEl）是一个支持查询和操作运行时对象导航图功能的强大的表达式语言. 
它的语法类似于传统EL，但提供额外的功能，最出色的就是函数调用和简单字符串的模板函数。  
尽管有其他可选的 Java 表达式语言，如 OGNL, MVEL,JBoss EL 等等，但 Spel 创建的初衷是了给 Spring 社区提供一种简单而高效的表达式语言，
一种可贯穿整个 Spring 产品组的语言。这种语言的特性应基于 Spring 产品的需求而设计。  
虽然SpEL引擎作为Spring 组合里的表达式解析的基础，但它不直接依赖于Spring,可独立使用，就好像它是一个独立的表达式语言。依赖包为 `org.springframework.expression`

## 应用场景
SpEL 为 Spring 提供了丰富的想象空间，除了一些基本的表达式操作之外，还支持
* 访问 bean 对象
* 调用方法，访问(修改)类(对象)属性
* 计算表达式
* 正则匹配
* ...

SpEL支持如下表达式：
1. 基本表达式： 字面量表达式、关系，逻辑与算数运算表达式、字符串连接及截取表达式、三目运算及Elivis表达式、正则表达式、括号优先级表达式；
2. 类相关表达式： 类类型表达式、类实例化、instanceof表达式、变量定义及引用、赋值表达式、自定义函数、对象属性存取及安全导航表达式、对象方法调用、Bean引用；
3. 集合相关表达式： 内联List、内联数组、集合，字典访问、列表，字典，数组修改、集合投影、集合选择；不支持多维内联数组初始化；不支持内联字典定义；
4. 其他表达式：模板表达式。

!> SpEL表达式中的关键字是不区分大小写的。


http://itmyhome.com/spring/expressions.html     --

https://www.cnblogs.com/yihuihui/p/12928323.html

https://blog.csdn.net/zxcbnm7089/article/details/104770600

https://zhuanlan.zhihu.com/p/174786047