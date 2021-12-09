> Redis是用C语言开发的一个高性能键值对数据库，可用于数据缓存，主要用于处理大量数据的高访问负载。

## redis使用场景

**1. 热点数据的缓存**

由于redis速度块、支持的数据类型比较丰富，所以redis很适合用来存储热点数据，另外结合expire，我们可以设置过期时间然后再进行缓存更新操作，这个功能最为常见，我们几乎所有的项目都有所运用。

**2. 计数器相关问题**

redis由于incrby命令可以实现原子性的递增，所以可以运用于高并发的秒杀活动、分布式序列号的生成、具体业务还体现在比如限制一个手机号发多少条短信、一个接口一分钟限制多少请求、一个接口一天限制调用多少次等等。

**3. 排行榜相关问题**

关系型数据库在排行榜方面查询速度普遍偏慢，所以可以借助redis的SortedSet进行热点数据的排序。  
在奶茶活动中，我们需要展示各个部门的点赞排行榜， 所以我针对每个部门做了一个SortedSet,然后以用户的openid作为上面的username,以用户的点赞数作为上面的score, 然后针对每个用户做一个hash,通过zrangebyscore就可以按照点赞数获取排行榜，然后再根据username获取用户的hash信息，这个当时在实际运用中性能体验也蛮不错的。

**4. 分布式锁**

* 如果不存在则成功设置缓存同时返回1，否则返回0 ，比如我们服务器是集群的，定时任务可能在两台机器上都会运行，所以在定时任务中首先 如果成功设置则执行，如果没有成功设置，则表明该定时任务已执行。当然结合具体业务，我们可以给这个lock加一个过期时间，比如说30分钟执行一次的定时任务，那么这个过期时间设置为小于30分钟的一个时间 就可以，这个与定时任务的周期以及定时任务执行消耗时间相关。  
当然我们可以将这个特性运用于其他需要分布式锁的场景中，结合过期时间主要是防止死锁的出现。  
* 验证前端的重复请求（可以自由扩展类似情况），可以通过redis进行过滤：每次请求将request Ip、参数、接口等hash作为key存储redis（幂等性请求），设置多长时间有效期，然后下次请求过来的时候先在redis中检索有没有这个key，进而验证是不是一定时间内过来的重复提交  
* 秒杀系统，基于redis是单线程特征，防止出现数据库“爆破”  
* 全局增量ID生成，类似“秒杀”

**5. 延时操作**

这个目前我做过相关测试，但是还没有运用到我们的实际项目中，下面我举个该特性的应用场景。比如在订单生产后我们占用了库存，10分钟后去检验用户是够真正购买，如果没有购买将该单据设置无效，同时还原库存。由于redis自2.8.0之后版本提供Keyspace Notifications功能，允许客户订阅Pub/Sub频道，以便以某种方式接收影响Redis数据集的事件。所以我们对于上面的需求就可以用以下解决方案，我们在订单生产时，设置一个key，同时设置10分钟后过期， 我们在后台实现一个监听器，监听key的实效，监听到key失效时将后续逻辑加上。当然我们也可以利用rabbitmq、activemq等消息中间件的延迟队列服务实现该需求。

**6. 分页、模糊搜索**

前几天我通过这个特性，对学校数据进行了模拟测试，学校数据60万左右，响应时间在700ms左右，比mysql的like查询稍微快一点，但是由于它可以避免大量的数据库io操作，所以总体还是比直接mysql查询更利于系统的性能保障。

**7. 点赞、好友等相互关系的存储**

Redis set对外提供的功能与list类似是一个列表的功能，特殊之处在于set是可以自动排重的，当你需要存储一个列表数据，又不希望出现重复数据时，set是一个很好的选择，并且set提供了判断某个成员是否在一个set集合内的重要接口，这个也是list所不能提供的。又或者在微博应用中，每个用户关注的人存在一个集合中，就很容易实现求两个人的共同好友功能。  
这个在奶茶活动中有运用，就是利用set存储用户之间的点赞关联的，另外在点赞前判断是否点赞过就利用了sismember方法，当时这个接口的响应时间控制在10毫秒内，十分高效。

**8. 队列**

由于redis有list push和list pop这样的命令，所以能够很方便的执行队列操作。

