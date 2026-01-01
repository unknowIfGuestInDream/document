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

### 补充 Workspace 扩展点

#### org.eclipse.core.resources.filterMatchers

定义资源过滤匹配器，用于过滤工作空间中的资源。

```xml
<extension point="org.eclipse.core.resources.filterMatchers">
   <filterMatcher
      id="com.example.myFilterMatcher"
      name="My Filter Matcher"
      class="com.example.filters.MyFilterMatcher"
      argumentType="string">
   </filterMatcher>
</extension>
```

**用途**:
- 自定义资源过滤规则
- 隐藏特定文件或目录
- 实现复杂的过滤逻辑

#### org.eclipse.core.resources.modelProviders

定义模型提供者，用于管理资源模型。

```xml
<extension point="org.eclipse.core.resources.modelProviders">
   <modelProvider
      class="com.example.models.MyModelProvider">
      <enablement>
         <with variable="projectNature">
            <equals value="com.example.nature"/>
         </with>
      </enablement>
   </modelProvider>
</extension>
```

**用途**:
- 提供资源模型抽象
- 支持团队操作
- 管理资源状态

#### org.eclipse.core.resources.moveDeleteHook

定义移动/删除钩子，用于在资源移动或删除时执行自定义逻辑。

```xml
<extension point="org.eclipse.core.resources.moveDeleteHook">
   <moveDeleteHook
      class="com.example.hooks.MyMoveDeleteHook">
   </moveDeleteHook>
</extension>
```

**Java 实现**:

```java
public class MyMoveDeleteHook implements IMoveDeleteHook {
    
    @Override
    public boolean deleteFile(IResourceTree tree, IFile file,
                             int updateFlags, IProgressMonitor monitor) {
        // 在文件删除前执行自定义逻辑
        System.out.println("准备删除文件: " + file.getName());
        return false; // 返回 false 表示继续默认删除操作
    }
    
    @Override
    public boolean deleteFolder(IResourceTree tree, IFolder folder,
                               int updateFlags, IProgressMonitor monitor) {
        // 在文件夹删除前执行自定义逻辑
        return false;
    }
    
    @Override
    public boolean deleteProject(IResourceTree tree, IProject project,
                                int updateFlags, IProgressMonitor monitor) {
        // 在项目删除前执行自定义逻辑
        return false;
    }
    
    @Override
    public boolean moveFile(IResourceTree tree, IFile source,
                           IFile destination, int updateFlags,
                           IProgressMonitor monitor) {
        // 在文件移动前执行自定义逻辑
        return false;
    }
    
    @Override
    public boolean moveFolder(IResourceTree tree, IFolder source,
                             IFolder destination, int updateFlags,
                             IProgressMonitor monitor) {
        // 在文件夹移动前执行自定义逻辑
        return false;
    }
    
    @Override
    public boolean moveProject(IResourceTree tree, IProject source,
                              IProjectDescription description,
                              int updateFlags, IProgressMonitor monitor) {
        // 在项目移动前执行自定义逻辑
        return false;
    }
}
```

**用途**:
- 拦截资源删除操作
- 拦截资源移动操作
- 实现自定义清理逻辑

#### org.eclipse.core.resources.refreshProviders

定义刷新提供者，用于自动刷新工作空间资源。

```xml
<extension point="org.eclipse.core.resources.refreshProviders">
   <refreshProvider
      name="My Refresh Provider"
      class="com.example.refresh.MyRefreshProvider">
   </refreshProvider>
</extension>
```

**用途**:
- 监控文件系统变化
- 自动刷新工作空间
- 同步外部变更

#### org.eclipse.core.resources.teamHook

定义团队钩子，用于集成版本控制系统。

```xml
<extension point="org.eclipse.core.resources.teamHook">
   <teamHook
      class="com.example.team.MyTeamHook">
   </teamHook>
</extension>
```

**用途**:
- 集成版本控制系统
- 处理团队操作
- 管理资源同步

#### org.eclipse.core.resources.variableResolvers

定义变量解析器，用于解析路径变量。

```xml
<extension point="org.eclipse.core.resources.variableResolvers">
   <variableResolver
      variable="MY_VAR"
      class="com.example.resolvers.MyVariableResolver">
   </variableResolver>
</extension>
```

