## 概述
Spring Retry提供了自动重新调用失败操作的功能。为了使处理更加健壮并且不易出现故障，有时它会自动重试失败的操作，以防它在后续尝试中成功。

## 引入依赖
从2.2.0开始，重试功能从Spring Batch中撤出。它现在是Spring Retry新库的一部分。

```xml
<dependency>
    <groupId>org.springframework.retry</groupId>
    <artifactId>spring-retry</artifactId>
    <version>1.2.5.RELEASE</version>
</dependency>
```

此外还需要引入aop依赖

## 使用
### 开启Spring Retry
将@EnableRetry注释添加到我们的启动类

spring retry 提供了编程式和Aop 注解 两种方式 通过编程式更好理解。

## 注解开发
### @Retryable
要向方法添加重试功能，可以使用@Retryable
```java
@Service
public interface MyService {
    @Retryable(
      value = { SQLException.class }, 
      maxAttempts = 2,
      backoff = @Backoff(delay = 5000))
    void retryService(String sql) throws SQLException;
    ...
}
```

Retryable注解参数：
* value：指定发生的异常进行重试
* include：指定异常重试，为空时，所以异常进行重试
* exclude：指定异常不重试，默认为空
* maxAttemps：重试次数，默认3
* backoff：则代表了延迟，默认是没有延迟的，就是失败后立即重试，当然加上延迟时间的处理方案更好，看业务场景，也可以不加括号里面的(delay = 3000L))，默认延迟1000ms.

@Backoff 注解 重试补偿策略：
* 不设置参数时，默认使用FixedBackOffPolicy（指定等待时间），重试等待1000ms
* delay:指定延迟后重试 
* multiplier:延迟的倍数，eg: delay=1000L,multiplier=2时，第一次重试为1秒，第二次为2秒，第三次为4秒
* 只设置delay,使用FixedBackOffPolicy，重试等待指定的毫秒数
* 设置delay和maxDealy时，重试等待在这两个值之间均态分布
* 设置delay、maxDealy、multiplier，使用 ExponentialBackOffPolicy（指数级重试间隔的实现 ），multiplier即指定延迟倍数，比如delay=5000l,multiplier=2,则第一次重试为5秒，第二次为10秒，第三次为20秒
* 当设置multiplier()属性不等于0时，同时也设置了random()属性时，使用ExponentialRandomBackOffPolicy

!> 注意这里如果@Retryable注解的方法是在Service层，然后在Controller层进行调用的，如果你在本类中调用，那么@Retryable 不会工作。因为当使用@Retryable时，Spring会在原始bean周围创建一个代理，然后可以在特殊情况下特殊处理，这也就是重试的原理了。所以在这种情况下，Spring推荐我们调用一个实际的方法，然后捕获我们在value中抛出的异常，然后根据@Retryable 的饿配置来进行调用。

### @Recover
用于方法。用于@Retryable失败时的“兜底”处理方法。 @Recover注释的方法必须要与@Retryable注解的方法“签名”保持一致，
第一入参为要重试的异常，其他参数与@Retryable保持一致，返回值也要一样，否则无法执行！

```java
@Retryable(value = SQLDataException.class, backoff = @Backoff(value = 0L))
    public String service3() throws SQLDataException {
        log.info("service3 open");
        throw new SQLDataException();
    }

    @Recover
    public String recover(SQLDataException ne) {
        return "SQLDataException recover";
    }
```

### @CircuitBreaker
用于方法，实现熔断模式。

* include 指定处理的异常类。默认为空
* exclude指定不需要处理的异常。默认为空
* vaue指定要重试的异常。默认为空
* maxAttempts 最大重试次数。默认3次
* openTimeout 配置熔断器打开的超时时间，默认5s，当超过openTimeout之后熔断器电路变成半打开状态（只要有一次重试成功，则闭合电路）
* resetTimeout 配置熔断器重新闭合的超时时间，默认20s，超过这个时间断路器关闭

