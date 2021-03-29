## LockSupport工具类

## ReentrantLock独占锁

## ReentrantReadWriteLock读写锁

## StampedLock

> java8新增的StampedLock

ReadWriteLock可以解决多线程同时读，但只有一个线程能写的问题。

如果我们深入分析ReadWriteLock，会发现它有个潜在的问题：如果有线程正在读，写线程需要等待读线程释放锁后才能获取写锁，即读的过程中不允许写，这是一种悲观的读锁。

要进一步提升并发执行效率，Java 8引入了新的读写锁：StampedLock。

StampedLock和ReadWriteLock相比，改进之处在于：读的过程中也允许获取写锁后写入！这样一来，我们读的数据就可能不一致，所以，需要一点额外的代码来判断读的过程中是否有写入，这种读锁是一种乐观锁。

乐观锁的意思就是乐观地估计读的过程中大概率不会有写入，因此被称为乐观锁。反过来，悲观锁则是读的过程中拒绝有写入，也就是写入必须等待。显然乐观锁的并发效率更高，但一旦有小概率的写入导致读取的数据不一致，需要能检测出来，再读一遍就行。

例子：

```java
public class Point {
    private final StampedLock stampedLock = new StampedLock();

    //x,y就是临界区的共享变量，访问的时候，注意线程安全
    private double x;
    private double y;
    //这里是对x,y的修改，所以需要写锁
    public void move(double deltaX, double deltaY) {
        //申请写锁，返回的是一个邮戳，unlock的时候需要用这个邮戳
        long stamp = stampedLock.writeLock(); // 获取写锁
        try {
            x += deltaX;
            y += deltaY;
        } finally {
            //使用邮戳释放刚才的写锁            
            stampedLock.unlockWrite(stamp); // 释放写锁
        }
    }

    //下面是一个读取，使用乐观锁，如果失败，转为普通读锁
    public double distanceFromOrigin() {
        //获得一个乐观锁
        long stamp = stampedLock.tryOptimisticRead();
        // 注意下面两行代码不是原子操作
        // 假设x,y = (100,200)
        double currentX = x, currentY = y;
        // 此处已读取到x=100，但x,y可能被写线程修改为(300,400)
        // 此处已读取到y，如果没有写入，读取是正确的(100,200)
        // 如果有写入，读取是错误的(100,400)
        //检查乐观读锁后是否有其他写锁发生 validate函数进行冲突校验
        if (!stampedLock.validate(stamp)) { 
            //如果有人跟我冲突了，所以就用悲观的策略进行补充， 也可以使用乐观锁 再自旋几次
            stamp = stampedLock.readLock(); // 获取一个悲观读锁
            try {
                currentX = x;
                currentY = y;
            } finally {
                stampedLock.unlockRead(stamp); // 释放悲观读锁
            }
        }

        return Math.sqrt(currentX * currentX + currentY * currentY);
    }

     //读锁向写锁转换
     void moveIfAtOrigin(double newX, double newY) { 
            // 这里直接用悲观策略，写的复杂一些，也可以用乐观策略
            long stamp = sl.readLock();
            try {
                //一个自旋，如果还在原点，就不停重试
                while (x == 0.0 && y == 0.0) {
                    //锁升级为写锁 ws=0表示失败 否则就是可用的邮戳
                    //如果邮戳已经表示写锁，则直接返回
                    long ws = sl.tryConvertToWriteLock(stamp);  //读锁转换为写锁
                    if (ws != 0L) {
                        //升级写锁成功，修改数据
                        stamp = ws;
                        x = newX;
                        y = newY;
                        break;
                    } else {
                        //升级写锁失败，显式释放读锁
                        sl.unlockRead(stamp);
                        //显式直接进行写锁，然后再通过循环再试
                        stamp = sl.writeLock();
                    }
                }
            } finally {
                sl.unlock(stamp);
            }
        }

}
```

和ReadWriteLock相比，写入的加锁是完全一样的，不同的是读取。注意到首先我们通过tryOptimisticRead()获取一个乐观读锁，并返回版本号。接着进行读取，读取完成后，我们通过validate()去验证版本号，如果在读取过程中没有写入，版本号不变，验证成功，我们就可以放心地继续后续操作。如果在读取过程中有写入，版本号会发生变化，验证将失败。在失败的时候，我们再通过获取悲观读锁再次读取。由于写入的概率不高，程序在绝大部分情况下可以通过乐观读锁获取数据，极少数情况下使用悲观读锁获取数据。

可见，StampedLock把读锁细分为乐观读和悲观读，能进一步提升并发效率。但这也是有代价的：一是代码更加复杂，二是StampedLock是不可重入锁，不能在一个线程中反复获取同一个锁。

StampedLock还提供了更复杂的将悲观读锁升级为写锁的功能，它主要使用在if-then-update的场景：即先读，如果读的数据满足条件，就返回，如果读的数据不满足条件，再尝试写。

**小结**  
StampedLock提供了乐观读锁，可取代ReadWriteLock以进一步提升并发性能；

StampedLock是不可重入锁。

