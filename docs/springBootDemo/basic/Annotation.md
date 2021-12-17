> 介绍一些其它的springBoot的注解

## @CookieValue
@CookieValue注解用于将请求的cookie数据映射到功能处理方法的参数上，用法和@Requestparam一样。

1. value：参数名称
2. required：是否必须
3. defaultValue：默认值

```java
 @CookieValue("JSESSIONID") String cookie
```

## @RequessHeader
@RequestHeader注解主要是将请求头的信息区数据，映射到功能处理方法的参数上，用法和@Requestparam一样。

1. value：参数名称
2. required：是否必须
3. defaultValue：默认值

```java
@RequestHeader("User-agent") String userAgent, @RequestHeader(value = "Accept") String[] accepts
```

## @RequestParam
将请求参数绑定到你控制器的方法参数上（是springmvc中接收普通参数的注解）

1. value：参数名称
2. required：是否必须
3. defaultValue：默认值

```java
@RequestParam("params") List<String> params
```

## @DateTimeFormat
可对Date,Calendar,Long时间类型的属性进行标注，它有以下属性
* iso 类型为DateTimeFormat.ISO
  * DateTimeFormat.ISO.DATE: 格式为yyyy-MM-dd
  * DateTimeFormat.ISO.TIME: 格式为hh:mm:ss.SSSZ
  * DateTimeFormat.ISO.DATE_TIME: 格式为yyyy-MM-dd hh:mm:ss.SSSZ
  * DateTimeFormat.ISO.NONE: 默认值，表示不应使用ISO格式的时间
* pattern  类型为String,使用自定义的时间格式字符串，如"yyyy-MM-dd HH:mm:ss"
* fallbackPatterns  
* style  类型为String, 通过样式指定日期时间的格式，由两位字符组成，第1位表示日期的样式，第2位表示时间的格式，以下是常用值
  * S: 短日期/时间的样式
  * M: 中日期/时间的样式
  * L: 长日期/时间的样式
  * F: 完整日期/时间的样式
  * -: 忽略日期/时间的样式

```java
@DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss") Date START_DATE_
```

## @NumberFormat
可对类似数字类型的属性进行标注，它有以下属性
* pattern 类型为String,使用自定义的数字格式化串，如"##,###.##"
* style 类型为NumberFormat.Style
  * DEFAULT: 默认值
  * NUMBER: 正常数字类型
  * PERCENT: 百分数类型
  * CURRENCY: 货币类型

## @PathVariable
通过 @PathVariable 可以将URL中占位符参数{xxx}绑定到处理器类的方法形参中@PathVariable("xxx")
```java
    @DeleteMapping(value = "clearCaches/{name}")
    public Map<String, Object> clearCaches(@PathVariable(required = false) String name) {
    }
```

## @RequestBody
@RequestBody主要用来接收前端传递给后端的json字符串中的数据的(请求体中的数据的)；而最常用的使用请求体传参的无疑是POST请求了，所以使用@RequestBody接收数据时，一般都用POST方式进行提交。在后端的同一个接收方法里，@RequestBody与@RequestParam()可以同时使用，@RequestBody最多只能有一个，而@RequestParam()可以有多个

如果参数时放在请求体中，application/json传入后台的话，那么后台要用@RequestBody才能接收到；如果不是放在请求体中的话，那么后台接收前台传过来的参数时，要用@RequestParam来接收，或在形参前 什么也不写也能接收

```java
    @PostMapping(value = "getCache}")
    public Map<String, Object> getCache(@RequestBody User user, RequestParam("token") String token) {
    }
```

## @ResponseBody
@responseBody注解的作用是将controller的方法返回的对象通过适当的转换器转换为指定的格式之后，写入到response对象的body区，通常用来返回JSON数据或者是XML数据，需要注意的呢，在使用此注解之后不会再走试图处理器，而是直接将数据写入到输入流中，他的效果等同于通过response对象输出指定格式的数据。

@ResponseBody是作用在方法上的，@ResponseBody 表示该方法的返回结果直接写入 HTTP response body 中，一般在异步获取数据时使用【也就是AJAX】。
```java
@RequestMapping("/login")
@ResponseBody
public Object login(String name, String password, HttpSession session) {
}
```

