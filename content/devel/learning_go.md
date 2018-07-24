Title: Learning Go 笔记
Date: 2015-06-05
Modified: 2015-06-05
Category: 开发
Tags: go

# Learning Go 笔记

## 介绍

### 离线文档

Go自带`godoc`用于查看程序模块的文档。

```shell
godoc builtin
```

### Hello World

```go
/* 这行是必须的，所有 Go 文件都必须以 package 开头，对于可单独运行的程序来说，package main 是必须的 */
package main

import "fmt" //导入 fmt 包

func main(){ //可执行程序入口函数
    fmt.Printf("Hello, world; or 汉字")
}
```

### 变量、类型和关键字

Go 使用类似 C 的语法，行结尾不需要分号，同一行放两个以上语句需要用分号隔开。Go 的变量类型放在变量名后面。如不写作`int a`而应该写作`a int`。声明变量时，变量就被赋予了这种类型的“自然”空值。如`var a int`，`a`值为`0`。`var a string`，`a`值为`""`。也可以将变量的声明和赋值合并为一步：

```go
var a int
a = 15
```

与下面的写法是同等的：

```go
a := 15
```

可以同时声明多个变量：

```go
var (
    x int
    a bool
)
```

`const`和`import`也支持这种写法。声明多个变量时还可以使用`var x, y int`，并且还可以同时赋值

```go
var a,b int
a,b := 20, 16
```

下划线`_`是个特殊的变量，任何赋给它的值都将被丢弃

```go
var b int
_,b := 34, 35
```

申明却未使用的变量在 Go 中是编译错误。

#### 布尔型

布尔值由常量`true`和`false`描述，类型为`bool`

#### 数值类型

Go 有如`int`的数值类型。这些类型的长度与机器相关，32 位机器上它是 32 位的，64 位机器上是 64 位的。int 只有 32 位或 64 位，没有其它的定义。`uint`也是同样的情况。

如果想使用明确的长度，也可以使用`int32`或`uint32`。可用的整数类型列表：`int8, int16, int32, int64, byte, uint8, uint16, uint32, uint64`。`byte`是`uint8`的别名。没有`float`类型，只有`float32, float64`。
所有这些类型的赋值是严格检查的，混合使用这些类型会产生编译错误。

#### 常量

Go 中的常量在编译时创建，只允许是数值、字符串或布尔型。可以使用`iota`建立枚举值：

```go
const (
    a = iota
    b = iota
)
```

第一行`iota`产生的值为`0`，每行增加`1`。甚至可以让 Go 自己重复`iota`：

```go
const (
    a = iota
    b //隐式的 b = iota
)
```
 
#### 字符串

Go 中的字符串是用双引号包括的 UTF-8 字符串。单引号中的是 UTF-8 字符，而不是字符串。
字符串是不可变的。如果希望像 C 中那样以数组的方式操作字符串，则需要使用`rune`，它能将字符串转化为数组：

```go
s := "hello"
c := []rune(s)
c[0] = 'c'
s2 := string(c)
```
 
#### 多行字符串

由于 Go 会自动在行末插入分号，因此需要小心使用多行字符串：

```go
s1 := "Starting part"       //;
    + "Ending part"         //;
s2 := "Starting part" +     //不会添加;
      "Ending part"         //;
```

 s1 写法是错误的。
另一种方法是使用反引号：

```go
s := `Starting part
    Ending part`
```

 要注意这种写法包含了反引号之间的所有字符（换行 ）。

#### Rune

`Rune`是`int32`的别名。它是一个 UTF-8 编码的指针。可以用于遍历字符串中的单个字符。

#### 复数

Go 原生支持复数类型。对应的类型是`complex128`（64 位实部和 64 位虚部）或`complex64`（32 位实部和 32 位虚部）。复数写作`re + imi`，`re`是实部，`im`是虚部：

```go
var c complex64 = 5 + 5i
fmt.Printf("Value is: %v",c)
```

#### 错误

Go 内置了错误类型。`var e error`创建了一个`error`类型的变量`e`，它的值为`nil`。`error`类型是一个接口。

