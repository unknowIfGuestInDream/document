# OSGi Service

## 什么是 OSGi Service

OSGi (Open Service Gateway initiative) Service 是 OSGi 框架提供的一种面向服务的架构(SOA)机制。它允许 Bundle（OSGi 中的模块单元）通过服务注册表来发布、查找和使用服务，实现了模块之间的松耦合。

### OSGi 核心概念

- **Bundle**: OSGi 中的模块单元，相当于一个 jar 包加上元数据
- **Service**: Bundle 对外提供的功能接口
- **Service Registry**: 服务注册表，管理所有已注册的服务
- **Bundle Context**: Bundle 与 OSGi 框架交互的上下文对象

## OSGi Service 的生命周期

```
注册服务 -> 服务可用 -> 使用服务 -> 注销服务
   ↓          ↓           ↓          ↓
REGISTERED  AVAILABLE   IN_USE   UNREGISTERED
```

### 服务状态说明

1. **REGISTERED**: 服务已注册到服务注册表
2. **AVAILABLE**: 服务可以被其他 Bundle 获取
3. **IN_USE**: 服务正在被使用
4. **UNREGISTERED**: 服务已从注册表中移除

## 定义服务接口

### 1. 创建服务接口

```java
package com.example.service;

/**
 * 日志服务接口
 */
public interface ILogService {
    
    /**
     * 记录信息日志
     */
    void info(String message);
    
    /**
     * 记录警告日志
     */
    void warn(String message);
    
    /**
     * 记录错误日志
     */
    void error(String message, Throwable throwable);
    
    /**
     * 记录调试日志
     */
    void debug(String message);
}
```

### 2. 服务接口的设计原则

- 接口要小而专注，遵循单一职责原则
- 使用纯 Java 接口，不依赖特定实现
- 考虑向后兼容性
- 提供清晰的文档说明

## 注册 OSGi Service

### 方式一：使用 BundleActivator 注册服务

```java
package com.example.service.impl;

import org.osgi.framework.BundleActivator;
import org.osgi.framework.BundleContext;
import org.osgi.framework.ServiceRegistration;
import com.example.service.ILogService;

public class Activator implements BundleActivator {
    
    private ServiceRegistration<ILogService> serviceRegistration;
    
    @Override
    public void start(BundleContext context) throws Exception {
        // 创建服务实例
        ILogService logService = new LogServiceImpl();
        
        // 注册服务
        serviceRegistration = context.registerService(
            ILogService.class,      // 服务接口
            logService,              // 服务实现
            null                     // 服务属性（可选）
        );
        
        System.out.println("LogService registered successfully");
    }
    
    @Override
    public void stop(BundleContext context) throws Exception {
        // 注销服务
        if (serviceRegistration != null) {
            serviceRegistration.unregister();
            serviceRegistration = null;
        }
        
        System.out.println("LogService unregistered");
    }
}
```

### 方式二：使用声明式服务 (Declarative Services)

#### 1. 创建服务实现类

```java
package com.example.service.impl;

import org.osgi.service.component.annotations.Component;
import com.example.service.ILogService;

@Component(
    immediate = true,                          // 立即激活
    service = ILogService.class,               // 声明服务接口
    property = {
        "service.description=Log Service",     // 服务描述
        "service.vendor=Example Company"       // 服务提供商
    }
)
public class LogServiceImpl implements ILogService {
    
    @Override
    public void info(String message) {
        System.out.println("[INFO] " + message);
    }
    
    @Override
    public void warn(String message) {
        System.out.println("[WARN] " + message);
    }
    
    @Override
    public void error(String message, Throwable throwable) {
        System.err.println("[ERROR] " + message);
        if (throwable != null) {
            throwable.printStackTrace();
        }
    }
    
    @Override
    public void debug(String message) {
        System.out.println("[DEBUG] " + message);
    }
}
```

#### 2. 配置 MANIFEST.MF

