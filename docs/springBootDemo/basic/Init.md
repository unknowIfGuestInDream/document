> 在我们用springboot搭建项目的时候，有时候会碰到在项目启动时初始化一些操作的需求，针对这种需求springboot(spring)为我们提供了以下几种方案供我们选择: 

- ApplicationRunner与CommandLineRunner接口 
- Spring Bean初始化的InitializingBean,init-method和PostConstruct 
- Spring的事件机制

## ApplicationRunner与CommandLineRunner

**ApplicationRunner**

```java
@Component
public class ApplicationRunnerTest implements ApplicationRunner {

    @Override
    public void run(ApplicationArguments args) throws Exception {
        System.out.println("ApplicationRunner");
    }
}
```

**CommandLineRunner**

```java
@Component
@Order(1)
public class CommandLineRunnerTest implements CommandLineRunner {

    @Override
    public void run(String... args) throws Exception {
        System.out.println("CommandLineRunner...");
    }
}
```

对于这两个接口而言，我们可以通过Order注解或者使用Ordered接口来指定调用顺序，@Order()中的值越小，优先级越高  
Order值相同ApplicationRunner的实现优先执行

**两者的联系与区别**

args为启动配置参数。

![](../../images/init/start.jpg ':size=800x600')

两个接口都有run()方法，只不过它们的参数不一样，CommandLineRunner的参数是最原始的参数，没有进行任何处理，ApplicationRunner的参数是ApplicationArguments,是对原始参数的进一步封装。

## InitializingBean接口

> InitializingBean接口为bean提供了初始化方法的方式，它只包括afterPropertiesSet方法，凡是继承该接口的类，在初始化bean的时候都会执行该方法。注意，实现该接口的最好加上Spring的注解注入，比如@Component

```java
@Component
public class KangBaHandler implements InitializingBean {

    @Override
    public void afterPropertiesSet() throws Exception {
        //bean初始化操作 
    }
}
```

**使用场景**：  
如策略+工厂设计模式 策略接口继承InitializingBean 实现类在afterPropertiesSet中注册工厂

## PostConstruct注解

> 被@PostConstruct修饰的方法会在服务器加载Servlet的时候运行，并且只会被服务器调用一次，类似于Serclet的inti()方法。被@PostConstruct修饰的方法会在构造函数之后，init()方法之前运行。

!> @PostConstruct和@PreDestroy 这两个注解是Java 5引入, 已经完全在Java 11中删除。

**使用场景**：  
如初始化查询数据，并且维护一个list容器，当做缓存使用

**特点：**  
1. 只有一个非静态方法能使用此注解
2. 被注解的方法不得有任何参数
3. 被注解的方法返回值必须为void
4. 被注解方法不得抛出已检查异常
5. 此方法只会被执行一次

## spring事件进行初始化操作

**利用ContextRefreshedEvent事件进行初始化操作**
```java
@Component
public class ApplicationListenerTest implements ApplicationListener<ContextRefreshedEvent> {

    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        System.out.println("我被调用了..");
    }
}
```

**利用ApplicationReadyEvent事件进行初始化操作**
```java
/**
 * springboot加载完成时候执行的事件。
 * 
 * @author: TangLiang
 * @date: 2021/1/22 23:48
 * @since: 1.0
 */
@Component
public class ApplicationReadyEventTest implements ApplicationListener<ApplicationReadyEvent> {
    @Override
    public void onApplicationEvent(ApplicationReadyEvent applicationReadyEvent) {
        System.out.println("ApplicationReadyEvent");
    }
}
```

## Spring项目启动的执行顺序

@PostConstruct > InitializingBean > ContextRefreshedEvent > ApplicationRunner > CommandLineRunner > ApplicationReadyEvent
所以使用的时候当心了， 使用不当容易造成未知的问题哦！

## 总结

轻量的逻辑可放在Bean的@PostConstruct方法中    
耗时长的逻辑如果放在@PostConstruct方法中，可使用独立线程执行  
@PostConstruct 方法固有地绑定到现有的 Spring bean，因此应仅将其用于此单个 bean 的初始化逻辑；  
初始化操作放在CommandLineRunner或ApplicationRunner的实现组件中，想获取复杂的命令行参数时，我们可以使用 ApplicationRunner    
对bean的初始化操作使用InitializingBean，比使用 @PostConstruct 更安全，因为如果我们依赖尚未自动注入的 @Autowired 字段，则 @PostConstruct 方法可能会遇到 NullPointerExceptions  
如果我们不需要获取命令行参数，我们可以通过 ApplicationListener<ApplicationReadyEvent> 创建一些全局的启动逻辑，我们还可以通过它获取 Spring Boot 支持的 configuration properties 环境变量参数  