### 操作符和内置函数

Go 支持通常的数值操作符。
Go 不支持操作符重载（或方法重载），但是一些内置的操作符是被重载过的。如：`+`可以用于整数、浮点、复数和字符串。

### 关键字

后面详细描述的关键字

 - `func`定义函数
 
 - `return`从函数中返回
 
 - `go`用于并发编程
 
 - `select`用于选择不同类型的通讯
 
 - `interface`
 
 - `struct`用于定义类型
 
 - `type`

### 控制结构

Go 的控制结构比较少。比如只有`for`是用于循环。`switch`和`if`都能像`for`一样接收初始化语句。另外还有被称为`type switch`和`multiway communications multiplexer(多路通信多路复用器)`的`select`。语法与`C`也有些不同，括号不是必需的，并且左括花号不换行：

```go
if x > 0 { // { 是必需的，且不能放到下一行
    return y
} else {
    return x
}
```

 `if`和`switch`支持初始化语句：

```go
if err := Chmod(8664); err != nil {
    fmt.Printf(err) //err的作用域被限制在 if 的 body 区
}
```

### Goto

Go 有`goto`语句，它能跳转到当前函数范围内的`label`。

### For

Go 的`for`循环有三种形式，只有一种带分号：

```go
for init; condition; post { }  //类似 C 中的 for
for condition { } //类似 while
for { } //无限循环
```

 Go 没有逗号操作符，`++`和`--`是语句不是表达式，如果你想要在`for`中使用多个变量就要使用并行赋值。

```go
for i, j := 0, len(a)-1; i < j; i, j = i+1, j-1 {
    a[i], a[j] = a[j], a[i]
}
```

### Break 和 continue

使用`break`可以退出当前循环。也可以用于跳转到指定的标签位置：

```go
J: for j := 0; j < 5; j++ {
    for i := 0; i < 10; i++ {
        if i > 5 {
            break J
        }
        println(i)
    }
}
```

 使用`continue`可以立即开始下一次循环。

### Range

关键字`range`可以用于循环。它可以用于`slices, array, strings, maps, channel`的循环。`range`是个迭代器，调用它时，它将返回它迭代对象的下一个键值对。
当对`slice`和`array`循环时`range`返回`slice`的`index`和对应位置的值。
也可以直接在字符串上使用`range`。它将解析 UTF-8 字符串并返回单个 Unicode 字符和它的位置。

### Switch

Go 的`switch`非常具有弹性。表达式不需要是常量甚至不需要是整数；`case`从上至下求值，直到找到一个匹配。因此可以使用它编写一个`if-else-if-else`：

```go
func unhex(c byte) byte {
    switch {
        case '0' <= c && c <= '9':
            return c - '0'
        case 'a' <= c && c <= 'f':
            return c - 'a' + 10
        case 'A' <= c && c <= 'F':
            return c - 'A' + 10
    }
    return 0
}
```

可以使用`default`匹配未能匹配的情况。

```go
switch i {
    case 0:
    case 1:
        f()
    default:
        g()
}
```

 `case`可以是逗号分隔的列表：

```go
func shouldEscape(c byte) bool {
    switch c {
        case ' ', '?', '&', '=', '#', '+':
            return true
    }
    return false
}
```

### 内置函数

内置函数不需要包含其它的包。

 - `close`：用于`channel`通讯中关闭`channel`。
 
 - `delete`：用于从`map`中删除一个元素。
 
 - `len`和`cap`：被用于多种不同的类型，`len`用于返回字符串`slice`和数组类型的长度。
 
 - `new`：用于为用户定义的数据类型分配内存。
 
 - `make`：用于为内置类型（`map, slice, channel`）分配内存。
 
 - `copy`：用于复制`slice`。
 
 - `append`：用于拼接`slice`。
 
 - `panic`和`recover`：用于异常机制。
 
 - `print`和`println`：低层次的打印函数可以不依赖于`fmt`包使用。主要用于调试。
 
 - `complex, real, img`：用于处理得数类型。

### Array, slice 和 map

#### Array

