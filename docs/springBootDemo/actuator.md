http://localhost:8080/actuator/
threaddump  用于返回线程快照，分析线程阻塞，死锁等
beans  用于返回 spring 容器加载的所有bean
heapdump  可以dump出当前jvm的heap
httptrace  最近的100个http请求，包括request和response内容。
loggers  查看日志级别
metrics 显示应用多样的度量信息
health 显示应用的健康状态
logfile 返回log file中的内容(如果logging.file或者logging.path被设置)
env 显示当前的环境特性
mappings 显示所有的@RequestMapping路径

