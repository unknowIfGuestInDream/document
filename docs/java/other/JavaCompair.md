> 本文旨在介绍Java11相对Java8的新特性，包括Java9与Java10引入的特性。主要是新的语法特性，模块化开发，
> 以及其他方面的一些新特性。

## 新的语法特性
Java11相对Java8，在语法上的新特性并不多。主要有：
1. 本地变量类型推断
2. HttpClient
3. Collection增强
4. Stream增强
5. Optional增强
6. String增强
7. InputStream增强

### 本地变量类型推断
Java10以后可以用var定义一个局部变量，不用显式写出它的类型。但要注意，被var定义的变量仍然是静态类型，编译器会试图去推断其类型。
```java
String strBeforeJava10 = "strBeforeJava10";
var strFromJava10 = "strFromJava10";
System.out.println(strBeforeJava10);
System.out.println(strFromJava10);
```
因此，要注意：

不兼容的类型是不能重新赋值的!
```java
// 例如下面的语句编译会失败，"InCompatible types."
strFromJava10 = 10;
```
只要编译器无法推断出变量类型，就会编译错误！
```java
// 例如下面这些都无法通过编译:
var testVarWithoutInitial;
var testNull = null;
var testLamda = () -> System.out.println("test");
var testMethodByLamda = () -> giveMeString();
var testMethod2 = this::giveMeString;
```
而推荐使用类型推断的场景有：

* 简化泛型声明  
```java
// 如下所示，Map <String，List <Integer >>类型，可以被简化为单个var关键字
var testList = new ArrayList<Map<String, List<Integer>>>();
for (var curEle : testList) {
    // curEle能够被推断出类型是 Map<String, List<Integer>>
    if (curEle != null) {
        curEle.put("test", new ArrayList<>());
    }
}
```
* lambda参数  
```java
// 从Java 11开始，lambda参数也允许使用var关键字：
Predicate<String> predNotNull = (var a) -> a != null && a.trim().length() > 0;
String strAfterFilter = Arrays.stream((new String[]{"a", "", null, "x"}))
        .filter(predNotNull)
        .collect(Collectors.joining(","));
System.out.println(strAfterFilter);
```

### HttpClient
Java 9开始引入HttpClient API来处理HTTP请求。 从Java 11开始，这个API正式进入标准库包。参考网址：http://openjdk.java.net/groups/net/httpclient/intro.html  
HttpClient具有以下特性:
* 同时支持 HTTP1.1 和 HTTP2 协议，并支持 websocket
* 同时支持同步和异步编程模型
* 将请求和响应主体作为响应式流(reactive-streams)处理，并使用构建器模式

**HttpClient**  
要发送http请求，首先要使用其构建器创建一个HttpClient。这个构建器能够配置每个客户端的状态：

* 首选协议版本 ( HTTP/1.1 或 HTTP/2 )
* 是否跟随重定向
* 代理
* 身份验证

一旦构建完成，就可以使用HttpClient发送多个请求。

**HttpRequest**  
HttpRequest是由它的构建器创建的。请求的构建器可用于设置:
* 请求URI
* 请求Method ( GET, PUT, POST )
* 请求主体(如果有)
* 超时时间
* 请求头

HttpRequest构建之后是不可变的，但可以发送多次。

**Synchronous or Asynchronous**  
请求既可以同步发送，也可以异步发送。当然同步的API会导致线程阻塞直到HttpResponse可用。
异步API立即返回一个CompletableFuture，
当HttpResponse可用时，它将获取HttpResponse并执行后续处理。

**Data as reactive-streams**  
请求和响应的主体作为响应式流(具有非阻塞背压的异步数据流)供外部使用。HttpClient实际上是请求正文的订阅者和响应正文字节的发布者。
BodyHandler接口允许在接收实际响应体之前检查响应代码和报头，并负责创建响应BodySubscriber。

