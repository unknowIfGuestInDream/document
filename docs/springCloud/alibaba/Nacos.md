> Spring Cloud Alibaba 致力于提供微服务开发的一站式解决方案，Nacos 作为其核心组件之一，可以作为注册中心和配置中心使用，本文将对其用法进行详细介绍。

## 简介

Nacos 致力于帮助您发现、配置和管理微服务。Nacos 提供了一组简单易用的特性集，帮助您快速实现动态服务发现、服务配置、服务元数据及流量管理。

Nacos 具有如下特性:
* 服务发现和服务健康监测：支持基于DNS和基于RPC的服务发现，支持对服务的实时的健康检查，阻止向不健康的主机或服务实例发送请求；
动态配置服务：动态配置服务可以让您以中心化、外部化和动态化的方式管理所有环境的应用配置和服务配置；
* 动态 DNS 服务：动态 DNS 服务支持权重路由，让您更容易地实现中间层负载均衡、更灵活的路由策略、流量控制以及数据中心内网的简单DNS解析服务；
* 服务及其元数据管理：支持从微服务平台建设的视角管理数据中心的所有服务及元数据。
使用Nacos作为注册中心

## 服务注册新增元数据

```java
import com.alibaba.cloud.nacos.ConditionalOnNacosDiscoveryEnabled;
import com.alibaba.cloud.nacos.NacosDiscoveryProperties;
import com.alibaba.cloud.nacos.NacosServiceManager;
import com.alibaba.cloud.nacos.discovery.NacosWatch;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.AutoConfigureBefore;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.cloud.client.CommonsClientAutoConfiguration;
import org.springframework.cloud.client.discovery.simple.SimpleDiscoveryClientAutoConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskScheduler;

import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * nacos客户端注册至服务端时，更改服务详情中的元数据
 */
@Configuration
@ConditionalOnNacosDiscoveryEnabled
@AutoConfigureBefore({SimpleDiscoveryClientAutoConfiguration.class, CommonsClientAutoConfiguration.class})
public class NacosDiscoveryClientConfiguration {

    /**
     * 程序环境
     */
    @Value("${spring.profiles.active:prod}")
    private String profiles;

    /**
     * 取操作系统版本
     */
    @Value("#{systemProperties['os.name']}")
    private String systemName;

    @Bean
    @ConditionalOnMissingBean
    public NacosDiscoveryProperties nacosProperties() {
        return new NacosDiscoveryProperties();
    }

    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnProperty(value = {"spring.cloud.nacos.discovery.watch.enabled"}, matchIfMissing = true)
    public NacosWatch nacosWatch(NacosServiceManager nacosServiceManager, NacosDiscoveryProperties nacosProperties, ObjectProvider<ThreadPoolTaskScheduler> taskScheduler) {
        //更改服务详情中的元数据，增加服务注册时间
        nacosProperties.getMetadata().remove("preserved.register.source");
        nacosProperties.getMetadata().put("startup.time", new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date()));
        nacosProperties.getMetadata().put("env", profiles);
        nacosProperties.getMetadata().put("systemName", systemName);
        return new NacosWatch(nacosServiceManager, nacosProperties, taskScheduler);
    }

}
```

## 共享配置
示例配置

```yaml
spring:
  profiles:
    active: dev
  application:
    name: xxx
  cloud:
    nacos:
      config:
        server-addr: http://localhost:8848
        file-extension: yaml
        group: DEFAULT_GROUP
        refresh-enabled: true
        namespace: aaaaa
        username: xxx
        password: xxx
        extension-configs:
          - data-id: pmnew-share-dev.yaml
            group: DEFAULT_GROUP
            refresh: true
        shared-configs[0]:
          data-id: pearl-common.yml # 配置文件名-Data Id
          group: PEARL_GROUP   # 默认为DEFAULT_GROUP
          refresh: false   # 是否动态刷新，默认为false
```

共享配置有 shared-configs 和 extension-configs属性，他们配制方法相同有两种写法，如上文配置

优先级：

file-extension > extension-configs > shared-configs  共享配置下标数字越大，优先级越高

## nacos2.0长连接配置

可通过指定nacos-client方式，提前使用Nacos2.0长连接功能
```xml
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        <version>2.2.5.RELEASE</version>
        <exclusions>
            <exclusion>
                <groupId>com.alibaba.nacos</groupId>
                <artifactId>nacos-client</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
        <version>2.2.5.RELEASE</version>
        <exclusions>
            <exclusion>
                <groupId>com.alibaba.nacos</groupId>
                <artifactId>nacos-client</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
    <dependency>
        <groupId>com.alibaba.nacos</groupId>
        <artifactId>nacos-client</artifactId>
        <version>2.0.1</version>
    </dependency>
```

## nacos后台启动
```shell script
nohup sh startup.sh -m standalone &
```

