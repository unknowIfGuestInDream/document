# Eclipse RCP 扩展点描述以及用法

## 什么是扩展点

扩展点(Extension Point)是 Eclipse RCP 中实现松耦合架构的核心机制。它允许插件定义一个可以被其他插件扩展的位置点，实现了插件之间的解耦和灵活扩展。

### 核心概念

- **扩展点(Extension Point)**: 由插件定义的扩展位置，声明了可以被扩展的接口规范
- **扩展(Extension)**: 其他插件对扩展点的具体实现
- **扩展点提供者**: 定义扩展点的插件
- **扩展提供者**: 实现扩展的插件

## 定义扩展点

### 1. 在 plugin.xml 中声明扩展点

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?eclipse version="3.4"?>
<plugin>
   <extension-point 
      id="customView" 
      name="Custom View Extension Point"
      schema="schema/customView.exsd"/>
</plugin>
```

### 2. 定义扩展点的 Schema

在 `schema/customView.exsd` 文件中定义扩展点的结构：

```xml
<?xml version='1.0' encoding='UTF-8'?>
<schema targetNamespace="com.example.rcp" xmlns="http://www.w3.org/2001/XMLSchema">
   <annotation>
      <appinfo>
         <meta.schema plugin="com.example.rcp" 
                      id="customView" 
                      name="Custom View"/>
      </appinfo>
   </annotation>

   <element name="extension">
      <complexType>
         <sequence>
            <element ref="view" minOccurs="1" maxOccurs="unbounded"/>
         </sequence>
         <attribute name="point" type="string" use="required"/>
         <attribute name="id" type="string"/>
         <attribute name="name" type="string"/>
      </complexType>
   </element>

   <element name="view">
      <complexType>
         <attribute name="id" type="string" use="required"/>
         <attribute name="name" type="string" use="required"/>
         <attribute name="class" type="string" use="required">
            <annotation>
               <appinfo>
                  <meta.attribute kind="java" 
                                 basedOn="org.eclipse.ui.part.ViewPart:"/>
               </appinfo>
            </annotation>
         </attribute>
         <attribute name="icon" type="string"/>
      </complexType>
   </element>
</schema>
```

### 3. 扩展点的 Java 接口定义

```java
package com.example.rcp;

public interface ICustomView {
    /**
     * 获取视图的唯一标识
     */
    String getId();
    
    /**
     * 获取视图的显示名称
     */
    String getName();
    
    /**
     * 创建视图内容
     */
    void createPartControl(Composite parent);
}
```

## 使用扩展点

### 1. 在 plugin.xml 中声明扩展

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?eclipse version="3.4"?>
<plugin>
   <extension point="com.example.rcp.customView">
      <view
         id="com.example.myapp.view1"
         name="My Custom View"
         class="com.example.myapp.views.MyView"
         icon="icons/view.png">
      </view>
   </extension>
</plugin>
```

### 2. 实现扩展类

```java
package com.example.myapp.views;

import org.eclipse.swt.widgets.Composite;
import org.eclipse.ui.part.ViewPart;

public class MyView extends ViewPart {
    
    public static final String ID = "com.example.myapp.view1";
    
    @Override
    public void createPartControl(Composite parent) {
        // 创建视图界面
        Label label = new Label(parent, SWT.NONE);
        label.setText("这是我的自定义视图");
    }
    
    @Override
    public void setFocus() {
        // 设置焦点
    }
}
```

## 读取扩展点配置

在扩展点提供者插件中，可以通过以下代码读取所有的扩展：

