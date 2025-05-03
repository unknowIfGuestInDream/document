> centos下利用mail命令进行邮件发送

安装mail
```shell
yum install mailx -y 
```

配置mail
```shell
vim /etc/mail.rc
```
#末尾添加发送者邮件地址
```shell
set from=xxxxx@qq.com
set smtp=smtp.qq.com
set smtp-auth-user=xxxxx@qq.com
set smtp-auth-password=邮箱密码 #邮箱密码使用SMTP授权码
set smtp-auth=login
```
重启服务
```shell
systemctl restart postfix.service
```
测试发送信息
```shell
echo "hello world" | mail -s "testmail"  xxxxxxxx@139.com
```