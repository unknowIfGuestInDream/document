>AOP可能对于广大开发者耳熟能详，它是Aspect Oriented Programming的缩写，翻译成中文就是：面向切面编程。这个可能是面试中经常提到的问题，同时它也是Spring框架中一个重大的特性，AOP主要实现的目的是针对业务处理过程中的切面进行提取，它所面对的是处理过程中的某个步骤或阶段，以获得逻辑过程中各部分之间低耦合性的隔离效果，对于我们开发中最常见的可能就是日志记录，事务处理，异常处理等等。

## 开启AOP

springboot使用aop的方式非常简单，只需要在项目中加入依赖spring-boot-starter-aop
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

**创建切面**

```java
/**
 * @author: TangLiang
 * @date: 2020/7/2 14:00
 * @since: 1.0
 */
@Aspect
@Component
//@Order(Ordered.LOWEST_PRECEDENCE-1)
@Order(1)
@Slf4j
public class WebLogAspect {

    /**
     * 定义切入点  具体到selectTest方法
     * 通过@Pointcut注解声明频繁使用的切点表达式
     */
    @Pointcut("execution(public * com.tangl.demo.controller.FirstController.selectTest(..)))")
    public void BrokerAspect() {

    }
    
    //controller包下所有包下的的select开头的方法
    @Pointcut("execution(* com.tangl.demo.controller.*.select*(..))")
    public void select() {

    }

    @Pointcut("execution(* com.tangl.demo.controller.*.insert*(..))")
    public void insert() {

    }
    
    //被LogAnno注解注释的方法
    @Pointcut("@annotation(com.tangl.demo.annotation.LogAnno)")
    public void logAnno() {
    }

    /**
     * @description 在连接点执行之前执行的通知
     */
    //  || 或
    @Before("BrokerAspect() || insert()")
    public void doBeforeGame(JoinPoint joinPoint) {
//        System.out.println("目标方法名为:" + joinPoint.getSignature().getName());
//        System.out.println("目标方法所属类的简单类名:" + joinPoint.getSignature().getDeclaringType().getSimpleName());
//        System.out.println("目标方法所属类的类名:" + joinPoint.getSignature().getDeclaringTypeName());
//        System.out.println("目标方法声明类型:" + Modifier.toString(joinPoint.getSignature().getModifiers()));
//        //获取传入目标方法的参数
//        Object[] args = joinPoint.getArgs();
//        for (int i = 0; i < args.length; i++) {
//            System.out.println("第" + (i + 1) + "个参数为:" + args[i]);
//        }
//        System.out.println("被代理的对象:" + joinPoint.getTarget());
//        System.out.println("代理对象自己:" + joinPoint.getThis());
    }

    //@Around("BrokerAspect()")
    @Around("logAnno()")
    public Object doAround(ProceedingJoinPoint pjd) {
        log.info("进入[{}]方法", pjd.getSignature().getName());
        Object result;
        // 获取方法签名
        MethodSignature methodSignature = (MethodSignature) pjd.getSignature();
        // 获取方法
        Method method = methodSignature.getMethod();
        //获取request 也可以通过注解 都是安全的
        HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes())
                .getRequest();
        try {
            //执行目标方法
            result = pjd.proceed();
            //用新的参数值执行目标方法
            //result = pjd.proceed(new Object[]{"newSpring", "newAop"});
            log.info("离开方法: {} ", pjd.getSignature().getName());
        } catch (Throwable e) {
            e.printStackTrace();
        }

        return result;
    }

    /**
     * @description 在连接点执行之后执行的通知（返回通知和异常通知的异常）
     */
    @After("BrokerAspect()")
    public void doAfterGame(JoinPoint joinPoint) {
    }

    /**
     * @description 在连接点执行之后执行的通知（返回通知）
     */
    @AfterReturning(value = "BrokerAspect()", returning = "result")
    public void doAfterReturningGame(JoinPoint joinPoint, Object result) {
    }

    /**
     * @description 在连接点执行之后执行的通知（异常通知）
     */
    @AfterThrowing(value = "BrokerAspect()", throwing = "exception")
    public void doAfterThrowingGame(JoinPoint joinPoint, Exception exception) {
    }

}
```

- @Aspect 表明是一个切面类
- @Component 将当前类注入到Spring容器内
- @Pointcut 切入点，其中execution用于使用切面的连接点。使用方法：execution(方法修饰符(可选) 返回类型 方法名 参数 异常模式(可选)) ，可以使用通配符匹配字符，*可以匹配任意字符。
- @Before 在方法前执行
- @After 在方法后执行
- @AfterReturning 在方法执行后返回一个结果后执行
- @AfterThrowing 在方法执行过程中抛出异常的时候执行
- @Around 环绕通知，就是可以在执行前后都使用，这个方法参数必须为ProceedingJoinPoint，proceed()方法就是被切面的方法，上面四个方法可以使用JoinPoint，JoinPoint包含了类名，被切面的方法名，参数等信息。

