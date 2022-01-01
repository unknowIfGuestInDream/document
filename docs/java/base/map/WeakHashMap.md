## WeakHashMap
WeakHashMap的键是“弱键”。在 WeakHashMap 中，当某个键不再正常使用时，会被从WeakHashMap中被自动移除。更精确地说，对于一个给定的键，其映射的存在并不阻止垃圾回收器对该键的丢弃，这就使该键成为可终止的，被终止，然后被回收。某个键被终止时，它对应的键值对也就从映射中有效地移除了。

### tomcat两级缓存
tomcat的源码里，实现缓存时会用到WeakHashMap

```java
package org.apache.tomcat.util.collections;

import java.util.Map;
import java.util.WeakHashMap;
import java.util.concurrent.ConcurrentHashMap;

public final class ConcurrentCache<K,V> {

    private final int size;

    private final Map<K,V> eden;

    private final Map<K,V> longterm;

    public ConcurrentCache(int size) {
        this.size = size;
        this.eden = new ConcurrentHashMap<>(size);
        this.longterm = new WeakHashMap<>(size);
    }

    public V get(K k) {
        V v = this.eden.get(k);
        if (v == null) {
            synchronized (longterm) {
                v = this.longterm.get(k);
            }
            if (v != null) {
                this.eden.put(k, v);
            }
        }
        return v;
    }

    public void put(K k, V v) {
        if (this.eden.size() >= size) {
            synchronized (longterm) {
                this.longterm.putAll(this.eden);
            }
            this.eden.clear();
        }
        this.eden.put(k, v);
    }
}
```

源码中有eden和longterm的两个map，tomcat在这里是使用ConcurrentHashMap和WeakHashMap做了分代的缓存。

* 在put方法里，在插入一个k-v时，先检查eden缓存的容量是不是超了。没有超就直接放入eden缓存，如果超了则锁定longterm将eden中所有的k-v都放入longterm。再将eden清空并插入k-v。
* 在get方法中，也是优先从eden中找对应的v，如果没有则进入longterm缓存中查找，找到后就加入eden缓存并返回。

经过这样的设计，相对常用的对象都能在eden缓存中找到，不常用（有可能被销毁的对象）的则进入longterm缓存。而longterm的key的实际对象没有其他引用指向它时，gc就会自动回收heap中该弱引用指向的实际对象，弱引用进入引用队列。longterm调用expungeStaleEntries()方法，遍历引用队列中的弱引用，并清除对应的Entry，不会造成内存空间的浪费。

### 利用WeakHashMap实现内存缓存

WeakHashMap的这种特性比较适合实现类似本地、堆内缓存的存储机制——缓存的失效依赖于GC收集器的行为。

假设一种应用场景：我们需要保存一批大的图片对象，其中values是图片的内容，key是图片的名字，这里我们需要选择一种合适的容器保存这些对象。

使用普通的HashMap并不是好的选择，这些大对象将会占用很多内存，并且还不会被GC回收，除非我们在对应的key废弃之前主动remove掉这些元素。WeakHashMap非常适合使用在这种场景下

具体实现如下:
```java
public class Test {

    public void test1() {
       WeakHashMap<UniqueImageName, BigImage> map = new WeakHashMap<>();
       BigImage bigImage = new BigImage("image_id");
       UniqueImageName imageName = new UniqueImageName("name_of_big_image"); //强引用

       map.put(imageName, bigImage);
       assertTrue(map.containsKey(imageName));

       imageName = null; //map中的values对象成为弱引用对象
       System.gc(); //主动触发一次GC

       await().atMost(10, TimeUnit.SECONDS).until(map::isEmpty);
    }
}
```

首先，创建一个WeakHashMap对象来存储BigImage实例，对应的key是UniqueImageName对象，保存到WeakHashMap里的时候，key是一个弱引用类型。

然后，我们将imageName设置为null，这样就没有其他强引用指向bigImage对象，按照WeakHashMap的规则，在下一次GC周期中会回收bigImage对象。

通过System.gc()主动触发一次GC过程，然后可以发现WeakHashMap成为空的了。





