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

## 插件

### drawio
[filename](https://cdn.jsdelivr.net/npm/docsify-drawio/test.drawio ':include :type=code')

### docsify-slides
允许您编写类似于幻灯片的文档

如果想默认隐藏 docsify 侧边栏，只需在 index.html 中的主体标签中添加 class="close"即可。
```html
<body class="close">...</body>
```

### docsify-accordion
使用手风琴的插件  

以 +（空格）开头，以 （空格）+ 结尾（空格很重要）会将列表转换为折叠式

```markdown

# FAQ Section

Introduction text for the FAQ page.

+ Question 1? +

  Answer 1

+ Question 2? +

  Answer 2

```

#### FAQ Section

Introduction text for the FAQ page.

+ Question 1? +

  Answer 1

+ Question 2? +

  Answer 2

### docsify-terminal-block
为您的文档添加漂亮的接线端子。它也具有 复制到剪贴板 功能。

 ```terminal
    npm run start
    $|npm run start
    $|warning|npm run build
    >|info|npm run start
     |...
    >|error|npm run start
    >|success|npm run start

    warning|npm run build
```

## 参考网站
[Document](https://www.tlcsdm.com/ ':target=_blank')  
[mall-learning](http://www.macrozheng.com/ ':target=_blank')  
[hashiqube](https://github.com/star3am/hashiqube ':target=_blank')