### 注解开发示例
```java
@Retryable(value = RemoteAccessException.class,
            // 退避策略 休息 5秒继续
            backoff = @Backoff(DELAY_TIME),

            // 重试策略 最大一个两次 包含第一次
            maxAttempts = 2,
            // 兜底方案 全部失败 调用当前类中的兜底方法
            recover = "recover"
    )
public Integer retryTestService() {
    int count = invokeCount.getAndIncrement();
    String url = "http://localhost:8080/unstableApi/500";
    if (count % 2 == 0 && count % 5 == 0) {
        url = "http://localhost:8080/unstableApi/200";
    }
    try {
        ResponseEntity<String> responseEntity = restTemplate.getForEntity(url, String.class);
    } catch (Exception e) {
        log.info("try get unstable api failed", e);
        throw new RemoteAccessException("500", e);
    }
    return 500;
}

/**
     * 作为恢复处理程序的方法调用的注释。合适的恢复处理程序具有Throwable类型（或Throwable的子类型）的第一个参数和与要从中恢复的@Retryable方法相同类型的返回值。Throwable第一个参数是可选的（但是没有它的方法只有在没有其他参数匹配时才会被调用）。后续参数按顺序从失败方法的参数列表中填充
     *
     * @param e
     */
@Recover
public Integer recover(RemoteAccessException e) {
    String stack = Arrays.toString(Thread.currentThread().getStackTrace());
    stack = stack.replaceAll(",", "\n");
    log.info("recover is begin : 堆栈 \n {}", stack);
    ResponseEntity<String> responseEntity = restTemplate.getForEntity("http://localhost:8080/unstableApi/200", String.class);
    log.info("remote response is {}", responseEntity.getBody());
    return Integer.parseInt(Objects.requireNonNull(responseEntity.getBody()));
}
```

### 总结
虽然注解使用简便，但是可配置的东西太少，如果想使用spring-retry强大的策略机制，并需定制化RetryTemplate。  
RetryTemplate 对象可以设置重试策略、补偿策略、重试监听等属性。

## RetryTemplate
### 接口介绍
Spring Retry提供了**RetryOperations**接口，它提供了一组execute()方法,每个方法都有一个RetryCallback参数

RetryCallback是execute（）的一个参数，它是一个接口，允许插入失败时需要重试的业务逻辑  
RetryCallback定义了重试的回调操作，定义好重试的操作后，就是怎么触发了重试了，重试策略就需要看RetryPolicy了。
```java
public interface RetryCallback<T> {
   T doWithRetry(RetryContext context) throws Throwable;
}
```

**RecoveryCallback** : 当结束时会调用recover（）方法，RetryOperations可以将控制权传递给另一个回调，称为RecoveryCallback。  
```java
@Override
public Object recover(RetryContext context) throws Exception {
    System.out.println("testRetryTemplate=========：recover");
    return null;
}
```

**RetryPolicy接口：**  
* canRetry 在每次重试的时候判断，是否需要继续
* open 重试开始前调用，保存上下文信息
* registerThrowable 重试的时候调用

这是一个重试策略接口，而其中它的重试策略具体有下面几种
* AlwaysRetryPolicy：总是重试，直到成功为止
* CircuitBreakerRetryPolicy：熔断器策略
* CompositeRetryPolicy：组合重试策略
* ExceptionClassifierRetryPolicy：不同异常策略
* NeverRetryPolicy：只允许callback一次的策略
* SimpleRetryPolicy：简单重试策略，默认重试最大次数为3次
* TimeoutRetryPolicy：超时重试策略，默认超时时间为1

而默认的重试策略则是SimpleRetryPlicy

**重试回退策略BackOffPolicy**

