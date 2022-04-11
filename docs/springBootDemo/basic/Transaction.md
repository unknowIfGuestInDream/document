> 大家所了解的事务Transaction，它是一些列严密操作动作，要么都操作完成，要么都回滚撤销。Spring事务管理基于底层数据库本身的事务处理机制。数据库事务的基础，是掌握Spring事务管理的基础。

## 特性

事务具备ACID四种特性，ACID是Atomic（原子性）、Consistency（一致性）、Isolation（隔离性）和Durability（持久性）的英文缩写。
  
1. 原子性（Atomicity）  
事务最基本的操作单元，要么全部成功，要么全部失败，不会结束在中间某个环节。事务在执行过程中发生错误，会被回滚到事务开始前的状态，就像这个事务从来没有执行过一样。
2. 一致性（Consistency）  
事务的一致性指的是在一个事务执行之前和执行之后数据库都必须处于一致性状态。如果事务成功地完成，那么系统中所有变化将正确地应用，系统处于有效状态。如果在事务中出现错误，那么系统中的所有变化将自动地回滚，系统返回到原始状态。
3. 隔离性（Isolation）  
指的是在并发环境中，当不同的事务同时操纵相同的数据时，每个事务都有各自的完整数据空间。由并发事务所做的修改必须与任何其他并发事务所做的修改隔离。事务查看数据更新时，数据所处的状态要么是另一事务修改它之前的状态，要么是另一事务修改它之后的状态，事务不会查看到中间状态的数据。
4. 持久性（Durability）  
指的是只要事务成功结束，它对数据库所做的更新就必须永久保存下来。即使发生系统崩溃，重新启动数据库系统后，数据库还能恢复到事务成功结束时的状态。

## 事务的传播特性 

事务传播行为就是多个事务方法调用时，如何定义方法间事务的传播。Spring定义了7中传播行为：

1. propagation_requierd：如果当前没有事务，就新建一个事务，如果已存在一个事务中，加入到这个事务中，这是Spring默认的选择。
2. propagation_supports：支持当前事务，如果没有当前事务，就以非事务方法执行。
3. propagation_mandatory：使用当前事务，如果没有当前事务，就抛出异常。
4. propagation_required_new：新建事务，如果当前存在事务，把当前事务挂起。
5. propagation_not_supported：以非事务方式执行操作，如果当前存在事务，就把当前事务挂起。
6. propagation_never：以非事务方式执行操作，如果当前事务存在则抛出异常。
7. propagation_nested：如果当前存在事务，则在嵌套事务内执行。如果当前没有事务，则执行与propagation_required类似的操作。

## 事务的隔离级别

1. read uncommited：是最低的事务隔离级别，它允许另外一个事务可以看到这个事务未提交的数据。
2. read commited：保证一个事物提交后才能被另外一个事务读取。另外一个事务不能读取该事物未提交的数据。
3. repeatable read：这种事务隔离级别可以防止脏读，不可重复读。但是可能会出现幻象读。它除了保证一个事务不能被另外一个事务读取未提交的数据之外还避免了以下情况产生（不可重复读）。
4. serializable：这是花费最高代价但最可靠的事务隔离级别。事务被处理为顺序执行。除了防止脏读，不可重复读之外，还避免了幻象读

脏读、不可重复读、幻象读概念说明：

* 脏读：指当一个事务正字访问数据，并且对数据进行了修改，而这种数据还没有提交到数据库中，这时，另外一个事务也访问这个数据，然后使用了这个数据。因为这个数据还没有提交那么另外一个事务读取到的这个数据我们称之为脏数据。依据脏数据所做的操作肯能是不正确的。
* 不可重复读：指在一个事务内，多次读同一数据。在这个事务还没有执行结束，另外一个事务也访问该同一数据，那么在第一个事务中的两次读取数据之间，由于第二个事务的修改第一个事务两次读到的数据可能是不一样的，这样就发生了在一个事物内两次连续读到的数据是不一样的，这种情况被称为是不可重复读。
* 幻象读：一个事务先后读取一个范围的记录，但两次读取的纪录数不同，我们称之为幻象读（两次执行同一条 select 语句会出现不同的结果，第二次读会增加一数据行，并没有说这两次执行是在同一个事务中）

## 事务几种实现方式

### 使用声明式事务@Transactional注解

