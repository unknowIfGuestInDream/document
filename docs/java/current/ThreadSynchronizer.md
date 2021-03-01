## CountDownLatch计数器

> CountDownLatch

```java
@SpringBootTest
@Slf4j
public class countDownLatchTest {
    @Autowired
    private RabbitTemplate rabbitTemplate;
    @Autowired
    private AsyncCountDown asyncCountDown;

    private static int mobile = 0;

    @Test
    public void countDownLatch() {
        CountDownLatch countDownLatch = new CountDownLatch(1);
        for (int i = 0; i < 2000; i++) {
            new Thread(new RunThread(countDownLatch)).start();
        }
        log.info("线程准备完毕");
        //启动多个线程
        countDownLatch.countDown();
    }

    private class RunThread implements Runnable {
        private final CountDownLatch startLatch;

        public RunThread(CountDownLatch startLatch) {
            this.startLatch = startLatch;
        }

        @Override
        public void run() {
            //等待
            try {
                startLatch.await();
                mobile += 1;
                LogDocument logDocument = new LogDocument();
                logDocument.setId(IdUtil.objectId());
                logDocument.setOperateType("测试CountDownLatch");
                logDocument.setBrowser("Firefox");
                logDocument.setVersion("64.0");
                logDocument.setOs("WINDOWS 7");
                logDocument.setIpName("TANGLIANG");
                logDocument.setIp("127.0.0.1");
                logDocument.setUrl("/hello");
                logDocument.setParams("{" + mobile + "}");
                logDocument.setCreateTime(DateUtils.parseDateToStr(DateUtils.YYYY_MM_DD_HH_MM_SS, new Date()));
                rabbitTemplate.convertAndSend("logToMongo", JSON.toJSONString(logDocument));
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        }
    }

    //和异步结合使用
    @Test
    public void async() throws InterruptedException {
        log.info("=====开始了=====");
        CountDownLatch countDownLatch = new CountDownLatch(2);
        asyncCountDown.dealNoReturnTask(countDownLatch);
        asyncCountDown.dealHaveReturnTask(6, countDownLatch);
        log.info("=====方法调用完成=====");
        countDownLatch.await();
        log.info("=====方法结束=====");
    }
}
```

## CycleBarrier回环屏障

> CycleBarrier

