Title: Better Builds With Maven 学习笔记
Date: 2009-09-21
Modified: 2009-09-21
Category: 开发
Tags: maven

# 开始
## 准备使用Maven
Maven默认读取<user_home>/.m2/settings.xml，通过proxy段的配置设置代理信息。通过mirror段设置镜像服务器。这两个配置在M2_HOME/conf/settings.xml中都有范例。将M2_HOME/bin添加到环境变量。运行
```
mvn -version
```
查看使用的Maven版本信息。

### 找到的相关资料
配置环境变量M2_HOME为Maven2的安装目录，这样即使是在使用maven-ant-tasks时也读取M2_HOME/conf/settings.xml。

在mirrors段添加镜像配置，当前比较快的国内镜像是：
```
 <mirror>
      <id>redv.com</id>
      <url>http://mirrors.redv.com/maven2</url>
      <mirrorOf>central</mirrorOf>
      <!-- Shanghai, China -->
    </mirror>
```

## 创建第一个Maven工程
使用Maven的`Archetype`机制创建第一个工程。Archetype被定义为原始的模式或模型，从它可以生成同一类型的东西。在Maven中，Archetype是工程的模板，它与用户输入的一些信息组合起来生成一个全功能的Maven工程。

创建工程
```
mvn archetype:create -DgroupId=com.mycompany.app -DartifactId=my-app
```
将创建一个my-app目录，目录中包含了一个pom.xml文件，它的内容如下：
```
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.mycompany.app</groupId>
  <artifactId>mvn-app</artifactId>
  <packaging>jar</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>mvn-app</name>
  <url>http://maven.apache.org</url>
  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>3.8.1</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
</project>
```
src目录包含了构建、测试、创建文档、部署工程所需的输入信息。

## 编译应用程序源码
进入<my-app>目录，执行：
```
mvn compile
```
将编译源码。Maven遵循“约定优于配置”的原则，这是Maven的第一个原则。默认情况下，源码放在src/main/java中。这个默认值并不会出现在POM文件中，实际上，它是从父级（根级）POM继承过来的。编译后的classes保存目录也是同样的方式处理的，默认它放在target/classes目录下。

是什么编译了应用程序源码？这是Maven的第二个原则“重用构建逻辑”。默认配置中配置了标准编译插件，它用于编译应用程序源码。同样的编译逻辑可以重用于其它的工程中。

上面了解了Maven如何找到应用程序源码，Maven怎样来编译应用源码，怎样调用编译插件。接下来的问题是，Maven如何能获取编译器插件？在Maven的标准安装中，找不到编译插件，因为它不是与Maven发布版一起发布的。Maven将在需要插件时自动下载插件。

当第一次执行编译命令（或其它任何命令），Mave将下载这个命令需要的插件及其依赖的其它插件。下次再执行同样的命令时，Maven将不再下载它，命令执行将快很多。

## 编译测试源码执行单元测试
```
mvn test
```
将进行单元测试。这时Maven将下载更多需要的插件。在执行单元测试前，Maven将编译主代码。
```
mvn test-compile
```
编译测试代码。但是当执行mvn test时总是会先执行compile和test-compile。

## 打包并安装到本地仓库
生成jar包执行
```
mvn package
```
查看工程的POM文件可以看到packaging元素被设置为jar。Maven通过这个设置了解到需要生成一个JAR文件。

安装到本地仓库
```
mvn install
```
可以通过修改settings.xml的localRepository设置仓库的位置。

注意：Surefire插件（它执行test）将按特定的命名约定查看测试代码。默认情况下，下面的测试将被包含：
```
**/*Test.java
**/Test*.java
**/*TestCase.java
```
下面的将不被包含：
```
**Abstract*Test.java
**/Abstract*TestCase.java
```

Maven的重用构建逻辑使得即使是使用默认的POM文件也可以执行大量基础构建操作，例如：
```
mvn site
```
可以为工程生成一个简单网站。

```
mvn clean
```
将清除target目录下旧的构建数据。

```
mvn idea:idea
```
可以产生一个IDEA工程。

```
mvn eclipse:eclipse
```
生成一个eclipse工程。

## 处理Classpath资源
src/main/resources是Maven推荐的保存资源文件的目录。可以将需要打包到JAR文件的资源放到这个目录。Maven使用的规则是所有放在src/main/resources目录下的文件和目录都将打包到JAR中。

默认生成的JAR文件中包含了META-INF目录。在这个目录下可以找到MANIFEST.MF和pom.xml和pom.properties。你可以创建自己的mainfest文件，如果不创建Maven将自动生成一个。也可以包含自己的资源文件，例如在src/main/resources目录下添加一个application.properties文件，重新打包则资源文件也将也现在JAR包中。

pom.xml和pom.properties文件被打包到JAR以便由Maven的每个artifact生成的JAR包都是自描述的，并且允许你包含自己的应用中的原数据。最简单的应用可能就是用于获取应用的版本号。操作POM文件需要使用Maven的工具，但是propertiest文件却可以使用标准Java API。

### 处理测试用Classpath的资源
添加资源到单元测试classpath，可以将资源添加到src/test/resources目录。在单元测试中，使用下面的代码片段在测试阶段访问资源：
<src lang="java">
// Retrieve resource
InputStream is = getClass().getResourceAsStream( "/test.properties" );
// Do something with the resource
</src>

可以使用下面的配置覆盖maven-jar-plugin的默认配置：
```
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-jar-plugin</artifactId>
  <configuration>
    <archive>
      <manifestFile>META-INF/MANIFEST.MF</manifestFile>
    </archive>
  </configuration>
</plugin>
```

### 过滤Classpath资源
有时资源文件中包含的一些值在构建时才能提供。Maven中可以使用资源过滤，动态的将资源属性值设置到资源文件中。将资源文件中的属性值设置为${<property name>}，这个属性可以是pom.xml或用户的settings.xml中定义的属性，或定义在外部properties文件，或都是系统属性。

需要将pom.xml中将需要进行过滤处理的资源目录的filtering属性设置为true。例：
```
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.mycompany.app</groupId>
  <artifactId>my-app</artifactId>
  <packaging>jar</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>Maven Quick Start Archetype</name>
  <url>http://maven.apache.org</url>
  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>3.8.1</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <resources>
      <resource>
        <directory>src/main/resources</directory>
        <filtering>true</filtering>
      </resource>
    </resources>
  </build>
</project>
```

使用资源过滤的举例：创建src/main/resources/META-INF/application.properties，内容设置为：
```
# application.properties
application.name=${project.name}
application.version=${project.version}
```
执行
```
mvn process-resources
```
target/classes目录下的application.properties文件内容将变为：
```
# application.properties
application.name=Maven Quick Start Archetype
application.version=1.0-SNAPSHOT
```

如果需要引用外部propertiest文件中的属性值，需要在pom.xml中添加对外部文件的引用。例如，创建一个外部资源文件src/main/filters/filter.properties：
```
# filter.properties
my.filter.value=hello!
```
将对它的引用添加到pom.xml中：
```
<build>
  <filters>
    <filter>src/main/filters/filter.properties</filter>
  </filters>
  <resources>
    <resource>
      <directory>src/main/resources</directory>
      <filtering>true</filtering>
    </resource>
  </resources>
</build>
```
然后在application.propertiest文件中引用对应的属性：
```
# application.properties
application.name=${project.name}
application.version=${project.version}
message=${my.filter.value}
```
再次执行mvn process-resources命令时会将message替换为外部文件中my.filter.value属性对应的值。

也可以在pom文件的properties段定义这些属性值。例如：
```
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.mycompany.app</groupId>
  <artifactId>my-app</artifactId>
  <packaging>jar</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>Maven Quick Start Archetype</name>
  <url>http://maven.apache.org</url>
  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>3.8.1</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <resources>
      <resource>
        <directory>src/main/resources</directory>
        <filtering>true</filtering>
      </resource>
    </resources>
  </build>
  <properties>
    <my.filter.value>hello</my.filter.value>
  </properties>
</project>
```
资源过滤也可以获取系统属性，也可以是编译到Java中的（java.version或user.home），或使用Java -D参数在命令行指定的属性。例如将application.propertiest文件设置为：
```
# application.properties
java.version=${java.version}
command.line.prop=${command.line.prop}
```
然后执行下面的命令：
```
mvn process-resources "-Dcommand.line.prop=hello again"
```

### 防止过滤二进制资源
某些情况下我们不希望属性过滤处理某些资源文件。比如图像文件。

