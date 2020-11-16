---
title: "Python虚拟环境管理"
date: 2018-05-12
modified: 2018-05-12
categories: ["开发"]
tags: ["python"]
---

Python虚拟环境的管理工具有很多种，我常用的有pyenv、virtualenv和conda。最近因为折腾深度学习环境经常需要安装不同版本的keras、tensorflow、pytorch等，折腾下来后总结下他们的区别。

- pyenv

可以用来安装多个不同的python发行版，除python官方版本外，也可以用来安装anaconda、miniconda。可以解决项目对python版本的依赖问题。

- virtualenv

可以为不同的项目创建隔离的python库环境。我之前的web项目多数使用它来进行环境隔离。一般可认为它不跨python解释器版本。

- pyenv-virtualenv

pyenv的一个插件，整合了pyenv和virtualenv。

- conda

既可以管理多个python版本，也可以管理项目的依赖环境。可以认为它是pyenv + virtualenv + pip的组合。

在包管理方面pip与conda的区别主要在于pip对本地库的跟踪不太好。即使有wheel，一些python程序库的本地库依赖仍然需要在操作系统中手工安装。由于不同python版本对本地库的依赖可能不一样，特别是在本地库依赖比较复杂的时候，手工安装就不便于跨多个python版本使用。比如，要同时在python2和python3下安装多个版本的cuda和cudnn的时候。conda在安装包的时候，本地库依赖基本上是由conda安装预编译好的版本。

在虚拟环境管理方面virtualenv与conda的方式也不完全相同。virtualenv在创建虚拟环境时，通过shim的方式调用发行版本对应的python解释器（应该也包括在发行版全局安装的其它程序，未测试）。而conda创建的虚拟环境则更彻底，连python解释器及基本的python包都会在虚拟环境中重新安装一份。带来负面影响是conda安装的虚拟环境通常会比virtualenv更占空间。

为了兼顾两者的优点，我同时在使用pyenv、pyenv-virtualenv、conda。安装的方式为：

1. 安装pyenv和pyenv-virtualenv。

2. 通过pyenv安装miniconda。

3. 通过pyenv activeate miniconda激活conda环境。

4. 通过conda创建各种深度学习隔离环境。

5. 使用的时候，通过minicnoda中的activate来激活conda创建的隔离环境（pyenv官方有对conda虚拟环境的支持，但是存在问题，建议使用miniconda自己的机制来管理conda环境切换）。