## 使用自定义注解记录日志

**定义一个方法级别的@Log注解，用于标注需要监控的方法：**

```java
/**
 * @author: TangLiang
 * @date: 2020/7/6 16:29
 * @since: 1.0
 */
@Target(ElementType.METHOD) // 方法注解
@Retention(RetentionPolicy.RUNTIME) // 运行时可见
public @interface LogAnno {
    String operateType() default "";// 记录日志的操作类型
}
```

**创建自定义注解对应切面**

为方便获取请求头信息，建议引入下面依赖
```xml
        <!--请求头user-Agent工具类-->
        <dependency>
            <groupId>eu.bitwalker</groupId>
            <artifactId>UserAgentUtils</artifactId>
            <version>1.20</version>
        </dependency>
```

```java
/**
 * @author: TangLiang
 * @date: 2020/7/2 14:00
 * @since: 1.0
 */
@Aspect
@Component
//@Order(Ordered.LOWEST_PRECEDENCE-1)
@Order(1)
@Slf4j
public class WebLogAspect {

    @Pointcut("@annotation(com.tangl.demo.annotation.LogAnno)")
    public void logAnno() {
    }

    @Around("logAnno()")
    public Object doAround(ProceedingJoinPoint pjd) {
        log.info("进入[{}]方法", pjd.getSignature().getName());
        Object result;
        // 获取方法签名
        MethodSignature methodSignature = (MethodSignature) pjd.getSignature();
        // 获取方法
        Method method = methodSignature.getMethod();
        LogAnno logAnno = method.getAnnotation(LogAnno.class);
        String operateType = logAnno.operateType();

        //获取request 也可以通过注解 都是安全的
        HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes())
                .getRequest();

        UserAgent userAgent = UserAgent.parseUserAgentString(request.getHeader("User-Agent"));   //req就是request请求
        Browser browser = userAgent.getBrowser();  //获取浏览器信息
        Version version = userAgent.getBrowserVersion();//浏览器版本
        OperatingSystem os = userAgent.getOperatingSystem(); //获取操作系统信息
        String ipName = IpUtils.getHostName();
        String ip = getIp(request);//获取ip地址
        String url = getUrl(request);//获取url
        Map<String, Object> paramMap = new HashMap();
        Object[] args = pjd.getArgs();
        String[] paramNames = ((CodeSignature) pjd.getSignature()).getParameterNames();
        for (int i = 0, leng = paramNames.length; i < leng; i++) {
            paramMap.put(paramNames[i], args[i]);
        }

        ObjectMapper mapper = new ObjectMapper();
        String paramJson = mapper.writeValueAsString(paramMap);
        log.info("方法描述: [{}]  浏览器: [{}]  浏览器版本： [{}]  操作系统: [{}]  用户: [{}]  IP: [{}]  URL: [{}] 参数： [{}]", operateType, browser, version, os, ipName, ip, url, paramJson);

        //将日志信息存到数据库
        //实战中日志存储操作不影响实际业务，建议对存储日志操作进行异步处理或者使用消息队列进行处理

        try {
            //执行目标方法
            result = pjd.proceed();
            //用新的参数值执行目标方法
            //result = pjd.proceed(new Object[]{"newSpring", "newAop"});
            log.info("离开方法: {} ", pjd.getSignature().getName());
        } catch (Throwable e) {
            e.printStackTrace();
            Map map = new HashMap();
            map.put("success", false);
            map.put("message", e.getMessage());
            log.error("异常信息: {} ", e.getMessage());
            return map;
        }

        return result;
    }
}
```

BaseUtil 获取ip跟url路径的方法
```java
public class BaseUtil {
    public static String getIp(HttpServletRequest request) {
        String ip = request.getHeader("X-FORWARDED-FOR");
        if (StringUtils.isEmpty(ip) || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("Proxy-Client-IP");
        }
        if (StringUtils.isEmpty(ip) || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("WL-Proxy-Client-IP");
        }
        if (StringUtils.isEmpty(ip) || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("HTTP_CLIENT_IP");
        }
        if (StringUtils.isEmpty(ip) || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getHeader("HTTP_X_FORWARDED_FOR");
        }
        if (StringUtils.isEmpty(ip) || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getRemoteAddr();
        }
        if ("0:0:0:0:0:0:0:1".equals(ip)) {
            return "127.0.0.1";
        }

        return ip;
    }

    public static String getUrl(HttpServletRequest request) {
        String url = request.getScheme() + "://" + request.getServerName() + ":" + request.getServerPort() + request.getServletPath();
        if (request.getQueryString() != null) {
            url += "?" + request.getQueryString();
        }

        return url;
    }
}
```

