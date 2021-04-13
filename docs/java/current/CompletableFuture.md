> java8 CompletableFuture类
   事实证明，只有当每个操作很复杂需要花费相对很长的时间（比如，调用多个其它的系统的接口；]
   比如，商品详情页面这种需要从多个系统中查数据显示的）的时候用CompletableFuture才合适，
   不然区别真的不大，还不如顺序同步执行

**并行流和CompletableFuture两者该如何选择**

这两者如何选择主要看任务类型，建议
如果你的任务是计算密集型的，并且没有I/O操作的话，那么推荐你选择Stream的并行流，
实现简单并行效率也是最高的
如果你的任务是有频繁的I/O或者网络连接等操作，那么推荐使用CompletableFuture，
采用自定义线程池的方式，根据服务器的情况设置线程池的大小，尽可能的让CPU忙碌起来

测试类

```java
@SpringBootTest
public class CompletableFutureTest {

    /**
     * runAsync() 异步无参返回
     *
     * @throws Exception
     */
    @Test
    public void asyncThread() throws Exception {
        CompletableFuture async1 = CompletableFuture.runAsync(() -> {
            try {
                Thread.sleep(1000);
                System.out.println(Thread.currentThread().getName());
                System.out.println("none return Async");
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
        // 调用get()将等待异步逻辑处理完成
        async1.get();
    }

    /**
     * supplyAsync() 异步有参返回
     *
     * @throws Exception
     */
    @Test
    public void asyncThread2() throws Exception {
        CompletableFuture<String> async2 = CompletableFuture.supplyAsync(() -> {
            return "hello";
        });
        String result = async2.get();
        // String result2 = async2.get(5L, TimeUnit.SECONDS);
        System.out.println(result);
    }

    /**
     * 自定义线程池，优化CompletableFuture
     *
     * @throws Exception
     */
    @Test
    public void asyncexecutor() throws Exception {
        ExecutorService executorService = Executors.newFixedThreadPool(Math.min(5, 50));
        CompletableFuture<String> async2 = CompletableFuture.supplyAsync(() -> {
            return "hello";
        }, executorService);
        String result = async2.get();
        // String result2 = async2.get(5L, TimeUnit.SECONDS);
        System.out.println(result);
    }

    /**
     * 当一个线程依赖另一个线程时，可以使用 thenApply 方法来把这两个线程串行化。
     * thenApplyAsync默认是异步执行的。这里所谓的异步指的是不在当前线程内执行。
     */
    @Test
    public void thenApply() throws Exception {
        CompletableFuture<Long> future = CompletableFuture.supplyAsync(new Supplier<Long>() {
            @Override
            public Long get() {
                long result = new Random().nextInt(100);
                System.out.println("result1=" + result);
                return result;
            }
        }).thenApply(new Function<Long, Long>() {
            @Override
            public Long apply(Long t) {
                long result = t * 5;
                System.out.println("result2=" + result);
                return result;
            }
        });

        long result = future.get();
        System.out.println(result);
    }

    /**
     * handle 是执行任务完成时对结果的处理。
     * handle 方法和 thenApply 方法处理方式基本一样。不同的是 handle 是在任务完成后再执行，
     * 还可以处理异常的任务。thenApply 只可以执行正常的任务，任务出现异常则不执行 thenApply 方法。
     * <p>
     * 从示例中可以看出，在 handle 中可以根据任务是否有异常来进行做相应的后续处理操作。
     * 而 thenApply 方法，如果上个任务出现错误，则不会执行 thenApply 方法。
     *
     * @throws Exception
     */
    @Test
    public void handler() throws Exception {
        CompletableFuture<Integer> future = CompletableFuture.supplyAsync(new Supplier<Integer>() {

            @Override
            public Integer get() {
                int i = 10 / 0;
                return new Random().nextInt(10);
            }
        }).handle(new BiFunction<Integer, Throwable, Integer>() {
            @Override
            public Integer apply(Integer param, Throwable throwable) {
                int result = -1;
                if (throwable == null) {
                    result = param * 2;
                } else {
                    System.out.println(throwable.getMessage());
                }
                return result;
            }
        });
        System.out.println(future.get());
    }

    /**
     * exceptionally处理异常
     */
    @Test
    public void exceptionally() throws Exception {
        CompletableFuture<String> future = CompletableFuture
                .supplyAsync(() -> {
                    System.out.println("doSomething...");
                    if (true) {
                        throw new RuntimeException("Test Exception");
                    }
                    return "Finish";
                })
                .exceptionally(throwable -> "Throwable exception message:" + throwable.getMessage());
        System.out.println(future.get());
    }

    /**
     * thenAccept接收上一阶段的输出作为本阶段的输入
     * 接收任务的处理结果，并消费处理，无返回结果。
     * 从示例代码中可以看出，该方法只是消费执行完成的任务，并可以根据上面的任务返回的结果进行处理。
     * 并没有后续的输错操作。
     *
     * @throws Exception
     */
    @Test
    public void thenAccept() throws Exception {
        CompletableFuture<Void> future = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                return new Random().nextInt(10);
            }
        }).thenAccept(integer -> {
            System.out.println(integer);
        });
        future.get();
    }

    /**
     * thenRun根本不关心前一阶段的输出，根本不不关心前一阶段的计算结果，因为它不需要输入参数
     * 只要上面的任务执行完成，就开始执行 thenRun
     *
     * @throws Exception
     */
    @Test
    public void thenRun() throws Exception {
        CompletableFuture<Void> future = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                return new Random().nextInt(10);
            }
        }).thenRun(() -> {
            System.out.println("thenRun ...");
        });
        future.get();
    }

    /**
     * thenCombine 合并任务
     * thenCombine 会把 两个 CompletionStage 的任务都执行完成后，
     * 把两个任务的结果一块交给 thenCombine 来处理。
     */
    @Test
    public void thenCombine() throws Exception {
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(new Supplier<String>() {
            @Override
            public String get() {
                return "hello";
            }
        });
        CompletableFuture<String> future2 = CompletableFuture.supplyAsync(new Supplier<String>() {
            @Override
            public String get() {
                return "hello";
            }
        });
        CompletableFuture<String> result = future1.thenCombine(future2, new BiFunction<String, String, String>() {
            @Override
            public String apply(String t, String u) {
                return t + " " + u;
            }
        });
        System.out.println(result.get());
    }

    /**
     * 当两个CompletionStage都执行完成后，把结果一块交给thenAcceptBoth来进行消耗
     */
    @Test
    public void thenAcceptBoth() throws Exception {
        CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                int t = new Random().nextInt(3);
                try {
                    TimeUnit.SECONDS.sleep(t);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("f1=" + t);
                return t;
            }
        });

        CompletableFuture<Integer> f2 = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                int t = new Random().nextInt(3);
                try {
                    TimeUnit.SECONDS.sleep(t);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("f2=" + t);
                return t;
            }
        });
        f1.thenAcceptBoth(f2, new BiConsumer<Integer, Integer>() {
            @Override
            public void accept(Integer t, Integer u) {
                System.out.println("f1=" + t + ";f2=" + u + ";");
            }
        });
    }

    /**
     * 两个CompletionStage，谁执行返回的结果快，我就用那个CompletionStage的结果进行下一步的转化操作
     */
    @Test
    public void applyToEither() throws Exception {
        CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                int t = new Random().nextInt(3);
                try {
                    TimeUnit.SECONDS.sleep(t);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("f1=" + t);
                return t;
            }
        });
        CompletableFuture<Integer> f2 = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                int t = new Random().nextInt(3);
                try {
                    TimeUnit.SECONDS.sleep(t);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("f2=" + t);
                return t;
            }
        });

        CompletableFuture<Integer> result = f1.applyToEither(f2, new Function<Integer, Integer>() {
            @Override
            public Integer apply(Integer t) {
                System.out.println(t);
                return t * 2;
            }
        });

        System.out.println(result.get());
    }

    /**
     * 两个CompletionStage，谁执行返回的结果快，我就用那个CompletionStage的结果进行下一步的消耗操作。
     *
     * @throws Exception
     */
    @Test
    public void acceptEither() throws Exception {
        CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                int t = new Random().nextInt(3);
                try {
                    TimeUnit.SECONDS.sleep(t);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("f1=" + t);
                return t;
            }
        });
        CompletableFuture<Integer> f2 = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                int t = new Random().nextInt(3);
                try {
                    TimeUnit.SECONDS.sleep(t);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("f2=" + t);
                return t;
            }
        });

        CompletableFuture<Integer> result = f1.applyToEither(f2, new Function<Integer, Integer>() {
            @Override
            public Integer apply(Integer t) {
                System.out.println(t);
                return t * 2;
            }
        });

        System.out.println(result.get());
    }

    /**
     * 两个CompletionStage，任何一个完成了都会执行下一步的操作（Runnable）
     *
     * @throws Exception
     */
    @Test
    public void runAfterEither() throws Exception {
        CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                int t = new Random().nextInt(3);
                try {
                    TimeUnit.SECONDS.sleep(t);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("f1=" + t);
                return t;
            }
        });

        CompletableFuture<Integer> f2 = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                int t = new Random().nextInt(3);
                try {
                    TimeUnit.SECONDS.sleep(t);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("f2=" + t);
                return t;
            }
        });
        f1.runAfterEither(f2, new Runnable() {

            @Override
            public void run() {
                System.out.println("上面有一个已经完成了。");
            }
        });
    }

    /**
     * 两个CompletionStage，都完成了计算才会执行下一步的操作（Runnable）
     *
     * @throws Exception
     */
    @Test
    public void runAfterBoth() throws Exception {
        CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                int t = new Random().nextInt(3);
                try {
                    TimeUnit.SECONDS.sleep(t);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("f1=" + t);
                return t;
            }
        });

        CompletableFuture<Integer> f2 = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                int t = new Random().nextInt(3);
                try {
                    TimeUnit.SECONDS.sleep(t);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("f2=" + t);
                return t;
            }
        });
        f1.runAfterBoth(f2, new Runnable() {

            @Override
            public void run() {
                System.out.println("上面两个任务都执行完成了。");
            }
        });
    }

    /**
     * thenCompose 方法允许你对两个 CompletionStage 进行流水线操作，
     * 第一个操作完成时，将其结果作为参数传递给第二个操作。
     *
     * @throws Exception
     */
    @Test
    public void thenCompose() throws Exception {
        CompletableFuture<Integer> f = CompletableFuture.supplyAsync(new Supplier<Integer>() {
            @Override
            public Integer get() {
                int t = new Random().nextInt(3);
                System.out.println("t1=" + t);
                return t;
            }
        }).thenCompose(new Function<Integer, CompletionStage<Integer>>() {
            @Override
            public CompletionStage<Integer> apply(Integer param) {
                return CompletableFuture.supplyAsync(new Supplier<Integer>() {
                    @Override
                    public Integer get() {
                        int t = param * 2;
                        System.out.println("t2=" + t);
                        return t;
                    }
                });
            }

        });
        System.out.println("thenCompose result : " + f.get());
    }

    /**
     * allOf() 多个异步处理(针对有参返回)
     *
     * @throws Exception
     */
    @Test
    public void asyncThread3() throws Exception {
        CompletableFuture<String> a = CompletableFuture.supplyAsync(() -> "hello");
        CompletableFuture<String> b = CompletableFuture.supplyAsync(() -> "youth");
        CompletableFuture<String> c = CompletableFuture.supplyAsync(() -> "!");

        CompletableFuture all = CompletableFuture.allOf(a, b, c);
        all.get();

        String result = Stream.of(a, b, c)
                .map(CompletableFuture::join)
                .collect(Collectors.joining(" "));

        System.out.println(result);
    }

    /**
     * anyOf() 多个异步随机处理(针对有参返回)
     *
     * @throws Exception
     */
    @Test
    public void asyncThread4() throws Exception {
        CompletableFuture<String> a = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(20);
                return "hello";
            } catch (Exception e) {
                e.printStackTrace();
                return "none~";
            }
        });
        CompletableFuture<String> b = CompletableFuture.supplyAsync(() -> "youth");
        CompletableFuture<String> c = CompletableFuture.supplyAsync(() -> "!");

        CompletableFuture<Object> any = CompletableFuture.anyOf(a, b, c);
        String result = (String) any.get();

        System.out.println(result);
    }

}
```