```java
package com.example.rcp;

import org.eclipse.core.runtime.*;

public class ExtensionReader {
    
    private static final String EXTENSION_POINT_ID = "com.example.rcp.customView";
    
    public static List<ICustomView> loadExtensions() {
        List<ICustomView> views = new ArrayList<>();
        
        IExtensionRegistry registry = Platform.getExtensionRegistry();
        IExtensionPoint extensionPoint = registry.getExtensionPoint(EXTENSION_POINT_ID);
        
        if (extensionPoint != null) {
            IExtension[] extensions = extensionPoint.getExtensions();
            
            for (IExtension extension : extensions) {
                IConfigurationElement[] elements = extension.getConfigurationElements();
                
                for (IConfigurationElement element : elements) {
                    try {
                        if ("view".equals(element.getName())) {
                            String id = element.getAttribute("id");
                            String name = element.getAttribute("name");
                            String icon = element.getAttribute("icon");
                            
                            // 创建可执行扩展
                            Object obj = element.createExecutableExtension("class");
                            if (obj instanceof ICustomView) {
                                views.add((ICustomView) obj);
                            }
                        }
                    } catch (CoreException e) {
                        // 处理异常
                        e.printStackTrace();
                    }
                }
            }
        }
        
        return views;
    }
}
```

## 常用的 Eclipse RCP 扩展点

### 1. org.eclipse.ui.views

定义视图扩展点，用于向工作台添加新的视图。

```xml
<extension point="org.eclipse.ui.views">
   <category
      id="com.example.views"
      name="Example Views">
   </category>
   <view
      id="com.example.views.SampleView"
      name="Sample View"
      icon="icons/sample.gif"
      category="com.example.views"
      class="com.example.views.SampleView">
   </view>
</extension>
```

### 2. org.eclipse.ui.editors

定义编辑器扩展点，用于打开和编辑特定类型的文件。

```xml
<extension point="org.eclipse.ui.editors">
   <editor
      id="com.example.editors.MyEditor"
      name="My Editor"
      icon="icons/editor.gif"
      extensions="myfile"
      class="com.example.editors.MyEditor">
   </editor>
</extension>
```

### 3. org.eclipse.ui.perspectives

定义透视图扩展点，用于创建自定义的工作台布局。

```xml
<extension point="org.eclipse.ui.perspectives">
   <perspective
      id="com.example.perspectives.MyPerspective"
      name="My Perspective"
      icon="icons/perspective.gif"
      class="com.example.perspectives.MyPerspective">
   </perspective>
</extension>
```

### 4. org.eclipse.ui.commands

定义命令扩展点，用于创建可重用的命令。

```xml
<extension point="org.eclipse.ui.commands">
   <command
      id="com.example.commands.myCommand"
      name="My Command"
      description="Execute my custom command"
      categoryId="com.example.commands.category"
      defaultHandler="com.example.handlers.MyHandler">
   </command>
</extension>
```

### 5. org.eclipse.ui.menus

定义菜单扩展点，用于添加菜单项和工具栏按钮。

```xml
<extension point="org.eclipse.ui.menus">
   <menuContribution
      locationURI="menu:org.eclipse.ui.main.menu?after=additions">
      <menu
         id="com.example.menus.sampleMenu"
         label="Sample Menu"
         mnemonic="M">
         <command
            commandId="com.example.commands.myCommand"
            style="push"
            tooltip="Execute My Command">
         </command>
      </menu>
   </menuContribution>
</extension>
```

## Eclipse 平台扩展点

Eclipse 平台提供了丰富的扩展点，可用于扩展平台基础设施的能力。以下是按功能分类的主要扩展点：

### Platform Runtime (平台运行时)

#### 1. org.eclipse.core.contenttype.contentTypes

定义内容类型，用于识别和处理不同类型的内容。

```xml
<extension point="org.eclipse.core.contenttype.contentTypes">
   <content-type
      id="com.example.myContentType"
      name="My Content Type"
      base-type="org.eclipse.core.runtime.text"
      file-extensions="myext"
      priority="high">
   </content-type>
</extension>
```

**用途**: 
- 识别文件类型
- 关联编辑器和查看器
- 提供特定于内容类型的功能

#### 2. org.eclipse.core.runtime.adapters

提供适配器工厂，用于在运行时将对象转换为其他类型。