比如src/main/resources/images不希望被过滤，这时应该排除这些资源。pom.xml设置如下：
```
<project>
  [...]
  <build>
    <resources>
      <resource>
        <directory>src/main/resources</directory>
        <filtering>true</filtering>
        <excludes>
          <exclude>images/**</exclude>
        </excludes>
      </resource>
      <resource>
        <directory>src/main/resources</directory>
        <includes>
          <include>images/**</include>
        </includes>
      </resource>
    </resources>
  </build>
  [...]
</project>
```

## 使用Maven插件
配置Maven插件的参数。

例如，指定Java编译器只允许编译JDK 5.0的源码。可以在POM中添加设置：
```
<project>
  [...]
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>2.0</version>
        <configuration>
          <source>1.5</source>
          <target>1.5</target>
        </configuration>
      </plugin>
    </plugins>
  </build>
  [...]
</project>
```
Maven 2的插件和工程的依赖很相似，在某种程度上它们确实如此。如果在本地找不到插件，则将自动下载插件，这更是与依赖关系的处理相同。插件与依赖同相样有groupId和version元素，但多数情况下这些元素不需要。

如果不指定groupId，则Maven将搜索org.apache.maven.plugins或org.codehause.mojo这两个groupId。你也可以在POM或settings.xml中指定goupId。

如果不指定版本Maven将尝试获取指定插件的最新版本。

通过mvn help:describe命令可以找到插件可选配置项。例如：
```
mvn help:describe -DgroupId=org.apache.maven.plugins \
 -DartifactId=maven-compiler-plugin -Dfull=true
```
也可以在 http://maven.apache.org/plugins/ 使用Maven Plugin Reference找到相关插件的配置信息。

# 使用Maven创建应用
## 介绍
将要创建的应用名叫Proficio，拉丁语的"help"。

## 设置应用程序的目录结构
在设置Proficio的目录结构时，注意Maven强调的实践标准化和构建模块化构建是很重要的。

这种实践自然将产生分离的可重用的开发工程。决定如何最优化的分解应用的原则叫做“分离关注点（Separation of Concerns）”原则，即SoC原则。

SoC有助于识别、封装、操作于有相关特殊概念、目标、任务或目的的软件片段。关注点是组织和分解软件的动力，更多的易于管理和理解的部分，每个都用于说明一个或多个特定关注点。

如上所述，Proficio样例工程将被设置为多个Maven模块：

  - Proficio API：Proficio的应用编程接口，它包含了一套接口。这些接口是主要组件（例如store）的API。

  - Proficio CLI：提供Proficio的命令行接口。

  - Proficio Core：API的实现。

  - Proficio Model：Proficio应用的数据模型，它包含了将被整个Proficio工程所使用的所有的类。

  - Proficio Stores：这个模块处理包含所有的存储模块。Proficio有一个简单的memory-based和XStream-based存储。

在Proficio的顶层POM中，可以看到所有子模块元素。一个模块指向另一个Maven工程，实际上它是指向另一个POM。Proficio的顶层POM文件如下：
```
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.devzuz.mvnbook.proficio</groupId>
  <artifactId>proficio</artifactId>
  <packaging>pom</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>Maven Proficio</name>
  <url>http://maven.apache.org</url>
  [...]
  <modules>
    <module>proficio-model</module>
    <module>proficio-api</module>
    <module>proficio-core</module>
    <module>proficio-stores</module>
    <module>proficio-cli</module>
  </modules>
  [...]
</project>
```
上面的版本号1.0-SNAPSHOT。对于一个有多模块的应用，通常将所有模块一起发布，所有模块使用一个公共的版本号。这是推荐的一种方式。

注意上面的packaging元素，这里它被设置为pom。对于包含模块的POM文件，packaging必须设置为pom：这告诉Maven你准备创建一个模块集。

Proficio应用的模块打包类型：
模块 || 打包类型
proficio-api | jar
proficio-cli | jar
proficio-core | jar
proficio-module | jar
proficio-stores | pom

proficio-stores模块有两个子模块。

## 使用工程继承
Maven最重要的功能之一就是工程继承。使用工程继承允许你在一个地方规定组织机构信息，规定部署信息，或规定通用的依赖。由Proficio工程产生的每个工程的POM文件，每个的顶部都有：
```
[...]
<parent>
  <groupId>com.devzuz.mvnbook.proficio</groupId>
  <artifactId>proficio</artifactId>
  <version>1.0-SNAPSHOT</version>
</parent>
[...]
```
这个片段允许你从指定的顶层的POM继承。顶层POM中指定了依赖JUnit 3.8.1。在这种情况下子工程中不再申明这个依赖也可以使用这个包。

为了了解在继承处理时发生的东西可以执行mvn help:effective-pom命令。这个命令将显示出最终的POM。在proficio的子工程中执行这个命令时可以看到依赖中出现了JUnit 3.8.1。

## 管理依赖关系
Maven可以让不同的工程共享程序包。

可以在顶层的POM中描述所有子工程共享的依赖。

例如Proficio的顶层POM：
```
<project>
  [...]
  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>com.devzuz.mvnbook.proficio</groupId>
        <artifactId>proficio-model</artifactId>
        <version>${project.version}</version>
      </dependency>
      <dependency>
        <groupId>com.devzuz.mvnbook.proficio</groupId>
        <artifactId>proficio-api</artifactId>
        <version>${project.version}</version>
      </dependency>
      <dependency>
        <groupId>com.devzuz.mvnbook.proficio</groupId>
        <artifactId>proficio-store-memory</artifactId>
        <version>${project.version}</version>
      </dependency>
      <dependency>
        <groupId>com.devzuz.mvnbook.proficio</groupId>
        <artifactId>proficio-store-xstream</artifactId>
        <version>${project.version}</version>
      </dependency>
      <dependency>
        <groupId>com.devzuz.mvnbook.proficio</groupId>
        <artifactId>proficio-core</artifactId>
        <version>${project.version}</version>
      </dependency>
      <dependency>
        <groupId>org.codehaus.plexus</groupId>
        <artifactId>plexus-container-default</artifactId>
        <version>1.0-alpha-9</version>
      </dependency>
    </dependencies>
  </dependencyManagement>
  [...]
</project>
```
注意${project.version}指定了版本，它与应用的版本对应。

在dependencyManagement一节，有多个Proficio依赖并且还依赖于Plexus IoC container。dependencyManagment元素与顶层POM的dependencies有重要区别。

dependencyManagement元素中包括的dependencies元素仅用于说明引用的版本号，对并不影响工程的依赖关系图，然而顶层的dependencies元素将影响依赖关系图。查看proficio-api模块的POM将只看到引用而没有指定版本：
```
<project>
  [...]
  <dependencies>
    <dependency>
      <groupId>com.devzuz.mvnbook.proficio</groupId>
      <artifactId>proficio-model</artifactId>
    </dependency>
  </dependencies>
</project>
```
这个依赖的版本号是从Proficio的顶层POM文件的dependencyManagement继承过来的。dependencyManagement指定了引用proficio-model的版本号为1.0-SNAPSHOT（被设置为${project.version}）这个版本号将注入到上面的依赖中。dependencyManagement中说明的dependencies只用于当某个依赖没有版本号的情况。

## 使用快照
当开发的应用具有多个模块时，通常每个模块的版本都在变更。API可能正在经历变迁或你的实现正在发生改变，或者在进行重构。你在构建时需要非常容易的实时获取最新版本，这是Maven的快照（snapshot）的概念。快照是Maven的一个artifact。查看Proficio的顶层POM可以看到指定了快照版本。
```
<project>
  [...]
  <version>1.0-SNAPSHOT</version>
  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>com.devzuz.mvnbook.proficio</groupId>
        <artifactId>proficio-model</artifactId>
        <version>${project.version}</version>
      </dependency>
      <dependency>
        <groupId>com.devzuz.mvnbook.proficio</groupId>
        <artifactId>proficio-api</artifactId>
        <version>${project.version}</version>
      </dependency>
      <dependency>
        <groupId>org.codehaus.plexus</groupId>
        <artifactId>plexus-container-default</artifactId>
        <version>1.0-alpha-9</version>
      </dependency>
    </dependencies>
  </dependencyManagement>
  [...]
</project>
```

    指定快照版本作为依赖时Maven将会查找新版本而不像手工指定版本时那样操作。快照依赖假定总是在变更，因此Maven将尝试更新它们。默认情况下Maven将以天为单位查找新版本，但你可以使用命令行参数-U来强制它查找新版本。当指定非快照的依赖时Maven将下载依赖并且不会进行重试。

