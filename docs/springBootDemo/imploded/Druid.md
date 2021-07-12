> druid是阿里巴巴开源的数据库连接池，提供了优秀的对数据库操作的监控功能，本文要讲解一下springboot项目怎么集成druid。

本文档主要讲springBoot配置druid多数据源的配置。  
springBoot默认的yml配置适合配置单数据源，如果要配置多数据的话最好手动配置；

**需要引入依赖:**

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!--  druid连接池 -->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
            <version>1.1.9</version>
        </dependency>
        <!--  mysql -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.35</version>
        </dependency>
        <!-- mariadb连接相关依赖-->
        <dependency>
            <groupId>org.mariadb.jdbc</groupId>
            <artifactId>mariadb-java-client</artifactId>
            <version>2.1.2</version>
        </dependency>
        <!-- AOP切面 druid监控需要 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-aop</artifactId>
        </dependency>
```

## 自定义druid配置:  
spring.datasource.master为mysql数据库。  
spring.datasource.cluster为mariddb数据库。  
其中上述两个是自定义配置，而非springBoot配置，只是前缀为spring.datasource，如果要修改前缀的话，则将master与cluster提出来即可。

```yaml
spring:
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource
    master:
      driver-class-name: com.mysql.jdbc.Driver
      url: jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=utf8&useSSL=true&serverTimezone=Asia/Shanghai&autoReconnect=true
      username: root
      password: root
      initialSize: 5
      maxActive: 300
      ## 配置获取连接等待超时的时间
      maxWait: 30000
#      remove-abandoned: true
#      remove-abandoned-timeout: 20
#      log-abandoned: true
      ## 配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒
      timeBetweenEvictionRunsMillis: 60000
      ## 配置一个连接在池中最小生存的时间，单位是毫秒
      minEvictableIdleTimeMillis: 30000
      ## 校验SQL，Oracle配置 spring.datasource.validationQuery=SELECT 1 FROM DUAL，如果不配validationQuery项，则下面三项配置无用
      validationQuery: SELECT 1 FROM DUAL
      testWhileIdle: true
      testOnBorrow: false
      testOnReturn: false
      ## 打开PSCache，并且指定每个连接上PSCache的大小
      poolPreparedStatements: true
      maxPoolPreparedStatementPerConnectionSize: 20
      filters: stat,wall,slf4j
      connectionProperties: druid.stat.mergeSql=true;druid.stat.slowSqlMillis=5000
      useGlobalDataSourceStat: true
    cluster:
      driver-class-name: org.mariadb.jdbc.Driver
      url: jdbc:mariadb://localhost:3307/mall?characterEncoding=utf-8&useSSL=false&useTimezone=true&serverTimezone=GMT%2B8
      username: root
      password: root
      initialSize: 5
      maxActive: 100
      ## 配置获取连接等待超时的时间
      maxWait: 30000
      #超时回收
#      remove-abandoned: true
#      # 超时连接回收时间，单位秒
#      remove-abandoned-timeout: 20
#      # 回收连接时打印日志
#      log-abandoned: true
      ## 配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒
      timeBetweenEvictionRunsMillis: 60000
      ## 配置一个连接在池中最小生存的时间，单位是毫秒
      minEvictableIdleTimeMillis: 30000
      ## 校验SQL，Oracle配置 spring.datasource.validationQuery=SELECT 1 FROM DUAL，如果不配validationQuery项，则下面三项配置无用
      #validationQuery: SELECT 1 FROM DUAL
      testWhileIdle: false
      testOnBorrow: false
      testOnReturn: false
      ## 打开PSCache，并且指定每个连接上PSCache的大小
      poolPreparedStatements: true
      maxPoolPreparedStatementPerConnectionSize: 20
      filters: stat,wall,slf4j
      connectionProperties: druid.stat.mergeSql=true;druid.stat.slowSqlMillis=5000
      useGlobalDataSourceStat: true
    druid:
      aop-patterns: com.tangl.demo.service.* #监听的包 需要根据自己的项目修改
      # 配置StatFilter
      web-stat-filter:
        #默认为false，设置为true启动
        enabled: true
        url-pattern: "/*"
        exclusions: "*.js,*.gif,*.jpg,*.bmp,*.png,*.css,*.ico,/druid/*"
        #配置StatViewServlet
      stat-view-servlet:
        enable: true
        url-pattern: "/druid/*"
        #允许那些ip
        allow:
        login-username: admin
        login-password: aSFAFQAFQVQA_ASDQDZXF259Q416F1SX61AQ21QF
        #禁止那些ip
        deny:
        #是否可以重置
        reset-enable: true
      filter:
        slf4j:
          enabled: true
          statement-create-after-log-enabled: false
          statement-log-enabled: false
          statement-executable-sql-log-enable: true
          statement-log-error-enabled: true
          result-set-log-enabled: false
```

## 多数据源配置

添加DataSourceConfig配置多数据源:

```java
/**
 * @author: TangLiang
 * @date: 2020/7/14 17:16
 * @since: 1.0
 */
@Configuration
public class DataSourceConfig {
    @Primary
    @Bean(name = "dataSource")
    @Qualifier("dataSource")
    @ConfigurationProperties(prefix = "spring.datasource.master")
    public DataSource mpDefault() {
        return new DruidDataSource();
    }

