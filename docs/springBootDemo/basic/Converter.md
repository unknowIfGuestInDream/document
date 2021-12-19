> Spring MVC 框架的 Converter<S，T> 是一个可以将一种数据类型转换成另一种数据类型的接口，这里 S 表示源类型，T 表示目标类型。开发者在实际应用中使用框架内置的类型转换器基本上就够了，但有时需要编写具有特定功能的类型转换器。

## 内置的类型转换器

在 Spring MVC 框架中，对于常用的数据类型，开发者无须创建自己的类型转换器，因为 Spring MVC 框架有许多内置的类型转换器用于完成常用的类型转换。Spring MVC 框架提供的内置类型转换包括以下几种类型。

1. 标量转换器

名称 | 作用
----|----
StringToBooleanConverter | 	String 到 boolean 类型转换
ObjectToStringConverter | Object 到 String 转换，调用 toString 方法转换
StringToNumberConverterFactory | String 到数字转换（例如 Integer、Long 等）
NumberToNumberConverterFactory | 数字子类型（基本类型）到数字类型（包装类型）转换
StringToCharacterConverter | String 到 Character 转换，取字符串中的第一个字符
NumberToCharacterConverter | 数字子类型到 Character 转换
CharacterToNumberFactory | Character 到数字子类型转换
StringToEnumConverterFactory | String 到枚举类型转换，通过 Enum.valueOf 将字符串转换为需要的枚举类型
EnumToStringConverter | 枚举类型到 String 转换，返回枚举对象的 name 值
StringToLocaleConverter | String 到 java.util.Locale 转换
PropertiesToStringConverter | java.util.Properties 到 String 转换，默认通过 ISO-8859-1 解码
StringToPropertiesConverter | String 到 java.util.Properties 转换，默认使用 ISO-8859-1 编码

2. 集合、数组相关转换器

名称 | 作用
----|----
ArrayToCollectionConverter | 	任意数组到任意集合（List、Set）转换
CollectionToArrayConverter | 	任意集合到任意数组转换
ArrayToArrayConverter | 	任意数组到任意数组转换
CollectionToCollectionConverter | 	集合之间的类型转换
MapToMapConverter | 	Map之间的类型转换
ArrayToStringConverter | 	任意数组到 String 转换
StringToArrayConverter | 	字符串到数组的转换，默认通过“，”分割，且去除字符串两边的空格（trim）
ArrayToObjectConverter | 	任意数组到 Object 的转换，如果目标类型和源类型兼容，直接返回源对象；否则返回数组的第一个元素并进行类型转换
ObjectToArrayConverter | 	Object 到单元素数组转换
CollectionToStringConverter | 	任意集合（List、Set）到 String 转换
StringToCollectionConverter | 	String 到集合（List、Set）转换，默认通过“，”分割，且去除字符串两边的空格（trim）
CollectionToObjectConverter | 	任意集合到任意 Object 的转换，如果目标类型和源类型兼容，直接返回源对象；否则返回集合的第一个元素并进行类型转换
ObjectToCollectionConverter | 	Object 到单元素集合的类型转换

## 自定义类型转换器

在使用时，必须编写一个实现org.springframework.core.convert.converter.Converter接口的java类。这个接口的声明如下

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

## 示例

场景：

> 例如有一个应用 springMVCDemo03 希望用户在页面表单中输入信息来创建商品信息。当输入“apple，10.58，200”时表示在程序中自动创建一个 new Goods，并将“apple”值自动赋给 goodsname 属性，将“10.58”值自动赋给 goodsprice 属性，将“200”值自动赋给 goodsnumber 属性。

1. 创建实体类

```java
public class GoodsModel {
    private String goodsname;
    private double goodsprice;
    private int goodsnumber;
    // 省略setter和getter方法
}
```

2. 创建控制器类