```java
@SpringBootTest
public class CyclicBarrierTest {
    //https://www.cnblogs.com/princessd8251/articles/4005578.html
    /*
    它允许一组线程互相等待，直到到达某个公共屏障点 (common barrier point)。
    在涉及一组固定大小的线程的程序中，这些线程必须不时地互相等待，
    此时 CyclicBarrier 很有用。因为该 barrier 在释放等待线程后可以重用，所以称它为循环 的 barrier。
    通俗点讲就是：让一组线程到达一个屏障时被阻塞，直到最后一个线程到达屏障时，
    屏障才会开门，所有被屏障拦截的线程才会继续干活。

    应用场景
    在某种需求中，比如一个大型的任务，常常需要分配好多子任务去执行，只有当所有子任务都执行完成时候，
    才能执行主任务，这时候，就可以选择CyclicBarrier了。
    CyclicBarrier试用与多线程结果合并的操作，用于多线程计算数据，最后合并计算结果的应用场景。
    比如我们需要统计多个Excel中的数据，然后等到一个总结果。
    我们可以通过多线程处理每一个Excel，执行完成后得到相应的结果，
    最后通过barrierAction来计算这些线程的计算结果，得到所有Excel的总和。
     */

    /*和CountDownLatch区别
     *
     * CountDownLatch的计数器只能使用一次，而CyclicBarrier的计数器可以使用reset()方法重置，
     * 可以使用多次，所以CyclicBarrier能够处理更为复杂的场景；
     * <p>
     * CyclicBarrier还提供了一些其他有用的方法，
     * 比如getNumberWaiting()方法可以获得CyclicBarrier阻塞的线程数量，
     * isBroken()方法用来了解阻塞的线程是否被中断；
     * <p>
     * CountDownLatch允许一个或多个线程等待一组事件的产生，
     * 而CyclicBarrier用于等待其他线程运行到栅栏位置。
     */

    //开会只有等所有的人到齐了才会开会
    @Test
    public void test1() {
        CyclicBarrier cyclicBarrier;

        cyclicBarrier = new CyclicBarrier(5, new Runnable() {
            @Override
            public void run() {
                System.out.println("人到齐了，开会吧....");
            }
        });

        for (int i = 0; i < 5; i++) {
            new Thread() {
                public void run() {
                    System.out.println(Thread.currentThread().getName() + "到了");
                    //等待
                    try {
                        cyclicBarrier.await();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }.start();
        }

    }

    //5个线程相互等待至都阻塞之后，所有线程一起执行，它也可以用于最大并发测试，或者死锁检测
    @Test
    public void test2() throws InterruptedException {
        CyclicBarrier cyclicBarrier = new CyclicBarrier(5, () -> {
            System.out.println(Thread.currentThread().getName() + " 等待线程达到临界点5，5个线程都执行");
        });
        Thread[] threads = new Thread[5];
        for (int index = 0; index < 5; index++) {
            threads[index] = new Thread(() -> {
                try {
                    System.out.println(Thread.currentThread().getName() + " parties:" + cyclicBarrier.getParties());
                    System.out.println(Thread.currentThread().getName() + " wait threads:" + (cyclicBarrier.getNumberWaiting() + 1) + "\n");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            });
            threads[index].start();
            TimeUnit.SECONDS.sleep(1);
        }
        for (Thread thread : threads) {
            thread.join();
        }
        System.out.println(Thread.currentThread().getName() + " isBroken:" + cyclicBarrier.isBroken());
    }

    //将上面的cyclicBarrier.await()改为cyclicBarrier.await(1, TimeUnit.SECONDS)，
    // 代码如下。我们会发现一个Timeout异常，其他都是BrokenBarrier异常。这时CyclicBarrier已经被破坏，调用reset才能重置至初始化状态
    @Test
    public void test3() throws InterruptedException {
        CyclicBarrier cyclicBarrier = new CyclicBarrier(5, () -> {
            System.out.println(Thread.currentThread().getName() + " 等待线程达到临界点5，5个线程都执行");
        });
        Thread[] threads = new Thread[5];
        for (int index = 0; index < 5; index++) {
            threads[index] = new Thread(() -> {
                try {
                    System.out.println(Thread.currentThread().getName() + " parties:" + cyclicBarrier.getParties());
                    System.out.println(Thread.currentThread().getName() + " wait threads:" + (cyclicBarrier.getNumberWaiting() + 1) + "\n");
                    cyclicBarrier.await(1, TimeUnit.SECONDS);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                    System.out.println(Thread.currentThread().getName() + " InterruptedException");
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                    System.out.println(Thread.currentThread().getName() + " BrokenBarrierException");
                } catch (TimeoutException e) {
                    e.printStackTrace();
                    System.out.println(Thread.currentThread().getName() + " TimeoutException");
                }
            });
            threads[index].start();
            TimeUnit.SECONDS.sleep(1);
        }
        for (Thread thread : threads) {
            thread.join();
        }
        if (cyclicBarrier.isBroken()) {
            System.out.println(Thread.currentThread().getName() + " CyclicBarrier被破坏了重置");
            cyclicBarrier.reset();
        }
        for (int index = 0; index < 10; index++) {
            new Thread(() -> {
                try {
                    System.out.println(Thread.currentThread().getName() + " parties:" + cyclicBarrier.getParties());
                    System.out.println(Thread.currentThread().getName() + " wait threads:" + (cyclicBarrier.getNumberWaiting() + 1) + "\n");
                    cyclicBarrier.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (BrokenBarrierException e) {
                    e.printStackTrace();
                }
            }).start();
            TimeUnit.SECONDS.sleep(1);
        }
    }
}
```

## Semaphore信号量

> Semaphore

```java
@SpringBootTest
public class SemaphoreTest {
    /*

    Semaphore 是 synchronized 的加强版，作用是控制线程的并发数量。
    就这一点而言，单纯的synchronized 关键字是实现不了的。
    常用于限制可以访问某些资源的线程数量，例如通过 Semaphore 限流。
     */

    @Test
    public void test1() {
        ExecutorService executorService = Executors.newCachedThreadPool();

        //信号量，只允许 3个线程同时访问
        Semaphore semaphore = new Semaphore(3);

        for (int i = 0; i < 10; i++) {
            final long num = i;
            executorService.submit(new Runnable() {
                @Override
                public void run() {
                    try {
                        //获取许可
                        semaphore.acquire();
                        //执行
                        System.out.println("Accessing: " + num);
                        Thread.sleep(new Random().nextInt(5000)); // 模拟随机执行时长
                        //释放
                        semaphore.release();
                        System.out.println("Release..." + num);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            });
        }

        executorService.shutdown();
    }
}
```