定义为：`[n]<type>`，`n`是数组的长度，`<type>`是数组元素的类型。数组的大小是它的类型的一部分，不能增长。数组是值：将一个数组赋值给另一个将会复制所有元素。如果将它传递给函数，函数接收到的将是数组的副本，而不是指针。

定义数组时可以将：`a := [3]int{1,2,3}`写作`a := [...]int{1,2,3}`，Go 会自动计数。

所有字段都必须指定，因此如果定义多维数组将会是如下的结构：

`a := [2][2]int{ [2]int{1,2}, [2]int{3,4}}`

或写作

`a := [2][2]int{ [...]int{1,2}, [...]int{3,4}}`

声明数组时总是会需要在方括号中输入数字或三个点。

定义 Array，slice 和 map 的表达方式已经被简化了：

`a := [2][2]int{ {1,2}, {3,4}}`

#### Slice

`Slice`与`Array`类似，但它可以添加元素。`slice`总是指向它内部的`array`。`slice`与是指向`array`的指针；`slice`是引用类型，将一个 slice 赋值给另一个 slice 时，两者指向同一个内部`array`。
`s1 := make([]int ,10)`创建了一个可以保存 10 个元素的`slice`。`slice := array[0:n]`从 array 中创建`slice`。`len(array) == cap(array) == m`。
使用`[I:J]`语法可以从`array`或`slice`中创建新的`slice`，包含从 I 至 J 的元素，长度为 J - I。

```go
a := [...]int{1,2,3,4,5}
s1 := a[2:4]
s2 := a[1:5]
s3 := a[:]
s4 := a[:4]
s5 := s2[:]
```

超出容量时会产生运行时错误。
使用`append`和`copy`可以扩展`slice`的元素。使用`append`向`slice`中添加0个或多个值到`slice`中将返回如果结果`slice` 的容量不够则会重新分配一块足够大的`slice`存放原有`slice`和新的元素。因此，返回的`slice`内部的数组有可能不是原来的数组。

```go
s0 := []int{0, 0}
s1 := append(s0, 2)
s2 := append(s1, 3, 5, 7)
s3 := append(s2, 20...)     //s3 == []int{0,0,2,3,5,7,0,0}
```

`copy`函数将源`slice`中的元素复制到目标`slice`，并返回复制的元素个数。源和目标可以重叠。可复制的数量是`len(src)`和`len(dst)`的最小值。

#### Map

声明方式：`map[<from type>]<to type>`。

```go
monthdays := map[string]int{
    "Jan": 31, "Feb": 28, "Mar": 31,
    "Apr": 30, "May": 31, "Jun": 30,
    "Jul": 31, "Aug": 31, "Sep": 30,
    "Oct": 31, "Nov": 30, "Dec": 31,    //需要这个逗号
}
```

使用`make`定义`map`：`monthdays := make(map[string]int)`。
使用方括号定位元素：`fmt.Printf("%d\n", somedays["Dec"])`
遍历 map 中的元素：

```go
year := 0
for _, days := range monthdays { //key 未使用，因此是 _
    year += days
}
```

添加元素：`monthdays["Undecim"] = 30`，测试检测元素是否存在：`value,present = monthdays["Jane"]`，如果存在，则`present`为`true`。
删除元素：`delete(monthdays, "Mar")`。

## 函数

函数声明的格式：

```go
type mytype int
func (p mytype) funcname(q int)(r,s int){ return 0,0}
```

 - `func`：关键字
 
 - `p mtype`：函数可以被绑定到指定的类型上。它被称为接收者（`receiver`）
 
 - `funcname`：函数名
 
 - `q int`：函数参数声明。参数是值传递的，会被复制。
 
 - `r,s int`：返回值类型声明。函数可以返回多个值。可以不给出具体名称，只声明类型。只有一个返回值时外部可以不加括号。没有返回值时，可以完全省略掉这个部分。
 
 - `return 0,0`：函数体。

函数声明不需要是有序的。编译器会扫描整个文件，不需要先声明函数原型。

### 作用域

定义在函数外的变量是全局变量。定义在函数内的是局部变量。如果名称相同，局部变量会隐藏局部变量。

