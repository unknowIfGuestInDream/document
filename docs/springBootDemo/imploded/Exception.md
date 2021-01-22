> 本文主要讲解如何在SpringBoot应用中使用统一异常处理。

1. 使用@ControllerAdvice或@RestControllerAdvice和@ExceptionHandler注解
2. 使用ErrorController类来实现。

需要添加依赖:
```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
```

## 使用@ControllerAdvice或@RestControllerAdvice和@ExceptionHandler注解

```java
/**
 * @author: TangLiang
 * @date: 2020/9/2 9:14
 * @since: 1.0
 */
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(NullPointerException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Map handle(NullPointerException exception) {
        Map<String, Object> result = new HashMap<>();
        result.put("result", exception.getLocalizedMessage());
        result.put("success", false);
        return result;
    }
}
```

注解@ControllerAdvice表示这是一个控制器增强类，当控制器发生异常且符合类中定义的拦截异常类，将会被拦截。
可以定义拦截的控制器所在的包路径  

注解ExceptionHandler定义拦截的异常类

## 使用ErrorController类来实现。

系统默认的错误处理类为BasicErrorController，将会显示如上的错误页面。  
这里编写一个自己的错误处理类，上面默认的处理类将不会起作用。  
getErrorPath()返回的路径服务器将会重定向到该路径对应的处理类，本例中为error方法。  

```java
@Slf4j
@RestController
public class HttpErrorController implements ErrorController {

    private final static String ERROR_PATH = "/error";

    @ResponseBody
    @RequestMapping(path  = ERROR_PATH )
    public Map error(HttpServletRequest request, HttpServletResponse response){
        Map<String, Object> result = new HashMap<>();
        log.info("访问/error" + "  错误代码："  + response.getStatus());
        result.put("success", false);
        return result;
    }
    @Override
    public String getErrorPath() {
        return ERROR_PATH;
    }
}
```

实战中通常会有一个统一的返回类，供前端进行处理，有的话替换掉Map即可。

测试类：
```java
@Slf4j
@RestController
@RequestMapping("/user")
public class TestController {

    @RequestMapping("/info1")
    public String test(){
      log.info("/user/info1");

      throw new NullPointerException("TestController have exception");
    }
}
```

## 区别

1. 注解@ControllerAdvice方式只能处理控制器抛出的异常。此时请求已经进入控制器中。
2. 类ErrorController方式可以处理所有的异常，包括未进入控制器的错误，比如404,401等错误
3. 如果应用中两者共同存在，则@ControllerAdvice方式处理控制器抛出的异常，类ErrorController方式未进入控制器的异常。
4. @ControllerAdvice或@RestControllerAdvice方式可以定义多个拦截方法，拦截不同的异常类，并且可以获取抛出的异常信息，自由度更大。

参考： [正规军springboot如何处理：参数校验、统一异常、统一响应](https://blog.csdn.net/chaitoudaren/article/details/105610962 ':target=_blank')