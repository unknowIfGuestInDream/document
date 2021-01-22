> 开发中经常会有一个需求就是要将本地的文件映射到服务器上，然后可以访问，通常我们的项目代码和上传的文件是分离的，比如项目在 D 盘的某个目录，而图片上传在 E 盘某目录，这时候就可以用到虚拟路径

需要添加依赖:
```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
```
## 方式一： 实现WebMvcConfigurer

yml新增自定义配置：
```yaml
#虚拟路径 格式参照： D:/images
word.picture.memory=D:/images
#如需配置Linux或者mac 需要修改com.newangels.rotables.config.ResourceConfig  file:/修改为file:
#word.picture.memory=/home/tangliangroot/Documents/images
#虚拟路径请求url  格式参照： /Document
word.picture.request=/Document
```

虚拟路径配置：
```java
/**
 * 虚拟路径
 *
 * @author: TangLiang
 * @date: 2020/12/16 11:52
 * @since: 1.0
 */
@Configuration
public class ResourceConfig implements WebMvcConfigurer {

    @Value("${word.picture.memory}")
    private String memory;

    @Value("${word.picture.request}")
    private String request;

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler(request + "/**").addResourceLocations("file:/" + memory + "/");
    }
}
```

以上配置 完后就可以在页面中使用 /Document/文件名 访问本地资源了。

## 方式二： 设置加载静态资源的路径

```yaml
web.upload-path=D:/images/
spring.mvc.static-path-pattern=/**
spring.resources.static-locations=classpath:/META-INF/resources/,classpath:/resources/, classpath:/static/, classpath:/public/,file:${web.upload-path}
```

其中 web.upload-path 是自定义的，后面的 D:/images/ 是本地路径。 第二行的 /** 表示后面的所有文件都可以访问 spring.resources.static-locations 在这里配置静态资源路径，前面说了这里的配置是覆盖默认配置，所以需要将默认的也加上否则static、public等这些路径将不能被当作静态资源路径，在这个最末尾的file:${web.upload-path}之所有要加file:是因为指定的是一个具体的硬盘路径，其他的使用classpath指的是系统环境变量

