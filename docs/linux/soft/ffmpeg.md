> Tencent Centos 8

FFmpeg 在默认的CentOS 8 源仓库中没有提供。你可以选择通过源文件编译安装 FFmpeg，或者使用dnf工具从Negativo17源仓库中安装。我们将会使用第二个选项。

完成下面的步骤，在 CentOS 8 上安装 FFmpeg：

1.Negativo17软件源依赖EPEL 和 PowerTools 软件源。以 root 或者其他有 sudo 权限的用户身份运行下面的命令，启用必须的软件源：

```shell
sudo dnf install epel-release
sudo yum config-manager --set-enabled PowerTools
sudo yum-config-manager --add-repo=https://negativo17.org/repos/epel-multimedia.repo
```

2.一旦软件源被启用，安装FFmpeg：

```shell
sudo dnf install ffmpeg
```

3.通过检测版本号，验证FFmpeg安装：

```shell
ffmpeg -version
```