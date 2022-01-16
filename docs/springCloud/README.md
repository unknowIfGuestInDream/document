# SpringCloud

## 简介

协调任何服务，简化分布式系统开发。

构建分布式系统不应该是复杂的，SpringCloud对常见的分布式系统模式提供了简单易用的编程模型，帮助开发者构建弹性、 可靠、协调的应用程序。
SpringCloud是在SpringBoot的基础上构建的，使开发者可以轻松入门并快速提高工作效率。 SpringCloud为开发人员提供了快速构建分布式系统架构的工具，例如配置管理，服务发现，断路器，智能路由，微代理，控制总线，
一次性令牌，全局锁定，领导选举，分布式会话，集群状态等。

springBoot与springCloud版本对应可以查看[https://start.spring.io/actuator/info](https://start.spring.io/actuator/info ':target=_blank')

下图作为参照

<details>
  <summary>示例json,最新对应关系请参照官网信息</summary>

```json
{
  "git": {
    "branch": "a158727ef939932ecf8f5e2bc2c4cf34e34309fd",
    "commit": {
      "id": "a158727",
      "time": "2022-01-11T09:03:51Z"
    }
  },
  "build": {
    "version": "0.0.1-SNAPSHOT",
    "artifact": "start-site",
    "versions": {
      "spring-boot": "2.6.2",
      "initializr": "0.12.0-SNAPSHOT"
    },
    "name": "start.spring.io website",
    "time": "2022-01-11T09:04:53.380Z",
    "group": "io.spring.start"
  },
  "bom-ranges": {
    "azure": {
      "3.2.0": "Spring Boot >=2.3.0.M1 and <2.4.0-M1",
      "3.5.0": "Spring Boot >=2.4.0.M1 and <2.5.0-M1",
      "3.10.0": "Spring Boot >=2.5.0.M1 and <2.6.0-M1"
    },
    "codecentric-spring-boot-admin": {
      "2.4.3": "Spring Boot >=2.3.0.M1 and <2.5.0-M1",
      "2.5.5": "Spring Boot >=2.5.0.M1 and <2.6.0-M1",
      "2.6.0": "Spring Boot >=2.6.0.M1 and <2.7.0-M1"
    },
    "solace-spring-boot": {
      "1.1.0": "Spring Boot >=2.3.0.M1 and <2.6.0-M1"
    },
    "solace-spring-cloud": {
      "1.1.1": "Spring Boot >=2.3.0.M1 and <2.4.0-M1",
      "2.1.0": "Spring Boot >=2.4.0.M1 and <2.6.0-M1"
    },
    "spring-cloud": {
      "Hoxton.SR12": "Spring Boot >=2.2.0.RELEASE and <2.4.0.M1",
      "2020.0.5": "Spring Boot >=2.4.0.M1 and <2.6.0-M1",
      "2021.0.0-M1": "Spring Boot >=2.6.0-M1 and <2.6.0-M3",
      "2021.0.0-M3": "Spring Boot >=2.6.0-M3 and <2.6.0-RC1",
      "2021.0.0-RC1": "Spring Boot >=2.6.0-RC1 and <2.6.1",
      "2021.0.0": "Spring Boot >=2.6.1 and <2.6.3-SNAPSHOT",
      "2021.0.1-SNAPSHOT": "Spring Boot >=2.6.3-SNAPSHOT and <2.7.0-M1"
    },
    "spring-cloud-gcp": {
      "2.0.7": "Spring Boot >=2.4.0-M1 and <2.6.0-M1"
    },
    "spring-cloud-services": {
      "2.3.0.RELEASE": "Spring Boot >=2.3.0.RELEASE and <2.4.0-M1",
      "2.4.1": "Spring Boot >=2.4.0-M1 and <2.5.0-M1",
      "3.3.0": "Spring Boot >=2.5.0-M1 and <2.6.0-M1"
    },
    "spring-geode": {
      "1.3.12.RELEASE": "Spring Boot >=2.3.0.M1 and <2.4.0-M1",
      "1.4.13": "Spring Boot >=2.4.0-M1 and <2.5.0-M1",
      "1.5.8": "Spring Boot >=2.5.0-M1 and <2.6.0-M1",
      "1.6.2": "Spring Boot >=2.6.0-M1 and <2.7.0-M1"
    },
    "vaadin": {
      "14.8.1": "Spring Boot >=2.1.0.RELEASE and <2.8.0-M1"
    },
    "wavefront": {
      "2.0.2": "Spring Boot >=2.1.0.RELEASE and <2.4.0-M1",
      "2.1.1": "Spring Boot >=2.4.0-M1 and <2.5.0-M1",
      "2.2.2": "Spring Boot >=2.5.0-M1 and <2.7.0-M1"
    }
  },
  "dependency-ranges": {
    "native": {
      "0.9.0": "Spring Boot >=2.4.3 and <2.4.4",
      "0.9.1": "Spring Boot >=2.4.4 and <2.4.5",
      "0.9.2": "Spring Boot >=2.4.5 and <2.5.0-M1",
      "0.10.0": "Spring Boot >=2.5.0-M1 and <2.5.2",
      "0.10.1": "Spring Boot >=2.5.2 and <2.5.3",
      "0.10.2": "Spring Boot >=2.5.3 and <2.5.4",
      "0.10.3": "Spring Boot >=2.5.4 and <2.5.5",
      "0.10.4": "Spring Boot >=2.5.5 and <2.5.6",
      "0.10.5": "Spring Boot >=2.5.6 and <2.5.9-SNAPSHOT",
      "0.10.6-SNAPSHOT": "Spring Boot >=2.5.9-SNAPSHOT and <2.6.0-M1",
      "0.11.0-M1": "Spring Boot >=2.6.0-M1 and <2.6.0-RC1",
      "0.11.0-M2": "Spring Boot >=2.6.0-RC1 and <2.6.0",
      "0.11.0-RC1": "Spring Boot >=2.6.0 and <2.6.1",
      "0.11.0": "Spring Boot >=2.6.1 and <2.6.2",
      "0.11.1": "Spring Boot >=2.6.2 and <2.6.3-SNAPSHOT",
      "0.11.2-SNAPSHOT": "Spring Boot >=2.6.3-SNAPSHOT and <2.7.0-M1"
    },
    "okta": {
      "1.4.0": "Spring Boot >=2.2.0.RELEASE and <2.4.0-M1",
      "1.5.1": "Spring Boot >=2.4.0-M1 and <2.4.1",
      "2.0.1": "Spring Boot >=2.4.1 and <2.5.0-M1",
      "2.1.4": "Spring Boot >=2.5.0-M1 and <2.6.0-M1"
    },
    "mybatis": {
      "2.1.4": "Spring Boot >=2.1.0.RELEASE and <2.5.0-M1",
      "2.2.1": "Spring Boot >=2.5.0-M1"
    },
    "camel": {
      "3.5.0": "Spring Boot >=2.3.0.M1 and <2.4.0-M1",
      "3.10.0": "Spring Boot >=2.4.0.M1 and <2.5.0-M1",
      "3.13.0": "Spring Boot >=2.5.0.M1 and <2.6.0-M1",
      "3.14.0": "Spring Boot >=2.6.0.M1 and <2.7.0-M1"
    },
    "picocli": {
      "4.6.2": "Spring Boot >=2.4.0.RELEASE and <2.6.0-M1"
    },
    "open-service-broker": {
      "3.2.0": "Spring Boot >=2.3.0.M1 and <2.4.0-M1",
      "3.3.1": "Spring Boot >=2.4.0-M1 and <2.5.0-M1",
      "3.4.0-M2": "Spring Boot >=2.5.0-M1 and <2.6.0-M1"
    }
  }
}
```

</details> 