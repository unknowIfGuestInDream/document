> 本文旨在介绍Java21相对Java17的新特性

## 新的语法特性
1. 简易的 Web 服务器
2. 优化 Java API 文档中的代码片段
3. 序列化集合
4. 记录模式
5. switch 的模式匹配
6. 虚拟线程

### 简易的 Web 服务器
Java 18 之后，你可以使用 jwebserver 命令启动一个简易的静态 Web 服务器。  
这个服务器不支持 CGI 和 Servlet，只限于静态文件。  
```shell
$ jwebserver
Binding to loopback by default. For all interfaces use "-b 0.0.0.0" or "-b ::".
Serving /cwd and subdirectories on 127.0.0.1 port 8000
URL: http://127.0.0.1:8000/
```

### 优化 Java API 文档中的代码片段
在 Java 18 之前，如果我们想要在 Javadoc 中引入代码片段可以使用 `pre>{@code ...}</pre>`
```java
/**
 * <pre>{@code
 *  lines of source code
 * }</pre>
 */
```
在 Java 18 之后，可以通过 @snippet 标签来做这件事情。
```java
/**
 * The following code shows how to use {@code Optional.isPresent}:
 * {@snippet :
 * if (v.isPresent()) {
 *     System.out.println("v: " + v.get());
 * }
 * }
 */
```

### 序列化集合
JDK 21 引入了一种新的集合类型：Sequenced Collections（序列化集合，也叫有序集合），这是一种具有确定出现顺序（encounter order）的集合
（无论我们遍历这样的集合多少次，元素的出现顺序始终是固定的）。序列化集合提供了处理集合的第一个和最后一个元素以及反向视图（与原始集合相反的顺序）的简单方法。

Sequenced Collections 包括以下三个接口：
* SequencedCollection
* SequencedSet
* SequencedMap

SequencedCollection 接口继承了 Collection接口， 提供了在集合两端访问、添加或删除元素以及获取集合的反向视图的方法。  
```java
interface SequencedCollection<E> extends Collection<E> {

  // New Method

  SequencedCollection<E> reversed();

  // Promoted methods from Deque<E>

  void addFirst(E);
  void addLast(E);

  E getFirst();
  E getLast();

  E removeFirst();
  E removeLast();
}
```
List 和 Deque 接口实现了SequencedCollection 接口。  
这里以 ArrayList 为例，演示一下实际使用效果：  
```java
ArrayList<Integer> arrayList = new ArrayList<>();

arrayList.add(1);   // List contains: [1]

arrayList.addFirst(0);  // List contains: [0, 1]
arrayList.addLast(2);   // List contains: [0, 1, 2]

Integer firstElement = arrayList.getFirst();  // 0
Integer lastElement = arrayList.getLast();  // 2

List<Integer> reversed = arrayList.reversed();
System.out.println(reversed); // Prints [2, 1, 0]
```

SortedSet 和 LinkedHashSet 实现了SequencedSet接口。  
```java
LinkedHashSet<Integer> linkedHashSet = new LinkedHashSet<>(List.of(1, 2, 3));

Integer firstElement = linkedHashSet.getFirst();   // 1
Integer lastElement = linkedHashSet.getLast();    // 3

linkedHashSet.addFirst(0);  //List contains: [0, 1, 2, 3]
linkedHashSet.addLast(4);   //List contains: [0, 1, 2, 3, 4]

System.out.println(linkedHashSet.reversed());   //Prints [4, 3, 2, 1, 0]
```
SequencedMap 接口继承了 Map接口， 提供了在集合两端访问、添加或删除键值对、获取包含 key 的 SequencedSet、
包含 value 的 SequencedCollection、包含 entry（键值对） 的 SequencedSet以及获取集合的反向视图的方法。  
```java
interface SequencedMap<K,V> extends Map<K,V> {

  // New Methods

  SequencedMap<K,V> reversed();

  SequencedSet<K> sequencedKeySet();
  SequencedCollection<V> sequencedValues();
  SequencedSet<Entry<K,V>> sequencedEntrySet();

  V putFirst(K, V);
  V putLast(K, V);


  // Promoted Methods from NavigableMap<K, V>

  Entry<K, V> firstEntry();
  Entry<K, V> lastEntry();

  Entry<K, V> pollFirstEntry();
  Entry<K, V> pollLastEntry();
}
```
SortedMap 和LinkedHashMap 实现了SequencedMap 接口

### 记录模式
记录模式（Record Patterns） 可对 record 的值进行解构，也就是更方便地从记录类（Record Class）中提取数据。并且，还可以嵌套记录模式和类型模式结合使用，
以实现强大的、声明性的和可组合的数据导航和处理形式。  
记录模式不能单独使用，而是要与 instanceof 或 switch 模式匹配一同使用。  
先以 instanceof 为例简单演示一下。  

