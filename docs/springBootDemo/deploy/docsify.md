## docsify介绍
> docsify 可以快速帮你生成文档网站。不同于 GitBook、Hexo 的地方是它不会生成静态的 .html 文件，所有转换工作都是在运行时。如果你想要开始使用它，只需要创建一个 index.html 就可以开始编写文档  
> 官网: [docsify](https://docsify.js.org/ ':target=_blank')

## 安装
参照官网文档

## 部署
推荐部署方式 通过nginx转发, 无需启动docsify项目  

nginx配置:
```
  server {
      listen  80;
      server_name xxx;
      location / {
        alias /usr/local/document/docs/;
        index  index.html;
      }

     include /etc/nginx/default.d/*.conf;
        error_page 404 /404.html;
        location = /404.html {
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
        }
   }
```

## 参考网站
[Document](https://www.tlcsdm.com/ ':target=_blank')  
[mall-learning](http://www.macrozheng.com/ ':target=_blank')