### 多值返回

### 命名的返回参数

在函数内可以像使用变量一样使用命名的返回参数。当命名了返回参数时，它们会在函数开始时被初始化为对应类型的零值。如果函数执行没有参数的`return`语句，则命名名返回参数的当前值会被返回。
命名并不是必须的，但它可以让代码变得简短清晰。

### 延时执行的代码（Deferred code）

Go 中的`defer`语句可以指定一个函数，该函数在当前函数退出之前执行。利用它可以编写以下代码，该代码能保证文件在函数退出前被关闭掉：

```go
func ReadWrite() bool {
    file.Open("file")
    defer file.Close()  //将 file.Close() 添加到 defer list
    if failureX {
        return false    //Close() 会被调用
    }
    if failureY {
        return false    //在这里执行
    }
    return true         //在这里执行
}
```

可以将多个函数添加到`deferred list`中：

```go
for i := 0; i < 5; i++{
    defer fmt.Printf("%d", i)
}
```

延时执行函数按`LIFO`执行。因此上面的代码将输出：4，3，2，1，0。
甚至可以在延时执行函数中修改返函数的返回值。

```go
func f()(ret int) {
    defer func() {
        ret++
    }()         //括号是必须的
    return 0    //实际将返回1。
}
```

### 可变长度参数（Variadic parameters）

声明方式：`func myfunc(arg ...int) {}`
在函数内部这些参数是一个`slice`：

```go
for _, n := range arg {
    fmt.Printf("And the number is: %d\n", n)
}
```

如果不指定可变长度参数的类型，它默认为空接口`interface{}`。参数传递：

```go
func myfunc(arg ...int) {
    myfunc2(arg...)
    myfunc2(arg[:2]...)
}
```

### 函数作为值

函数也是值，可以被赋值给变量：

```go
func main() {
    a := func(){
        println("Hello")
    }
    a()
}
```

使用`fmt.Printf("%T\n",a)`来显示`a`的类型，它将显示为`func()`。

### 回调

因为函数也是值，因此它们也可以作为回调函数：

```go
func printit(x int) {
    fmt.Printf("%v\n", x)   //打印出结果
}

func callback(y int, f func(int)) {
    f(y)
}
```

### Panic and recovering

Go 没有这机制。它提供了`panic-and-recover`机制。应该将它作为最后的手段。

#### Panic

它是一个用于停止处理流程并进行`panicking`的内置函数。当函数`F`调用`panic`时，执行过程被停止，延时执行函数（deferred function）被正常执行。`F`将返回。对于调用者来说`F`的行为就像是在调用`panic`函数。这个过程会在调用栈上持续，超越到当前`goroutine`返回，在这个时候程序崩溃。

#### Recover

内置函数`recover`将获取到`panicking goroutine`控制权。Recover 只在 deferred 函数内有效。
在正常执行过程中，调用`recover`将不产生任何效果，并返回`nil`。如果当前`goroutine`处于`panicking`状态，调用`recover`将会捕获到传递给`panic`的值并恢复正常执行。

```go
func throwsPanic(f func()) (b bool) {   //参数f是有可能产生 panic 的函数
    defer func() {
        if x := recover(); x != nil {   //在defer中检查是否产生了 panic
            b = true                    //产生 panic 时修改返回值
        }
    }()
    f()
    return
}
```

## 包

包是函数和数据的集合。文件名可以与包名不同。通常包名用小写字符。包可能会包含多个文件，它们共享相同的名称。

```go
package even

func Env(i int) bool {      //可导出函数
    return i % 2 == 0
}

func odd(i int) bool {      //私有函数
    return i % 2 == 1
}
```

 大写开头的函数是可导出的，小写开头的函数是私有函数。

### 标识符

#### 包名

包名应该是简单的小写单词；不要使用下划线或混合大小写。导入时可以重命名`import bar "bytes"`。
包名是基于它的源码目录的；位于`src/pkg/compress/gzip`使用`compress/gzip`来导入，但是使用时的名称是`bzip`而不是`compress_gzip`或`compressGzip`。
导入的包需要使用名称来引用它的内容，因此包中的导出名称可以避免重复。比如`bufio`中的`Reader`，不需要称为`BufReader`，因为用户必须使用`bufio.Reader`来引用它。
Go 使用`MizedCaps, mixedCaps`格式而不推荐使用下划线分隔多个单词。