HttpRequest和HttpResponse类型提供了许多便利的工厂方法，用于创建请求发布者和响应订阅者，以处理常见的主体类型，
如文件、字符串和字节。这些便利的实现要么累积数据，直到可以创建更高级别的Java类型（如String），要么就文件流传输数据。
BodySubscriber和BodyPublisher接口可以实现为自定义反应流处理数据。

HttpRequest和HttpResponse还提供了转换器，用于将 java.util.concurrent.Flow 的 Publisher/Subscriber 类型转换为 
HTTP Client的 BodyPublisher/BodySubscriber 类型。

**HTTP/2**  
Java HTTP Client支持 HTTP/1.1 和 HTTP/2。默认情况下，客户端将使用 HTTP/2 发送请求。发送到尚不支持 HTTP/2 的服务器的请求将自动降级为 HTTP/1.1。
以下是HTTP/2带来的主要改进:
* 标头压缩。 HTTP/2 使用 HPACK 压缩，从而减少了开销。
* 与服务器的单一连接减少了建立多个TCP连接所需的往返次数。
* 多路复用。 在同一连接上，同时允许多个请求。
* 服务器推送。 可以将其他将来需要的资源发送给客户端。
* 二进制格式。 更紧凑。

由于HTTP/2是默认的首选协议，并且在需要的地方无缝地实现回退到HTTP/1.1，那么当HTTP/2被更广泛地部署时，Java HTTP客户端就无需修正它的应用代码。

<details>
  <summary>代码演示</summary>

