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

## ObjectUtils 对象工具类
1、获取对象的基本信息
```java
// 获取对象的类名。参数为 null 时，返回字符串："null" 
String nullSafeClassName(Object obj)
// 参数为 null 时，返回 0
int nullSafeHashCode(Object object)
// 参数为 null 时，返回字符串："null"
String nullSafeToString(boolean[] array)
// 获取对象 HashCode（十六进制形式字符串）。参数为 null 时，返回 0 
String getIdentityHexString(Object obj)
// 获取对象的类名和 HashCode。 参数为 null 时，返回字符串："" 
String identityToString(Object obj)
// 相当于 toString()方法，但参数为 null 时，返回字符串：""
String getDisplayString(Object obj)
```

2、判断工具
```java
// 判断数组是否为空
boolean isEmpty(Object[] array)
// 判断参数对象是否是数组
boolean isArray(Object obj)
// 判断数组中是否包含指定元素
boolean containsElement(Object[] array, Object element)
// 相等，或同为 null时，返回 true
boolean nullSafeEquals(Object o1, Object o2)
/*
判断参数对象是否为空，判断标准为：
    Optional: Optional.empty()
       Array: length == 0
CharSequence: length == 0
  Collection: Collection.isEmpty()
         Map: Map.isEmpty()
 */
boolean isEmpty(Object obj)
```

