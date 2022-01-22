> Spring Boot在所有内部日志中使用Commons Logging，但是默认配置也提供了对常用日志的支持，如：Java Util Logging，Log4J, Log4J2和Logback。每种Logger都可以通过配置使用控制台或者文件输出日志内容。  
SLF4J —— Simple Logging Facade For Java，它是一个针对于各类Java日志框架的统一Facade抽象。Java日志框架众多——常用的有java.util.logging, log4j, logback，commons-logging, Spring框架使用的是Jakarta Commons Logging API（JCL）。而SLF4J定义了统一的日志抽象接口，而真正的日志实现则是在运行时决定的——它提供了各类日志框架的绑定。  
Logback是log4j框架的作者开发的新一代日志框架，它效率更高、能够适应诸多的运行环境，同时天然支持SLF4J。  
默认情况下，Spring Boot会用Logback来记录日志，并用INFO级别输出到控制台。在运行应用程序和其他例子时，你应该已经看到很多INFO级别的日志了

## 自定义logback.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE configuration>
<configuration>
    <!-- 使用默认的格式  -->
    <include resource="org/springframework/boot/logging/logback/defaults.xml"/>
    <include resource="org/springframework/boot/logging/logback/console-appender.xml"/>
    <!--应用名称-->
    <property name="APP_NAME" value="springBootDemo"/>
    <!--日志文件保存路径-->
    <property name="LOG_FILE_PATH" value="${LOG_FILE:-${LOG_PATH:-${LOG_TEMP:-${java.io.tmpdir:-/tmp}}}/logs}"/>
    <contextName>${APP_NAME}</contextName>
    <!--每天记录日志到文件appender-->
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <!--如果只是想要 Info 级别的日志，只是过滤 info 还是会输出 Error 日志，因为 Error 的级别高， 所以我们使用下面的策略，可以避免输出 Error 的日志-->
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <!--过滤 Error-->
            <level>ERROR</level>
            <!--匹配到就禁止-->
            <onMatch>DENY</onMatch>
            <!--没有匹配到就允许-->
            <onMismatch>ACCEPT</onMismatch>
        </filter>
        <!--日志名称，如果没有File 属性，那么只会使用FileNamePattern的文件路径规则如果同时有<File>和<FileNamePattern>，那么当天日志是<File>，明天会自动把今天的日志改名为今天的日期。即，<File> 的日志都是当天的。-->
        <!--<File>logs/info.spring-boot-demo-logback.log</File>-->
        <!--滚动策略，按照时间滚动 TimeBasedRollingPolicy-->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