**Java 实现**:

```java
public class MyVariableResolver implements IStringVariableResolver {
    
    @Override
    public String resolveValue(IStringVariable variable, String argument)
            throws CoreException {
        // 解析变量值
        if ("MY_VAR".equals(variable.getName())) {
            return "/path/to/resource";
        }
        return null;
    }
}
```

**用途**:
- 定义自定义路径变量
- 动态解析资源路径
- 支持可移植项目配置

## Platform Text 扩展点

Platform Text 提供了丰富的文本编辑功能扩展点，用于增强文本编辑器的能力。

### File Buffers

#### org.eclipse.core.filebuffers.annotationModelCreation

定义注解模型创建器，用于为文件缓冲区创建注解模型。

```xml
<extension point="org.eclipse.core.filebuffers.annotationModelCreation">
   <factory
      class="com.example.text.MyAnnotationModelFactory"
      contentTypeId="org.eclipse.core.runtime.text">
   </factory>
</extension>
```

**用途**:
- 创建自定义注解模型
- 管理文档注解
- 支持错误标记显示

#### org.eclipse.core.filebuffers.documentCreation

定义文档创建器，用于创建特定类型的文档。

```xml
<extension point="org.eclipse.core.filebuffers.documentCreation">
   <factory
      class="com.example.text.MyDocumentFactory"
      contentTypeId="com.example.myContentType">
   </factory>
</extension>
```

**用途**:
- 创建自定义文档类型
- 支持特殊文档格式
- 实现文档初始化逻辑

#### org.eclipse.core.filebuffers.documentSetup

定义文档设置参与者，用于配置文档属性。

```xml
<extension point="org.eclipse.core.filebuffers.documentSetup">
   <participant
      class="com.example.text.MyDocumentSetupParticipant"
      contentTypeId="com.example.myContentType">
   </participant>
</extension>
```

**用途**:
- 配置文档分区
- 设置文档属性
- 初始化文档结构

### Editors

#### org.eclipse.ui.editors.annotationTypes

定义注解类型，用于在编辑器中显示特定类型的注解。

```xml
<extension point="org.eclipse.ui.editors.annotationTypes">
   <type
      name="com.example.myAnnotation"
      super="org.eclipse.ui.workbench.texteditor.error"
      markerType="com.example.myMarker"
      markerSeverity="2">
   </type>
</extension>
```

**用途**:
- 定义错误、警告、信息注解
- 关联标记类型
- 配置注解显示

#### org.eclipse.ui.editors.documentProviders

定义文档提供者，用于管理编辑器文档。

```xml
<extension point="org.eclipse.ui.editors.documentProviders">
   <provider
      class="com.example.editors.MyDocumentProvider"
      extensions="myext">
   </provider>
</extension>
```

**用途**:
- 提供文档内容
- 管理文档持久化
- 处理文档保存

#### org.eclipse.ui.editors.markerAnnotationSpecification

定义标记注解规范，用于配置标记在编辑器中的显示。

```xml
<extension point="org.eclipse.ui.editors.markerAnnotationSpecification">
   <specification
      annotationType="com.example.myAnnotation"
      label="My Annotation"
      icon="icons/marker.png"
      textPreferenceKey="myAnnotationText"
      textPreferenceValue="true"
      highlightPreferenceKey="myAnnotationHighlight"
      highlightPreferenceValue="false"
      colorPreferenceKey="myAnnotationColor"
      colorPreferenceValue="255,0,0"
      presentationLayer="5"
      overviewRulerPreferenceKey="myAnnotationOverview"
      overviewRulerPreferenceValue="true"
      verticalRulerPreferenceKey="myAnnotationRuler"
      verticalRulerPreferenceValue="true">
   </specification>
</extension>
```

**用途**:
- 配置注解显示样式
- 设置注解颜色和图标
- 控制注解在标尺中的显示

#### org.eclipse.ui.editors.markerUpdaters

定义标记更新器，用于在文档变更时更新标记位置。

```xml
<extension point="org.eclipse.ui.editors.markerUpdaters">
   <updater
      class="com.example.editors.MyMarkerUpdater"
      markerType="com.example.myMarker">
   </updater>
</extension>
```

