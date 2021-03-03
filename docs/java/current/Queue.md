## ConcurrentLinkedQueue

## LinkedBlockingQueue

## ArrayBlockingQueue

## PriorityBlockingQueue

## DelayQueue

优势：java 自身支持的阻塞式队列，对性能损耗小、及时、使用简单。

缺陷：  
1. 数据不能持久化，服务停止了消息就不存在了。
2. 不适应分布式环境，消息都存在JVM内存里面了，多个服务JVM不互通，分布式场景中使用需要做额外处理。

```java
@Data
public class DelayMessage implements Delayed {

 private final long delayTime; //延迟时间
 private final long expire;  //到期时间
 private String msg;   //发送消息

 public DelayMessage(long delay, String msg) {
 delayTime = delay;
 this.msg = msg;
 expire = System.currentTimeMillis() + delay;
    }

 /**
     * 剩余时间=到期时间-当前时间
     */
 @Override
 public long getDelay(TimeUnit unit) {
 return unit.convert(this.expire - System.currentTimeMillis() , TimeUnit.MILLISECONDS);
    }

 /**
     * 优先队列里面优先级规则
     */
 @Override
 public int compareTo(Delayed o) {
 return (int) (this.getDelay(TimeUnit.MILLISECONDS) -o.getDelay(TimeUnit.MILLISECONDS));
    }

 public static void main(String[] args) throws  Exception{
        BlockingQueue<DelayMessage> queue=new DelayQueue<DelayMessage>();
        DelayMessage sendMsg=new DelayMessage(10000,"我很帅也很温柔");//10秒后激活消息
 queue.offer(sendMsg);//发送消息
 DelayMessage receiverMsg= queue.take();//阻塞获取消息
 System.out.println(receiverMsg.getMsg());
    }
}
```
