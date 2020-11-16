---
title: "JBoss Seam 学习笔记"
date: 2009-01-15
modified: 2009-01-15
categories: ["开发"]
tags: ["seam","jsf"]
---

#  JBoss Seam介绍
Seam是一个for Java EE5的应用框架。它是从下面的规则得到灵感的：

 - 集成JSF和EJB3.0

  

 - 集成AJAX。

  Seam支持两个开源的JSF AJAX解决方案：ICEFaces和Ajax4JSF。这些解决方案让你可以在应用中添加AJAX支持而不需要编写JS代码。

  Seam也支持内置EJB3组件的的JavaScript远程调用。AJAX客户端可以很容易的调用服务端组件和JMS主题，而不需要中间动作层。

  这两种办法都工作得比较好，如果不是有Seam内置的并发和状态管理，它确保了许多并发和异步的AJAX请求被安全高效的在服务端被处理。

 - 集成业务流程作为一流的构件。

  集成了jBPM，并允许定义会话层。JSF为这个会话层提供了强大的事件模型。Seam通过暴露jBPM的业务流程相关的事件，使用同样的事件处理机制，为所有Seam的组件模型提供了统一的事件模型。

 - 一种“填充”

 - 申明性状态管理

 - 双射

 - 工作区管理

 - 到处都是带注释的POJO

 - 易测试

 - 开始！

  Seam可以工作于任何支持EJB3的应用服务器中。通过使用Jboss嵌入式EJB3容器，甚至可以在Servlet容器中使用Seam，比如Tomcat或任何J2EE应用服务器。

  在现在并不是所有的人都准备迁移到EJB3。因此，在这期间可以把Seam作为一种框架来使用，使用JSF作展现，Hibernate作持久层，JavaBean处理应用逻辑。当准备迁移到EJB3.0时，迁移将比较直接。

#  Chapter 1. Seam教程

#  Chapter 2. 使用seam-gen开始Seam
##  2.1 开始之前
确保你有JDK 5或JDK 6，JBoss AS 4.0.5和Ant 1.6。

JBoss有完善的热部署和重新部署WAR和EAR的功能。但不幸的是，由于JVM的Bug，重新部署一个EAR——通常是在开发阶段——最终将导致JVM Perm Gen溢出。因此，我们推荐在开发阶段调整JVM参数。推荐的参数为：
```
-Xms512m -Xmx1024m -XX:PermSize=256m -XX:MaxPermSize=512
```
如果你没有足够的内存，推荐使用下面的参数：
```
-Xms256m -Xmx512m -XX:PermSize=128m -XX:MaxPermSize=256
```
如果你从命令行运行JBoss，则可以修改bin/conf下的配置来配置JVM参数。

##  2.2 设置一个新的Eclipse工程
首先我们需要配置一个seam-gen环境：JBoss AS安装路径、Eclipse工作空间、数据库连接：
```
cd jboss-seam-home
seam setup
```
根据提示输入相关的信息。其中重要的选项是选择EAR和WAR部署。EAR工程支持EJB 3.0需要Java EE 5。WAR工程不支持EJB 3.0，但可以部署到J2EE环境中。WAR包简单易懂。如果安装了支持EJB 3.0的JBoss，选择ear。否则，选择war。

如果数据模型已经存在，请确保告诉了seam-gen数据库表已经存在于数据库。

设置保存在seam-gen/build.properties，但你可以再次运行seam set来修改。

进入Eclipse工作空间，执行：
```
seam new-project
```
它将复制Seam需要的jar文件，需要的JDBC驱动包到新的Eclipse工程中，并生成所有需要的资源和配置文件，facelets模板文件和样式，Eclipse元数据和Ant脚本。这个Eclipse工程将自动部署到JBoss中一个展开的目录中。在Eclipse中点击New -> Project... -> General -> Project -> Next，不要选择Java Project。

如果Eclipse中默认的JDK不是Java SE 5或Java SE 6，你需要设置工程的默认编译器。

你也可以在Eclipse外部，使用seam explode。