**用途**:
- 更新标记位置
- 处理文档编辑
- 保持标记同步

#### org.eclipse.ui.editors.templates

定义代码模板，用于快速插入常用代码片段。

```xml
<extension point="org.eclipse.ui.editors.templates">
   <contextType
      id="com.example.templates.context"
      name="My Template Context"
      class="com.example.templates.MyContextType">
   </contextType>
   <template
      id="com.example.template1"
      name="My Template"
      description="Insert my code template"
      contextTypeId="com.example.templates.context"
      pattern="public class ${className} {&#x0A;    ${cursor}&#x0A;}">
   </template>
</extension>
```

**用途**:
- 提供代码片段
- 支持模板变量
- 加速代码编写

### Generic Editor

#### org.eclipse.ui.genericeditor.autoEditStrategies

定义自动编辑策略，用于在输入时自动格式化代码。

```xml
<extension point="org.eclipse.ui.genericeditor.autoEditStrategies">
   <autoEditStrategy
      class="com.example.editor.MyAutoEditStrategy"
      contentType="com.example.myContentType">
   </autoEditStrategy>
</extension>
```

**用途**:
- 自动缩进
- 自动闭合括号
- 智能换行

#### org.eclipse.ui.genericeditor.characterPairMatchers

定义字符配对匹配器，用于高亮显示配对的字符。

```xml
<extension point="org.eclipse.ui.genericeditor.characterPairMatchers">
   <characterPairMatcher
      class="com.example.editor.MyCharacterPairMatcher"
      contentType="com.example.myContentType">
   </characterPairMatcher>
</extension>
```

**用途**:
- 高亮配对括号
- 支持跳转到匹配字符
- 提供括号匹配提示

#### org.eclipse.ui.genericeditor.contentAssistProcessors

定义内容辅助处理器，用于提供代码补全建议。

```xml
<extension point="org.eclipse.ui.genericeditor.contentAssistProcessors">
   <contentAssistProcessor
      class="com.example.editor.MyContentAssistProcessor"
      contentType="com.example.myContentType">
   </contentAssistProcessor>
</extension>
```

**Java 实现**:

```java
public class MyContentAssistProcessor implements IContentAssistProcessor {
    
    @Override
    public ICompletionProposal[] computeCompletionProposals(
            ITextViewer viewer, int offset) {
        List<ICompletionProposal> proposals = new ArrayList<>();
        
        // 添加补全建议
        proposals.add(new CompletionProposal(
            "public", offset, 0, 6,
            null, "public", null, "Public modifier"
        ));
        
        return proposals.toArray(new ICompletionProposal[0]);
    }
    
    @Override
    public IContextInformation[] computeContextInformation(
            ITextViewer viewer, int offset) {
        return null;
    }
    
    @Override
    public char[] getCompletionProposalAutoActivationCharacters() {
        return new char[] { '.' };
    }
    
    @Override
    public char[] getContextInformationAutoActivationCharacters() {
        return null;
    }
    
    @Override
    public String getErrorMessage() {
        return null;
    }
    
    @Override
    public IContextInformationValidator getContextInformationValidator() {
        return null;
    }
}
```

**用途**:
- 提供代码补全
- 智能提示
- 上下文感知建议

#### org.eclipse.ui.genericeditor.foldingReconcilers

定义折叠调节器，用于支持代码折叠功能。

```xml
<extension point="org.eclipse.ui.genericeditor.foldingReconcilers">
   <foldingReconciler
      class="com.example.editor.MyFoldingReconciler"
      contentType="com.example.myContentType">
   </foldingReconciler>
</extension>
```

**用途**:
- 实现代码折叠
- 定义折叠区域
- 改善大文件阅读体验

#### org.eclipse.ui.genericeditor.highlightReconcilers

定义高亮调节器，用于语法高亮。

```xml
<extension point="org.eclipse.ui.genericeditor.highlightReconcilers">
   <highlightReconciler
      class="com.example.editor.MyHighlightReconciler"
      contentType="com.example.myContentType">
   </highlightReconciler>
</extension>
```

**用途**:
- 实现语法高亮
- 高亮显示关键字
- 提供视觉反馈