#### 包文档

每个包都应该包含包注释，包注释放在包语句的前面。包含多个文件的包，包注释应该只在一个文件中存在。包注释应该介绍并提供整个包的信息。它将会出现在`godoc`的最前面。
每个定义（被导出）的函数应该有一行简单短的注释对其进行说明。

### 测试包

测试文件保存在包目录中，并且命名为`*_test.go`，测试文件与其它 Go 程序一样，但是`go test`只会执行这些测试函数。每个测试函数都有相同的签名，并且名称都是以`Test`开头：`func TestXxx(t *testing.T)`测试成功的函数只需要返回即可，测试失败时可以用下面的函数通知`go test`：

 - `func (t *T) Fail()`：标明测试函数失败，但继续执行。
 
 - `func (t *T) FailNow()`：标明测试函数失败并停止执行，同一文件中的其它测试被跳过，然后继续执行下一个测试。
 
 - `func (t *T) Log(args ...interface{})`：以类似`Print()`的方式格式化它的参数，并记录错误日志。
 
 - `func (t *T) Fatal(args ...interface{})`：等效于在`Log()`后执行`FailNow()`。
 
示例：

```go
package even
import "testing"

func TestEven(t *testing.T) {
    if ! Even(2) {
            t.Log("2 should be even!")
            t.Fail()
    }
}
```

Go 测试工具也允许你编写示例函数，它可以作为文档和测试用例，这些函数需要以`Example`开头：

```go
func ExampleEven() {
    if Even(2) {
        fmt.Printf("Is even\n")
    }
    // Output:
    // Is even
}
```

最后的两行注释是`example`的一部分，`go test`使用它来检查输出并以此判断测试是否失败。

### 常用包

 - `fmt`：格式化输出。
 
 - `io`：提供原始的 I/O 接口。
 
 - `bufio`：实现缓冲 I/O。
 
 - `sort`：集合排序。
 
 - `strconv`：字符串与基础数据类型的转换。
 
 - `os`：操作系统功能接口。
 
 - `sync`：提供同步基础功能，如排它锁等。
 
 - `flag`：命令行参数解析。
 
 - `encoding/json`：用于编码解码`JSON`对象。
 
 - `html/template`：生成文本输出的数据驱动模板。
 
 - `net/http`：解析`HTTP`请求响应，URL提供了一个可扩展的`HTTP`服务和客户端。
 
 - `unsafe`：提供超出 Go 类型安全的功能（指针类型转换等）。通常应该不使用它。
 
 - `reflect`：用于实现运行时反射功能。
 
 - `os/exec`：用于运行外部命令。

## 基础知识

Go 有指针但没有指针运算，因此他们更像 C 里的引用。调用函数时，总是传值的。因此为了修改传递的参数，应该使用指针。
新声明的指针与其它类型一样也被赋了零值，它的值为`nil`，表示它不指向任何东西。为了让它指向某些东西，需要使用取地址操作符`&`来获取地址。

```go
var p *int
fmt.Printf("%v", p)     //nil
var i int
p = &i
fmt.Printf("%v", p)     //指针地址
fmt.Printf("%v\n", *p)  //8
```

### 内存分配

Go 有垃圾收集器，使用`new`和`make`分配内存。它们的区别：

#### `new`

`new`的行为与其它语言中差不多：`new(T)`分配`T`类型的零值并返回它的地址，值为`*T`类型。
要注意返回的是零值。比如`bytes.Buffer`的零值为空的缓冲。`sync.Mutex`的零值是一个未上锁的互斥量。
分配内存与声明都会初始化为零值：

```go
p := new(SyncedBuffer)
var v SyncedBuffer
```

 上面的`p`和`v`都能马上使用。

#### `make`

