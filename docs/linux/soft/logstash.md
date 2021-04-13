> logstash 版本 7.6.2

1. 下载

```
wget https://artifacts.elastic.co/downloads/logstash/logstash-7.6.2.tar.gz
```

解压

```
tar -zxvf logstash-7.6.2.tar.gz
```

将屏幕输入的字符串输出到elasticsearch服务中

```
/usr/local/logstash/bin/logstash -e 'input { stdin{} } output { elasticsearch { hosts => ["127.0.0.1:9200"] } }'
```

收集系统日志的conf

```markdown
input {
    file {
        path => "/var/log/messages"
        type => "system"
        start_position => "beginning"
    }
    file {
        path => "/application/es/to/logs/elasticsearch.log"
        type => "es-error"
        start_position => "beginning"
    }
}
output {
    if [type] == "system" {
        elasticsearch {
            hosts => ["10.0.0.169:9200"]
            index => "system-%{+YYYY.MM.dd}"
        }
    }
    if [type] == "es-error" {
        elasticsearch {
            hosts => ["10.0.0.169:9200"]
            index => "es-error-%{+YYYY.MM.dd}"
        }
    }
}
```

执行命令启动logstash服务:

```
/usr/local/logstash/bin/logstash -f logstash.conf
```