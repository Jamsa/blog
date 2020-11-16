---
title: "Spring Cloud 上手10-日志收集"
date: 2018-06-13
modified: 2018-06-13
categories: ["开发"]
tags: ["spring cloud"]
---

这是Spring Cloud上手系列的第十篇，代码放在[GitHub](https://github.com/Jamsa/sc-cloud)上，随着本系列文章更新。

# ELK简介

ELK是Logstash、ElasticSearch和Kibana的组合。Logstash处理日志的收集，ElasticSearch处理日志的检索，Kibana对日志进行可视化展示和查询。

在Spring Cloud微服务架构下可以使用ElasticSearch来存储两类信息：一类是通过Logstash收集的各个应用的日志，另一类是作为Zipkin的持久化存储。

## Zipkin持久化

Zipkin本身支持采用ElasticSearch作为其存储引擎，它可以直接与ElasticSearch交互，将跟踪信息保存至ElasticSearch。

## 日志收集方式

微服务应用的日志则情况更复杂。ELK与Spring Cloud的集成有两种方式：

 - 一种是各个微服务节点上部署Logstash实例。微服务输出日志时，按Logstash的需要输出为json格式。Logstash则监控这些日志目录，并将这些日志发送至ElasticSearch。由于Logstash是采用jruby实现的，fatjar有20M左右，并且它进行日志处理时候会消耗较多的cpu资源，会影响到微服务节点的性能，因此一般不建议采用此方案。
 
 ![日志收集-elk-logstash1](../spring_cloud_tut/logstash1.png)
 
 - 另一种方式是微服务节点上部署轻量化的日志收集器。通过日志收集器收集日志并转发至独立的Logstash节点。收集器的形式有很多种，可以直接使用Logger将日志转发给Logstash（这篇文章里我们使用这种方式），也可以使用轻量化的日志收集器Filebeat、rsyslog等。

 ![日志收集-elk-logstash2](../spring_cloud_tut/logstash2.png)
 
# 准备ELK环境

为测试方便，我们使用Docker来运行ELK镜像，这里不直接使用ELK官方镜像。官方镜像的E L K各个组件是独立的。为了测试方便，我们使用集成了ELK三个组件的像。

 1. 安装ELK镜像
 
 ```
 docker pull sebp/elk
 ```
 
 2. 顺便将rabbitmq也换成Docker方式运行
 
 ```
 docker pull rabbitmq:3-management
 ```
 
 因为我们要访问rabbitmq的控制台，所以要安装`3-management`，`rabbitmq`镜像不带插件。
 
 3. 编写`docker-compose.yml`配置文件
 
 在根模块的`support/docker`目录下新建`docker-compose.yml`配置文件，内容如下：
 
 ```yaml
elk:
  image: sebp/elk
  ports:
    - "5601:5601"
    - "9200:9200"
    - "5044:5044"

rabbitmq:
  image: rabbitmq:3-management
  ports:
    - "15672:15672"
    - "5672:5672"
    - "5673:5673"
    - "4369:4369"
    - "25672:25672"
 ```
 
 4. 在这个目录下执行`docker-compose up`启动容器。
 
 之后可以从本机的`15672`、`9200`、`5601`分别看到RabbitMQ、ElasticSearch、Kibana的相关信息：
 
 ![日志收集-docker-rabbitmq](../spring_cloud_tut/docker-rabbitmq.png)
 
 ![日志收集-docker-elasticsearch](../spring_cloud_tut/docker-elasticsearch.png)
 
 ![日志收集-docker-kibana](../spring_cloud_tut/docker-kibana.png) 

# ELK与Zipkin集成

[上一篇](../spring_cloud_tut9/)文章中使用Zipkin进行调用链的跟踪。各个服务的调用信息通过RabbitMQ传递至Zipkin服务。默认情况下这些信息是保存在内存中的，并没有进行持久化。我们可以将ELK中的ElasticSearch来存储Zipkin服务接收的数据。

## 添加依赖

在根模块的`build.gradle`中添加`io.zipkin.java:zipkin-autoconfigure-storage-elasticsearch-http`依赖：

```groovy
        //zipkin服务端
        "zipkin-server":"io.zipkin.java:zipkin-server",
        "zipkin-server-ui":"io.zipkin.java:zipkin-autoconfigure-ui",
        "zipkin-server-rabbit":"io.zipkin.java:zipkin-autoconfigure-collector-rabbitmq:2.3.1",
        "zipkin-server-elasticsearch":"io.zipkin.java:zipkin-autoconfigure-storage-elasticsearch-http:2.3.1",
```

向`zipkin`模块的`build.gradle`中添加该依赖：

```groovy
dependencies {
    //ZipKin服务
    compile libs.'zipkin-server'
    compile libs.'zipkin-server-ui'
    compile libs.'zipkin-server-rabbit'
    compile libs.'zipkin-server-elasticsearch'
}
```

## 修改配置

在`zipkin`模块的`application.yml`中添加存储配置：

```yaml
zipkin:
  collector:
    rabbitmq:
      addresses: localhost:5672
      password: guest
      username: guest
      queue: zipkin
  storage:
    type: elasticsearch
    elasticsearch:
      cluster: elasticsearch
      hosts: http://localhost:9200
      index: zipkin
      index-shards: 5
      index-replicas: 1
```

## 构建和测试

重新构建`zipkin`模块并重新运行。再次访问`http://localhost:9000/api/consumer/hello?name=dfdsdsds`产生一些跟踪数据。再访问`http://localhost:5601`的Kibana控制台，就能看到`zipkin`产生的数据了。

![日志收集-zipkin-kibana](../spring_cloud_tut/elk-zipkin-kibana.png)


# ELK日志收集

接下来我们配置各个应用的日志转发功能，将日志信息保存至ELK。

Spring Boot应用默认使用logback来记录日志。Logstash有针对logback的支持，可以直接在logback中增加Logstash的Appender就可以将日志转化为JSON并存储至ElasticSearch。

## 添加依赖

在根模块的`build.gradle`的`ext.libs`中添加`logstash`依赖:

```groovy
        //logstash
        "logstash":"net.logstash.logback:logstash-logback-encoder:4.6"
```

将该依赖添加至`service`、`gateway`应用中：

```groovy
    // service 和 gateway 工程的依赖，zipkin 客户端
    if(name=='service'||name=='gateway') {
        dependencies {
            compile libs.'zipkin-client'
            compile libs.'spring-rabbit'
            compile libs.'logstash'
        }
    }
```

## 增加配置

我们以`consumer:service`模块为例。在`resources`目录下增加`logback-spring.xml`，内容如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appender name="LOGSTASH" class="net.logstash.logback.appender.LogstashTcpSocketAppender">
        <destination>localhost:4560</destination>
        <encoder charset="UTF-8" class="net.logstash.logback.encoder.LogstashEncoder"/>
    </appender>

    <include resource="org/springframework/boot/logging/logback/base.xml"/>

    <root level="INFO">
        <appender-ref ref="LOGSTASH"/>
        <appender-ref ref="CONSOLE"/>
    </root>
</configuration>
```

这里配置为将日志发送至`localhost:4560`，我们希望这个端口是Logstash的日志收集端口。由于我们使用的ELK镜像并没有开放这个端口，因此我们需要对`docker-compose.yml`稍做调整，让它加载我们自己的配置文件。

从ELK镜像的[GitHub](https://github.com/spujadas/elk-docker)上查看源码，可以看到镜像开放了`5044`作为`Filebeat`日志收集端口。但是在我们简单的验证环境上用不上，我们希望在`4560`开放`Logstash`的日志收集端口。查看镜像源码可以看到`30-output.conf`配置文件，这个文件只配置了`output`，将这个文件复制到`support/docker/elk-30-output.conf`，并添加`input`配置，开放`logstash`日志收集端口。

```
input {
    tcp {
        port => 4560
        codec => json_lines
    }
}

output {
  elasticsearch {
    hosts => ["localhost"]
    manage_template => false
    index => "%{[@metadata][beat]}-%{+YYYY.MM.dd}"
    document_type => "%{[@metadata][type]}"
  }
}
```

调整`docker-compose.yml`，让ELK容器加载我们的配置文件。

```yaml
elk:
  image: sebp/elk
  ports:
    - "5601:5601"
    - "9200:9200"
    - "5044:5044"
    - "4560:4560"
  volumes:
    - ./elk-30-output.conf:/etc/logstash/conf.d/30-output.conf

rabbitmq:
  image: rabbitmq:3-management
  ports:
    - "15672:15672"
    - "5672:5672"
    - "5673:5673"
    - "4369:4369"
    - "25672:25672"
```

重新运行`docker-compose up`。在docker控制台能看到`4560`端口的监听信息：

![日志收集-zipkin-kibana](../spring_cloud_tut/docker-logstash-input.png)

## 构建并运行

在根模块下重新构建`consumer:service`模块并运行。

进入Kibana控制台的Management -> Index Patterns可以看到产生了新的索引信息：

![日志收集-kibana-logstash](../spring_cloud_tut/kibana-logstash.png)

图中的`%{[@metadata][beat]}-2018.06.13`与`elk-30-output.conf`中`output`段的配置是对应的。创建完索引后，在Kibana控制台的Discover界面上，就能看到`consumer:service`产生的日志了。

![日志收集-kibana-logstash-log](../spring_cloud_tut/kibana-logstash-log.png)
