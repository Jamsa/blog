Title: Rust Mod和文件系统
Date: 2018-08-21
Modified: 2018-08-21
Category: 开发
Tags: rust

本文是读《Rust程序设计语言第二版》Mod和文件系统相关内容的笔记。阅读这本书所敲的代码放在[Github](https://github.com/Jamsa/trpl/blob/master/src/lib.rs)上。代码没有按书的结构分章节创建工程，而是将所有代码放在一个单独的工程中。

# 模块

使用`Cargo`创建新项目时，默认创建的是二进制`crate`而不是创建库`crate`。创建库`crate`要使用`--lib`参数而不是`--bin`参数：

```
$ cargo new communicator --lib
$ cd communicator
```

这时会生成`src/lib.rs`而不是`src/main.rs`。

在上面链接的示例中，我没有使用这种方式创建`mod`。因为敲的所有示例都在一个工程中，所以只需要添加`lib.rs`，`Cargo.toml`中也没有增加内容，只是添加了调用`lib.rs`的[uselib.rs](https://github.com/Jamsa/trpl/blob/master/src/uselib.rs)。


## 模块定义

`Rust`默认只知道`lib.rs`中的内容，通过它来查找对应的`模块名.rs`。

可以在`src/lib.rs`中定义一个或多个模块

```rust
mod network {
    fn connect() {
    }
}

mod client {
    fn connect() {
    }
}
```

在模块外调用这些函数，需要指定模块名并使用命名空间语法`::`，如：`network::connect()`。

模块间是可以嵌套的：

```rust
mod network {
    fn connect() {
    }

    mod client {
        fn connect() {
        }
    }
}
```

## 模块移动到其它文件

位于层级中的模块，非常类似于文件系统结构。可以利用Rust模块系统，使用多个文件分解Rust项目。这样就不需要将所有代码都放在`src/lib.rs`或`src/main.rs`了。

下面我们将要把下面的`client`、`network`和`server`三个模块拆分至各自的`.rs`文件中。

`src/lib.rs`

```rust
mod client {
    fn connect() {
    }
}

mod network {
    fn connect() {
    }

    mod server {
        fn connect() {
        }
    }
}
```

### 第一步：拆分`client`

`src/lib.rs`

```rust
mod client;

mod network {
    fn connect() {
    }

    mod server {
        fn connect() {
        }
    }
}
```

`src/client.rs`

```rust
fn connect() {
}
```

注意在上面的`client.rs`里，不再需要`mod`声明，因为在`src/lib.rs`中已经声明了`client` `mod`。

### 第二步：拆分`network`

`src/lib.rs`

```rust
mod client;

mod network;
```

`src/network.rs`

```rust
fn connect() {
}

mod server {
    fn connect() {
    }
}
```

这个拆分方法与上次一样，只不过在`network.rs`中，保留了`server`模块的声明。

### 第三步：拆分`server`

如果我们按上面的方式继续拆。就是将`src/network.rs`改为

```rust
fn connect() {
}

mod server;
```

并增加`src/server.rs`

```rust
fn connect() {
}
```

但是，在这样修改后`cargo build`会报错。

```
$ cargo build
   Compiling communicator v0.1.0 (file:///projects/communicator)
error: cannot declare a new module at this location
 --> src/network.rs:4:5
  |
4 | mod server;
  |     ^^^^^^
  |
note: maybe move this module `src/network.rs` to its own directory via `src/network/mod.rs`
 --> src/network.rs:4:5
  |
4 | mod server;
  |     ^^^^^^
note: ... or maybe `use` the module `server` instead of possibly redeclaring it
 --> src/network.rs:4:5
  |
4 | mod server;
  |     ^^^^^^
```

这说明`src/network.rs`与`src/lib.rs`在某些方面是不同的。错误信息中建议的方式是：

 1. 新建名为`network`的目录，这是父模块的名字。
 
 2. 将`src/network.rs`移至新建的`network`目录，并重命名为`src/network/mod.rs`。
 
 3. 将`src/server.rs`移动到`network`目录中。
 
整个目录结构变为：

```
└── src
    ├── client.rs
    ├── lib.rs
    └── network
        ├── mod.rs
        └── server.rs
```

移动完毕后，各文件的内容如下：

 1. `src/lib.rs`

```rust
pub mod client;

pub mod network;
```

 2. `src/client.rs`

```rust
pub fn connect(){
    println!("client::connect");
}
```

 3. `src/network/mod.rs`

```rust
pub fn connect(){
    println!("network::connect()");
}

pub mod server;
```

 4. `src/network/server.rs`
 
```rust
pub  fn connect(){
    println!("network::server::connect()");
    println!("in server mod,super::connect() = network::connect() : ");
    super::connect();
}
```

使用`src/usrlib.rs`调用这些模块：

```rust
mod client;
mod network;

use client::connect;

//use network::connect;

fn main() {
    connect();
    network::connect();
    network::server::connect();
    // 从根模块开始引用
    ::client::connect();
}
```

## 模块文件系统的规则

 - 如果`foo`模块没有子模块，应该`foo`的声明放在`foo.rs`文件中。
 
 - 如果`foo`模块有子模块，应该将`foo`的声明放在`foo/mod.rs`中。
 

# 使用`pub`控制可见性

使用`extern crate communicator`可以从外部模块中将`communicator`库`crate`引入到作用域。从外部`crate`的角度来看，我们所创建的所有模块都位于一个与`crate`同名的模块内，即位于`communicator`内部。这个顶层模块被称为`crate`的`根模块`。

即便在项目的子模块中使用外部`crate`，`extern crate`也应该位于根模块（即`src/main.rs`或`src/lib.rs`中）。在子模块中，我们可以像顶层模块那样引用外部`crate`中的项了。

Rust上下文中涉及`公有`和`私有`的概念。所有代码默认是私有的，除了自己之外，别人不允许使用这些代码。如果不在自己的项目中使用某个函数，编译器会警告该函数未被使用。

为了将函数标记为公有，需要在声明的开头增加`pub`关键字。

## 私有性规则

 - 如果一个项是公有的，它能被任何父模块访问
 
 - 如果一个项是私有的，它能被其直接父模块及任何子模块访问

# 在不同模块中引用命名

使用`use`关键字将指定的模块引入作用域；它并不会将其子模块也引入。

枚举也像模块一样组成了某种命名空间，也可以使用`use`来导入枚举成员。

可以使用`*`语法，也称`glob`运算符将某个命名空间下的所有名称都引入作用域：`use TrafficLight::*;`

使用`super`关键字访问父模块：`super::client::connect();`
