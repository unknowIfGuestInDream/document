> Spring Cloud Consul 为 SpringBoot 应用提供了 Consul的支持，Consul既可以作为注册中心使用，也可以作为配置中心使用，本文将对其用法进行详细介绍。

## 简介

Consul是HashiCorp公司推出的开源软件，提供了微服务系统中的服务治理、配置中心、控制总线等功能。
这些功能中的每一个都可以根据需要单独使用，也可以一起使用以构建全方位的服务网格，
总之Consul提供了一种完整的服务网格解决方案。

Spring Cloud Consul 具有如下特性：
* 支持服务治理：Consul作为注册中心时，微服务中的应用可以向Consul注册自己，并且可以从Consul获取其他应用信息；
* 支持客户端负责均衡：包括Ribbon和Spring Cloud LoadBalancer；
* 支持Zuul：当Zuul作为网关时，可以从Consul中注册和发现应用；
* 支持分布式配置管理：Consul作为配置中心时，使用键值对来存储配置信息；
* 支持控制总线：可以在整个微服务系统中通过 Control Bus 分发事件消息。