**9. 位操作（大数据处理）**

用于数据量上亿的场景下，例如几亿用户系统的签到，去重登录次数统计，某用户是否在线状态等等。  
想想一下腾讯10亿用户，要几个毫秒内查询到某个用户是否在线，你能怎么做？千万别说给每个用户建立一个key，然后挨个记（你可以算一下需要的内存会很恐怖，而且这种类似的需求很多，腾讯光这个得多花多少钱。。）好吧。这里要用到位操作——使用setbit、getbit、bitcount命令。  
原理是：  
redis内构建一个足够长的数组，每个数组元素只能是0和1两个值，然后这个数组的下标index用来表示我们上面例子里面的用户id（必须是数字哈），那么很显然，这个几亿长的大数组就能通过下标和元素值（0和1）来构建一个记忆系统，上面我说的几个场景也就能够实现。用到的命令是：setbit、getbit、bitcount

**10. 最新列表**

例如新闻列表页面最新的新闻列表，如果总数量很大的情况下，尽量不要使用select a from A limit 10这种low货，尝试redis的 LPUSH命令构建List，一个个顺序都塞进去就可以啦。不过万一内存清掉了咋办？也简单，查询不到存储key的话，用mysql查询并且初始化一个List到redis中就好了。

## Redis项目配置

首先安装Redis，具体步骤可以百度，然后引入依赖：

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>

        <!-- 对象池，使用redis时必须引入 -->
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-pool2</artifactId>
        </dependency>
```

application.yml

```yaml
spring:
  redis:
    host: localhost
    password: ENC(k27pYXuWBDRKKoL7g/AMwr17J/fwm46M)
    # 连接超时时间（记得添加单位，Duration）
    timeout: 3000
    # Redis默认情况下有16个分片，这里配置具体使用的分片
    database: 0
    lettuce:
      pool:
        # 连接池最大连接数（使用负值表示没有限制） 默认 8
        max-active: 8
        # 连接池最大阻塞等待时间（使用负值表示没有限制） 默认 -1
        max-wait: -1ms
        # 连接池中的最大空闲连接 默认 8
        max-idle: 8
        # 连接池中的最小空闲连接 默认 0
        min-idle: 0
  cache:
    # 一般来说是不用配置的，Spring Cache 会根据依赖的包自行装配
    type: redis
## 自定义redis key
redis:
  key:
    prefix:
      authCode: "demo:authCode:"
    expire:
      authCode: 120 # 验证码超期时间
```

## Redis属性配置

```java
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.serializer.SerializerFeature;
import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.fasterxml.jackson.annotation.PropertyAccessor;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.jsontype.impl.LaissezFaireSubTypeValidator;
import lombok.extern.slf4j.Slf4j;
import org.aopalliance.intercept.MethodInterceptor;
import org.aopalliance.intercept.MethodInvocation;
import org.springframework.aop.MethodBeforeAdvice;
import org.springframework.aop.framework.ProxyFactory;
import org.springframework.aop.framework.adapter.MethodBeforeAdviceInterceptor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.CachingConfigurerSupport;
import org.springframework.cache.interceptor.CacheErrorHandler;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.cache.RedisCacheConfiguration;
import org.springframework.data.redis.cache.RedisCacheManager;
import org.springframework.data.redis.cache.RedisCacheWriter;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.data.redis.serializer.Jackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializationContext;
import org.springframework.data.redis.serializer.RedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

import java.lang.reflect.Method;
import java.time.Duration;

/**
 * cache默认配置，如果需要自由操作Redis 调用 RedisService
 *
 * @author 唐亮
 * @date 13:02 2020/7/11
 * @return
 */
@Configuration
@Slf4j
public class RedisConfig extends CachingConfigurerSupport {

