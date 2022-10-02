> 本文旨在介绍Java17相对Java11的新特性

## 新的语法特性
1. 文本块
2. switch表达式
3. record关键字
4. sealed classes密封类
5. instanceof模式匹配
6. 有用的空指针异常
7. 日期周期格式化
8. 精简数字格式化支持
9. Stream.toList()简化


### 文本块
Java 13（13、14预览，15正式） 引入了文本块来解决多行文本的问题，文本块主要以三重双引号开头，
并以同样的以三重双引号结尾终止，Java 14 在 Java 13 引入的文本块的基础之上，新加入了两个转义符 \ 和 \s，
分别用于阻止插入换行符和避免末尾空白字符被去掉。文本块增强了使用 String 来表达 HTML、XML、SQL 或 JSON 
等格式字符串的编码可读性，且易于维护。

```java
public class TextBlocksExample {

    @Test
    public void strTest() {
        //换行
        var str = """
                Hello World!
                Java 17 is now available!
                """;
        System.out.println(str);
    }

    @Test
    public void blankTest() {
        /**
         * \  行终止符，用于阻止插入换行符
         * \s 表示一个空格，用来避免末尾的空白字符被去掉
         */
        var str = """
                Hello World!\
                Java 17 is now available!    \s
                """;
        System.out.println(str);
    }

    @Test
    public void jsonStrTest() {
        //有引号也不需要转义
        var str = """
                {
                    id: 1,
                    username: "nathan",
                    age: 25
                }
                """;
        System.out.println(str);
    }

    @Test
    public void htmlStrTest() {
        var str = """
                <html>
                    <body>
                       <p>Java 17 is now available!</p>
                    </body>
                </html>
                """;
        System.out.println(str);
    }
}
```

### switch表达式
在 Java 12（12、13预览，14正式） 之后，对 Switch 表达式进行了改进，比传统写法更简便，
在 Java17 的预览版中，还支持对类型的匹配。

用箭头 (->) 替换冒号 (:) 并确保在大小写中使用表达式。Switch 表达式的默认行为是没有失败，因此不需要 break。  
case 中做不止一件事情时，可以使用方括号来表示 case 块，并在返回值时使用关键字 yield,可以在“旧” switch 语法中使用 yield 关键字也很酷。这里不需要 break。

```java
public class SwitchExample {

    /**
     * 传统做法
     */
    @Test
    public void switchBeforeTest() {
        Character c= 'B';
        String res;
        switch (c) {
            case 'A':
                res = "优秀";
                break;
            case 'B':
                res = "良好";
                break;
            case 'C':
                res = "及格";
                break;
            default:
                res = "未知等级";
        }
        Assert.assertEquals("良好", res);
    }

    /**
     * 新的 switch 表达式
     */
    @Test
    public void switchNowTest() {
        var c = 'B';
        var res = switch (c) {
            case 'A' -> "优秀";
            case 'B' -> "良好";
            case 'C' -> {
                System.out.println("c: " + c);
                yield "及格";
            }
            default -> "未知等级";
        };
        Assert.assertEquals("良好", res);
    }

    /**
     * 类型检查
     * 根据 object 不同的类型和条件做不同的处理
     * 这个是 17 的预览特性
     */
    @Test
    public void formatTest() {
        Object o = 1000000000;
        String formatted = switch (o) {
            //相当于 if (o instanceof Integer && (int)o > 10)
            case Integer i && i > 10 -> String.format("a large Integer %d", i);
            case Integer i -> String.format("a small Integer %d", i);
            case Long l    -> String.format("a Long %d", l);
            default        -> o.toString();
        };
        System.out.println(formatted);
    }
}
```

### record关键字
从 Java14（14、15预览，16正式）之后，可以使用 record 定义不可变数据类，用于在类和应用程序之间的数据传输（DTO 类），
通过构造函数创建对象，JVM 会自动生成 getter 方法供使用，有点类似于 Lombok 的作用。
区别是 Lombok 只是生成代码，而 record 类型的类附加了不可变且透明的语义，这既是优点也是缺点。
Record 类不能存在任何隐藏状态，适用于作为标准化的类使用，不适合作为一个普通的 java bean 使用，更不用说代替 Lombok。

```java
public class RecordClassExample {

    @Test
    public void recordTest() {
        var user = new User(1, "nathan", 25);
        Assert.assertEquals(1, user.id());
        Assert.assertEquals("nathan", user.username());
        Assert.assertEquals(25, user.age());
        //User[id=1, username=nathan, age=25]
        System.out.println(user);
    }

    @Test
    public void recordTest2() {
        Person p1 = new Person("java", 18, "北京市西城区");
        Person p2 = new Person(null, 28, "北京市东城区");
        record PersonRecord(String name, int age) {}
        PersonRecord p1Record = new PersonRecord(p1.getName(), p1.getAge());
        PersonRecord p2Record = new PersonRecord(p2.getName(), p2.getAge());
    }
}

/**
 * 不可变数据透明载体类
 */
record User(long id, String username, int age) {
    //private int otherInt;
    /*{
        System.out.println();
    }*/
    //明确声明全部参数的构造器
    /*public User(long id, String username, int age) {
        this.id = id;
        this.username = username;
        this.age = age;
    }*/
    //全参数构造器简化写法
    /*public User {
    }*/
    //其他构造器要明确调用其他已定义构造器，最后调用最底层还是声明全部参数的构造器
    public User(){
        this(1, "nathan", 25);
    }
}
```