```xml
<extension point="org.eclipse.core.runtime.adapters">
   <factory
      class="com.example.adapters.MyAdapterFactory"
      adaptableType="com.example.MyClass">
      <adapter type="org.eclipse.ui.model.IWorkbenchAdapter"/>
   </factory>
</extension>
```

**用途**:
- 实现对象类型转换
- 支持接口适配
- 提供动态类型扩展

#### 3. org.eclipse.core.runtime.applications

定义可执行的应用程序入口点。

```xml
<extension point="org.eclipse.core.runtime.applications"
           id="myapp"
           name="My Application">
   <application>
      <run class="com.example.MyApplication"/>
   </application>
</extension>
```

**用途**:
- 定义 Eclipse 应用程序启动入口
- 支持多应用程序配置
- 实现自定义应用程序生命周期

#### 4. org.eclipse.core.runtime.preferences

定义首选项初始化器，用于设置默认首选项值。

```xml
<extension point="org.eclipse.core.runtime.preferences">
   <initializer
      class="com.example.preferences.PreferenceInitializer">
   </initializer>
</extension>
```

**Java 实现**:

```java
public class PreferenceInitializer extends AbstractPreferenceInitializer {
    @Override
    public void initializeDefaultPreferences() {
        IPreferenceStore store = Activator.getDefault().getPreferenceStore();
        store.setDefault("myPreference", "defaultValue");
        store.setDefault("myIntPreference", 100);
        store.setDefault("myBooleanPreference", true);
    }
}
```

**用途**:
- 初始化默认首选项
- 配置应用程序默认设置
- 管理用户配置

#### 5. org.eclipse.core.runtime.products

定义产品配置，用于品牌化和配置 Eclipse 应用程序。

```xml
<extension point="org.eclipse.core.runtime.products"
           id="myproduct">
   <product
      name="My Product"
      application="com.example.myapp"
      description="My Eclipse RCP Product">
      <property
         name="appName"
         value="MyApp"/>
      <property
         name="aboutText"
         value="My Application v1.0"/>
   </product>
</extension>
```

**用途**:
- 定义产品品牌信息
- 配置启动画面和图标
- 设置产品属性

#### 6. org.eclipse.equinox.preferences.preferences

定义首选项范围，用于管理不同级别的首选项存储。

```xml
<extension point="org.eclipse.equinox.preferences.preferences">
   <scope
      name="myScope"
      class="com.example.preferences.MyScopeImpl">
   </scope>
</extension>
```

**用途**:
- 创建自定义首选项范围
- 管理多层次配置
- 实现首选项持久化策略

### Workspace (工作空间)

#### 1. org.eclipse.core.filesystem.filesystems

定义文件系统实现，用于访问不同的存储系统。

```xml
<extension point="org.eclipse.core.filesystem.filesystems">
   <filesystem
      scheme="myfs">
      <run class="com.example.filesystem.MyFileSystem"/>
   </filesystem>
</extension>
```

**用途**:
- 实现自定义文件系统
- 支持远程文件访问
- 集成云存储服务

#### 2. org.eclipse.core.resources.builders

定义增量项目构建器，用于自动化构建过程。

```xml
<extension point="org.eclipse.core.resources.builders"
           id="myBuilder"
           name="My Builder">
   <builder
      hasNature="true">
      <run class="com.example.builders.MyBuilder"/>
   </builder>
</extension>
```

**Java 实现**:

```java
public class MyBuilder extends IncrementalProjectBuilder {
    
    public static final String BUILDER_ID = "com.example.myBuilder";
    
    @Override
    protected IProject[] build(int kind, Map<String, String> args,
                              IProgressMonitor monitor) throws CoreException {
        if (kind == FULL_BUILD) {
            fullBuild(monitor);
        } else {
            IResourceDelta delta = getDelta(getProject());
            if (delta == null) {
                fullBuild(monitor);
            } else {
                incrementalBuild(delta, monitor);
            }
        }
        return null;
    }
    
    private void fullBuild(IProgressMonitor monitor) throws CoreException {
        // 执行完全构建
        getProject().accept(resource -> {
            // 处理资源
            return true;
        });
    }
    
    private void incrementalBuild(IResourceDelta delta, IProgressMonitor monitor)
            throws CoreException {
        // 执行增量构建
        delta.accept(deltaVisitor -> {
            IResource resource = deltaVisitor.getResource();
            // 处理变更的资源
            return true;
        });
    }
}
```