```java
package jdk11;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.WebSocket;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionStage;
import java.util.concurrent.TimeUnit;

/**
 * HttpClient
 *
 * @author zhaochun
 */
 public class TestCase02HttpClient {
    public static void main(String[] args) throws Exception {
        TestCase02HttpClient me = new TestCase02HttpClient();
        me.testHttpClientGetSync();
        me.testHttpClientGetAsync();
        me.testHttpClientPost();

        // 同一个HttpClient先登录网站获取token，再请求受限制资源，从而爬取需要认证的资源
        me.testLogin();

        // HttpClient支持websocket
        me.testWebsocket();
    }

    private void testHttpClientGetSync() {
        var url = "https://openjdk.java.net/";
        var request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();
        var client = HttpClient.newHttpClient();
        try {
            System.out.println(String.format("send begin at %s", LocalDateTime.now()));
            // 同步请求
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            System.out.println(String.format("send end at %s", LocalDateTime.now()));
            System.out.println(String.format("receive response : %s", response.body().substring(0, 10)));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void testHttpClientGetAsync() {
        var url = "https://openjdk.java.net/";
        var request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();
        var client = HttpClient.newHttpClient();
        try {
            System.out.println(String.format("sendAsync begin at %s", LocalDateTime.now()));
            // 异步请求
            client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                    .thenApply(stringHttpResponse -> {
                        System.out.println(String.format("receive response at %s", LocalDateTime.now()));
                        return stringHttpResponse.body();
                    })
                    .thenAccept(s -> System.out.println(String.format("receive response : %s at %s", s.substring(0, 10), LocalDateTime.now())));
            System.out.println(String.format("sendAsync end at %s", LocalDateTime.now()));

            // 为了防止异步请求尚未返回主线程就结束(jvm会退出)，这里让主线程sleep 10秒
            System.out.println("Main Thread sleep 10 seconds start...");
            Thread.sleep(10000);
            System.out.println("Main Thread sleep 10 seconds stop...");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void testHttpClientPost() {
        var url = "http://localhost:30001/jdk11/test/helloByPost";
        var request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "text/plain")
                .POST(HttpRequest.BodyPublishers.ofString("zhangsan"))
                .build();
        var client = HttpClient.newHttpClient();
        try {
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            System.out.println(response.statusCode());
            System.out.println(response.body());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void testLogin() throws Exception {
        var client = HttpClient.newHttpClient();
        // 某测试环境用户登录URL
        var urlLogin = "http://x.x.x.x:xxxx/xxx/login";
        var requestObj = new HashMap<String, Object>();
        requestObj.put("username", "xxxxxx");
        requestObj.put("password", "xxxxxxxxxxxxxxxx");
        var objectMapper = new ObjectMapper();
        var requestBodyJson = objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(requestObj);
        var requestLogin = HttpRequest.newBuilder()
                .uri(URI.create(urlLogin))
                .header("Content-Type", "application/json;charset=UTF-8")
                .POST(HttpRequest.BodyPublishers.ofString(requestBodyJson))
                .build();
        HttpResponse<String> responseLogin = client.send(requestLogin, HttpResponse.BodyHandlers.ofString());
        // 这里的登录网站使用token，而没有使用session，因此我们需要从返回的报文主体中查找token信息；
        // 如果是使用session的网站，这里需要从响应的headers中查找"set-cookie"从而获取session id，并在后续请求中，将sid设置到header的Cookie中。
        // 如： responseLogin.headers().map().get("set-cookie")获取cookies，再从中查找sid。
        var loginResponse = responseLogin.body();
        var mpLoginResponse = objectMapper.readValue(loginResponse, Map.class);
        var dataLogin = (Map<String, Object>) mpLoginResponse.get("data");
        var token = dataLogin.get("token").toString();
        // 测试环境获取某资源的URL
        var urlGetResource = "http://xxxx:xxxx/xxx/resource";
        var requestRes = HttpRequest.newBuilder()
                .uri(URI.create(urlGetResource))
                .header("Content-Type", "application/json;charset=UTF-8")
                // 注意，token并非一定设置到header的Authorization中，这取决于网站验证的方式，也有可能token也放到cookie里。
                // 但对于使用session的网站，sid都是设置在cookie里的。如: .header("Cookie", "JSESSIONID=" + sid)
                .header("Authorization", token)
                .GET()
                .build();
        HttpResponse<String> responseResource = client.send(requestRes, HttpResponse.BodyHandlers.ofString());
        var response = responseResource.body();
        System.out.println(response);
    }

    private void testWebsocket() {
        var wsUrl = "ws://localhost:30001/ws/test";
        var httpClient = HttpClient.newHttpClient();
        WebSocket websocketClient = httpClient.newWebSocketBuilder()
                .buildAsync(URI.create(wsUrl), new WebSocket.Listener() {
                    @Override
                    public void onOpen(WebSocket webSocket) {
                        System.out.println("onOpen : webSocket opened.");
                        webSocket.request(1);
                    }

                    @Override
                    public CompletionStage<?> onText(WebSocket webSocket, CharSequence data, boolean last) {
                        System.out.println("onText");
                        webSocket.request(1);
                        return CompletableFuture.completedFuture(data)
                                .thenAccept(System.out::println);
                    }

                    @Override
                    public CompletionStage<?> onClose(WebSocket webSocket, int statusCode, String reason) {
                        System.out.println("ws closed with status(" + statusCode + "). cause:" + reason);
                        webSocket.sendClose(statusCode, reason);
                        return null;
                    }

                    @Override
                    public void onError(WebSocket webSocket, Throwable error) {
                        System.out.println("error: " + error.getLocalizedMessage());
                        webSocket.abort();
                    }
                }).join();

        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // last参数用于指示websocketClient，本次发送的数据是否是完整消息的最后部分。
        // 如果是false，则websocketClient不会把消息发送给websocket后台的listener，只会把数据缓存起来；
        // 当传入true时，会将之前缓存的数据和这次的数据拼接起来一起发送给websocket后台的listener。
        websocketClient.sendText("test1", false);
        websocketClient.sendText("test2", true);

        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        websocketClient.sendText("org_all_request", true);

        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        websocketClient.sendText("employee_all_request", true);

        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        websocketClient.sendClose(WebSocket.NORMAL_CLOSURE, "Happy ending.");
    }
}
```

</details> 

### Collection增强
List,Set,Map有了新的增强方法：of与copyOf。

**List的of与copyOf**  
List.of根据传入的参数列表创建一个新的不可变List集合；List.copyOf根据传入的list对象创建一个不可变副本。
```java
var listImmutable = List.of("a", "b", "c");
var listImmutableCopy = List.copyOf(listImmutable);
```

