## 安装oracle

[oracle安装](https://www.cnblogs.com/xuzhaoyang/p/11264557.html ':target=_blank')

在安装oracle时使用图形化界面时，要登录到linux上

命令修改为

```shell script
export DISPLAY=:0
./runInstaller

```

创建数据库

[数据库创建](https://www.cnblogs.com/xuzhaoyang/p/11265240.html ':target=_blank')

运行以下命令来打开数据库创建图形程序

```shell script
export DISPLAY=:0
dbca
```

