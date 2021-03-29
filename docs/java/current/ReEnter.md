> 可重入锁，也叫做递归锁，指的是在同一线程内，外层函数获得锁之后，内层递归函数仍然可以获取到该锁。
> 换一种说法：同一个线程再次进入同步代码时，可以使用自己已获取到的锁。

## 作用

防止在同一线程中多次获取锁而导致死锁发生。

如下，我们通过自旋锁来判断是否会发生死锁：

```java
public class SpinLock {
    private AtomicReference<Thread> sign = new AtomicReference<>();
    public void lock(){
        Thread current = Thread.currentThread();
        while (!sign.compareAndSet(null,current)){
        }
    }
    public void unlock(){
        Thread cur = Thread.currentThread();
        sign.compareAndSet(cur,null);
    }
}

public class SpinLockDemo {
    private SpinLock lock =  new SpinLock();
    class Widget{
        public void doSomething(){
            lock.lock();
            System.out.println("Widget calling doSomething");
            lock.unlock();
        }
    }

    class LoggingWidget extends Widget {
        @Override
        public void doSomething() {
            lock.lock();
            System.out.println("LoggingWidget calling doSomething");
            super.doSomething();
            lock.unlock();
        }
    }

    public static void main(String[] args){
        SpinLockDemo spinLockDemo = new SpinLockDemo();
        SpinLockDemo.Widget widget = spinLockDemo.new LoggingWidget();
        widget.doSomething();
    }
}
```

输出结果：
LoggingWidget calling doSomething

我们可以看到在LoggingWidget类中doSomething方法时，通过锁进入临界区，并在临界区中调用了父类的该方法，而父类的方法要获取到同一个锁，被阻塞，导致死锁发生。

## 常见的可重入锁

* Synchronized关键字：

```java
public class SynchronizedDemo {
     class Widget{
        public synchronized void doSomething(){
            System.out.println("Widget calling doSomething...");
        }
    }

     class LoggingWidget extends Widget{
        @Override
        public synchronized void doSomething() {
            System.out.println("LoggingWidget calling doSomething");
            super.doSomething();
        }
    }

    public static void main(String[] args){
         SynchronizedDemo synchronizedDemo = new SynchronizedDemo();
        SynchronizedDemo.Widget widget = synchronizedDemo.new LoggingWidget();
        widget.doSomething();
    }
}
```

输出结果：
LoggingWidget calling doSomething
Widget calling doSomething...

根据结果，我们可以看到Synchronized关键字是可重入锁。

* ReetrantLock：

```java
public class ReentrantLockDemo {
    private Lock lock =  new ReentrantLock();
    class Widget{
        public void doSomething(){
            lock.lock();
            System.out.println("Widget calling doSomething");
            lock.unlock();
        }
    }

    class LoggingWidget extends Widget {
        @Override
        public void doSomething() {
            lock.lock();
            System.out.println("LoggingWidget calling doSomething");
            super.doSomething();
            lock.unlock();
        }
    }

    public static void main(String[] args){
        ReentrantLockDemo reentrantLockDemo = new ReentrantLockDemo();
        Widget widget = reentrantLockDemo.new LoggingWidget();
        widget.doSomething();
    }

}
```

输出结果：
LoggingWidget calling doSomething
Widget calling doSomething

根据结果，我们可以看出ReetrantLock锁时可重入的。

## 实现可重入锁

为每个锁关联一个获取计数器和一个所有者线程，当计数值为0时，这个锁就被认为是没有被任何线程所占有的。
当线程请求一个未被持有的锁时，计数值将会递增。而当线程退出同步代码时，计数器会相应地递减。当计数值为0时，则释放该锁。

如下：我们通过修改自旋锁来实现一个可重入的自旋锁

```java
public class SpinLockDemo {
    private MySpinLock lock =  new MySpinLock();
    class Widget{
        public void doSomething(){
            lock.lock();
            System.out.println("Widget calling doSomething");
            lock.unlock();
        }
    }

    class MySpinLock{
        private AtomicReference<Thread> owner = new AtomicReference<>();
        private int count = 0;
        public void lock(){
            Thread cur = Thread.currentThread();
            if (cur == owner.get()){
                count ++;
                return;
            }
            while (! owner.compareAndSet(null,cur)){

            }
        }

        public void unlock(){
            Thread cur = Thread.currentThread();
            if (cur == owner.get()){
                if (count != 0){
                    count --;
                } else {
                    owner.compareAndSet(cur,null);
                }
            }
        }
    }

    class LoggingWidget extends Widget {
        @Override
        public void doSomething() {
            lock.lock();
            System.out.println("LoggingWidget calling doSomething");
            super.doSomething();
            lock.unlock();
        }
    }

    public static void main(String[] args){
        SpinLockDemo spinLockDemo = new SpinLockDemo();
        SpinLockDemo.Widget widget = spinLockDemo.new LoggingWidget();
        widget.doSomething();
    }
}
```

输出结果：
LoggingWidget calling doSomething
Widget calling doSomething