实现类：
* ExponentialBackOffPolicy：指数回退策略，线程安全的，适合并发操作。需要设置Sleeper。其中InitialInterval（设置初始睡眠间隔值。默认值是100毫秒。不能设置为小于1的值）、MaxInterval（最大回退周期的Setter。默认是30000(30秒)。如果调用此方法的值小于1，则重置为1。设置这个值以避免无限等待如果后退了大量的次数(或者避免如果乘数被设置太高）、Multiplier（设置乘数值默认是2.0，如果小于等于1.0，则是1.0）.如果不设置则使用默认值。
* NoBackOffPolicy：没有回退策略，每次立即执行
* FixedBackOffPolicy：固定时间回退策略，默认回退1000ms。
* UniformRandomBackOffPolicy：随机回退策略，默认最小时间是500ms，最大时间是1500ms。
* ExponentialRandomBackOffPolicy：随机指数退避策略

### RetryTemplate配置
```java
@Configuration
public class AppConfig {

    @Bean
    public RetryTemplate retryTemplate() {
        RetryTemplate retryTemplate = new RetryTemplate();

        FixedBackOffPolicy fixedBackOffPolicy = new FixedBackOffPolicy();
        fixedBackOffPolicy.setBackOffPeriod(2000l);
        retryTemplate.setBackOffPolicy(fixedBackOffPolicy);

        SimpleRetryPolicy retryPolicy = new SimpleRetryPolicy();
        retryPolicy.setMaxAttempts(2);
        retryTemplate.setRetryPolicy(retryPolicy);

        return retryTemplate;
    }
}
```

这个RetryPolicy确定了何时应该重试操作。  
其中SimpleRetryPolicy定义了重试的固定次数，另一方面，BackOffPolicy用于控制重试尝试之间的回退。  
最后，FixedBackOffPolicy会使重试在继续之前暂停一段固定的时间。

### 使用RetryTemplate
要使用重试处理来运行代码，我们可以调用retryTemplate.execute()方法：
```java
retryTemplate.execute(new RetryCallback<Void, RuntimeException>() {
    @Override
    public Void doWithRetry(RetryContext arg0) {
        myService.templateRetryService();
        ...
    }
});
```

我们可以使用lambda表达式代替匿名类：
```java
retryTemplate.execute(arg0 -> {
    myService.templateRetryService();
    return null;
});
```

示例1
```java
public void retryTest() {
        RetryTemplate template = new RetryTemplate();
        TimeoutRetryPolicy policy = new TimeoutRetryPolicy();
        policy.setTimeout(30000L);
        template.setRetryPolicy(policy);
        try {
            String result = template.execute(new RetryCallback<String, Exception>() {
                // 重试操作
                @Override
                public String doWithRetry(RetryContext retryContext) throws Exception {
                    return "";
                }
            }, new RecoveryCallback<String>() {
                @Override
                public String recover(RetryContext retryContext) throws Exception {
                    return "";
                }
            });

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
```

示例2
```java
public void testRetryTemplate() throws Throwable {
        RetryTemplate retryTemplate = new RetryTemplate();
        //设置重试策略 最大重试次数2次（什么时候重试）,默认遇到Exception异常时重试。
        SimpleRetryPolicy retryPolicy = new SimpleRetryPolicy();
        retryPolicy.setMaxAttempts(2);
        retryTemplate.setRetryPolicy(retryPolicy);

        // 设置重试间隔时间 3S
        FixedBackOffPolicy fixedBackOffPolicy = new FixedBackOffPolicy();
        fixedBackOffPolicy.setBackOffPeriod(3000l);
        retryTemplate.setBackOffPolicy(fixedBackOffPolicy);

        //使用重试
        retryTemplate.execute(new RetryCallback<Object, Throwable>() {

            @Override
            public Object doWithRetry(RetryContext context) throws Throwable {
                myService.retryService("testRetryTemplate");
                return null;
            }
        }, new RecoveryCallback<Object>() {

            @Override
            public Object recover(RetryContext context) throws Exception {
                System.out.println("testRetryTemplate=========：recover");
                return null;
            }
        });
    }
```

示例3
```java
// 获取原始的对象
RetryTestService targetRetryTestService = (RetryTestService) AopTargetUtils.getTarget(retryTestService);

RetryTemplate retryTemplate = RetryTemplate.builder()
    .maxAttempts(2)
    .fixedBackoff(DELAY_TIME)
    .retryOn(RemoteAccessException.class)
    .traversingCauses()
    // 非必须
    .withListener(retryListener)
    .build();

Integer responseBody = retryTemplate.execute(new RetryCallback<Integer, RemoteAccessException>() {

    @Override
    public Integer doWithRetry(RetryContext context) throws RemoteAccessException {
        // 调用业务
        return targetRetryTestService.retryTestService();
    }
}, new RecoveryCallback<Integer>() {
    // 垫底方案
    @Override
    public Integer recover(RetryContext context) throws Exception {
        // 兜底调用业务
        return targetRetryTestService.recover((RemoteAccessException) context.getLastThrowable());
    }
});
log.info("programmingRetry retryTestService response result is {}", responseBody);
```

### 监听器
监听器在重试时提供另外的回调。我们可以用这些来关注跨不同重试的各个横切点。

#### 添加回调
回调在RetryListener接口中提供：
```java
public class DefaultListenerSupport extends RetryListenerSupport {
    @Override
    public <T, E extends Throwable> void close(RetryContext context,
      RetryCallback<T, E> callback, Throwable throwable) {
        logger.info("onClose");
        ...
        super.close(context, callback, throwable);
    }

    @Override
    public <T, E extends Throwable> void onError(RetryContext context,
      RetryCallback<T, E> callback, Throwable throwable) {
        logger.info("onError"); 
        ...
        super.onError(context, callback, throwable);
    }

    @Override
    public <T, E extends Throwable> boolean open(RetryContext context,
      RetryCallback<T, E> callback) {
        logger.info("onOpen");
        ...
        return super.open(context, callback);
    }
}
```

open和close的回调在整个重试之前和之后执行，而onError应用于单个RetryCallback调用。

#### 注册侦听器
接下来，我们将我们的监听器（DefaultListenerSupport）注册到我们的RetryTemplate bean：
```java
@Configuration
public class AppConfig {
    ...

    @Bean
    public RetryTemplate retryTemplate() {
        RetryTemplate retryTemplate = new RetryTemplate();
        ...
        retryTemplate.registerListener(new DefaultListenerSupport());
        return retryTemplate;
    }
}
```

### 测试
```java
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(
  classes = AppConfig.class,
  loader = AnnotationConfigContextLoader.class)
public class SpringRetryIntegrationTest {

    @Autowired
    private MyService myService;

    @Autowired
    private RetryTemplate retryTemplate;

    @Test(expected = RuntimeException.class)
    public void givenTemplateRetryService_whenCallWithException_thenRetry() {
        retryTemplate.execute(arg0 -> {
            myService.templateRetryService();
            return null;
        });
    }
}
```

从测试日志中可以看出，我们已经正确配置了RetryTemplate和RetryListener：
```shell script
2020-01-09 20:04:10 [main] INFO  c.p.s.DefaultListenerSupport - onOpen 
2020-01-09 20:04:10 [main] INFO  c.pinmost.springretry.MyServiceImpl - throw RuntimeException in method templateRetryService() 
2020-01-09 20:04:10 [main] INFO  c.p.s.DefaultListenerSupport - onError 
2020-01-09 20:04:12 [main] INFO  c.pinmost.springretry.MyServiceImpl - throw RuntimeException in method templateRetryService() 
2020-01-09 20:04:12 [main] INFO  c.p.s.DefaultListenerSupport - onError 
2020-01-09 20:04:12 [main] INFO  c.p.s.DefaultListenerSupport - onClose
```