<!--            <fileNamePattern>${LOG_FILE_PATH}/${APP_NAME}-%d{yyyy-MM-dd}.%i.log</fileNamePattern>-->
            <fileNamePattern>logs/info/${APP_NAME}-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <!--只保留最近30天的日志-->
            <maxHistory>30</maxHistory>
            <!--用来指定日志文件的上限大小，那么到了这个值，就会删除旧的日志-->
            <!--<totalSizeCap>1GB</totalSizeCap>-->
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <!-- maxFileSize:这是活动文件的大小，默认值是10MB -->
                <maxFileSize>10MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
        </rollingPolicy>
        <!--        <encoder>-->
        <!--            <pattern>%date [%thread] %-5level [%logger{50}] %file:%line - %msg%n</pattern>-->
        <!--            <charset>UTF-8</charset> &lt;!&ndash; 此处设置字符集 &ndash;&gt;-->
        <!--        </encoder>-->
        <encoder>
            <pattern>${FILE_LOG_PATTERN}</pattern>
        </encoder>
    </appender>

    <appender name="FILE_ERROR" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <!--如果只是想要 Error 级别的日志，那么需要过滤一下，默认是 info 级别的，ThresholdFilter-->
        <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
            <level>Error</level>
        </filter>
        <!--日志名称，如果没有File 属性，那么只会使用FileNamePattern的文件路径规则如果同时有<File>和<FileNamePattern>，那么当天日志是<File>，明天会自动把今天的日志改名为今天的日期。即，<File> 的日志都是当天的。-->
        <!--<File>logs/error.spring-boot-demo-logback.log</File>-->
        <!--滚动策略，按照时间滚动 TimeBasedRollingPolicy-->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!--文件路径,定义了日志的切分方式——把每一天的日志归档到一个文件中,以防止日志填满整个磁盘空间-->
            <FileNamePattern>logs/error/${APP_NAME}-%d{yyyy-MM-dd}.%i.log</FileNamePattern>
            <!--只保留最近30天的日志-->
            <maxHistory>30</maxHistory>
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <!-- maxFileSize:这是活动文件的大小，默认值是10MB -->
                <maxFileSize>10MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
        </rollingPolicy>
        <encoder>
            <pattern>${FILE_LOG_PATTERN}</pattern>
        </encoder>
    </appender>
 
    <!-- 引入logstash依赖    -->
        <!-- 
        <dependency>
            <groupId>net.logstash.logback</groupId>
            <artifactId>logstash-logback-encoder</artifactId>
            <version>5.1</version>
        </dependency>    -->
    <!--业务日志输出到LogStash-->
    <appender name="LOG_STASH_BUSINESS" class="net.logstash.logback.appender.LogstashTcpSocketAppender">
        <destination>localhost:4560</destination>
        <encoder charset="UTF-8" class="net.logstash.logback.encoder.LoggingEventCompositeJsonEncoder">
            <providers>
                <timestamp>
                    <timeZone>Asia/Shanghai</timeZone>
                </timestamp>
                <!--自定义日志输出格式-->
                <pattern>
                    <pattern>
                        {
                        "project": "springbootdemo",
                        "level": "%level",
                        "createTime": "%d{yyyy-MM-dd HH:mm:ss.SSS}",
                        "service": "${APP_NAME:-}",
                        "pid": "${PID:-}",
                        "thread": "%thread",
                        "class": "%logger",
                        "message": "%message",
                        "stack_trace": "%exception{20}"
                        }
                    </pattern>
                </pattern>
            </providers>
        </encoder>
    </appender>

    <root>
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="FILE"/>
        <appender-ref ref="FILE_ERROR"/>
        <appender-ref ref="LOG_STASH_BUSINESS"/>
    </root>
</configuration>
```

## yml配置日志
```yaml
logging:
  level:
    root: info #日志配置,DEBUG,INFO,WARN,ERROR
```

如需要添加druid的sql输出则需要修改为：
```yaml
logging:
  level:
    root: info #日志配置,DEBUG,INFO,WARN,ERROR
    druid:
      sql:
        Statement: DEBUG
```

## 异步日志
系统中日志打印会严重影响到性能，所以通常要使用异步日志，此外，开发中会使用控制台输出日志，二生产中不需要，下面给出本人常用配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <include resource="org/springframework/boot/logging/logback/defaults.xml"/>
    <include resource="org/springframework/boot/logging/logback/console-appender.xml"/>
    <!--应用名称-->
    <property name="APP_NAME" value="gateway"/>
    <!--日志文件保存路径-->
    <property name="LOG_FILE_PATH" value="logs"/>
    <contextName>${APP_NAME}</contextName>

    <appender name="FILE_ERROR" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
            <level>Error</level>
        </filter>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <FileNamePattern>logs/gateway/error/${APP_NAME}-%d{yyyy-MM-dd}.%i.log</FileNamePattern>
            <maxHistory>30</maxHistory>
            <maxFileSize>2GB</maxFileSize>
        </rollingPolicy>
        <encoder>
            <pattern>${FILE_LOG_PATTERN}</pattern>
        </encoder>
    </appender>

    <appender name="accessLog" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <FileNamePattern>logs/gateway/access/access-%d{yyyy-MM-dd}.%i.log</FileNamePattern>
            <maxHistory>30</maxHistory>
            <maxFileSize>2GB</maxFileSize>
        </rollingPolicy>
        <encoder>
            <pattern>%msg%n</pattern>
        </encoder>
    </appender>

    <appender name="async" class="ch.qos.logback.classic.AsyncAppender">
        <appender-ref ref="accessLog"/>
    </appender>

    <logger name="reactor.netty.http.server.AccessLog" level="INFO" additivity="false">
        <appender-ref ref="async"/>
    </logger>

    <!-- 异步处理文件日志，提高生产环境性能 -->
    <appender name ="ASYNC_FILE" class= "ch.qos.logback.classic.AsyncAppender">
        <discardingThreshold>0</discardingThreshold>
        <queueSize>512</queueSize>
        <neverBlock>true</neverBlock>
        <appender-ref ref="FILE_ERROR"/>
    </appender>

    <root>
        <springProfile name="dev">
            <appender-ref ref="CONSOLE"/>
        </springProfile>
        <appender-ref ref="ASYNC_FILE"/>
    </root>
</configuration>
```

