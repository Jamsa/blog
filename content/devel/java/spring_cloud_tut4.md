---
title: "Spring Cloud 上手4-服务消费者"
date: 2018-06-03
modified: 2018-06-06
categories: ["开发"]
tags: ["spring cloud"]
---

这是Spring Cloud上手系列的第四篇，代码放在[GitHub](https://github.com/Jamsa/sc-cloud)上，随着本系列文章更新。

# 版本依赖的坑

在写前面几篇的时候都没感觉到SpringCloud的依赖关系处理必须使用`io.spring.dependency-management`来处理。在使用Feign进行服务消费时遇到很多错误：

 - Feign服务客户端的Bean无法实例化
 
 - java.lang.NoClassDefFoundError: feign/Feign$Builder
 
和其它很多错误。现在已经将[第一篇](../spring_cloud_tut1/)中的构建依赖处理好。

# 配置模块依赖

在`consumer:service`工程的`build.gradle`中添加以下配置：

```gradle
dependencies {
    compile project(':provider:api')
    compile libs.'eureka-client'  //Eureka客户端
}

jar {
    manifest {
        attributes "Manifest-Version": 1.0,
                'Main-Class': 'com.github.jamsa.sc.consumer.controller.ConsumerController'
    }
}
```
即这个工程有三个主要的依赖：

 - `provider:api`中的接口声明。
 
 - 它也是Eureka客户端工程，也依赖于`eureka-client`。
 
  - 对`feign`的依赖则由全局的`build.gradle`中处理。

# 使用Feign在消费方编写API进行消费

`consumer:service`中添加消费接口，和对应的Fallback实现，fallback实现中不需要配置`@RequestParam`这类注解，因为它不是对远程方法的引用，它本身就是无法连接远程服务时的替代实现。

```java
/**
 * 引用服务提供方提供的接口
 */
@FeignClient(name="sc-provider",fallback = FeignFallbackConsumerRemoteService.class)
public interface ConsumerRemoteService{
    @RequestMapping(value="/provider/hello",method= RequestMethod.GET)
    String hello(@RequestParam("name") String name);
}

@Component
public class FeignFallbackConsumerRemoteService implements ConsumerRemoteService {

    @Override
    public String hello(String name) {
        return "未连接远程服务";
    }
}
```

添加控制器：

```java

/**
 * 服务消费方
 */
@SpringBootApplication
@EnableEurekaClient
@EnableFeignClients(basePackages = {"com.github.jamsa.sc.consumer.service"})
@RestController
@RequestMapping("/consumer")
@ComponentScan(basePackages={"com.github.jamsa.sc.consumer"})
public class ConsumerController{

    //注入服务接口
    @Autowired
    private ConsumerRemoteService consumerRemoteService;

    @RequestMapping("/hello")
    public String hello(@RequestParam String name) {
        return "Hello From Remote:"+consumerRemoteService.hello(name);
    }

    public static void main(String[] args) {
        SpringApplication.run(ConsumerController.class,args);
    }
}
```

在工程根目录使用`gradle :consumer:service:build`构建之后，执行`java -jar consumer/service/build/libs/sc-consumer-service-0.0.1.jar`。启动完毕后，就可以通过`http://localhost:9011/consumer/hello?name=Jamsa`直接访问就能看到从`provider`返回的信息。

# 使用Feign 和服务提供方的API进行消费

使用服务提供方的API，只是在消费端编写接口继承提供方的接口。所共享的代码也仅仅只是接口中的方法声明和各类注解了。

这里我们另外编写一个使用`provider:api`中的接口的服务：

```java
@FeignClient(name="sc-provider",fallback = FeignFallbackConsumerRemoteService.class)
@RequestMapping("/provider")
public interface ConsumerRemoteApiService extends ProviderRemoteService {

}
```

如上所述，这只是一个空接口。

将它注入到`ConsumerController`中，并在`helloByApi`这个方法中调用：

```java
    @Autowired
    private ConsumerRemoteApiService consumerRemoteApiService;

    @RequestMapping("/helloByApi")
    public String helloByApi(@RequestParam String name) {
        return "Hello From Remote By API:"+consumerRemoteApiService.hello(name);
    }
```

重新构建并运行之后，访问`http://localhost:9011/consumer/helloByApi?name=Jamsa`，结果报错了：

```
Whitelabel Error Page

This application has no explicit mapping for /error, so you are seeing this as a fallback.

Sun Jun 03 23:04:58 CST 2018
There was an unexpected error (type=Internal Server Error, status=500).
status 404 reading ConsumerRemoteApiService#hello(String); content: {"timestamp":1528038298528,"status":404,"error":"Not Found","message":"No message available","path":"/hello"}
```

这是因为我在api中写的`RequestMapping`并非最终的`uri`，我在`ProviderController`上添加了`@RequestMapping("/provider")`注解，最终`hello`方法被映射到了`/provider/hello`上。

在上面这种方式进行消费时，虽然我在`ConsumerRemoteApiService`中也添加了`@RequestMapping("/provider")`注解，但是这个注解好像被忽略掉了，估计是因为被注解的类上没有`Controller`注解。

如果要让这种方式调用成功，就不能在`ProviderController`上添加`@RequestMapping`注解。需要将它的内容合并到`ProviderRemoteService`的`@RequestMapping`。

`ProviderController`调整为

```java
/**
 *  服务提供方
 * Created by zhujie on 2018/5/29.
 */
@SpringBootApplication
@EnableEurekaClient
@RestController
@ComponentScan(basePackages={"com.github.jamsa.sc.provider"})
//@RequestMapping("/provider")
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

`ProvicerRemoteServic`调整为：

```java
public interface ProviderRemoteService {
    @RequestMapping(value="/provider/hello",method= RequestMethod.GET)
    String hello(@RequestParam("name") String name);//这个name对服务消费方是必须的，否则调用时会报错
}
```

调整完毕后重新构建`provider:service`和`consumer:service`（因为它们都依赖于`provider:api`），重新运行这两个应用，就能在`http://localhost:9011/consumer/helloByApi?name=Jamsa`看到期望的结果了。

# 直接使用RestTempalte消费服务

除使用Feign外，我们也可以直接使用RestTemplate来进行服务消费。

首先，为了配置方便，我们在`controller`包下增加`Config`配置`RestTemplate`。

```java
@Configuration
public class Config {
    @Bean
    @LoadBalanced
    public RestTemplate getRestTemplate() {
        return new RestTemplate();
    }

}
```

然后，在`ConsumerController`中注入`RestTemplate`并添加这种调用方式的测试入口。

```java
@Autowired
    private RestTemplate restTemplate;

    @RequestMapping("/helloByRest")
    public String helloByRest(@RequestParam String name) {
        return "Hello From Remote By RestTemplate: "+restTemplate.getForObject("http://SC-PROVIDER/provider/hello?name="+name,String.class);
    }
```


注意，这里的`@LoadBalanced`注解，如果不使用这个注解，我们在调用服务的时候就只能使用`http://localhost:9010/provider/hello`这种固定的URL。在这里我们使用的URL是通过服务名拼接的，`http://SC-PROVIDER/provider/hello`并非真实服务提供方的URL，而是由`http://{Eureka服务名}/...`构成的，为什么可以这样调用呢？还是因为我们在`RestTempate`这个bean定义的地方使用了`@LoadBalanced`注解。

如果不添加这个注解，`RestTempalte`将不具备负载均衡的能力，只能单点调用。添加这个注解后对RestTemplate的调用将被拦截，拦截器将使用Ribbon提供的负载均衡能力，从Eureka中获取服务节点，并挑选某个节点调用。

相关细节可参考 [这篇文章](https://blog.csdn.net/puhaiyang/article/details/79682177)。


