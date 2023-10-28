> Swagger是一款可以快速生成符合RESTful风格API并进行在线调试的插件。

在此之前，我们先聊聊什么是REST。REST实际上为Representational State Transfer的缩写，翻译为“表现层状态转化” 。如果一个架构符合REST 原则，就称它为RESTful架构。  
实际上，“表现层状态转化”省略了主语，完整的说应该是“资源表现层状态转化”。  
什么是资源（Resource）？资源指的是网络中信息的表现形式，比如一段文本，一首歌，一个视频文件等等；    
什么是表现层（Reresentational）？表现层即资源的展现在你面前的形式，比如文本可以是JSON格式的，也可以是XML形式的，甚至为二进制形式的。图片可以是gif，也可以是PNG；  
什么是状态转换（State Transfer）？用户可使用URL通过HTTP协议来获取各种资源，HTTP协议包含了一些操作资源的方法，比如：GET 用来获取资源， POST 用来新建资源 , PUT 用来更新资源，
 DELETE 用来删除资源， PATCH 用来更新资源的部分属性。通过这些HTTP协议的方法来操作资源的过程即为状态转换。

下面对比下传统URL请求和RESTful风格请求的区别：

| 描述 | 传统请求                          | 方法  | RESTful请求         | 方法     |
|----|-------------------------------|-----|-------------------|--------|
| 查询 | /user/query?name=mrbird       | GET | /user?name=mrbird | GET    |
| 详情 | /user/getInfo?id=1            | GET | /user/1           | GET    |
| 创建 | /user/create?name=mrbird      | GET | /user             | POST   |
| 修改 | /user/update?name=mrbird&id=1 | GET | /user             | PUT    |
| 删除 | /user/delete?id=1             | GET | /user             | DELETE |

从上面这张表，我们大致可以总结下传统请求和RESTful请求的几个区别：

1. 传统请求通过URL来描述行为，如create，delete等；RESTful请求通过URL来描述资源。
2. RESTful请求通过HTTP请求的方法来描述行为，比如DELETE，POST，PUT等，并且使用HTTP状态码来表示不同的结果。
3. RESTful请求通过JSON来交换数据。

## Swagger注解

* @Api：修饰整个类，描述Controller的作用；
* @ApiOperation：描述一个类的一个方法，或者说一个接口；
* @ApiParam：单个参数描述；
* @ApiModel：用对象来接收参数；
* @ApiProperty：用对象接收参数时，描述对象的一个字段；
* @ApiResponse：HTTP响应其中1个描述；
* @ApiResponses：HTTP响应整体描述；
* @ApiIgnore：使用该注解忽略这个API；
* @ApiError ：发生错误返回的信息；
* @ApiImplicitParam：一个请求参数；
* @ApiImplicitParams：多个请求参数。

## 编写RESTful API接口

Spring Boot中包含了一些注解，对应于HTTP协议中的方法：

* @GetMapping对应HTTP中的GET方法；
* @PostMapping对应HTTP中的POST方法；  
* @PutMapping对应HTTP中的PUT方法；  
* @DeleteMapping对应HTTP中的DELETE方法；  
* @PatchMapping对应HTTP中的PATCH方法。


## 配置一：swagger2版本在3.0.0之前

引入依赖：

```xml
        <!--swagger-->
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger2</artifactId>
            <version>2.7.0</version>
        </dependency>
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger-ui</artifactId>
            <version>2.7.0</version>
        </dependency>
```

yaml自定义配置:

```yaml
# Swagger配置
swagger:
  # 是否开启swagger
  enabled: true
  # 请求前缀
  pathMapping: /

```

Swagger配置文件：