## @RequestPart
@RequestPart用于将multipart/form-data类型数据映射到控制器处理方法的参数中。除了@RequestPart注解外，@RequestParam同样可以用于此类操作。

他们最大的不同是，当请求方法的请求参数类型不再是String类型的时候。 @RequestParam适用于name-value String类型的请求域，@RequestPart适用于复杂的请求域（像JSON，XML）

```java
    @RequestMapping("uploadFile")
    public JsonResult uploadFile(@RequestPart("file") MultipartFile file,@RequestPart("file") Part part, @RequestParam String bucket){
    }
```

## @RequestAttribute
它只能使用在方法入参上。获取HTTP的请求（request）对象属性值，用来传递给控制器的参数。相当于ServletRequest.getAttribute()

@RequestAttribute只负责从request里面取属性值，至于你什么时候往里放值，是有多种方式的可以达到的：
1. @ModelAttribute注解预存
2. HandlerInterceptor拦截器中预存
3. 请求转发带过来

## @SessionAttribute
获取HTTP的请求（session）对象属性值。相当于HttpSession.getAttribute()

## @ModelAttribute
它将方法参数/方法返回值绑定到web view的Model里面。只支持@RequestMapping这种类型的控制器哦。它既可以标注在方法入参上，也可以标注在方法（返回值）上。

但是请注意，当请求处理导致异常时，引用数据和所有其他模型内容对Web视图不可用，因为该异常随时可能引发，使Model内容不可靠。因此，标注有@Exceptionhandler的方法不提供对Model参数的访问

```java
@RestController
@RequestMapping
public class HelloController {

	// 放置attr属性值
    @ModelAttribute
    public Person personModelAttr(HttpServletRequest request) {
        request.setAttribute("myApplicationName", "fsx-application");
        return new Person("非功能方法", 50);
    }

    @GetMapping("/testRequestAttr")
    public void testRequestAttr(@RequestAttribute("myApplicationName") String myApplicationName, HttpServletRequest request, ModelMap modelMap) {
        System.out.println(myApplicationName); //fsx-application

        // 从request里获取
        System.out.println(request.getAttribute("myApplicationName")); //fsx-application

        // 从model里获取
        System.out.println(modelMap.get("myApplicationName")); // null 获取不到attr属性的
        System.out.println(modelMap.get("person")); // Person(name=非功能方法, age=50)
    }
}
```

请求/testRequestAttr，结果打印如下：
```shell
fsx-application
fsx-application
null
Person(name=非功能方法, age=50)
```

## @SessionAttributes
该注解顾名思义，作用是将Model中的属性同步到session会话当中，方便在下一次请求中使用(比如重定向场景)。  
虽然说Session的概念在当下前后端完全分离的场景中已经变得越来越弱化了，但是若为web开发者来说，我仍旧强烈不建议各位扔掉这个知识点，我建议能够熟练使用@SessionAttributes来简化平时的开发

这个注解只能标注在类上，用于在多个请求之间传递参数，类似于Session的Attribute。  
但不完全一样：一般来说@SessionAttributes设置的参数只用于暂时的传递，而不是长期的保存，长期保存的数据还是要放到Session中。（比如重定向之间暂时传值，用这个注解就很方便）

官方解释：当用@SessionAttributes标注的Controller向其模型Model添加属性时，将根据该注解指定的名称/类型检查这些属性，若匹配上了就顺带也会放进Session里。匹配上的将一直放在Sesson中，直到你调用了SessionStatus.setComplete()方法就消失了