```
Manifest-Version: 1.0
Bundle-ManifestVersion: 2
Bundle-Name: Log Service Implementation
Bundle-SymbolicName: com.example.service.impl
Bundle-Version: 1.0.0
Bundle-Vendor: Example Company
Bundle-RequiredExecutionEnvironment: JavaSE-1.8
Service-Component: OSGI-INF/*.xml
Import-Package: org.osgi.service.component.annotations,
 com.example.service
```

#### 3. DS 组件描述文件 (OSGI-INF/LogServiceImpl.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<scr:component xmlns:scr="http://www.osgi.org/xmlns/scr/v1.1.0" 
               name="com.example.service.impl.LogServiceImpl">
   <implementation class="com.example.service.impl.LogServiceImpl"/>
   <service>
      <provide interface="com.example.service.ILogService"/>
   </service>
</scr:component>
```

## 获取和使用 OSGi Service

### 方式一：通过 BundleContext 获取服务

```java
package com.example.client;

import org.osgi.framework.BundleActivator;
import org.osgi.framework.BundleContext;
import org.osgi.framework.ServiceReference;
import com.example.service.ILogService;

public class ClientActivator implements BundleActivator {
    
    private ILogService logService;
    
    @Override
    public void start(BundleContext context) throws Exception {
        // 获取服务引用
        ServiceReference<ILogService> serviceRef = 
            context.getServiceReference(ILogService.class);
        
        if (serviceRef != null) {
            // 获取服务实例
            logService = context.getService(serviceRef);
            
            // 使用服务
            if (logService != null) {
                logService.info("Client bundle started");
            }
        } else {
            System.err.println("LogService not found!");
        }
    }
    
    @Override
    public void stop(BundleContext context) throws Exception {
        if (logService != null) {
            logService.info("Client bundle stopping");
            
            // 释放服务引用
            ServiceReference<ILogService> serviceRef = 
                context.getServiceReference(ILogService.class);
            if (serviceRef != null) {
                context.ungetService(serviceRef);
            }
        }
    }
}
```

### 方式二：使用 ServiceTracker

ServiceTracker 可以自动跟踪服务的生命周期，推荐使用。

```java
package com.example.client;

import org.osgi.framework.BundleActivator;
import org.osgi.framework.BundleContext;
import org.osgi.util.tracker.ServiceTracker;
import com.example.service.ILogService;

public class ClientActivator implements BundleActivator {
    
    private ServiceTracker<ILogService, ILogService> serviceTracker;
    
    @Override
    public void start(BundleContext context) throws Exception {
        // 创建服务跟踪器
        serviceTracker = new ServiceTracker<>(
            context,
            ILogService.class,
            null
        );
        
        // 打开跟踪器
        serviceTracker.open();
        
        // 获取服务
        ILogService logService = serviceTracker.getService();
        if (logService != null) {
            logService.info("Client bundle started");
        }
    }
    
    @Override
    public void stop(BundleContext context) throws Exception {
        // 关闭跟踪器
        if (serviceTracker != null) {
            ILogService logService = serviceTracker.getService();
            if (logService != null) {
                logService.info("Client bundle stopping");
            }
            
            serviceTracker.close();
            serviceTracker = null;
        }
    }
}
```

### 方式三：使用声明式服务注入

这是推荐的方式，由框架自动管理服务依赖。

```java
package com.example.client;

import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Reference;
import org.osgi.service.component.annotations.ReferenceCardinality;
import org.osgi.service.component.annotations.ReferencePolicy;
import com.example.service.ILogService;

@Component(immediate = true)
public class LogClient {
    
    private ILogService logService;
    
    /**
     * 注入日志服务
     * 当服务可用时自动调用
     */
    @Reference(
        cardinality = ReferenceCardinality.MANDATORY,  // 必需的依赖
        policy = ReferencePolicy.STATIC                // 静态策略
    )
    public void setLogService(ILogService logService) {
        this.logService = logService;
        this.logService.info("LogService injected successfully");
    }
    
    /**
     * 服务被移除时调用
     */
    public void unsetLogService(ILogService logService) {
        if (this.logService == logService) {
            this.logService.info("LogService is being removed");
            this.logService = null;
        }
    }
    
