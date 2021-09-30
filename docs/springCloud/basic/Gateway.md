> Spring Cloud Gateway 为 SpringBoot 应用提供了API网关支持，具有强大的智能路由与过滤器功能，本文将对其用法进行详细介绍。

## 简介

Gateway是在Spring生态系统之上构建的API网关服务，基于Spring 5，Spring Boot 2和 Project Reactor等技术。
Gateway旨在提供一种简单而有效的方式来对API进行路由，以及提供一些强大的过滤器功能， 例如：熔断、限流、重试等。

Spring Cloud Gateway 具有如下特性：
* 基于Spring Framework 5, Project Reactor 和 Spring Boot 2.0 进行构建；
* 动态路由：能够匹配任何请求属性；
* 可以对路由指定 Predicate（断言）和 Filter（过滤器）；
* 集成Hystrix的断路器功能；
* 集成 Spring Cloud 服务发现功能；
* 易于编写的 Predicate（断言）和 Filter（过滤器）；
* 请求限流功能；
* 支持路径重写。

## 示例配置

bootstrap.yml

```yaml
spring:
  ## 切换生产环境时 profiles属性注释
  profiles:
    active: dev
  application:
    name: newangels-gateway
  cloud:
    nacos:
      config:
        server-addr: 10.18.26.213:8848
        file-extension: yaml
        group: DEFAULT_GROUP
        refresh-enabled: true
```

newangels-gateway-dev.yaml

```yaml
server:
  port: 8701
spring:
  cloud:
    nacos:
      discovery:
        server-addr: 10.18.26.213:8848
    gateway:
      discovery:
        locator:
          enabled: true
          lower-case-service-id: true
      globalcors:
        cors-configurations:
          '[/**]':
            allowedHeaders: '*'
            allowedOrigins: '*'
            allowedMethods: '*'                      
  servlet:
    multipart:
      enabled: true
      max-file-size: 31457280
      max-request-size: 31457280
  jackson:
    date-format: yyyy/MM/dd HH:mm:ss
    time-zone: GMT+8
management:
  endpoints:
    web:
      exposure:
        include: '*'
  endpoint:
    health:
      show-details: always
```

gateway默认cors配置比较简单，通常选择自定义配置
```java
@Configuration
public class CorsConfig {

    @Bean
    public CorsWebFilter corsWebFilter() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.addAllowedHeader("*");
        configuration.addAllowedMethod("*");
        configuration.addAllowedOrigin("*");
        // 是否允许携带cookie跨域
        configuration.setAllowCredentials(true);
        source.registerCorsConfiguration("/**", configuration);
        return new CorsWebFilter(source);
    }

}
```

## 开启Reactor Netty日志
logback-spring.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <include resource="org/springframework/boot/logging/logback/defaults.xml"/>
    <include resource="org/springframework/boot/logging/logback/console-appender.xml"/>
    <springProperty scop="context" name="spring.application.name" source="spring.application.name" defaultValue=""/>
    <!--应用名称-->
    <property name="APP_NAME" value="${spring.application.name}"/>
    <!--日志文件保存路径-->
    <property name="LOG_FILE_PATH" value="logs"/>
    <contextName>${APP_NAME}</contextName>

    <appender name="accessLog" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <FileNamePattern>logs/${APP_NAME}/access/access-%d{yyyy-MM-dd}.%i.log</FileNamePattern>
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
</configuration>
```

启动命令新增 -Dreactor.netty.http.server.accessLogEnabled=true 启动日志
```shell script
java -Dreactor.netty.http.server.accessLogEnabled=true -jar gateway.jar
```