## 解决依赖冲突和使用版本号范围
在Maven 2.0中通过引入依赖传递，使得可以在简单的POM文件中只指定你直接需要的依赖，并且Maven可以计算出完整的依赖关系图。但是，随着图的增涨，不可避免的将产生一个或多个artifacts需要依赖的不同版本。这种情况下，Maven必须选择使用哪个版本。

Maven通常选择这个关系树中顶层的“最接近的版本（nearest）”，Maven选择版本号跨度最小的版本。如果在POM中指定了版本，则将被使用而不管其它的原因。但这种方式也有下面的限制：

 - 选择的版本可能没有某个依赖的组件所需要的功能。

 - 如果在相同的级别先择了多个不同的版本，则结果将是不明确的。

手工解决冲突，可以从依赖树中移除不正确的版本，或者可以用正确的版本来覆盖掉树中的版本。移除不正确的版本需要在运行Maven时指定-X标识来找出不正确的版本。例如，如果在proficio-core模块运行mvn -X test将输出：
```
proficio-core:1.0-SNAPSHOT
  junit:3.8.1 (selected for test)
  plexus-container-default:1.0-alpha-9 (selected for compile)
    plexus-utils:1.0.4 (selected for compile)
    classworlds:1.1-alpha-2 (selected for compile)
    junit:3.8.1 (not setting scope to compile; local scope test wins)
  proficio-api:1.0-SNAPSHOT (selected for compile)
    proficio-model:1.0-SNAPSHOT (selected for compile)
    plexus-utils:1.1 (selected for compile)
```
这样可以找出当前操作所使用的详细版本信息，一旦找出了不正确的版本，你可以将它从依赖关系图中移除。例如，这个例子中，plexus-utils出现了两次，Proficio需要1.1版。为确保这个依赖，可以修改plexus-container-default的依赖，例如：
```
<dependency>
  <groupId>org.codehaus.plexus</groupId>
  <artifactId>plexus-container-default</artifactId>
  <version>1.0-alpha-9</version>
  <exclusions>
    <exclusion>
      <groupId>org.codehaus.plexus</groupId>
      <artifactId>plexus-utils</artifactId>
    </exclusion>
  </exclusions>
</dependency>
```
这保证了Maven将忽略1.04版的plexus-utils，而使用1.1版。

另一种方法确保在依赖中使用特定版本，是将它直接包含在POM中，例：
```
<dependencies>
  <dependency>
    <groupId>org.codehaus.plexus</groupId>
    <artifactId>plexus-utils</artifactId>
    <version>1.1</version>
    <scope>runtime</scope>
  </dependency>
</dependencies>
```
但是这种方式是不被推荐的除非你是在制作一个绑定了自己的依赖的artifact，并且它自身不会作为一个依赖（例如，是一个WAR文件）。原因是这种做法歪曲了真实的依赖关系图，在工程自身作为依赖被重用时将导致问题。

在这里指定了runtime作用范围。这是因为，在这种情况下，依赖只是用于打包而不是编译。实际上，如果依赖是在编译时需要，它应该总是出现在当前POM的依赖中——而不管另一个依赖是否使用了它。

上面的这些解决都只是理想化的，但它可以提高你自己的依赖的质量，避免你在构建自己的产品时的风险。这一点在构建一个应用程序框架时是非常重要的，因为它将广泛的被其它人使用。为达到这个目标，可以使用版本范围来替代这种方式。

当上面的plexus-utils的版本被设置为1.1时，标明首选依赖的是1.1版，但其它版本可能也能够接受。Maven并不知道哪个版本可以工作，因此当与其它依赖冲突时，Maven确保所有的版本使用前面描述的“最近依赖（nearest dependency）”技术来决定使用哪个版本。

但是，你可能需要一个plexus-utils 1.1版中的功能。这时，依赖应该指定为下面的形式：
```
<dependency>
  <groupId>org.codehaus.plexus</groupId>
  <artifactId>plexus-utils</artifactId>
  <version>[1.1,)</version>
</dependency>
```
这表示在版本冲突时仍将使用nearest dependency技术，但是版本号必须符合给定的范围。如果版本不匹配，则下一个最接近的版本将被测试，如此继续。最后，如果没有匹配的版本，或本来就没有冲突，则使用指定的版本[1.1,)。这表示将从仓库中获取最小的版本号大于或等于1.1的版本。

版本范围范例表：

范围 || 含义
(,1.0] | 小于或等于1.0
[1.2,1.3] | 处于1.2和1.3之间（含1.3）
[1.0,2.0) | 大于或等于1.0，但小于2.0
[1.5,) | 大于或等于1.5
(,1.1),(1.1,) | 除1.1外的任何版本

通过指定使用的版本范围，使得构建时依赖管理机制更加可靠并且减少异常的情况。但应该避免过度的详细。例如，如果两个版本范围依赖图不交叉，那么构建将失败。

为了解版本范围是如何工作的，需要了解版本是怎样进行比较的。下面展示了Maven是如何分割版本号的。
```
1.0.1-20060211.131141-1
```
从左至右依次为：

1为主版本号

0为次版本号

1为Bug修正号

20060211.131141为限定版本号

1为构建号

在目前的版本方案中，快照版本是一种特殊的情况，在这种情况下限定号和构建号可以同时存在。在正式版本中，可以只提供限定号或只提供构建号。有意设置的限定号标识出了一个较优先的版本（例如：alpha-1，beta-1，rc1）。对于快照版本，限定号必须是文本“snapshot”或时间戳。构建号是一个自增号在发布时标明是补丁构建。

版本中的元素依次决定哪个版本较新——首先是主版本号，如果主版本号相等，则比较次版本号，接下来是Bug修正号，限定号，最后比较构建号。带限定号的版本比不带限定号的版本要旧；比如1.2-beta比1.2旧。包含了构建号的版本比不带构建号的版本新；比如1.2-beta-1比1.2-beta新。某些情况下，版本可能会不匹配这个语法。在这些情况下，两个版本号将作为字符串进行比较。

当使用快照版本测试编译发布版本或自己测试发布测试版本时应该将它们部署到快照仓库，这将在第七章讨论。这保证了在版本范围中的beta版本才会使用，除非工程显式的申明了使用快照版本。

最后要注意的是当使用版本范围时版本更新是如何被决定的。这个机制与前面介绍的快照版本更新机制是相同的，即每天从版本库中更新一次版本。但是，这可以通过配置每个仓库来设置更新的频率，或在命令行使用-U参数强制Maven执行更新。

例：
```
<repository>
  [...]
  <releases>
    <updatePolicy>interval:60</updatePolicy>
  </releases>
</repository>
```

## 利用构建生命周期
第二章中将Maven描述为一个正确调整插件执行方式或顺序的应用框架，这实际上就是Maven的默认构建生命周期。Maven默认的构建生命周期对于大多数工程来说不需要增加任何内容就可以满足了——当然，有时工程需要增加不同的内容到Maven的默认构生命周期来满足构建的需求。

例如，Proficio需要从model生成Java源码。Maven通过允许申明插件来满足这个需求，将它绑定到Maven默认生命周期的一个标准阶段——generate-sources阶段。

Maven的插件是为特定任务而创建的，这意味着插件将被绑定到默认的生命周期的一个特定阶段。在Proficio中，Modello插件被用于生成Proficio的数据模型的Java源码。查看proficio-model的POM可以看到plugins元素配置了Modello插件。
```
<project>
  <parent>
    <groupId>com.devzuz.mvnbook.proficio</groupId>
    <artifactId>proficio</artifactId>
    <version>1.0-SNAPSHOT</version>
  </parent>
  <modelVersion>4.0.0</modelVersion>
  <artifactId>proficio-model</artifactId>
  <packaging>jar</packaging>
  <name>Proficio Model</name>
  <build>
    <plugins>
      <plugin>
        <groupId>org.codehaus.modello</groupId>
        <artifactId>modello-maven-plugin</artifactId>
        <version>1.0-alpha-5</version>
        <executions>
          <execution>
            <goals>
              <goal>java</goal>
            </goals>
          </execution>
        </executions>
        <configuration>
          <version>1.0.0</version>
          <packageWithVersion>false</packageWithVersion>
          <model>src/main/mdo/proficio.mdo</model>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```
这与第二章中maven-compiler-plugin的申明非常相似，但这里可以看到额外的execution元素。Maven中的插件可以有多个goal，因此你需要指定你希望运行插件的哪个goal，这可以通过在execution中的goal元素来指定。

