> spring2.x内嵌tomcat默认使用NIO模式

依赖版本2.5.1
```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
```

## 配置
参数 | 介绍
----|----
<font color=FF0000>server.tomcat.accept-count = 100</font> | 所有可能的请求处理线程正在使用时，传入连接请求的最大队列长度
server.tomcat.accesslog.buffered = true	 | 缓冲区输出，使其只被定期刷新
server.tomcat.accesslog.directory = logs | 创建日志文件的目录可以相对于tomcat base dir或absolute
server.tomcat.accesslog.enabled = false	 | 启用访问日志
server.tomcat.accesslog.file-date-format = .yyyy-MM-dd | 要在日志文件名中放置的日期格式
server.tomcat.accesslog.pattern = common | 访问日志的格式模式
server.tomcat.accesslog.prefix = access_log | 日志文件名前缀
server.tomcat.accesslog.rename-on-rotate = false | 将文件名中的日期戳延迟到旋转时间
server.tomcat.accesslog.request-attributes-enabled = false | 设置请求的IP地址，主机名，协议和端口的请求属性
server.tomcat.accesslog.rotate = true | 启用访问日志轮换
server.tomcat.accesslog.suffix = .log | 日志文件名后缀
server.tomcat.additional-tld-skip-patterns | 匹配要忽略TLD扫描的jar的附加模式的逗号分隔列表
server.tomcat.background-processor-delay = 10s	 | 匹配要忽略TLD扫描的jar的附加模式的逗号分隔列表
<font color=FF0000>server.tomcat.basedir</font> | Tomcat基本目录。如果未指定，将使用临时目录
<font color=FF0000>server.tomcat.max-connections = 8192</font> | 服务器在任何给定时间接受和处理的最大连接数 
server.tomcat.max-http-post-size = 2MB | HTTP帖子内容的最大大小
<font color=FF0000>server.tomcat.threads.max = 200</font> | 最大工作线程数
<font color=FF0000>server.tomcat.threads.min-spare = 10</font> | 最小工作线程数
server.tomcat.port-header = X-Forwarded-Port | 用于覆盖原始端口值的HTTP头的名称
server.tomcat.remoteip.protocol-header | 保存传入协议的头,通常命名为"X-Forwarded-Proto"
server.tomcat.remoteip.protocol-header-https-value = https	| 指示传入请求使用SSL的协议头的值
server.tomcat.redirect-context-root = true	| 是否通过在路径上附加/重定向到上下文根的请求
server.tomcat.remoteip.remote-ip-header	| 从中提取远程ip的HTTP头的名称。例如X-FORWARDED-FOR
server.tomcat.uri-encoding = UTF-8	| 用于解码URI的字符编码

参数配置建议  
* server.tomcat.accept-count： 队列做缓冲池用，但也不能无限长，消耗内存，出队入队也耗CPU，生产环境建议1000，触发的请求超过(最大工作线程数+等待队列长度)后拒绝处理
* server.tomcat.threads.max：最大工作线程数，默认200, 建议为cpu核心数的200-250倍
* server.tomcat.threads.min-spare：最小工作线程数，初始化分配线程数，默认10, 生产环境可以给大一点，以应对启动后大量进入的用户

## 开启apr模式
从操作系统级别解决异步IO问题，大幅度的提高服务器的处理和响应性能， 也是Tomcat运行高并发应用的首选模式。

### windows下开启
windows下安装配置native和apr只需要在环境变量path里能够找到 tcnative-1.dll即可，这个文件在 高版本tomcat\bin\ 目录下会存在  
内置tomcat版本是9，下载对应tomcat包，将bin目录下的tcnative-1.dll拷贝到jdk安装目录的bin目录下

内置tomcat使用Http11AprProtocol配置
```java
import lombok.extern.slf4j.Slf4j;
import org.apache.catalina.LifecycleListener;
import org.apache.catalina.core.AprLifecycleListener;
import org.springframework.boot.web.embedded.tomcat.TomcatServletWebServerFactory;
import org.springframework.boot.web.servlet.server.ServletWebServerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@Slf4j
public class TomcatConfig {

    @Bean
    public ServletWebServerFactory servletWebServerFactory() {
        TomcatServletWebServerFactory container = new TomcatServletWebServerFactory();
        LifecycleListener arpLifecycle = new AprLifecycleListener();
        container.setProtocol("org.apache.coyote.http11.Http11AprProtocol");
        container.addContextLifecycleListeners(arpLifecycle);
        return container;
    }

}
```

启动测试即可

### Linux下开启
[官网文档](http://tomcat.apache.org/tomcat-8.0-doc/apr.html#Linux  ':target=_blank')
[安装配置native和apr](https://tomcat.apache.org/native-doc/  ':target=_blank')
[参考配置](https://blog.csdn.net/xyang81/article/details/51502766  ':target=_blank')

