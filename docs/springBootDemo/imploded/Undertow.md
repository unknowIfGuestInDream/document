> 在 Spring Boot 框架中，我们使用最多的是 Tomcat，这是 Spring Boot 默认的容器技术，
>而且是内嵌式的 Tomcat。同时，Spring Boot 也支持 Undertow 容器，
>我们可以很方便的用 Undertow 替换 Tomcat，而 Undertow 的性能和内存使用方面都优于Tomcat

**1、引入maven依赖**  
版本2.5.1
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <!-- 默认是使用的tomcat -->
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<!-- undertow容器支持 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-undertow</artifactId>
</dependency>
```

**2、undertow的基本配置**
```yaml
server:
  undertow:
    accesslog:
      enabled: false # 是否打开 undertow 日志，默认为 false
      dir: logs # 设置访问日志所在目录
    threads:
      io: 4 # 指定工作者线程的 I/0 线程数，默认为 2 或者 CPU 的个数
      worker: 256 # 指定工作者线程个数，默认为 I/O 线程个数的 8 倍
    buffer-size: 1024 # 这些buffer会用于服务器连接的IO操作,有点类似netty的池化内存管理；
    direct-buffers: true # 是否分配的直接内存(NIO直接分配的堆外内存)
```

**3、一个特别的报错警告**
解决使用undertow容器报io.undertow.websockets.jsr -

UT026010: Buffer pool was not set on WebSocketDeploymentInfo, the default pool will be used  
处理：  
新增一个component注解的类，具体如下：
```java
@Component
public class UndertowPoolCustomizer implements WebServerFactoryCustomizer<UndertowServletWebServerFactory> {

    @Override
    public void customize(UndertowServletWebServerFactory factory) {
        factory.addDeploymentInfoCustomizers(deploymentInfo -> {
            WebSocketDeploymentInfo webSocketDeploymentInfo = new WebSocketDeploymentInfo();
            webSocketDeploymentInfo.setBuffers(new DefaultByteBufferPool(false, 1024));
            deploymentInfo.addServletContextAttribute("io.undertow.websockets.jsr.WebSocketDeploymentInfo", webSocketDeploymentInfo);
        });
    }
}
```