#### org.eclipse.ui.genericeditor.hoverProviders

定义悬停提供者，用于显示悬停提示信息。

```xml
<extension point="org.eclipse.ui.genericeditor.hoverProviders">
   <hoverProvider
      class="com.example.editor.MyHoverProvider"
      contentType="com.example.myContentType">
   </hoverProvider>
</extension>
```

**用途**:
- 显示文档提示
- 提供快速信息
- 显示错误详情

#### org.eclipse.ui.genericeditor.icons

定义图标提供者，用于在编辑器中显示图标。

```xml
<extension point="org.eclipse.ui.genericeditor.icons">
   <icon
      class="com.example.editor.MyIconProvider"
      contentType="com.example.myContentType">
   </icon>
</extension>
```

**用途**:
- 在编辑器标尺显示图标
- 标识特殊行
- 提供视觉标记

#### org.eclipse.ui.genericeditor.presentationReconcilers

定义呈现调节器，用于管理文本样式。

```xml
<extension point="org.eclipse.ui.genericeditor.presentationReconcilers">
   <presentationReconciler
      class="com.example.editor.MyPresentationReconciler"
      contentType="com.example.myContentType">
   </presentationReconciler>
</extension>
```

**用途**:
- 管理文本样式
- 实现语法着色
- 配置文本显示

#### org.eclipse.ui.genericeditor.reconcilers

定义调节器，用于后台分析文档。

```xml
<extension point="org.eclipse.ui.genericeditor.reconcilers">
   <reconciler
      class="com.example.editor.MyReconciler"
      contentType="com.example.myContentType">
   </reconciler>
</extension>
```

**用途**:
- 后台语法检查
- 实时错误检测
- 增量分析

#### org.eclipse.ui.genericeditor.quickAssistProcessors

定义快速辅助处理器，用于提供快速修复建议。

```xml
<extension point="org.eclipse.ui.genericeditor.quickAssistProcessors">
   <quickAssistProcessor
      class="com.example.editor.MyQuickAssistProcessor"
      contentType="com.example.myContentType">
   </quickAssistProcessor>
</extension>
```

**用途**:
- 提供快速修复
- 代码重构建议
- 自动修正错误

#### org.eclipse.ui.genericeditor.textDoubleClickStrategies

定义双击策略，用于自定义双击选择行为。

```xml
<extension point="org.eclipse.ui.genericeditor.textDoubleClickStrategies">
   <textDoubleClickStrategy
      class="com.example.editor.MyDoubleClickStrategy"
      contentType="com.example.myContentType">
   </textDoubleClickStrategy>
</extension>
```

**用途**:
- 自定义双击选择
- 智能选择单词
- 选择语法元素

### Text Editor

#### org.eclipse.ui.workbench.texteditor.codeMiningProviders

定义代码挖掘提供者，用于在编辑器中显示内联提示。

```xml
<extension point="org.eclipse.ui.workbench.texteditor.codeMiningProviders">
   <codeMiningProvider
      class="com.example.editor.MyCodeMiningProvider"
      label="My Code Mining">
      <enabledWhen>
         <with variable="editorInput">
            <adapt type="org.eclipse.core.resources.IFile">
               <test property="org.eclipse.core.resources.extension"
                     value="java"/>
            </adapt>
         </with>
      </enabledWhen>
   </codeMiningProvider>
</extension>
```

**用途**:
- 显示方法引用计数
- 显示参数提示
- 提供内联信息

#### org.eclipse.ui.workbench.texteditor.hyperlinkDetectors

定义超链接检测器，用于在编辑器中创建可点击的链接。

```xml
<extension point="org.eclipse.ui.workbench.texteditor.hyperlinkDetectors">
   <hyperlinkDetector
      id="com.example.hyperlinkDetector"
      name="My Hyperlink Detector"
      class="com.example.editor.MyHyperlinkDetector"
      targetId="com.example.editor">
   </hyperlinkDetector>
</extension>
```

**用途**:
- 创建导航链接
- 支持跳转到定义
- 打开相关资源

#### org.eclipse.ui.workbench.texteditor.hyperlinkDetectorTargets

定义超链接检测器目标，用于组织超链接检测器。

