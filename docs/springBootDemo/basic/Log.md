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

## yml配置日志：
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