> Spring Boot Admin 可以对SpringBoot应用的各项指标进行监控，可以作为微服务架构中的监控中心来使用，本文将对其用法进行详细介绍。

## 简介

Spring Boot Admin 简介
SpringBoot应用可以通过Actuator来暴露应用运行过程中的各项指标，Spring Boot Admin通过这些指标来监控SpringBoot应用，
然后通过图形化界面呈现出来。Spring Boot Admin不仅可以监控单体应用，还可以和Spring Cloud的注册中心相结合来监控微服务应用。

Spring Boot Admin 可以提供应用的以下监控信息：
* 监控应用运行过程中的概览信息；
* 度量指标信息，比如JVM、Tomcat及进程信息；
* 环境变量信息，比如系统属性、系统环境变量以及应用配置信息；
* 查看所有创建的Bean信息；
* 查看应用中的所有配置信息；
* 查看应用运行日志信息；
* 查看JVM信息；
* 查看可以访问的Web端点；
* 查看HTTP跟踪信息。