**用途**:
- 实现自动编译
- 代码生成
- 资源验证和处理

#### 3. org.eclipse.core.resources.fileModificationValidator

定义文件修改验证器，用于控制文件修改权限。

```xml
<extension point="org.eclipse.core.resources.fileModificationValidator">
   <validator
      class="com.example.validators.MyFileModificationValidator">
   </validator>
</extension>
```

**用途**:
- 集成版本控制系统
- 实现文件锁定机制
- 验证文件修改权限

#### 4. org.eclipse.core.resources.markers

定义标记类型，用于在资源上显示问题、任务等信息。

```xml
<extension point="org.eclipse.core.resources.markers"
           id="mymarker"
           name="My Marker">
   <super type="org.eclipse.core.resources.problemmarker"/>
   <persistent value="true"/>
   <attribute name="severity"/>
   <attribute name="message"/>
   <attribute name="lineNumber"/>
</extension>
```

**使用示例**:

```java
// 创建标记
IMarker marker = resource.createMarker("com.example.mymarker");
marker.setAttribute(IMarker.SEVERITY, IMarker.SEVERITY_ERROR);
marker.setAttribute(IMarker.MESSAGE, "错误信息");
marker.setAttribute(IMarker.LINE_NUMBER, 10);

// 查找标记
IMarker[] markers = resource.findMarkers(
    "com.example.mymarker",
    true,  // includeSubtypes
    IResource.DEPTH_INFINITE
);
```

**用途**:
- 显示编译错误和警告
- 标记待办任务
- 显示代码问题

#### 5. org.eclipse.core.resources.natures

定义项目性质，用于标识项目类型和关联构建器。

```xml
<extension point="org.eclipse.core.resources.natures"
           id="mynature"
           name="My Nature">
   <runtime>
      <run class="com.example.natures.MyNature"/>
   </runtime>
   <builder id="com.example.myBuilder"/>
</extension>
```

**Java 实现**:

```java
public class MyNature implements IProjectNature {
    
    public static final String NATURE_ID = "com.example.mynature";
    
    private IProject project;
    
    @Override
    public void configure() throws CoreException {
        // 添加构建器
        IProjectDescription desc = project.getDescription();
        ICommand[] commands = desc.getBuildSpec();
        
        for (ICommand command : commands) {
            if (command.getBuilderName().equals(MyBuilder.BUILDER_ID)) {
                return;
            }
        }
        
        ICommand[] newCommands = new ICommand[commands.length + 1];
        System.arraycopy(commands, 0, newCommands, 0, commands.length);
        ICommand command = desc.newCommand();
        command.setBuilderName(MyBuilder.BUILDER_ID);
        newCommands[newCommands.length - 1] = command;
        desc.setBuildSpec(newCommands);
        project.setDescription(desc, null);
    }
    
    @Override
    public void deconfigure() throws CoreException {
        // 移除构建器
    }
    
    @Override
    public IProject getProject() {
        return project;
    }
    
    @Override
    public void setProject(IProject project) {
        this.project = project;
    }
}
```

**用途**:
- 定义项目类型（Java项目、Web项目等）
- 关联特定的构建器
- 配置项目特性

### Debug (调试)

#### org.eclipse.debug.core.launchConfigurationTypes

定义启动配置类型，用于配置和启动应用程序。

```xml
<extension point="org.eclipse.debug.core.launchConfigurationTypes">
   <launchConfigurationType
      id="com.example.launchType"
      name="My Launch Type"
      delegate="com.example.launch.MyLaunchDelegate"
      modes="run, debug"
      public="true">
   </launchConfigurationType>
</extension>
```

