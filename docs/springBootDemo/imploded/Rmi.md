>​Java RMI，即 远程方法调用(Remote Method Invocation)，一种用于实现远程过程调用(RPC)(Remote procedure call)的Java API， 能直接传输序列化后的Java对象和分布式垃圾收集。它的实现依赖于Java虚拟机(JVM)，因此它仅支持从一个JVM到另一个JVM的调用。

## 服务端

IUserService.java

```java
public interface IUserService {
    String invokingRemoteService();
}
```

UserServiceImpl.java

```java
@Service
public class UserServiceImpl implements IUserService {
    @Override
    public String invokingRemoteService() {
        // TODO Auto-generated method stub
        String result = "欢迎你调用远程接口";
        return result;
    }
}
```

RmiConfig.java

```java
@Configuration
@RequiredArgsConstructor
public class RmiConfig {
    private final IUserService userService;

    @Bean
    public RmiServiceExporter getRmiServiceExporter() {
        RmiServiceExporter rmiServiceExporter = new RmiServiceExporter();
        rmiServiceExporter.setServiceName("userService");
        rmiServiceExporter.setService(userService);
        rmiServiceExporter.setServiceInterface(IUserService.class);
        rmiServiceExporter.setRegistryPort(2002);
        return rmiServiceExporter;
    }
}
```

## 客户端

RmiClient.java

```java
@Configuration
public class RmiClient {

    @Bean(name = "userService")
    public RmiProxyFactoryBean getUserService() {
        RmiProxyFactoryBean rmiProxyFactoryBean = new RmiProxyFactoryBean();
        rmiProxyFactoryBean.setServiceUrl("rmi://127.0.0.1:2002/userService");
        rmiProxyFactoryBean.setServiceInterface(IUserService.class);
        return rmiProxyFactoryBean;
    }
}
```

IUserService.java
```java
public interface IUserService {

    String invokingRemoteService();
}
```

RmiTest.java

```java
@SpringBootTest
public class RmiTest {
    @Autowired
    private IUserService userService;
    @Test
    public void excel() throws Exception {
        System.out.println(userService.invokingRemoteService());
    }
}
```
