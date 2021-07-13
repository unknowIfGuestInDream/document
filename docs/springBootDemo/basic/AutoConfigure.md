> @AutoConfigureAfter, @AutoConfigureBefore, @AutoConfigureOrder 是 spring-boot-autoconfigure包下的注解
  其作用顾名思义，将在SpringBoot项目中的配置类进行排序

!> SpringBoot 只会对spring.factories文件读取到的配置类进行排序。

![](../../images/autoConfigure/autoConfigure1.png)

## @AutoConfigureAfter和@AutoConfigureBefore

1、创建META-INF/spring.factories文件

![](../../images/autoConfigure/autoConfigure2.png)

```
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
com.tang.starter.config.ExampleAutoConfigure,\
com.tang.starter.config.ConfigurationA,\
com.tang.starter.config.ConfigurationB
```

2、添加@AutoConfigureAfter或@AutoConfigureBefore

![](../../images/autoConfigure/autoConfigure3.png)

![](../../images/autoConfigure/autoConfigure4.png)

## @AutoConfigureOrder

1、创建META-INF/spring.factories文件

2、添加@AutoConfigureOrder

![](../../images/autoConfigure/autoConfigure5.png)

AutoConfigureOrder后的值越小，越靠前加载