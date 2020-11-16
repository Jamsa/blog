---
title: "将科学上网工具从ss切换到了v2ray"
date: 2018-09-11
modified: 2018-09-11
categories: ["效率"]
tags: [""]
---

昨天使用ss的时候发现bandwagon上做ss服务的vps IP又被墙了，这是最近几个月来第二次被墙了。

通过[bwg提供的链接](https://kiwivm.64clouds.com/main-exec.php?mode=blacklistcheck)确认IP已经被墙，在这个链接上也可以更换vps ip。最近由于墙使用了机器学习算法已经识别了ss包的特征（应该是连接阶段模拟http包的特征，我是在手机wifi信号不好的情况下，在4G和wifi间反复切换，ss反复重连时被墙的。上次被墙也是类似的情况，两次被墙都是在使用电信线路的时候），被墙的机率提高，虽然在bwg已经将更换IP的限制从8周调整为了5周，但是从ss迁移至其它科学上网工具已经是必须的了。

在没有其它更合适的科学上网工具的情况下，准备切换至[v2ray](https://www.v2ray.com/chapter_00/install.html)。

由于我的vps上的centos版本较旧。在安装v2ray的时候遇到两个问题：
 
首先是v2ray的go.sh执行时没有回应

```
bash <(curl -L -s https://install.direct/go.sh)
```

这是因为curl命令在执行时报了ssl错误，只需要执行

```
yum -y update nss
```

再运行上面的命令进行安装。

如果你的vps是centos6.x版本的，在go.sh将v2ray变为系统服务时，仍然会出错：

```
Failed to install daemon. Please install it manually.
```

这时需要手工创建`/etc/init.d/v2ray`服务脚本，参见[v2ray github issue](https://github.com/v2ray/v2ray-core/issues/101#issuecomment-214670792%5D)。

安装完成后，记得修改`/etc/v2ray/config.json`上的`client id`。

在客户端方面，v2ray的客户端功能没有ss的客户端功能强大，但也基本上够用了。在MacOS上有`V2RayX`，在Android平台上有`v2rayNG`。

