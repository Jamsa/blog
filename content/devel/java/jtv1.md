Title: JTV开发笔记1-开始
Date: 2018-07-17
Modified: 2018-07-17
Category: 开发
Tags: scala, netty

本文是[Jtv](http://jamsa.github.com/Jamsa/jtv)的开发笔记。Jtv是一个远程桌面工具。

# 起因

因为工作原因，我经常需要进行远程桌面操作。尝试过多种不同的远程桌面方案，如：QQ远程、Teamviewer、Windows远程桌面、Hamachi等等。在速度比较稳定的，且支持内网连接的工具里只有Teamviewer和QQ远程能稳定使用。切换至Mac环境后，Teamviewer就成了唯一选择，Teamviewer被判定为商业使用后，每5分钟会中断一次，无法正常使用。之间也尝试过使用ngrok配合其它内网vnc工具来进行远程连接。但这些方式都不太方便，比如使用ngrok + Windows远程桌面也能连接，但是远程桌面和VNC都无法与远程用户共享桌面。

由于这些原因，就有了自己开发一个简化版远程桌面工具的想法。

# 目标

仅把它当作个业余项目，近期目标是实现：以中心服务器进行交换，支持内网连接的远程桌面和控制功能。

# 技术选型

个人项目选型上比较自由，主要考虑以下几个方面：

 - 考虑到跨平台使用，选定在Java平台上。
 
 - 利用Swing的Robot类可实现对键盘、鼠标的控制。
 
 - Java语言写Swing相关的内容太啰嗦，选Scala了。
 
 - 网络通讯模块选择netty。

选择的版本如下：

 - scala 2.12.6
 
 - sbt 1.1.6
 
 - netty 4.1.25.Final
 
# 工程创建

使用`sbt`来创建工程，工程代号`jtv`。

 1. 创建工程目录结构
 
```
➜  jtv git:(master) ✗ tree -L 2
.
├── README.md
├── build.sbt
├── client
│   ├── src
├── common
│   ├── src
├── project
│   ├── Dependencies.scala
│   ├── build.properties
│   ├── plugins.sbt
├── server
│   ├── src
```
 
 1. 在`project/build.properties`中添加`sbt.version=1.1.6`定义sbt版本。
 
 1. 在`project/plugin.sbt`中引用打包插件`addSbtPlugin("com.typesafe.sbt" % "sbt-native-packager" % "1.3.5")`
 
 1. 将依赖集中定义在`project/Dependencies.scala`中，内容如下：
 
```scala
import sbt._

object Dependencies {
  lazy val scalaTest = "org.scalatest" %% "scalatest" % "3.0.3"
  lazy val netty = "io.netty" % "netty-all" % "4.1.25.Final"
  lazy val logging = "com.typesafe.scala-logging" %% "scala-logging" % "3.9.0"
  lazy val logback =  "ch.qos.logback" % "logback-classic" % "1.2.3"
}
```
 
 使用了`scala-logging`日志模块。
 
 1. 在`build.sbt`中定义各个模块：
 
```scala
import Dependencies._

lazy val commonSettings = Seq(
  organization := "com.github.jamsa.jtv",
  version := "0.1.0",
  scalaVersion := "2.12.6",
  libraryDependencies += scalaTest % Test,
  libraryDependencies += netty,
  libraryDependencies += logging,
  libraryDependencies += logback
)

lazy val common = (project in file("common"))
  .settings(
    commonSettings,
    name := "jtv-common"
  )

lazy val client = (project in file("client")).dependsOn(common)
  .settings(
    commonSettings,
    name := "jtv-client",
    mainClass in Compile := Some("com.github.jamsa.jtv.client.manager.JtvClientManager")
  ).enablePlugins(JavaAppPackaging)

lazy val server = (project in file("server")).dependsOn(common)
  .settings(
    commonSettings,
    name := "jtv-server",
    mainClass in Compile := Some("com.github.jamsa.jtv.server.JtvMain")
  ).enablePlugins(JavaAppPackaging)


lazy val root = (project in file(".")).aggregate(common, client, server)
  .settings(
    name := "jtv"
  )
```
 
 `commonSettings`为各模块的共享定义。`common`模块为公共依赖模块，主要存放通讯协议、网络层相关的公用类和工具类。`client`模块为安装在最终客户机器上的客户端程序。`server`模块为处理数据交换的服务程序。
 
 在`client`和`server`上启用`JavaAppPackaging`插件，以便输出最终的发布包。

 
