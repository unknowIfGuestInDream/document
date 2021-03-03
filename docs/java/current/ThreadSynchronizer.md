## CountDownLatch计数器

> CountDownLatch是一个同步工具类，允许一个或多个线程一直等待，直到其他线程运行完成后再执行。

**使用场景**
1. 让多个线程等待
2. 和让单个线程等待。

**常用方法说明**
* CountDownLatch(int count); 构造方法，创建一个值为count 的计数器。
* await();阻塞当前线程，将当前线程加入阻塞队列。​
* await(long timeout, TimeUnit unit);在timeout的时间之内阻塞当前线程,时间一过则当前线程可以执行，​
* countDown();对计数器进行递减1操作，当计数器递减至0时，当前线程会去唤醒阻塞队列里的所有线程。

**场景1 让多个线程等待：模拟并发，让并发线程一起执行**

为了模拟高并发，让一组线程在指定时刻(秒杀时间)执行抢购，这些线程在准备就绪后，进行等待(CountDownLatch.await())，
直到秒杀时刻的到来，然后一拥而上；这也是本地测试接口并发的一个简易实现。

在这个场景中，CountDownLatch充当的是一个发令枪的角色；
就像田径赛跑时，运动员会在起跑线做准备动作，等到发令枪一声响，运动员就会奋力奔跑。和上面的秒杀场景类似，代码实现如下：

```markdown
CountDownLatch countDownLatch = new CountDownLatch(1);
for (int i = 0; i < 5; i++) {
    new Thread(() -> {
        try {
            //准备完毕……运动员都阻塞在这，等待号令
            countDownLatch.await();
            String parter = "【" + Thread.currentThread().getName() + "】";
            System.out.println(parter + "开始执行……");
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }).start();
}

Thread.sleep(2000);// 裁判准备发令
countDownLatch.countDown();// 发令枪：执行发令
```

**场景2 让单个线程等待：多个线程(任务)完成后，进行汇总合并**

很多时候，我们的并发任务，存在前后依赖关系；比如数据详情页需要同时调用多个接口获取数据，并发请求获取到数据后、
需要进行结果合并；或者多个数据操作完成后，需要数据check；这其实都是：在多个线程(任务)完成后，进行汇总合并的场景。

```markdown
CountDownLatch countDownLatch = new CountDownLatch(5);
for (int i = 0; i < 5; i++) {
    final int index = i;
    new Thread(() -> {
        try {
            Thread.sleep(1000 + ThreadLocalRandom.current().nextInt(1000));
            System.out.println("finish" + index + Thread.currentThread().getName());
            countDownLatch.countDown();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }).start();
}

countDownLatch.await();// 主线程在阻塞，当计数器==0，就唤醒主线程往下执行。
System.out.println("主线程:在所有任务运行完成后，进行结果汇总");
```

**工作原理**

CountDownLatch是通过一个计数器来实现的，计数器的初始值为线程的数量；
调用await()方法的线程会被阻塞，直到计数器 减到 0 的时候，才能继续往下执行；

调用了await()进行阻塞等待的线程，它们阻塞在Latch门闩/栅栏上；只有当条件满足的时候（countDown() N次，将计数减为0），
它们才能同时通过这个栅栏；以此能够实现，让所有的线程站在一个起跑线上。

countDown()方法则是将计数器减1；

在CountDownLatch的构造函数中，指定的线程数量，只能指定一次；由于CountDownLatch采用的是减计数，因此当计数减为0时，
计数器不能被重置。这是和CyclicBarrier的一个重要区别。

CountDownLatch 的源码在JUC并发工具中，也相对算是简单的；  
底层基于 AbstractQueuedSynchronizer 实现，CountDownLatch 构造函数中指定的count直接赋给AQS的state；
每次countDown()则都是release(1)减1，最后减到0时unpark阻塞线程；这一步是由最后一个执行countdown方法的线程执行的。  
而调用await()方法时，当前线程就会判断state属性是否为0，如果为0，则继续往下执行，如果不为0，则使当前线程进入等待状态，
直到某个线程将state属性置为0，其就会唤醒在await()方法中等待的线程。

**CountDownLatch实现原理**

**1、创建计数器**  
当我们调用CountDownLatch countDownLatch=new CountDownLatch(4) 时候，此时会创建一个AQS的同步队列，
并把创建CountDownLatch 传进来的计数器赋值给AQS队列的 state，所以state的值也代表CountDownLatch所剩余的计数次数；

