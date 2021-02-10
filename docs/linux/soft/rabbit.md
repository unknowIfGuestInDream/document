> rabbitmq 版本 3.6.8

1. 安装需要插件

```markdown
yum -y install make gcc gcc-c++ kernel-devel m4 ncurses-devel openssl-devel unixODBC-devel
```

2. 安装erlang

```markdown
yum install erlang
```

安装完成后可以检测是否安装成功，使用如下命令：

```markdown
erl
```

如果安装成功,进入Erlang后可以使用如下命令退出Erlang：

```markdown
q().
```

3. 安装RabbitMQ

首先下载一个RabbitMQ，可以在本地下载上传到服务器，也可以直接下载，命令如下：

```markdown
wget https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.8/rabbitmq-server-3.6.8-1.el7.noarch.rpm
```

然后使用如下命令：

```markdown
rpm --import https://www.rabbitmq.com/rabbitmq-release-signing-key.asc
yum install rabbitmq-server-3.6.8-1.el7.noarch.rpm
rpm -i --nodeps rabbitmq-server-3.6.8-1.el7.noarch.rpm
```

启动RabbitMQ

```markdown
/sbin/service rabbitmq-server start
```

创建用户admin

```markdown
rabbitmqctl add_user admin admin
```

给用户admin授权

```markdown
rabbitmqctl  set_permissions -p "/" admin '.*' '.*' '.*'
```

给用户admin赋予administrator角色

```markdown
rabbitmqctl set_user_tags admin administrator
```

开启RabbitMQ控制台

```markdown
rabbitmq-plugins enable rabbitmq_management
```