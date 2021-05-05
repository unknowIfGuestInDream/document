> mongodb 版本 4.2.9

https://www.cnblogs.com/hunanzp/p/12297386.html

1、 下载文件或者ftp上传文件

```
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-4.2.3.tgz
```

2、 解压文件

```
tar -zxvf mongodb-linux-x86_64-rhel70-4.2.3.tgz
```

3、 将解压后的目录剪切到一个新目录 mongodb

```
mv mongodb-linux-x86_64-rhel70-4.2.3 mongodb
```

4、 创建数据库目录

到mongodb下新建data/db目录

```
cd mongodb
mkdir -p data/db
```

5、 创建日志目录

在mongodb目录下继续创建子目录log，后续mongodb的日志文件会存储在这目录下。

```
mkdir log
```

6、 创建配置文件目录

还是在mongodb下，我们需要创建一个etc子目录，在子目录下创建mongodb.conf  
重点：mongodb.conf文件非常重要，它的配置如果错误则mongodb启动会失败。

```
mkdir etc
vim ./etc/mongodb.conf
```

在新建的mongodb.conf输入下面内容

```
dbpath=/root/mongodb/data/db  #数据文件存放目录
logpath=/root/mongodb/log/mongodb.log   #日志文件
port=27017   #端口
fork=true    #以守护程序的方式启用，即在后台运行
journal=false
bind_ip=*
```

7、 启动mongodb

在/root/mongodb/bin工作目录下执行下面命令开始启动Mongodb

```
./mongod --config /root/mongodb/etc/mongodb.conf
```