```xml
<extension point="org.eclipse.ui.workbench.texteditor.hyperlinkDetectorTargets">
   <target
      id="com.example.hyperlinkTarget"
      name="My Hyperlink Target"
      description="Target for my hyperlink detectors">
   </target>
</extension>
```

**用途**:
- 组织超链接检测器
- 定义检测器作用域
- 管理链接类型

#### org.eclipse.ui.workbench.texteditor.rulerColumns

定义标尺列，用于在编辑器标尺中显示自定义列。

```xml
<extension point="org.eclipse.ui.workbench.texteditor.rulerColumns">
   <column
      id="com.example.rulerColumn"
      name="My Ruler Column"
      class="com.example.editor.MyRulerColumn"
      enabled="true"
      global="true"
      includeInMenu="true">
   </column>
</extension>
```

**用途**:
- 显示自定义标尺列
- 添加行号显示
- 提供额外信息栏

#### org.eclipse.ui.workbench.texteditor.quickDiffReferenceProvider

定义快速差异参考提供者，用于显示文档变更。

```xml
<extension point="org.eclipse.ui.workbench.texteditor.quickDiffReferenceProvider">
   <referenceprovider
      id="com.example.quickDiffProvider"
      label="My Quick Diff Provider"
      class="com.example.editor.MyQuickDiffProvider">
   </referenceprovider>
</extension>
```

**用途**:
- 显示文档变更
- 对比原始版本
- 提供差异视图

#### org.eclipse.ui.workbench.texteditor.spellingEngine

定义拼写检查引擎，用于检查文档拼写。

```xml
<extension point="org.eclipse.ui.workbench.texteditor.spellingEngine">
   <spellingEngine
      id="com.example.spellingEngine"
      label="My Spelling Engine"
      class="com.example.editor.MySpellingEngine"
      default="false">
   </spellingEngine>
</extension>
```

**用途**:
- 实现拼写检查
- 提供拼写建议
- 支持自定义字典

## PDE 扩展点

PDE (Plug-in Development Environment) 提供了一系列扩展点，用于扩展插件开发环境的能力。以下是 PDE 的主要扩展点：

### 1. org.eclipse.ui.trace.traceComponents

定义跟踪组件，用于调试和跟踪插件运行。

```xml
<extension point="org.eclipse.ui.trace.traceComponents">
   <component
      id="com.example.trace"
      label="Example Trace Component">
      <bundle
         name="com.example.plugin"
         consumed="false">
      </bundle>
   </component>
</extension>
```

**用途**:
- 启用插件运行时跟踪
- 调试插件行为
- 性能分析和诊断

### 2. org.eclipse.pde.build.fetchFactories

定义获取工厂，用于从版本控制系统获取源代码。

```xml
<extension point="org.eclipse.pde.build.fetchFactories">
   <factory
      id="com.example.fetchFactory"
      class="com.example.build.MyFetchFactory">
   </factory>
</extension>
```

**Java 实现**:

```java
public class MyFetchFactory implements IFetchFactory {
    
    @Override
    public void generateRetrieveElementCall(
            Map<String, Object> entryInfos,
            IPath destination,
            Map<String, Object> buildProperties) {
        // 实现从版本控制系统获取代码的逻辑
        String cvstag = (String) entryInfos.get("tag");
        String cvsroot = (String) entryInfos.get("cvsRoot");
        // ... 获取代码
    }
    
    @Override
    public void generateRetrieveFilesCall(
            Map<String, Object> entryInfos,
            IPath destination,
            String[] files,
            Map<String, Object> buildProperties) {
        // 实现获取特定文件的逻辑
    }
}
```

**用途**:
- 支持自定义版本控制系统
- 自动化构建过程中的代码获取
- 集成企业内部的源代码管理工具

### 3. org.eclipse.pde.core.bundleClasspathResolvers

定义 Bundle 类路径解析器，用于解析和管理插件的类路径。

```xml
<extension point="org.eclipse.pde.core.bundleClasspathResolvers">
   <resolver
      nature="com.example.nature"
      class="com.example.pde.MyClasspathResolver">
   </resolver>
</extension>
```

**Java 实现**:

