> Spring的Converter可以将一种类型转换成另一种类型。

在使用时，必须编写一个实现org.springframework.core.convert.converter.Converter接口的java类。这个接口的声明如下

https://blog.csdn.net/liushangzaibeijing/article/details/82493910  
https://www.cnblogs.com/yy3b2007com/p/11757900.html

```java
public interface Converter<S, T> {
    T convert(S var1);
}
```

这里的S表示源类型，T表示目标类型。  
下面展示了一个将String类型转换成Date类型的Converter

```java
public class StringToDateConverter implements Converter<String, Date>{
    private static final Log logger = LogFactory.getLog(StringToDateConverter.class);
    private String datePattern;

    public StringToDateConverter(String datePattern) {
        this.datePattern = datePattern;
    }

    public Date convert(String s) {
        try {
            SimpleDateFormat dateFormat = new SimpleDateFormat(datePattern);
            dateFormat.setLenient(false);
            return dateFormat.parse(s);
        } catch (ParseException e) {
            throw new IllegalArgumentException("invalid date format. Please use this pattern\"" + datePattern + "\"");
        }
    }
}
```

Formatter和Converter一样，也是将一种类型转换成另一种类型。但是，Formatter的源类型必须是一个String。  
在使用时，必须编写一个实现org.springframework.format.Formatter接口的java类。这个接口的声明如下

```java
public interface Formatter<T> extends Printer<T>, Parser<T> {
}
public interface Printer<T> {
    String print(T var1, Locale var2);
}
public interface Parser<T> {
    T parse(String var1, Locale var2) throws ParseException;
}
```

这里的T表示输入字符串要转换的目标类型。  
parse方法利用指定的Locale将一个String解析成目标类型。print方法相反，它是返回目标对象的字符串表示法。  
下面展示了一个将String类型转换成Date类型的Formatter  
```java
public class DateFormatter implements Formatter<Date>{
    private String datePattern;
    private SimpleDateFormat dateFormat;

    public DateFormatter(String datePattern) {
        this.dateFormat = dateFormat;
        dateFormat = new SimpleDateFormat(datePattern);
        dateFormat.setLenient(false);
    }
    public Date parse(String s, Locale locale) throws ParseException {
        try {
            SimpleDateFormat dateFormat = new SimpleDateFormat(datePattern);
            dateFormat.setLenient(false);
            return dateFormat.parse(s);
        } catch (ParseException e) {
            throw new IllegalArgumentException("invalid date format. Please use this pattern\"" + datePattern + "\"");
        }
    }

    public String print(Date date, Locale locale) {
        return dateFormat.format(date);
    }
}
```

选择Converter还是Formatter

Converter是一般工具，可以将一种类型转换成另一种类型。例如，将String转换成Date，或者将Long转换成Date。Converter既可以用在web层，也可以用在其它层中。
Formatter只能将String转成成另一种java类型。例如，将String转换成Date，但它不能将Long转换成Date。所以，Formatter适用于web层。为此，在Spring MVC应用程序中，选择Formatter比选择Converter更合适。

配置一(推荐)

```java
@Configuration
public class ResourceConfig implements WebMvcConfigurer {
    /**
     * 添加自定义的Converters和Formatters.
     */
    @Override
    public void addFormatters(FormatterRegistry registry) {
        //添加字符串转换list的自定义转换器
        registry.addFormatter(new DateFormatter());
        //添加字符串转换Date的自定义转换器
        registry.addConverter(new StringToDateConverter());
    }
}
```

使用该方式会破坏SpringBoot默认加载静态文件的默认配置，需要重新进行添加. 切记  
配置二

```java
@Configuration
public class WebConfig {

  @Autowired
  private RequestMappingHandlerAdapter requestMappingHandlerAdapter;

  @PostConstruct
  public void addConversionConfig() {
    ConfigurableWebBindingInitializer initializer = (ConfigurableWebBindingInitializer) requestMappingHandlerAdapter
        .getWebBindingInitializer();
    if (initializer.getConversionService() != null) {
      GenericConversionService genericConversionService = (GenericConversionService) initializer.getConversionService();
      genericConversionService.addConverter(new StringToDateConverter());
    }
  }
}
```