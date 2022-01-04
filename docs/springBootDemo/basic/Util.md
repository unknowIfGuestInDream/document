> spring提供了许多工具类 位于org.springframework.util包下

## stopWatch计时工具类

```markdown
    @Test
    void test() throws InterruptedException {
        StopWatch sw = new StopWatch("test");
        sw.start("task1");
        // do something
        Thread.sleep(100);
        sw.stop();
        sw.start("task2");
        // do something
        Thread.sleep(200);
        sw.stop();
        System.out.println(sw.prettyPrint());
    }
```

## AnnotationUtils注解工具类

```markdown
// 通过 AnnotationUtils.findAnnotation 获取 RateLimiter 注解
        RateLimiter rateLimiter = AnnotationUtils.findAnnotation(method, RateLimiter.class);
```

常用方法：  
1. getAnnotation: 从某个类获取某个annotation
2. findAnnotation: 从类或方法中查找某个annotation。
3. isAnnotationDeclaredLocally: 验证annotation是否直接注释在类上而不是集成来的。
4. isAnnotationInherited: 验证annotation是否继承于另一个class。
5. getAnnotationAttributes: 获取annotation的所有属性。
6. getValue: 获取指定annotation的值. 
7. getDefaultValue: 获取指定annotation或annotation 属性的默认值

## FileCopyUtils文件操作

> FileCopyUtils，它提供了许多一步式的静态操作方法，能够将文件内容拷贝到一个目标 byte[]、String 甚至一个输出流或输出文件中。

[FileCopyUtils API](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/util/FileCopyUtils.html ':target=_blank')


## PropertiesLoaderUtils属性文件操作

> PropertiesLoaderUtils 允许您直接通过基于类路径的文件地址加载属性资源

## StringUtils字符串工具类

* 首字母大写： public static String capitalize(String str)
* 首字母小写：public static String uncapitalize(String str)
* 判断字符串是否为null或empty： public static boolean hasLength(String str)
* 判断字符串是否为非空白字符串(即至少包含一个非空格的字符串)：public static boolean hasText(String str)
* 获取文件名：public static String getFilename(String path) 如e.g. "mypath/myfile.txt" -> "myfile.txt"
* 获取文件扩展名：public static String getFilenameExtension(String path) 如"mypath/myfile.txt" -> "txt"
* 还有譬如数组转集合、集合转数组、路径处理、字符串分离成数组、数组或集合合并为字符串、数组合并、向数组添加元素等。
  
## CollectionUtils集合工具类

> 判断集合是否为空 isEmpty等

## NumberUtils数字处理 

* 字符串转换为Number并格式化，包括具体的Number实现类，如Long、Integer、Double，字符串支持16进制字符串，并且会自动去除字符串中的空格：
* public static <T extends Number> T parseNumber(String text, Class<T> targetClass)
* public static <T extends Number> T parseNumber(String text, Class<T> targetClass, NumberFormat numberFormat)
* 各种Number中的转换，如Long专为Integer，自动处理数字溢出（抛出异常）：
* public static <T extends Number> T convertNumberToTargetClass(Number number, Class<T> targetClass)  

## DigestUtils MD5加密

> 字节数组的MD5加密 public static String md5DigestAsHex(byte[] bytes)

## Assert断言工具类

平时做判断通常都是这样写：
```markdown
if (message== null || message.equls("")) {  
    throw new IllegalArgumentException("输入信息错误!");  
} 
```

用Assert工具类上面的代码可以简化为：  
```markdown
Assert.hasText((message, "输入信息错误!");
```

Assert 类中的常用断言方法：  
Assert.notNull(Object object, "object is required")    -    对象非空   
Assert.isTrue(Object object, "object must be true")   -    对象必须为true     
Assert.notEmpty(Collection collection, "collection must not be empty")    -    集合非空    
Assert.hasLength(String text, "text must be specified")   -    字符不为null且字符长度不为0     
Assert.hasText(String text, "text must not be empty")    -     text 不为null且必须至少包含一个非空格的字符    
Assert.isInstanceOf(Class clazz, Object obj, "clazz must be of type [clazz]")    -    obj必须能被正确造型成为clazz 指定的类  

## ServletRequestUtils请求工具类

```markdown
//取请求参数的整数值：
public static Integer getIntParameter(ServletRequest request, String name)
public static int getIntParameter(ServletRequest request, String name, int defaultVal) -->单个值
public static int[] getIntParameters(ServletRequest request, String name) -->数组
还有譬如long、float、double、boolean、String的相关处理方法。
```

## UriComponents URL编码工具类

```java
@SpringBootTest
public class UriComponentsTest {

    //构造一个简单的URI
    @Test
    public void UriComponents1(){
        UriComponents uriComponents = UriComponentsBuilder.newInstance()
                .scheme("http").host("www.github.com").path("/constructing-uri")
                .queryParam("name", "tom")
                .build();
        System.out.println(uriComponents.toUriString());
    }

    //构造一个编码的URI
    @Test
    public void UriComponents2(){
        UriComponents uriComponents = UriComponentsBuilder.newInstance()
                .scheme("http").host("www.github.com").path("/constructing uri").build().encode();
        System.out.println(uriComponents.toUriString());
    }


    //通过模板构造URI
    @Test
    public void UriComponents3(){
        UriComponents uriComponents = UriComponentsBuilder.newInstance()
                .scheme("http").host("www.github.com").path("/&#123;path-name&#125;")
                .query("name=&#123;keyword&#125;")
                .buildAndExpand("constructing-uri", "tomcat");
        System.out.println(uriComponents.toUriString());
    }


    //从已有的URI中获取信息
    @Test
    public void UriComponents4(){
        // 使用fromUriString()方法，便可以把一个字符串URI转换为UriComponents对象，
        // 并且可以通过getQueryParams()方法取出参数。
        UriComponents result = UriComponentsBuilder
                .fromUriString("https://www.github.com/constructing-uri?name=tomcat").build();
        MultiValueMap<String, String> expectedQueryParams = new LinkedMultiValueMap<>(1);
        expectedQueryParams.add("name", "tomcat");
        System.out.println(result.getQueryParams());
    }
}
```

参考： [Spring 常用的一些工具类](https://www.cnblogs.com/myitnews/p/14017649.html ':target=_blank')