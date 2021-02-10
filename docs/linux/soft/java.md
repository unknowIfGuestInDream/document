> java 版本 1.8.0_171

1. 下载JDK,通过Xftp等工具传输到Linux上。
2. 执行以下命令，新建 JDK 安装目录

```markdown
mkdir /usr/java
```

3. 执行以下命令，将 JDK 源码包解压到指定位置

```markdown
tar xzf jdk-8u221-linux-x64.tar.gz -C /usr/java
```

4. 执行以下命令，打开 profile 文件。

```markdown
vim /etc/profile
```

5. 按 i 切换至编辑模式，在 export PATH USER ... 后另起一行，根据您实际使用的 JDK 版本添加以下内容。

```markdown
export JAVA_HOME=/usr/java/jdk1.8.0_221（您的 JDK 版本）
export CLASSPATH=$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib
export PATH=$JAVA_HOME/bin:$PATH
```

添加完成后，如下图所示：

6. 按 Esc，输入 :wq，保存文件并返回。
7. 执行以下命令，读取环境变量。

```markdown
source /etc/profile
```

8. 执行以下命令，查看 JDK 是否已经安装成功。

```markdown
java -version
```


