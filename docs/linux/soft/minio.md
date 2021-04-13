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