```java
import com.google.common.base.Predicates;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.*;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spi.service.contexts.SecurityContext;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

import java.util.ArrayList;
import java.util.List;

/**
 * http://localhost:8080/swagger-ui.html
 *
 * @author: TangLiang
 * @date: 2020/7/29 10:48
 * @since: 1.0
 */
@Configuration
@EnableSwagger2
public class SwaggerConfig {

    /**
     * 是否开启swagger
     */
    @Value("${swagger.enabled}")
    private boolean enabled;

    /**
     * 设置请求的统一前缀
     */
    @Value("${swagger.pathMapping}")
    private String pathMapping;

    /**
     * 创建API
     */
    @Bean
    public Docket createRestApi() {
        return new Docket(DocumentationType.SWAGGER_2)
                // 是否启用Swagger
                .enable(enabled)
                // 用来创建该API的基本信息，展示在文档的页面中（自定义展示的信息）
                .apiInfo(apiInfo())
                // 设置哪些接口暴露给Swagger展示
                .select()
                // 扫描所有有注解的api，用这种方式更灵活
                .apis(RequestHandlerSelectors.withMethodAnnotation(ApiOperation.class))
                // 扫描指定包中的swagger注解
                // .apis(RequestHandlerSelectors.basePackage("com.ruoyi.project.tool.swagger"))
                // 扫描所有 .apis(RequestHandlerSelectors.any())
                .paths(PathSelectors.any())
                .paths(Predicates.not(PathSelectors.regex("/actuator.*")))//actuator路径跳过
                .build()
                /* 设置安全模式，swagger可以设置访问token */
                .securitySchemes(securitySchemes())
                .securityContexts(securityContexts())
                .pathMapping(pathMapping);
    }

    /**
     * 安全模式，这里指定token通过Authorization头请求头传递
     */
    private List<ApiKey> securitySchemes() {
        List<ApiKey> apiKeyList = new ArrayList<ApiKey>();
        apiKeyList.add(new ApiKey("Authorization", "Authorization", "header"));
        return apiKeyList;
    }

    /**
     * 安全上下文
     */
    private List<SecurityContext> securityContexts() {
        List<SecurityContext> securityContexts = new ArrayList<>();
        securityContexts.add(
                SecurityContext.builder()
                        .securityReferences(defaultAuth())
                        .forPaths(PathSelectors.regex("^(?!auth).*$"))
                        .build());
        return securityContexts;
    }

    /**
     * 默认的安全上引用
     */
    private List<SecurityReference> defaultAuth() {
        AuthorizationScope authorizationScope = new AuthorizationScope("global", "accessEverything");
        AuthorizationScope[] authorizationScopes = new AuthorizationScope[1];
        authorizationScopes[0] = authorizationScope;
        List<SecurityReference> securityReferences = new ArrayList<>();
        securityReferences.add(new SecurityReference("Authorization", authorizationScopes));
        return securityReferences;
    }

    /**
     * 添加摘要信息
     */
    private ApiInfo apiInfo() {
        // 用ApiInfoBuilder进行定制
        return new ApiInfoBuilder()
                // 设置标题
                .title("springBootDemo接口文档")
                // 描述
                .description("springBoot的学习项目")
                // 作者信息
                .contact(new Contact("唐亮", "https://github.com/unknowIfGuestInDream", "tang97155@163.com"))
                // 版本
                .version("版本号:" + "1.1")
                .build();
    }
}
```

## 测试Demo

```java
import io.swagger.annotations.*;
import org.springframework.web.bind.annotation.*;

import java.util.*;

/**
 * swagger 用户测试方法
 *
 * @author ruoyi
 */
@Api("用户信息管理")
@RestController
@RequestMapping("/test/user")
public class TestController {
    private final static Map<Integer, UserEntity> users = new LinkedHashMap<Integer, UserEntity>();

    {
        users.put(1, new UserEntity(1, "admin", "admin123", "15888888888"));
        users.put(2, new UserEntity(2, "ry", "admin123", "15666666666"));
    }

    @ApiOperation("获取用户列表")
    @GetMapping("/list")
    public Map userList() {
        Map map = new HashMap();
        List<UserEntity> userList = new ArrayList<UserEntity>(users.values());
        map.put("success", true);
        map.put("userList", userList);
        return map;
    }

    @ApiOperation("获取用户详细")
    @ApiImplicitParam(name = "userId", value = "用户ID", required = true, dataType = "int", paramType = "path")
    @GetMapping("/{userId}")
    public Map getUser(@PathVariable Integer userId) {
        Map map = new HashMap();
        if (!users.isEmpty() && users.containsKey(userId)) {
            map.put("success", true);
            map.put("userId", users.get(userId));
        } else {
            map.put("success", false);
            map.put("message", "用户不存在");
        }
        return map;
    }

    @ApiOperation("新增用户")
    @ApiImplicitParam(name = "userEntity", value = "新增用户信息", dataType = "UserEntity")
    @PostMapping("/save")
    public Map save(UserEntity user) {
        Map map = new HashMap();
        if (user == null || user.getUserId() == null) {
            map.put("success", false);
            map.put("message", "用户ID不能为空");
        } else {
            map.put("success", true);
            map.put(user.getUserId(), user);
        }
        return map;
    }

    @ApiOperation("更新用户")
    @ApiImplicitParam(name = "userEntity", value = "新增用户信息", dataType = "UserEntity")
    @PutMapping("/update")
    public Map update(UserEntity user) {
        Map map = new HashMap();
        if (user == null || user.getUserId() == null) {
            map.put("success", false);
            map.put("message", "用户ID不能为空");
        } else if (users.isEmpty() || !users.containsKey(user.getUserId())) {
            map.put("success", false);
            map.put("message", "用户不存在");
        } else {
            map.put("success", true);
            map.put(user.getUserId(), user);
        }
        users.remove(user.getUserId());
        return map;
    }

    @ApiOperation("删除用户信息")
    @ApiImplicitParam(name = "userId", value = "用户ID", required = true, dataType = "int", paramType = "path")
    @DeleteMapping("/{userId}")
    public Map delete(@PathVariable Integer userId) {
        Map map = new HashMap();
        if (!users.isEmpty() && users.containsKey(userId)) {
            users.remove(userId);
            map.put("success", true);
        } else {
            map.put("success", false);
            map.put("message", "用户不存在");
        }
        return map;
    }
}

@ApiModel("用户实体")
@Data
class UserEntity {
    @ApiModelProperty("用户ID")
    private Integer userId;

    @ApiModelProperty("用户名称")
    private String username;

    @ApiModelProperty("用户密码")
    private String password;

    @ApiModelProperty("用户手机")
    private String mobile;

    public UserEntity() {
    }

    public UserEntity(Integer userId, String username, String password, String mobile) {
        this.userId = userId;
        this.username = username;
        this.password = password;
        this.mobile = mobile;
    }
}
```