`make(T, args)`与`new(T)`的目标不同，它只用于创建`slice`，`map`和`channel`，并且它返回的是初始化过的（非零值）`T`而不是`*T`。原因在于这三种类型的底层数据结构在使用前需要初始化。以`slice`为例如果不初始化它的初始值为`nil`。

#### 构造器和初始化

有些情况下零值不能直接使用需要进行初始化。以`os`中的一个方法为例：

```go
func NewFile(fd int, name string) *File {
    if fd < 0 {
        return nil
    }
    f := new(File)
    f.fd = fd
    f.name = name
    f.direinfo = nil
    f.nepipe = 0
    return f
}
```

 可以简化为

```go
func NewFile(fd int, name string) *File{
    if fd < 0 {
        return nil
    }
    f := File{fd, name, nil, 0}
    return &f
}
```

 其中的创建文件对象的一行，还可以简化为：

```go
return &File{fd:fd, name:name}
```

 未传递的字段将会是字段类型的零值。即`new(File)`与`&File{}`是等效的。

### 自定义类型

`type foo int`创建了一个与`int`相同的类型。更复杂的类型需要使用`struct`关键字。

```go
type NameAge struct {
    name string //不导出
    age int     //不导出
}
```

#### 结构字段

结构体的每个项是一个字段：

```go
struct {
    x,y int
    A *[] int
    F func()
}
```

 如果忽略字段名，那么会创建一个匿名字段：

```go
struct {
    T1      //自动产生名称为 T1 的字段
    *T2     //自动产生名称为 *T2 的字段
    P.T3    //自动产生名称为 T3 的字段
    x,y int
}
```

 字段名以大写开头的会被导出，可以被其它包读写。小写开头的字段是对当前包私有的。

#### 方法

有两种方法可以创建处理所定义的类型的函数：
1. 函数调用：创建函数时带类型参数（即函数参数类型）：`func doSomething(n1 *NameAge, n2 int){}`
2. 方法调用：创建只工作于特定类型的函数：`func (n1 *NameAge) doSomething(n2 int){}`，使用：`var n*NameAge; n.doSomething(2)`

使用函数或方法取决于程序员，但是满足接口时必须使用方法。
在上面的情况中这种代码不是错误：`var n NameAge; n.doSomething(2)`这里`a`不是指针。这种情况下 Go 会搜索类型`NameAge`的方法列表，找不到之后将会搜索类型`*NameAge`的方法列表，然后将方法调用转化为`(&n).doSomething(2)`。
定义结构时的方法不同会导致结构所包含的方法也不同，有结构体

```go
type Mutex struct {}
func (m *Mutex) Lock() {}
func (m *Mutex) Unlock() {}
```

 之后定义两种新的类型：

```go
type NewMutex Mutex
type PrintableMutex struct {Mutex}
```

现在`NewMutex`与`Mutex`是相等的，但是它没有`Mutex`的任何方法，它的方法是空的。但是`PrintableMutex`继承了`Mutex`的方法，它的`Mutex`属性上绑定了`Lock`和`Unlock`方法。

### 类型转换

类型转换由操作符完成，但看起来像是函数调用，如：`byte()`。不是所有转换都是允许的。
别名类型同样需要转换，不能直接赋值。

### 组合

当前的 Go 不是面向对象的编程语言因此没有继承，需要实现“继承”效果时可以嵌入一个类型。

## 接口

Go 中`interface`有多种含义。所有类型都有一个接口，就是该类型定义的方法的集合。例如：

```type S struct { i int}
func (p *S) Get() int {return p.i }
func (p *S) Put(v int) { p.i = v }
```

 你可以定义一个接口类型：

```go
type I inteface {
    Get() int
    Put(int)
}
```

 `S`是实现了接口`I`的，因为它定义了两个`I`所需要的方法。注意，实现接口并不需要显式的声明。
使用接口值：

```go
func f(p I) {
    fmt.Println(p.Get())
    p.Put(1)
}
```

这里`p`是一个接口类型的值。`S`实现了接口`I`，我们可以传递指向类型`S`的指针给函数：`var s S; f(&s)`。这里需要传递指针的原因在于我们将方法定义在操作指针类型上了。这不是必需的——我们可以将方法定义的值上——但是`Put`方法将不会按期望的方式工作。

