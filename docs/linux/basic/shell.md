> 超实用shell脚本

好用的Shell脚本分享仓库:  
1. [useful-scripts](https://github.com/oldratlee/useful-scripts ':target=_blank')
2. [doubi](https://github.com/ToyoDAdoubi/doubi ':target=_blank')

## 自动化部署
```shell
#!/bin/bash

# 定义项目目录和代码仓库地址
project_dir="/var/www/myapp"
repo_url="git@github.com:user/myapp.git"

# 拉取最新代码
cd $project_dir
git pull $repo_url

# 安装依赖
npm install

# 修改配置文件
sed -i 's/DATABASE_HOST=localhost/DATABASE_HOST=db.example.com/' .env

# 重启服务
systemctl restart myapp

echo "部署完成！"
```
## 检查url是否可用
```shell
#!/bin/bash  
URL_LIST="www.baidu.com www.agasgf.com"
for URL in $URL_LIST; do
    FAIL_COUNT=0
    for ((i=1;i<=3;i++)); do
        HTTP_CODE=$(curl -o /dev/null --connect-timeout 3 -s -w "%{http_code}" $URL)
        if [ $HTTP_CODE -ne 200 ]; then
            let FAIL_COUNT++
        else
            break
        fi
    done
    if [ $FAIL_COUNT -eq 3 ]; then
        echo "Warning: $URL Access failure!"
    fi
done
```

## 根据 PID 显示进程所有信息
```shell
#! /bin/bash

read -p "请输入要查询的PID: " P

n=`ps -aux| awk '$2~/^'${P}'$/{print $0}'|wc -l`

if [ $n -eq 0 ];then
 echo "该PID不存在！！"
 exit
fi
echo -e "\e[32m--------------------------------\e[0m"
echo "进程PID: ${P}"
echo "进程命令：$(ps -aux| awk '$2~/^'$P'$/{for (i=11;i<=NF;i++) printf("%s ",$i)}')"
echo "进程所属用户: $(ps -aux| awk '$2~/^'$P'$/{print $1}')"
echo "CPU占用率：$(ps -aux| awk '$2~/^'$P'$/{print $3}')%"
echo "内存占用率：$(ps -aux| awk '$2~/^'$P'$/{print $4}')%"
echo "进程开始运行的时间：$(ps -aux| awk '$2~/^'$P'$/{print $9}')"
echo "进程运行的时间：$(ps -aux| awk '$2~/^'$P'$/{print $10}')"
echo "进程状态：$(ps -aux| awk '$2~/^'$P'$/{print $8}')"
echo "进程虚拟内存：$(ps -aux| awk '$2~/^'$P'$/{print $5}')"
echo "进程共享内存：$(ps -aux| awk '$2~/^'$P'$/{print $6}')"
echo -e "\e[32m--------------------------------\e[0m"
```

## 根据进程名显示该进程所有信息
根据输入的程序的名字模糊过滤出所对应的 PID，并显示出详细信息，如果有多个PID，则全部显示  
```shell
#! /bin/bash

read -p "请输入要查询的进程名：" NAME

N=`ps -aux | grep $NAME | grep -v grep | wc -l` ##统计进程总数

if [ $N -le 0 ];then
  echo "该进程名没有运行！"
fi
i=1
while [ $N -gt 0 ]
do
  echo -e "\e[32m***************************************************************\e[0m"
  echo "进程PID: $(ps -aux | grep $NAME | grep -v grep | awk 'NR=='$i'{print $0}'| awk '{print $2}')"
  echo "进程命令：$(ps -aux | grep $NAME | grep -v grep | awk 'NR=='$i'{print $0}'| awk '{for (j=11;j<=NF;j++) printf("%s ",$j)}')"
  echo "进程所属用户: $(ps -aux | grep $NAME | grep -v grep | awk 'NR=='$i'{print $0}'| awk '{print $1}')"
  echo "CPU占用率：$(ps -aux | grep $NAME | grep -v grep | awk 'NR=='$i'{print $0}'| awk '{print $3}')%"
  echo "内存占用率：$(ps -aux | grep $NAME | grep -v grep | awk 'NR=='$i'{print $0}'| awk '{print $4}')%"
  echo "进程开始运行的时间：$(ps -aux | grep $NAME | grep -v grep | awk 'NR=='$i'{print $0}'| awk '{print $9}')"
  echo "进程运行的时间：$(ps -aux | grep $NAME | grep -v grep | awk 'NR=='$i'{print $0}'| awk '{print $10}')"
  echo "进程状态：$(ps -aux | grep $NAME | grep -v grep | awk 'NR=='$i'{print $0}'| awk '{print $8}')"
  echo "进程虚拟内存：$(ps -aux | grep $NAME | grep -v grep | awk 'NR=='$i'{print $0}'| awk '{print $5}')"
  echo "进程共享内存：$(ps -aux | grep $NAME | grep -v grep | awk 'NR=='$i'{print $0}'| awk '{print $6}')"
  echo -e "\e[32m***************************************************************\e[0m"
  let N-- i++
done
```

## 查看 tcp 的连接状态
```shell
#! /bin/bash

#统计不同状态 tcp 连接（除了 LISTEN ）
all_status_tcp=$(netstat -nt | awk 'NR>2 {print $6}' | sort | uniq -c)

#打印各状态 tcp 连接以及连接数
all_tcp=$(netstat -na | awk '/^tcp/ {++S[$NF]};END {for(a in S) print a, S[a]}')


#统计有哪些 IP 地址连接到了本地 80 端口（ipv4）
connect_80_ip=$(netstat -ant| grep -v 'tcp6' | awk '/:80/{split($5,ip,":");++S[ip[1]]}END{for (a in S) print S[a],a}' |sort -n)


#输出前十个连接到了本地 80 端口的 IP 地址（ipv4）
top10_connect_80_ip=$(netstat -ant| grep -v 'tcp6' | awk '/:80/{split($5,ip,":");++S[ip[1]]}END{for (a in S) print S[a],a}' |sort -rn|head -n 10)


echo -e "\e[31m不同状态(除了LISTEN) tcp 连接及连接数为：\e[0m\n${all_status_tcp}"
echo -e "\e[31m各个状态 tcp 连接以及连接数为：\e[0m\n${all_tcp}"
echo -e "\e[31m连接到本地80端口的 IP 地址及连接数为：\e[0m\n${connect_80_ip}"
echo -e "\e[31m前十个连接到本地80端口的 IP 地址及连接数为：\e[0m\n${top10_connect_80_ip}"
```

## 显示系统性能
```shell
#!/bin/bash

#物理内存使用量
mem_used=$(free -m | grep Mem | awk '{print$3}')

#物理内存总量
mem_total=$(free -m | grep Mem | awk '{print$2}')

#cpu核数
cpu_num=$(lscpu  | grep 'CPU(s)' | awk 'NR==1 {print$2}')

#平均负载
load_average=$(uptime  | awk -F : '{print$5}')

#用户态的CPU使用率
cpu_us=$(top -d 1 -n 1 | grep Cpu | awk -F',' '{print $1}' | awk '{print $(NF-1)}')

#内核态的CPU使用率
cpu_sys=$(top -d 1 -n 1 | grep Cpu | awk -F',' '{print $2}' | awk '{print $(NF-1)}')

#等待I/O的CPU使用率
cpu_wa=$(top -d 1 -n 1 | grep Cpu | awk -F',' '{print $5}' | awk '{print $(NF-1)}')

#处理硬中断的CPU使用率
cpu_hi=$(top -d 1 -n 1 | grep Cpu | awk -F',' '{print $6}' | awk '{print $(NF-1)}')

#处理软中断的CPU使用率
cpu_si=$(top -d 1 -n 1 | grep Cpu | awk -F',' '{print $7}'| awk '{print $(NF-1)}')

echo -e "物理内存使用量(M)为：${mem_used}"
echo -e "物理内存总量(M)为：${mem_total}"
echo -e "cpu核数为：${cpu_num}"
echo -e "平均负载为：${load_average}"
echo -e "用户态的CPU使用率为：${cpu_us}"
echo -e "内核态的CPU使用率为：${cpu_sys}"
echo -e "等待I/O的CPU使用率为：${cpu_wa}"
echo -e "处理硬中断的CPU使用率为：${cpu_hi}"
echo -e "处理软中断的CPU使用率为：${cpu_si}"
```

## 一键查看服务器利用率
```shell
#!/bin/bash
function cpu(){
 
 util=$(vmstat | awk '{if(NR==3)print $13+$14}')
 iowait=$(vmstat | awk '{if(NR==3)print $16}')
 echo "CPU -使用率：${util}% ,等待磁盘IO相应使用率：${iowait}:${iowait}%"
 
}
function memory (){
 
 total=`free -m |awk '{if(NR==2)printf "%.1f",$2/1024}'`
    used=`free -m |awk '{if(NR==2) printf "%.1f",($2-$NF)/1024}'`
    available=`free -m |awk '{if(NR==2) printf "%.1f",$NF/1024}'`
    echo "内存 - 总大小: ${total}G , 使用: ${used}G , 剩余: ${available}G"
}
disk(){
 
 fs=$(df -h |awk '/^\/dev/{print $1}')
    for p in $fs; do
        mounted=$(df -h |awk '$1=="'$p'"{print $NF}')
        size=$(df -h |awk '$1=="'$p'"{print $2}')
        used=$(df -h |awk '$1=="'$p'"{print $3}')
        used_percent=$(df -h |awk '$1=="'$p'"{print $5}')
        echo "硬盘 - 挂载点: $mounted , 总大小: $size , 使用: $used , 使用率: $used_percent"
    done
 
}
function tcp_status() {
    summary=$(ss -antp |awk '{status[$1]++}END{for(i in status) printf i":"status[i]" "}')
    echo "TCP连接状态 - $summary"
}
cpu
memory
disk
tcp_status
```

## 找出占用CPU 内存过高的进程
```shell
#!/bin/bash
echo "-------------------CUP占用前10排序--------------------------------"
ps -eo user,pid,pcpu,pmem,args --sort=-pcpu  |head -n 10
echo "-------------------内存占用前10排序--------------------------------"
ps -eo user,pid,pcpu,pmem,args --sort=-pmem  |head -n 10
```

## 查看网卡的实时流量
```shell
#!/bin/bash
eth0=$1
echo  -e    "流量进入--流量传出    "
while true; do
 old_in=$(cat /proc/net/dev |grep $eth0 |awk '{print $2}')
 old_out=$(cat /proc/net/dev |grep $eth0 |awk '{print $10}')
 sleep 1
 new_in=$(cat /proc/net/dev |grep $eth0 |awk '{print $2}')
 new_out=$(cat /proc/net/dev |grep $eth0 |awk '{print $10}')
 in=$(printf "%.1f%s" "$((($new_in-$old_in)/1024))" "KB/s")
 out=$(printf "%.1f%s" "$((($new_out-$old_out)/1024))" "KB/s")
 echo "$in $out"
done
```

## 批量检测网站是否异常并邮件通知
```shell
#!/bin/bash  
URL_LIST="www.baidu.com www.ctnrs.com www.der-matech.net.cn www.der-matech.com.cn www.der-matech.cn www.der-matech.top www.der-matech.org"
for URL in $URL_LIST; do
    FAIL_COUNT=0
    for ((i=1;i<=3;i++)); do
        HTTP_CODE=$(curl -o /dev/null --connect-timeout 3 -s -w "%{http_code}" $URL)
        if [ $HTTP_CODE -eq 200 ]; then
            echo "$URL OK"
            break
        else
            echo "$URL retry $FAIL_COUNT"
            let FAIL_COUNT++
        fi
    done
    if [ $FAIL_COUNT -eq 3 ]; then
        echo "Warning: $URL Access failure!"
  echo "网站$URL坏掉，请及时处理" | mail -s "$URL网站高危" 1794748404@qq.com
    fi
done
```

## Nginx访问日志分析
```shell
#!/bin/bash
# 日志格式: $remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" "$http_x_forwarded_for"
LOG_FILE=$1
echo "统计访问最多的10个IP"
awk '{a[$1]++}END{print "UV:",length(a);for(v in a)print v,a[v]}' $LOG_FILE |sort -k2 -nr |head -10
echo "----------------------"
 
echo "统计时间段访问最多的IP"
awk '$4>="[01/Dec/2018:13:20:25" && $4<="[27/Nov/2018:16:20:49"{a[$1]++}END{for(v in a)print v,a[v]}' $LOG_FILE |sort -k2 -nr|head -10
echo "----------------------"
 
echo "统计访问最多的10个页面"
awk '{a[$7]++}END{print "PV:",length(a);for(v in a){if(a[v]>10)print v,a[v]}}' $LOG_FILE |sort -k2 -nr
echo "----------------------"
 
echo "统计访问页面状态码数量"
awk '{a[$7" "$9]++}END{for(v in a){if(a[v]>5)print v,a[v]}}' $LOG_FILE |sort -k3 -nr
```

## Nginx访问日志自动按天（周、月）切割
```shell
#!/bin/bash
#nginx日志目录
LOG_DIR=/www/server/nginx/logs
#获取到上一天的时间
YESTERDAY_TIME=$(date -d "yesterday" +%F)
#归档日志取时间
LOG_MONTH_DIR=$LOG_DIR/$(date +"%Y-%m")
#归档日志的名称
LOG_FILE_LIST="access.log"
 
for LOG_FILE in $LOG_FILE_LIST; do
    [ ! -d $LOG_MONTH_DIR ] && mkdir -p $LOG_MONTH_DIR
    mv $LOG_DIR/$LOG_FILE $LOG_MONTH_DIR/${LOG_FILE}_${YESTERDAY_TIME}
done
 
kill -USR1 $(cat $LOG_DIR/nginx.pid)
```

## 自动发布Java项目（Tomcat）
```shell
#!/bin/bash
DATE=$(date +%F_%T)
 
TOMCAT_NAME=$1
TOMCAT_DIR=/usr/local/$TOMCAT_NAME
ROOT=$TOMCAT_DIR/webapps/ROOT
 
BACKUP_DIR=/data/backup
WORK_DIR=/tmp
PROJECT_NAME=tomcat-java-demo
 
# 拉取代码
cd $WORK_DIR
if [ ! -d $PROJECT_NAME ]; then
   git clone https://github.com/lizhenliang/tomcat-java-demo
   cd $PROJECT_NAME
else
   cd $PROJECT_NAME
   git pull
fi
 
# 构建
mvn clean package -Dmaven.test.skip=true
if [ $? -ne 0 ]; then
   echo "maven build failure!"
   exit 1
fi
 
# 部署
TOMCAT_PID=$(ps -ef |grep "$TOMCAT_NAME" |egrep -v "grep|$$" |awk 'NR==1{print $2}')
[ -n "$TOMCAT_PID" ] && kill -9 $TOMCAT_PID
[ -d $ROOT ] && mv $ROOT $BACKUP_DIR/${TOMCAT_NAME}_ROOT$DATE
unzip $WORK_DIR/$PROJECT_NAME/target/*.war -d $ROOT
$TOMCAT_DIR/bin/startup.sh
```

## DOS攻击防范（自动屏蔽攻击IP）
```shell
#!/bin/bash
DATE=$(date +%d/%b/%Y:%H:%M)
#nginx日志
LOG_FILE=/usr/local/nginx/logs/demo2.access.log
#分析ip的访问情况
ABNORMAL_IP=$(tail -n5000 $LOG_FILE |grep $DATE |awk '{a[$1]++}END{for(i in a)if(a[i]>10)print i}')
for IP in $ABNORMAL_IP; do
    if [ $(iptables -vnL |grep -c "$IP") -eq 0 ]; then
        iptables -I INPUT -s $IP -j DROP
        echo "$(date +'%F_%T') $IP" >> /tmp/drop_ip.log
    fi
done
```

## 监控系统资源,并发送告警通知
```shell
#!/bin/bash

# 定义监控项和阈值
cpu_threshold=80
mem_threshold=90
disk_threshold=85

# 获取监控数据
cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
mem_usage=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
disk_usage=$(df -h | awk '$NF=="/"{printf "%s", $5}' | sed 's/%//g')

# 判断是否超过阈值并发送告警
if [ $cpu_usage -gt $cpu_threshold ]; then
    echo "CPU使用率超过阈值！" | mail -s "CPU告警" admin@example.com
fi

if [ $mem_usage -gt $mem_threshold ]; then
    echo "内存使用率超过阈值！" | mail -s "内存告警" admin@example.com
fi

if [ $disk_usage -gt $disk_threshold ]; then
    echo "磁盘使用率超过阈值！" | mail -s "磁盘告警" admin@example.com
fi
```