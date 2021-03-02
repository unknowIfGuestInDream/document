> Stream流

1. distinct: 对于Stream中包含的元素进行去重操作（去重逻辑依赖元素的equals方法），新生成的Stream中没有重复的元素；
2. filter: 对于Stream中包含的元素使用给定的过滤函数进行过滤操作，新生成的Stream只包含符合条件的元素；
3. map: 对于Stream中包含的元素使用给定的转换函数进行转换操作，新生成的Stream只包含转换生成的元素。
这个方法有三个对于原始类型的变种方法，分别是：mapToInt，mapToLong和mapToDouble。这三个方法也比较好理解，
比如mapToInt就是把原始Stream转换成一个新的Stream，这个新生成的Stream中的元素都是int类型。之所以会有这样三个变种方法，
可以免除自动装箱/拆箱的额外消耗；
4. flatMap：和map类似，不同的是其每个元素转换得到的是Stream对象，会把子Stream中的元素压缩到父集合中；
5. peek: 生成一个包含原Stream的所有元素的新Stream，同时会提供一个消费函数（Consumer实例），新Stream每个元素被消费的时候都会执行给定的消费函数；
6. limit: 对一个Stream进行截断操作，获取其前N个元素，如果原Stream中包含的元素个数小于N，那就获取其所有的元素；
7. skip: 返回一个丢弃原Stream的前N个元素后剩下元素组成的新Stream，如果原Stream中包含的元素个数小于N，那么返回空Stream；

性能问题

在对于一个Stream进行多次转换操作，每次都对Stream的每个元素进行转换，而且是执行多次，
这样时间复杂度就是一个for循环里把所有操作都做掉的N（转换的次数）倍啊。其实不是这样的，转换操作都是lazy的，
多个转换操作只会在汇聚操作（见下节）的时候融合起来，一次循环完成。我们可以这样简单的理解，Stream里有个操作函数的集合，
每次转换操作就是把转换函数放入这个集合中，在汇聚操作的时候循环Stream对应的集合，然后对每个元素执行所有的函数。

汇聚（Reduce）Stream

汇聚操作（也称为折叠）接受一个元素序列为输入，反复使用某个合并操作，把序列中的元素合并成一个汇总的结果。
比如查找一个数字列表的总和或者最大值，或者把这些数字累积成一个List对象。Stream接口有一些通用的汇聚操作，
比如reduce()和collect()；也有一些特定用途的汇聚操作，比如sum(),max()和count()。
注意：sum方法不是所有的Stream对象都有的，只有IntStream、LongStream和DoubleStream是实例才有。

搜索相关
* allMatch：是不是Stream中的所有元素都满足给定的匹配条件
* anyMatch：Stream中是否存在任何一个元素满足匹配条件
* findFirst: 返回Stream中的第一个元素，如果Stream为空，返回空Optional
* noneMatch：是不是Stream中的所有元素都不满足给定的匹配条件
* max和min：使用给定的比较器（Operator），返回Stream中的最大|最小值

