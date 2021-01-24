> 我们都知道，一个程序的瓶颈通常都在数据库，很多场景需要获取相同的数据。比如网站页面数据等，需要一次次的请求数据库，导致大部分时间都浪费在数据库查询和方法调用上，这时就可以利用到缓存来缓解这个问题。

新增依赖:

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-cache</artifactId>
        </dependency>
```