@Transactional注解 可以作用于接口、接口方法、类以及类方法上。当作用于类上时，该类的所有 public 方法将都具有该类型的事务属性，同时，我们也可以在方法级别使用该标注来覆盖类级别的定义。

虽然@Transactional 注解可以作用于接口、接口方法、类以及类方法上，但是 Spring 建议不要在接口或者接口方法上使用该注解，因为这只有在使用基于接口的代理时它才会生效。另外， @Transactional注解应该只被应用到 public 方法上，这是由Spring AOP的本质决定的。如果你在 protected、private 或者默认可见性的方法上使用 @Transactional 注解，这将被忽略，也不会抛出任何异常。

默认情况下，只有来自外部的方法调用才会被AOP代理捕获，也就是，类内部方法调用本类内部的其他方法并不会引起事务行为，即使被调用方法使用@Transactional注解进行修饰。

@Transactional注解属性

```java
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Inherited
@Documented
public @interface Transactional {

    /**
     * 当在配置文件中有多个 TransactionManager , 可以用该属性指定选择哪个事务管理器。
     */
    @AliasFor("transactionManager")
    String value() default "";

    /**
     * 同上。
     */
    @AliasFor("value")
    String transactionManager() default "";

    /**
     * 事务的传播行为，默认值为 REQUIRED。
     */
    Propagation propagation() default Propagation.REQUIRED;

    /**
     * 事务的隔离规则，默认值采用 DEFAULT。
     */
    Isolation isolation() default Isolation.DEFAULT;

    /**
     * 事务超时时间。
     */
    int timeout() default TransactionDefinition.TIMEOUT_DEFAULT;

    /**
     * 是否只读事务
     */
    boolean readOnly() default false;

    /**
     * 用于指定能够触发事务回滚的异常类型。
     */
    Class<? extends Throwable>[] rollbackFor() default {};

    /**
     * 同上，指定类名。
     */
    String[] rollbackForClassName() default {};

    /**
     * 用于指定不会触发事务回滚的异常类型
     */
    Class<? extends Throwable>[] noRollbackFor() default {};

    /**
     * 同上，指定类名
     */
    String[] noRollbackForClassName() default {};

}
```

### 使用编程式事务TransactionTemplate

编程式事务管理使用TransactionTemplate或者直接使用底层的PlatformTransactionManager。对于编程式事务管理，spring推荐使用TransactionTemplate。

和编程式事务相比，声明式事务唯一不足地方是，后者的最细粒度只能作用到方法级别，无法做到像编程式事务那样可以作用到代码块级别。但是即便有这样的需求，也存在很多变通的方法，比如，可以将需要进行事务管理的代码块独立为方法等等。

```java
/**
    * 定义事务管理bean
    */
   @Bean
   public PlatformTransactionManager transactionManager() {
   	DataSourceTransactionManager transactionManager = new DataSourceTransactionManager();
   	transactionManager.setDataSource(dataSource());// 注入dataSource
   	return transactionManager;
   }
   /**
    * 定义TransactionTemplate类型的bean
    */
   @Bean
   public TransactionTemplate transactionTemplate() {
   	TransactionTemplate transactionTemplate=new TransactionTemplate();
   	transactionTemplate.setTransactionManager(transactionManager());//注入事务管理器
   	return transactionTemplate;
   }
```

```java
private final TransactionTemplate transactionTemplate;
        //无返回值
        transactionTemplate.execute(new TransactionCallbackWithoutResult() {
            @Override
            protected void doInTransactionWithoutResult(TransactionStatus status) {
               String sql = "insert into T_ENGG_APPLY_ACCEPT_FILE (ID, ENGG_APPLY_ACCEPT_ID, FILEFOLDERLISTRECORD_ID) values (?, ?, ?)";
               jdbcTemplate.update(sql, new Object[]{ID, ENGG_APPLY_ACCEPT_ID, FILEFOLDERLISTRECORD_ID});
            }
        });

        //执行带有返回值<Object>的事务管理
        transactionTemplate.execute(new TransactionCallback<Object>() {
            @Override
            public Object doInTransaction(TransactionStatus transactionStatus) {
                    //.......   业务代码
                    return new Object();
            }
        });
```

在编程式事务中可以不用显式的使用try,catch，手动回滚，TransactionTemplate会在遇到错误的时候自动回滚