```markdown
    public CountDownLatch(int count) {
        if (count < 0) throw new IllegalArgumentException("count < 0");
        this.sync = new Sync(count);//创建同步队列，并设置初始计数器值
    }
```

**2、阻塞线程**  
当我们调用countDownLatch.wait()的时候，会创建一个节点，加入到AQS阻塞队列，并同时把当前线程挂起。

```markdown
    public void await() throws InterruptedException {
        sync.acquireSharedInterruptibly(1);
    }
```

判断计数器是技术完毕，未完毕则把当前线程加入阻塞队列

```markdown
    public final void acquireSharedInterruptibly(int arg)
            throws InterruptedException {
        if (Thread.interrupted())
            throw new InterruptedException();
        //锁重入次数大于0 则新建节点加入阻塞队列，挂起当前线程
        if (tryAcquireShared(arg) < 0)
            doAcquireSharedInterruptibly(arg);
    }
```

构建阻塞队列的双向链表，挂起当前线程

```markdown
private void doAcquireSharedInterruptibly(int arg)
        throws InterruptedException {
        //新建节点加入阻塞队列
        final Node node = addWaiter(Node.SHARED);
        boolean failed = true;
        try {
            for (;;) {
                //获得当前节点pre节点
                final Node p = node.predecessor();
                if (p == head) {
                    int r = tryAcquireShared(arg);//返回锁的state
                    if (r >= 0) {
                        setHeadAndPropagate(node, r);
                        p.next = null; // help GC
                        failed = false;
                        return;
                    }
                }
                //重组双向链表，清空无效节点，挂起当前线程
                if (shouldParkAfterFailedAcquire(p, node) &&
                    parkAndCheckInterrupt())
                    throw new InterruptedException();
            }
        } finally {
            if (failed)
                cancelAcquire(node);
        }
    }
```

**3、计数器递减**  
当我们调用countDownLatch.down()方法的时候，会对计数器进行减1操作，AQS内部是通过释放锁的方式，对state进行减1操作，
当state=0的时候证明计数器已经递减完毕，此时会将AQS阻塞队列里的节点线程全部唤醒。

```markdown
    public void countDown() {
        //递减锁重入次数，当state=0时唤醒所有阻塞线程
        sync.releaseShared(1);
    }
```

```markdown
public final boolean releaseShared(int arg) {
        //递减锁的重入次数
        if (tryReleaseShared(arg)) {
            doReleaseShared();//唤醒队列所有阻塞的节点
            return true;
        }
        return false;
    }
 private void doReleaseShared() {
        //唤醒所有阻塞队列里面的线程
        for (;;) {
            Node h = head;
            if (h != null && h != tail) {
                int ws = h.waitStatus;
                if (ws == Node.SIGNAL) {//节点是否在等待唤醒状态
                    if (!compareAndSetWaitStatus(h, Node.SIGNAL, 0))//修改状态为初始
                        continue;
                    unparkSuccessor(h);//成功则唤醒线程
                }
                else if (ws == 0 &&
                         !compareAndSetWaitStatus(h, 0, Node.PROPAGATE))
                    continue;                // loop on failed CAS
            }
            if (h == head)                   // loop if head changed
                break;
        }
    }
```

**CountDownLatch与Thread.join**

CountDownLatch的作用就是允许一个或多个线程等待其他线程完成操作，看起来有点类似join() 方法，
但其提供了比 join() 更加灵活的API。  
CountDownLatch可以手动控制在n个线程里调用n次countDown()方法使计数器进行减一操作，
也可以在一个线程里调用n次执行减一操作。  
而 join() 的实现原理是不停检查join线程是否存活，如果 join 线程存活则让当前线程永远等待。
所以两者之间相对来说还是CountDownLatch使用起来较为灵活。

**CountDownLatch与CyclicBarrier**

CountDownLatch和CyclicBarrier都能够实现线程之间的等待，只不过它们侧重点不同：

* CountDownLatch一般用于一个或多个线程，等待其他线程执行完任务后，再才执行
* CyclicBarrier一般用于一组线程互相等待至某个状态，然后这一组线程再同时执行
另外，CountDownLatch是减计数，计数减为0后不能重用；而CyclicBarrier是加计数，可置0后复用。

## CycleBarrier回环屏障

> CycleBarrier允许一组线程全部等待彼此达到共同屏障点的同步辅助。循环阻塞在涉及固定大小的线程方的程序中很有用，
> 这些线程必须偶尔等待彼此。屏障被称为循环 ，因为它可以在等待的线程被释放之后重新使用。

