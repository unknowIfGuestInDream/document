> 当我们构建一个 Spring 应用的时候，有时我们想在满足指定条件的时候才将某个 bean 加载到应用上下文中， 在Spring 4.0 时代，我们可以通过 @Conditional 注解来实现这类操作  
> @Conditional系列注解需结合@Configuration一起使用 

**注解详解**

Spring Boot 对 @Conditional 注解为我们做了细化，这些注解都定义在 org.springframework.boot.autoconfigure.condition package 下

https://www.1024sky.cn/blog/article/614

https://www.cnblogs.com/qdhxhz/p/11020434.html

https://cloud.tencent.com/developer/article/1490442

## @ConditionalOnProperty

## @ConditionalOnBean 和 ConditionalOnMissingBean

## @ConditionalOnClass 和 @ConditionalOnMissingClass

## @ConditionalOnExpression

## @ConditionalOnSingleCandidate

## @ConditionalOnResource

## @ConditionalOnJndi

## @ConditionalOnJava

## @ConditionalOnWebApplication 和 @ConditionalOnNotWebApplication

## @ConditionalOnCloudPlatform

## 组合条件

