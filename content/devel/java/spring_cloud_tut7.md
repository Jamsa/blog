Title: Spring Cloud 上手7-配置中心
Date: 2018-06-07
Modified: 2018-06-07
Category: 开发
Tags: spring cloud

这是Spring Cloud上手系列的第七篇，代码放在[GitHub](https://github.com/Jamsa/sc-cloud)上，随着本系列文章更新。

# 概述

通过Spring Cloud Config可以对各个系统的配置信息进行集中管理和维护。

Spring Cloud Config服务端读取git、svn或本地目录（包括classpath路径)中保存的配置信息。

将Spring Cloud Config服务作为Eureka客户端，则为Config Server提供高可用。Config Client程序可以通过Eureka获取Config Server的信息并读取配置。

# Spring Cloud Config Server配置

## 添加依赖

Spring Config 服务相关的两个依赖是`org.springframework.cloud:spring-cloud-config-server`和`org.springframework.cloud:spring-cloud-config-client`，分别对应于配置服务的服务端和客户端。

我们先在根模块的`build.gradle`中添加程序库依赖。

```groovy
//依赖
ext.libs = [
        "spring-cloud":"org.springframework.cloud:spring-cloud-dependencies:${versions.springCloud}",
        "spring-web":"org.springframework:spring-web:${versions.spring}",
        "spring-boot":"org.springframework.boot:spring-boot-starter",
        "eureka-server":"org.springframework.cloud:spring-cloud-starter-netflix-eureka-server",
        "eureka-client":"org.springframework.cloud:spring-cloud-starter-netflix-eureka-client",
        "zuul":"org.springframework.cloud:spring-cloud-starter-netflix-zuul",
        "feign":"org.springframework.cloud:spring-cloud-starter-feign",
        "config-server":"org.springframework.cloud:spring-cloud-config-server",
        "config-client":"org.springframework.cloud:spring-cloud-config-client"
]
```

## 添加config模块

在根模块下添加新的`config`，以它作为Config Server。将这个模块添加至根模块的`settings.gradle`中。

```groovy
rootProject.name = 'sc-cloud'

include 'registry','gateway','config'
include 'provider:api','provider:service'
include 'consumer:api','consumer:service'
```

在`config`模块自己的`build.gradle`中添加`config-server`依赖，并配置好`Main-Class`：

```groovy
dependencies {
    compile libs.'config-server'
    compile libs.'eureka-client'
}

jar {
    manifest {
        attributes "Manifest-Version": 1.0,
                'Main-Class': 'com.github.jamsa.sc.config.Application'
    }
}
```

## MainClass

添加配置服务程序的入口类Application:

```java
@SpringBootApplication
@EnableEurekaClient
@EnableConfigServer
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
```

这里我们直接做高可用配置，添加了`@EnableEurekaClient`注解，这样配置服务的客户端就能通过Eureka注册中心获取配置服务器的信息。

如果不将配置服务注册至Eureka，配置中心的客户端程序仍然能通过完整的URL来访问配置服务。但无法提供高可用支持。

## 对服务程序进行配置

添加`application.yml`配置文件。

```yaml
eureka:
  instance:
    hostname: localhost
  client:
    serviceUrl:
      defaultZone: http://localhost:9001/eureka/
spring:
  application:
    name: sc-config
  profiles:
    active: native #使用本地目录读取配置文件，而不是从版本仓库
  cloud:
    config:
      server:
        native:
          searchLocations:classpath:/config
        git:
          uri: http://xxx.git
          searchPaths: config #配置文件放在根目录时不需要配置
server:
  port: 9002
management:
  security:
    enabled: false
```

这里将`spring.profiles.active`配置为`native`，是为了使用本地目录。`spring.cloud.config.server.native`是针对`native profile`的配置，在这个配置文件里可以配置多个`profile`，由`active`确定使用哪个`profile`。可以创建多套不同的`profile`，分别用于本机开发、测试、生产部署。

## 添加样例配置文件

根据`application.xml`中指定的`searchLocations`，我们在`config`模块的`src/resources`目录下添加`config`目录来保存配置信息。在这个目录下添加以下两个配置文件：

`config-for-client-dev.yml`

```yaml
env:
  name:dev
  username:uname for dev
```

`config-for-client-test.properties`

```
env.name=tet
env.username=uname for test
```

## 打包运行配置服务程序

在`sc-cloud`根模块，执行`gradle build`编译整个工程。然后运行

`java -jar config/build/libs/sc-config-0.0.1.jar`

启动配置服务程序。

启动完毕后，在Eureka注册中心中可以查看到这个新的服务。

![配置中心]({attach}spring_cloud_tut/config1.png)

也可以通过`http://localhost:9002/config-for-client-dev.yml`和`http://localhost:9002/config-for-client-test.properties`访问上节中的配置文件。

![配置中心-配置信息dev]({attach}spring_cloud_tut/config2.png)

![配置中心-配置信息test]({attach}spring_cloud_tut/config3.png)


