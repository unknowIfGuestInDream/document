> 部署时需要查询PID终止进程，然后重新启动jar，相对较繁琐，可以通过构建shell脚本的方式方便操作

!> 注意：jar 包与shell脚本文件必须在同一目录下

创建脚本gen.sh

```shell
cat > gen.sh
```

然后修改下面的代码并粘贴 APP_NAME改成自己的文件名

```shell
#!/bin/bash

APP_NAME=gen-3.2.jar
 

usage() {
echo "Usage: sh gen.sh [start|stop|restart|status]"
exit 1 
}
 

is_exist() {
pid=`ps -ef | grep $APP_NAME | grep -v grep | awk '{print $2}' `

if [ -z "${pid}" ]
then
 return 1
else
 return 0
fi
}
 

start() {
is_exist
if [ $? -eq "0" ]
then
 echo "${APP_NAME} is already running. pid=${pid} ."
else
 nohup java -jar $APP_NAME > /dev/null 2>&1 &
fi
}
 
#停止方法
stop() {
is_exist
if [ $? -eq "0" ]
then
 kill -9 $pid
else
 echo "${APP_NAME} is not running"
fi
}
 
#输出运行状态
status() {
   is_exist
if [ $? -eq "0" ]
then
     echo "${APP_NAME} is running. Pid is ${pid}"
else
     echo "${APP_NAME} is not running."
fi
}
 
#重启
restart() {
  stop
  start
}
 
#根据输入参数，选择执行对应方法，不输入则执行使用说明
case "$1" in
"start")
start
;;
"stop")
stop
;;
"status")
status
;;
"restart")
restart
;;
*)
usage
;;
esac
```

Ctrl + D 退出

赋权

```shell
chmod u+x gen.sh
```

然后即可使用

```shell
sh gen.sh usage  ## 查看可用命令
sh gen.sh start  ## 启动jar
sh gen.sh stop  ## 停止jar
sh gen.sh restart  ## 重启jar
sh gen.sh status  ## 查看jar包状态
```