### sealed classes密封类
在一般情况，如果一个类没有被 final 关键字修饰，那么其他类就可以继承该类。
从 Java15（15、16预览，17正式） 开始，可以使用 sealed 修饰一个类或接口，
并通过 permits 指定哪几个类可以从该类继承，继承的子类必须使用 final 或者 non-sealed 修饰。

```java
//接口也可以 sealed interface Animal permits Cat, Dog {
abstract sealed class Animal permits Cat, Dog {
    void eat() {
        System.out.println("have a meal.");
    }
    abstract void speak();
}
//需要明确用 final 修饰
final class Cat extends Animal {
    @Override
    void speak() {
        System.out.println("miao");
    }
}
//如果想被继承的话用 non-sealed 修饰
non-sealed class Dog extends Animal {
    @Override
    void speak() {
        System.out.println("wang");
    }
}

class Husky extends Dog {
    @Override
    void speak() {
        System.out.println("Stupid humans!");
    }
}
```

### instanceof模式匹配
Java 14（14、15预览，16正式） 中，对 instanceof 模式匹配做了改进，允许程序中的逻辑判断从对象中有条件地提取组件，
以编写更简洁和安全的表达式。

```java
public class InstanceofExample {

    @Test
    public void instanceofTest() {
        Object obj = "string value";
        //传统写法
        if (obj instanceof String) {
            String str = (String) obj;
            Assert.assertEquals(str, obj);
        }
        //新写法
        if (obj instanceof String s) {
            Assert.assertEquals(s, obj);
        }
        //还可以做其他操作
        if (obj instanceof String s && s.contains("val")) {
            Assert.assertEquals(s, obj);
        }
    }

}
```

### 有用的空指针异常
有用的 NullPointerException 将节省一些宝贵的分析时间。以下代码导致 NullPointerException。
```java
public class HelpfulNullPointerExceptions {

    public static void main(String[] args) {
        HashMap<String, GrapeClass> grapes = new HashMap<>();
        grapes.put("grape1", new GrapeClass(Color.BLUE, 2));
        grapes.put("grape2", new GrapeClass(Color.white, 4));
        grapes.put("grape3", null);
        var color = ((GrapeClass) grapes.get("grape3")).getColor();
    }
}
```
在Java 11中，输出将显示NullPointerException发生的行号，但不知道哪个方法调用时产生的null，必须通过调试的方式找到。
```java
Exception in thread "main" java.lang.NullPointerException
        at com.xx.xx.HelpfulNullPointerExceptions.main(HelpfulNullPointerExceptions.java:13)
```

在 Java 17 中，相同的代码会产生以下输出，其中准确显示了 NullPointerException 发生的位置。
```java
Exception in thread "main" java.lang.NullPointerException: Cannot invoke "com.xx.xx.GrapeClass.getColor()" because the return value of "java.util.HashMap.get(Object)" is null
    at com.xx.xx.HelpfulNullPointerExceptions.main(HelpfulNullPointerExceptions.java:13)
```

### 日期周期格式化
在Java 17中添加了一个新的模式B,用于格式化DateTime,它根据Unicode标准指示一天时间段。

使用默认的中文语言环境，打印一天中的几个时刻
```java
DateTimeFormatter dtf = DateTimeFormatter.ofPattern("B");
System.out.println(dtf.format(LocalTime.of(8, 0)));
System.out.println(dtf.format(LocalTime.of(13, 0)));
System.out.println(dtf.format(LocalTime.of(20, 0)));
System.out.println(dtf.format(LocalTime.of(23, 0)));
System.out.println(dtf.format(LocalTime.of(0, 0)));

//上午
//下午
//晚上
//晚上
//午夜
//如果是英语环境则输出
//in the morning
//in the afternoon
//in the evening
//at night
//midnight
```

### 精简数字格式化支持
在NumberFormat中添加了一个工厂方法，可以根据Unicode标准以紧凑的、人类可读的形式格式化数字。

SHORT格式如下所示:
```java
NumberFormat fmt = NumberFormat.getCompactNumberInstance(Locale.ENGLISH, NumberFormat.Style.SHORT);
System.out.println(fmt.format(1000));
System.out.println(fmt.format(100000));
System.out.println(fmt.format(1000000));
//1K
//100K
//1M
```

LONG格式如下所示：
```java
fmt = NumberFormat.getCompactNumberInstance(Locale.ENGLISH, NumberFormat.Style.LONG);
System.out.println(fmt.format(1000));
System.out.println(fmt.format(100000));
System.out.println(fmt.format(1000000));
//1 thousand
//100 thousand
//1 million
```

### Stream优化
Java 16 引入 Stream.toList() 为更方便的添加集合方法（取代以前的 .collect(Collectors.toList()) ）, 
还有 Stream.mapMulti 方法，允许用多个元素替换流中的元素。

```java
@Test
public void streamTest() {
    //.toList() 代替 .collect(Collectors.toList())
    Stream.of(1, 2, 3, 4, 5)
            .filter(i -> i % 2 == 0)
            //.count(Collectors.toList())
            .toList()
            .forEach(System.out::println);

    //mapMulti 用多个元素替换流中的元素，原来 flatMap 也能实现
    Stream.of(1, 2, 3)
            //.flatMap(num -> Stream.of(num + num, num * num, " "))
            .mapMulti((num, downstream) -> {
                downstream.accept(num + num);
                downstream.accept(num * num);
                downstream.accept(" ");
            })
            .forEach(System.out::print);
}
```