通俗点讲就是：让一组线程到达一个屏障时被阻塞，直到最后一个线程到达屏障时，屏障才会开门，所有被屏障拦截的线程才会继续干活。

**应用场景**

在某种需求中，比如一个大型的任务，常常需要分配好多子任务去执行，只有当所有子任务都执行完成时候，
才能执行主任务，这时候，就可以选择CyclicBarrier了。  
CyclicBarrier适用与多线程结果合并的操作，用于多线程计算数据，最后合并计算结果的应用场景。  
比如我们需要统计多个Excel中的数据，然后等到一个总结果。我们可以通过多线程处理每一个Excel，执行完成后得到相应的结果，
最后通过barrierAction来计算这些线程的计算结果，得到所有Excel的总和。

```java
@SpringBootTest
public class CyclicBarrierTest {

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

> Semaphore一个计数信号量。在概念上，信号量维持一组许可证。如果有必要，每个acquire()都会阻塞，
> 直到许可证可用，然后才能使用它。每个release()添加许可证，潜在地释放阻塞获取方。
> 但是，没有使用实际的许可证对象; Semaphore只保留可用数量的计数，并相应地执行。
> 信号量通常用于限制线程数，而不是访问某些（物理或逻辑）资源
 
Semaphore 是 synchronized 的加强版，作用是控制线程的并发数量。就这一点而言，单纯的synchronized 关键字是实现不了的。

**使用场景**

用于那些资源有明确访问数量限制的场景，常用于限流 。  
比如：数据库连接池，同时进行连接的线程有数量限制，连接不能超过一定的数量，当连接达到了限制数量后，
后面的线程只能排队等前面的线程释放了数据库连接才能获得数据库连接。  
比如：停车场场景，车位数量有限，同时只能容纳多少台车，车位满了之后只有等里面的车离开停车场外面的车才可以进入。

**常用方法说明**

* acquire()
获取一个令牌，在获取到令牌、或者被其他线程调用中断之前线程一直处于阻塞状态。
* acquire(int permits)
获取一个令牌，在获取到令牌、或者被其他线程调用中断、或超时之前线程一直处于阻塞状态。    
* acquireUninterruptibly() 
获取一个令牌，在获取到令牌之前线程一直处于阻塞状态（忽略中断）。    
* tryAcquire()
尝试获得令牌，返回获取令牌成功或失败，不阻塞线程。​
* tryAcquire(long timeout, TimeUnit unit)
尝试获得令牌，在超时时间内循环尝试获取，直到尝试获取成功或超时返回，不阻塞线程。​
* release()
释放一个令牌，唤醒一个获取令牌不成功的阻塞线程。​
* hasQueuedThreads()
等待队列里是否还存在等待线程。​
* getQueueLength()
获取等待队列里阻塞的线程数。
​
drainPermits()
清空令牌把可用令牌数置为0，返回清空令牌的数量。
​
availablePermits()
返回可用的令牌数量。

**用semaphore 实现停车场提示牌功能**

每个停车场入口都有一个提示牌，上面显示着停车场的剩余车位还有多少，当剩余车位为0时，不允许车辆进入停车场，
直到停车场里面有车离开停车场，这时提示牌上会显示新的剩余车位数。

业务场景
1. 停车场容纳总停车量10。
2. 当一辆车进入停车场后，显示牌的剩余车位数响应的减1.
3. 每有一辆车驶出停车场后，显示牌的剩余车位数响应的加1。
4. 停车场剩余车位不足时，车辆只能在外面等待。

```java
public class TestCar {
​
    //停车场同时容纳的车辆10
    private  static  Semaphore semaphore=new Semaphore(10);
​
    public static void main(String[] args) {
​
        //模拟100辆车进入停车场
        for(int i=0;i<100;i++){
​
            Thread thread=new Thread(new Runnable() {
                public void run() {
                    try {
                        System.out.println("===="+Thread.currentThread().getName()+"来到停车场");
                        if(semaphore.availablePermits()==0){
                            System.out.println("车位不足，请耐心等待");
                        }
                        semaphore.acquire();//获取令牌尝试进入停车场
                        System.out.println(Thread.currentThread().getName()+"成功进入停车场");
                        Thread.sleep(new Random().nextInt(10000));//模拟车辆在停车场停留的时间
                        System.out.println(Thread.currentThread().getName()+"驶出停车场");
                        semaphore.release();//释放令牌，腾出停车场车位
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            },i+"号车");
​
            thread.start();
        }
    }
}
```

**Semaphore实现原理**

**1、Semaphore初始化**  
`Semaphore semaphore=new Semaphore(2);`

1. 当调用new Semaphore(2) 方法时，默认会创建一个非公平的锁的同步阻塞队列。
2. 把初始令牌数量赋值给同步队列的state状态，state的值就代表当前所剩余的令牌数量。

**2、获取令牌**  
`semaphore.acquire();`

1. 当前线程会尝试去同步队列获取一个令牌，获取令牌的过程也就是使用原子的操作去修改同步队列的state,
获取一个令牌则修改为state=state-1。
2. 当计算出来的state<0，则代表令牌数量不足，此时会创建一个Node节点加入阻塞队列，挂起当前线程。
3. 当计算出来的state>=0，则代表获取令牌成功。

源码

```markdown
    /**
     *  获取1个令牌
     */
    public void acquire() throws InterruptedException {
        sync.acquireSharedInterruptibly(1);
    }
```

```markdown
    /**
     * 共享模式下获取令牌，获取成功则返回，失败则加入阻塞队列，挂起线程
     * @param arg
     * @throws InterruptedException
     */
    public final void acquireSharedInterruptibly(int arg)
            throws InterruptedException {
        if (Thread.interrupted())
            throw new InterruptedException();
        //尝试获取令牌，arg为获取令牌个数，当可用令牌数减当前令牌数结果小于0,则创建一个节点加入阻塞队列，挂起当前线程。
        if (tryAcquireShared(arg) < 0)
            doAcquireSharedInterruptibly(arg);
    }
```

```markdown
    /**
     * 1、创建节点，加入阻塞队列，
     * 2、重双向链表的head，tail节点关系，清空无效节点
     * 3、挂起当前节点线程
     * @param arg
     * @throws InterruptedException
     */
    private void doAcquireSharedInterruptibly(int arg)
        throws InterruptedException {
        //创建节点加入阻塞队列
        final Node node = addWaiter(Node.SHARED);
        boolean failed = true;
        try {
            for (;;) {
                //获得当前节点pre节点
                final Node p = node.predecessor();
                if (p == head) {
                    int r = tryAcquireShared(arg);//返回锁的state
                    if (r >= 0) {
                        setHeadAndPropagate(node, r);
                        p.next = null; // help GC
                        failed = false;
                        return;
                    }
                }
                //重组双向链表，清空无效节点，挂起当前线程
                if (shouldParkAfterFailedAcquire(p, node) &&
                    parkAndCheckInterrupt())
                    throw new InterruptedException();
            }
        } finally {
            if (failed)
                cancelAcquire(node);
        }
    }
```

**3、释放令牌**  
`semaphore.release();`

当调用semaphore.release() 方法时
1. 线程会尝试释放一个令牌，释放令牌的过程也就是把同步队列的state修改为state=state+1的过程
2. 释放令牌成功之后，同时会唤醒同步队列的所有阻塞节共享节点线程
3. 被唤醒的节点会重新尝试去修改state=state-1 的操作，如果state>=0则获取令牌成功，否则重新进入阻塞队列，挂起线程。

源码

```markdown
    /**
     * 释放令牌
     */
    public void release() {
        sync.releaseShared(1);
    }
```

```markdown
    /**
     *释放共享锁，同时唤醒所有阻塞队列共享节点线程
     * @param arg
     * @return
     */
    public final boolean releaseShared(int arg) {
        //释放共享锁
        if (tryReleaseShared(arg)) {
            //唤醒所有共享节点线程
            doReleaseShared();
            return true;
        }
        return false;
    }
```

```markdown
    /**
     * 唤醒所有共享节点线程
     */
    private void doReleaseShared() {
        for (;;) {
            Node h = head;
            if (h != null && h != tail) {
                int ws = h.waitStatus;
                if (ws == Node.SIGNAL) {//是否需要唤醒后继节点
                    if (!compareAndSetWaitStatus(h, Node.SIGNAL, 0))//修改状态为初始0
                        continue;
                    unparkSuccessor(h);//唤醒h.nex节点线程
                }
                else if (ws == 0 &&
                         !compareAndSetWaitStatus(h, 0, Node.PROPAGATE));
            }
            if (h == head)                   // loop if head changed
                break;
        }
    }
```