由于拷贝的集合本身就是一个不可变对象，因此拷贝实际上并没有创建新的对象，直接使用了原来的不可变对象。
```java
// 结果为true
System.out.println(listImmutable == listImmutableCopy);
// 不可变对象不能进行修改
try {
    listImmutable.add("d");
} catch (Throwable t) {
    System.out.println("listImmutable can not be modified!");
}
try {
    listImmutableCopy.add("d");
} catch (Throwable t) {
    System.out.println("listImmutableCopy can not be modified!");
}
```
如果想快速新建一个可变的集合对象，可以直接使用之前的不可变集合作为构造参数，创建一个新的可变集合。
```java
var listVariable = new ArrayList<>(listImmutable);
var listVariableCopy = List.copyOf(listVariable);
```
新创建的可变集合当然是一个新的对象，从这个新对象拷贝出来的不可变副本也是一个新的对象，并不是之前的不可变集合。
```java
System.out.println(listVariable == listImmutable); // false
System.out.println(listVariable == listVariableCopy); // false
System.out.println(listImmutable == listVariableCopy); // false
// 新的可变集合当然是可以修改的
try {
    listVariable.add("d");
} catch (Throwable t) {
    System.out.println("listVariable can not be modified!");
}
// 可变集合拷贝出来的副本依然是不可变的
try {
    listVariableCopy.add("d");
} catch (Throwable t) {
    System.out.println("listVariableCopy can not be modified!");
}
```

**Set的of和copyOf**  
Set的of和copyOf与List类似。
```java
var set = Set.of("a", "c", "r", "e");
var setCopy = Set.copyOf(set);
System.out.println(set == setCopy);
```
但要注意，用of创建不可变Set时，要确保元素不重复，否则运行时会抛出异常: "java.lang.IllegalArgumentException: duplicate element"
```java
try {
    var setErr = Set.of("a", "b", "a");
} catch (Throwable t) {
    t.printStackTrace();
}
```
当然创建可变set后添加重复元素不会抛出异常，但会被去重
```java
var setNew = new HashSet<>(set);
setNew.add("c");
System.out.println(setNew.toString());
```

**Map的of和copyOf**  
Map的of和copyOf与list,set类似，注意of方法的参数列表是依次传入key和value：
```java
var map = Map.of("a", 1, "b", 2);
var mapCopy = Map.copyOf(map);
System.out.println(map == mapCopy);
```
当然也要注意创建不可变Map时，key不能重复
```java
try {
    var mapErr = Map.of("a", 1, "b", 2, "a", 3);
} catch (Throwable t) {
    t.printStackTrace();
}
```

### Stream增强
Java8开始引入stream，Java11提供了一些扩展：

* 单个元素直接构造为Stream对象
* dropWhile与takeWhile
* 重载iterate方法用于限制无限流范围

单个元素直接构造为Stream对象  
注意null与""的区别：
```java
long size1 = Stream.ofNullable(null).count();
System.out.println(size1); // 0
long size2 = Stream.ofNullable("").count();
System.out.println(size2); // 1
```

**dropWhile与takeWhile**  
dropWhile，对于有序的stream，从头开始去掉满足条件的元素，一旦遇到不满足元素的就结束
```java
List lst1 = Stream.of(1, 2, 3, 4, 5, 4, 3, 2, 1)
        .dropWhile(e -> e < 3)
        .collect(Collectors.toList());
System.out.println(lst1); // [3, 4, 5, 4, 3, 2, 1]
```

takeWhile，对于有序的stream，从头开始保留满足条件的元素，一旦遇到不满足的元素就结束
```java
List lst2 = Stream.of(1, 2, 3, 4, 5, 4, 3, 2, 1)
        .takeWhile(e -> e < 3)
        .collect(Collectors.toList());
System.out.println(lst2); // [1, 2]
```