* springProfile: 读取spring.profiles.active设置的值，设置不同环境的不同逻辑。多环境用逗号隔开，也可使用 | !逻辑字符，如 springProfile name="dev | test"
* discardingThreshold 丢弃日志的阈值，为防止队列满后发生阻塞。默认队列剩余容量 ＜ 队列长度的20%，就会丢弃TRACE、DEBUG和INFO级日志 为0时不会丢弃日志
* includeCallerData 默认false：方法行号、方法名等信息不显示
* queueSize 控制阻塞队列大小，使用的ArrayBlockingQueue阻塞队列，默认容量256：内存中最多保存256条日志
* neverBlock 控制队列满时，加入的数据是否直接丢弃，不会阻塞等待，默认是false。队列满时，offer不阻塞，而put会阻塞;neverBlock为true时，使用offer

queueSize、discardingThreshold和neverBlock三参密不可分，务必按业务需求设置：
* 若优先绝对性能，设置neverBlock = true，永不阻塞
* 若优先绝不丢数据，设置discardingThreshold = 0，即使≤INFO级日志也不会丢。但最好把queueSize设置大一点，毕竟默认的queueSize显然太小，太容易阻塞。
* 若兼顾，可丢弃不重要日志，把queueSize设置大点，再设置合理的discardingThreshold

## MDC实现日志追踪

### 简介
MDC（Mapped Diagnostic Context，映射调试上下文）是 log4j 和 logback 提供的一种方便在多线程条件下记录日志的功能。某些应用程序采用多线程的方式来处理多个用户的请求。在一个用户的使用过程中，可能有多个不同的线程来进行处理。典型的例子是 Web 应用服务器。当用户访问某个页面时，应用服务器可能会创建一个新的线程来处理该请求，也可能从线程池中复用已有的线程。在一个用户的会话存续期间，可能有多个线程处理过该用户的请求。这使得比较难以区分不同用户所对应的日志。当需要追踪某个用户在系统中的相关日志记录时，就会变得很麻烦。

一种解决的办法是采用自定义的日志格式，把用户的信息采用某种方式编码在日志记录中。这种方式的问题在于要求在每个使用日志记录器的类中，都可以访问到用户相关的信息。这样才可能在记录日志时使用。这样的条件通常是比较难以满足的。MDC 的作用是解决这个问题。

MDC 可以看成是一个与当前线程绑定的哈希表，可以往其中添加键值对。MDC 中包含的内容可以被同一线程中执行的代码所访问。当前线程的子线程会继承其父线程中的 MDC 的内容。当需要记录日志时，只需要从 MDC 中获取所需的信息即可。MDC 的内容则由程序在适当的时候保存进去。对于一个 Web 应用来说，通常是在请求被处理的最开始保存这些数据。

### 优点
* 如果你的系统已经上线，突然有一天老板说我们增加一些用户数据到日志里分析一下。如果没有MDC我猜此时此刻你应该处于雪崩状态。MDC恰到好处的让你能够实现在日志上突如其来的一些需求
* 如果你是个代码洁癖，封装了公司LOG的操作，并且将处理线程跟踪日志号也封装了进去，但只有使用了你封装日志工具的部分才能打印跟踪日志号，其他部分(比如hibernate、mybatis、httpclient等等)日志都不会体现跟踪号。当然我们可以通过linux命令来绕过这些困扰。
* 使代码简洁、日志风格统一

### 使用
* clear() => 移除所有MDC
* get (String key) => 获取当前线程MDC中指定key的值
* getContext() => 获取当前线程MDC的MDC
* put(String key, Object o) => 往当前线程的MDC中存入指定的键值对
* remove(String key) => 删除当前线程MDC中指定的键值对
```java
            MDC.put("TRACEID",BaseUtils.getUuid());
            result = (Map<String, Object>) pjd.proceed();
            log.info("BaseUtils.getUuid()");
            MDC.remove("TRACEID");
```

```xml
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{50} - %msg%n - %X{TRACEID}</pattern>
        </encoder>
```

### 示例-链路追踪
在微服务中，链路追踪实现大致有两种，以ziplin为代表的日志链路追踪和以SkyWalking,pinpoing为代表的javaagent实现