    @Value("${redis.key.prefix.authCode}")
    private String REDIS_KEY_PREFIX_AUTH_CODE;
    @Value("${redis.key.expire.authCode}")
    private Long AUTH_CODE_EXPIRE_SECONDS;

    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory) {
        RedisSerializer<Object> serializer = redisSerializer();
        RedisTemplate<String, Object> redisTemplate = new RedisTemplate<>();
        redisTemplate.setConnectionFactory(redisConnectionFactory);
        redisTemplate.setKeySerializer(new StringRedisSerializer());
        redisTemplate.setValueSerializer(serializer);
        redisTemplate.setHashKeySerializer(new StringRedisSerializer());
        redisTemplate.setHashValueSerializer(serializer);
        redisTemplate.afterPropertiesSet();

        //运用代理添加redis日志,如果不需要日志，可以取消下面代码，直接返回redisTemplate
        ProxyFactory proxyFactory = new ProxyFactory();
        proxyFactory.setTarget(redisTemplate);
        //setProxyTargetClass为true，就是以cglib动态代理方式生成代理类，淡然设置为false，就是默认用JDK动态代理技术
        proxyFactory.setProxyTargetClass(true);
        proxyFactory.addAdvice(new MethodInterceptor() {
            @Override
            public Object invoke(MethodInvocation methodInvocation) throws Throwable {
                //拦截opsForHash
                Boolean b = methodInvocation.getMethod().getName().equals("opsForValue");
                if (b) {
                    //取得opsForHash结果
                    ValueOperations valueOperations = (ValueOperations) methodInvocation.proceed();
                    //对hashOperations代理
                    ProxyFactory proxyFactory = new ProxyFactory();
                    proxyFactory.setTarget(valueOperations);
                    proxyFactory.setProxyTargetClass(false);
                    //添加日志
                    proxyFactory.addAdvice(new MethodBeforeAdviceInterceptor(new MethodBeforeAdvice() {
                        @Override
                        public void before(Method method, Object[] args, Object o) throws Throwable {
                            log.debug("method:{}, args:{}", method.getName(), JSON.toJSONString(args, SerializerFeature.PrettyFormat));
                        }
                    }));
                    //返回代理
                    return proxyFactory.getProxy();
                }
                return methodInvocation.proceed();
            }
        });
        Object proxy = proxyFactory.getProxy();
        return (RedisTemplate<String, Object>) proxy;
        //return redisTemplate;
    }

    @Bean
    public RedisSerializer<Object> redisSerializer() {
        //创建JSON序列化器
        Jackson2JsonRedisSerializer<Object> serializer = new Jackson2JsonRedisSerializer<>(Object.class);
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
        objectMapper.activateDefaultTyping(LaissezFaireSubTypeValidator.instance,
                ObjectMapper.DefaultTyping.NON_FINAL, JsonTypeInfo.As.PROPERTY);
        serializer.setObjectMapper(objectMapper);
        return serializer;
    }

    @Bean
    public CacheManager redisCacheManager(RedisConnectionFactory redisConnectionFactory) {
        RedisCacheWriter redisCacheWriter = RedisCacheWriter.nonLockingRedisCacheWriter(redisConnectionFactory);
        //设置Redis缓存有效期为1天
        RedisCacheConfiguration redisCacheConfiguration = RedisCacheConfiguration
                .defaultCacheConfig()
                .serializeValuesWith(RedisSerializationContext.SerializationPair.fromSerializer(redisSerializer()))
                .prefixCacheNameWith(REDIS_KEY_PREFIX_AUTH_CODE)
                //失效时间
                .entryTtl(Duration.ofSeconds(AUTH_CODE_EXPIRE_SECONDS))
                .disableCachingNullValues();
        //.disableKeyPrefix();
        return new RedisCacheManager(redisCacheWriter, redisCacheConfiguration);
    }

    @Override
    public CacheErrorHandler errorHandler() {
        return new IgnoreExceptionCacheErrorHandler();
    }
}
```

Redis缓存异常处理:

```java
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.Cache;
import org.springframework.cache.interceptor.CacheErrorHandler;

/**
 * @author: TangLiang
 * @date: 2020/10/6 8:01
 * @since: 1.0
 */
@Slf4j
public class IgnoreExceptionCacheErrorHandler implements CacheErrorHandler {

    @Override
    public void handleCacheGetError(RuntimeException exception, Cache cache, Object key) {
        log.error(exception.getMessage(), exception);
    }

    @Override
    public void handleCachePutError(RuntimeException exception, Cache cache, Object key, Object value) {
        log.error(exception.getMessage(), exception);
    }

    @Override
    public void handleCacheEvictError(RuntimeException exception, Cache cache, Object key) {
        log.error(exception.getMessage(), exception);
    }

