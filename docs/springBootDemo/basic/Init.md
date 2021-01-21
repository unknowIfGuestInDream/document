> 在我们用springboot搭建项目的时候，有时候会碰到在项目启动时初始化一些操作的需求，针对这种需求springboot(spring)为我们提供了以下几种方案供我们选择: 

- ApplicationRunner与CommandLineRunner接口 
- Spring Bean初始化的InitializingBean,init-method和PostConstruct 
- Spring的事件机制

https://blog.csdn.net/pjmike233/article/details/81908540
http://www.360doc.com/content/20/0308/11/13328254_897664573.shtml

## ApplicationRunner与CommandLineRunner

https://www.jianshu.com/p/5d4ffe267596
https://blog.csdn.net/weixin_38362455/article/details/83023025
https://blog.csdn.net/moneyshi/article/details/108864172
https://www.jianshu.com/p/01e08aef73c9

## PostConstruct注解

> 被@PostConstruct修饰的方法会在服务器加载Servlet的时候运行，并且只会被服务器调用一次，类似于Serclet的inti()方法。被@PostConstruct修饰的方法会在构造函数之后，init()方法之前运行。

https://blog.csdn.net/weixin_39417722/article/details/106339756  
https://blog.csdn.net/lxh_worldpeace/article/details/106789546

## 事件

ApplicationStartedEvent：spring boot启动开始时执行的事件  
ApplicationEnvironmentPreparedEvent：spring boot 对应Enviroment已经准备完毕，但此时上下文context还没有创建。  
ApplicationPreparedEvent:spring boot上下文context创建完成，但此时spring中的bean是没有完全加载完成的。  
ApplicationReadyEvent：springboot加载完成时候执行的事件。  
ApplicationFailedEvent:spring boot启动异常时执行事件 

https://www.cnblogs.com/exmyth/p/7750770.html