随后访问http://localhost:8080/swagger-ui.html即可。

## 配置二：swagger2版本在3.0.0之后

> springfox 3.0.0版本已经有了自己的SpringBoot Starter，使用起来更契合SpringBoot项目，非常方便。

首先在pom.xml中添加springfox官方Swagger依赖；

```xml
<!--springfox swagger官方Starter-->
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-boot-starter</artifactId>
    <version>3.0.0</version>
</dependency>
```

添加Swagger的Java配置，配置好Api信息和需要生成接口文档的类扫描路径即可；

```java
/**
 * Swagger2API文档的配置
 */
@Configuration
public class Swagger2Config {
    @Bean
    public Docket createRestApi() {
        return new Docket(DocumentationType.SWAGGER_2)
                .apiInfo(apiInfo())
                .select()
                .apis(RequestHandlerSelectors.basePackage("扫描包路径"))
                .paths(PathSelectors.any())
                .build();
    }

    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("SwaggerUI演示")
                .description("springBootDemo")
                .contact(new Contact("唐亮", null, null))
                .version("1.0")
                .build();
    }
}
```

> 访问路径 http://localhost:8080/swagger-ui/

如果集成Spring Security则需要在访问接口时添加一个合法的Authorization请求头即可，新增以下代码

```markdown
 private List<SecurityScheme> securitySchemes() {
        //设置请求头信息
        List<SecurityScheme> result = new ArrayList<>();
        ApiKey apiKey = new ApiKey("Authorization", "Authorization", "header");
        result.add(apiKey);
        return result;
    }

    private List<SecurityContext> securityContexts() {
        //设置需要登录认证的路径
        List<SecurityContext> result = new ArrayList<>();
        result.add(getContextByPath("/brand/.*"));
        return result;
    }

    private SecurityContext getContextByPath(String pathRegex) {
        return SecurityContext.builder()
                .securityReferences(defaultAuth())
                .forPaths(PathSelectors.regex(pathRegex))
                .build();
    }

    private List<SecurityReference> defaultAuth() {
        List<SecurityReference> result = new ArrayList<>();
        AuthorizationScope authorizationScope = new AuthorizationScope("global", "accessEverything");
        AuthorizationScope[] authorizationScopes = new AuthorizationScope[1];
        authorizationScopes[0] = authorizationScope;
        result.add(new SecurityReference("Authorization", authorizationScopes));
        return result;
    }
```

与之前版本相比

* 旧版本需要依赖springfox-swagger2和springfox-swagger-ui两个配置，新版本一个Starter就搞定了，而且之前的版本如果不使用新版本的swagger-models和swagger-annotations依赖，访问接口会出现NumberFormatException问题；
* 新版本去除了一些第三方依赖，包括guava，之前使用旧版本时就由于guava版本问题导致过依赖冲突
* 新版本和旧版本文档访问路径发生了变化，新版本为：http://localhost:8080/swagger-ui/ ，旧版本为：http://localhost:8080/swagger-ui.html
* 新版本中新增了一些SpringBoot配置，springfox.documentation.enabled配置可以控制是否启用Swagger文档生成功能
* 比如说我们只想在dev环境下启用Swagger文档，而在prod环境下不想启用，旧版本我们可以通过@Profile注解实现；

```java
@Configuration
@EnableSwagger2
@Profile(value = {"dev"})
public class Swagger2Config {

}
```

* 新版本我们在SpringBoot配置文件中进行配置即可，springfox.documentation.enabled在application-dev.yml配置为true，在application-prod.yml中配置为false。