    @Override
    public void handleCacheClearError(RuntimeException exception, Cache cache) {
        log.error(exception.getMessage(), exception);
    }
}
```

## Redis基础操作工具类

### Redis基础操作接口:

```java
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * redis操作Service
 *
 * @author: TangLiang
 * @date: 2020/8/1 12:00
 * @since: 1.0
 */
public interface RedisService {
    /**
     * 保存属性
     */
    void set(String key, Object value, long time);

    /**
     * 保存属性
     */
    void set(String key, Object value);

    /**
     * 获取属性
     */
    Object get(String key);

    /**
     * 删除属性
     */
    Boolean del(String key);

    /**
     * 批量删除属性
     */
    Long del(List<String> keys);

    /**
     * 设置过期时间
     */
    Boolean expire(String key, long time);

    /**
     * 获取过期时间
     */
    Long getExpire(String key);

    /**
     * 判断是否有该属性
     */
    Boolean hasKey(String key);

    /**
     * 按delta递增
     */
    Long incr(String key, long delta);

    /**
     * 按delta递减
     */
    Long decr(String key, long delta);

    /**
     * 获取Hash结构中的属性
     */
    Object hGet(String key, String hashKey);

    /**
     * 向Hash结构中放入一个属性
     */
    Boolean hSet(String key, String hashKey, Object value, long time);

    /**
     * 向Hash结构中放入一个属性
     */
    void hSet(String key, String hashKey, Object value);

    /**
     * 直接获取整个Hash结构
     */
    Map<Object, Object> hGetAll(String key);

    /**
     * 直接设置整个Hash结构
     */
    Boolean hSetAll(String key, Map<String, Object> map, long time);

    /**
     * 直接设置整个Hash结构
     */
    void hSetAll(String key, Map<String, Object> map);

    /**
     * 删除Hash结构中的属性
     */
    void hDel(String key, Object... hashKey);

    /**
     * 判断Hash结构中是否有该属性
     */
    Boolean hHasKey(String key, String hashKey);

    /**
     * Hash结构中属性递增
     */
    Long hIncr(String key, String hashKey, Long delta);

    /**
     * Hash结构中属性递减
     */
    Long hDecr(String key, String hashKey, Long delta);

    /**
     * 获取Set结构
     */
    Set<Object> sMembers(String key);

    /**
     * 向Set结构中添加属性
     */
    Long sAdd(String key, Object... values);

    /**
     * 向Set结构中添加属性
     */
    Long sAdd(String key, long time, Object... values);

    /**
     * 是否为Set中的属性
     */
    Boolean sIsMember(String key, Object value);

    /**
     * 获取Set结构的长度
     */
    Long sSize(String key);

    /**
     * 删除Set结构中的属性
     */
    Long sRemove(String key, Object... values);

    /**
     * 获取List结构中的属性
     */
    List<Object> lRange(String key, long start, long end);

    /**
     * 获取List结构的长度
     */
    Long lSize(String key);

    /**
     * 根据索引获取List中的属性
     */
    Object lIndex(String key, long index);

    /**
     * 向List结构中添加属性
     */
    Long lPush(String key, Object value);

    /**
     * 向List结构中添加属性
     */
    Long lPush(String key, Object value, long time);

    /**
     * 向List结构中批量添加属性
     */
    Long lPushAll(String key, Object... values);

    /**
     * 向List结构中批量添加属性
     */
    Long lPushAll(String key, Long time, Object... values);