    /**
     * 使用服务
     */
    public void doWork() {
        if (logService != null) {
            logService.info("Doing some work...");
        }
    }
}
```

## 服务属性

服务可以携带属性信息，用于服务的过滤和选择。

### 注册带属性的服务

```java
// 方式一：使用 BundleActivator
Dictionary<String, Object> properties = new Hashtable<>();
properties.put("service.description", "Log Service Implementation");
properties.put("service.vendor", "Example Company");
properties.put("log.level", "DEBUG");

serviceRegistration = context.registerService(
    ILogService.class,
    new LogServiceImpl(),
    properties
);

// 方式二：使用声明式服务注解
@Component(
    service = ILogService.class,
    property = {
        "service.description=Log Service Implementation",
        "service.vendor=Example Company",
        "log.level=DEBUG"
    }
)
public class LogServiceImpl implements ILogService {
    // 实现代码
}
```

### 根据属性过滤服务

```java
// 使用 LDAP 过滤器语法
String filter = "(&(objectClass=" + ILogService.class.getName() + ")" +
                 "(log.level=DEBUG))";

ServiceReference<?>[] refs = context.getServiceReferences(
    ILogService.class.getName(),
    filter
);

if (refs != null && refs.length > 0) {
    ILogService service = (ILogService) context.getService(refs[0]);
    // 使用服务
}
```

### 在声明式服务中使用过滤器

```java
@Reference(
    target = "(log.level=DEBUG)"  // 只注入 log.level=DEBUG 的服务
)
public void setLogService(ILogService logService) {
    this.logService = logService;
}
```

## 服务的动态性

OSGi 服务支持动态注册和注销，需要正确处理服务的动态性。

### 处理服务动态变化

```java
import org.osgi.util.tracker.ServiceTracker;
import org.osgi.util.tracker.ServiceTrackerCustomizer;

public class DynamicLogClient implements ServiceTrackerCustomizer<ILogService, ILogService> {
    
    private BundleContext context;
    private ServiceTracker<ILogService, ILogService> tracker;
    
    public DynamicLogClient(BundleContext context) {
        this.context = context;
        this.tracker = new ServiceTracker<>(context, ILogService.class, this);
        this.tracker.open();
    }
    
    @Override
    public ILogService addingService(ServiceReference<ILogService> reference) {
        System.out.println("Service added: " + reference);
        ILogService service = context.getService(reference);
        
        // 服务可用时的处理
        if (service != null) {
            service.info("New LogService is now available");
        }
        
        return service;
    }
    
    @Override
    public void modifiedService(ServiceReference<ILogService> reference, 
                                ILogService service) {
        System.out.println("Service modified: " + reference);
        
        // 服务属性变化时的处理
        if (service != null) {
            service.info("LogService properties modified");
        }
    }
    
    @Override
    public void removedService(ServiceReference<ILogService> reference, 
                              ILogService service) {
        System.out.println("Service removed: " + reference);
        
        // 服务不可用时的处理
        if (service != null) {
            service.info("LogService is being removed");
        }
        
        context.ungetService(reference);
    }
    
    public void shutdown() {
        if (tracker != null) {
            tracker.close();
        }
    }
}
```

## 服务排名

当多个服务实现同一个接口时，可以通过服务排名来指定优先级。

```java
// 注册服务时指定排名
Dictionary<String, Object> properties = new Hashtable<>();
properties.put(Constants.SERVICE_RANKING, 100);  // 排名值，越大优先级越高

context.registerService(
    ILogService.class,
    new LogServiceImpl(),
    properties
);

