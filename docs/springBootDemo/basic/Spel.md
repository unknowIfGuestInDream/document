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

## 语法

SpringEL基础语法格式为#{...}或者${...}。其中以$开头的被称为属性占位符 ，只能用来取值 ，
不能进行表达式计算 ，比如我们常见的@Value(开头的被称为属性占位符，只能用来取值，不能进行表达式计算，
比如我们常见的@Value(开头的被称为属性占位符，只能用来取值，不能进行表达式计算，
比如我们常见的@Value({userName})就是从配置文件取值。
以**#**开头的可以进行表达式计算，例如#{T(java.lang.Math).PI}

### SpringEL支持的操作符如下

| 语法                                 | 说明                                     | 示例                                          |
|------------------------------------|----------------------------------------|---------------------------------------------|
| 字面量                                | 使用单引号或者通过转义双引号。                        | “null”, " “jack” "                          |
| 集合  (properties,lists,maps,arrays) | 像list,map,array等集合可以调用其方法              | “list.get(0)”                               |
| 索引器                                | 使用符号[]可以访问其成员                          | “list[0]”                                   |
| 内部初始化(inner lists/maps)            | 格式:{value}或{key:value},成员以逗号分隔         | " {0,1,2,3,4} “或” {0:name,1:age,3:gender} " |
| 数组构造器(new 操作符)                     | 直接在表达式中,可初始化并分配数组                      | " new int[3] ";支持所有的数组初始化语法                 |
| 比较操作符                              | 可使用比如>,<,=等等的比较运算符                     | “3<5”                                       |
| 逻辑操作符                              | 表达式中的逻辑操作符,使用and,or和not                | " ‘a’ =.= ‘a’ or ‘b’ =.=‘c’ "               |
| 算术操作符                              | 表达式支持的有+,-,*,/,%,^(平方)等等               | " 5+3+2*10 "                                |
| instanceof操作符                      | " obj instanceof Type ",返回Boolean类型    | “‘jack’ instanceof T(java.lang.String)”     |
| matches操作符                         | 正则匹配,支持大部分的匹配符                         | " str matches ‘regex expression’ "          |
| 类型引用操作符 T()                        | 可以引用具体的类java.lang包中的引用不需全类名,反之使用.      | " T(Math).random() "                        |
| new操作符                             | 使用new操作符可实例化对象,但应使用全类名                 | " new java.util.ArrayLis() "                |
| 变量引用操作符#                           | 与求值上下文有关,内置的有#this和#root               | " #var "                                    |
| bean引用操作符@                         | 可引用容器中注册的bean,依据beanName               | " @beanName "                               |
| 三元操作符 ？：                           | 类似于java的三元操作符                          | " 1+1 == 2 ? ‘y’:‘n’ "                      |
| 安全导航操作符?                           | 考虑空值异常的情况,若使用?操作符,遇到此异常时,不抛出,而是返回null. | " list?.get(12) "                           |

### 关系表达式
| 序号 | 符号   | 示例              |
|----|------|-----------------|
| 1  | 等于   | 1 EQ 2, 1 == 2  |
| 2  | 不等于  | 1 NE 2, 1 != 2  |
| 3  | 大于   | 1 GT 2, 10 > 2  |
| 4  | 大于等于 | 1 GE 2, 10 >= 2 |
| 5  | 小于   | 1 LT 2, 10 < 2  |
| 6  | 小于等于 | 1 LE 2, 10 <= 2 |

### 逻辑表达式
| 序号 | 符号                 | 示例                                     |
|----|--------------------|----------------------------------------|
| 1  | 与(且) ，AND( && )    | true && false, true and false          |
| 2  | 或，or(&#124;&#124;) | true &#124;&#124; false, true or false |
| 3  | 非，not（!）           | not true,  ! true                      |

### 集合过滤
| 序号 | 表达式            | 说明             |
|----|----------------|----------------|
| 1  | ?[expression]  | 选择符合条件的元素      |
| 2  | ^ [expression] | 选择符合条件的第一个元素   |
| 3  | $[expression]  | 选择符合条件的最后一个元素  |
| 4  | ![expression]  | 可对集合中的元素挨个进行处理 |

```java
// 集合
parser.parseExpression("{1, 3, 5, 7}.?[#this > 3]").getValue(); // [5, 7] , 选择元素
parser.parseExpression("{1, 3, 5, 7}.^[#this > 3]").getValue(); // 5 , 第一个
parser.parseExpression("{1, 3, 5, 7}.$[#this > 3]").getValue(); // 7 , 最后一个
parser.parseExpression("{1, 3, 5, 7}.![#this + 1]").getValue(); // [2, 4, 6, 8] ,每个元素都加1
// map
Map<Integer, String> map = Maps.newHashMap();
map.put(1, "A");
map.put(2, "B");
map.put(3, "C");
map.put(4, "D");
parser.parseExpression("#map.?[key > 3]").getValue(context);             // {4=D}
parser.parseExpression("#map.?[value == 'A']").getValue(context);        // {1=A}
parser.parseExpression("#map.?[key > 2 and key < 4]").getValue(context); // {3=C}
```

### 测试用例
```java
@SpringBootTest
public class spelTest {
    @Value("#{5}")
    private Integer num1;
    @Value("#{'hello'}")
    private String str1;
    @Value("#{1.024E+3}")
    private Long long1;
    @Value("#{0xFFFF}")
    private Integer num2;
    @Value("#{'true'}")
    private boolean bool1;
    @Value("#{true}")
    private String bool2;
    @Value("#{2+2*3/2}")
    private double dou1;
    @Value("#{10 % 3}")
    private double dou2;
    @Value("#{10 MOD 3}")
    private double dou3;
    @Value("#{2 ^ 3}")
    private double dou4;
    @Value("#{'1 == 2'}")
    private String bool3;
    @Value("#{'1 EQ 2'}")
    private String bool4;
    @Value("#{1 EQ 2}")
    private boolean bool5;
    @Value("#{10 between {5,20}}")
    private boolean bool6;
    @Value("#{new int[3]}")
    private int[] int1;
    @Value("#{{'jack','rose','lili'}}")
    private List<String> list1;
    @Value("#{{0:'jack',1:'rose',2:'lili'}}")
    private Map<String, Object> map1;
    @Value("#{1+1>2 ? 'Y':'N'}")
    private String str3;
    @Value("#{T(Math).abs(-1)}")
    private Integer int2;
    @Value("#{'asdf' instanceof T(String)}")
    private boolean bool7;
    @Value("#{#name?.toUpperCase()}")
    private String str4;
    @Value("#{{1, 3, 5, 7}.?[#this > 3]}")//this表示当前的对象
    private int[] int3;
    @Value("#{not false}")
    private boolean bool8;
    @Value("#{! false}")
    private String str5;
    @Value("#{true && false}")
    private String str6;
    @Value("#{true || false}")
    private String str7;

    @Test
    public void spel1() {
        System.out.println(num1);
        System.out.println(str1);
        System.out.println(long1);
        System.out.println(num2);
        System.out.println(bool1);
        System.out.println(bool2);
        System.out.println(dou1);
        System.out.println(dou2);
        System.out.println(dou3);
        System.out.println(dou4);
        System.out.println(bool3);
        System.out.println(bool4);
        System.out.println(bool5);
        System.out.println(bool6);
        System.out.println(int1.length);
        System.out.println(list1);
        System.out.println(map1);
        System.out.println(str3);
        System.out.println(int2);
        System.out.println(bool7);
        System.out.println(str4);
        System.out.println(int3.length);
        System.out.println(bool8);
        System.out.println(str5);
        System.out.println(str6);
        System.out.println(str7);
    }
}
```

## @Value注入
```java
    @Value("normal")
    private String normal; // 注入普通字符串

    @Value("#{systemProperties['os.name']}")
    private String systemPropertiesName; // 注入操作系统属性

    @Value("#{ T(java.lang.Math).random() * 100.0 }")
    private double randomNumber; //注入表达式结果

    @Value("#{beanInject.another}")
    private String fromAnotherBean; // 注入其他Bean属性：注入beanInject对象的属性another，类具体定义见下面

    @Value("classpath:com/tl/test.txt")
    private Resource resourceFile; // 注入文件资源

    @Value("http://www.baidu.com")
    private Resource testUrl; // 注入URL资源

    @Value("${app.name}")
    private String appName; // 这里的值来自application.properties，spring boot启动时默认加载此文件

    @Value("${spring.profiles.active:prod}")
    private String profiles;//spring.profiles.active属性不存在时为true

    @Value("#{dataSource.url}") //获取bean的属性  
    private String jdbcUrl; 
```

## 参考文档
* [http://itmyhome.com/spring/expressions.html](http://itmyhome.com/spring/expressions.html ':target=_blank')
* [https://zhuanlan.zhihu.com/p/174786047](https://zhuanlan.zhihu.com/p/174786047 ':target=_blank')