    /**
     * 从List结构中移除属性
     */
    Long lRemove(String key, long count, Object value);
}
```

### Redis基础工具实现类:

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.TimeUnit;

/**
 * redis操作实现类
 *
 * @author: TangLiang
 * @date: 2020/8/1 12:01
 * @since: 1.0
 */
@Service
public class RedisServiceImpl implements RedisService {
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Override
    public void set(String key, Object value, long time) {
        redisTemplate.opsForValue().set(key, value, time, TimeUnit.SECONDS);
    }

    @Override
    public void set(String key, Object value) {
        redisTemplate.opsForValue().set(key, value);
    }

    @Override
    public Object get(String key) {
        return redisTemplate.opsForValue().get(key);
    }

    @Override
    public Boolean del(String key) {
        return redisTemplate.delete(key);
    }

    @Override
    public Long del(List<String> keys) {
        return redisTemplate.delete(keys);
    }

    @Override
    public Boolean expire(String key, long time) {
        return redisTemplate.expire(key, time, TimeUnit.SECONDS);
    }

    @Override
    public Long getExpire(String key) {
        return redisTemplate.getExpire(key, TimeUnit.SECONDS);
    }

    @Override
    public Boolean hasKey(String key) {
        return redisTemplate.hasKey(key);
    }

    @Override
    public Long incr(String key, long delta) {
        return redisTemplate.opsForValue().increment(key, delta);
    }

    @Override
    public Long decr(String key, long delta) {
        return redisTemplate.opsForValue().increment(key, -delta);
    }

    @Override
    public Object hGet(String key, String hashKey) {
        return redisTemplate.opsForHash().get(key, hashKey);
    }

    @Override
    public Boolean hSet(String key, String hashKey, Object value, long time) {
        redisTemplate.opsForHash().put(key, hashKey, value);
        return expire(key, time);
    }

    @Override
    public void hSet(String key, String hashKey, Object value) {
        redisTemplate.opsForHash().put(key, hashKey, value);
    }

    @Override
    public Map<Object, Object> hGetAll(String key) {
        return redisTemplate.opsForHash().entries(key);
    }

    @Override
    public Boolean hSetAll(String key, Map<String, Object> map, long time) {
        redisTemplate.opsForHash().putAll(key, map);
        return expire(key, time);
    }

    @Override
    public void hSetAll(String key, Map<String, Object> map) {
        redisTemplate.opsForHash().putAll(key, map);
    }

    @Override
    public void hDel(String key, Object... hashKey) {
        redisTemplate.opsForHash().delete(key, hashKey);
    }

    @Override
    public Boolean hHasKey(String key, String hashKey) {
        return redisTemplate.opsForHash().hasKey(key, hashKey);
    }

    @Override
    public Long hIncr(String key, String hashKey, Long delta) {
        return redisTemplate.opsForHash().increment(key, hashKey, delta);
    }

    @Override
    public Long hDecr(String key, String hashKey, Long delta) {
        return redisTemplate.opsForHash().increment(key, hashKey, -delta);
    }

    @Override
    public Set<Object> sMembers(String key) {
        return redisTemplate.opsForSet().members(key);
    }

    @Override
    public Long sAdd(String key, Object... values) {
        return redisTemplate.opsForSet().add(key, values);
    }

    @Override
    public Long sAdd(String key, long time, Object... values) {
        Long count = redisTemplate.opsForSet().add(key, values);
        expire(key, time);
        return count;
    }

    @Override
    public Boolean sIsMember(String key, Object value) {
        return redisTemplate.opsForSet().isMember(key, value);
    }

    @Override
    public Long sSize(String key) {
        return redisTemplate.opsForSet().size(key);
    }

    @Override
    public Long sRemove(String key, Object... values) {
        return redisTemplate.opsForSet().remove(key, values);
    }

    @Override
    public List<Object> lRange(String key, long start, long end) {
        return redisTemplate.opsForList().range(key, start, end);
    }

    @Override
    public Long lSize(String key) {
        return redisTemplate.opsForList().size(key);
    }

    @Override
    public Object lIndex(String key, long index) {
        return redisTemplate.opsForList().index(key, index);
    }

    @Override
    public Long lPush(String key, Object value) {
        return redisTemplate.opsForList().rightPush(key, value);
    }

    @Override
    public Long lPush(String key, Object value, long time) {
        Long index = redisTemplate.opsForList().rightPush(key, value);
        expire(key, time);
        return index;
    }

    @Override
    public Long lPushAll(String key, Object... values) {
        return redisTemplate.opsForList().rightPushAll(key, values);
    }

    @Override
    public Long lPushAll(String key, Long time, Object... values) {
        Long count = redisTemplate.opsForList().rightPushAll(key, values);
        expire(key, time);
        return count;
    }

    @Override
    public Long lRemove(String key, long count, Object value) {
        return redisTemplate.opsForList().remove(key, count, value);
    }
}
```

## Redis工具类测试

