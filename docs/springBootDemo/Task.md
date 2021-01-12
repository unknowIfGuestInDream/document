>task是Spring 内置的一个定时器，他可以不想Quartz那样麻烦的配置；Scheduled task有三种使用的方式，一种是在注解上直接使用task定时任务，第二种是可以进行更改定时任务的时间，第三种是可以进行手动启动定时任务和停止定时任务以及更改定时任务的时间；

启动类新增 @EnableScheduling注解来支持Task;

## 在注解上直接使用task定时任务 :id=task1

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

!> 使用Scheduled Task的弊端就是不适用于分布式集群的操作，Scheduled Task是一种轻量级的任务定时调度器，相比于Quartz,减少了很多的配置信息，但是Scheduled Task不适用于服务器集群，引文在服务器集群下会出现任务被多次调度执行的情况，因为集群的节点之间是不会共享任务信息的，每个节点的定时任务都会定时执行

?> 由于Task是单线程的，所以实战中可以配置定时任务线程池或者通过spring的注解@Async异步调用

## 可更改的定时任务 :id=task2

```java

import java.util.Date;
 
import org.apache.log4j.Logger;
import org.springframework.scheduling.Trigger;
import org.springframework.scheduling.TriggerContext;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.SchedulingConfigurer;
import org.springframework.scheduling.config.ScheduledTaskRegistrar;
import org.springframework.scheduling.support.CronTrigger;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
 
@RestController
@EnableScheduling
@RequestMapping("/task")
public class TaskController implements SchedulingConfigurer {
 
    private Logger logger = Logger.getLogger(TaskController.class);
 
    /**
     * 定时任务的定时器表达式： 秒 分 时 日期 月 星期
     * 注意：有的地方说定时正则表达式可以有year，即7个元素，但是，在spring-boot里面，只能是6个元素，没有年。
     */
    private String cronExpression = "1/5 * * * * *";
 
    /**
     * 通过REST API请求对参数进行修改，定时规则进行调整
     * @param exp
     * @return
     */
    @RequestMapping("/change")
    public String change(@RequestParam("exp") String exp) {
        cronExpression = exp;
        logger.info("new cron expression: " + exp);
        return cronExpression;
    }
 
    /**
     * 定时任务要执行的方法
     * @return
     */
    private Runnable getTask() {
        Runnable task = new Runnable() {
            @Override
            public void run() {
            	logger.info("==定时任务==开始: " + new Date());
            	
            	//业务处理，忽视所有异常
                try {
                	//do something
                	
				} catch (Exception e) {
					e.printStackTrace();
				}
                
                logger.info("==定时任务==结束: " + new Date());
            }
        };
        return task;
    }
 
    /**
     * 调度实现的时间控制
     * @param scheduledTaskRegistrar
     */
    @Override
    public void configureTasks(ScheduledTaskRegistrar scheduledTaskRegistrar) {
        Trigger trigger=new Trigger() {
            @Override
            public Date nextExecutionTime(TriggerContext triggerContext) {
                CronTrigger cronTrigger=new CronTrigger(cronExpression);
                return cronTrigger.nextExecutionTime(triggerContext);
            }
        };
        scheduledTaskRegistrar.addTriggerTask(getTask(), trigger);
    }
}
```

!> 这种方式控制不强，没有持久化，不随时启动停止