即使把剩下的元素都收集到了无序的set中，但在此之前，stream对象是有序的，因此结果包含了原来stream中最后的[a2]和[a1]：
```java
Set set1 = Stream.of("a1", "a2", "a3", "a4", "a5", "a4", "a3", "a2", "a1")
        .dropWhile(e -> "a3".compareTo(e) > 0)
        .collect(Collectors.toSet());
System.out.println(set1); // [a1, a2, a3, a4, a5]
```

如果先创建一个无序不重复的set集合，set无序更准确的说法是不保证顺序不变，事实上是有顺序的。
因此这里会发现，dropWhile还是按set当前的元素顺序判定的，一旦不满足条件就结束。
```java
Set<String> set = new HashSet<>();
for (int i = 1; i <= 100 ; i++) {
    set.add("test" + i);
}
System.out.println(set);
Set setNew = set.stream()
        .dropWhile(s -> "test60".compareTo(s) > 0)
        .collect(Collectors.toSet());
System.out.println(setNew);
```

**重载iterate方法用于限制无限流范围**  
java8里可以创建一个无限流，比如下面这个数列，起始值是1，后面每一项都在前一项的基础上 * 2 + 1，通过limit限制这个流的长度：
```java
Stream<Integer> streamInJava8 = Stream.iterate(1, t -> 2 * t + 1);
// 打印出该数列的前十个: 1,3,7,15,31,63,127,255,511,1023
System.out.println(streamInJava8.limit(10).map(Object::toString).collect(Collectors.joining(",")));
```

从Java9开始，iterate方法可以添加一个判定器，例如，限制数的大小不超过1000
```java
Stream<Integer> streamFromJava9 = Stream.iterate(1, t -> t < 1000, t -> 2 * t + 1);
// 这里打印的结果是 1,3,7,15,31,63,127,255,511
System.out.println(streamFromJava9.map(Objects::toString).collect(Collectors.joining(",")));
```

### Optional增强
可以将Optional对象直接转为stream
```java
Optional.of("Hello openJDK11").stream()
        .flatMap(s -> Arrays.stream(s.split(" ")))
        .forEach(System.out::println);
```

可以为Optional对象提供一个默认的Optional对象
```java
System.out.println(Optional.empty()
        .or(() -> Optional.of("default"))
        .get());
```

### String增强
String方面，针对空白字符(空格，制表符，回车，换行等)，提供了一些新的方法。

**isBlank**  
判断目标字符串是否是空白字符。以下结果全部为true：
```java
// 半角空格
System.out.println(" ".isBlank());
// 全角空格
System.out.println("　".isBlank());
// 半角空格的unicode字符值
System.out.println("\u0020".isBlank());
// 全角空格的unicode字符值
System.out.println("\u3000".isBlank());
// 制表符
System.out.println("\t".isBlank());
// 回车
System.out.println("\r".isBlank());
// 换行
System.out.println("\n".isBlank());
// 各种空白字符拼接
System.out.println(" \t\r\n　".isBlank());
```

**strip，stripLeading与stripTrailing**  
去除首尾的空白字符:
```java
// 全角空格 + 制表符 + 回车 + 换行 + 半角空格 + <内容> + 全角空格 + 制表符 + 回车 + 换行 + 半角空格
var strTest = "　\t\r\n 你好 jdk11　\t\r\n ";

// strip 去除两边空白字符
System.out.println("[" + strTest.strip() + "]");
// stripLeading 去除开头的空白字符
System.out.println("[" + strTest.stripLeading() + "]");
// stripTrailing 去除结尾的空白字符
System.out.println("[" + strTest.stripTrailing() + "]");
```

**repeat**  
重复字符串内容，拼接新的字符串:
```java
var strOri = "jdk11";
var str1 = strOri.repeat(1);
var str2 = strOri.repeat(3);
System.out.println(str1);
System.out.println(str2);
// repeat传入参数为1时，不会创建一个新的String对象，而是直接返回原来的String对象。
System.out.println(str1 == strOri);
```

**lines**  
lines方法用 r 或 n 或 rn 对字符串切割并返回stream对象:
```java
var strContent = "hello java\rhello jdk11\nhello world\r\nhello everyone";
// lines方法用 \r 或 \n 或 \r\n 对字符串切割并返回stream对象
strContent.lines().forEach(System.out::println);
System.out.println(strContent.lines().count());
```