## 使用Profiles
Profile是Maven提供的用于创建构建生命周期中的不同环境变量、不同的平台、不同JVM、不同的测试数据库、或引用不同的本地文件系统的方法。通常你可以在POM中封装，以保证构建的可移植性，但有时你需要考虑变化的交叉系统的情况，这也是Maven中引入profile的原因。

Profile使用POM中的一个子集元素来指定，可以用多种方式来启用。Profile在构建时修改POM，意味着它将用于给不同的目标环境中的参数集（比如，在开发环境、测试环境、产品环境下应用服务器根路径）不同参数值。

Profile也可以很容易的实现团队中不同成员生成不同的构建结果。也可以通过profile阻止构建的移植性。Profile可以定义在下面三个地方：

 - Maven的配置文件（通常是<user_home>/.m2/settings.xml）

 - 与POM同一目录下的名为profiles.xml的文件

 - POM文件中

优先级依次为POM文件、profiles.xml、settings.xml。这也是Maven中的基本原则。

settings.xml中设置profile会影响所有的构建，因此它适合“全局”的profiles。profiles.xml允许设置单个工程的构建而不用修改POM。基于POM的profiles是首选方式，因为这样更具有移植性（它们将在布署时发布到仓库，对于源于仓库的子构建或依赖来说也同样有效）。

因为移植性的原因，那些不会发布到仓库中的文件不允许修改任何基础构建。因此，profiles.xml和settings.xml只允许定义：

 - 仓库repositories

 - 插件仓库pluginRepositories

 - 属性properties

其它的信息必须在POM的profile中指定或在POM自身指定。例如，如果settings.xml中有一个profile它可以注入一个依赖，你的工程运行需要settings注入的依赖，一旦这个工程部部署到仓库中它将不能解决它的依赖。因为其中一个依赖设置在settings.xml的profile中了。

注意：respositories、pluginRepositories和properties也可以在POM内部的profiles指定。因此，在POM外部指定的profiles只允许使用POM内部指定的profiles选项的一个小的子集。

可以在POM中定义的profile：

 - repositories

 - pluginRepositories

 - dependencies

 - plugins

 - properties(not actually available in the main POM, but used behind the scenes)

 - modules

 - reporting

 - dependencyManagement

 - distributionManagement

构建元素的子集，由下面组成：

 - defaultGoal

 - resources

 - testResources

 - finalName

有多种方法启用profiles：

 - 在命令行上使用-P选项。这个选项接收以逗号名分隔的profile的id列表。当指定这个选项时，这些指定在参数中的profiles将被激活。例：
```
mvn -Pprofile1,profile2 install
```

 - Profiles可以在Maven settings文件通过activeProfiles段中激活。这段接收activeProfile元素的列表，每个都包括了一个profile-id。注意你必须在settings.xml文件中定义了这些profiles。例：
```
<settings>
  [...]
  <profiles>
    <profile>
      <id>profile1</id>
      [...]
    </profile>
  </profiles>
  <activeProfiles>
    <activeProfile>profile1</activeProfile>
  </activeProfiles>
  [...]
</settings>
```

 - Profiles可以在检测到构建环境时自动触发。这些在profile的activation段设置。目前这种检测仅限于匹配JDK版本号的前缀、当前系统属性或系统属性的值。例如：
```
<profile>
  <id>profile1</id>
  [...]
  <activation>
    <jdk>1.4</jdk>
  </activation>
</profile>
```
  这个激器将在JDK的版本以1.4开始时被触发。
```
<profile>
  <id>profile1</id>
  [...]
  <activation>
    <property>
      <name>debug</name>
    </property>
  </activation>
</profile>
```
  上面的profile将在系统属性debug被指定时被触发。
```
<profile>
  <id>profile1</id>
  [...]
  <activation>
    <property>
      <name>environment</name>
      <value>test</value>
    </property>
  </activation>
</profile>
```
  最后的这个例子将在系统属性environment属性设置为true时激活。

在熟悉profiles后，可以使用它组装不同的Proficio系统：一个配置方案是memory-base存储，另一个是XStream-based存储。这些将在proficio-cli模块中使用。proficio-cli模块的profile定义如下：
```
<project>
 [...]
 <!-- Profiles for the two assemblies to create for deployment -->
 <profiles>
  <!-- Profile which creates an assembly using the memory based store -->
  <profile>
   <id>memory</id>
   <build>
    <plugins>
     <plugin>
      <artifactId>maven-assembly-plugin</artifactId>
      <configuration>
       <descriptors>
        <descriptor>src/main/assembly/assembly-store-memory.xml</descriptor>
       </descriptors>
      </configuration>
     </plugin>
    </plugins>
   </build>
   <activation>
    <property>
     <name>memory</name>
    </property>
   </activation>
  </profile>
  <!-- Profile which creates an assembly using the xstream based store -->
  <profile>
   <id>xstream</id>
   <build>
    <plugins>
     <plugin>
      <artifactId>maven-assembly-plugin</artifactId>
      <configuration>
       <descriptors>
        <descriptor>src/main/assembly/assembly-store-xstream.xml</descriptor>
       </descriptors>
      </configuration>
     </plugin>
    </plugins>
   </build>
   <activation>
    <property>
     <name>xstream</name>
    </property>
   </activation>
  </profile>
 </profiles>
</project>
```
可以看到两个profiles：一个id为memory另一个id为xstream。在每个profile中你可以配置插件。也可以看到profile通过一个系统属性进行激活。这个例子依赖于前面已经执行过的一些构建步骤，因此应该先在工程的顶级目录执行mvn install确保需要的组件被安装到本地仓库。

如果想基于memory-based存储进行构建，可以执行：
```
mvn -Dmemory clean assembly:assembly
```
如果想基于XStream-based存储进行，可以执行：
```
mvn -Dxstream clean assembly:assembly
```
这两种方式构建的结果都保存在target目录中，如果对输出使用jar tvf命令，可以看到memory-base方式构建时只包含了proficio-store-memory-1.0-SNAPSHOT.jar，当使用XStream-based方式时，只包含了proficio-store-xstream-1.0-SNAPSHOT.jar。

## 部署应用
当前Maven支持多种部署方式包括文件系统部署、SSH2部署、SFTP部署、FTP部署和外部SSH部署。为了进行部署，需要正确的配置POM中的distributionManagement元素，通常是在顶级POM中，因为子POM可以继承这些信息。

### 文件系统部署
```
<project>
  [...]
  <distributionManagement>
    <repository>
      <id>proficio-repository</id>
      <name>Proficio Repository</name>
      <url>file://${basedir}/target/deploy</url>
    </repository>
  </distributionManagement>
  [...]
</project>
```

### SSH2部署
```
<project>
  [...]
  <distributionManagement>
    <repository>
      <id>proficio-repository</id>
      <name>Proficio Repository</name>
      <url>scp://sshserver.yourcompany.com/deploy</url>
    </repository>
  </distributionManagement>
  [...]
</project>
```

### SFTP部署
```
<project>
  [...]
  <distributionManagement>
    <repository>
      <id>proficio-repository</id>
      <name>Proficio Repository</name>
      <url>sftp://ftpserver.yourcompany.com/deploy</url>
    </repository>
  </distributionManagement>
  [...]
</project>
```

### 外部SSH部署
前面三个部署方式是包含在Maven内部的，因此只需要distributionMangement元素，但使用外部SSH命令部署则还要使用一个构建扩展。
```
<project>
  [...]
  <distributionManagement>
    <repository>
      <id>proficio-repository</id>
      <name>Proficio Repository</name>
      <url>scpexe://sshserver.yourcompany.com/deploy</url>
    </repository>
  </distributionManagement>
  <build>
    <extensions>
      <extension>
        <groupId>org.apache.maven.wagon</groupId>
        <artifactId>wagon-ssh-external</artifactId>
        <version>1.0-alpha-6</version>
      </extension>
    </extensions>
  </build>
  [...]
</project>
```
这个构建扩展指定使用Wagon外部SSH提供都，它将你的文件移动到远程服务器上。Wagon是Maven中通用的用于传送的机制。

### FTP部署
FTP部署也必须指定一个构建扩展。
```
<project>
  [...]
  <distributionManagement>
    <repository>
      <id>proficio-repository</id>
      <name>Proficio Repository</name>
      <url>ftp://ftpserver.yourcompany.com/deploy</url>
    </repository>
  </distributionManagement>
  <build>
    <extensions>
      <extension>
        <groupId>org.apache.maven.wagon</groupId>
        <artifactId>wagon-ftp</artifactId>
        <version>1.0-alpha-6</version>
      </extension>
    </extensions>
  </build>
  [...]
</project>
```
一旦配置完POM后，可以执行
```
mvn deploy
```
进行部署。

