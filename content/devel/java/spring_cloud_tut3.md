Title: Spring Cloud 上手3-服务提供者
Date: 2018-05-30
Modified: 2018-05-30
Category: 开发
Tags: spring cloud

这是Spring Cloud上手系列的第三篇，代码放在[GitHub](https://github.com/Jamsa/sc-cloud)上，随着本系列文章更新。

# 微服务下的代码共享

对于微服务间是否需要进行代码共享，大家都有不同的看法。

虽然，实际的生产应用中，我个人是倾向于不共享代码的。这样可以避免代码上的强依赖，加快服务构建的速度。但是，在[下一篇]({filename}spring_cloud_tut4.md)讲服务消费的时候将使用几种不同的方式来调用服务。在本系列文章的其它地方，为减少代码量，我们主要使用了api模块在服务提供方和消费方间进行代码共享。

Philipp Hauer的两篇文章可供参考

[RESTful API Design. Best Practices in a Nutshell](https://blog.philipphauer.de/restful-api-design-best-practices/)

[Don't Share Libraries among Microservices](https://blog.philipphauer.de/dont-share-libraries-among-microservices/)

# 创建服务提供者

我们在`provider`中创建一个服务，启动`provider-service`应用后，将在`Eureka`注册中心中看到它。

在[第一篇文章]({filename}spring_cloud_tut1.md)提到过，`provider`只起目录分类作用，不是实际工程，实际工程是它下面的两个子模块`api`和`service`其中`api`提供客户端调用的接口，供后面使用`Feign`使用，`service`是一个Spring Boot应用，提供实际的服务。

## 配置模块依赖

前面提到过`api`模块如果没有依赖需要声明，就不需要添加`build.gradle`了。`service`则需要添加`build.gradle`，添加配置，设置`Main-Class`信息：

```groovy
dependencies {
    compile project(':provider:api')
    compile libs.'eureka-client'
}

jar {
    manifest {
        attributes "Manifest-Version": 1.0,
                'Main-Class': 'com.github.jamsa.sc.provider.controller.ProviderController'
    }
}
```

这里的`compile project(':provider:api')`标明`service`模块依赖于`api`模块。

## 创建服务

在`api`模块中添加远程服务接口：

```java
public interface ProviderRemoteService {
    @RequestMapping(value="/hello",method= RequestMethod.GET)
    String hello(@RequestParam("name") String name);//这个name对服务消费方是必须的，否则调用时会报错
}
```

这个接口可供服务提供方和消费方共享。

在`service`模块中编写Spring Boot程序入口和服务实现：

```java
@SpringBootApplication
@EnableEurekaClient
@RestController
@ComponentScan(basePackages={"com.github.jamsa.sc.provider"})
@RequestMapping("/provider")
public class ProviderController implements ProviderRemoteService {

    @Override
    public String hello(String name) {
        return "Hello "+name;
    }

    public static void main(String[] args) {
        SpringApplication.run(ProviderController.class,args);
    }
}
```

这里的`@EnableEurekaClient`注解用于向服务注册中心注册服务。另一个类似的注解是`@EnableDiscoveryClient`两者的区别在于前者来自于`spring-cloud-netflix`只能用于`eureka`，后者来自于`spring-cloud-commons`，可用于其它类型的注册中心，如果使用了`eureka`则两者的作用是一样的。

在`application.yml`中配置服务注册中心地址：

```yaml
spring:
  application:
    name: sc-provider
server:
  port: 9010
eureka:
  instance:
    hostname: localhost
  client:
    serviceUrl:
      defaultZone: http://localhost:9001/eureka/
```

## 构建并启动服务

在根模块中使用`gradle :provider:service:build`构建服务注册中心应用。

完成后使用`java -jar provider/service/build/libs/sc-provider-service-0.0.1.jar`启动服务注册中心。

就能在`http://localhost:9001`查看到`SC_PROVIDER`服务的注册信息了。

![Eureka服务注册中心]({attach}spring_cloud_tut/eureka2.png)

访问`http://localhost:9010/provider/hello?name=Jamsa`能直接访问到该服务。

