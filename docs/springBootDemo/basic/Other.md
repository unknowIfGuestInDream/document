## springBoot设置启动样式

将自己的启动样式文件banner.txt放入默认路径resources下。  
如果自定义文件位置&文件名的话 需要修改yml配置：
```yaml
spring:
  banner:
    location: static/public/banner.txt
```

## springBoot设置时区

```yaml
spring:
  jackson:
    date-format: yyyy/MM/dd HH:mm:ss
    time-zone: GMT+8
```

## 多个配置文件

用于切换生产环境与测试环境配置，或者将较长的配置分离出去。

```yaml
spring:
  profiles:
    active: druid
    #切换配置文件
  #    spring.profiles.include: druid,ddd
```

## 文件上传限制

```yaml
spring:
  servlet:
    multipart:
      enabled: true
      max-file-size: 10MB 
      max-request-size: 20MB
```