**用途**:
- 定义启动配置
- 支持运行和调试模式
- 自定义启动流程

### Help (帮助)

#### org.eclipse.help.toc

定义帮助目录，用于集成在线帮助文档。

```xml
<extension point="org.eclipse.help.toc">
   <toc file="toc.xml" primary="true"/>
</extension>
```

**toc.xml 示例**:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<toc label="My Application Help">
   <topic label="Getting Started" href="html/gettingstarted.html">
      <topic label="Installation" href="html/installation.html"/>
      <topic label="Quick Start" href="html/quickstart.html"/>
   </topic>
   <topic label="User Guide" href="html/userguide.html">
      <topic label="Features" href="html/features.html"/>
      <topic label="Configuration" href="html/configuration.html"/>
   </topic>
</toc>
```

**用途**:
- 提供在线帮助文档
- 组织帮助内容
- 支持搜索和索引

### Team (团队协作)

#### org.eclipse.team.core.repository

定义版本控制仓库提供者。

```xml
<extension point="org.eclipse.team.core.repository">
   <repository
      class="com.example.team.MyRepositoryProvider"
      typeClass="com.example.team.MyRepositoryType"
      id="com.example.repository">
   </repository>
</extension>
```

**用途**:
- 集成版本控制系统（Git、SVN等）
- 实现团队协作功能
- 管理代码仓库

## 扩展点使用建议

### 选择合适的扩展点

1. **UI 扩展**: 使用 `org.eclipse.ui.*` 扩展点
2. **资源管理**: 使用 `org.eclipse.core.resources.*` 扩展点
3. **运行时配置**: 使用 `org.eclipse.core.runtime.*` 扩展点
4. **调试支持**: 使用 `org.eclipse.debug.*` 扩展点
5. **帮助系统**: 使用 `org.eclipse.help.*` 扩展点

### 扩展点组合使用

许多功能需要组合多个扩展点：

```xml
<!-- 完整的项目类型定义 -->
<!-- 1. 定义项目性质 -->
<extension point="org.eclipse.core.resources.natures">
   <runtime>
      <run class="com.example.MyNature"/>
   </runtime>
   <builder id="com.example.myBuilder"/>
</extension>

<!-- 2. 定义构建器 -->
<extension point="org.eclipse.core.resources.builders">
   <builder hasNature="true">
      <run class="com.example.MyBuilder"/>
   </builder>
</extension>

<!-- 3. 定义视图 -->
<extension point="org.eclipse.ui.views">
   <view
      id="com.example.myView"
      name="My View"
      class="com.example.MyView">
   </view>
</extension>

<!-- 4. 定义透视图 -->
<extension point="org.eclipse.ui.perspectives">
   <perspective
      id="com.example.myPerspective"
      name="My Perspective"
      class="com.example.MyPerspective">
   </perspective>
</extension>
```

## 最佳实践

### 1. 扩展点的命名规范

- 使用插件的完全限定名作为前缀，例如：`com.example.rcp.customView`
- 名称要清晰表达扩展点的用途
- 使用小写字母，单词之间使用点号分隔

### 2. Schema 设计原则

- 定义清晰的属性和元素结构
- 为每个属性提供详细的文档说明
- 使用合适的数据类型和约束
- 考虑向后兼容性

### 3. 扩展点的版本管理

- 避免对已发布的扩展点进行破坏性修改
- 如果必须修改，考虑创建新版本的扩展点
- 提供迁移指南和废弃通知

### 4. 错误处理

- 在读取扩展配置时要处理各种异常情况
- 对于无效的扩展配置，应该记录日志但不影响其他扩展
- 提供友好的错误提示信息

### 5. 性能优化

- 延迟加载扩展实现类，只有在真正需要时才调用 `createExecutableExtension()`
- 缓存已读取的扩展配置信息
- 避免在启动时加载所有扩展

## 调试扩展点

### 查看所有注册的扩展点

```java
IExtensionRegistry registry = Platform.getExtensionRegistry();
IExtensionPoint[] extensionPoints = registry.getExtensionPoints();