```java
public class MyClasspathResolver implements IBundleClasspathResolver {
    
    @Override
    public IClasspathEntry[] getAdditionalClasspathEntries(
            BundleDescription bundleDescription,
            IProgressMonitor monitor) {
        List<IClasspathEntry> entries = new ArrayList<>();
        
        // 添加自定义类路径条目
        IPath libraryPath = new Path("/path/to/library.jar");
        IClasspathEntry entry = JavaCore.newLibraryEntry(
            libraryPath,
            null,  // source attachment
            null   // source attachment root
        );
        entries.add(entry);
        
        return entries.toArray(new IClasspathEntry[0]);
    }
}
```

**用途**:
- 解析外部依赖库
- 自定义类路径管理
- 支持特殊的库加载需求

### 4. org.eclipse.pde.core.javadoc

定义 Javadoc 位置，用于关联插件的 API 文档。

```xml
<extension point="org.eclipse.pde.core.javadoc">
   <javadoc
      path="doc/api">
      <plugin id="com.example.plugin"/>
   </javadoc>
</extension>
```

**用途**:
- 提供 API 文档链接
- 改善开发体验
- 支持代码提示和帮助

### 5. org.eclipse.pde.core.pluginClasspathContributors

定义插件类路径贡献者，用于向插件添加额外的类路径条目。

```xml
<extension point="org.eclipse.pde.core.pluginClasspathContributors">
   <contributor
      class="com.example.pde.MyClasspathContributor">
   </contributor>
</extension>
```

**Java 实现**:

```java
public class MyClasspathContributor implements IClasspathContributor {
    
    @Override
    public List<IClasspathEntry> getInitialEntries(
            BundleDescription bundleDescription) {
        List<IClasspathEntry> entries = new ArrayList<>();
        
        // 根据插件配置添加类路径
        String extraLibs = bundleDescription.getUserObject();
        if (extraLibs != null) {
            // 解析并添加额外的库
            IPath path = new Path(extraLibs);
            entries.add(JavaCore.newLibraryEntry(path, null, null));
        }
        
        return entries;
    }
    
    @Override
    public List<IClasspathEntry> getEntriesForDependency(
            BundleDescription project,
            BundleDescription addedDependency) {
        // 为依赖项添加类路径条目
        return Collections.emptyList();
    }
}
```

**用途**:
- 动态添加类路径依赖
- 支持复杂的依赖管理
- 集成第三方库

### 6. org.eclipse.pde.core.source

定义源代码位置，用于关联插件的源代码。

```xml
<extension point="org.eclipse.pde.core.source">
   <location
      path="src">
      <plugin id="com.example.plugin"/>
   </location>
</extension>
```

**用途**:
- 提供源代码调试支持
- 改善开发体验
- 支持源代码浏览

### 7. org.eclipse.pde.core.targetLocations

定义目标平台位置，用于配置插件的运行环境。

```xml
<extension point="org.eclipse.pde.core.targetLocations">
   <location
      id="com.example.targetLocation"
      name="Example Target Location"
      class="com.example.pde.MyTargetLocation">
   </location>
</extension>
```

**Java 实现**:

```java
public class MyTargetLocation extends AbstractBundleContainer {
    
    @Override
    protected TargetBundle[] resolveBundles(
            ITargetDefinition definition,
            IProgressMonitor monitor) throws CoreException {
        List<TargetBundle> bundles = new ArrayList<>();
        
        // 从自定义位置解析 Bundle
        // 例如：从远程仓库、数据库等
        File bundleFile = new File("/path/to/bundle.jar");
        if (bundleFile.exists()) {
            TargetBundle bundle = new TargetBundle(bundleFile);
            bundles.add(bundle);
        }
        
        return bundles.toArray(new TargetBundle[0]);
    }
    
    @Override
    public String getType() {
        return "MyTargetLocation";
    }
    
    @Override
    public String getLocation(boolean resolve) throws CoreException {
        return "/custom/target/location";
    }
}
```

**用途**:
- 自定义目标平台源
- 支持企业内部的插件仓库
- 灵活配置运行环境

### 8. org.eclipse.pde.core.targets

定义目标平台定义，用于配置完整的目标平台。

```xml
<extension point="org.eclipse.pde.core.targets">
   <target
      id="com.example.target"
      name="Example Target"
      definition="targets/example.target">
   </target>
</extension>
```

