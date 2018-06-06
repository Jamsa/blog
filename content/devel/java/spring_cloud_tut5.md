Title: Spring Cloud 上手5-服务网关
Date: 2018-06-04
Modified: 2018-06-04
Category: 开发
Tags: spring cloud

这是Spring Cloud上手系列的第四篇，代码放在[GitHub](https://github.com/Jamsa/sc-cloud)上，随着本系列文章更新。

# ZUUL概述

服务网关是微服务中向外部系统提供REST API过程中起服务路由、负载均衡的角色。也可将权限控制等功能放在服务网关上，为微服务提供保护。

SpringCloud Netflix中的Zuul承担了这样的功能。它可以作为Eureka客户端与Eureka集成，实现自动的服务路由。也可以通过配置文件来调整路由的策略，对内部服务提供保护。

使用Zuul的典型场景是这样的：

```
                              -------------
                             (   外部调用  )
                              -------------
                                    ||
                         +-----------------------+
                         |         Zuul          |
                         +-----------------------+
                                    ||
                                    ||
                         +-----------------------+
                         |       consumer        |
                         +-----------------------+
                               ||          || 
                         +----------+  +---------+
                         |Service A |  |Service B|
                         | provider |  | provider|
                         |          |  |         |
                         +----------+  +---------+

```

外部调用通过Zuul调用内部的REST服务，通常情况下内部并不会把所有服务都暴露给外部。上图中的`Sercie A/B provider`就只是供内部调用的，`consumer`供外部系统调用的服务。

# 使用Zuul开发服务网关

在我们的示例中服务网关放在`gateway`模块中。

## 依赖配置

`gateway`模块的`build.gradle`:

```groovy
dependencies {
    compile libs.'zuul'
    compile libs.'eureka-client'
}

jar {
    manifest {
        attributes "Manifest-Version": 1.0,
                'Main-Class': 'com.github.jamsa.sc.gateway.Application'
    }
}
```

从上面可以看出`gateway`模块也是一个`eureka-client`模块，它通过eureka查询服务信息，并自动对eureka上注册的服务进行映射。

## 入口程序

`Application`类的内容也相当简单:

```java
@SpringBootApplication
@EnableZuulProxy
@EnableEurekaClient
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
```

只需要添加`@EnableZuulProxy`和`@EnableEurekaClient`注解，基本的服务网关就完成了。

## 配置信息

再来看看`application.yml`的内容：

```yaml
eureka:
  instance:
    hostname: localhost
  client:
    serviceUrl:
      defaultZone: http://localhost:9001/eureka/
spring:
  application:
    name: sc-gateway
server:
  port: 9000
zuul:
  routes:
    sc-consumer:
      path: /api/**
      serviceId: sc-consumer
management:
  security:
    enabled: false
```

这里与之前的`eureka-client`工程并没有不同，只是多了`management`和`zuul`段。`management`段中禁用的安全检查，以便我们能直接通过`http://localhost:9000/routes`来查看路由信息。由于`spring-cloud-starter-zuul`已经包含了`spring-boot-starter-actuator`，它本身具备路由管理能力，只不过默认情况下直接访问`/routes`会报`Unauthorized 401`错误。

`zuul`段的配置信息用于路由规则配置，上面配置文件中的作用是将`sc-consumer`这个应用映射至`http://localhost:9000/api/**`下。

因为`zuul`也是`eureka`客户端工程，它会自动映射`eureka`注册中心注册的服务，所以，即使上面不添加`zuul`这段配置，我们也能通过`http://localhost:9000/服务id/**`访问到对应的服务。比如，通过`http://localhost:9000/sc-provider/provider/hello?name=Jamsa`就能访问到`:provider:service`应用。

# 路由配置

以上配置完成后，我们可以通过`http://localhost:9000/routes`看下路由表:

```
{"/api/**":"sc-consumer","/sc-consumer/**":"sc-consumer","/sc-provider/**":"sc-provider"}
```

从这里能看到`sc-provider`和`sc-consumer`都被映射到了应用名称对应的`URL`下，`/api/**`是来自配置文件的映射配置，也被映射到了`sc-consumer`应用。

如果我们想保护`sc-provider`，不将它暴露到外部怎么办呢？有两种方式，第一种是添加`ignoredServices`规则，匹配上这个表达式的服务名将被不被自动映射；第二种是使用`ignore-patterns`规则，匹配上这个规则的路径会被忽略。例如：

```yaml
zuul:
  ignoredServices: '*' #忽略所有服务
  routes:
    sc-consumer:
      path: /api/**
      serviceId: sc-consumer
```

```yaml
zuul:
  ignoredServices: sc-provider #忽略sc-provider服务
  routes:
    sc-consumer:
      path: /api/**
      serviceId: sc-consumer
```

```yaml
zuul:
  ignored-patterns: /**/hello/**  #忽略所有包含/hello/的路径
  routes:
    sc-consumer:
      path: /api/**
      serviceId: sc-consumer
```

[参考](http://blog.51cto.com/1754966750/1958422)

