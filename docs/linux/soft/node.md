> node 版本 12.16.2

1. 执行以下命令，下载 Node.js Linux 64位二进制安装包。或者自己从官网下载安装包后通过Xftp等工具上传到服务器。

```markdown
wget https://nodejs.org/dist/v10.16.3/node-v10.16.3-linux-x64.tar.xz
```

2. 执行以下命令，解压安装包。

```markdown
tar xvf node-v10.16.3-linux-x64.tar.xz
```

3. 依次执行以下命令，创建软链接。

```markdown
ln -s /root/node-v10.16.3-linux-x64/bin/node /usr/local/bin/node
ln -s /root/node-v10.16.3-linux-x64/bin/npm /usr/local/bin/npm
```

成功创建软链接后，即可在云服务器任意目录下使用 node 及 npm 命令。

4. 