**目标定义文件示例** (example.target):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<target name="Example Target" sequenceNumber="1">
   <locations>
      <location includeAllPlatforms="false" includeConfigurePhase="false" 
                includeMode="planner" includeSource="true" type="InstallableUnit">
         <unit id="org.eclipse.platform.feature.group" version="0.0.0"/>
         <repository location="https://download.eclipse.org/releases/latest"/>
      </location>
   </locations>
</target>
```

**用途**:
- 预定义目标平台配置
- 标准化开发环境
- 简化项目设置

### 9. org.eclipse.pde.ui.launchShortcuts

定义启动快捷方式，用于快速启动特定类型的应用程序。

```xml
<extension point="org.eclipse.pde.ui.launchShortcuts">
   <shortcut
      id="com.example.launchShortcut"
      class="com.example.ui.MyLaunchShortcut"
      label="Run as My Application"
      icon="icons/launch.png"
      modes="run, debug">
      <contextualLaunch>
         <enablement>
            <with variable="selection">
               <count value="1"/>
               <iterate>
                  <adapt type="org.eclipse.core.resources.IProject">
                     <test property="org.eclipse.core.resources.projectNature"
                           value="com.example.nature"/>
                  </adapt>
               </iterate>
            </with>
         </enablement>
      </contextualLaunch>
   </shortcut>
</extension>
```

**Java 实现**:

```java
public class MyLaunchShortcut implements ILaunchShortcut {
    
    @Override
    public void launch(ISelection selection, String mode) {
        if (selection instanceof IStructuredSelection) {
            IStructuredSelection structuredSelection = (IStructuredSelection) selection;
            Object element = structuredSelection.getFirstElement();
            
            if (element instanceof IProject) {
                launchProject((IProject) element, mode);
            }
        }
    }
    
    @Override
    public void launch(IEditorPart editor, String mode) {
        IFile file = editor.getEditorInput().getAdapter(IFile.class);
        if (file != null) {
            launchProject(file.getProject(), mode);
        }
    }
    
    private void launchProject(IProject project, String mode) {
        try {
            // 创建或获取启动配置
            ILaunchManager manager = DebugPlugin.getDefault().getLaunchManager();
            ILaunchConfigurationType type = manager.getLaunchConfigurationType(
                "com.example.launchConfigType"
            );
            
            ILaunchConfiguration[] configs = manager.getLaunchConfigurations(type);
            ILaunchConfiguration config = null;
            
            // 查找已有配置或创建新配置
            for (ILaunchConfiguration c : configs) {
                if (c.getAttribute("project", "").equals(project.getName())) {
                    config = c;
                    break;
                }
            }
            
            if (config == null) {
                ILaunchConfigurationWorkingCopy workingCopy = type.newInstance(
                    null,
                    manager.generateLaunchConfigurationName(project.getName())
                );
                workingCopy.setAttribute("project", project.getName());
                config = workingCopy.doSave();
            }
            
            // 启动
            DebugUITools.launch(config, mode);
            
        } catch (CoreException e) {
            e.printStackTrace();
        }
    }
}
```

**用途**:
- 提供快速启动入口
- 简化应用程序启动流程
- 改善用户体验

### 10. org.eclipse.pde.ui.newExtension

定义新扩展向导，用于帮助用户创建新的扩展点贡献。

```xml
<extension point="org.eclipse.pde.ui.newExtension">
   <wizard
      id="com.example.newExtensionWizard"
      name="Example Extension"
      icon="icons/extension.png"
      category="com.example.category"
      class="com.example.ui.NewExtensionWizard"
      point="com.example.extensionPoint">
   </wizard>
</extension>
```

**Java 实现**:

```java
public class NewExtensionWizard extends BaseExtensionPointMainPage {
    
    @Override
    public void addPages() {
        addPage(new NewExtensionWizardPage());
    }
    
    class NewExtensionWizardPage extends WizardPage {
        
        private Text nameText;
        private Text classText;
        
        protected NewExtensionWizardPage() {
            super("newExtensionPage");
            setTitle("新建扩展");
            setDescription("创建一个新的扩展点贡献");
        }
        