使用MDC可以简单实现日志链路追踪，大致如下：

前台请求时在header中添加traceId属性，携带唯一id来到后台，通过日志记录的方式完成链路追踪

<details>
  <summary>MDC实现链路追踪</summary>

1. 项目中添加拦截器
```java
public class LogInterceptor implements HandlerInterceptor {
      @Override
      public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
          //如果有上层调用就用上层的ID
          String traceId = request.getHeader(BaseUtils.TRACE_ID);
          if (traceId == null) {
              traceId = BaseUtils.getUuid();
          }
          MDC.put(BaseUtils.TRACE_ID, traceId);
          return true;
      }
  
      @Override
      public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView)
              throws Exception {
      }
  
      @Override
      public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex)
              throws Exception {
          //调用结束后删除
          MDC.remove(BaseUtils.TRACE_ID);
      }
  }
```
此时，可以在aop中处理日志时获取traceId,记录日志

2. 解决子线程打印日志丢失traceId问题
子线程在打印日志的过程中traceId将丢失，解决方式为重写线程池.
```java
@Slf4j
public class VisiableThreadPoolTaskExecutor extends ThreadPoolTaskExecutor {

    private void showThreadPoolInfo(String prefix) {
        ThreadPoolExecutor threadPoolExecutor = getThreadPoolExecutor();
        log.info("{}, {},taskCount [{}], completedTaskCount [{}], activeCount [{}], queueSize [{}]",
                this.getThreadNamePrefix(),
                prefix,
                threadPoolExecutor.getTaskCount(),
                threadPoolExecutor.getCompletedTaskCount(),
                threadPoolExecutor.getActiveCount(),
                threadPoolExecutor.getQueue().size());
    }

    @Override
    public void execute(Runnable task) {
        showThreadPoolInfo("1. do execute");
        super.execute(ThreadMdcUtil.wrap(task, MDC.getCopyOfContextMap()));
    }

    @Override
    public void execute(Runnable task, long startTimeout) {
        showThreadPoolInfo("2. do execute");
        super.execute(task, startTimeout);
    }

    @Override
    public Future<?> submit(Runnable task) {
        showThreadPoolInfo("1. do submit");
        return super.submit(ThreadMdcUtil.wrap(task, MDC.getCopyOfContextMap()));
    }

    @Override
    public <T> Future<T> submit(Callable<T> task) {
        showThreadPoolInfo("2. do submit");
        return super.submit(ThreadMdcUtil.wrap(task, MDC.getCopyOfContextMap()));
    }

    @Override
    public ListenableFuture<?> submitListenable(Runnable task) {
        showThreadPoolInfo("1. do submitListenable");
        return super.submitListenable(task);
    }

    @Override
    public <T> ListenableFuture<T> submitListenable(Callable<T> task) {
        showThreadPoolInfo("2. do submitListenable");
        return super.submitListenable(task);
    }

}
```
说明：
* 继承ThreadPoolExecutor类，重新执行任务的方法
* 通过ThreadMdcUtil对任务进行一次包装
* 线程traceId封装工具类：ThreadMdcUtil.java
```java
public class ThreadMdcUtil {
    public static void setTraceIdIfAbsent() {
        if (MDC.get(BaseUtils.TRACE_ID) == null) {
            MDC.put(BaseUtils.TRACE_ID, BaseUtils.getUuid());
        }
    }

    public static <T> Callable<T> wrap(final Callable<T> callable, final Map<String, String> context) {
        return () -> {
            if (context == null) {
                MDC.clear();
            } else {
                MDC.setContextMap(context);
            }
            setTraceIdIfAbsent();
            try {
                return callable.call();
            } finally {
                MDC.clear();
            }
        };
    }

    public static Runnable wrap(final Runnable runnable, final Map<String, String> context) {
        return () -> {
            if (context == null) {
                MDC.clear();
            } else {
                MDC.setContextMap(context);
            }
            setTraceIdIfAbsent();
            try {
                runnable.run();
            } finally {
                MDC.clear();
            }
        };
    }
}
```
说明【以封装Runnable为例】：
* 判断当前线程对应MDC的Map是否存在，存在则设置
* 设置MDC中的traceId值，不存在则新生成，针对不是子线程的情况，如果是子线程，MDC中traceId不为null
* 执行run方法