事实上 Go 是鸭式类型，不需要声明一个类型是否实现了某一类型。但它不是纯的鸭式类型，因为 Go 编译嘎嘎将进行静态类型检查，检查精英是否实现了接口。但是，Go 有真正的动态特性，它将一种接口转化为另一接口。通常情况下，这一转换发生在运行时。如果转换失败，程序将出错并产生运行时错误。

Go 中的接口与其它语言中的理念类似：`C++`中的纯抽像虚拟基类，`Haskell`中的`typeclasses`或`Python`中的鸭式类型。但是其它语言没有能组合接口值、静态类型检查、运行时动态类型转换并且不需要显式的在类型声明时声明它满足某个接口。因此 Go 中的接口是非常强大、具有弹性、高效并且易于编写的。

当有多个类型实现某一接口时，可以根据类型进行处理：

```go
func f(p I) {
    switch t := p.(type) {
        case *S:
        case *R:
        case S:
        case R:
        default:
    }
}
```

 在`switch`之外使用`(type)`是非法的。这并不是唯一一种在运行时检查类型的方法。你也可以使用`; ok`的格式检查接口类型是否实现了特定的接口：

```go
if t, ok := something.(I); ok {
    // something 实现了接口 I
    // t 是类型
}
```

 当你确定变量实现了某一接口时可以用`t := something.(I)`

*空接口*
因为每个类型都满足空接口：`interface {}`。我们可以定义一个通用函数以空接口作为它的参数：

```go
func g(something interface{}) int {
    return something.(I).Get()
}
```

 使用这一方法是要注意，传递给`g`的参数不管是否实现了接口`I`时都不会产生编译错误，但在运行时，如果参数未实现接口`I`就会产生运行时错误。

### 方法

方法是有接收者的函数。可以在任何类型上定义方法（不能定义在属于其它包的类型上，同样也包括内置的`int`类型）。但是你可以定义自己的`int`类型然后添加方法：

```go
type Foo int
func  (self Foo) Emit() {
    fmt.Printf("%v", self)
}
type Emitter interface {
    Emit()
}
```

#### 接口类型上的方法

接口定义了方法集，方法包含了实际的代码。即方法是接口的实现。因此接收者（receiver）不能是接口类型。
接收类型必须是`T`或`*T`格式，`T`是类型名。`T`被称为接收者基础类型。这个基础类型不能是指针或接口类型必须定义在与方法相同的包里。

*接口指针*
Go 中使用接口指针是没有必要的。实际上创建指向接口值的指针是非法的。

### 接口名称

通常，只有一个方法的接口被命名为方法名加`-er`后缀。

#### 内省和反射

下例展示了如何通过反射包检查定义在类型`Person`中的`tag`（`namestr`）：

```go
type Person struct {
    name string "namestr"   // namestr 是 tag
    age int
}
func ShowTag(i interface{}) { //使用 *Person 来调用
    switch t := reflect.TypeOf(i); t.Kind() {
        case reflect.Ptr:
            tag := t.Elem().Field(0).Tag
    }
}
```

 使用反射获取类型和值

```go
func show(i interface{}) {
    switch t := i.(type) {
        case *Person:
            t := reflect.TypeOf(i)  //类型元数据
            v := reflect.ValueOf(i) //实际值
            tag := t.Elem().Field(0).Tag
            name := t.Elem().Field(0).String()
    }
}
```

 设置值的方式与获取值的方式类似，但是只允许在导出成员上使用，在私有成员上使用时会产生运行时错误。

## 并发程序

`goroutine`与已有的线程、协程或进程等概念不完全一样。它有自己的模型：它是与其它`goroutine`并行执行的，有着相同的地址空间的函数。它是轻量级的，仅比分配栈空间多一点点消耗。而初始时栈是很小的，所以它们也是廉价的，并且随着需要在堆空间上分配（和释放）。

`goroutine`是个普通函数，只需要使用关键字`go`作为 开头。