### InputStream增强
InputStream提供了一个新的方法transferTo，将输入流直接传输到输出流：
```java
inputStream.transferTo(outputStream);
```

## 模块化开发简介
如果把 Java 8 比作单体应用，那么引入模块系统之后，从 Java 9 开始，Java 就华丽的转身为微服务。模块系统，项目代号 Jigsaw，
最早于 2008 年 8 月提出(比 Martin Fowler 提出微服务还早 6 年)，2014 年跟随 Java 9 正式进入开发阶段，最终跟随 Java 9 发布于 2017 年 9 月。

那么什么是模块系统?官方的定义是A uniquely named, reusable group of related packages, as well as resources (such as images and XML files) 
and a module descriptor.模块的载体是 jar 文件，一个模块就是一个 jar 文件，但相比于传统的 jar 文件，模块的根目录下多了一个module-info.class 文件，
也即 module descriptor。 module descriptor 包含以下信息：

* 模块名称
* 依赖哪些模块
* 导出模块内的哪些包(允许直接 import 使用)
* 开放模块内的哪些包(允许通过 Java 反射访问)
* 提供哪些服务
* 依赖哪些服务

也就是说，任意一个 jar 文件，只要加上一个合法的 module descriptor，就可以升级为一个模块。这个看似微小的改变，到底可以带来哪些好处?在我看来，至少带来四方面的好处。

第一，原生的依赖管理。有了模块系统，Java 可以根据 module descriptor计算出各个模块间的依赖关系，一旦发现循环依赖，启动就会终止。
同时，由于模块系统不允许不同模块导出相同的包(即 split package，分裂包)，所以在查找包时，Java 可以精准的定位到一个模块，从而获得更好的性能。

第二，精简 JRE。引入模块系统之后，JDK 自身被划分为 94 个模块。通过 Java 9 新增的 jlink 工具，开发者可以根据实际应用场景随意组合这些模块，
去除不需要的模块，生成自定义 JRE，从而有效缩小 JRE 大小。得益于此，JRE 11 的大小仅为 JRE 8 的 53%，从 218.4 MB缩减为 116.3 MB，
JRE 中广为诟病的巨型 jar 文件 rt.jar 也被移除。更小的 JRE 意味着更少的内存占用，这让 Java 对嵌入式应用开发变得更友好。

第三，更好的兼容性。自打 Java 出生以来，就只有 4 种包可见性，这让 Java 对面向对象的三大特征之一封装的支持大打折扣，类库维护者对此叫苦不迭，
只能一遍又一遍的通过各种文档或者奇怪的命名来强调这些或者那些类仅供内部使用，擅自使用后果自负云云。
Java 9 之后，利用 module descriptor 中的 exports 关键词，模块维护者就精准控制哪些类可以对外开放使用，哪些类只能内部使用，
换句话说就是不再依赖文档，而是由编译器来保证。类可见性的细化，除了带来更好的兼容性，也带来了更好的安全性。

第四，提升 Java 语言开发效率。Java 9 之后，Java 像开挂了一般，一改原先一延再延的风格，严格遵循每半年一个大版本的发布策略，
从 2017 年 9 月到 2020 年 3 月，从 Java 9 到 Java 14，三年时间相继发布了 6 个版本，无一延期。这无疑跟模块系统的引入有莫大关系。
前文提到，Java 9 之后，JDK 被拆分为 94 个模块，每个模块有清晰的边界(module descriptor)和独立的单元测试，对于每个 Java 语言的开发者而言，
每个人只需要关注其所负责的模块，开发效率因此大幅提升。这其中的差别，就好比单体应用架构升级到微服务架构一般，版本迭代速度不快也难。

## 新工具或新功能
从Java9到Java11，陆续提供了一些新的工具或功能。