```java
@Controller
@RequestMapping("/my")
public class ConverterController {
    @RequestMapping("/converter")
    /*
     * 使用@RequestParam
     * ("goods")接收请求参数，然后调用自定义类型转换器GoodsConverter将字符串值转换为GoodsModel的对象gm
     */
    public String myConverter(@RequestParam("goods") GoodsModel gm, Model model) {
        model.addAttribute("goods", gm);
        return "showGoods";
    }
}
```

3. 创建自定义类型转换器类

```java
public class GoodsConverter implements Converter<String, GoodsModel> {
    public GoodsModel convert(String source) {
        // 创建一个Goods实例
        GoodsModel goods = new GoodsModel();
        // 以“，”分隔
        String stringvalues[] = source.split(",");
        if (stringvalues != null && stringvalues.length == 3) {
            // 为Goods实例赋值
            goods.setGoodsname(stringvalues[0]);
            goods.setGoodsprice(Double.parseDouble(stringvalues[1]));
            goods.setGoodsnumber(Integer.parseInt(stringvalues[2]));
            return goods;
        } else {
            throw new IllegalArgumentException(String.format(
                    "类型转换失败， 需要格式'apple, 10.58,200 ',但格式是[% s ] ", source));
        }
    }
}
```

4. 注册类型转换器

```java
@Configuration
public class ResourceConfig implements WebMvcConfigurer {
    /**
     * 添加自定义的Converters和Formatters.
     */
    @Override
    public void addFormatters(FormatterRegistry registry) {
        //添加字符串转换Date的自定义转换器
        registry.addConverter(new GoodsConverter());
    }
}
```

5. 创建相关视图

```html
<form action="${pageContext.request.contextPath}/my/converter" method= "post">
    请输入商品信息（格式为apple, 10.58,200）:
    <input type="text" name="goods" /><br>
    <input type="submit" value="提交" />
</form>
```

## 拓展: Java8时间作为控制层参数

> Springboot项目中在controller层直接使用时间作为参数

### 方法1

```yaml
spring:
  mvc:
    format:
      date: yyyy-MM-dd
      date-time: yyyy-MM-dd HH:mm:ss
      time: HH:mm:ss
```

### 方法2
```java
    @Bean
    public Converter<String, LocalDateTime> localDateTimeConverter() {
        return new Converter<String,LocalDateTime>() {
            @Override
            public LocalDateTime convert(String source) {
                return LocalDateTime.parse(source, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
            }
        };
    }

    @Bean
    public Converter<String, LocalDate> localDateConverter() {
        return new Converter<String, LocalDate>() {
            @Override
            public LocalDate convert(String source) {
                return LocalDate.parse(source, DateTimeFormatter.ofPattern("yyyy-MM-dd"));
            }
        };
    }

    @Bean
    public Converter<String, LocalTime> localTimeConverter() {
        return new Converter<String, LocalTime>() {
            @Override
            public LocalTime convert(String source) {
                return LocalTime.parse(source, DateTimeFormatter.ofPattern("HH:mm:ss"));
            }
        };
    }

    @Bean
    public Converter<String, Date> dateConverter() {
        return new Converter<String, Date>() {
            @Override
            public Date convert(String source) {
                SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                try {
                    return format.parse(source);
                } catch (ParseException e) {
                    throw new RuntimeException(e);
                }
            }
        };
    }
```

!> 上述代码不可以使用lamada简写，会导致springBoot解析失败

### 注意

> [!CAUTION]
> 上面方法结果一样, 直接使用对应类接参即可，注意使用方法1时如果使用了dateConverter即Date类型的自定义消息类型，那么接取值也要符合上述规范，不能使用@DateTimeFormat注解接取其他规范的数据，而方法2则对Date类型无影响  
> 此外，前台Date对象直接往后台传的话会接取失败，最好是符合规范的字符串数据

接参示例：
```java
    @GetMapping("selectDataBaseInfo")
    public Map<String, Object> selectDataBaseInfo(LocalDate date) {
        System.out.println(date);
        return BaseUtils.success();
    }
```
