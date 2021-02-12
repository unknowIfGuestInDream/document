> springboot整合redis

首先安装Redis，具体步骤可以百度，然后引入依赖：

## Redis项目配置

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