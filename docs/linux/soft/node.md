> node 版本 15.9.0

1. 执行以下命令，下载 Node.js Linux 64位二进制安装包。或者自己从官网下载安装包后通过Xftp等工具上传到服务器。

```
cd /usr/local
wget https://nodejs.org/dist/v15.9.0/node-v15.9.0-linux-x64.tar.gz
```

2. 执行以下命令，解压安装包。

```
tar xvf node-v15.9.0-linux-x64.tar.gz
mv node-v15.9.0-linux-x64 node
```

3. 依次执行以下命令，创建软链接。

```
ln -s /usr/local/node/bin/node /usr/local/bin/node
ln -s /usr/local/node/bin/npm /usr/local/bin/npm
```

成功创建软链接后，即可在云服务器任意目录下使用 node 及 npm 命令。

4. 依次执行以下命令，查看 Node.js 及 npm 版本信息。

```
node -v
npm -v
```