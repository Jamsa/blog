Title: Spring Cloud 上手1-准备
Date: 2018-05-30
Modified: 2018-06-03
Category: 开发
Tags: spring cloud

# 目标

从15年开始我一直在使用Dubbo框架进行开发，少量在使用Spring Boot开发一些独立的App服务程序。Spring Cloud相关的文档资料看了不少，但“纸上得来终觉浅，绝知此事要躬行”。所以就有了做一个Spring Cloud Demo工程的想法，主要用来体验Spring Cloud的各种组件和功能。

代码放在[GitHub](https://github.com/Jamsa/sc-cloud)上，随着本系列文章更新。

# 规划

先从最简单的Demo开始，使用SpringCloud的基础功能：Eureka、Zuul、Feign。后续再考虑添加Stream，Bus相关的内容。在工程数量较多，不好维护了，再考虑采用docker和minikube来进行管理。借用一句话“好的架构就像眼镜，你会知道什么时候需要它”。

工程目录规划如下：

```
├── build.gradle
├── common
│   ├── build.gradle
│   └── src
│       └── main
├── provider
│   ├── api
│   │   └── src
│   └── service
│       ├── build.gradle
│       └── src
├── consumer
│   ├── api
│   │   └── src
│   └── service
│       ├── build.gradle
│       └── src
├── gateway
│   ├── build.gradle
│   └── src
├── registry
│   ├── build.gradle
│   └── src
├── settings.gradle
├── support
└── web
```

 - `provider`和`consumer`为两个业务服务模块，其中`provider`和`consumer`只做目录分类用，不是实际的模块。`api`和`service`是模块，`api`存放客户端服务端共享的接口和类，`service`是实际的服务提供者。

 - `registry`为Eureka为基础构建的服务注册中心。
 
 - `gateway`为Zuul为基础构建的服务网关，是外部访问的入口。
 
 - `common`存放公共类，非SpringBoot模块。
 
 - `support`存放支持程序运行的`docker-compose`配置信息和`docker`容器数据卷。

在构建工具的选择上，Github上各路大神的SpringCloud Demo基本上都是以Maven为主的。我这里选择gradle了，只是为了减少编写配置信息。

# Gradle配置规划

使用Gradle进行多模块配置，可选的配置方案有两种，一种是把配置信息集中在根模块的构建文件中集中配置，另一种是各模块独立配置。这里我考虑结合使用这两种配置方式，将全局配置和版式化的配置集中在根模块的build.gradle进行管理，各个子模块的只在自己的build.gradle中维护其依赖声明等个性化的信息。

## 根模块的settings.gradle

```groovy
rootProject.name = 'sc-cloud'

include 'registry','gateway'
include 'provider:api','provider:service'
include 'consumer:api','consumer:service'
```
根模块代号`sc-cloud`，包含`registry`，`gateway`和`provider`、`consumer`模块下的`api`和`service`模块。由于Gradle在处理`incdlude ‘provider:api‘`时也会把`provider`包含进去，因此我们在build.gradle中进行全局性配置时需要排除这些只起分类作用的模块。

## 根模块的build.gradle

```groovy
//依赖版本号
ext.versions = [
        spring: '4.3.17.RELEASE',
        springCloud :'Edgware.SR3'
]
//依赖
ext.libs = [
        "spring-cloud":"org.springframework.cloud:spring-cloud-dependencies:${versions.springCloud}",
        "spring-web":"org.springframework:spring-web:${versions.spring}",
        "spring-boot":"org.springframework.boot:spring-boot-starter",
        "eureka-server":"org.springframework.cloud:spring-cloud-starter-netflix-eureka-server",
        "eureka-client":"org.springframework.cloud:spring-cloud-starter-netflix-eureka-client",
        "zuul":"org.springframework.cloud:spring-cloud-starter-netflix-zuul",
        "feign":"org.springframework.cloud:spring-cloud-starter-feign"
]
//只起分类作用的目录
ext.excludeFolds = ["provider","consumer"]

buildscript {
    ext {
        //springIOVersion = '1.0.5.RELEASE'
        springBootVersion = '1.5.13.RELEASE'
    }
    repositories {
        maven { url "http://maven.aliyun.com/nexus/content/groups/public/" }
        mavenCentral()
    }
    dependencies {
        classpath "org.springframework.boot:spring-boot-gradle-plugin:${springBootVersion}"
    }
}


subprojects {
    //对分类目录不需要进行配置
    if(excludeFolds.contains(name)) return
    

    repositories {
        maven { url "http://maven.aliyun.com/nexus/content/groups/public/" }
        mavenCentral()
    }

    apply plugin: 'java'

    apply plugin: "io.spring.dependency-management"

    dependencyManagement {
        imports {
            mavenBom libs.'spring-cloud'
        }
    }

    //api工程不需要使用spring boot插件
    if(!name.contains("api")) {
        apply plugin: 'org.springframework.boot'
    }

    sourceCompatibility = '1.8'
    targetCompatibility = '1.8'
    group = 'org.github.jamsa.sc'
    version = '0.0.1'

    if(name=='api'){
        // API类工程的基本依赖
        dependencies {
            compile libs.'spring-web'
        }
    }else{
        // Feign客户端工程的基本依赖
        dependencies {
            compile libs.'feign'
            compile libs.'eureka-client'
        }
    }

    //设置打包参数
    tasks.withType(Jar) {
        //包名为 sc-项目名-模块名，如果父项目为根项目，则不添加“项目名”
        archivesBaseName = "sc-"+(project.parent==rootProject?project.name:project.parent.name+"-"+project.name)
        baseName = archivesBaseName
    }
}

```

需要排除的分类目录，在`ext.excludeFolds`中维护，`subprojects`根据这个配置项进行排除。`subprojects`段中集中处理各模块的公共依赖和Gradle插件，如`api`模块都不需要依赖`spring boot`插件，但是需要`spring-web`；自动处理打包参数，设置打包名称。

这样处理后`api`类的子模块如果没有其它依赖，就不再需要添加`build.gradle`。`service`类的包，则只需要声明依赖和为`jar`任务指定`Main-Class`。

需要注意的是`io.spring.dependency-management`，这个依赖管理插件。由于SpringCloud组件较多依赖关系复杂，使用该插件才能正确的配置好版本间的依赖关系，该插件能自动根据`springCloud`版本号自动选择下面那些相依赖的组件的版本。而上面指定的spring版本也是根据依赖查询到的版本号。

`buildscript`中的内容主要处理gradle `spring boot`插件，该插件主要用于打包FatJar。因此，在API工程中不需要启用这一插件。

## `provider:service`的build.gradle

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

它声明了依赖于`:provider:api`并设定了`Main-Class`。
