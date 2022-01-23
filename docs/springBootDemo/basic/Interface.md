## WebMvcConfigurer
```java
@Component
public class MyWebMvcConfiguration implements WebMvcConfigurer {

    @Override
    public void configurePathMatch(PathMatchConfigurer configurer) {
        configurer.setUseSuffixPatternMatch();
        configurer.setUseRegisteredSuffixPatternMatch();
        configurer.setUseTrailingSlashMatch();
        //url路径解析（查找路径匹配的时候，解析url去匹配对应的映射器）
        configurer.setUrlPathHelper();
        //路径匹配器，拿到多个映射器后
        configurer.setPathMatcher();  
    }

    //配置视图解析器
    @Override
    public void configureViewResolvers(ViewResolverRegistry registry) {
        registry.jsp("/WEB-INF/jsp/", ".jsp");
        registry.enableContentNegotiation(new MappingJackson2JsonView());  //.jsp访问到的资源目录
    }

    //内容裁决器配置，处理器映射器和适配器公用组件，默认值是ContentNegotiationManager
    //配置内容裁决的一些参数的
    @Override
    public void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
        /* 是否通过请求Url的扩展名来决定media type */
        configurer.favorPathExtension(true)
                /* 不检查Accept请求头 */
                .ignoreAcceptHeader(true)
                .parameterName("mediaType")
                /* 设置默认的media Type */
                .defaultContentType(MediaType.TEXT_HTML)
                /* 请求以.html结尾的会被当成MediaType.TEXT_HTML*/
                .mediaType("html", MediaType.TEXT_HTML)
                /* 请求以.json结尾的会被当成MediaType.APPLICATION_JSON*/
                .mediaType("json", MediaType.APPLICATION_JSON);
    }

    //配置适配器(RequestMappingHandlerAdapter)中异步请求的相关处理组件
    @Override
    public void configureAsyncSupport(AsyncSupportConfigurer configurer) {
        //关联 adapter.setTaskExecutor(); 设置异步处理自定义线程池
        configurer.setTaskExecutor();
        //关联 adapter.setAsyncRequestTimeout();设置异步处理超时时间
        configurer.setDefaultTimeout();
        //adapter.setCallableInterceptors(); 设置异步回调拦截器
        configurer.registerCallableInterceptors();
        //adapter.setDeferredResultInterceptors();，设置延迟处理结果拦截器
        configurer.registerDeferredResultInterceptors();
    }

    //注册一个默认的Handler,处理静态资源文件，当到不到的文件的时候交个这个默认的处理
    @Override
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        configurer.enable();
    }

    //添加格式化器
    @Override
    public void addFormatters(FormatterRegistry registry) {

    }

    //添加注册拦截器
    @Override
    public void addInterceptors(InterceptorRegistry registry) {

    }
    //添加资源处理器
    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/resource/**").addResourceLocations("d://");
    }

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/cors/**")
                .allowedHeaders("*")
                .allowedMethods("POST","GET")
                .allowedOrigins("*");
    }

    //实现一个请求到视图的映射，而无需书写controller
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        //访问/login路径时直接返回index页面
        registry.addViewController("/index").setViewName("index");
    }

    //添加参数解析器，排在内置的之后
    @Override
    public void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {

    }

    //添加返回值解析器，排在内置的之后
    @Override
    public void addReturnValueHandlers(List<HandlerMethodReturnValueHandler> handlers) {

    }

    //添加消息转换器(可能覆盖默认的，跟配置有关)
    @Override
    public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {

    }
    //增加消息转换器，放在默认的之后
    @Override
    public void extendMessageConverters(List<HttpMessageConverter<?>> converters) {

    }

    //自定义异常解析器（覆盖默认）
    @Override
    public void configureHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {

    }
    //增加异常解析器，不覆盖默认的
    @Override
    public void extendHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {

    }

    //添加参数校验器，不建议重写
    @Override
    public Validator getValidator() {
        return null;
    }

    @Override
    public MessageCodesResolver getMessageCodesResolver() {
        return null;
    }
}
```

<details>
  <summary>示例： url转换</summary>

```java
public class CustomUrlPathHelper extends UrlPathHelper {

    @Override
    public String getLookupPathForRequest(HttpServletRequest request) {
        String url =  super.getLookupPathForRequest(request);
        if (url.startsWith("/test")){
            String substring = url.substring(5);
            return substring;
        }
        return url;
    }
}
```
```java
@Component
public class CustomMvcConfig implements WebMvcConfigurer {

    @Override
    public void configurePathMatch(PathMatchConfigurer configurer) {
        configurer.setUrlPathHelper(new CustomUrlPathHelper());
    }
}
```

</details> 

<details>
  <summary>示例：将参数自定义参数解析器放到系统内置之前生效</summary>

