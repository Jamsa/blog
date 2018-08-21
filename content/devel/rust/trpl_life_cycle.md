Title: Rust变量生命周期管理
Date: 2018-08-21
Modified: 2018-08-21
Category: 开发
Tags: rust

本文是读《Rust程序设计语言第二版》生命周期相关内容的笔记。

# 生命周期

Rust生命周期用于控制变量的作用域，主要目标是避免悬垂引用。

以下面的代码为例

｀``rust
{
    let r;

    {
        let x = 5;
        r = &x;
    }

    println!("r: {}", r);
}
```

编译时会产生如下错误：


```
error: `x` does not live long enough
   |
6  |         r = &x;
   |              - borrow occurs here
7  |     }
   |     ^ `x` dropped here while still borrowed
...
10 | }
   | - borrowed value needs to live until here
```

因为`x`变量离开作用域后会被释放，导致`r`无法正常使用。

编译器中的这个部分被称为`借用检查器`，它比较变量的作用域，以保证所有的借用都是有效的。

以下面这段可正确编译的代码为例：

```rust
{
    let x = 5;            // -----+-- 'b
                          //      |
    let r = &x;           // --+--+-- 'a
                          //   |  |
    println!("r: {}", r); //   |  |
                          // --+  |
}                         // -----+
```

由于`x`的生命周期`'b`比`r`的生命周期`'a`要大，Rust知道`r`中的引用在`x`有效的时候也总是会有效。

如果将它修改为

```rust
{
    let r;                // -------+-- 'a
                          //        |
    {                     //        |
        let x = 5;        // -+-----+-- 'b
        r = &x;           //  |     |
    }                     // -+     |
                          //        |
    println!("r: {}", r); //        |
}                         // -------+
```

Rust编译器会发现`x`的生命周期`'b`比`r`的生命周期`'a`要小得多，即被引用者比引用者存在的时间更短，因此无法编译。

# 生命周期注解

以书中`longest`函数为例：

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
```

函数签名中的`'a`为生命周期参数，它不改变任何传入后返回值的生命周期，它主要用于借用检查。在这里的含义是指：函数会获取到两个参数，它们都与生命周期`'a`存在一样长的字符串`slice`。函数返回一个同样与生命周期`'a`一样长的字符串`slice`。

当具体的引用传入`longest`时，被`'a`替代的生命周期是`x`与`y`的作用域相重叠的部分。即`'a`的具体生命周期会等于`x`和`y`的生命周期较小的那个。因为我们用`'a`标了返回引用值，因此返回引用值也只会在`'a`生命周期内有效，即与`x`和`y`中较短的生命周期结束之前保持有效。

因此，下面这段代码能编译通过：

```rust
fn main() {
    let string1 = String::from("long string is long");

    {
        let string2 = String::from("xyz");
        let result = longest(string1.as_str(), string2.as_str());
        println!("The longest string is {}", result);
    }
}
```

如果调整这段代码为

```rust
fn main() {
    let string1 = String::from("long string is long");
    let result;
    {
        let string2 = String::from("xyz");
        result = longest(string1.as_str(), string2.as_str());
    }
    println!("The longest string is {}", result);
}
```

编译将无法通过。即使去掉`println!`行，也无法编译通过。

按正常理解，这段代码里到`println!`这行，`string1`和`result`应该是有效的，因为最长的变量`string1`和返回值`result`都没有离开作用域。

但是，由于生命周期参数告诉Rust，`longest`函数所返回引用的生命周期，应与传入参数的生命周期中较短的那个保持一致。（'a所指代的是x和y生命周期相重叠的部分，而返回值生命周期应该与此重叠部分相同，即等于较短的那个）而这里`result`的生命周期已经超过了`string2`的生命周期，因此，无法通过借用检查。

返回值的生命周期注解应与参数相关联，无关联时也将出现编译错误。例如：

```rust
fn longest<'a>(x: &str, y: &str) -> &'a str {
    let result = String::from("really long string");
    result.as_str()
}
```


# 生命周期省略

以下函数不需要添加生命周期注解也能成功编译：

```rust
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}
```

在Rust的早期版本（pre-1.0）中，这样的代码是无法编译的。Rust团队将一些常用的模式编码进了编译器，检查器能在这些固定的模式下推断出生命周期，而不再强制显式的增加注解。

被编码进Rust引用分析的模式被称为`生命周期省略规则`。这些规则是一些特定的场景，此时编译器会考虑，如果代码符合这些场景，就不需要指定生命周期参数。

省略规则并不能推断所有的情况，如果Rust无法推断生命周期时，它会给出编译错误。

## 编译器判断不需要明确生命周期注解的规则

定义：函数或方法的参数的生命周期被称为`输入生命周期（input lifetimes）`，而返回值的生命周期被称为`输出生命周期（output lifetimes）`。

编译器判断不需要明确生命周期注解的规则有3条。第一条适用于输入生命周期，后两条适用于输出生命周期。检查完三条规则后，仍然存在无法计算出生命周期的引用时，编译器将报错。

 - 每一个是引用的参数都有它自己的生命周期参数。换句话说就是，有一个引用参数的函数有一个生命周期参数：`fn foo<'a>(x: &'a i32)`，有两个引用参数的函数有两个不同的生命周期参数，`fn foo<'a, 'b>(x: &'a i32, y: &'b i32)`，依此类推。
 
 - 如果只有一个输入生命周期参数，那么它被赋予所有输出生命周期参数：`fn foo<'a>(x: &'a i32) -> &'a i32`。

 - 如果方法有多个输入生命周期参数，不过其中之一因为方法的缘故为`&self`或`&mut self`，那么`self`的生命周期被赋给所有输出生命周期参数。这使得方法编写起来更简洁。
 
# 静态生命周期

`static`生命周期存活于整个程序期间。

所有字符串字面值都拥有`static`生命周期。字面值相当于：

```rust
let s: &'static str = "I have a static lifetime.";
```


 
