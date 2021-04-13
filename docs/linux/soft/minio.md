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
MINIO_ACCESS_KEY=myminioadmin MINIO_SECRET_KEY=myminioadmin nohup ./minio server --config-dir /usr/software/minio/config /usr/software/minio/data>  /usr/software/minio/minio.log 2>&1 &#
```