## 为应用程序创建Web站点
前面已经完成了Proficio的构建、测试、部署，现在可以为这个应用创建一个标准的Web站点。对于Procio这样的应，推荐在顶级目录创建用于生成站点的资源目录。

所有用于生成站点的文件保存在src/site目录。src/site目录中也有子目录保存支持文档。Maven支持大量同的文件格式。

当前支持得最好的格式：

 - XDOC格式，它是一个被Apache广泛使用的简单的XML格式。

 - APT（Almost Plain Text）,与wiki格式类似的格式。

 - FML格式，FAQ格式。一个简单的XML格式管理FAQ。

 - DocBook Simple格式，它是一个比完整的DocBook格式简单一些的格式。

Maven也有限的支持：

 - Twiki格式，这是一种流行的Wiki格式。

 - Confluence格式，这是另一种流行的Wiki格式。

 - DocBook格式。

在后面的章节将了解支持较好的那些格式，但你应该熟悉下面的目标：

 - 配置banner的外观。

 - 配置站点的皮肤。

 - 配置发布数据的格式。

 - 配置banner下显示的链接。

 - 配置放入生成的页面的<head/>元素中的信息。

 - 配置显示在导航栏中的菜单项。

 - 配置项目报表的外观。

查看Proficio应用的src/site可以看到站点的描述：
```
<project name="Proficio">
  <bannerLeft>
    <name>Proficio</name>
    <href>http://maven.apache.org/</href>
  </bannerLeft>
  <bannerRight>
    <name>Proficio</name>
    <src>http://maven.apache.org/images/apache-maven project.png</src>
  </bannerRight>
  <skin>
    <groupId>org.apache.maven.skins</groupId>
    <artifactId>maven-default-skin</artifactId>
    <version>1.0-SNAPSHOT</version>
  </skin>
  <publishDate format="dd MMM yyyy" />
  <body>
    <links>
      <item name="Apache" href="http://www.apache.org/"/>
      <item name="Maven" href="http://maven.apache.org/"/>
      <item name="Continuum" href="http://maven.apache.org/continuum"/>
    </links>
    <head><meta name="faq" content="proficio"/></head>
    <menu name="Quick Links">
      <item name="Features" href="/maven-features.html"/>
    </menu>
    <menu name="About Proficio">
      <item name="What is Proficio?" href="/what-is-maven.html"/>
    </menu>
    ${reports}
  </body>
</project>
```
这是一个相当标准的Web站点描述，每个元素的说明如下：

站点描述元素 || 说明
bannerLeft and bannerRight | 这些元素包括名称、href和可选的src元素，可以用于图像。
skin | 这个元素看起来像是依赖的描述（使用了相同的机制来获取皮肤）控制站点使用的皮肤。
publishDate | 发布日期的格式，使用的Java类中的SimpleDateFormat。
body/links | 控制banner下的链接引用只需要name和href。
body/head | head元素允许你插入任何信息到生成的页面。可以加metadata、script（如Google Analytics）。

Maven中最流行的功能之一就是花较少的功夫就可以生成标准的报表。只要简单的在站点描述中包含${reports}引用，默认情况下是包含的，工程信息报表将自动生成的被添加上来。标准的工程信息报表包含下面的内容：

 - 依赖关系报告

 - 邮件列表报告

 - 持续集成报告

 - 源码仓库报告

 - 发行版本跟踪报告

 - 工程团队报告

 - 版权

尽管标准报表很有用，通常你需要自定义工程的报表。报表的创建和显示控制是在POM的build/reports元素中。你可以选择生成报表的信息，只要列举出需要包含在站点中的报表即可。这个插件的配置方式如下：
```
<project>
  [...]
  <reporting>
    [...]
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-project-info-reports-plugin</artifactId>
        <reportSets>
          <reportSet>
            <reports>
              <report>dependencies</report>
              <report>project-team</report>
              <report>mailing-list</report>
              <report>cim</report>
              <!--
              Issue tracking report will be omitted
              <report>issue-tracking</report>
              -->
              <report>license</report>
              <report>scm</report>
            </reports>
          </reportSet>
        </reportSets>
      </plugin>
    </plugins>
    [...]
  </reporting>
  [...]
</project>
```
执行
```
mvn site
```
生成站点。

生成的站点放在target目录下。如果有其它的资源，如图片、PDF等可以存放在src/site/resources。当站点被生成时src/site/resources将被复制到站点的顶级目录。

# 构建J2EE应用程序


# 开发Maven插件
如第二章所述，Maven实际上是一个平台，它在构建生命周期中执行插件来执行构建一个项目时需要进行的任务。Maven核心API处理与POM定义相关操作，解决工程的依赖关系，组织和运行插件。实际执行任务或工作是由一套与工程的构建生命周期相关联的插件集来完成的。这使得Maven的插件框架极其重要，不光是在构建工程的过种中，在对工程的功能进行扩展，如集成外部工具和系统时也同样重要。

多数工程中Maven提供的插件足够满足多数构建过程的需要。即使要执行一些特殊的任务，也可能已经存在了这样的插件。可以在Apache Maven project和CodeHaus Mojo project或其它第三方网站找到与Maven集成的插件。如果找不到合适的插件，可能就需要编写客户化插件将这些任务集成到构建生命周期中。

## 回顾插件技术
Mojo是Maven应用的基本工作单元。它执行原子性的构建任务，用于描述构建过程中的单个步骤。一些mojo结合起来完成相关的任务，它们被打包到plugin中。

与Java中的包一样，plugin提供了分组的机制，将在构建生命周期中提供类似功能的多个mojo进行分组。比如，maven-compiler-plugin包含两个mojo：compile和testCompile。在这里，它们的任务都是编译代码。对这些mojo进行打包向用户提供了一致的访问机制，允许共享POM中添加的单个段的配置。另外，它也使mojo之间共享代码更方便。

Mojo描述了构建过程中的单个任务。工程的构建过程包含了一套mojo的集合，它们按定义好的特定顺序执行。这个顺序被称为“构建生命周期”，它被定义为一套任务分类的集合，称为“构建阶段”。当Maven执行构建时，它按生命周期顺序执行每个阶段相关的mojo。

mojo与构建阶段的关系被称为“构建building”。

Maven实际上定义了三个不同的构建周期，这章讨论默认的构建生命周期，它用于主要的构建活动（其它两个处理清理工作目录和生成Web站点）。

多数mojo被分为不同的分类，对应于构建生命周期的阶段。因此，mojo自然的与一个阶段绑定，这决定了在这个周期中的某个任务该在何时执行。由于阶段绑定提供了mojo在生命周期中的分组机制，通过连续的各个阶段可以决定前一个价码应该做什么。因此，为确保与其它插件的兼容，为你的插件提供恰当的阶段绑定是很重要的。

 mojo通常指定了一个默认的阶段绑定，它们可以被绑定到构建过程的任何阶段。甚至，一个mojo可以通过配置工程POM文件的executions段被绑定到同一构建生命周期的多个位置。每个excution可以为它申明的mojo集合指定一个单独的构建阶段。但是，在mojo执行前，它可能需要某些活动先被执行完成，因此应该在重新绑定mojo之前检查文档以了解它。

 某些情况下，mojo可以被设计为独立于构建生命周期之外。比如mojo可能从版本库中检出代码，或为一个新的工程创建目录结构。这些mojo通常是被直接调用的，它们不会与构建生命周期的某个阶段绑定，因为他们不能被自动划分到典型的构建过程中。讨论这些mojo与Maven构建过程本身有些跑题了，因为它们通常是由POM的维护者执行的任务，或通过集成外部开发工具来完成。

## 开始插件开发
为了了解Maven插件开发技术，你需要较好的了解插件是如何构建的以及它们如何与他们的环境进行交互。作为插件开发都，你必须了解构建生命周期阶段的绑定和参数的注入。了解这个框架使你了解每个mojo都需要的Maven构建状态信息，并决定将mojo绑定到哪个构建阶段。

### 插件框架
Maven提为插件供了强大的框架，包括较好的生命周期定义，依赖关系管理，参数解析和注入。通过生命周期，Maven也较好的定义了生成工程发布包等等。将mojo绑定到构建生命周期使得mojo可以知道哪些处理阶段已经完成了。使用Maven的参数注入，使mojo可以获取构建的状态。参数注入和生命周期绑定是所有mojo开发的基础。

