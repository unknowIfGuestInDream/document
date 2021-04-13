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

oracle to es 配置

```markdown
input {
 stdin { }
 jdbc {
        jdbc_connection_string => "jdbc:oracle:thin:@10.18.26.86:1521:pmnew"

        jdbc_user => "pmnew"

        jdbc_password => "pmnew"

        jdbc_driver_library => "E:/mysqlJAR/ojdbc6-11.2.0.3.jar"

        jdbc_driver_class => "Java::oracle.jdbc.driver.OracleDriver"

        jdbc_paging_enabled => "true"

        jdbc_page_size => "50000"
		tracking_column => "creation_date_"
        use_column_value => true
        tracking_column_type => "timestamp"
		statement => "SELECT * FROM ER_WORK_TICKET_DETAIL WHERE CREATION_DATE_ > :sql_last_value AND CREATION_DATE_ < sysdate ORDER BY CREATION_DATE_ ASC"
        schedule => "* * * * *"
    }
 }

filter {
	# 把时间字段的值赋值给@timestamp字段
    ruby {
        code => "event.set('@timestamp',event.get('creation_date_'))"
    }
	# 把数据表中的id值赋值给es中的_id,移除无关的字段
    mutate {
        remove_field => ["@version"]
    }
} 
 
 output {
     stdout {
        codec => json_lines
    }
    elasticsearch {
        hosts => "localhost:9200"
        index => "work_ticket_detail"
        document_type => "_doc"
        document_id => "%{work_ticket_detail_id_}"
    }
}
```

mysql to es

```markdown
input {
 stdin { }
    jdbc {
        jdbc_connection_string => "jdbc:mysql://localhost:3306/mydb?characterEncoding=UTF-8&useSSL=false&autoReconnect=true"

        jdbc_user => "root"

        jdbc_password => "mysql"

        jdbc_driver_library => "D:/driver_class/mysql-connector-java-5.1.47.jar"

        jdbc_driver_class => "com.mysql.jdbc.Driver"

        jdbc_paging_enabled => "true"

        jdbc_page_size => "50000"
		tracking_column => "id"
        use_column_value => true
        tracking_column_type => "numeric"
        statement => "SELECT * FROM pms_product WHERE id > :sql_last_value ORDER BY id ASC"
        schedule => "* * * * *"
    }
}
 
filter {
	# 把时间字段的值赋值给@timestamp字段
    #ruby {
    #    code => "event.set('@timestamp',event.get('creation_date_'))"
    #}
	# 把数据表中的id值赋值给es中的_id,移除无关的字段
    mutate {
        remove_field => ["@version"]
    }
} 
 output {
     stdout {
        codec => json_lines
    }
    elasticsearch {
        hosts => "localhost:9200"
        index => "pmsproduct"
        document_type => "_doc"
        document_id => "%{id}"
    }
}
```

收集项目日志

```markdown
input {
    tcp {
	 mode => "server"
     host =>"localhost"
     port => 4560
     codec => json_lines
        }
}

output {
     elasticsearch {
	    action => "index"
        hosts => "localhost:9200"
        index => "springbootdemo-%{+YYYY.MM.dd}"
     }
     stdout { codec=> rubydebug }
}
```