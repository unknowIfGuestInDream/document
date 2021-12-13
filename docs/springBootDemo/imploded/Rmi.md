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

## 拓展-Spring RPC

Spring对RPC有丰富的支持,给出了以下几种方案
* RMI 基于RMI协议，使用java的序列化机制，客户端服务端都必须时java，RMI协议不被防火墙支持，只能在内网使用
* Hessian 基于HTTP协议，使用自身的序列化机制，客户端服务端可以是不同的语言，HTTP协议被防火墙支持，可被外网访问
* Burlap 已过时
* HttpInvoker 基于HTTP协议，使用java的序列化机制，客户端服务端都必须时java，必须使用spring，HTTP协议被防火墙支持，可被外网访问
* web service 基于SOAP协议，使用自身的序列化机制，客户端服务端可以是不同的语言，HTTP+XML（WSDL语法）协议被防火墙支持，可被外网访问

### 客户端
```java
import javax.jws.WebParam;

import com.zgg.group2.rpcserver.bean.RPCPojo;

public interface RpcService {
	RPCPojo get();
	RPCPojo post(@WebParam RPCPojo obj);
	RPCPojo put(@WebParam RPCPojo obj);
	RPCPojo delete(@WebParam Integer id);
}
```

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.remoting.caucho.HessianProxyFactoryBean;
import org.springframework.remoting.httpinvoker.HttpInvokerProxyFactoryBean;
import org.springframework.remoting.rmi.RmiProxyFactoryBean;

import com.zgg.group2.rpcserver.api.RpcService;

@Configuration
public class RpcBundler {
	//RMI
	@Bean
	public RmiProxyFactoryBean rpcService() {
		RmiProxyFactoryBean factory = new RmiProxyFactoryBean();
		//url-  rmi://ip:port/serviceName
		factory.setServiceUrl("rmi://127.0.0.1:1099/rpcService");
		factory.setServiceInterface(RpcService.class);
		return factory;
	}

	//Hessian
//	@Bean
	public HessianProxyFactoryBean rpcHessianService() {
		HessianProxyFactoryBean proxy = new HessianProxyFactoryBean();
		//url-  http://ip:port/finalName/hessianBeanName
		proxy.setServiceUrl("http://127.0.0.1:8080/group2-level1-web-rest/hessian");
		proxy.setServiceInterface(RpcService.class);
		return proxy;
	}

	//Spring HTTP-invoker
//	@Bean
	public HttpInvokerProxyFactoryBean rpcInvokerService() {
		HttpInvokerProxyFactoryBean proxy = new HttpInvokerProxyFactoryBean();
		//url-  http://ip:port/finalName/invokerBeanName
		proxy.setServiceUrl("http://127.0.0.1:8080/group2-level1-web-rest/invoker");
		proxy.setServiceInterface(RpcService.class);
		return proxy;
	}
	
}
```

### 服务端
```java
import javax.jws.WebParam;

import com.zgg.group2.rpcserver.bean.RPCPojo;

public interface RpcService {
	RPCPojo get();
	RPCPojo post(@WebParam RPCPojo obj);
	RPCPojo put(@WebParam RPCPojo obj);
	RPCPojo delete(@WebParam Integer id);
}
```

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.remoting.caucho.HessianServiceExporter;
import org.springframework.remoting.httpinvoker.HttpInvokerServiceExporter;
import org.springframework.remoting.rmi.RmiServiceExporter;

import com.zgg.group2.rpcserver.api.RpcService;

@Configuration
public class RpcPublisher {

	//RMI
	@Bean
	public RmiServiceExporter exporter(RpcService rpcService) {
		RmiServiceExporter exporter = new RmiServiceExporter();
		exporter.setService(rpcService);
		exporter.setServiceName("rpcService");
		exporter.setServiceInterface(RpcService.class);
		exporter.setRegistryPort(1099);
		return exporter;
	}
	//Hessian
//	@Bean(name="/hessian")
	public HessianServiceExporter hessianExporter(RpcService rpcService) {
		HessianServiceExporter exporter = new HessianServiceExporter();
		exporter.setService(rpcService);
		exporter.setServiceInterface(RpcService.class);
		return exporter;
	}

	//Spring HTTP-invoker
//	@Bean(name="/invoker")
	public HttpInvokerServiceExporter invokerExporter(RpcService rpcService) {
		HttpInvokerServiceExporter exporter = new HttpInvokerServiceExporter();
		exporter.setService(rpcService);
		exporter.setServiceInterface(RpcService.class);
		return exporter;
	}

	//web service
	//spring继承坑无数，不建议使用，读者可对齐自行封装
}
```