### REPL交互式编程
Java提供了一个新的工具jshell，Java终于可以像python，scala等语言那样，交互式演示语法了。
```
$ /usr/java/jdk-11.0.7+10/bin/jshell 
|  欢迎使用 JShell -- 版本 11.0.7
|  要大致了解该版本, 请键入: /help intro

jshell> var str1 = "hello world";
str1 ==> "hello world"

jshell> System.out.println(str1);
hello world

jshell>
```

### 单文件源代码程序的直接执行
一个单文件源代码，即，单独的java文件，有main方法，且只依赖jdk类库以及自己文件内部定义的类，可以直接用java执行而无需先编译再执行编译后的class文件了。

这对于一些简单的脚本开发是个利好。
```java
java Test.java
```

### 完全支持Linux容器(包括docker)
在Docker容器中运行Java应用程序一直存在一个问题，那就是在容器中运行的JVM程序在设置内存大小和CPU使用率后，会导致应用程序的性能下降。
这是因为Java应用程序没有意识到它正在容器中运行。随着Java10的发布，这个问题总算得以解诀，JVM现在可以识别由容器控制组(cgroups) 设置的约束，
可以在容器中使用内存和CPU约束来直接管理Java应用程序，其中包括:
* 遵守容器中设置的内存限制
* 在容器中设置可用的CPU
* 在容器中设置CPU约束

### 支持Unicode 10
Unicode 10新增了8518个字符，总计达到了136690个字符。包括56个新的emoji表情符号。

JDK11在java.lang下增加了4个类来处理:
* CharacterData00.class
* CharacterData01.class
* CharacterData02.class
* CharacterData0E.class

### 新支持的加密算法
Java实现了RFC7539中指定的ChaCha20和Poly1305两种加密算法，代替RC4。
RFC7748定义的密钥协商方案更高效，更安全，JDK增加了两个新的接口XECPublicKey和XECPrivateKey。

### Low-Overhead Heap Profiling
免费的低耗能飞行记录仪和堆分析仪。

通过JVMTI的SampledObjectAlloc回调提供了一个开销低的heap分析方式提供一个低开销的，为了排错java应用问题，以及JVM问题的数据收集框架。

希望达到的目标如下:
* 提供用于生产和消费数据作为事件的API
* 提供缓存机制和二进制数据格式
* 允许事件配置和事件过滤
* 提供OS,JVM和JDK库的事件

### Flight Recorder
Flight Recorder 源自飞机的黑盒子。 Flight Recorder 以前是商业版的特性，在java11当中开源出来，它可以导出事件到文件中，之后可以用Java Mission Control 来分析。

两种启动方式:
* 可以在应用启动时配置java -XX:StartFlightRecording
* 应用启动之后，使用jcmd来录制，如下代码:

```shell
$ jcmd <pid> JFR.start  # 启动记录仪
$ jcmd <pid> JFR.dump.filename=recording.jfr  # 将记录内容保存到文件里
$ jcmd <pid> JFR.stop  # 停止记录仪
```

## 垃圾回收器
Java11新增了两种垃圾回收器，并改善了Java8开始提供的G1垃圾回收器。

### ZGC
Experimental(实验性质)，生产环境不建议使用

ZGC是Java11最引人瞩目的新特性。

启用方法：-XX:+UnlockExperimentalVMOptions -XX:+UseZGC

说明：ZGC, A Scalable Low-Latency Garbage collector( Experimental) ，一个可伸缩的低延时的垃圾回收器。GC暂停时间不会超过10ms，既能处理几百兆的小堆，也能处理几个T的大堆。和G1相比，应用吞吐能力不会下降超过15%，为未来的GC功能和利用colord指针以及Load barriers 优化奠定了基础。初始只支持64位系统。

ZGC的设计目标是:支持TB级内存容量，暂停时间低(<10ms)，对整个程序吞吐量的影响小于15%。将来还可以扩 展实现机制，以支持不少令人兴奋的功能，例如多层堆(即热对象置于DRAM和冷对象置于NVMe闪存)，或压缩堆。

