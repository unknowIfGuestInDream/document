> Spring Cloud OpenFeign 是声明式的服务调用工具，它整合了Ribbon和Hystrix，拥有负载均衡和服务容错功能，本文将对其用法进行详细介绍。

## 简介

Feign是声明式的服务调用工具，我们只需创建一个接口并用注解的方式来配置它，就可以实现对某个服务接口的调用，
简化了直接使用RestTemplate来调用服务接口的开发量。Feign具备可插拔的注解支持，
同时支持Feign注解、JAX-RS注解及SpringMvc注解。
当使用Feign时，Spring Cloud集成了Ribbon和Eureka以提供负载均衡的服务调用及基于Hystrix的服务容错保护功能。

## 示例配置
```java
@Component
public class FeignConfig implements RequestInterceptor {

    @Override
    public void apply(RequestTemplate requestTemplate) {
        RequestAttributes requestAttributes = RequestContextHolder.getRequestAttributes();
        if (Objects.nonNull(requestAttributes)) {
            ServletRequestAttributes var2 = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
            HttpServletRequest var3 = var2.getRequest();
            requestTemplate.header("token", new String[]{CookieUtil.getCookieByName(var3, "token")});
            requestTemplate.header("requestType", new String[]{"feign"});
        } else {
            //非web调用feign，RequestContextHolder.getRequestAttributes()是null的，所以需要在空的情况赋值一次
            RequestContextHolder.setRequestAttributes(new ServletRequestAttributes(new MockHttpServletRequest()));
        }
    }
}
```