3. 解决HTTP调用丢失traceId
在使用HTTP调用第三方服务接口时traceId将丢失，需要对HTTP调用工具进行改造，在发送时在request header中添加traceId，在下层被调用方添加拦截器获取header中的traceId添加到MDC中  
HTTP调用有多种方式，比较常见的有HttpClient、OKHttp、RestTemplate，所以只给出这几种HTTP调用的解决方式 

**HttpClient**  
实现HttpClient拦截器
```java
public class HttpClientTraceIdInterceptor implements HttpRequestInterceptor {
    @Override
    public void process(HttpRequest httpRequest, HttpContext httpContext) throws HttpException, IOException {
        String traceId = MDC.get(BaseUtils.TRACE_ID);
        //当前线程调用中有traceId，则将该traceId进行透传
        if (traceId != null) {
            //添加请求体
            httpRequest.addHeader(BaseUtils.TRACE_ID, traceId);
        }
    }
}
```
实现HttpRequestInterceptor接口并重写process方法

如果调用线程中含有traceId，则需要将获取到的traceId通过request中的header向下透传下去

为HttpClient添加拦截器  
```java
 private static CloseableHttpClient httpClient = HttpClientBuilder.create()
              .addInterceptorFirst(new HttpClientTraceIdInterceptor())
              .build();
```

**OKHttp**  
实现OKHttp拦截器  
```java
 public class OkHttpTraceIdInterceptor implements Interceptor {
      @Override
      public Response intercept(Chain chain) throws IOException {
          String traceId = MDC.get(BaseUtils.TRACE_ID);
          Request request = null;
          if (traceId != null) {
              //添加请求体
              request = chain.request().newBuilder().addHeader(BaseUtils.TRACE_ID, traceId).build();
          }
          Response originResponse = chain.proceed(request);
          return originResponse;
      }
  }
```
实现Interceptor拦截器，重写interceptor方法，实现逻辑和HttpClient差不多，如果能够获取到当前线程的traceId则向下透传  
为OkHttp添加拦截器  
```java
 private static OkHttpClient client = new OkHttpClient.Builder()
              .addNetworkInterceptor(new OkHttpTraceIdInterceptor())
              .build();
```

**RestTemplate**  
实现RestTemplate拦截器  
```java
 public class RestTemplateTraceIdInterceptor implements ClientHttpRequestInterceptor {
      @Override
      public ClientHttpResponse intercept(HttpRequest httpRequest, byte[] bytes, ClientHttpRequestExecution clientHttpRequestExecution) throws IOException {
          String traceId = MDC.get(BaseUtils.TRACE_ID);
          if (traceId != null) {
              httpRequest.getHeaders().add(BaseUtils.TRACE_ID, traceId);
          }
          return clientHttpRequestExecution.execute(httpRequest, bytes);
      }
  }
```
实现ClientHttpRequestInterceptor接口，并重写intercept方法，其余逻辑都是一样的  
为RestTemplate添加拦截器  
```java
 restTemplate.setInterceptors(Arrays.asList(new RestTemplateTraceIdInterceptor()));
```

**第三方服务拦截器**  
HTTP调用第三方服务接口全流程traceId需要第三方服务配合，第三方服务需要添加拦截器拿到request header中的traceId并添加到MDC中

```java
public class LogInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        //如果有上层调用就用上层的ID
        String traceId = request.getHeader(BaseUtils.TRACE_ID);
        if (traceId == null) {
            traceId = TraceIdUtils.getTraceId();
        }
        
        MDC.put(BaseUtils.TRACE_ID, traceId);
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView)
            throws Exception {
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex)
            throws Exception {
        MDC.remove(BaseUtils.TRACE_ID);
    }
}
```

</details> 

## logj2
参考页面

[Spring Boot 2.x中如何使用Log4j2记录日志](https://mp.weixin.qq.com/s/3zE4B1n80gJkP4j0oheaFw ':target=_blank')  
[springboot使用log4j2](https://blog.csdn.net/weixin_45414738/article/details/108874711 ':target=_blank')  
[Springboot 2.x 使用 Log4j2 异步打印日志](https://cloud.tencent.com/developer/article/1767713 ':target=_blank')  
[配置Log4j2，实现不同环境日志打印](https://www.cnblogs.com/cicada-smile/p/10992157.html ':target=_blank')  
[springboot log4j2.xml读取application.yml中的属性值](https://blog.csdn.net/ajdxwz/article/details/92101822 ':target=_blank')