    @Bean(name = "tfJdbcTemplate")
    public JdbcTemplate tfJdbcTemplate(@Qualifier("dataSource") DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

    @Bean(name = "txDataSource")
    @Qualifier("txDataSource")
    @ConfigurationProperties(prefix = "spring.datasource.cluster")
    public DataSource txDataSource() {
        return new DruidDataSource();
    }

    @Bean(name = "txJdbcTemplate")
    public JdbcTemplate txJdbcTemplate(@Qualifier("txDataSource") DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

}
```

## 去除Druid首页广告

druid监控首页会有阿里云广告，可以新增配置文件RemoveDruidAdConfig去掉广告

```java
/**
 * @author 唐亮
 * @date 22:42 2020/6/28
 * @return
 */
@Configuration
@ConditionalOnWebApplication
@AutoConfigureAfter(DruidDataSourceAutoConfigure.class)
@ConditionalOnProperty(name = "spring.datasource.druid.stat-view-servlet.enable",
        havingValue = "true", matchIfMissing = true)
public class RemoveDruidAdConfig {

    /**
     * 方法名: removeDruidAdFilterRegistrationBean
     * 方法描述:  除去页面底部的广告
     * @param properties
     * @return org.springframework.boot.web.servlet.FilterRegistrationBean
     * @throws
     */
    @Bean
    public FilterRegistrationBean removeDruidAdFilterRegistrationBean(DruidStatProperties properties)
    {
        // 获取web监控页面的参数
        DruidStatProperties.StatViewServlet config = properties.getStatViewServlet();
        // 提取common.js的配置路径
        String pattern = config.getUrlPattern() != null ? config.getUrlPattern() : "/druid/*";
        String commonJsPattern = pattern.replaceAll("\\*", "js/common.js");

        final String filePath = "support/http/resources/js/common.js";

        //创建filter进行过滤
        Filter filter = new Filter() {
            @Override
            public void init(FilterConfig filterConfig) throws ServletException {
            }

            @Override
            public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
                    throws IOException, ServletException {
                chain.doFilter(request, response);
                // 重置缓冲区，响应头不会被重置
                response.resetBuffer();
                // 获取common.js
                String text = Utils.readFromResource(filePath);
                // 正则替换banner, 除去底部的广告信息
                text = text.replaceAll("<a.*?banner\"></a><br/>", "");
                text = text.replaceAll("powered.*?shrek.wang</a>", "");
                response.getWriter().write(text);
            }

            @Override
            public void destroy() {
            }
        };
        FilterRegistrationBean registrationBean = new FilterRegistrationBean();
        registrationBean.setFilter(filter);
        registrationBean.addUrlPatterns(commonJsPattern);
        return registrationBean;
    }
}
```

## 自定义接口获取Druid监控数据

除此之外，如果druid监控中有你需要的数据，也可以自定义接口返回你需要的数据，如：  

```java
/**
 * /druid-stat 接口获取到统计数据
 *
 * @author 唐亮
 * @date 22:40 2020/6/28
 * @return
 */
@RestController
public class DruidStatController {
    @GetMapping("/druid-stat")
    public Object druidStat() {
        // DruidStatManagerFacade#getDataSourceStatDataList 该方法可以获取所有数据源的监控数据
        // 除此之外 DruidStatManagerFacade 还提供了一些其他方法，我们可以按需选择使用。
        return DruidStatManagerFacade.getInstance().getDataSourceStatDataList();
    }
}
```

## 测试

新增测试方法测试数据源配置

```java
/**
 * @author: TangLiang
 * @date: 2020/7/15 8:34
 * @since: 1.0
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class tlDataSource {

    @Autowired
    JdbcTemplate txJdbcTemplate;

    @Autowired
    JdbcTemplate tfJdbcTemplate;

    @Test
    public void tlTest() {
        String sql = "select count(*) from product";
        int count = tfJdbcTemplate.queryForObject(sql, Integer.class);
        System.out.println(count);
        count = txJdbcTemplate.queryForObject(sql, Integer.class);
        System.out.println(count);
    }

    @Test
    public void maria() {
        String sql = "select * from product";
        List<Map<String, Object>> list = txJdbcTemplate.queryForList(sql);
        System.out.println(list.size());
        list.forEach(System.out::println);
    }
}
```

## druid监控不生效

通常yml配置是没问题的，如果druid的spring监控不生效或者不想在yml配置的话，可以手动配置

```markdown
    /**
     * druid的spring监控
     *
     * @return
     */
    @Bean
    public DruidStatInterceptor druidStatInterceptor() {
        DruidStatInterceptor dsInterceptor = new DruidStatInterceptor();
        return dsInterceptor;
    }

    @Bean
    @Scope("prototype")
    public JdkRegexpMethodPointcut druidStatPointcut() {
        JdkRegexpMethodPointcut pointcut = new JdkRegexpMethodPointcut();
        pointcut.setPatterns("com.newangels.er.service.*"); //druid监控的包
        return pointcut;
    }

    @Bean
    public DefaultPointcutAdvisor druidStatAdvisor(DruidStatInterceptor druidStatInterceptor, JdkRegexpMethodPointcut druidStatPointcut) {
        DefaultPointcutAdvisor defaultPointAdvisor = new DefaultPointcutAdvisor();
        defaultPointAdvisor.setPointcut(druidStatPointcut);
        defaultPointAdvisor.setAdvice(druidStatInterceptor);
        return defaultPointAdvisor;
    }
```

