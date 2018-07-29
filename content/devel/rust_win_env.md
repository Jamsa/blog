Title: 使用 Chocolatey 在 Win10 下配置 rust 开发环境
Date: 2018-07-29
Modified: 2018-07-29
Category: 开发
Tags: rust, chocolatey, cargo, msvc, racer

# 简介

最近因学习`rust`编程语言，需要在家中的 Win10 系统上安装`rust`开发环境。

安装的目标是在`vscode`中配合`racer`实现代码提示功能。

因刚开始接触`rust`对于`rust`的不同`channel`、`toolchain`及`racer`的情况都不太了解所以起了不少弯路，所以编写本文档记录下相关的过程。

主要参考了：

 - [rustup 安装说明](https://github.com/rust-lang-nursery/rustup.rs/#other-installation-methods)

 - [Rust 开发环境指北](https://zhuanlan.zhihu.com/p/26944087?open_source=weibo_search)

 - [racer 安装说明](https://github.com/racer-rust/racer)

基础概念：

 - `rustup`：是`rust`官方推荐的`rust`多版本维护工具。它的功能类似于`Python`的`Conda`或`pyenv`这类工具。

 - `cargo`：是`rust`的构建工具。它的功能类似于`Python`的`pip`或`Java`的`Maven`等工具，既可以管理依赖也可以管理项目的构建。

 - `racer`：是一个支持`vscode`和`emacs`等编译器的`rust`代码自动完成的工具。

 - `crate`：`rust`中的程序库。

# `rust`的安装

## `rust`的版本选择

`rust`在 Windows 上有多个版本可供选择，主要是因为`rust`编译器目前还依赖于`c`的链接工具，一些第三方的库在构建时依赖于`c`工具链。早期的`rust`版本主要使用`mingw`来进行编译，这个版本被称为`gnu`版，从官方文档来看，这个版本应该是包含了`mingw`的一些工具，不需要安装额外的工具。另一个版本，也是官方推荐的版本是使用`msvc`，它使用`Visual Studio`进行构建，需要安装`Visual Studio`，以便在编译程序时使用相关的编译构建工具。加上`cpu`架构分`i686`和`x86_64`，这样版本选择就有了`2*2=4`个，再算上`rust`的三个版本通道`stable`、`beta`、`nightly`，一共就有了`12`个可供选择的版本。那么如何选择版本呢？官方更推荐使用`msvc`版本，`racer`的 [github](https://github.com/racer-rust/racer) 上提示，从 2.1 版开始，它需要使用 `nightly` 版本才能编译。 我试了用`stable`进行编译，会产生错误`#![feature(rustc_private, box_syntax)]`，看错误信息是因为`stable`不支持`feature`这个函数（刚入门，不确定它是否是函数）。这样我就选择了`nightly`通道上的`msvc`版本。

根据选择的版本，我们需要安装以下程序：

 - `rustup`

 - `msbuilder`及`vcbuilder`

 - `cmake`

## `rustup`及`toolchain`的选择

我使用 [chocolatey](https://chocolatey.org) 管理 Windows 上的软件安装。

在`chocolatey`网站上搜索`rustup`是搜索不到的，因为它不是`stable`软件。需要使用以下命令进行安装。

```
choco install rustup --pre
```

安装完`rustup`之后，默认它会安装`stable msvc`版的编译器及相关工具，我们需要切换至`nightly msvc`。使用以下命令来安装`nightly`版本，并将其设置为默认使用的版本。这里我还删除了`stable`版本。

```
rustup toolchain add nightly
rustup toolchain remove stable
rustup default nightly
```

使用`rustup`从官网下载的速度比较慢。也可以设置`rustup`的镜像仓库以提高`rustup`的下载速度。这个设置没有配置文件，只需要设置环境变量:

```
set RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static
set RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup

```

至此`nightly msvc`版本的`rust`编译器及其工具已经安装完毕。

# 编译工具链的安装

## 安装`msbuild`、`vctools`和`cmake`

安装完`rust`的工具后，就已经可以编译`rust`程序了。安装`msbuild`和`vctools`主要是因为在编译`racer`及其它依赖于`c/c++`编译器的程序库时需要它们。`cmake`则是因为`racer`的安装说明中提到编译`racer`时依赖于`cmake`。

使用以下命令可以完成编译工具链的安装
```
choco install microsoft-build-tools
choco install visualstudio2017-workload-vctools
choco install cmake
```
开始的时候我认为安装完`microssoft-build-tools`就会包含`vctools`，因为在`msbuild 2015`中是包含了`c/c++`工具链的。只安装`microsoft-build-tools`就直接编译`racer`会报找不到`link.exe`的错误，查询`chocolatey`上的包信息，可以看到`microsoft-build-tools`在当前实际指向[visualstudio2017buildtools](https://chocolatey.org/packages/visualstudio2017buildtools)这个包，这个包的说明中有明确的说明

```
By default, the package installs only the bare minimum required (the MSBuild Tools workload). The easiest way to add more workloads is to use the workload packages:
- .NET Core build tools
- Visual C++ build tools
- Web development build tools.
```

它只包含了最小的依赖，如果需要使用`vctools`需要安装额外的`workload`，即`visualstudio2017-workload-vctools`。

至此，编译`racer`需要的工具都已经准备好了。

# 编译安装racer

按`racer`官方文档只需要使用`cargo +nightly install racer`即可编译安装了。但是我在编译时，遇到了几个问题。

## 设置`crate`镜像仓库

在使用`cargo`编译程序时会自动从`crate`仓库下载程序的依赖，过程类似于`maven`仓库或`npm`仓库中下载依赖。默认的`crate`仓库的访问速度非常慢，可以在`%HOME%\.cargo\config`中添加以下内容，以切换至中科大的`crate`镜像仓库：

```
[registry]
index = "git://mirrors.ustc.edu.cn/crates.io-index"
```

## 设置PATH环境变量

上面安装的一系列工具都没有设置到`PATH`中去，使用不方便，也会影响`cargo`命令的执行。我使用`cmder`，直接将对`PATH`的修改放在了`cmder`的设置中。相关内容如下：

```
set PATH=%ConEmuBaseDir%\Scripts;%PATH%;C:\Program Files\Git\bin;C:\tools\miniconda3\Scripts;C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\MSBuild\15.0\Bin\amd64;C:\Program Files\CMake\bin;C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Auxiliary\Build;C:\Users\Lenovo\.cargo\bin\;
```

主要添加了`cargo`和`msbuild`相关的目录。

## 开始编译

完成上述设置后，我开始使用`cargo +nightly install racer`构建`racer`，结果报错了：

```
Compiling same-file v1.0.2 (registry `git://mirrors.ustc.edu.cn/crates.io-index`)
error: failed to run custom build command for `libssh2-sys v0.2.8 (registry `git://mirrors.ustc.edu.cn/crates.io-index`)`
process didn't exit successfully: `C:\Users\Lenovo\AppData\Local\Temp\cargo-installN2GxW9\release\build\libssh2-sys-7b470d6e1aaab76f\build-script-build` (exit code: 101)
--- stderr
fatal: not a git repository (or any of the parent directories): .git
thread 'main' panicked at '

couldn't determine visual studio generator
if VisualStudio is installed, however, consider running the appropriate vcvars script before building this crate
', C:\Users\Lenovo\.cargo\registry\src\mirrors.ustc.edu.cn-61ef6e0cd06fb9b8\cmake-0.1.31\src\lib.rs:552:25
note: Run with `RUST_BACKTRACE=1` for a backtrace.

warning: build failed, waiting for other jobs to finish...
error: failed to compile `racer v2.1.3 (registry `git://mirrors.ustc.edu.cn/crates.io-index`)`, intermediate artifacts can be found at `C:\Users\Lenovo\AppData\Local\Temp\cargo-installN2GxW9`

Caused by:
  build failed

```

从`racer`和`rust`的`issue`中查到是构建工具的问题，那么问题有可能出在`msbuild`或`rust`的`cmake`库，或者`cmake`本身。在查`couldn't determine visual studio generator`的时候还走了不少弯路，看到`issue`上贴出的代码还以为是`rust`和`cmake`库不支持`vs2017`，因为`issue`上的这个错误，就是因为`rust cmake`库上写死了`vsbuild`的版本，从代码来看高于`vs2015`的版本就不认了，有人也确实是使用`vs2015`就没有报这个错误。

在查阅`rust cmake`库的[相关代码](https://github.com/alexcrichton/cmake-rs/blob/4a45b77f7e1734a7929ec5c64d4a4b1d9397b24a/src/lib.rs#L575)发现新版本已经是支持`vs2017`的了，那问题就有可能是出在`vsbuild`本身上了。

因为`rust`官网对于安装`vs`并没有明确，推荐的链接是安装完整的`visual studio community`并包含`c/c++`选项，而我安装的只是构建工具链。一开始我认为需要安装完整的`visual studio`，后来才想起来`vsbuild`和`vctool`的 2017 版在使用前是需要设置环境变量的。

先在控制台中运行

```
"C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64
```

会配置好相关的环境变量，之后再使用`cargo +nightly install racer`进行构建和安装就没有问题了。

# 开发工具

## 编辑器集成

参照[Rust 开发环境指北](https://zhuanlan.zhihu.com/p/26944087?open_source=weibo_search)在`vscode`中安装`rust`相关插件，使用`cargo`在`rust`环境上安装相关的程序库和`rust`源码，就可以实现代码提示功能，此处不再缀述。

## 调试器

可参照[这篇文章](https://www.brycevandyk.com/debug-rust-on-windows-with-visual-studio-code-and-the-msvc-debugger/)进行配置。我使用的时候报错误了，没有找到`rust`源码，应该是我没有设置`rust`源码目录的环境变量所致。

`vscode`中使用的是`c/c++`调试器，不知道是否仍然需要安装完整的`vscode`才会包含相应的调试器。

花了一天多折腾到当前这个状况，对于我个初学者已经够用了。