**简单定义一个记录类：**
```java
record Shape(String type, long unit){}
```

没有记录模式之前：
```java
Shape circle = new Shape("Circle", 10);
if (circle instanceof Shape shape) {

  System.out.println("Area of " + shape.type() + " is : " + Math.PI * Math.pow(shape.unit(), 2));
}
```
有了记录模式之后：
```java
Shape circle = new Shape("Circle", 10);
if (circle instanceof Shape(String type, long unit)) {
  System.out.println("Area of " + type + " is : " + Math.PI * Math.pow(unit, 2));
}
```

**再看看记录模式与 switch 的配合使用。**  
定义一些类：
```java
interface Shape {}
record Circle(double radius) implements Shape { }
record Square(double side) implements Shape { }
record Rectangle(double length, double width) implements Shape { }
```

没有记录模式之前：
```java
Shape shape = new Circle(10);
switch (shape) {
    case Circle c:
        System.out.println("The shape is Circle with area: " + Math.PI * c.radius() * c.radius());
        break;

    case Square s:
        System.out.println("The shape is Square with area: " + s.side() * s.side());
        break;

    case Rectangle r:
        System.out.println("The shape is Rectangle with area: + " + r.length() * r.width());
        break;

    default:
        System.out.println("Unknown Shape");
        break;
}
```

有了记录模式之后：
```java
Shape shape = new Circle(10);
switch(shape) {

  case Circle(double radius):
    System.out.println("The shape is Circle with area: " + Math.PI * radius * radius);
    break;

  case Square(double side):
    System.out.println("The shape is Square with area: " + side * side);
    break;

  case Rectangle(double length, double width):
    System.out.println("The shape is Rectangle with area: + " + length * width);
    break;

  default:
    System.out.println("Unknown Shape");
    break;
}
```

记录模式可以避免不必要的转换，使得代码更建简洁易读。而且，用了记录模式后不必再担心 null 或者 NullPointerException，代码更安全可靠。

### switch 的模式匹配
增强 Java 中的 switch 表达式和语句，允许在 case 标签中使用模式。当模式匹配时，执行 case 标签对应的代码。  
在下面的代码中，switch 表达式使用了类型模式来进行匹配。
```java
static String formatterPatternSwitch(Object obj) {
    return switch (obj) {
        case Integer i -> String.format("int %d", i);
        case Long l    -> String.format("long %d", l);
        case Double d  -> String.format("double %f", d);
        case String s  -> String.format("String %s", s);
        default        -> obj.toString();
    };
}
```

### 虚拟线程
虚拟线程（Virtual Thread）是 JDK 而不是 OS 实现的轻量级线程(Lightweight Process，LWP），由 JVM 调度。许多虚拟线程共享同一个操作系统线程，
虚拟线程的数量可以远大于操作系统线程的数量。  
在引入虚拟线程之前，java.lang.Thread 包已经支持所谓的平台线程，也就是没有虚拟线程之前，我们一直使用的线程。
JVM 调度程序通过平台线程（载体线程）来管理虚拟线程，一个平台线程可以在不同的时间执行不同的虚拟线程（多个虚拟线程挂载在一个平台线程上），
当虚拟线程被阻塞或等待时，平台线程可以切换到执行另一个虚拟线程。

相比较于平台线程来说，虚拟线程是廉价且轻量级的，使用完后立即被销毁，因此它们不需要被重用或池化，每个任务可以有自己专属的虚拟线程来运行。
虚拟线程暂停和恢复来实现线程之间的切换，避免了上下文切换的额外耗费，兼顾了多线程的优点，简化了高并发程序的复杂，可以有效减少编写、
维护和观察高吞吐量并发应用程序的工作量。

虚拟线程在其他多线程语言中已经被证实是十分有用的，比如 Go 中的 Goroutine、Erlang 中的进程。  
四种创建虚拟线程的方法：
```java
// 1、通过 Thread.ofVirtual() 创建
Runnable fn = () -> {
  // your code here
};

Thread thread = Thread.ofVirtual(fn)
                      .start();

// 2、通过 Thread.startVirtualThread() 、创建
Thread thread = Thread.startVirtualThread(() -> {
  // your code here
});

// 3、通过 Executors.newVirtualThreadPerTaskExecutor() 创建
var executorService = Executors.newVirtualThreadPerTaskExecutor();

executorService.submit(() -> {
  // your code here
});

class CustomThread implements Runnable {
  @Override
  public void run() {
    System.out.println("CustomThread run");
  }
}

//4、通过 ThreadFactory 创建
CustomThread customThread = new CustomThread();
// 获取线程工厂类
ThreadFactory factory = Thread.ofVirtual().factory();
// 创建虚拟线程
Thread thread = factory.newThread(customThread);
// 启动线程
thread.start();
```



