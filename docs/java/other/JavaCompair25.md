> 本文旨在介绍Java25相对Java21的新特性

## 新的语法特性
1. 紧凑源文件 & 实例主方法
2. 灵活的构造函数体
3. 作用域值（Scoped Values）
4. 紧凑对象头
5. Shenandoah 分代垃圾回收器
6. 安全增强

### 紧凑源文件 & 实例主方法
简化 Java 程序入口，可写无类声明的 void main() 方法；引入 java.lang.IO 简化控制台 I/O；自动导入 java.base 模块中的公共顶级类等

```java
//旧
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
//新
void main() { 
  System.out.println("Hello Java 25！"); // 直接运行，无需public static
}
```

### 灵活的构造函数体
允许在构造函数中，在调用 this() 或 super() 之前执行一些额外的语句。  
之前: this() 或 super() 必须是构造函数中的第一条语句。  
之后:
  
```java
public class Person {
    private final String name;
    public Person(String firstName, String lastName) {
        String fullName = firstName + " " + lastName;
        // 正确：现在可以先执行语句
        super();
        this.name = fullName;
    }
}
```

### 作用域值（Scoped Values）
允许在线程内和跨线程共享不可变数据，旨在替代 ThreadLocal，优化虚拟线程不可变信息的传递。  
优点: 不可变性保证线程安全，内存占用比 ThreadLocal 低约 40%，生命周期自动绑定，无内存泄漏风险，尤其适合虚拟线程场景。

```java
import java.lang.ScopedValue;

public class ScopedValueExample {
    private static final ScopedValue<String> USER_ID = ScopedValue.newInstance();

    public static void main(String[] args) throws Exception {
        ScopedValue.where(USER_ID, "user123").run(() -> {
            System.out.println("Current user: " + USER_ID.get());
        });
    }
}

```

### 紧凑对象头
说明：将对象头从 128 位压缩至 64 位，减少小对象的内存占用。  
启用：添加 JVM 参数 -XX:+UseCompactObjectHeaders。  
优点: 显著减少内存占用（小型对象最多可节省 33%），提升执行效率（CPU 时间减少，GC 频率降低）。测试显示堆占用减少 22%，
CPU 时间减少 8%，GC 次数减少 15%。无需修改代码即可受益，对微服务、云环境等内存受限场景尤其有利。

### Shenandoah 分代垃圾回收器
说明：Shenandoah GC 的分代模式正式成为生产就绪特性。  
启用：-XX:+UseShenandoahGC -XX:ShenandoahGCMode=generational。  
优点: 针对新生代和老年代采用差异化回收策略，停顿时间降低高达 40%，适合高吞吐应用。

### 安全增强
引入一些列加密工具类，实现信息加密，例如引入基于晶格密码的 ML-KEM（密钥封装）和 ML-DSA（数字签名）算法，实现代码如下：

```java
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-DSA");
KeyPair kp = kpg.generateKeyPair();

Signature sig = Signature.getInstance("ML-DSA");
sig.initSign(kp.getPrivate());
        sig.update(message);
byte[] signature = sig.sign();

// 验证签名
sig.initVerify(kp.getPublic());
        sig.update(message);
boolean verified = sig.verify(signature);
```