        @Override
        public void createControl(Composite parent) {
            Composite container = new Composite(parent, SWT.NULL);
            container.setLayout(new GridLayout(2, false));
            
            Label nameLabel = new Label(container, SWT.NULL);
            nameLabel.setText("名称:");
            
            nameText = new Text(container, SWT.BORDER | SWT.SINGLE);
            nameText.setLayoutData(new GridData(GridData.FILL_HORIZONTAL));
            
            Label classLabel = new Label(container, SWT.NULL);
            classLabel.setText("类:");
            
            classText = new Text(container, SWT.BORDER | SWT.SINGLE);
            classText.setLayoutData(new GridData(GridData.FILL_HORIZONTAL));
            
            setControl(container);
        }
    }
    
    @Override
    public boolean performFinish() {
        try {
            // 在 plugin.xml 中添加扩展配置
            IPluginModelBase model = getPluginModel();
            IPluginExtension extension = model.getPluginFactory().createExtension();
            extension.setPoint("com.example.extensionPoint");
            
            IPluginElement element = model.getFactory().createElement(extension);
            element.setName("example");
            element.setAttribute("name", nameText.getText());
            element.setAttribute("class", classText.getText());
            
            extension.add(element);
            model.getPluginBase().add(extension);
            
            return true;
        } catch (CoreException e) {
            e.printStackTrace();
            return false;
        }
    }
}
```

**用途**:
- 简化扩展点使用
- 提供向导式创建流程
- 减少配置错误

## PDE 扩展点使用场景

### 开发工具增强

结合使用多个 PDE 扩展点可以创建强大的开发工具：

```xml
<!-- 完整的 PDE 工具链 -->

<!-- 1. 自定义启动快捷方式 -->
<extension point="org.eclipse.pde.ui.launchShortcuts">
   <shortcut
      id="com.example.launch"
      class="com.example.MyLaunchShortcut"
      label="Run My App"
      modes="run, debug">
   </shortcut>
</extension>

<!-- 2. 类路径贡献 -->
<extension point="org.eclipse.pde.core.pluginClasspathContributors">
   <contributor class="com.example.MyClasspathContributor"/>
</extension>

<!-- 3. 目标平台位置 -->
<extension point="org.eclipse.pde.core.targetLocations">
   <location
      id="com.example.target"
      class="com.example.MyTargetLocation">
   </location>
</extension>

<!-- 4. 扩展向导 -->
<extension point="org.eclipse.pde.ui.newExtension">
   <wizard
      id="com.example.wizard"
      name="New Extension"
      class="com.example.NewExtensionWizard"
      point="com.example.extensionPoint">
   </wizard>
</extension>
```

### 调试和跟踪

```xml
<!-- 启用跟踪支持 -->
<extension point="org.eclipse.ui.trace.traceComponents">
   <component
      id="com.example.trace"
      label="Example Component Trace">
      <bundle name="com.example.plugin">
         <trace option="debug" label="Debug Mode">
            <description>
               启用详细的调试输出
            </description>
         </trace>
         <trace option="performance" label="Performance">
            <description>
               记录性能指标
            </description>
         </trace>
      </bundle>
   </component>
</extension>
```

**使用跟踪选项**:

```java
// 在代码中检查跟踪选项
if (Platform.getDebugOption("com.example.plugin/debug") != null) {
    System.out.println("Debug mode enabled");
}

if (Platform.getDebugOption("com.example.plugin/performance") != null) {
    long startTime = System.currentTimeMillis();
    // 执行操作
    long endTime = System.currentTimeMillis();
    System.out.println("Operation took: " + (endTime - startTime) + "ms");
}
```

## 扩展点使用建议

### 选择合适的扩展点

1. **UI 扩展**: 使用 `org.eclipse.ui.*` 扩展点
2. **资源管理**: 使用 `org.eclipse.core.resources.*` 扩展点
3. **运行时配置**: 使用 `org.eclipse.core.runtime.*` 扩展点
4. **调试支持**: 使用 `org.eclipse.debug.*` 扩展点
5. **帮助系统**: 使用 `org.eclipse.help.*` 扩展点
6. **插件开发**: 使用 `org.eclipse.pde.*` 扩展点

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