3、其他工具方法
```java
// 向参数数组的末尾追加新元素，并返回一个新数组
<A, O extends A> A[] addObjectToArray(A[] array, O obj)
// 原生基础类型数组 --> 包装类数组
Object[] toObjectArray(Object source)
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

1、输入
```java
// 从文件中读入到字节数组中
byte[] copyToByteArray(File in)
// 从输入流中读入到字节数组中
byte[] copyToByteArray(InputStream in)
// 从输入流中读入到字符串中
String copyToString(Reader in)
```

2、输出
```java
// 从字节数组到文件
void copy(byte[] in, File out)
// 从文件到文件
int copy(File in, File out)
// 从字节数组到输出流
void copy(byte[] in, OutputStream out) 
// 从输入流到输出流
int copy(InputStream in, OutputStream out) 
// 从输入流到输出流
int copy(Reader in, Writer out)
// 从字符串到输出流
void copy(String in, Writer out)
```

## PropertiesLoaderUtils属性文件操作

> PropertiesLoaderUtils 允许您直接通过基于类路径的文件地址加载属性资源

## StringUtils字符串工具类
1、字符串判断工具
```java
// 判断字符串是否为 null，或 ""。注意，包含空白符的字符串为非空
boolean isEmpty(Object str)
// 判断字符串是否是以指定内容结束。忽略大小写
boolean endsWithIgnoreCase(String str, String suffix)
// 判断字符串是否已指定内容开头。忽略大小写
boolean startsWithIgnoreCase(String str, String prefix) 
// 是否包含空白符
boolean containsWhitespace(String str)
// 判断字符串非空且长度不为 0，即，Not Empty
boolean hasLength(CharSequence str)
// 判断字符串是否包含实际内容，即非仅包含空白符，也就是 Not Blank
boolean hasText(CharSequence str)
// 判断字符串指定索引处是否包含一个子串。
boolean substringMatch(CharSequence str, int index, CharSequence substring)
// 计算一个字符串中指定子串的出现次数
int countOccurrencesOf(String str, String sub)
```

2、字符串操作工具
```java
//首字母大写
String capitalize(String str)
//首字母小写
String uncapitalize(String str)
// 查找并替换指定子串
String replace(String inString, String oldPattern, String newPattern)
// 去除尾部的特定字符
String trimTrailingCharacter(String str, char trailingCharacter) 
// 去除头部的特定字符
String trimLeadingCharacter(String str, char leadingCharacter)
// 去除头部的空白符
String trimLeadingWhitespace(String str)
// 去除头部的空白符
String trimTrailingWhitespace(String str)
// 去除头部和尾部的空白符
String trimWhitespace(String str)
// 删除开头、结尾和中间的空白符
String trimAllWhitespace(String str)
// 删除指定子串
String delete(String inString, String pattern)
// 删除指定字符（可以是多个）
String deleteAny(String inString, String charsToDelete)
// 对数组的每一项执行 trim() 方法
String[] trimArrayElements(String[] array)
// 将 URL 字符串进行解码
String uriDecode(String source, Charset charset)
```

3、路径相关工具方法
```java
// 解析路径字符串，优化其中的 “..” 
String cleanPath(String path)
// 解析路径字符串，解析出文件名部分
String getFilename(String path)
// 解析路径字符串，解析出文件后缀名
String getFilenameExtension(String path)
// 比较两个两个字符串，判断是否是同一个路径。会自动处理路径中的 “..” 
boolean pathEquals(String path1, String path2)
// 删除文件路径名中的后缀部分
String stripFilenameExtension(String path) 
// 以 “. 作为分隔符，获取其最后一部分
String unqualify(String qualifiedName)
// 以指定字符作为分隔符，获取其最后一部分
String unqualify(String qualifiedName, char separator)
```
  
## CollectionUtils集合工具类
1、集合判断工具
```java
// 判断 List/Set 是否为空
boolean isEmpty(Collection<?> collection)
// 判断 Map 是否为空
boolean isEmpty(Map<?,?> map)
// 判断 List/Set 中是否包含某个对象
boolean containsInstance(Collection<?> collection, Object element)
// 以迭代器的方式，判断 List/Set 中是否包含某个对象
boolean contains(Iterator<?> iterator, Object element)
// 判断 List/Set 是否包含某些对象中的任意一个
boolean containsAny(Collection<?> source, Collection<?> candidates)
// 判断 List/Set 中的每个元素是否唯一。即 List/Set 中不存在重复元素
boolean hasUniqueObject(Collection<?> collection)
```

2、集合操作工具
```java
// 将 Array 中的元素都添加到 List/Set 中
<E> void mergeArrayIntoCollection(Object array, Collection<E> collection)  
// 将 Properties 中的键值对都添加到 Map 中
<K,V> void mergePropertiesIntoMap(Properties props, Map<K,V> map)
// 返回 List 中最后一个元素
<T> T lastElement(List<T> list)  
// 返回 Set 中最后一个元素
<T> T lastElement(Set<T> set) 
// 返回参数 candidates 中第一个存在于参数 source 中的元素
<E> E findFirstMatch(Collection<?> source, Collection<E> candidates)
// 返回 List/Set 中指定类型的元素。
<T> T findValueOfType(Collection<?> collection, Class<T> type)
// 返回 List/Set 中指定类型的元素。如果第一种类型未找到，则查找第二种类型，以此类推
Object findValueOfType(Collection<?> collection, Class<?>[] types)
// 返回 List/Set 中元素的类型
Class<?> findCommonElementType(Collection<?> collection)
```

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

## ResourceUtils 资源工具类
1、从资源路径获取文件
```java
// 判断字符串是否是一个合法的 URL 字符串。
static boolean isUrl(String resourceLocation)
// 获取 URL
static URL getURL(String resourceLocation) 
// 获取文件（在 JAR 包内无法正常使用，需要是一个独立的文件）
static File getFile(String resourceLocation)
```

2、Resource
```java
// 文件系统资源 D:\...
FileSystemResource
// URL 资源，如 file://... http://...
UrlResource
// 类路径下的资源，classpth:...
ClassPathResource
// Web 容器上下文中的资源（jar 包、war 包）
ServletContextResource
// 判断资源是否存在
boolean exists()
// 从资源中获得 File 对象
File getFile()
// 从资源中获得 URI 对象
URI getURI()
// 从资源中获得 URI 对象
URL getURL()
// 获得资源的 InputStream
InputStream getInputStream()
// 获得资源的描述信息
String getDescription()
```

## ReflectionUtils 反射工具类
1、获取方法
```java
// 在类中查找指定方法
Method findMethod(Class<?> clazz, String name) 
// 同上，额外提供方法参数类型作查找条件
Method findMethod(Class<?> clazz, String name, Class<?>... paramTypes) 
// 获得类中所有方法，包括继承而来的
Method[] getAllDeclaredMethods(Class<?> leafClass) 
// 在类中查找指定构造方法
Constructor<T> accessibleConstructor(Class<T> clazz, Class<?>... parameterTypes) 
// 是否是 equals() 方法
boolean isEqualsMethod(Method method) 
// 是否是 hashCode() 方法 
boolean isHashCodeMethod(Method method) 
// 是否是 toString() 方法
boolean isToStringMethod(Method method) 
// 是否是从 Object 类继承而来的方法
boolean isObjectMethod(Method method) 
// 检查一个方法是否声明抛出指定异常
boolean declaresException(Method method, Class<?> exceptionType) 
```

2、执行方法
```java
// 执行方法
Object invokeMethod(Method method, Object target)  
// 同上，提供方法参数
Object invokeMethod(Method method, Object target, Object... args) 
// 取消 Java 权限检查。以便后续执行该私有方法
void makeAccessible(Method method) 
// 取消 Java 权限检查。以便后续执行私有构造方法
void makeAccessible(Constructor<?> ctor) 
```

3、获取字段
```java
// 在类中查找指定属性
Field findField(Class<?> clazz, String name) 
// 同上，多提供了属性的类型
Field findField(Class<?> clazz, String name, Class<?> type) 
// 是否为一个 "public static final" 属性
boolean isPublicStaticFinal(Field field) 
```

4、设置字段
```java
// 获取 target 对象的 field 属性值
Object getField(Field field, Object target) 
// 设置 target 对象的 field 属性值，值为 value
void setField(Field field, Object target, Object value) 
// 同类对象属性对等赋值
void shallowCopyFieldState(Object src, Object dest)
// 取消 Java 的权限控制检查。以便后续读写该私有属性
void makeAccessible(Field field) 
// 对类的每个属性执行 callback
void doWithFields(Class<?> clazz, ReflectionUtils.FieldCallback fc) 
// 同上，多了个属性过滤功能。
void doWithFields(Class<?> clazz, ReflectionUtils.FieldCallback fc, 
                  ReflectionUtils.FieldFilter ff) 
// 同上，但不包括继承而来的属性
void doWithLocalFields(Class<?> clazz, ReflectionUtils.FieldCallback fc) 
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