// 使用声明式服务指定排名
@Component(
    service = ILogService.class,
    property = {
        Constants.SERVICE_RANKING + ":Integer=100"
    }
)
public class LogServiceImpl implements ILogService {
    // 实现代码
}
```

## 最佳实践

### 1. 服务接口设计

- 保持接口简单和专注
- 避免在接口中使用特定实现的类型
- 为接口方法提供清晰的文档
- 考虑接口的版本兼容性

### 2. 服务生命周期管理

- 正确处理服务的注册和注销
- 使用 ServiceTracker 或声明式服务来管理依赖
- 在服务不可用时提供降级方案
- 避免在服务回调中执行耗时操作

### 3. 使用声明式服务

- 优先使用声明式服务而不是 BundleActivator
- 利用依赖注入简化代码
- 使用 @Reference 注解管理服务依赖
- 正确设置服务的生命周期策略

### 4. 服务属性使用

- 使用有意义的属性名
- 遵循 OSGi 服务属性命名规范
- 合理使用过滤器选择服务
- 文档化自定义服务属性

### 5. 错误处理

- 检查服务是否为 null
- 处理服务不可用的情况
- 记录服务相关的异常信息
- 提供服务降级机制

## 常见问题

### 1. 服务循环依赖

避免服务之间的循环依赖，可以通过以下方式解决：

```java
// 使用动态引用策略
@Reference(
    cardinality = ReferenceCardinality.OPTIONAL,
    policy = ReferencePolicy.DYNAMIC
)
public void setDependentService(IDependentService service) {
    this.dependentService = service;
}
```

### 2. 服务获取失败

```java
// 方案一：使用可选依赖
@Reference(
    cardinality = ReferenceCardinality.OPTIONAL
)
public void setLogService(ILogService logService) {
    this.logService = logService;
}

// 方案二：提供默认实现
ILogService logService = tracker.getService();
if (logService == null) {
    logService = new DefaultLogService();  // 使用默认实现
}
```

### 3. 服务版本兼容性

```java
// 在 MANIFEST.MF 中指定版本范围
Import-Package: com.example.service;version="[1.0,2.0)"

// 使用服务属性指定版本
@Component(
    service = ILogService.class,
    property = {
        "service.version=1.0.0"
    }
)
public class LogServiceImpl implements ILogService {
    // 实现代码
}

// 根据版本选择服务
@Reference(
    target = "(service.version=1.0.0)"
)
public void setLogService(ILogService logService) {
    this.logService = logService;
}
```

## 完整示例：服务工厂模式

服务工厂可以为每个使用者创建独立的服务实例。

```java
import org.osgi.framework.Bundle;
import org.osgi.framework.ServiceFactory;
import org.osgi.framework.ServiceRegistration;

public class LogServiceFactory implements ServiceFactory<ILogService> {
    
    @Override
    public ILogService getService(Bundle bundle, 
                                  ServiceRegistration<ILogService> registration) {
        // 为每个 Bundle 创建独立的服务实例
        System.out.println("Creating LogService for bundle: " + bundle.getSymbolicName());
        return new LogServiceImpl(bundle.getSymbolicName());
    }
    
    @Override
    public void ungetService(Bundle bundle, 
                            ServiceRegistration<ILogService> registration, 
                            ILogService service) {
        // 清理服务实例
        System.out.println("Releasing LogService for bundle: " + bundle.getSymbolicName());
        // 执行清理操作
    }
}

// 注册服务工厂
public class Activator implements BundleActivator {
    
    private ServiceRegistration<ILogService> registration;
    
    @Override
    public void start(BundleContext context) throws Exception {
        LogServiceFactory factory = new LogServiceFactory();
        registration = context.registerService(
            ILogService.class,
            factory,
            null
        );
    }
    
    @Override
    public void stop(BundleContext context) throws Exception {
        if (registration != null) {
            registration.unregister();
        }
    }
}
```

## 总结

OSGi Service 是构建模块化应用的核心机制，它提供了：

1. **服务注册表**: 统一的服务管理和查找机制
2. **动态性**: 支持服务的动态注册、查找和注销
3. **版本管理**: 支持同一服务的多个版本共存
4. **解耦**: 服务提供者和消费者之间的松耦合
5. **生命周期管理**: 自动处理服务的生命周期

在 Eclipse RCP 开发中，合理使用 OSGi Service 可以构建出高度模块化、可扩展的应用程序。推荐使用声明式服务来简化开发，提高代码的可维护性。