转到`http://localhost:8080/helloworld`查看欢迎页面。这是一个facelet页面，vew/home/xhtml，使用的模板为`view/layout/template.xhtml`可以修改这个页面或模板，修改将立即生效。

不要害怕生成的工程目录中的XML配置文档。它们中多数是标准的Java EE原料，这些原料只要创建一次就不再需要查看，在所有Seam工程中它们有90%是相同的。

生成的工程包括三个数据库和持久化配置。jboss-beans.xml，persistence-test.xml和import-test.sql文件用于基于HSQLDB做TestNG单元测试。测试用的数据库数据存储在import-test.sql中,它们在运行测试前被导出到数据库。project-dev-ds.xml，persistence-dev.xml和import-dev.sql用于部署到开发数据库。这个数据库配置是否自动导出到数据库取决于你使用seam-gen是否告诉它你工作于已经存在的数据库上。myproject-prod-ds.xml，persistence-prod.xml和import-prod.sql文件用于部署到产品数据库。这个数据库配置不会自动导出和部署。

##  2.3 创建一个新的action
如果你使用传递的action风格的web应用框架，你可以使用下面的方法创建一个无状态的action方法：
```
seam new-action
```
Seam将提示一些信息，并生成新的facelet页面和Seam组件。
```
C:\Projects\jboss-seam>seam new-action ping
Buildfile: C:\Projects\jboss-seam\seam-gen\build.xml

validate-workspace:

validate-project:

action-input:
    [input] Enter the Seam component name
ping
    [input] Enter the local interface name [Ping]

    [input] Enter the bean class name [PingBean]

    [input] Enter the action method name [ping]

    [input] Enter the page name [ping]


setup-filters:

new-action:
     [echo] Creating a new stateless session bean component with an action method
     [copy] Copying 1 file to C:\Projects\hello\src\com\hello
     [copy] Copying 1 file to C:\Projects\hello\src\com\hello
     [copy] Copying 1 file to C:\Projects\hello\src\com\hello\test
     [copy] Copying 1 file to C:\Projects\hello\src\com\hello\test
     [copy] Copying 1 file to C:\Projects\hello\view
     [echo] Type 'seam restart' and go to http://localhost:8080/helloworld/ping.seam

BUILD SUCCESSFUL
Total time: 13 seconds
C:\Projects\jboss-seam>
```
由于我们添加了新的Seam组件，我们需要重新部署。你可以使用seam restart，或运行build.xml中的restart任务。另一种方法是编辑`resources/META-INF/application`文件来重启。不需要每次都重启JBoss。

现在转到`http://localhost:8080/helloworld/ping.seam`然后点击按钮。你将看到执行了src中的action中的代码。可以在ping()方法中设置断点，然后再次点击。

最后，在测试包中找到PingTest.xml文件并使用Eclipse的TestNG插件来执行集中测试。也可以使用seam tesst或build.xml中的test任务。

##  2.4 创建一个带action的form
创建form的步骤：
```
seam new-form
```
```
C:\Projects\jboss-seam>seam new-form
Buildfile: C:\Projects\jboss-seam\seam-gen\build.xml

validate-workspace:

validate-project:

action-input:
    [input] Enter the Seam component name
hello
    [input] Enter the local interface name [Hello]

    [input] Enter the bean class name [HelloBean]

    [input] Enter the action method name [hello]

    [input] Enter the page name [hello]


setup-filters:

new-form:
     [echo] Creating a new stateful session bean component with an action method
     [copy] Copying 1 file to C:\Projects\hello\src\com\hello
     [copy] Copying 1 file to C:\Projects\hello\src\com\hello
     [copy] Copying 1 file to C:\Projects\hello\src\com\hello\test
     [copy] Copying 1 file to C:\Projects\hello\view
     [copy] Copying 1 file to C:\Projects\hello\src\com\hello\test
     [echo] Type 'seam restart' and go to http://localhost:8080/hello/hello.seam

BUILD SUCCESSFUL
Total time: 5 seconds
C:\Projects\jboss-seam>
```
重启应用，转到`http://localhost:8080/helloworld/hello.seam`。

