> 本文主要记录IDEA的一些常用设置, IDEA版本为2019.3.5

## 基本设置

### 常用默认快捷键

快捷键 | 描述
----|----
alt+f7 | 查找方法在哪里调用.变量在哪里被使用
ctrl+shift+f | 全局搜索
ctrl+shift+f | 全局替換
ctrl+f | 当前文件搜索
ctrl+f | 当前文件替換
alt+insert | 生成getter,setter,tostring等
ctrl+d | 复制当前行到下一行
ctrl+alt+l | 代码格式化
ctrl+alt+o | 格式化import引用
alt+enter | 提示可能的操作
ctrl+g | 跳转到指定行

### 配置IDEA运行内存

![](../../images/idea/idea12.png)

Xmx分配2G到3G最佳，根据个人电脑情况决定

### 显示IDEA内存指示

![](../../images/idea/idea13.png)

### 打开IDEA时设置不重新打开最近的项目

> IDEA默认会打开最近的项目，有时候我们需要自己选择要打开的项目，不勾选该选项可以实现。

![](../../images/idea/idea1.png)

### 设置新建类文件的类注释模版

![](../../images/idea/idea2.png)

```markdown
/**
    *@author: ${USER}
    *@date: ${DATE} ${TIME}
    *@since: 1.0
    */
```

其中${USER}可以通过配置IDEA来设置名字 -Duser.name=。

![](../../images/idea/idea3.png)

### 开启IDEA的自动编译（静态）

打开顶部工具栏 File -> Settings -> Default Settings -> Build -> Compiler 然后勾选 Build project automatically 。

![](../../images/idea/idea4.png)

### 开启IDEA的自动编译（动态）

具体步骤：同时按住 Ctrl + Shift + Alt + / 然后进入Registry ，勾选自动编译并调整延时参数。

. compiler.automake.allow.when.app.running -> 自动编译
. compile.document.save.trigger.delay -> 自动更新文件(主要是针对静态文件如JS CSS的更新，将延迟时间减少后，直接按F5刷新页面就能看到效果)

![](../../images/idea/idea5.webp)

### 设置自动显示（鼠标移动显示）方法注释

![](../../images/idea/idea6.png)

### IDEA设置显示中文文档API

首先，我们从网上下载好对应的java最新的中文api文档，chm格式的.  
之后在命令行中使用hh.exe把chm解包，获得html文件 
 
```markdown
hh.exe -decompile javadoc java8.chm
```

在IDEA设置doc文档的路径  

![](../../images/idea/idea7.png)

把鼠标放在String类上或者方法上，显示的结果如下图所示，  

![](../../images/idea/idea8.png)

### 方法分割线

![](../../images/idea/idea9.png)

### 设置格式化代码后多行空行转为一行

![](../../images/idea/idea10.png)

### 自动导入包

![](../../images/idea/idea11.png)

### 快捷键进入全屏或免打扰模式

![](../../images/idea/idea14.png)

设置快捷键 进入免打扰模式，设置自己想要的快捷键

![](../../images/idea/idea15.png)

## IDEA插件

### lombok

> Lombok为Java语言添加了非常有趣的附加功能，你可以不用再为实体类手写getter,setter等方法，通过一个注解即可拥有。

### translation

> 很好用的翻译插件

### CodeGlance

![](../../images/idea/idea_code.png)

### Git Commit Template

> 代码提交模板

![](../../images/idea/idea_git.png)

### gitee

> 配置IDEA集成gitee 

![](../../images/idea/idea_gitee.png)

### Grep console

> 过滤日志、给不同级别的日志或者给不同pattern的日志加上背景颜色与上层颜色

![](../../images/idea/idea_grep.webp)

### Maven Helper

> pom文件位置显示出相关依赖关系，且对于冲突的依赖进行标红，极大方便了排除冲突依赖的工作。