#### 参与构建生命周期
大多数插件完全由mojo组成并根据它们的功能被绑定到构建生命周期的各个阶段。例如，某个工程的源码需要被编译并被打包到一个jar文件中以便发布。在这个构建过程中，Maven将为生成‘jar’包执行一个默认的生命周期。‘jar’包过程的定义被绑定到下面的生命周期阶段：

生命周期阶段 || mojo || 插件
process-resources | resources | maven-resources-plugin
compile | compile | maven-compiler-plugin
process-test-resources | testResources | maven-resources-plugin
test-compile | testCompile | maven-compiler-plugin
test | test | maven-surefire-plugin
package | jar | maven-jar-plugin
install | install | maven-install-plugin
deploy | deploy | maven-deploy-plugin

当命令Maven执行生命周期中的打包阶段时，上面至少有两个mojo将被执行。首先，maven-compile-plugin中的compile mojo将源代码编译到output目录。然后，maven-jar-plugin中的jar mojo将收集到的class文件打包到jar文件中。

 在这个例子的构建过程中仅仅只有这些mojo将被执行。因为这个假想的工程没有“非代码”资源，因此maven-resources-plugin中没有mojo会被执行。每个与资源相关的mojo将发现没有非代码资源的这个问题，它们将不会修改构建过程。这不是Maven框架的功能，而是mojo设计中的一个需要。好的mojo设计能决定什么时候不执行，它通常与执行时做出的修改一样重要。

如果Maven工程中也包含了单元测试源码，则另外两个mojo将被触发处理单元测试。maven-compiler-plugin中的testCompile mojo编译测试代码，然后maven-surefire-plugin中的test mojo将执行这些编译过的测试。这些mojo总是被定义在生命周期中，但现在它们什么也不做。

根据具体的工程，许多插件可以增加到默认的生命周期定义中来，提供各种各样的功能，例如部署到资源仓库、校验工程的内容、生成工程的Web站点，等等。Maven的插件框架确保几乎所有的东西都可以被集成到构建生命周期。这种扩展性也是使得Maven如此强大的部分原因。

#### 访问构建信息
为了使mojo能有效的执行，它需要获取当前构建的状态信息。这些信息来自于两方面：

 - 工程信息——来自于工程的POM，或来自于前面的mojo执行时通过编程的方式所做的修改。

 - 环境信息——这些更加静态，包括用户、机器、Maven设置、系统属性、执行Maven时指定的系统属性。

为了访问当前构建的状态，Maven允许mojo使用表达式设置参数值。在运行时，与参数关联的表达式将在当前的构建状态中被解析，并将结果注入mojo。通过正确的使用参数表达式，mojo可以保持它的依赖的最小化，从而避免了遍历整个构建状态对象图。

例如，一个给源码打补丁的mojo需要找到工程的源码和补丁文件。这个可以使用下面的表达式mojo从当前的构建信息中获取源码目录列表：
```
${project.compileSourceRoots}
```
假设补丁文件的保存目录是作为mojo的配置在POM中设置的，这个表达式可以使用类似下面的表达式获取这个信息：
```
${patchDirectory}
```

#### 插件描述
Maven的插件描述是一个嵌入到插件的jar包中的描述文件，存放在/META-INF/maven/plugin.xml。描述文件XML格式的，它告诉Maven在这个插件包中包含的mojo集。包含的信息有：mojo实现类（或它在插件jar包中的路径）的信息，各个mojo应该被绑定到生命周期的哪个阶段，mojo申明的参数集和其它信息。

在这个描述中，每个申明的mojo参数信息中都描述了多种用于获取参数值的表达式，描述了它是否可编辑，是否是mojo执行所必需的，以及参数值被注入到mojo实例的机制。

插件描述非常强大足够满足各种pojo的需要。但这种弹性是要付出代价的。为了获得这种弹性，它使用了复杂的语法。手工编写插件描述需要插件开发者了解Maven插件框架的底层细节——那些开发者不使用的细节，除非在配置描述时。这也是Maven插件开发工具出现的原因。通过从插件开发抽象许多细节，Maven的插件开发工具只暴露那些与插件实现语言相关的规范。（Maven's development tools expose only relevant specifications in a format convenient for a given plugin's implementation language）

### 插件开发工具
为了创建插件描述，Maven提供了插件工具从多种不同格式中分析mojo的元数据。元数据被直接嵌入到源码中，它的格式与mojo的实现语言关。简言之，Maven的插件开发工具解除了手工维护mojo元数据的负担。插件开发工具分为下面两个分类：

 - 插件解析框架——它知道如何从Maven支持的语言中解析出格式化的元数据。这个框架生成插件的文档和插件的描述；它包括一个应用框架的库，这些库提供了一套程序库（通常是每种mojo支持的语言都有一个）。

 - maven-plugin-plugin——它使用插件解析框架，从mojo实现中解析出元数据，加上从插件自己的配置文件（插件工程POM）中获取的其它插件级元数据；maven-plugin-plugin简单的将插件作为前面所述的resource-generating step对标准的jar生命周期进行增强。

当然，用户编写mojo的元数据的格式依赖于用于实现该mojo的语言。使用Java时，最简单的方式是提供javadoc注释来标明mojo的属性和参数。例如，maven-clean-plugin中的clean mojo提供了下面的类级的javadoc注入：
```
/**
 * @goal clean
 */
public class CleanMojo extends AbstractMojo
```
这个注释告诉插件开发工具mojo的名称，以便它可以在生命周期中被引用，比如在POM配置文件中，或直接调用（比如从命令行）。clean mojo也定义了下面的内容：
```
/**
 * Be verbose in the debug log-level?
 *
 * @parameter expression="${clean.verbose}" default-value="false"
 */
private boolean verbose;
```
这个注释标明了这个字段是一个mojo参数。这个参数注释也指定了两个属性，表达式和默认值。首先指定参数的默认值应该被设置为false。第二个指定这个参数可以在命令行进行配置：
```
-Dclean.verbose=false
```
另外，也可以在POM中配置这个参数：
```
<configuration>
  <verbose>false</verbose>
</configuration>
```
从上面可以看到参数名没有的显式的通过注释来指定；当使用@parameter注释时这是隐式指定的。

我们可以直接申明字段而不是使用javadoc注释来初始化这个默认值，例如：
```
private boolean verbose = false;
```
但如果你需要注入的默认值包含了一个参数表达式时的情况。例如，下面是maven-resources-plugin中的resources mojo使用字段注释：
```
/**
 * Directory containing the classes.
 *
 * @parameter default-value="${project.build.outputDirectory}"
 */
private File classesDirectory;
```
在这种情况下，不可能用需要的值来初始化这个java.io.File类型的字段，它指向当前工程的输出目录。当这个mojo被实例化后，这个值是从POM中获取并被注入的。由于插件工具也可以基于这些注释生成文档，因此通过元数据指定默认值是一个较好的方法，而不是在Java字段中初始化字段。

上面这些注释是适应于用Java编写的mojo。如果你用其它语言mojo，比如Ant，这时指定元数据的定义将不同。但它们的原理是一样的。

#### 选择mojo的实现语言

### 使用本章范例的提示
保持例子的简单。以便于理解。

新建一个名为buildinfo的工程，它使用这个插件。

## 开发第一个Mojo
本章的开发目标是围绕一个称为Guniea Pig的简单工程。开发的成果将能获取构建信息并将被部署Maven开发仓库。

### BuildInfo的一个例子：使用一个Java编写的Mojo获取信息
试想POM包含了这样一个profile，它将在系统属性os.name的值为Linux时被触发。当被触发时，这个profile将添加一个Linux下特定的新的依赖到工程中，有这个依赖的情况下在Linux下才能构建成功。当这个profile没有被触发时，一个默认的依赖将被注入，这个依赖是windows下的一个库。而这个依赖只在测试时需要而不会传递到依赖于本工程的其它工程。

由于这个值非常重要。如果测试的依赖包含于这样一个profile中，当这个profile被触发时它能决定构建的成功或失败。因此，应该在构建信息文件中包含这个系统属性的说明以便他人能理解环境对这个构建的影响。

#### 先决条件：构建生成buildinfo生成器工程
在编写buildinfo插件之前，你必须先将buildinfo生成器库安装到Maven本地仓库中。Buildinfo插件是对这个生成器的简单封装，它提供了一个很薄的适配层以便从Maven构建中运行生成器。这种方式也给出了一个重要的实践提示；通过将生成器从Maven构建代码中分离，你可以编写任何类型的适配器或前端代码，在不同的场景下使用用可重用的工具。

