---
title: "Linux内核设备驱动第三版读书笔记"
date: 2008-01-17
modified: 2008-01-17
categories: ["开发"]
tags: ["linux"]
---

# Chap 2 构建和运行内核

## 设置测试系统
书中的例子以Kernel 2.6.x为基础（2.6.10）。

## Hello World模块
```c
#include <linux/init.h>
#include <linux/module.h>
MODULE_LICENSE("Dual BSD/GPL");
static int hello_init(void)
{
printk(KERN_ALERT "Hello, world\n");
return 0;
}
static void hello_exit(void)
{
printk(KERN_ALERT "Goodbye, cruel world\n");
}
module_init(hello_init);
module_exit(hello_exit);
```
这个模块包含两个函数，一个在模块被加载到内核时时被调用（hello_init），一个在模块被移除时被调用（hello_exit）。module_init和module_exit这两行使用了特殊的内核宏来标明两个行数所扮演的角色。另一个特殊的宏（MODULE_LICENSE）用于告诉内核这个模块具有自由的许可；如果没有这个申明，内核将在模块加载时发出警告。

printk函数定义于Linux内核中并对模块有效；它的作用类似标准C库中的printf函数。内核需要自己的打印函数，因为它独立运行，没有C库的辅助。模块可以调用printk，因为在insmod加载它之后，模块被链接到内核并可以访问内核所公开的符号（函数和变量）。字符串KERN_ALERT是消息的优先级。在这个模块中我们指定了一个高的优先级，因为消息在默认优先级下可能显示不出来，这依赖于你运行的内核版本，klogd守护进程的版本和你的配置。

可以使用insmod和rmmod工具来测试模块。
```
% make
make[1]: Entering directory `/usr/src/linux-2.6.10'
CC [M] /home/ldd3/src/misc-modules/hello.o
Building modules, stage 2.
MODPOST
CC /home/ldd3/src/misc-modules/hello.mod.o
LD [M] /home/ldd3/src/misc-modules/hello.ko
make[1]: Leaving directory `/usr/src/linux-2.6.10'
% su
root# insmod ./hello.ko
Hello, world
root# rmmod hello
Goodbye cruel world
root#
```
为使上面的命令能执行，你必须有一个适当的配置，并且内核树在makefile可以找到的地方（这里是/usr/src/linux-2.6.10）。

根据你的系统投递消息行的机制不同，你的输出也可能不同。特别是上面的屏幕输出是来自于文本终端；如果你在window系统下的模块终端中运行insmod和rmmod，你可能看不到任何东西。消息可以被发送到某个系统日志文件，比如/var/log/messages（各发行版本不同）。内核消息投递机制在Chap4详述。

## 内核模块与应用的差异
多数中小型程序从头至尾执行一个单一的任务，每个内核模块只是注册自己为以后的请求提供服务，它的初始化函数将立即结束。换言之，模块的初始化函数是为将来调用模块的函数作准备的；就好像模块在说“我在这里，这是我可以做的。”。模块的退出函数（例中的hello_exit）函数在模块被卸载之前被调用。它告诉模块“我不存在了；不要再要求我做任何事情。”这类似于事件驱动程序，并非所有应用程序都是事件驱动的，但每个内核模块都是的。事件驱动的应用程序和内核代码另一个主要不同的是退出函数：应用程序结束时可以延时来释放资源或做清除操作，内核模块则必须小心撤销init函数设置的所有东西，或保留一小块直到系统被重新启动。

另外，内核模块卸载的能力是模块化的一个功能，可以节约开发时间，可以测试不同版本的驱动而不用重启机器。

应用程序中通过链接阶段来解决对外部函数库的引用。比如printf就定义在libc中。内核模块只能链接内核；不能链接库。比如printk函数，就像printf的内核内部的版本被导出到模块中。它表现得像printf函数，只有少量的不同，主要的一个就是缺乏浮点支持。
