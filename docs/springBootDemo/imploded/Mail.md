> 在项目的维护过程中，我们通常会在应用中加入短信或者邮件预警功能，比如当应用出现异常宕机时应该及时地将预警信息发送给运维或者开发人员，本文将介绍如何在Spring Boot中发送邮件。在Spring Boot中发送邮件使用的是Spring提供的org.springframework.mail.javamail.JavaMailSender，其提供了许多简单易用的方法，可发送简单的邮件、HTML格式的邮件、带附件的邮件，并且可以创建邮件模板。

引入依赖:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-mail</artifactId>
</dependency>
```

邮件配置

```yaml
spring:
  mail:
    host: smtp.163.com
    username: 你的账号
    password: 你的密码(邮件开启smtp的密码)
    default-encoding: UTF-8
    properties:
      mail:
        display:
          sendmail: spring-boot-demo
        smtp:
          ssl: true
          auth: true
          starttls:
            enable: true
            required: true
```

邮箱服务器地址:
* QQ smtp.qq.com
* sina smtp.sina.cn
* aliyun smtp.aliyun.com
* 163 smtp.163.com