##  2.5 从已存的数据库生成一个应用
在数据库中手工创建一些表.输入:
```
seam generate-entities
```
重启应用,转到`http://localhost:8080/helloworld`。你可以浏览数据库，编辑已经存在的对象，创建新对象。如果你查看生成的代码，你将对它的简单感到吃惊！Seam被设置为易于访问数据，即不想使用seam-gen的用户。

##  2.6 使用EAR部署应用
最后，我们需要能将应用打包成标准的Java EE 5 的包。首先，我们需要运行`seam unexplode`移除wxploded目录。输入`seam deploy`命令部署EAR，或运行生成的工程中的`deploy`任务。也可以使用`seam undeploy`取消部署。

默认情况下，将使用`dev`配置来部署应用。EAR将包含persistence-dev.xml和import-dev.sql和myproject-dev-ds.xml。可以使用`prod`配置文件来部署，输入：
```
seam -Dprofile=prod deploy
```
你也可以定义自己的应用部署配置文件。只需要添加适当的文件——比如，persistence-staging.xml、import-staging.sql和myproject-staging-ds.xml并使用`-Dprofile=staging`。

##  2.7 Seam和增量热部署
当使用解压后的目录（exploded directory）部署Seam应用时，你将在开发时获得增量热部署的支持。也可以在components.xml中启动debug模式来启动Seam和Facelets的调试模式：
```
<core:init debug="true"/>
```
现在，下面的文件可以重新部署而不需要重启web应用：
```
 任何facelets页面
 任何pages.xml文件
```
但如果你修改了Java代码，我们仍然需要重启应用。（在Jboss中可以通过修改EAR部署中的顶级部署描述application.xml，或WAR部署中的web.xml的时间戳。）

但如果你想快速进行编辑/编译/测试周期，Seam支持JavaBean组件的增量部署。为使用这个功能，你必须将JavaBean组件部署到WEB-INF/dev目录，以便被特殊的Seam classloader加载，而不是被WAR或EAR的classloader加载。

你需要知道有下面的限制：

 - 组件必须是JavaBean组件，不能是EJB3 Bean（我们正在修正这个限制）

 - 实例不能被热部署

 - 通过components.xml部署的组件不可以被热部署

 - 热部署的组件对于WEB-INF/dev之外的class loader是不可见的

 - Seam debug模式必须被启用

如果你使用seam-gen生成了一个WAR工程，增量热部署对于src/action源码目录下的类都是可用的。但是，seam-gen不支持EAR工程的热部署。

#  3 上下文组件模型
Seam中两个核心的概念是上下文（context）的概念和组件（component）概念。组件是有状态对象，使用EJB，组件的实例与一个上下文关联，在上下文中被命名，Seam允许组件树被动态装配和重新装配。

##  3.1 Seam上下文
Seam上下文是被框架创建和销毁的。应用不显示的使用Java API控制上下文的界限。上下文通常是隐式的。有些情况下，上下文界限通过注释来设置。

基本的Seam上下文是：

 - 有状态上下文（Stateless context）

 - 事件（或请求）上下文（Event(or request) context）

 - 页面上下文（Page context）

 - 对话上下文（Conversation context）

 - 会话上下文（Session context）

 - 业务流程上下文（Business process context）

 - 应用上下文（Application context）

你能从servlet和相关规范中识别出其中一些上下文。但其中两个可能是新的概念：对话上下文和业务流上下文。在web应用中状态管理比较脆弱和易于出的一个原因在于三个内置上下文（request，session和application）从业务逻辑的观点来看没有特别的含义。一个用户登录session，比如，任意构建的实际应用工作流。因此，多数Seam组件处于对话上下文或业务流程上下文中，因为它们对于应用是有含义的。

###  3.1.1 有状态上下文
真正有状态的组件（有状态session bean）总是存在于有状态上下文中。有状态组件并不是很有趣，可以证明不是很面向对象。但它仍然是很重要的且经常使用。