```java
package com.tangl.demo.controller.redis;

import com.tangl.demo.annotation.LogAnno;
import com.tangl.demo.redis.RedisService;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.CacheManager;
import org.springframework.data.redis.cache.RedisCache;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.HashMap;
import java.util.Map;

/**
 * @author: TangLiang
 * @date: 2020/8/1 12:02
 * @since: 1.0
 */
@Api(tags = "Redis测试")
@Controller
@RequestMapping("/redis")
public class RedisController {
    @Autowired
    private RedisService redisService;

    @ApiOperation("测试简单缓存")
    @RequestMapping(value = "/simpleTest", method = RequestMethod.GET)
    @ResponseBody
    public Map simpleTest() {
        Map result = new HashMap();
        String key = "redis:simple:" + "1001";
        redisService.set(key, 1000);
        result.put("success", true);
        result.put("result", redisService.get(key));
        return result;
    }

    @ApiOperation("获取简单缓存")
    @RequestMapping(value = "/getSimpleTest", method = RequestMethod.GET)
    @ResponseBody
    public Map getSimpleTest(String name) {
        Map result = new HashMap();
        result.put("success", true);
        result.put("result", redisService.get(name));
        return result;
    }

    @ApiOperation("测试简单缓存递增")
    @RequestMapping(value = "/simpleTestIns", method = RequestMethod.GET)
    @ResponseBody
    public Map simpleTestIns() {
        Map result = new HashMap();
        String key = "redis:simple:" + "1001";
        redisService.incr(key, 1);
        result.put("success", true);
        result.put("result", redisService.get(key));
        return result;
    }

    @ApiOperation("测试Hash结构的缓存")
    @RequestMapping(value = "/hashTest", method = RequestMethod.GET)
    @ResponseBody
    public Map hashTest() {
        Map result = new HashMap();
        String key = "redis:hash:" + "1002";
        Map<String, Object> value = new HashMap<>();
        value.put("id", "1");
        value.put("name", "唐三");
        redisService.hSetAll(key, value);
        result.put("success", true);
        result.put("result", redisService.hGetAll(key));
        return result;
    }

    @ApiOperation("测试Hash结构的缓存&添加一个key")
    @RequestMapping(value = "/hashTestKey", method = RequestMethod.GET)
    @ResponseBody
    public Map hashTestKey() {
        Map result = new HashMap();
        String key = "redis:hash:" + "1002";
        redisService.hSet(key, "age", 18);
        result.put("success", true);
        result.put("result", redisService.hGetAll(key));
        return result;
    }

    @ApiOperation("测试Set结构的缓存")
    @RequestMapping(value = "/setTest", method = RequestMethod.GET)
    @ResponseBody
    public Map setTest() {
        Map result = new HashMap();
        String key = "redis:set:all";
        Map<String, Object> value = new HashMap<>();
        value.put("id", "1");
        value.put("name", "唐三");
        redisService.sAdd(key, value);
        result.put("success", true);
        result.put("result", redisService.sMembers(key));
        return result;
    }

    @ApiOperation("测试List结构的缓存")
    @RequestMapping(value = "/listTest", method = RequestMethod.GET)
    @ResponseBody
    public Map listTest() {
        String key = "redis:list:all";
        Map result = new HashMap();
        Map<String, Object> value = new HashMap<>();
        value.put("id", "1");
        value.put("name", "唐三");
        redisService.lPushAll(key, value);
        //redisService.lRemove(key, 1, value);
        result.put("success", true);
        result.put("result", redisService.lRange(key, 0, 3));
        return result;
    }

    @ApiOperation("测试List结构的缓存&根据索引获取")
    @RequestMapping(value = "/listTestIndex", method = RequestMethod.GET)
    @ResponseBody
    public Map listTestIndex() {
        String key = "redis:list:all";
        Map result = new HashMap();
        Map<String, Object> value = new HashMap<>();
        value.put("id", "3");
        value.put("name", "唐三");
        redisService.lPush(key, value);
        result.put("success", true);
        result.put("size", redisService.lSize(key));
        result.put("res", redisService.lIndex(key, 3));
        result.put("result", redisService.lRange(key, 0, 3));
        return result;
    }
}
```