for (IExtensionPoint point : extensionPoints) {
    System.out.println("Extension Point: " + point.getUniqueIdentifier());
    System.out.println("  Label: " + point.getLabel());
    System.out.println("  Contributor: " + point.getContributor().getName());
}
```

### 查看特定扩展点的所有扩展

```java
String extensionPointId = "com.example.rcp.customView";
IExtensionPoint extensionPoint = registry.getExtensionPoint(extensionPointId);

if (extensionPoint != null) {
    IExtension[] extensions = extensionPoint.getExtensions();
    System.out.println("Found " + extensions.length + " extensions");
    
    for (IExtension extension : extensions) {
        System.out.println("Extension: " + extension.getLabel());
        System.out.println("  From plugin: " + extension.getContributor().getName());
    }
}
```

## 示例：完整的扩展点实现

### 场景：创建一个数据源扩展点

#### 1. 定义数据源接口

```java
public interface IDataSource {
    String getId();
    String getName();
    Connection getConnection() throws SQLException;
    void close();
}
```

#### 2. 在 plugin.xml 中声明扩展点

```xml
<extension-point 
   id="dataSource" 
   name="Data Source Extension Point"
   schema="schema/dataSource.exsd"/>
```

#### 3. 其他插件实现扩展

```xml
<extension point="com.example.rcp.dataSource">
   <dataSource
      id="com.example.mysql"
      name="MySQL Database"
      class="com.example.datasource.MySQLDataSource">
   </dataSource>
</extension>
```

#### 4. 实现类

```java
public class MySQLDataSource implements IDataSource {
    private Connection connection;
    
    @Override
    public String getId() {
        return "com.example.mysql";
    }
    
    @Override
    public String getName() {
        return "MySQL Database";
    }
    
    @Override
    public Connection getConnection() throws SQLException {
        if (connection == null || connection.isClosed()) {
            connection = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/mydb",
                "user", "password"
            );
        }
        return connection;
    }
    
    @Override
    public void close() {
        if (connection != null) {
            try {
                connection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}
```

#### 5. 数据源管理器

```java
public class DataSourceManager {
    private static DataSourceManager instance;
    private Map<String, IDataSource> dataSources;
    
    private DataSourceManager() {
        dataSources = new HashMap<>();
        loadDataSources();
    }
    
    public static DataSourceManager getInstance() {
        if (instance == null) {
            instance = new DataSourceManager();
        }
        return instance;
    }
    
    private void loadDataSources() {
        IExtensionRegistry registry = Platform.getExtensionRegistry();
        IExtensionPoint point = registry.getExtensionPoint(
            "com.example.rcp.dataSource"
        );
        
        if (point != null) {
            IExtension[] extensions = point.getExtensions();
            for (IExtension extension : extensions) {
                IConfigurationElement[] elements = 
                    extension.getConfigurationElements();
                    
                for (IConfigurationElement element : elements) {
                    try {
                        String id = element.getAttribute("id");
                        Object obj = element.createExecutableExtension("class");
                        
                        if (obj instanceof IDataSource) {
                            dataSources.put(id, (IDataSource) obj);
                        }
                    } catch (CoreException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }
    
    public IDataSource getDataSource(String id) {
        return dataSources.get(id);
    }
    
    public Collection<IDataSource> getAllDataSources() {
        return dataSources.values();
    }
}
```

## 总结

扩展点机制是 Eclipse RCP 架构的核心，它提供了：

1. **松耦合**: 扩展点提供者和扩展实现者之间没有直接依赖
2. **可扩展性**: 可以在不修改原有代码的情况下添加新功能
3. **灵活性**: 支持在运行时动态发现和加载扩展
4. **模块化**: 促进了应用的模块化设计

掌握扩展点的定义和使用是开发高质量 Eclipse RCP 应用的关键。
