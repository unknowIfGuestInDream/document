> 在项目的维护过程中，我们通常会在应用中加入短信或者邮件预警功能，比如当应用出现异常宕机时应该及时地将预警信息发送给运维或者开发人员，本文将介绍如何在Spring Boot中发送邮件。在Spring Boot中发送邮件使用的是Spring提供的org.springframework.mail.javamail.JavaMailSender，其提供了许多简单易用的方法，可发送简单的邮件、HTML格式的邮件、带附件的邮件，并且可以创建邮件模板。

引入依赖:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-mail</artifactId>
</dependency>
```

邮件配置

```yaml
spring:
  mail:
    host: smtp.163.com
    username: 你的账号
    password: 你的密码(邮件开启smtp的密码)
    default-encoding: UTF-8
    properties:
      mail:
        display:
          sendmail: spring-boot-demo
        smtp:
          ssl: true
          auth: true
          starttls:
            enable: true
            required: true
```

邮箱服务器地址:
* QQ smtp.qq.com
* sina smtp.sina.cn
* aliyun smtp.aliyun.com
* 163 smtp.163.com

发送邮件例子： 

```java
import com.tangl.demo.annotation.LogAnno;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;

import javax.mail.internet.MimeMessage;
import java.io.File;
import java.util.Date;

/**
 * @author: TangLiang
 * @date: 2020/8/6 13:37
 * @since: 1.0
 */
@RestController
//@RequestMapping("/email")
@Api(tags = "邮件业务")
public class EmailController {

    @Autowired
    private JavaMailSender jms;
    @Autowired
    private TemplateEngine templateEngine;
    @Value("${spring.mail.username}")
    private String from;

    @ApiOperation("发送简单邮件")
    @RequestMapping(value = "/sendSimpleEmail", method = RequestMethod.GET)
    @LogAnno(operateType = "发送简单邮件")
    public String sendSimpleEmail() {
        try {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setFrom(from);
            message.setCc(from);//抄送人
            message.setTo("xxx@qq.com"); // 接收地址
            message.setSubject("一封简单的邮件"); // 标题
            message.setText("使用Spring Boot发送简单邮件。"); // 内容
            jms.send(message);
            return "发送成功";
        } catch (Exception e) {
            e.printStackTrace();
            return e.getMessage();
        }
    }

    @ApiOperation("发送HTML格式的邮件")
    @RequestMapping(value = "/sendHtmlEmail", method = RequestMethod.GET)
    @LogAnno(operateType = "发送HTML格式的邮件")
    public String sendHtmlEmail() {
        MimeMessage message = null;
        try {
            message = jms.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true);
            helper.setFrom(from);
            helper.setTo("xxx@qq.com"); // 接收地址
            helper.setSubject("一封HTML格式的邮件"); // 标题
            // 带HTML格式的内容
            StringBuffer sb = new StringBuffer("<p style='color:#6db33f'>使用Spring Boot发送HTML格式邮件。</p>");
            helper.setText(sb.toString(), true);  //true表示发送HTML格式邮件
            jms.send(message);
            return "发送成功";
        } catch (Exception e) {
            e.printStackTrace();
            return e.getMessage();
        }
    }

    @ApiOperation("发送带附件的邮件")
    @RequestMapping(value = "/sendAttachmentsMail", method = RequestMethod.GET)
    @LogAnno(operateType = "发送带附件的邮件")
    public String sendAttachmentsMail() {
        MimeMessage message = null;
        try {
            message = jms.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true);
            helper.setFrom(from);
            helper.setTo("xxx@qq.com"); // 接收地址
            helper.setSubject("一封带附件的邮件"); // 标题
            helper.setText("详情参见附件内容！"); // 内容
            // 传入附件
            FileSystemResource file = new FileSystemResource(new File("E:\\demo.xlsx"));
            helper.addAttachment("测试附件.xlsx", file);
            jms.send(message);
            return "发送成功";
        } catch (Exception e) {
            e.printStackTrace();
            return e.getMessage();
        }
    }

    @ApiOperation("发送带静态资源的邮件")
    @RequestMapping(value = "/sendInlineMail", method = RequestMethod.GET)
    @LogAnno(operateType = "发送带静态资源的邮件")
    public String sendInlineMail() {
        MimeMessage message = null;
        try {
            message = jms.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true);
            helper.setFrom(from);
            helper.setTo("xxx@qq.com"); // 接收地址
            helper.setSubject("一封带静态资源的邮件"); // 标题
            helper.setText("<html><body>博客图：<img src='cid:img'/></body></html>", true); // 内容
            // 传入附件
            FileSystemResource file = new FileSystemResource(new File("C:\\Users\\Public\\Pictures\\Sample Pictures\\Hydrangeas.jpg"));
            helper.addInline("img", file);
            jms.send(message);
            return "发送成功";
        } catch (Exception e) {
            e.printStackTrace();
            return e.getMessage();
        }
    }

    @ApiOperation("发送模板邮件")
    @RequestMapping(value = "/sendTemplateEmail", method = RequestMethod.GET)
    @LogAnno(operateType = "发送模板邮件")
    public String sendTemplateEmail(String id) {
        MimeMessage message = null;
        try {
            message = jms.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true);
            helper.setFrom(from);
            helper.setCc(from);//抄送人
            helper.setTo("xxx@qq.com"); // 接收地址
            helper.setSubject("邮件摸板来信回复"); // 标题
            // 处理邮件模板
            Context context = new Context();
            context.setVariable("id", id);
            context.setVariable("code", "774875");
            String template = templateEngine.process("emailTemplate", context);
            helper.setText(template, true);
            jms.send(message);
            return "发送成功";
        } catch (Exception e) {
            e.printStackTrace();
            return e.getMessage();
        }
    }
}
```

发送模板邮件需要引入模板解析引擎依赖，这个例子中使用的模板解析引擎为Thymeleaf，所以首先引入Thymeleaf依赖：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

yaml配置:

```yaml
spring
  thymeleaf:
    mode: HTML
    encoding: UTF-8
    prefix: classpath:/templates/
    suffix: .html
    cache: false
```

在template目录下创建一个emailTemplate.html模板：

```html
<!DOCTYPE html>
<html lang="zh" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8" />
    <title>模板</title>
</head>

<body>
    您好，您的验证码为{code}，请在两分钟内使用完成操作。
</body>
</html>
```