构建buildinfo生成器类，执行下面的步骤：
```
cd buildinfo
mvn install
```

#### 使用archetype插件生成插件工程的基础代码
现在buildinfo生成器的类库已经被安装到Maven仓库，有助于我们使用Maven的archetype插件从标准插件工程模板中创建一个简单的基础工程从而转到插件编写过程。一旦插件工程结构就绪，编写pojo就简单了。为了生成基础的buildinfo插件，只要执行：
```
mvn archetype:create -DgroupId=com.devzuz.mvnbook.plugins \
-DartifactId=maven-buildinfo-plugin \
-DarchetypeArtifactId=maven-archetype-mojo
```
 当运行这个命令时将看到警告信息“${project.build.directory} is not a valid reference”这是用于生成插件代码的Velocity模板产生的，不影响工程的正常使用。

上面的命令在maven-buildinfo-plugin下创建了一个标准结构的工程。这个目录下包含了一个基础的POM和一个示例pojo。为完成这个插件，你对POM进行修改：

 - 修改name元素为Maven BuildInfo Plugin。

 - 移除url元素，因为这个插件现在没有与Web站点关联。

以后还需要修改POM，比如修改mojo的依赖关系。

由于你需要创建自己的mojo，因此应该删除示例mojo。示例保存在：
```
src\main\java\com\devzuz\mvnbook\plugins\MyMojo.java
```

#### mojo
一个简单的Java编写的mojo：
```
/**
 * Write the environment information for the current build execution
 * to an XML file.
 * @goal extract
 * @phase package
 * @requiresDependencyResolution test
 *
 */
public class WriteBuildInfoMojo extends AbstractMojo {
    /**
     * Determines which system properties are added to the buildinfo file.
     * @parameter
     */
 private String systemProperties;
    /**
     * The location to write the buildinfo file. Used to attach the buildinfo
     * to the project jar for installation and deployment.
     * @parameter expression="${buildinfo.outputFile}" default- \
value="${project.build.directory}/${project.artifactId}- \
${project.version}-buildinfo.xml"
     * @required
     */
    private File outputFile;
    public void execute() throws MojoExecutionException {
        BuildInfo buildInfo = new BuildInfo();
        addSystemProperties( buildInfo );
        try {
            BuildInfoUtils.writeXml( buildInfo, outputFile );
        } catch ( IOException e ) {
            throw new MojoExecutionException( "Error writing buildinfo \
XML file. Reason: " + e.getMessage(), e );
        }
    }
    private void addSystemProperties( BuildInfo buildInfo ) {
        Properties sysprops = System.getProperties();
        if ( systemProperties != null ) {
            String[] keys = systemProperties.split( "," );
            for ( int i = 0; i < keys.length; i++ ) {
                String key = keys[i].trim();
                String value = sysprops.getProperty( key, \
BuildInfoConstants.MISSING_INFO_PLACEHOLDER );
                buildInfo.addSystemProperty( key, value );
            }
        }
    }
}
```
这个mojo的代码部分比较简单，值得关注的是javadoc注释。在类级的javadoc注释中，有两个特殊的注释：
```
/**
 * @goal extract
 * @phase package
 */
```
第一个注释@goal，告诉插件工具将这个类当作mojo。当调用这个mojo时，你将使用这个名称。第二个注释告诉Maven这个mojo应该在构建生命周期的哪个阶段被执行。在这里，你从环境中收集信息并将它同工程产品一起发布到maven仓库中。因此，应该在package阶段执行这个mojo，以便它被添加到工程产品中。通常，打包阶段也是获取信息并添加到构建结果中的最佳阶段。

类级注释的下面是字段级的javadoc注释，它用于指定mojo的参数。每个都指向一个特定参数，以便可以独立的设置。systemProperties参数变量：
```
/**
 * @parameter expression="${buildinfo.systemProperties}"
 */
```
这是一种最为简单的指定参数的情况。使用@parameter注释，没有属性，将允许在POM中插件配置中指定这个mojo字段。你可能想要允许用户指定哪些系统属性应该被包含到构建信息文件中，使用expression属性，你可以指定参数从命令行引用的名称。在这种情况下，expression属性可以被设置为系统属性的列表：
```
localhost $ mvn buildinfo:extract \
-Dbuildinfo.systemProperties=java.version,user.dir
```

 执行这个命令的模块应该使用buildinfo前缀。在这里，guinea-pig模块应该使用buildinfo这个goal前缀来绑定到maven-buildinfo-plugin，以便在guinea-pig目录下执行上面的命令。

最后，outputFile参数出现在一个更加复杂的参数注释例子中。由于你对这个参数有更加复杂的要求，这个复杂性是合理的：
```
/**
* The location to write the buildinfo file. Used to attach the buildinfo
* for installation and deployment.
*
* @parameter expression="${buildinfo.outputFile}" default- \
value="${project.build.directory}/${project.artifactId}- \
${project.version}-buildinfo.xml"
*
* @required
*/
```
在这里，mojo不运行除非它知道将构建信息写到哪个文件。为确保这个参数有一个值，mojo使用了@required注释。如果在配置mojo时这个参数没有值，这个构建将产生错误。另外，你可能需要让mojo从工程中计算出这个值作为这个参数的默认值。在这里注释中使用几个表达式来指定默认输出路径。

#### 插件的POM
Mojo编写完后，你可以构建一个简单POM文件以便你构建这个插件，例如：
```
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.devzuz.mvnbook.plugins</groupId>
  <artifactId>maven-buildinfo-plugin</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>maven-plugin</packaging>

  <dependencies>
    <dependency>
      <groupId>org.apache.maven</groupId>
      <artifactId>maven-plugin-api</artifactId>
      <version>2.0</version>
    </dependency>
    <dependency>
      <groupId>com.devzuz.mvnbook.shared</groupId>
      <artifactId>buildinfo</artifactId>
      <version>1.0-SNAPSHOT</version>
    </dependency>
[...]
  </dependencies>
</project>
```
这个POM申明了工程的标识和它的两个依赖。

注意依赖中的buildinfo，它提供了解析和格式化构建信息文件的工具。依赖中也指定了maven-plugin，这表示这个插件将遵循构建生命周期映射。

#### 绑定到构建生命周期
现在已经有了方法来获取构建时的环境信息，你需要确保每个构建都能得到这个信息。最简单的保证方法就是将extract mojo绑定到构建生命周期，让它在每次构建时都被触发。这包括了修改标准的jar生命周期。可以通过向Guinea Pig的POM中配置新的插件，例如：
```
<build>
  [...]
  <plugins>
    <plugin>
      <groupId>com.devzuz.mvnbook.plugins</groupId>
      <artifactId>maven-buildinfo-plugin</artifactId>
      <executions>
        <execution>
          <id>extract</id>
          <configuration>
            <systemProperties>os.name,java.version</systemProperties>
          </configuration>
          <goals>
            <goal>extract</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
    [...]
  </plugins>
  [...]
</build>
```
上面的绑定将在构建生命周期的package阶段执行maven-buildinfo-plugin的extract mojo，并获取系统的os.name属性。

#### 输出
现在你有了一个mojo和一个POM，你可以构建这个插件并试用！首先，使用下面的命令构建buildinfo插件：
```
cd C:\book-projects\maven-buildinfo-plugin
mvn clean install
```

接下来，通过将buildinfo插件绑定到Guinea Pig工程来测试插件。
```
cd C:\book-projects\guinea-pig
mvn package
```
当执行Guinea Pig的构建时，你可以看到类似下面的输出：
```
[...]
[INFO] [buildinfo:extract {execution: extract}]
[INFO]
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO] ------------------------------------------------------------------------
[INFO] Guinea Pig Sample Application ......................... SUCCESS [6.468s]
[INFO] Guinea Pig API ........................................ SUCCESS [2.359s]
[INFO] Guinea Pig Core ....................................... SUCCESS [0.469s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESSFUL
[INFO] ------------------------------------------------------------------------
[...]
```
在target目录下，应该有一个新的文件：
```
guinea-pig-1.0-SNAPSHOT-buildinfo.xml
```
在这个文件中，可以看到类似下面的信息：
```
<?xml version="1.0" encoding="UTF-8"?><buildinfo>
  <systemProperties>
    <java.version>1.5.0_06</java.version>
    <os.name>Windows XP</os.name>
  </systemProperties>
  <sourceRoots>
    <sourceRoot>src\main\java</sourceRoot>
  </sourceRoots>
  <resourceRoots>
    <resourceRoot>src\main\resources</resourceRoot>
  </resourceRoots>
</buildinfo>
```
当然OS的名称和java的版本可能会不同。

