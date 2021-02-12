> Spring Boot中结合Hibernate Validator可以实现优雅的参数校验，而不必在业务代码中写一大堆的参数校验逻辑

引入依赖:

```xml
        <!--参数校验-->
        <dependency>
            <groupId>org.hibernate</groupId>
            <artifactId>hibernate-validator</artifactId>
            <version>5.1.1.Final</version>
        </dependency>
```

## 校验注解

注解 | 描述
----|----
@Null | 限制只能为null
@NotNull | 限制必须不为null
@AssertFalse | 限制必须为false
@AssertTrue | 	限制必须为true
@DecimalMax(value) | 限制必须为一个不大于指定值的数字
@DecimalMin(value) | 限制必须为一个不小于指定值的数字
@Digits(integer,fraction) | 限制必须为一个小数，且整数部分的位数不能超过integer， 小数部分的位数不能超过fraction
@Future | 限制必须是一个将来的日期
@Past | 限制必须是一个过去的日期
@Max(value) | 限制必须为一个不大于指定值的数字
@Min(value) | 限制必须为一个不小于指定值的数字
@Past | 限制必须是一个过去的日期
@Pattern(value) | 限制必须符合指定的正则表达式
@Size(max,min) | 限制字符长度必须在min到max之间
@SafeHtml | 字符串是安全的html
@URL | 字符串是合法的URL
@NotBlank | 字符串必须有字符
@NotEmpty | 字符串不为NULL，集合有字符
@AssertFalse | 必须是false
@AssertTrue | 必须是true

## 示例

新建一个表单实体类，并加上注解：

```java
@Data
public class Demo implements Serializable {

    @NotEmpty(message="用户名不能为空")
    @Length(min=6,max = 12,message="用户名长度必须位于6到12之间")
    private String userName;


    @NotEmpty(message="密码不能为空")
    @Length(min=6,message="密码长度不能小于6位")
    private String passWord;

    @Email(message="请输入正确的邮箱")
    private String email;

    @Pattern(regexp = "^(\\d{18,18}|\\d{15,15}|(\\d{17,17}[x|X]))$", message = "身份证格式错误")
    private String idCard;

}
```

测试控制层：

```java
@RestController
public class TestDemoController {

    @PostMapping("/")
    public String testDemo(@Valid Demo demo,BindingResult bindingResult){
        StringBuffer stringBuffer = new StringBuffer();
        if(bindingResult.hasErrors()){
            List<ObjectError> list =bindingResult.getAllErrors();
            for (ObjectError objectError:list) {
                stringBuffer.append(objectError.getDefaultMessage());
                stringBuffer.append("---");
            }
        }
        return stringBuffer!=null?stringBuffer.toString():"";
    }
}
```

参数添加了@Valid注解，这会告知Spring，需要确保这个对象满足校验限制。  
Errors参数要紧跟在带有@Valid注解的参数后面。  
可以通过postman或者idea的Test Restful Web Service测试。  

## 自定义校验规则

上面的注解都是较为简单的注解，实际编程中校验的规则可能五花八门。当自带的这些注解无法满足我们的需求时，我们也可以自定义校验注解。下面是一个自定义校验注解的基本格式：

```java
import javax.validation.Constraint;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target({ElementType.FIELD, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = MyConstraintValidator.class)
public @interface MyConstraint {

    String message();

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
```

其中@Constraint注解表明这个注解是用于规则校验的，  
validatedBy属性表明用什么去校验，这里我们指定的类为MyConstraintValidator。  
注解还包含了三个书属性，属性message指定当校验不通过的时候提示什么信息。

接下来编写MyConstraintValidator，代码如下所示：

```java
import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

public class MyConstraintValidator implements ConstraintValidator<MyConstraint, Object> {

    @Override
    public void initialize(MyConstraint myConstraint) {
        System.out.println("my validator init");
    }

    @Override
    public boolean isValid(Object o, ConstraintValidatorContext constraintValidatorContext) {
        System.out.println(o);
        return false;
    }
}
```

MyConstraintValidator实现了ConstraintValidator接口，该接口必须指定两个泛型，第一个泛型指的是上面定义的注解类型，第二个泛型表示校验对象的类型。  
MyConstraintValidator实现了ConstraintValidator接口的initialize方法和isValid方法。  
initialize方法用于该校验初始化的时候进行一些操作；isValid方法用于编写校验逻辑，第一个参数为需要校验的值，第二个参数为校验上下文。

## 全局参数校验

这里介绍一种结合全局异常捕获的方式来实现低耦合简洁的参数校验解决方案。

### 方法参数校验

@Validated是@Valid 的一次封装，是Spring提供的校验机制使用。@Valid不提供分组功能

```java
@RestController
@Validated
public class InformationController {
    @GetMapping("/inforOther")
    public String inforOther(@NotNull(message = "名字不能为空") String name, @Max(value = 99, message = "年龄不能大于99岁") Integer age) {
        return "name: " + name + " ,age:" + age;
    }
}
```

使用这种方式参数校验不通过时，会抛出javax.validation.ConstraintViolationException，我们使用全局异常捕获来处理这种异常：

```java
/**
 * @author: TangLiang
 * @date: 2020/9/2 9:14
 * @since: 1.0
 */
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(ValidationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Map handle(ValidationException exception) {
        Map<String, Object> result = new HashMap<>();
        List<Map<String, Object>> list = new ArrayList<>();
        if (exception instanceof ConstraintViolationException) {
            ConstraintViolationException exs = (ConstraintViolationException) exception;

            Set<ConstraintViolation<?>> violations = exs.getConstraintViolations();
            for (ConstraintViolation<?> item : violations) {
                list.add(new HashMap() {
                    {
                        put("message", item.getMessage());
                    }
                });
            }
            //打印验证不通过的信息
            log.error("{}", exception.getLocalizedMessage());
        }
        result.put("result", list);
        result.put("success", false);
        return result;
    }
}
```

### 使用实体传参

```markdown
@GetMapping("test2")
public String test2(@Valid User user) {
    return "success";
}
```

这时候我们需要在GlobalExceptionHandler捕获org.springframework.validation.BindException异常：

```markdown
/**
 * 统一处理请求参数校验(实体对象传参)
 *
 * @param e BindException
 * @return FebsResponse
 */
@ExceptionHandler(BindException.class)
@ResponseStatus(HttpStatus.BAD_REQUEST)
public String validExceptionHandler(BindException e) {
    StringBuilder message = new StringBuilder();
    List<FieldError> fieldErrors = e.getBindingResult().getFieldErrors();
    for (FieldError error : fieldErrors) {
        message.append(error.getField()).append(error.getDefaultMessage()).append(",");
    }
    message = new StringBuilder(message.substring(0, message.length() - 1));
    return message.toString();

}
```