```java
@Controller
@RequestMapping("/sessionattr/demo")
@SessionAttributes(value = {"book", "description"}, types = {Double.class})
public class RedirectController {

    @RequestMapping("/index")
    public String index(Model model, HttpSession httpSession) {
        model.addAttribute("book", "天龙八部");
        model.addAttribute("description", "我乔峰是个契丹人");
        model.addAttribute("price", new Double("1000.00"));

        // 通过Sesson API手动放一个进去
        httpSession.setAttribute("hero", "fsx");

        //跳转之前将数据保存到Model中，因为注解@SessionAttributes中有，所以book和description应该都会保存到SessionAttributes里（注意：不是session里）
        return "redirect:get";
    }

    // 关于@ModelAttribute 下文会讲
    @RequestMapping("/get")
    public String get(@ModelAttribute("book") String book, ModelMap model, HttpSession httpSession, SessionStatus sessionStatus) {
        //可以从model中获得book、description和price的参数
        System.out.println(model.get("book") + ";" + model.get("description") + ";" + model.get("price"));

        // 从sesson中也能拿到值
        System.out.println(httpSession.getAttribute("book"));
        System.out.println("API方式手动放进去的：" + httpSession.getAttribute("hero"));
        // 使用@ModelAttribute也能拿到值
        System.out.println(book);

        // 手动清除SessionAttributes
        sessionStatus.setComplete();
        return "redirect:complete";
    }

    @RequestMapping("/complete")
    @ResponseBody
    public String complete(ModelMap modelMap, HttpSession httpSession) {
        //已经被清除，无法获取book的值
        System.out.println(modelMap.get("book"));
        System.out.println("API方式手动放进去的：" + httpSession.getAttribute("hero"));
        return "sessionAttributes";
    }

}
```

我们只需要访问入口请求/index就可以直接看到控制台输出如下：
```shell
天龙八部;我乔峰是个契丹人;1000.0
天龙八部
API方式手动放进去的：fsx
天龙八部
null
API方式手动放进去的：fsx
```

@SessionAttributes注解设置的参数有3类方式去使用它：
* 在视图view中（比如jsp页面等）通过request.getAttribute()或session.getAttribute获取
* 在后面请求返回的视图view中通过session.getAttribute或者从model中获取（这个也比较常用）
* 自动将参数设置到后面请求所对应处理器的Model类型参数或者有@ModelAttribute注释的参数里面（结合@ModelAttribute一起使用应该是我们重点关注的）

**总结**  
@SessionAttributes指的是Spring MVC的Session。向其中添加值得时候，同时会向 HttpSession中添加一条。在sessionStatus.setComplete();的时候，会清空Spring MVC
的Session，同时清除对应键的HttpSession内容，但是通过，request.getSession.setAttribute()方式添加的内容不会被清除掉。其他情况下，Spring MVC的Session和HttpSession使用情况相同。

## @ResponseStatus
@ResponseStatus的作用就是为了改变HTTP响应的状态码，可以在代码中的三个地方使用它，分别如下

1、标注在@RequestMapping上  
```java
    @RequestMapping("/demo2")
    @ResponseBody
    @ResponseStatus(code = HttpStatus.OK)
    public String demo2(){
        return "hello world";
    }
```
这里作用就是改变服务器响应的状态码 ,比如一个本是200的请求可以通过@ResponseStatus 改成404/500等等

2、标注在@ControllerAdvice中  
```java
@ControllerAdvice
@ResponseStatus
public class MyControllerAdvice {
 
    @ExceptionHandler({ArithmeticException.class})
    public ModelAndView fix(Exception e){
        Map map=new HashMap();
        map.put("ex",e.getMessage());
        return new ModelAndView("error",map);
    }
 
}
```
@ControllerAdvice标注初衷我想就是程序运行过程中发生异常，对异常如何处理？  而@ResponseStatus标注在@ControllerAdvice类或者该类下的@ExceptionHandler上，区别大概就是，

原来比如请求程序抛出异常，异常被捕获，走@ExceptionHandler，正常走完状态码是200.

@ControllerAdvice或者 @ExceptionHandler标注了@ReponseStatus，那走完状态码就是500.

如果你再给@ResponseStatus添加了reason属性，不管捕获异常方法咋返回，都是服务器的错误码捕获界面，比如上面我的例子，给@ResponseStatus添加reason=”your defined message”.

3、自定义类型的异常添加注解@ResponseStatus
```java
@ResponseStatus(code = HttpStatus.INTERNAL_SERVER_ERROR,reason = "not  an error , just info")
public class MyException extends RuntimeException {
    public MyException() {
    }
 
    public MyException(String message) {
        super(message);
    }
}
```

