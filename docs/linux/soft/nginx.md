> 系统环境CentOS 7.6

1.执行以下命令，安装 Nginx。

```
yum install -y nginx
```

2.执行以下命令，打开 nginx.conf 文件

```
vim /etc/nginx/nginx.conf
```

3.按 “i” 切换至编辑模式，编辑 nginx.conf 文件

具体配置可参考 [Nginx配置](springBootDemo/deploy/Nginx?id=linux环境下nginx配置例子)

4.按 “Esc”，输入 “:wq”，保存文件并返回

5.执行以下命令启动 Nginx

```
systemctl start nginx
```

6.执行以下命令，设置 Nginx 为开机自启动

```
systemctl enable nginx
```

7.在本地浏览器中访问以下地址，查看 Nginx 服务是否正常运行

```
http://云服务器实例的公网
```

显示如下，则说明 Nginx 安装配置成功

![](../../images/linux/nginx/nginx1.png)

8.其它命令

* systemctl status nginx 查看nginx状态
* systemctl start nginx
* systemctl stop nginx 停止nginx
* systemctl restart nginx 重启nginx
* service nginx restart  重启nginx