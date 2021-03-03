> ThreadPoolExecutor 线程池，顾名思义，用来存放线程的一个容器

**java自带的线程池工厂**

java自带有一个线程池工厂，工厂里面的线程池分了如下几类：

Executors.newSingleThreadExecutor：创建一个单线程的线程池。这个线程池只有一个线程在工作，也就是相当于单线程串行执行所有任务。如果这个唯一的线程因为异常结束，那么会有一个新的线程来替代它。此线程池保证所有任务的执行顺序按照任务的提交顺序执行。

Executors.newFixedThreadPool：创建固定大小的线程池。每次提交一个任务就创建一个线程，直到线程达到线程池的最大大小。线程池的大小一旦达到最大值就会保持不变，如果某个线程因为执行异常而结束，那么线程池会补充一个新线程。

Executors.newCachedThreadPool：创建一个可缓存的线程池。如果线程池的大小超过了处理任务所需要的线程，那么就会回收部分空闲（60秒不执行任务）的线程，当任务数增加时，此线程池又可以智能的添加新线程来处理任务。此线程池不会对线程池大小做限制，线程池大小完全依赖于操作系统（或者说JVM）能够创建的最大线程大小。

Executors.newScheduledThreadPool：创建一个大小无限的线程池。此线程池支持定时以及周期性执行任务的需求

Executors.newWorkStealingPool：这个是jdk1.8新增的线程池，适合处理比较耗时的工作任务。

**实际使用的线程池**

都不用。  
先看一眼线程池工作流程：  

>如果正在运行的线程数量小于corePoolSize，那么马上创建线程运行这个任务；  
 如果正在运行的线程数量大于或等于corePoolSize，那么将这个任务放入队列；  
 如果这时候队列满了且正在运行的线程数量还小于maximumPoolSize，那么还是要创建非核心线程立刻运行这个任务；  
 如果队列满了且正在运行的线程数量大于或等于maximumPoolSize，那么线程池会启动饱和拒绝策略来执行

再看看阿里规约

>【强制】线程池不允许使用 Executors 去创建,而是通过 ThreadPoolExecutor 的方式，
> 这样的处理方式可以让写的同学更加明确线程池的运行规则，规避资源耗尽的风险。  
> 说明：Executors 返回的线程池对象的弊端如下：
> 1) FixedThreadPool 和 SingleThreadPool :
> 允许的请求队列长度为 Integer.MAX_VALUE，可能会堆积大量的请求，从而导致 OOM 。
> 2) CachedThreadPool 和 ScheduledThreadPool :允许的创建线程数量为 Integer.MAX_VALUE ,可能会创建大量的线程，从而导致 OOM 。

这四个线程池有两个不限制队列长度，有两个不限制线程数，这在极高并发下是非常危险的，比如阿里的双十二，绝对秒炸。
而且，没有合适的拒绝策略，虽然这四个要么不限制队列长，要么不限制线程数的线程池看起来都用不到，所以拒绝策略就是抛个异常就没了。

```markdown
public ThreadPoolExecutor(int corePoolSize,
                              int maximumPoolSize,
                              long keepAliveTime,
                              TimeUnit unit,
                              BlockingQueue<Runnable> workQueue,
                              ThreadFactory threadFactory,
                              RejectedExecutionHandler handler) {
        if (corePoolSize < 0 ||
            maximumPoolSize <= 0 ||
            maximumPoolSize < corePoolSize ||
            keepAliveTime < 0)
            throw new IllegalArgumentException();
        if (workQueue == null || threadFactory == null || handler == null)
            throw new NullPointerException();
        this.corePoolSize = corePoolSize;
        this.maximumPoolSize = maximumPoolSize;
        this.workQueue = workQueue;
        this.keepAliveTime = unit.toNanos(keepAliveTime);
        this.threadFactory = threadFactory;
        this.handler = handler;
    }
```

其中：
1. corePoolSize：表示该线程池最小的工作线程数。默认情况下，当需要使用时创建线程，也可以调用 prestartAllCoreThreads() 方法进行预创建所有的核心线程。
2. maximumPoolSize：表示该线程池最大的线程数量，理论上将其设置为无限大，就会创建无限多的线程，当然，创建线程的数量最终由系统资源也就是操作系统决定。
3. keepAliveTime：表示空闲线程的超时时间，(单位为纳秒）。但在构造函数中，单位与unit 参数配合使用，最终转换为纳秒。
4. unit：表示空闲线程超时的时间单位，可选值有：java.util.concurrent.TimeUnit中的值，SECONDS(秒)，MINUTES(分)，HOURS(小时)，DAYS(天) 等。
5. workQueue ：表示工作队列(其实是一个runnable队列，在线程池中定义为Worker)，其基类为：java.util.concurrent.BlockingQueue。
6. threadFactory：线程工厂，通常用于创建线程，以及命令规则。默认为： Executors.defaultThreadFactory()。
7. handler 表示处理策略，当workQueue队列满时，以及创建线程错误时的处理策略。其基类为 java.util.concurrent.RejectedExecutionHandler。默认为：AbortPolicy 策略。