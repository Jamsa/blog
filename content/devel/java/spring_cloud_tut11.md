Title: Spring Cloud 上手11-配置优化
Date: 2018-06-14
Modified: 2018-06-14
Category: 开发
Tags: spring cloud

这是Spring Cloud上手系列的第十一篇，代码放在[GitHub](https://github.com/Jamsa/sc-cloud)上，随着本系列文章更新。

# 概述

本篇主要对各应用的配置进行优化，原因主要有两个：

 - 此前[配置中心]({filename}spring_cloud_tut7.md)一文中只把`provider:service`与配置中心进行了集成，其它应用仍是读取本地的配置信息。
 
 - 写至本篇的时候，发现各个模块的配置文件已经比较乱了，存在大量重复配置，配置文件中也存在一些不需要的配置项，需要进行一轮整理。
 
 - 增加`profile`支持为后面将容器化做准备。
 
优化的目标：

 - 配置中心（config）和注册中心（registry）读取本地配置信息外（先有鸡还是先有蛋的问题，只能读取本地配置文件）。
 
 - 服务网关(gateway)、服务提供者（provider:service）、服务消费者（consumer:service）、调用链分析（zipkin）应用都只保留`boostrap.yml`配置文件，且该配置文件中只保留注册中心地址、应用名称、端口等基本信息。其余配置信息移至配置中心的共享配置文件（application.yml）或应用对应的配置文件（{application}.yml）。
 
 - 添加`profile`支持，默认使用`dev` profile。在配置中心保存的各个应用的配置文件不添加`{application}-{profile}.yml`配置文件（减少配置文件的量），profile相关的配置信息写在`{application}.yml`中。

# 添加依赖

检查要使用配置中心的各个应用的依赖配置，至少需要添加`eureka-client`和`config-client`两个依赖。例如，zipkin的依赖配置：

```groovy
dependencies {
    compile libs.'eureka-client'
    compile libs.'config-client' //Config客户端
    //ZipKin服务
    compile libs.'zipkin-server'
    compile libs.'zipkin-server-ui'
    compile libs.'zipkin-server-rabbit'
    compile libs.'zipkin-server-elasticsearch'
}
```

# 调整配置

## 配置中心服务程序

调整后配置中心服务程序的`application.yml`如下：

```yaml
spring:
  profiles:
    active: dev,native #使用本地目录读取配置文件，而不是从版本仓库
  application:
    name: sc-config
  cloud:
    config:
      server:
        native:
          searchLocations: file:/Users/zhujie/Documents/devel/Java/sc-cloud/support/config #需要从sc-cloud目录下运行程序
          #searchLocations:classpath:/config
        #git:
        #  uri: http://xxx.git
        #  searchPaths: config #配置文件放在根目录时不需要配置
server:
  port: 9002

#取消权限验证
management:
  security:
    enabled: false

# 启用/restart端点重新启动应用程序上下文。
endpoints:
  restart:
    enabled: true

logging:
  level:
    root: INFO
    org.springframework.web.servlet.DispatcherServlet: DEBUG
    org.springframework.cloud.sleuth: DEBUG

---
# dev profile
spring:
  profiles: dev

eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:9001/eureka/

---
# docker profile
spring:
  profiles: docker

eureka:
  client:
    serviceUrl:
     defaultZone: http://sc-config-0.eureka.default.svc.cluster.local:9001/eureka/,http://sc-config-1.eureka.default.svc.cluster.local:9001/eureka/

```

这里将`dev`和`docker`两个`profile`写在了同一配置文件中。

## 配置中心客户端程序

调整后的`provider:service`的`bootstrap.yml`配置文件如下：

```yaml
spring:
  profiles:
    active: dev
  application:
    name: sc-provider
  cloud:
    config:
      failFast: true #快速失败
      discovery:
        serviceId: sc-config #配置服务中心的应用名称
        enabled: true
server:
  port: 9010

---
# dev profile
spring:
  profiles: dev

eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:9001/eureka/

---
# docker profile
spring:
  profiles: docker

eureka:
  client:
    serviceUrl:
     defaultZone: http://sc-config-0.eureka.default.svc.cluster.local:9001/eureka/,http://sc-config-1.eureka.default.svc.cluster.local:9001/eureka/
```

内容比原来的精简了很多，这是因为其它配置信息移入了配置仓库的`application.yml`中。

## 配置中心的配置仓库

### 公共配置文件

Spring Cloud 配置中心客户端支持共享配置文件。存放在配置中心根目录的`application*.yml`配置文件会被各个应用加载。我们将公用配置信息保存在`support/config/application.yml`中：

```yaml
#公共配置

spring:
  zipkin:
    rabbitmq:
      queue: zipkin
  sleuth:
    sampler:
      percentage: 1.0
  cloud:
    bus:
      trace:
        enabled: true

#取消权限验证
management:
  security:
    enabled: false


# 启用/restart端点重新启动应用程序上下文。
endpoints:
  restart:
    enabled: true

logging:
  level:
    root: INFO
    org.springframework.web.servlet.DispatcherServlet: DEBUG
    org.springframework.cloud.sleuth: DEBUG

---
# dev profile
spring:
  profiles: dev

  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest

---
# docker profile
spring:
  profiles: docker

  rabbitmq:
    host: rabbitmq
    port: 5672
    username: guest
    password: guest
```

### 应用配置文件

各个配置中心客户端在启动时，会从配置中心读取应用的私有配置，文件名为`support/config/{application}-{profile}.yml`。以`zipkin`应用的配置文件`sc-zipkin.yml`为例：

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
      index: zipkin
      index-shards: 5
      index-replicas: 1

---
# dev profile
spring:
  profiles: dev

zipkin:
  collector:
    rabbitmq:
      addresses: localhost:5672
  storage:
    elasticsearch:
      hosts: http://localhost:9200
---
# docker profile
spring:
  profiles: docker

zipkin:
  collector:
    rabbitmq:
      addresses: rabbitmq:5672
  storage:
    elasticsearch:
      hosts: http://elk:9200
```

# 构建和运行

各应用的配置文件都默认使用`dev` profile，配置的内容与之前是相同的。因此只需在根模块下使用`gradle build`重新构建。

注意，上面配置中心客户端应用都是通过注册中心获取`sc-config`应用的信息，以服务的方式来访问配置中心。因此，在启动应用时要先启动注册中心、之后是配置中心，然后再启动其它应用。