### BuildInfo的例子：使用Ant Mojo通知其它开发者
现在一些重要信息已经被获取，你需要在这个工程的产品被部署时与团队中的其它人分享这些信息。在Maven的世界中要记住“部署deployement”表示将工程产品注入到Maven仓库系统。现在，需要发送一个通知邮件到工程开发的邮件列表，以便其它团队成员来访问。

当然，这样的任务可以使用基于Java的mojo通过JavaMail API来处理。但这需要写大量的代码和测试，更简单的办法是使用Ant。

在编写完发送通知邮件的Ant target后，你只需要编写一个mojo来将这个target封装到Maven构建过程中。

#### Ant target
新的mojo保存在notify.build.xml中，内容如下：
```
<project>
  <target name="notify-target">
    <mail from="maven@localhost" replyto="${listAddr}"
      subject="Build Info for Deployment of ${project.name}"
       mailhost="${mailHost}" mailport="${mailPort}"
       messagefile="${buildinfo.outputFile}">

      <to>${listAddr}</to>

    </mail>
  </target>
</project>
```

#### Mojo Metadata文件
不同于之前的例子，Ant mojo的metadata是保存在单独的文件中的，它使用命名约定与构建脚本关联。在这个例子中，构建脚本被命名为notify.build.xml。对应的metadata文件名为notify.mojos.xml，内容如下：
```
<pluginMetadata>
  <mojos>
    <mojo>
      <call>notify-target</call>
      <goal>notify</goal>
      <phase>deploy</phase>
      <description><![CDATA[
        Email environment information from the current build to the
        development mailing list when the artifact is deployed.
      ]]></description>
      <parameters>
        <parameter>
          <name>buildinfo.outputFile</name>
          <defaultValue>
              ${project.build.directory}/${project.artifactId}- \
${project.version}-buildinfo.xml
            </defaultValue>
          <required>true</required>
          <readonly>false</readonly>
        </parameter>
        <parameter>
          <name>listAddr</name>
          <required>true</required>
        </parameter>
        <parameter>
          <name>project.name</name>
          <defaultValue>${project.name}</defaultValue>
          <required>true</required>
          <readonly>true</readonly>
        </parameter>
        <parameter>
          <name>mailHost</name>
          <expression>${mailHost}</expression>
          <defaultValue>localhost</defaultValue>
          <required>false</required>
        </parameter>
        <parameter>
          <name>mailPort</name>
          <expression>${mailPort}</expression>
          <defaultValue>25</defaultValue>
          <required>false</required>
        </parameter>
      </parameters>
    </mojo>
  </mojos>
</pluginMetadata>
```
初看起来，文件内容与Java编写的mojo包含的metadata是不同的；但细看就可以发现有许多相似的地方。

首先，由于现在你对于用来描述mojo的metadata类型已经有一个较好的概念，总体结构应该比较熟悉。与Java的例子中一样，mojo级的metadata描述绑定的阶段和mojo的名称等细节。

metadata指定mojo的参数列表，每个都有自己的信息，如名字、表达式、默认值和其它信息。表达式的语法用于从构建状态解析信息，参数标识如required仍然存在，但是是通过XML表达的。

当这个mojo被执行时，Maven仍然将解析并注入这些参数到mojo中；不同之处在于用来注入的方式。在Java中，参数注入通过直接注入到字段或通过JavaBean风格的setXXX()方法进行。在基于Ant的mojo中，参数注入是作为属性被Ant工程实例引用的。

 Ant参数注入应遵循下面的原则：如果参数类型是java.lang.String（默认），则它的值是作为属性被注入的；其它的值将作为工程的属性引用被注入。在这个例子中，所有mojo参数类型都为java.lang.String。如果某个参数是其它类型的，你需要在<name>元素中添加<type>元素来描述参数的类型。

最后，注意这个mojo被绑定到生命周期的deploy阶段。这是这个mojo中一个重要的地方，因为你准备在这时发送邮件到开发邮件列表。如果绑定在其它阶段，它将产生大量垃圾邮件。而放在deploy阶段，则只在新的工程产品被部署到远程仓库中时才会发送邮件。

#### 为Ant Mojos修改插件POM
由于Maven 2.0不支持基于Ant的mojo（将在2.0.2中支持Ant），需要一些特殊的配置来让maven-plugin-plugin识别Ant mojos。幸运的是，Maven允许POM-specific注入插件级的依赖，以便插件使用框架提供的功能。（in order to accommodate plugins that take a framework approach to providing their functionality. ）

maven-plugin-plugin是一个完善的例子，它通过使用maven-plugin-tools-api库中的MojoDescriptorExtractor接口。这个库定义了一套从原生格式（Java或其它语言编写的pojo）解析并生成mojo描述信息的接口集，这些描述信息包括了插件描述文件。maven-plugin-plugin的Java和BeanShell版中提供了上述接口的实现库。

这允许开发者不需要额外的配置就可以在基于Java或BeanShell的mojo中生成描述信息。为了开发基于Ant的mojo，你需要使用maven-plugin-plugin来支持Ant mojo。

为达到这个目的，你需要在POM配置中将maven-plugin-tools-ant库添加到maven-plguin-plugin的依赖中。
```
<project>
  [...]
  <build>
    <plugins>
      <plugin>
        <groupId>com.devzuz.mvnbook.plugins</groupId>
  <artifactId>maven-plugin-plugin</artifactId>
        <dependencies>
          <dependency>
            <groupId>org.apache.maven</groupId>
            <artifactId>maven-plugin-tools-ant</artifactId>
            <version>2.0.2</version>
          </dependency>
        </dependencies>
      </plugin>
    </plugins>
  </build>
  [...]
</project>
```
另外，由于插件现在包括了一个基于Ant的mojo，它需要一些新的依赖，例如：
```
<dependencies>
  [...]
  <dependency>
    <groupId>org.apache.maven</groupId>
    <artifactId>maven-script-ant</artifactId>
    <version>2.0.2</version>
  </dependency>
  <dependency>
    <groupId>ant</groupId>
    <artifactId>ant</artifactId>
    <version>1.6.5</version>
  </dependency>
  [...]
</dependencies>
```
第一个新依赖是用于封装Ant构建脚本的mojo API，它们对于在Maven构建过程中将Ant脚本作为mojo总是需要的。第二个新的依赖，是对Ant库的依赖。

#### 将Notify Mojo绑定到生命周期
Ant mojo插件的描述生成完后，它与Maven中其它类型的mojo一样。甚至配置都是一样的。在Guinea PIG POM中添加Ant mojo：
```
<build>
  [...]
  <plugins>
    <plugin>
      <groupId>com.devzuz.mvnbook.plugins</groupId>
<artifactId>maven-buildinfo-plugin</artifactId>
      <executions>
        <execution>
          <id>extract</id>
          [...]
        </execution>
        <execution>
          <id>notify</id>
          <goals>
            <goal>notify</goal>
          </goals>
          <configuration>
            <listAddr>dev@guineapig.codehaus.org</listAddr>
          </configuration>
        </execution>
      </executions>
    </plugin>
    [...]
  </plugins>
</build>
```
 <execution>——它将extract mojo绑定到构建中。notify mojo放在另一个<execution>中。这是因为一个execution只能包含构建生命周期中的一个阶段，并且这两个mojo不应该在同一个构建阶段执行。

为了告诉notify mojo将邮件发送到里，还应该在configuration一节中配置listAddr参数值。

现在执行下面的命令：
```
mvn deploy
```
构建过程将执行构建步骤并部署jar——，它也将在打包阶段获取环境信息，并在部署阶段发送邮件到Guinea Pig开发者邮件列表。

 注意：应该配置distributionManagement和scm以便能成功的执行mvn deploy。

## 高级Mojo开发
前面的例子展示了如何申明简单的mojo参数，如何使用名称和绑定阶段来注释mojo。下面的例子将包含更多与mojo开发相关的高级主题。下面的章节互相没有依赖，对于开发基本的mojo来说并不是必须的。但如果你想知道如何开发插件来管理依赖、工程源码和资源、产品附件，那么准备开始吧！

# 评估工程的健康度

# 使用Maven进行团队协作

# 迁移到Maven







