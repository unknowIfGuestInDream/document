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

| HTTP method | RestTemplate methods |
|-------------|----------------------|
| DELETE      | delete               |
| GET         | getForObject         |
| GET         | getForEntity         |
| HEAD        | headForHeaders       |
| OPTIONS     | optionsForAllow      |
| POST        | postForLocation      |
| POST        | postForObject        |
| POST        | postForEntity        |
| PUT         | put                  |
| any         | exchange             |
| any         | execute              |

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
        //请求工厂类是否应用缓冲请求正文内部，默认值为true，
        // 当post或者put大文件的时候会造成内存溢出情况，设置为false将数据直接流入底层HttpURLConnection。
        HttpComponentsClientHttpRequestFactory factory = new HttpComponentsClientHttpRequestFactory();
        factory.setBufferRequestBody(true);
        //设置客户端和服务端建立连接的超时时间
        requestFactory.setConnectTimeout(5000);
        //设置客户端从服务端读取数据的超时时间
        requestFactory.setReadTimeout(5000);
        //设置从连接池获取连接的超时时间，不宜过长
        requestFactory.setConnectionRequestTimeout(200);
        restTemplate.setRequestFactory(factory);
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

## 手动指定转换器
调用reseful接口传递的数据内容是json格式的字符串，返回的响应也是json格式的字符串。然而restTemplate.postForObject方法的请求参数RequestBean和返回参数ResponseBean却都是java类。是RestTemplate通过HttpMessageConverter自动帮我们做了转换的操作

默认情况下RestTemplate自动帮我们注册了一组HttpMessageConverter用来处理一些不同的contentType的请求。
如StringHttpMessageConverter来处理text/plain;MappingJackson2HttpMessageConverter来处理application/json;MappingJackson2XmlHttpMessageConverter来处理application/xml。
你可以在org.springframework.http.converter包下找到所有spring帮我们实现好的转换器。
如果现有的转换器不能满足你的需求，你还可以实现org.springframework.http.converter.HttpMessageConverter接口自己写一个。


```markdown
        RestTemplate restTemplate = new RestTemplate();
        //获取RestTemplate默认配置好的所有转换器
        List<HttpMessageConverter<?>> messageConverters = restTemplate.getMessageConverters();
        //默认的MappingJackson2HttpMessageConverter在第7个 先把它移除掉
        messageConverters.remove(6);
        //添加上GSON的转换器
        messageConverters.add(6, new GsonHttpMessageConverter());
```

这个简单的例子展示了如何使用GsonHttpMessageConverter替换掉默认用来处理application/json的MappingJackson2HttpMessageConverter

## 设置底层连接方式
要创建一个RestTemplate的实例，您可以像上述例子中简单地调用默认的无参数构造函数。这将使用java.net包中的标准Java类作为底层实现来创建HTTP请求。
但很多时候我们需要像传统的HttpClient那样设置HTTP请求的一些属性。RestTemplate使用了一种很偷懒的方式实现了这个需求，那就是直接使用一个HttpClient作为底层实现

```markdown
        //生成一个设置了连接超时时间、请求超时时间、异常最大重试次数的httpClient
        RequestConfig config = RequestConfig.custom().setConnectionRequestTimeout(10000).setConnectTimeout(10000).setSocketTimeout(30000).build();
        HttpClientBuilder builder = HttpClientBuilder.create().setDefaultRequestConfig(config).setRetryHandler(new DefaultHttpRequestRetryHandler(5, false));
        HttpClient httpClient = builder.build();
        //使用httpClient创建一个ClientHttpRequestFactory的实现
        ClientHttpRequestFactory requestFactory = new HttpComponentsClientHttpRequestFactory(httpClient);
         //ClientHttpRequestFactory作为参数构造一个使用作为底层的RestTemplate
        RestTemplate restTemplate = new RestTemplate(requestFactory);
```

## 设置拦截器
有时候我们需要对请求做一些通用的拦截设置，这就可以使用拦截器进行处理。拦截器需要我们实现org.springframework.http.client.ClientHttpRequestInterceptor接口自己写。

举个简单的例子，写一个在header中根据请求内容和地址添加令牌的拦截器

```java
public class TokenInterceptor implements ClientHttpRequestInterceptor
{
    @Override
    public ClientHttpResponse intercept(HttpRequest request, byte[] body, ClientHttpRequestExecution execution) throws IOException
    {
        //请求地址
        String checkTokenUrl = request.getURI().getPath();
        //token有效时间
        int ttTime = (int) (System.currentTimeMillis() / 1000 + 1800);
        //请求方法名 POST、GET等
        String methodName = request.getMethod().name();
        //请求内容
        String requestBody = new String(body);
        //生成令牌 此处调用一个自己写的方法，有兴趣的朋友可以自行google如何使用ak/sk生成token，此方法跟本教程无关，就不贴出来了
        String token = TokenHelper.generateToken(checkTokenUrl, ttTime, methodName, requestBody);
        //将令牌放入请求header中
        request.getHeaders().add("X-Auth-Token",token);

        return execution.execute(request, body);
    }
}
```

创建RestTemplate实例的时候可以这样向其中添加拦截器

```markdown
        RestTemplate restTemplate = new RestTemplate();
        //向restTemplate中添加自定义的拦截器
        restTemplate.getInterceptors().add(new TokenInterceptor());
```