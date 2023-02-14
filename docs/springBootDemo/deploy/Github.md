> 解决连接git/github失败问题

## 修改hosts文件

由于github 的dns被污染，通常连接github都会出现失败现象，可以通过修改hosts文件解决

首先通过[Ping.cn](https://www.ping.cn/dns/github.com ':target=_blank') 在检测详情中找到解析时间最短的地址(注意选择运营商)

**修改配置文件**  
在`C:\Windows\System32\drivers\etc`文件夹下修改hosts文件

`
xxx.xxx.xxx.xxx github.com
`

**刷新配置**  
```shell
ipconfig /flushdns
```

## FastGithub(推荐)

github 加速器 [FastGithub](https://github.com/dotnetcore/FastGithub ':target=_blank')
