> RestTemplate是Spring提供的用于访问Rest服务的客户端，RestTemplate提供了多种便捷访问远程Http服务的方法,能够大大提高客户端的编写效率。

需要引入依赖

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
```

## 简述
> RestTemplate是Spring用于同步client端的核心类，简化了与http服务的通信，并满足RestFul原则，程序代码可以给它提供URL，并提取结果。默认情况下，RestTemplate默认依赖jdk的HTTP连接工具。当然你也可以 通过setRequestFactory属性切换到不同的HTTP源，比如Apache HttpComponents、Netty和OkHttp。

RestTemplate能大幅简化了提交表单数据的难度，并且附带了自动转换JSON数据的功能，但只有理解了HttpEntity的组成结构（header与body），且理解了与uriVariables之间的差异，才能真正掌握其用法。这一点在Post请求更加突出

该类的入口主要是根据HTTP的六个方法制定：

HTTP method | RestTemplate methods
----|----
DELETE | delete
GET | getForObject
GET | getForEntity
HEAD | headForHeaders
OPTIONS | optionsForAllow
POST | postForLocation
POST | postForObject
POST | postForEntity
PUT | put
any | exchange
any | execute

## 配置
需要配置后才可以使用RestTemplate

```java
@Configuration
public class HttpConfig {
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

RestTemplate默认使用
进入RestTemplate源码会发现，RestTemplate默认使用ISO_8859_1编码

<details>
  <summary>展开</summary>
  
```markdown
public RestTemplate() {
        this.messageConverters = new ArrayList();
        this.errorHandler = new DefaultResponseErrorHandler();
        this.headersExtractor = new RestTemplate.HeadersExtractor();
        this.messageConverters.add(new ByteArrayHttpMessageConverter());
        this.messageConverters.add(new StringHttpMessageConverter());
        this.messageConverters.add(new ResourceHttpMessageConverter(false));
```

进入 StringHttpMessageConverter类源码会发现

```markdown
    public StringHttpMessageConverter() {
        this(DEFAULT_CHARSET);
    }

    static {
        DEFAULT_CHARSET = StandardCharsets.ISO_8859_1;
    }
```
  
</details>

如果需要修改RestTemplate编码为UTF-8, 可以修改配置类

```java
@Configuration
public class HttpConfig {

    @Bean
    public RestTemplate restTemplate() {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.getMessageConverters().set(1, new StringHttpMessageConverter(StandardCharsets.UTF_8));
        return restTemplate;
    }
}
```

但是更推荐以下方式:

```java
@Configuration
public class HttpConfig {

    @Bean
    public RestTemplate restTemplate() {
        RestTemplate restTemplate = new RestTemplate();
        //修改为UTF-8编码
        List<HttpMessageConverter<?>> messageConverters = restTemplate.getMessageConverters();
        for (int i = 0; i < messageConverters.size(); i++) {
            HttpMessageConverter<?> httpMessageConverter = messageConverters.get(i);
            if (httpMessageConverter.getClass().equals(StringHttpMessageConverter.class)) {
                messageConverters.set(i, new StringHttpMessageConverter(StandardCharsets.UTF_8));
            }
        }
        return restTemplate;
    }
}
```

## 调用403错误
这个时候，需要在请求头中加上user-agent属性来假装成浏览器欺骗服务器

```markdown
    private final RestTemplate restTemplate;

    @Override
    public Map<String, Object> selectDateInfo(LocalDate localDate) {
        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
        headers.add("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36");
        HttpEntity<String> entity = new HttpEntity<>("parameters", headers);

        ResponseEntity<HashMap> response = restTemplate.exchange("http://xxx/api/info/{date}", HttpMethod.GET, entity, HashMap.class,
                LocalDate.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd")));
        return response.getBody();
    }
```

## 参考

[](https://www.cnblogs.com/javazhiyin/p/9851775.html  ':target=_blank')
[简书](https://www.jianshu.com/p/90ec27b3b518  ':target=_blank')