如果只是为了返回状态码，建议只使用 @ResponseStatus(code=xxxx)这样来设置响应状态码；  
如果抛出异常，不建议@ControllerAdvice里面的 @ResponseStatus和自定义异常上的  @ResponseStatus一起使用，  
按照我的阅读理解，两个一起使用肯定是一个生效，而且是 @ControllerAdvice中的@ResponseStatus生效.

## @CrossOrigin
Spring Framework 4.2GA为CORS提供了第一类支持，使您比通常的基于过滤器的解决方案更容易和更强大地配置它。所以springMVC的版本要在4.2或以上版本才支持@CrossOrigin

注解可作用在类和方法上

* origins: 允许可访问的域列表.匹配的域名是跨域预请求 Response 头中的 'Access-Control-Allow_origin' 字段值
* maxAge: 准备响应前的缓存持续的最大时间（以秒为单位）。
* originPatterns: 允许可访问的域列表
* allowedHeaders: 跨域请求中允许的请求头中的字段类型， 该值对应跨域预请求 Response 头中的 'Access-Control-Allow-Headers' 字段值。 不设置确切值默认支持所有的header字段（Cache-Controller、Content-Language、Content-Type、Expires、Last-Modified、Pragma）跨域访问
* exposedHeaders: 跨域请求请求头中允许携带的除Cache-Controller、Content-Language、Content-Type、Expires、Last-Modified、Pragma这六个基本字段之外的其他字段信息，对应的是跨域请求 Response 头中的 'Access-control-Expose-Headers'字段值
* methods: 跨域HTTP请求中支持的HTTP请求类型（GET、POST...），不指定确切值时默认与 Controller 方法中的 methods 字段保持一致
* allowCredentials: 该值对应的是是跨域请求 Response 头中的 'Access-Control-Allow-Credentials' 字段值。浏览器是否将本域名下的 cookie 信息携带至跨域服务器中。默认携带至跨域服务器中，但要实现 cookie 共享还需要前端在 AJAX 请求中打开 withCredentials 属性

```java
@CrossOrigin(maxAge = 3600)
@RestController
@RequestMapping("/account")
public class AccountController {

    @CrossOrigin(origins = "http://domain2.com")
    @GetMapping("/{id}")
    public Account retrieve(@PathVariable Long id) {
        // ...
    }

    @DeleteMapping("/{id}")
    public void remove(@PathVariable Long id) {
        // ...
    }
}
```

**总结**  
注解方式与过滤器方式适用场景：  
过滤器方式适合于大范围的控制跨域，比如某个controller类的所有放大全部支持某个或几个具体的域名跨域访问的情形。而对于细粒度的跨域控制，比如一个 controller 类中 methodA 支持域名 originA 跨域访问， methodB 支持域名 originB 跨域访问的情况，当然过滤器方式也能实现，但适用注解的方式能轻松很多，尤其是上述情况比较多的情形。

## @MatrixVariable
如果要处理这样的URL：/cars/cell;low=10;brand=a,b,c并获取变量的值

这样的URL中分号后面的变量称为矩阵变量

要在springboot中使用@MatrixVariable处理这样的变量，首先需要重写WebMvcConfigurer中的configurePathMatch方法：

```java

@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void configurePathMatch(PathMatchConfigurer configurer) {
        UrlPathHelper urlPathHelper = new UrlPathHelper();
        urlPathHelper.setRemoveSemicolonContent(false);
        configurer.setUrlPathHelper(urlPathHelper);
    }
```

https://blog.csdn.net/qq_45833786/article/details/111998043

https://blog.csdn.net/qq_45594990/article/details/117392074?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-1.highlightwordscore&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-1.highlightwordscore

https://my.oschina.net/u/2453016/blog/546724

https://blog.csdn.net/securitit/article/details/110675867

## @RequestScope
https://blog.csdn.net/xyjy11/article/details/114201623
## @SessionScope
## @ApplicationScope
## @Lookup
https://blog.csdn.net/ydonghao2/article/details/90898845

https://www.jianshu.com/p/fc574881e3a2