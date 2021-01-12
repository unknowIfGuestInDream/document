#springBoot-Task定时任务

>task是Spring 内置的一个定时器，他可以不想Quartz那样麻烦的配置；Scheduled task有三种使用的方式，一种是在注解上直接使用task定时任务，第二种是可以进行更改定时任务的时间，第三种是可以进行手动启动定时任务和停止定时任务以及更改定时任务的时间；

启动类新增 @EnableScheduling注解来支持Task;

### 在注解上直接使用task定时任务 :id=task1

测试用例:
```java
@Slf4j
@Component
@Async
public class ScheduledService {
    //https://cron.qqe2.com/ cron生成网址

    /*
    fixedRate：定义一个按一定频率执行的定时任务
    上一次开始执行时间点之后多长时间再执行

    fixedRateString fixedRate 意思相同，只是使用字符串的形式。唯一不同的是支持占位符。

    fixedDelay：定义一个按一定频率执行的定时任务，与上面不同的是，改属性可以配合initialDelay，
    上一次执行完毕时间点之后多长时间再执行

    fixedDelayString 与 3. fixedDelay 意思相同，只是使用字符串的形式。唯一不同的是支持占位符。如：
    @Scheduled(fixedDelayString = "5000") //上一次执行完毕时间点之后5秒再执行
    占位符的使用(配置文件中有配置：time.fixedDelay=5000)：
     @Scheduled(fixedDelayString = "${time.fixedDelay}")

     initialDelay第一次延迟多长时间后再执行 如：
     @Scheduled(initialDelay=1000, fixedRate=5000) //第一次延迟1秒后执行，之后按fixedRate的规则每5秒执行一次
      initialDelayString 与initialDelay 意思相同，只是使用字符串的形式。唯一不同的是支持占位符。
     */

    //cron：通过表达式来配置任务执行时间
    @Scheduled(cron = "0/5 * * * * *")
    public void scheduled() {
        log.info("=====>>>>>使用cron  {}", System.currentTimeMillis());
    }

    @Scheduled(fixedRate = 5000)
    public void scheduled1() {
        log.info("=====>>>>>使用fixedRate{}", System.currentTimeMillis());
    }

    @Scheduled(fixedDelay = 5000)
    public void scheduled2() {
        log.info("=====>>>>>fixedDelay{}", System.currentTimeMillis());
    }

}
```

!>使用Scheduled Task的弊端就是不适用于分布式集群的操作，Scheduled Task是一种轻量级的任务定时调度器，相比于Quartz,减少了很多的配置信息，但是Scheduled Task不适用于服务器集群，引文在服务器集群下会出现任务被多次调度执行的情况，因为集群的节点之间是不会共享任务信息的，每个节点的定时任务都会定时执行

由于Task是单线程的，所以实战中可以配置定时任务线程池或者通过spring的注解@Async异步调用