GC是java主要优势之一。然而，当GC停顿太长，就会开始影响应用的响应时间。消除或者减少GC停顿时长，java将有可能在更广泛的应用场景中成长为一个更有吸引力的平台。此外,现代系统中可用内存不断增长,用户和程序员希望JVM能够以高效的方式充分利用这些内存，并且无需长时间的GC暂停时间。

ZGC是一个并发，基于region,压缩型的垃圾收集器，只有root扫描阶段会STW,因此GC停顿时间不会随着堆的增长和存活对象的增长而变长。

### Epsilon
Experimental(实验性质)，生产环境不建议使用

启用方法：-XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC

说明：开发一个处理内存分配但不实现任何实际内存回收机制的GC,一旦可用堆内存用完,JVM就会退出，如果有System.gc()调用，实际上什么也不会发生(这种场景下和-XX:+DisableExplicitGC效果一样), 因为没有内存回收,这个实现可能会警告用户尝试强制GC是徒劳的。

主要用途如下:

* 性能测试(它可以帮助过滤掉GC引起的性能假象)
* 内存压力测试(例如,知道测试用例应该分配不超过1GB的内存,我们可以使用-Xmx1g -XX:+UseEpsilonGC，如果程序有问题，则程序会崩溃。
* 非常短的JOB任务(对于这种任务，GC是在浪费资源)
* VM接口测试
* Last-drop延迟&吞吐改进

### 更好的G1
对于G1 GC,相比于JDK8,升级到JDK 11即可免费享受到:并行的Full GC,快速的CardTable扫描，自适应的堆占用比例调整(IHOP),在并发标记阶段的类型卸载等等。
这些都是针对G1的不断增强，其中串行FullGC等甚至是曾经被广泛诟病的短板，你会发现GC配置和调优在JDK11中越来越方便。

## 移除与不再推荐使用的类库或功能
Java9到Java11，陆续移除了一些类库或功能。

### 移除了Java EE和CORBA Moudles
在java11中移除了不太使用的JavaEE模块和CORBA技术。

CORBA来自于二十世纪九十年代，Oracle认为，现在用CORBA开发现代Java应用程序已经没有意义了，维护CORBA的成本已经超过了保留它带来的好处。

但是删除CORBA将使得那些依赖于JDK提供部分CORBAAPI的CORBA实现无法运行。目前还没有第三方CORBA版本，也不确定是否会有第三方愿意接手CORBA API的维护工作。

在java11中将java9标记废弃的Java EE及CORBA模块移除掉,具体如下:

xml 相关被移除的：
* java.xml.ws
* java.xml.bind
* java.xml.ws
* java.xml.ws.annotation
* jdk.xml.bind
* jdk.xml.ws  
只剩下java.xml, java.xml.crypto.jdk.xml.dom 这几个模块。

其它被移除的Java EE和CORBA相关类库:
* java.corba
* java.se.ee
* java.activation
* java.transaction(但是java11新增了一个java.transaction.xa模块)

### 其他移除的类库
* com.sun.awt.AWTUtilities
* sun.miss.Unsafe.defineClass
* Thread.destroy() 以及 Thread.stop(Throwable) 方法
* sun.nio.ch.disableSystemWideOverlappingFileLockCheck 属性
* sun.locale.formatasdefault 属性
* jdk snmp 模块
* javafx
* java Mission Control
* Root Certificates: 一些根证书被移除：Baltimore Cybertrust Code Signing CA, SECOM Root Certificate, AOL and Swisscom Root Certificates

其中，使用java.lang.invoke.MethodHandles.Lookup.defineClass来替代移除的sun.miss.Unsafe.defineClass。

### 将Nashorn Javascript标记为不推荐
将Javascript引擎标记为Deprecate，后续版本会移除，有需要的可以考虑使用开源的GraalVM。

### 将Pack200 Tools and API标记为不推荐
java11中将pack200以及unpack200工具以及java.tiljar中的Pack200 API标记为Deprecate。
因为Pack200主要是用来压缩jar包的工具，由于网络下载速度的提升以及java9引入模块化系统之后不再依赖Pack200，因此这个版本将其标记为Deprecate。


