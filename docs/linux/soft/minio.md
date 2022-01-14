> minio 

1. 下载

进入 /usr/local目录

```
wget https://dl.minio.io/server/minio/release/linux-amd64/minio
```

2. 赋权

```
chmod +x minio
```

3. 后台启动

```
MINIO_ACCESS_KEY=tangliang MINIO_SECRET_KEY=tangliang nohup ./minio server /home/minio/data> /home/minio/minio.log 2>&1 &#
```

4. 非后台启动

```
./minio server /home/minio/data
```

## 实时备份
实时备份通过mc客户端德mirror镜像实现

首先在备份服务器运行一个minio服务端

主服务器安装mc客户端
```shell
wget https://dl.min.io/client/mc/release/linux-amd64/mc
```
赋予执行权限
```javascript
chmod +x mc
```
使用命令给客户端添加一个服务端
```javascript
./mc config host add minio80 http://192.168.51.80:9000 username password --api s3v4
```
查看服务器文件桶
```javascript
./mc ls minio80
```
创建镜像
```javascript
nohup ./mc mirror --overwrite --remove --watch /home/deptthree/data/minioClient/data/ minio80/78file/ &
```
更多参数执行 -h查看