**测试**

```markdown
    @PostMapping(value = "selectTest")
    @ResponseBody
    @LogAnno(operateType = "查询Test")
    public Map<String, Object> selectTest(String ID_) throws SQLException {
        Map<String, Object> result = new HashMap<String, Object>();
        result.put("success", true);
        return result;
    }
```

## 结合 Guava 的 RateLimiter 实现限流

引入依赖: 
```xml
        <!-- 谷歌工具组件-->
        <dependency>
            <groupId>com.google.guava</groupId>
            <artifactId>guava</artifactId>
            <version>29.0-jre</version>
        </dependency>
```

**定义一个限流注解 RateLimiter**
```java
/**
 * 限流注解
 *
 * @author: TangLiang
 * @date: 2020/12/18 21:38
 * @since: 1.0
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface RateLimiter {
    int NOT_LIMITED = 0;

    /**
     * qps
     */
    @AliasFor("qps") double value() default NOT_LIMITED;

    /**
     * qps
     */
    @AliasFor("value") double qps() default NOT_LIMITED;

    /**
     * 超时时长
     */
    int timeout() default 0;

    /**
     * 超时时间单位
     */
    TimeUnit timeUnit() default TimeUnit.MILLISECONDS;
}
```

> 注意代码里使用了 AliasFor 设置一组属性的别名，所以获取注解的时候，需要通过 Spring 提供的注解工具类 AnnotationUtils 获取，不可以通过 AOP 参数注入的方式获取，否则有些属性的值将会设置不进去。

** 定义一个切面 RateLimiterAspect**

```java
/**
 * 限流切面
 *
 * @author: TangLiang
 * @date: 2020/12/18 21:38
 * @since: 1.0
 */
@Slf4j
@Aspect
@Component
public class RateLimiterAspect {
    private static final ConcurrentMap<String, com.google.common.util.concurrent.RateLimiter> RATE_LIMITER_CACHE = new ConcurrentHashMap<>();

    @Pointcut("@annotation(com.tangl.demo.annotation.RateLimiter)")
    public void rateLimit() {

    }

    /*
    注意代码里使用了 AliasFor 设置一组属性的别名，所以获取注解的时候，
    需要通过 Spring 提供的注解工具类 AnnotationUtils 获取，不可以通过 AOP 参数注入的方式获取，否则有些属性的值将会设置不进去。
     */
    @Around("rateLimit()")
    public Object pointcut(ProceedingJoinPoint point) throws Throwable {
        MethodSignature signature = (MethodSignature) point.getSignature();
        Method method = signature.getMethod();
        // 通过 AnnotationUtils.findAnnotation 获取 RateLimiter 注解
        RateLimiter rateLimiter = AnnotationUtils.findAnnotation(method, RateLimiter.class);
        if (rateLimiter != null && rateLimiter.qps() > RateLimiter.NOT_LIMITED) {
            double qps = rateLimiter.qps();
            if (RATE_LIMITER_CACHE.get(method.getName()) == null) {
                // 初始化 QPS
                RATE_LIMITER_CACHE.put(method.getName(), com.google.common.util.concurrent.RateLimiter.create(qps));
            }

            log.debug("【{}】的QPS设置为: {}", method.getName(), RATE_LIMITER_CACHE.get(method.getName()).getRate());
            // 尝试获取令牌
            if (RATE_LIMITER_CACHE.get(method.getName()) != null && !RATE_LIMITER_CACHE.get(method.getName()).tryAcquire(rateLimiter.timeout(), rateLimiter.timeUnit())) {
                throw new RuntimeException("手速太快了，慢点儿吧~");
            }
        }
        return point.proceed();
    }
}
```

**定义两个API接口用于测试限流**

```java
/**
 * 限流
 *
 * @author: TangLiang
 * @date: 2020/12/18 21:43
 * @since: 1.0
 */
@RestController
@RequestMapping("/rateLimit")
@Slf4j
public class RateLimitController {

    //限流请求
    @RateLimiter(value = 1.0, timeout = 300)
    @GetMapping("/test1")
    public Map test1() {
        Map<String,Object> result = new HashMap();
        result.put("message","hello");
        result.put("description","别想一直看到我，不信你快速刷新看看~");
        log.info("【test1】被执行了。。。。。");
        return result;
    }

    //不限流请求
    @GetMapping("/test2")
    public Map test2() {
        Map<String,Object> result = new HashMap();
        result.put("message","hello");
        result.put("description","我一直都在，卟离卟弃");
        log.info("【test2】被执行了。。。。。");
        return result;
    }
}
```