###  3.1.2 事件上下文
事件上下文是“窄”的有状态上下文，它是对web request上下文的封装。但是事件上下文与JSF请求的生命周期相关是事件上下文最重要的一个例子，它是你最常用的。与事件上下文关联的组件将在请求结束时被销毁，但它们的状态在请求周期中是有效的。

当你通过RMI或Seam Remoting调用Seam组件，事件环境的创建和销毁仅在调用的期间。

###  3.1.3 页面上下文
页面组件允许你关联状态到一个被渲染的页面实例。你可以在你的事件监听中初始化状态，或当实际渲染页面时，然后可以从任何发源于这个页面的事件中访问它。这对于类似可选项列表这类的功能非常有用，这种情况下列表可能通过修改服务端修改数据而改变。状态实际上被序列化到客户端，因此这个机构对于多窗口操作和后退按钮来说非常健壮。

###  3.1.4 对话上下文
对话上下文是Seam中的一个中心概念。一个对话上下文对于用户来说是一组功能的集合。它可能处于多个用户交互，多个请求和多次数据库事务之间。但对于用户，一个对话只解决一个单一的问题。比如，“旅馆登记”，“批准合同”，“创建定单“都是对话。你可以把一个对话当作一个单一的”用例“，但这不是很准确。

一个对话保持了关于“用户在这个窗口中正在做什么”的状态。在一个时间点上一个单一用户可以使用多个窗口拥有有多个对话。对话上下文允许我们确保多个不同的对话间不产生冲突。

你可能需要花一些时间了解对话在应用中的作用。但一旦你使用它，你将喜欢上这个概念。

一些对话只是简单的一个请求。对话跨多个请求可以使用Seam提供的注释来划分。

一些对话也是任务。一个任务是一个长时间的业务处理，当它成功时可能触发业务流程状态的变迁。Seam为任务的划分提供了一套特殊的注释。

对话可以嵌套，这是一个高级功能。

通常，对话状态由Seam保持在请求之间的servlet session中。Seam实现可配置的对话超时，自动清除无效的对话，这确保单个用户的session状态不会过度增长。

在同一个进程中Seam串行处理同一个长时间运行的对话上下文。

Seam也可以配置为在客户端浏览器中保持对话状态。

###  3.1.5 Session上下文
Session上下文保持登录用户session相关的状态。某些情况下这对于在多个对话间共享状态很有用，我们通常不赞成在session上下文中保持除登录用户全局信息外的其它组件。

在JSR-168 portal环境，session上下文代表portlet session。

###  3.1.6 业务流上下文











#  Chapter 3. 上下文组件模型


（未完成）

#  环境配置
直接运行setup.bat按提示操作。

要注意的一些问题：
 1. seam必须要在相匹配的JBoss版本上才能运行。我的机器上安装的JBoss为4.2.0GA，开始的时候试了一下运行jboss-seam-2.0.0.CR2，maven提示安装jboss-seam-gen这个包，手工下载了这个包，然后在jboss-seam-2.0.0.CR2/build/maven2/bin下的mvn命令来安装这个包。（注：在2.0.0.CR3中已经没有这个问题了）

 2. jboss-seam-1.x版本在JBoss-4.2.0GA上运行出错。jboss-seam-1.x需要JBoss-4.0.5x。

 3. 部署jboss-seam-2.0.0.CR2/examples下的例子时需要先修改jboss-seam-2.0.0.CR2/build.properties添加一行指定jboss的路径，jboss.home=d:\\jboss-4.2.0.GA。注意：即使在seam.bat setup时指定了正确的JBoss的路径，这里也必须要设置，这好像是jboss-seam-2.0.0.CR2的一个BUG。

#  创建一个简单的例子
##  seam create-project
创建一个项目

##  seam create-action
创建一个action类

##  seam create-form
创建一个表单

##  seam generate-entities
基于数据库生成CRUD代码（没有D）。
测试这个例子时不应该使用hsqldb，除非写了import.sql文件。在hsqldb启动后创建了表，否则在创建实体重启后会找不到表。

#  components.xml文件
##  分页
可以通过在components.xml中注入每页最多显式的记录数，也可以修改XxxList类的getMaxResults的返回值。