```go
ready("Tea", 2)     //普通函数调用
go ready("Tea", 2)  //作为 goroutine 运行
```

 在程序退出时，所有`goroutine`都会停止。为了修复这个问题，需要一些能够同`goroutine`通讯的机制。这一机制通过`channels`的形式使用。`channel`与`Unix shell`中的双向管道类似：可以通过它发送或接收值。这些值只能是特定的类型：`channel`类型。定义它时也需要定义发送到`channel`的值的类型。必须使用`make`创建`channel`。

```go
var c chan int  //定义传输整数的全局的 channel
func ready(w string, sec int) {
    time.Sleep(time.Duration(sec) * time.Second)
    ft.Println(w, "is ready!")
    c <- 1      //发送整数 1
}
func main(){
    c = make(chan int)  //初始化 c
    go ready("Tea", 2)  //开始 goroutine
    go ready("Coffee", 1)
    fmt.Println("I'm waiting, but not too long")
    <-c     //从 channel 上接收值，收到的值将被丢弃
    <-c
}
```

 这个列子仍然有些问题，它从`channel`上读取了两次。如果在不知道启动了多少个`goroutine`的情况下怎么办呢？这就要使用到 Go 的另一个关键字：`select`。通过`select`可以监听`channel`上输入的数据。将上例中的两行`<-c`换以下代码之后，程序会一直等下去，只到从`channel c`上收到多个响应时才会退出循环L。

```go
L: for {
    select {
        case <- c:
            i++
            if i > 1 {
                break L
            }
    }
}
```

 虽然`goroutine`是并发执行的，但它们并不是并行运行的。如果不告诉 Go 额外的东西，同一时刻只会有一个`goroutine`执行。利用`runetime.GOMAXPROCS(n)`可以设置`goroutine`并行执行的数量。
 
`GOMAXPROCS`设置了同时运行的`CPU`的最大数量，并返回之前的设置。如果`n<1`，不会改变当前设置。也可以通过设置环境变量`GOMAXPROCS`为它设置值。

### 更多关于 channel

在 Go 中使用`ch := make(chan bool)`创建`channel`时，`bool`型的无缓冲`channel`将被创建。这意味着：首先，如果读取（`value := <- ch`）它将会被阻塞，直到有数据接收。其次，任何发送（`ch<-5`）将会被阻塞，直到数据被读出。无缓冲`channel`可以方便的在多个`goroutine`间同步。

Go 也允许指定`channel`缓冲区的大小，用于设定`channel`可存储元素的数量。`ch := make(chan bool, 4)`创建了可以存储 4 个元素的`bool`型`channel`。

*关闭 channel *
当`channel`被关闭后，读取端需要知道这个事情。下面的代码演示了如何检查`channel`是否被关闭:

```go
x, ok = <-ch
```

 当`ok`为`true`时意味着`channel`未被关闭，可以读取数据。否则表示它已经被关闭了。

## 通讯

### io.Reader

Go 的 I/O 核心是接口`io.Reader`和`io.Writer`。
在 Go 中读写文件使用`os`包就可以了：

```go
package main
import "os"
func main() {
    buf := make([]byte, 1024)
    f, _ := os.Open("/etc/passwd")
    defer f.Close()
    for {
        n, _ := f.Read(buf)
        if n == 0 { break }
        os.Stdout.Write(buf[:n])
    }
}
```

 缓冲 I/O，则需要`bufio`包：

```go
package main
import {"os"; "bufio"}
func main() {
    buf := make([]byte, 1024)
    f, _ := os.Open("/etc/passwd")
    defer f.Close()
    r := bufio.NewReader(f)
    w := bufio.NewWriter(os.Stdout)
    defer w.Flush()
    for {
        n, _ := r.Read(buf)
        if n == 0 { break }
        w.Write(buf[0:n])
    }
}
```
 
### 命令行参数

命令行参数在程序中通过`os.Args`获取。`flags`包提供了接口来解析参数。

### 执行命令

`os/exec`包可以执行外部命令，这也是在 Go 中主要的执行命令的方法。

### 网络

所有网络相关的类型和函数可以在`net`包中找到。