```java
public class ParamTestResover implements HandlerMethodArgumentResolver {

    //被 MapMethodProcessor处理了，走不到自定义的
    //解析map类型的入参，并且使用@ParamResoverTest注解标记
    @Override
    public boolean supportsParameter(MethodParameter parameter) {
        boolean annotation = parameter.hasParameterAnnotation(ParamResoverTest.class);
        boolean isMap = Map.class.isAssignableFrom(parameter.getParameterType());
        return annotation && isMap ;
    }

    @Override
    public Object resolveArgument(MethodParameter parameter, ModelAndViewContainer mavContainer, NativeWebRequest webRequest, WebDataBinderFactory binderFactory) throws Exception {
        Iterator<String> parameterNames = webRequest.getParameterNames();
        Map map = new HashMap();
        while (parameterNames.hasNext()){
            String next = parameterNames.next();
            String arg = webRequest.getParameter(next);
            map.put(next,arg);
        }
        return map;
    }
}
```
注册方式1  
```java
public class RequestMappingHandlerAdapterSelf extends RequestMappingHandlerAdapter {

    @Override
    public void afterPropertiesSet() {
        super.afterPropertiesSet();
        List<HandlerMethodArgumentResolver> resolverList = new ArrayList<HandlerMethodArgumentResolver>();
        //将自定义的参数解析器添加到首位
        resolverList.add(new ParamTestResover());
        //复制内置的参数解析器
        resolverList.addAll(super.getArgumentResolvers());
        //覆盖原来内置的参数解析器
        super.setArgumentResolvers(resolverList);
    }
}
```
注册方式2
```java
@Component
public class CustomMvcConfig implements WebMvcConfigurer {

    @Override
    public void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {
        List<HandlerMethodArgumentResolver> resolverList = new ArrayList<HandlerMethodArgumentResolver>()
        resolverList.add(new ParamTestResover());
        resolverList.addAll(resolvers);
    }
}
```

</details> 

## RequestMappingHandlerMapping
如果要提供RequestMappingHandlerMapping，RequestMappingHandlerAdapter或ExceptionHandlerExceptionResolver的自定义实例，并且仍然保留Spring Boot MVC自定义，则可以声明WebMvcRegistrations类型的bean，并使用它提供这些组件的自定义实例。

[https://blog.csdn.net/kaerbuka/article/details/105399821](https://blog.csdn.net/kaerbuka/article/details/105399821 ':target=_blank')  
[https://xhope.top/?p=1486](https://xhope.top/?p=1486 ':target=_blank')

<details>
  <summary>示例：为URL统一加版本控制</summary>

https://blog.csdn.net/Heron22/article/details/109532698

</details> 

## HandlerMethodArgumentResolver
参数解析器

https://cloud.tencent.com/developer/article/1808370

## DisposableBean
bean销毁（other文档）
https://www.jianshu.com/p/6f2cbbbc8781

## ImportSelector
[https://www.jianshu.com/p/5e7752c42a0d](https://www.jianshu.com/p/5e7752c42a0d ':target=_blank')  
[https://www.cnblogs.com/niechen/p/9262452.html](https://www.cnblogs.com/niechen/p/9262452.html ':target=_blank')

## ImportBeanDefinitionRegistrar
[https://zhuanlan.zhihu.com/p/91461558](https://zhuanlan.zhihu.com/p/91461558 ':target=_blank')
## SmartLifecycle
[https://blog.csdn.net/bronze5/article/details/106558309](https://blog.csdn.net/bronze5/article/details/106558309 ':target=_blank')
## ApplicationContextAware
当前的application context从而调用容器的服务  
[https://www.jianshu.com/p/4c0723615a52](https://www.jianshu.com/p/4c0723615a52 ':target=_blank')

## ConfigurableApplicationContext
[https://www.cnblogs.com/sharpest/p/10885820.html](https://www.cnblogs.com/sharpest/p/10885820.html ':target=_blank')

## BeanNameAware
获得到容器中Bean的名称  
[https://www.cnblogs.com/xiaozhuanfeng/p/10790695.html](https://www.cnblogs.com/xiaozhuanfeng/p/10790695.html ':target=_blank')

## BeanFactoryAware
获得当前bean Factory,从而调用容器的服务
## MessageSourceAware
得到message source从而得到文本信息
## ResourceLoaderAware
获取资源加载器,可以获得外部资源文件  
[https://www.cnblogs.com/frankltf/p/11736830.html](https://www.cnblogs.com/frankltf/p/11736830.html ':target=_blank')
## EnvironmentAware
[https://blog.csdn.net/bazhuayu_1203/article/details/78658196](https://blog.csdn.net/bazhuayu_1203/article/details/78658196 ':target=_blank')