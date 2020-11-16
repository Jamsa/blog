---
title: "Docker for Mac从容器访问主机服务"
date: 2019-01-01
modified: 2019-01-01
categories: ["开发"]
tags: ["docker"," mac"]
---

最近两天，在配置本机一套分布式系统的单点登录功能时，需要用到`Nginx`做同域单点登录，本打算直接用`docker`运行一个`nginx`容器就能解决，没想到在使用时却遇到了问题，`nginx`无法访问主机上运行的服务。

在使用docker时可以通过端口映射将容器内的端口暴露给主机访问。但是在从docker容器中访问主机网络却不那么方便。特别是在Mac或Windows主机上。

因为在Mac或Windows主机上，docker实际上是运行在主机提供的虚拟化服务上，相当于运行在一个Linux虚拟机中。从主机上查看时是找不到`docker0`网桥设备的，这个设备在虚拟机上。

当我们需要从容器内访问主机网络时，不能使用`localhost`访问，而要使用主机的局域网地址，如果主机没有连接网络，则非常不方便。实际上在虚拟机的`docker0`网桥上，Mac主机会被分配一个`192.168.65.0`段的地址，默认`192.168.65.1`是网关地址，`192.168.65.2`就是主机地址。从容器内通过这个地址是可以访问到主机上的服务的。

从[Docker for Mac网络配置文档](https://docs.docker.com/docker-for-mac/networking/#use-cases-and-workarounds)上查到，从`18.03`开始，可以使用`gateway.docker.internal`和`host.docker.internal`来访问`docker0`网桥上的网关和主机网络（不建议在生产环境使用）。

以下是我的nginx配置片段，它将主机上的8000端口映射至，nginx `/r1doc/`目录：

```
location /r1doc/ {
		proxy_pass http://host.docker.internal:8000/; 
	 }
```

