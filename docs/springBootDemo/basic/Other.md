## springBoot设置启动样式

将自己的启动样式文件banner.txt放入默认路径resources下。  
如果自定义文件位置&文件名的话 需要修改yml配置：
```yaml
spring
  banner:
    location: static/public/banner.txt
```

## springBoot设置时区

```yaml
spring
  jackson:
    date-format: yyyy/MM/dd HH:mm:ss
    time-zone: GMT+8
```