上述封装了常用的基础操作方法，还有一些其他的方法，如对key的“bound”(绑定)便捷化操作API，可以通过bound封装指定的key，然后进行一系列的操作而无须“显式”的再次指定Key，即BoundKeyOperations：

1. BoundValueOperations
2. BoundSetOperations
3. BoundListOperations
4. BoundSetOperations
5. BoundHashOperations

还有multiGet, getAndSet, append, keys, setIfAbsent等方法。

## StringRedisTemplate与RedisTemplate

1. 两者的关系是StringRedisTemplate继承RedisTemplate。  
2. 两者的数据是不共通的；也就是说StringRedisTemplate只能管理StringRedisTemplate里面的数据，RedisTemplate只能管理RedisTemplate中的数据。
3. SDR默认采用的序列化策略有两种，一种是String的序列化策略，一种是JDK的序列化策略。  
StringRedisTemplate默认采用的是String的序列化策略，保存的key和value都是采用此策略序列化保存的。  
RedisTemplate默认采用的是JDK的序列化策略，保存的key和value都是采用此策略序列化保存的。

## 使用scan代替keys指令

keys * 这个命令千万别在生产环境乱用。特别是数据庞大的情况下。因为Keys会引发Redis锁，并且增加Redis的CPU占用。很多公司的运维都是禁止了这个命令的
当需要扫描key，匹配出自己需要的key时，可以使用 scan 命令。

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.connection.RedisConnection;
import org.springframework.data.redis.core.Cursor;
import org.springframework.data.redis.core.ScanOptions;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

@Component
public class RedisHelper {
	
	@Autowired
	private StringRedisTemplate stringRedisTemplate;
	
	/**
	 * scan 实现
	 * @param pattern	表达式
	 * @param consumer	对迭代到的key进行操作
	 */
	public void scan(String pattern, Consumer<byte[]> consumer) {
		this.stringRedisTemplate.execute((RedisConnection connection) -> {
			try (Cursor<byte[]> cursor = connection.scan(ScanOptions.scanOptions().count(Long.MAX_VALUE).match(pattern).build())) {
				cursor.forEachRemaining(consumer);
				return null;
			} catch (IOException e) {
				e.printStackTrace();
				throw new RuntimeException(e);
			}
		});
	}

	/**
	 * 获取符合条件的key
	 * @param pattern	表达式
	 * @return
	 */
	public List<String> keys(String pattern) {
		List<String> keys = new ArrayList<>();
		this.scan(pattern, item -> {
			//符合条件的key
			String key = new String(item,StandardCharsets.UTF_8);
			keys.add(key);
		});
		return keys;
	}
}
```

## 注解+redis接口防刷

https://mp.weixin.qq.com/s/whrBi7SSGJrZS8l5RWaTWg

## 使用redis存储session

在pom.xml中添加

```
<dependency>
     <groupId>org.springframework.session</groupId>
      <artifactId>spring-session-data-redis</artifactId>
</dependency>
```

在启动类（任意新建一个空类都可以）上面添加注解：@EnableRedisHttpSession(maxInactiveIntervalInSeconds = 86400*30)

@EnableRedisHttpSession注解其中maxInactiveIntervalInSeconds参数是设置Session失效时间，开启注解后spring会生成一个新的拦截器，用于实现Session共享操作

启动项目后进入页面 会发现信息存储到了redis中

测试方法获取sessionid值，具体代码如下：

```java
@RequestMapping("/uid")
public String uid(HttpSession session) {
    UUID uid = (UUID) session.getAttribute("uid");
    if (uid == null) {
        uid = UUID.randomUUID();
    }
    session.setAttribute("uid", uid);
    return session.getId();
}
```

## Redisson简单用法

Redisson - 是一个高级的分布式协调Redis客服端，能帮助用户在分布式环境中轻松实现一些Java的对象 (Bloom filter, BitSet, Set, SetMultimap, ScoredSortedSet, SortedSet, Map, ConcurrentMap, List, ListMultimap, Queue, BlockingQueue, Deque, BlockingDeque, Semaphore, Lock, ReadWriteLock, AtomicLong, CountDownLatch, Publish / Subscribe, HyperLogLog)。

https://www.cnblogs.com/cjsblog/p/11273205.html  
https://blog.csdn.net/u010963948/article/details/79240050