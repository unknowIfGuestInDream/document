> 在我们用springboot搭建项目的时候，有时候会碰到在项目启动时初始化一些操作的需求，针对这种需求springboot(spring)为我们提供了以下几种方案供我们选择: 

- ApplicationRunner与CommandLineRunner接口 
- Spring Bean初始化的InitializingBean,init-method和PostConstruct 
- Spring的事件机制

https://blog.csdn.net/pjmike233/article/details/81908540
http://www.360doc.com/content/20/0308/11/13328254_897664573.shtml

## ApplicationRunner与CommandLineRunner

## PostConstruct注解

> 被@PostConstruct修饰的方法会在服务器加载Servlet的时候运行，并且只会被服务器调用一次，类似于Serclet的inti()方法。被@PostConstruct修饰的方法会在构造函数之后，init()方法之前运行。