---
title: "Programming in Scala 的读书笔记"
date: 2010-12-27
modified: 2010-12-27
categories: ["开发"]
tags: ["scala"]
---

# 语言基础

## 变量定义
 - scala的两种变量：val和var。val类似Java中的final变量。

 - scala中使用类型推断：
```scala
val msg = "Hello, world"
```
 scala根据后面的字符串推断出msg是String类型的。

 - 在变量名后添加冒号和变量类型可以显式指定变量类型：
```scala
val msg:String = "hello, world"
```

## 函数定义
 - 例
```scala
def max(x: Int, y: Int): Int = {
  if (x > y) x
  else y
}
```

 - 括号外等号之前的类型为max的返回类型。这里可以不用显式的指定返回类型，编译器会推断出类型。但有时会需要显式的指定，比如函数是递归的时。
 
 - 如果函数仅由一个句子组成，可以不写等号后的大括号
```scala
def max2(x: Int, y: Int) = if (x > y) x else y
```

 - 不带参数也无返回值的函数
```scala
def greet() = println("Hello, world!")
```
 解释器回应`greet: ()Unit`。空括号表示函数不带参数。Unit是greet的结果类型。相当于Java中的void。

##  Scala脚本
 - 在脚本中使用args(0)来访问命令行参数。

##  while循环
 - Scala默认的缩进风格是缩进2格。
 - Java风格的i++和++i在Scala无效，自增必须写成`i = i + 1`或`i += 1`
 - Scala和Java一样，while或if的布尔表达式要放在括号里。

##  foreach和for表达式
 - foreach
```scala
args.foreach(arg: String) =>  println(arg))
```

 - foreach的参数被称作function literal。它的标准格式是
```scala
(x: Int, y: Int) => x + y
```
 例子中arg的类型也可以去掉，因为编译器可以根据args的类型推断出arg的类型


 - foreach偏应用函数版本
```scala
args.foreach(println)
```

 - for表达式
```scala
for(arg <- args)
  println(arg)

for(i <- 0 to 2)
  println(i)
```
 to是一个带Int参数的方法。`0 to 2`被解释为`(0).to(2)`。这里arg和i没有说明它是var还是val，但它总会是val，因为在循环体中不能修改它们的值。

##  类型参数化数组
 - 类型化参数类似Java中的泛型类型参数。
```scala
val greetStrings = new Array[String](3)
greetStrings(0) = "Hello"
```
 Scala里访问数组元素时是将索引放在圆括号里。从这里也可以看出来val的不可变。定义的val不能重新赋值，但并不代表val对象本身不可变。如上面给数组的第1个元素赋值。

 - Scala没有操作符重载，都是方法调用。`+-*/`都可以作为方法名称。包括对数组的访问也是使用()，而不是方括号，它实际上调用是是数组的apply方法，因为当在一个变量上使用括号时，默认将调用这个变量的apply方法。如`greetString(0)`将被转化为`greetString.apply(0)`。而当对带括号并包含一个到多个参数的变量赋值时，将调用变量的update方法。如`greetString(0)="Hello"`将被转化为`greetString.update(0,"Hello")`。

 - 通过伴生对象中的工厂方法创建数组：
```scala
val numNames = Array("zero","one","two")
```
 这个代码调用了class Array的伴生对象object Array的apply方法，这个apply方法能接收可变数量的参数。

##  List

 - scala.List不同于Java的List它是不可变的。

 - 使用cons方法`::`将元素添加到原来的List之前产生新的List。

 - 使用`:::`可以将两个List连接起来产生新的List。

 - 定义空类可以使用Nil，而定义新的List可以将所有元素用cons（即::）连接，最后再连接一个Nil。

 - List不支持append，append将随列表长度变长耗时将线性增长。使用cons连接的耗时是常量时间。可以通过cons连接后再调用reverse，或使用ListBuffer，ListBuffer支持以append方式操作可变列表。

##  Tuple

 - 元组也不可变，它与List不同的时它可以保存不同类型的元素。

 - 初始化：
```scala
val pair = (99, "Luftballons")
println(pair._1)
println(pair._2)
```

 - 元组的类型取决于它的元素数量。pair的类型是Tupe2[Int, String]。而('u','r','the',1,4,"me")则是Tupe6(Char,Char,String,Int,Int,String)。

 - 访元组元素问时从_1开始。当前版本的Scala只支持到_22。

 - 元组没有使用括号来访问元素，因为apply方法返回的元素是同一类型的。而元组中访问不同元素时，返回类型是不同的。

##  Set和Map
 - Scala中有两套Set和Map，分别支持可变和不可变的方式使用Set和Map。不可变类型是默认的，不需要导入。

 - 两套Set特质都扩展了scala.collection.Set这个特质。分别是scala.collection.immutable.Set和scala.collection.mutable.Set。这两个特质都可以调用+方法添加元素，但两者的行为不同，可变集将会把元素添加到自身，而不可变集将会创建一个包含了新元素的新集。

 - 使用可变集时变量可以是val，但变量内部的元素数量仍然可以改变。而使用不可变集添加元素时如果要将新集保存到原来的变量上，则要使用var，因为不可变集在添加新元素后将返回一个新的集。

 - Set伴生对象定义了apply工厂方法。

 - 两个Map特质都扩展了scala.collection.Map这个特质。分别是scala.collection.immutable.Map和scala.collection.mutable.Map。

 - Map元素使用`->`方法来添加元素。在任何对象上调用`->`将产生一个包含键和值的二元元组，这个是通过隐式转换来实现的。Map的基本操作：
```scala
import scala.collection.mutable.Map
val treasureMap = Map[Int, String]()
treasureMap += (1 -> "Go to island")
treasureMap += (2 -> "Find big X on ground")
treasureMap += (3 -> "Dig.")
```
 使用不可变Map，不需要导入
```scala
val romanNumeral = Map(
 1 -> "I", 2 -> "II", 3 -> "III", 4 -> "IV", 5 -> "V"
println(romanNumeral(4))
```

##  函数式风格
 - 崇尚val，不可变对象和没有副作用的方法。只在特定情况下才使用var，可变对象和有副作用的方法。

##  从文件里读取行

 - List对象的reduceLeft方法接收的函数将会应用于List的头两个元素，然后再把函数应用于第一次计算的结果和第三个元素，依次下去，并返回最后一次的计算结果。例如，计算长度最长的行：
```scala
val longestLine = lines.reduceLeft(
  (a,b) => if (a.length > b.length) a else b
)
```


#  类、字段和方法
 - 类定义包含字段（val或var）和方法（用def定义）统称为：成员。

 - 传递给方法的参数都是val，不能重新赋值。

 - 方法最后的return语句是可选的，如果没有发现任何显式的返回语句，Scala方法将返回方法中最后一个计算得到的值。推荐的风格是避免显式的尤其是多个返回语句。代之以把每个方法当作是创建返回值的表达式。鼓励构建很小的方法，把大的方法分解成多个更小的方法。

 - 方法如果仅计算单个结果表达式，可以去掉大括号。
```scala
class ChecksumAccumulator {
  private var sum = 0
  def add(b: Byte): Unit = sum += b
  def checksum(): Int = ~(sum & 0xFF) + 1
}
```

 - 没有参数的方法很像是过程（procedure），是一种为了副作用而执行的方法。表示这种方法的另一种方式是去掉结果类型和等号。例如：
```scala
class ChecksumAccumulator {
  private var sum = 0
  def add(b: Byte) { sum += b }
  def checksum(): Int = ~(sum & 0xFF) + 1
}
```

 - 去掉方法体前的等号后，方法的结果将注定是Unit。即使方法最后一行的结果不是Unit，仍然将返回Unit。

 - public是Scala方法的默认访问级别。

 - 跨行的表达式中，操作符要放在上一行的行末。或者将表达式包含在括号中。
```scala
x + 
y

(x
+ y)
```

##  分号推断的规则

 - 疑问行由一个不能合法作为语句结尾的字结束，如句点或中缀操作符。

 - 下一行开始于不能作为语句开始的字。

 - 行结束于括号或方括号内部，因为这些符号不可能容纳多个语句。

##  Singletone对象

 - Scala没有静态成员，而是提供了单例对象。

 - 当单例对象与类同名时，被称作类的伴生对象。它们必须在同一个源文件里定义。类和它的伴生对象可以互相访问私有成员。

 - 单例对象不带参数，而类可以，因为它不能用new来初始化。每个单例对象都被作为由一个静态变量指向的虚构类的一个实例来实现，因此它们与Java静态类有着相似的初始化语法。它会在第一次访问时初始化。虚构类的名称是对象名加一个美元符号。

 - 不与伴生类共享相同名称的单例对象被称为孤立对象。程序的入口main函数要求被定义在孤立对象中。

##  Scala程序
 - 要执行Scala程序，一定要提供一个main方法，它仅带一个参数，Array[String]，且结果类型为Unit的孤立单例对象。

 - Scala隐式的导入了java.lang和scala的成员，和名为Predef的单例对象中的成员到每个Scala源文件中。

 - Scala里并不要求类名和文件名相同。如果不是脚本，推荐的风格是像Java那样按类名来命名文件。

##  Application特质
 - 大括号之间的代码被收集进了单例对象的主构造器，并在类被初始化时执行。

 - Application特质中不能访问传递给main的参数。

 - 因为某些JVM线程模型的局限，如果程序是多线程的就需要显式的main方法。通常只在程序较简单和单线程的情况下才使用Application特质。

#  基本类型的操作

##  基本类型
 - Byte，Short，Int，Long和Char被称为integral类型。Float和Double被称为numeric类型。

 - 除String位于java.lang包外，其余所有基本类型都是scala的成员。

##  文本表示

 - 整数、浮点、字符、字符串的表示与Java类似。

 - raw String用三引号包含，不需要转义。

 - 符号文本写作`'标识符`，这里标识符可以是任何字母或数字标识符。这种文本被映射成预定义类scala.Symbol的实例。;`'cymbal`将被编译器扩展为工厂方法调用：Symbol("cymbal")。符号对象可以访问它的name属性。符号是被interned的，即把同一符号文本写两次时，两个表达式将指向同一个Symbol对象。

 - 布尔类型只有true和false。

##  操作符和方法

 - Scala中任何方法都可以当作操作符

 - 中缀操作符前后带两个操作数

 - 前缀操作符和后缀操作符都是unary的，它们仅有一个操作数。这些前缀操作符是在值类型对象上调用方法的简写方式。在这种情况下，方法名在操作符上前缀了“unary_”。例如Scala会把表达式`-2.0`转换成方法调用`(2.0).unary_-`。可以当作前缀操作符的标识符只有`+ - ! ~`。如果使用其它其它符号，如`unary_*`则不能像`*p`这样调用，只能写作`p.unary_*`。

 - 后缀操作符是不用点或括号调用的不带任何参数的方法。Scala里可以省略方法调用的空括号。

##  数学运算
 - 可以通过中缀操作符，`+ - * / %`在任何数字类型上调用数学方法。

 - 数字类型还提供了一元前缀操作符`+ -`，即方法`unary_+`和`unary_-`。

##  关系和逻辑操作
 - 与Java一样，逻辑与和逻辑或都有短路的概念。

 - Scala中短路机制是因为Scala方法都有延迟对参数求值甚至是取消求值的机制。这个机制被称作by-name parameter。

##  位操作符

##  对象相等性
 - 相等性检测会处理null，它使用了一个简单的规则：首先检查左侧是否为null，如果不是，则调用equals方法。这种类型的比较对于不同的对象也会产生true，只要他们的内容相同并且它们的equals方法是基于内容编写的。

 - Scala与Java里`==`的区别。在Java里对于原始类型是直接比较值的相等性，与Scala一样。然而对于参考类型，Java是比较两个变量是否都指向JVM堆里的同一个对象。Scala也提供了这种机制，名字是eq。不过，eq和它的反义词ne，仅仅可以用于直接映射到Java的对象。

##  操作符优先级和关联性
 - 无论如何，使用括号都是好的风格。或许唯一不用查书就可以知道的优先级关系就是乘除法操作比加减法操作的优先级要高。

##  富包装器
 - Scala的基本类型上调用的方法多于之前所介绍的。很多方法是通过隐式转换（implicit conversion）来实现的。每个基本类型都有一个“富包装器”，要查看基本类型的所有方法时，还应该看下每个基本类型的富包装器的API文档。类名都是“Rich基本类型名”，位于scala.runtime包中。


#  函数式对象
 - 如果类没有主体，就不一定需要一对空括号。

 - 根据类参数Scala编译器会收集这类参数并创造一个带同样参数类型和数量的主构造器。

 - 不可变对象有可能因为要复制很大的对象图而产生性能瓶颈。有时会需要提供可变对象的版本。

 - 对象构造的先决条件，在主构造器中使用require函数来检查条件是否都满足，当它返回false时将抛出IllegalArgumentException来阻止对象被构造。

 - 在进行方法覆盖时override关键字是必须的。

 - 参数化对象的参数只可以在对象内部访问。在对象外部只能访问对象的属性。

 - this关键字指向当前执行方法被调用的对象实例，如果使用在构造器里就是指正被创建的对象实例。

 - Scala里主构造器之外的构造器称为从构造器。每个从构造器的第一个动作都是调用同一个类里其它的构造器。

 - Scala编译器将按字段在源码中出现的次序进行初始化。

 - 标识符的约定：构成标识符的有字母数字式和操作符。

  - 字母数字标识符起始于一个字母或下划线，之后可以跟字母、数字或下划线。‘$’字符也被当作字母，但是被保留作为编译器产生的标识符之用。Scala遵循Java驼峰式标识的习惯。不同的Java的在于常量命名，scala里constant并不同于val。Java常量命名通常都使用大写，Scala里常量命名习惯也是使用驼峰式风格。

  - 操作符是如：+、:、?、~或#的可打印ASCII字符。这些标识字符将在转换为以‘$’分隔的方法名称。

  - 混合标识符：由字母数字组成，后面跟前下划线和一个操作符标识符。如，unary_+被用于定义一元的‘+’操作符的方法名。myvar_=被用于定义赋值操作符的方法名。

  - 文本标识符：是用反引号`...`包含的任意字符串。例如yield是Scala保留字，如果我们要调用Java中Thread的静态方法yield就需要写作：Thread.`yield`()。

 - 隐式转换能在需要的时候自动把一种类型转换为另一种类型。隐匿转换要起作用需要定义在作用范围之内。它的转换是由编译器完成的，不会显式的出现在代码中。

#  内置控制结构

 - 几乎所有Scala的控制结构都会产生值。

 - Scala中所有赋值语句总是返回Unit。因此下面的代码将出问题：
```scala
var line = ""
while ((line = readLine()) != "") //不起作用
  println("Read: " = line)
```
 这里用!=比较Unit和String将永远为true。

 - for语句


  例1 :: 常见例
```scala
val filesHere = (new java.io.File(".")).listFiles
for (file <- filesHere)
  println(file)
```

 
  例2 :: 不常见用法
```scala
for(i <- 0 to filesHere.length - 1)
  println(filesHere(i))
```

  例3 :: to（包含上限）
```scala
for( i <- 1 to 4)
  println("Iteration " + i)
```

  例4 :: until（不含上限）
```scala
for( i <- 1 until 4)
  println("Iteration " + i)
```

  例5 :: 过滤
```scala
val filesHere = (new java.io.File(".")).listFiles
for (file <- filesHere if file.getName.endsWith(".scala"))
  println(file)
```

  例6 :: 多个过滤条件
```scala
val filesHere = (new java.io.File(".")).listFiles
for (
  file <- filesHere
  if file.isFile;
  if file.getName.endsWith(".scala")
) println(file)
```

  例7 :: 嵌套枚举（多层嵌套循环）
```scala
def fileLines(file: java.io.File) = 
  scala.io.Source.fromFile(file).getLines.toList

def grep(pattern: String) = 
  for {
    file <- filesHere
    if file.getName.endsWith(".scala")
    line <- fileLines(file)
    if line.trim.matches(pattern)
  } println(file + ": " + line.trim)
grep(".*gcd.*")
```

  例8 :: mid-stream变量绑定，代替上例中两次调用trim。变量作为val引入和使用，但不带关键字val。
```scala
def grep(pattern: String) = 
  for {
    file <- filesHere
    if file.getName.endsWith(".scala")
    line <- fileLines(file)
    trimmed = line.trim
    if trimmed.matches(pattern)
  } println(file + ": " + trimmed)
grep(".*gcd.*")
```

  例9 :: 使用yield创建新集合。格式`for {子名} yield {循环体}`
```scala
def scalaFiles = 
  for {
    file <- filesHere
    if file.getName.endsWith(".scala")
  } yield file
```
```scala
val forLineLengths = 
  for {
    file <- filesHere
    if file.getName.endsWith(".scala")
    line <- fileLines(file)
    trimmed = line.trim
    if trimmed.matches(".*for.*")
  } yield trimmed.length
```

 - 异常不需要申明在throws子名中。异常的catch子名中使用模式匹配来处理异常。try-catch-finally也可以产生值。应该避免在finally中返回值。

 - match表达式。

 - Scala中没有break和continue语句。

 - 变量作用范围与Java区别在于Java不允许你在内部范围内创建与外部范围变量同名的变量。

#  函数和闭包

 - 本地函数就像使用本地变量，它仅在包含它的代码块中可见。

 - 可以把函数写成函数文本（literal）并把它们像值（value）一样传递。函数文本被编译为类，类在运行期实例化的时候是一个函数值（function value）。

##  函数基础信息
完整的函数定义格式：
```scala
def max(x: Int, y: Int): Int = {
  if (x > Y)
    x
  else
    y
}
```

 - 有时函数定义会要求显示定义返回类型。比如函数是递归的。
 
 - 如果函数仅由一个句子组成，可以不写大括号。`def max2(x: Int, y: Int) = if (x>y) x else y`

 - 函数中可以定义函数，就像定义局部变量，称为本地函数。

##  函数文本
 - 函数文本基本格式：
```scala
(x: Int, y: Int) => x + y
```
 括号里是参数，右箭头右边是函数体。
   

 - 函数被编译成一个类，类在运行时是一个函数值：function value。

 - 函数文本（literal）也被编译为函数值，例`(x: Int) => x + 1`。函数文本中超过一个语句时，用大括号包住函数体。函数的返回值是最后一行的表达式的值。

##  函数文本短格式

 - 函数文本的短格式，例：
```scala
someNumbers.filter((x) => x>0)
```
 这里的someNumbers中的元素是整数类型的，因为类型推断系统可以得知x的类型，因此不需要说明x的类型。

 - 甚至可以进一步省去函数文本短格式中被推断的参数外的括号，如：
```scala
someNumbers.filter(x => x > 0)
```

##  占位符

 - 如果参数在函数文本内仅出现一次，则可以将参数省略为下划线。如：
```scala
someNumbers.filter(_>0)
```

 - 当将下划线作为占位符时，编译器可能没有足够的信息推断缺失的参数类型。这时需要指定参数类型，如：
```scala
var f=(_: Int) + (_:Int)
```
 注意这里的多个下划线是指代不同的参数，每个参数在函数文本中只出现一次的情况下才能使用这种格式。多个下划线按顺序代表第一个参数，第二个....

##  偏应用函数
 - 使用下划线代表全部或部分参数。
```scala
val a = sum _
a(1,2,3)

val b = sum(1,_: Int,3)
b(2)
```

 - 编译器根据这些信息产生一个新的函数类。新类的apply方法的参数个数和类型由占位符信息而决定。

 - 如果你写一个省略所有参数的偏应用程序表达式，而在代码的那个地方正需要一个函数，则你可以去掉下划线。
```scala
someNumbers.foreach(println _)
someNumbers.foreach(println)
```

##  闭包

 - 名称来源：通过“捕获”自由变量的绑定对函数文本执行的“关闭”动作。不带自由变量的函数文本：`(x: Int) => x + 1`被称为closed term（小段源码），这在严格意义上讲不是闭包，因为这个代码在编写的时候就已经封闭了。但任何带自由变量的函数文本，如`(x: Int) => x + more`都是open term。因此任何类似`(x: Int) => x + more`需要在运行时创建的函数必须捕获自由变量more的绑定。由于这个函数值是关闭`(x: Int) => x + more`这个open term的行动的最终产物，得到的函数值将包含一个指向捕获的more变量的参考，因此被称为闭包。

 - 如果more在闭包创建后改变了，闭包将看到这个变化。闭包对捕获变量的作出的改变在闭包外也可见。如果在闭包中修改了more，则more在闭包外也可见。Scala的闭包捕获了变量本身，而不是变量指向的值。
```scala
var more = 1
val addMore = (x: Int) => x + more
addMore(10) //11
more = 9999
addMore(10) //10009
```

 - 如果闭包访问了某些在程序运行时有若干不同备份的变量，例如，闭包使用了某个函数的本地变量，而这个函数又被调用了很多次。每次访问使用的将是闭包在被创建的时候活跃的变量。
```scala
def makeIncreaser(more: Int) = (x: Int) => x + more
val inc1 = makeIncreaser(1)
val inc9999 = makeIncreaser(9999)
inc1(10) //11
inc9999(10) //10009
```

 - 上例中Scala编译器重新安排了makeIncreaser的参数使得捕获的参数继续存在于堆中。

##  重复参数

 - 函数的最后一个参数可以是重复的，用于支持可变长度参数列表。通过在参数类型后放一个星号来标明。

 - 函数内部，重复参数的类型是声明参数类型的数组。但是你不能直接使用数组作为重复参数传入，这在编译时将出错。如果需要这样做，则要在调用时在数组参数后面添加一个冒号和一个_*符号。`echo(arr: _*)`

##  尾递归

 - Scala编译器检测到尾递归时将使用新值更新函数参数，然后把它替换成一个回到开头的跳转。（类似while，但更代码更优美和简明）

 - 由于JVM的约束，在两个函数间相间的进行递归调用将得到到优化。如果递归中的最后一个调用是函数值也不能获得优化。
```scala
def isEven(x: Int): Boolean =
  if (x == 0) true else isOdd(x - 1)
def isOdd(x: Int): Boolean = 
  if (x == 0) false else isEven(x - 1)

val funValue = nestedFun _
def nestedFun(x: Int){
 if (x !=0) { println(x); funValue(x - 1) }
}
```

#  控制抽象

##  减少重复代码
```scala
def filesMatching(query: String, 
    matcher: (String, String) => Boolean) = { 
  for (file <- filesHere; if matcher(file.getName, query)) 
    yield file 
}

def filesEnding(query: String) = 
  filesMatching(query, _.endsWith(_)) 
def filesContaining(query: String) = 
  filesMatching(query, _.contains(_)) 
def filesRegex(query: String) = 
  filesMatching(query, _.matches(_)) 
```

```scala
object FileMatcher { 
  private def filesHere = (new java.io.File(".")).listFiles 
  private def filesMatching(matcher: String => Boolean) = 
    for (file <- filesHere; if matcher(file.getName)) 
      yield file 
  def filesEnding(query: String) = 
    filesMatching(_.endsWith(query)) 
  def filesContaining(query: String) = 
    filesMatching(_.contains(query)) 
  def filesRegex(query: String) = 
    filesMatching(_.matches(query)) 
}
```

##  简化客户代码

##  Curry化
 - 通过Curry化我们可以创建“感觉像是原生语言支持”的控制抽象。

 原始的例子
```scala
def plainOldSum(x: Int, y: Int) = x + y
plainOldSum(1, 2) //3
```
 curry化后
```scala
def curriedSum(x: Int)(y: Int) = x + y
curriedSum(1)(2) //3
```
 这里实际相当于下面的调用过程：
```scala
def first(x: Int) = (y: Int) => x + y
val second = first(1)
second(2) //3
```

##  编写新的控制结构
 - 可以通过创建以函数作为参数的方法来定义新的控制结构。
```scala
def twice(op: Double => Double, x: Double) = op(op(x))
twice(_ + 1, 5) //7.0
```

 - 自定义控制结构版本1
```scala
def withPrintWriter(file: File, op: PrintWriter => Unit) { 
  val writer = new PrintWriter(file) 
  try { 
    op(writer) 
  } finally { 
    writer.close() 
  } 
}

withPrintWriter( 
  new File("date.txt"), 
  writer => writer.println(new java.util.Date) 
) 
```

 - 如果方法调用只传入一个参数，可以使用大括号替代小括号包围的参数。
```scala
println("Hello, world!")
println{"Hello, world!"}
```

 - withPrintWriter带两个参数，因此不能使用大括号。我们可以curry化第一个参数。
```scala
def withPrintWriter(file: File)(op: PrintWriter => Unit){
  val writer = new PrintWriter(file)
  try {
    op(writer)
  } finally {
    writer.close()
  }
}

val file = new File("date.txt")
withPrintWriter(file){
  writer => writer.println(new java.util.Date)
}
```

##  by-name参数

 - 使用by-name参数可以实现像if或while那样的控制结构。没有参数传入大括号之间的代码。

 原始的例子，需要使用参数
```scala
var assertionsEnabled = true
def myAssert(predicate: () => Boolean) = 
  if (assertionsEnabled && !predicate())
    throw new AssertionError

//使用它有点难看
myAssert(() => 5 > 3)
```

 使用by-name参数修改。by-name参数在定义参数类型的时候使用`=>`而不是`() =>`。
```scala
def byNameAssert(predicate: => Boolean) = 
  if(assertionsEnabled && !predicate)
    throw new AssertionError

//
byNameAssert(5 > 3)
```

 例3
```scala
def boolAssert(predicate: Boolean) = 
  if(assertionsEnabled && !predicate)
    throw new AssertionError
```
这个例子与byNameAssert存在重要的区别。由于boolAssert的参数是Boolean，括号中的表达式将先于boolAssert的调用被执行。当assertionEnabled为false时，boolAssert仍将产生副作用，而byNameAssert不会。

#  组合与继承

##  抽象类

 - 抽象成员的类本身必须被声明为抽象，抽象成员本身不需要添加abstract关键字。

##  定义无参数方法

 - 无参数方法在Scala中是非常普通的。带有空括号的方法定义，被称为空括号方法。推荐的习惯是在没有参数并且方法仅通过读含的方式访问可变状态（不改变可变状态）时，使用无参数方法。这个惯例支持统一访问原则，即客户代码不应受通过字段还是方法实现属性的决定的影响。

 - 下面两组不同的定义对于用户来讲并没有区别。区别在于方法调用可能要稍慢一些，而属性访问则在初始化的时候已经计算了。其重点在于Element类的客户不应在其内部实现发生改变的时候受影响。

 - Scala中可以使用空括号方法重载无参数方法，反之亦可。可以在调用任何不带参数的方法时省略空的括号。

 - 原则上Scala上的函数调用中可以省略所有空括号。但在调用的方法存在副作用时，推荐仍然写一对空括号。例如，方法执行了I/O，或写入了var变量，或读取了不属于接收参数内的var变量，直接或间接的使用了可变对象。这种情况下括号作为线索说明了这个调用触发了一些计算。

 - 总的来说，Scala里定义不带参数也没有副使用的方法为无参数方法，省略空的括号是鼓励的风格，另一方面不要定义没有括号的带副作用的方法，因为那样的话方法调用看上去会像选择一个字段，这样客户在看到副作用时会觉得奇怪。同样的，当你调用带副使用的函数时请添加上空括号。另一种考虑这个问题方法是：如果你调用的函数执行了操作就使用括号，如果仅提供了对某个属性的访问就省略括号。

##  扩展类

 - extends子句有两个效果：使子类从父类继承所有非私有的成员，使子类成为父类的子类型。

 - 如果忽略extends子句，Scala编译器隐式的假设你的类从scala.AnyRef继承。

##  重载方法和字段

 - Scala中字段和方法属于相同的命名空间。这使得字段重载无参数方法成为可能。

 - Scala里禁止在同一个类里有同样的名称定义字段和方法。而在Java中方法名可以与字段同名。

 - Scala仅为定义准备了两个命名空间（值（字段、方法、包、单例对象）、类型（类、特质）），而Java有四个（字段、方法、类型、包）。

##  定义参数化字段

 - 在定义中组合参数和字段避免同时编写参数和赋值。

##  调用超类构造器

 - 在定义子类时，直接将父类的构造器的参数放在父类名后面的括号里。

##  使用override修饰符

 - Scala里所有重载了父类具体成员的成员都需要这个修饰符。

 - 编译器根据这个信息，可以避免不安全的方法覆盖。

##  多态和动态绑定

##  定义final成员

 - 当要确保成员不被子类重载时，使用final修饰符。
 - 要确保类不被重载时，在类上使用final修饰符。

##  使用组合与继承

##  实现above，beside和toString
 - Scala里的数组表示为Java数组，但支持更多的方法。特别是Scala里的数组继承自类scala.Seq，能够表现象序列这样的结构并包含许多访问的转换序列的方法。
 - zip操作符可以将两个参数变成Tuple2。
```scala
scala> Array(1,2,3) zip Array("a","b")
res1: Array[(Int, java.lang.String)] = Array((1,a), (2,b))
```
 从上面可以看出如果两个操作数组的其中一个比另一个长，zip将舍弃余下的元素。
 - for循环中将this.contents和that.contents两个数组的元素zip到line1和line2，然后使用for表达式的yield部分来产生结果。结果类型的枚举遍历的表达式类型一致。
```scala
scala> for((line1,line2) <- Array(1,2,3) zip Array("a","b")) yield line1+line2
res0: Array[java.lang.String] = Array(1a, 2b)
```
 - 序列中定义了mkString方法，它能返回序列中所有元素组成的字符串。
```scala
scala> Array(1,2,3) mkString "\n"
res4: String =
1
2
3
```

##  定义工厂对象
 - 可以在基类的伴生对象中定义多个工厂方法来产生不同子类型的对象。
```scala
object Element {
  def elem(contents: Array[String]): Element = new ArrayElements(contents)
  def elem(chr: Char, width: Int, height: Int): Element = new UniformElement(chr, width, height)
  def elem(line: String): Element = new LineElement(line)
}
```
 - 伴生类里可以直接调用伴生对象中的方法，可以缩短代码。
```scala
import Element.elem 
abstract class Element { 
def contents: Array[String] 
def width: Int = 
if (height == 0) 0 else contents(0).length 
def height: Int = contents.length 
def above(that: Element): Element = 
elem(this.contents ++ that.contents) 
def beside(that: Element): Element = 
elem( 
for ( 
(line1, line2) <- this.contents zip that.contents 
) yield line1 + line2 
) 
override def toString = contents mkString "\n" 
} 
```
 - 使用工厂方法后，使得子类型可以是私有的。
```scala
object Element {
   private class ArrayElement( 
    val contents: Array[String] 
  ) extends Element 
  private class LineElement(s: String) extends Element { 
    val contents = Array(s) 
    override def width = s.length 
    override def height = 1 
  } 
  private class UniformElement( 
    ch: Char, 
    override val width: Int, 
    override val height: Int 
  ) extends Element { 
    private val line = ch.toString * width 
    def contents = Array.make(height, line) 
  } 

  def elem(contents: Array[String]): Element = new ArrayElements(contents)
  def elem(chr: Char, width: Int, height: Int): Element = new UniformElement(chr, width, height)
  def elem(line: String): Element = new LineElement(line)
}
```

#  Scala的类层级
　-　每个类都继承自Any类。Scala还在类层级的底端定义了Null和Nothing，主要都扮演通用的子类。Nothing是所有类的子类。

##  Scala类层级
　-　Any中定义了`==,!=,equals`，还有`hashCode`和`toString`。Any中的`==,!=`方法，被声明为final，因此它们不能在子类里重载。实际上`==`总与equals相同，`!=`总是于equals相反。
　-　Any有两个子类：AnyVal和AnyRef。
　-　AnyVal是九个内建值类（Byte、Short、Char、Int、Long、Float、Double、Boolean、Unit）的父类。内建值类除Unit外，其它的都对应于Java原始类型。Scala里这些类的实例都写成文本。不能用new创建这些类的实例，因为这些值类都被定义成既是抽象的又是final的。Unit大约对应于Java中的void；被用途不返回任何有效结果的方法的结果类型。Unit只有一个实例值，写作()。所有值类都是scala.AnyVal的子类型，它们之间互相没有继承关系。值类之间可以进行隐式转换。隐匿转换还为值类增加了功能，如min,max,until,to和abs都是定义在类scala.runtime.RichInt里的，并且有一个从类Int到RichInt的隐式转换。
 - AnyRef是Scala里所有引用类的基类。在Java里AnyRef实际上就是类java.lang.Object的别名。Scala类与Java类不同在于它们还继承自ScalaObject物特别的标记特质。ScalaObject包含了scala编译器定义和实现的方法，作用是让Scala程序执行更有效。到现在为止，ScalaObject只包含了单个方法`$tag`，用于内部以提高模式匹配的速度。

##  原生类型是如何实现的
 - 当数据需要被当作对象看侍时，Scala使用对象类型，如java.lang.Integer。它与Java5的自动装箱机制差异在于Scala里的装箱比Java里的更少见。
 - AnyRef类型定义了eq方法，它不能被重载且实现为对比对象的引用（类似Java里的`==`）。它的反义方法为ne。
 - Scala中的`==`被设计为透明的参考类型代表的东西。对值类型来说，就是自然（数学或自然）相等。对引用类型，`==`被视为继承自Object的equals方法的别名。这个方法被初始地定义为引用相等，但被许多子类重载实现它们的相等概念。

##  底层类型
 - scala.Null和scala.Nothing是用于统一方式处理某些“边界情况”的特殊类型。
 - Null是null类型的引用；它是每个引用类的子类。Null不能赋值给值类型。
 - Nothing是Scala类层级中最底端；它是任何类型的子类型。没有这个类型的值。Nothing的一个用处是标明不正常的终止。例如：
```scala
def error(message:String): Nothing = throw new RuntimeException(message) 
def divide(x:Int, y:Int): Int = 
  if(y != 0) x / y 
  else error("can't divide by zero") 
```

#  特质
 - 物质是Scala中代码复用的基础单元。特质封装了方法和字段定义，并且可以通过混入到类中重用它们。类可以混入任意个特质。

##  特质如何工作
 - 特质的定义使用关键字trait，其它与类定义无异。
 - 特质与类一样会有默认超类AnyRef。
 - 可以使用extends或with关键字把特质混入到类中。Scala“混入”特质而不是继承，特质的混入与其它语言中的多继承有重要的差别。
 - 使用extends关键字混入特质时，隐式地继承了特质的超类。例如下例中，Frog是AnyRef（Philosophical的超类）的子类并混入了Philosophical。从特质继承的方法可以像从超类继承的方法那样使用。
```scala
class Frog extends Philosophical {
  override def toString = "green"
}
```
 - 如果想把特质混入到扩展自超类的类里，可以用extends指明父类，用with混入特质。
```scala
class Animal 
trait HasLegs 
class Frog extends Animal with Philosophical with HasLegs { 
  override def toString = "green" 
} 
```
 - 特质就像是带有具体方法的Java接口，不过它可以做得更多。比如，它可以声明字段和维持状态值。实际上，可以用特质定义任何用类定义做的事，并且语法也一样，除了两点：第一，特质不能有任何“类”参数，也就是说传递给类的主构造器的参数。另一个差别在于不论在类的哪个角落，super调用都是静态绑定的，在特质中，它们是动态绑定的。调用的实现将在每一次特质被混入到具体类的时候才被决定。这种处理super的行为使得特质能以可堆叠的改变方式：stackable modifications工作。

##  瘦接口对阵胖接口
 - 要使用特质丰满接口，只要简单地定义一个具有少量抽象方法的特质——特质接口的瘦部分——和潜在的大量具体方法，所有的都实现在抽象方法上。然后你就可以把丰满了的特质混入到类中，实现接口的瘦部分，并最终得到具有全部胖接口内容的类。

##  特质用来做可堆叠的改变
下面部分用FreeMind写的
[[scala-tip/Programming In Scala.png]]

#  Case Class和模式匹配

Case Class是Scala中用于匹配对象的一种方法。通常情况下只要在需要使用模式匹配的类的class关键字前添加case关键字就可以了。

##  Case Class的例子
```scala
abstract class Expr
case class Var(name: String) extends Expr
case class Number(num: Double) extends Expr
case class UnOp(operator: String, arg: Expr) extends Expr
case class BinOp(operator: String, left: Expr, right: Expr) extends Expr
```
从上例也可以看出Scala中class定义时类体部分可以为空。

###  Case classes
每个Expr的子类都有一个case修饰符。有这个修饰符的类被称为Case class。使用这个修饰符后Scala编译器将会为这个类添加特殊的语法效果。

首先，它会给这个类添加一个工厂方法。比如使用Var("x")来构造对象而不需要new Var("x")。这个工厂方法在嵌套使用这个类时更显方便。
```scala
val op = BinOp("+", Number(1), v)
```

第二个语法效果是所有参数列表中的参数被隐式的添加了val前缀，因此它们被当作了类的字段。

第三，编译器将为Case class添加toString，hashCode和equals方法。它们可用于打印，计算hash值或递归的按对象结构中的字段进行对比。由于Scala中==总是会使用equals，这意味case class中的元素也将会按结构进行对比。
```scala
scala>println(op)
BinOp(+,Number(1.0),Var(x))
scala>op.right== Var("x")
res3:Boolean=true
```

###  模式匹配
Case class的另一个好处是支持模式匹配。例如要实现下面的规则：
```scala
UnOp("-", UnOp("-", e))=> e //Doublenegation
BinOp("+", e, Number(0))=> e //Addingzero
BinOp("*", e, Number(1))=> e //Multiplyingbyone
```
使用模式匹配来实现这些规则：
```scala
scala>simplifyTop(UnOp("-", UnOp("-", Var("x"))))
res4:Expr=Var(x)
def simplifyTop(expr: Expr): Expr =expr match {
  case UnOp("-", UnOp("-",e))=>e //Doublenegation
  case BinOp("+",e, Number(0))=>e //Addingzero
  case BinOp("*",e, Number(1))=>e //Multiplyingbyone
  case _=>expr
}
```
上例中的simplifyTop包含匹配表达式。匹配表达类似于Java中的switch，但它通常出现在selector表达式的后面：
```scala
selector match { alternatives }
```
而不是
```scala
switch (selector) { alternatives }
```
模式匹配包含于一个alternatives序列中，每个匹配都以关键字case开头。每个alternative包含了一个模式和一个以上的表达式，它将在匹配时被执行。箭头符号=>将模式和表达式分开。

匹配表达式将按模式匹配的书写顺序执行。当=>左边的模式匹配上时，=>右边的表达式将被执行。

常量匹配比如"+"或1的匹配与使用==是等效的。类似e这样的变量匹配将匹配所的值。然后变量指向case语句右边的值。在这个例子中，前三个例子中，在匹配范围内，e变量都绑定到了变量上。通配符匹配s模式（_）也匹配所有值，但它不会绑定变量值。在例中的最后是默认匹配，它只是返回expr，不对表达式做任何操作。

构造器模式如UnOp("-",e)。这个模式匹配所有第一个参数匹配"-"第二个参数匹配e且类型为UnOp的值。构造器的参数自身也是匹配模式。这允许我们使用简单的标记写出深度匹配。例如：
```scala
UnOp("-", UnOp("-",e))
```

####  模式匹配与switch的比较
匹配表达式可以被看作Java风格的switch。Java风格的switch可以很自然的用匹配表达式来表示，每个模式都是常量最后的模式可以是一个通配符（它用于表示switch中的default）。switch与模式匹配有三处不同：

 - Scala中的匹配是表达式，它总会产生一个值

 - Scala的alternative表达式不会“fall through”到下一个匹配情况（不需要break）。

 - 如果没有任何模式匹配，将会抛出MatchError异常。这意味着你总会需要有一个默认的匹配，即使它什么也不做。
```scala
expr match {
case BinOp(op,left,right)=>
  println(expr+"isabinaryoperation")
case _=>
}
```
这个例子中的第二种情况没有代码，因此它不会执行任何操作。这个例子中的两种情况都会返回空值‘()’，这也是整个匹配表达式的结果。

##  模式类型

###  通配符匹配模式
通配符模式（_）匹配所有对象。常用于作为默认值，捕获所有的情况，例如：
```scala
expr match {
  case BinOp(op,left,right)=>
    println(expr+"isabinaryoperation")
  case _=>
}
```
通配符也可用于忽略对象的某些部分。比如，在前面的例子中并不需要关心BinOp的元素。只需要检查它是不是BinOp。因此可以使用通配符匹配：
```scala
expr match {
  case BinOp(_,_,_)=>println(expr+"isabinaryoperation")
  case _=>println("It'ssomethingelse")
}
```

###  常量匹配模式
常量模式只匹配自身。任何字面量（literal）都可以用于常量模式。比如，5，true和"hello"都是常量模式。任何val或singleton对象也可以用作常量模式。比如，Nil是一个singleton对象，它可以用于匹配空列表（empty list）：
```scala
def describe(x: Any)=x match {
  case 5 => "five"
  casetrue => "truth"
  case "hello" => "hi!"
  case Nil => "theemptylist"
  case _=> "somethingelse"
}

scala>describe(5)
res5:java.lang.String=five

scala>describe(true)
res6:java.lang.String=truth

scala>describe("hello")
res7:java.lang.String=hi!

scala>describe(Nil)
res8:java.lang.String=theemptylist

scala>describe(List(1,2,3))
res9:java.lang.String=somethingelse

```

###  变量匹配模式
变量模式匹配任何对象，与通配符模式类似。与通配符不同之处在于，Scala将会绑定对象到变量。你可以在后面使用这个变量来操作匹配的对象。比如下例：
```scala
expr match {
  case 0 => "zero"
  case somethingElse=> "notzero:"+somethingElse
}
```

变量还是常量？

常量模式可以有符号名称。比如前面以经看到的使用Nil作为模式。下例中，模式匹配常量E(2.71828...)和Pi(3.14159...)。
```scala
scala> import Math.{E, Pi}
importMath.{E,Pi}
scala>E match {
	case Pi => "strange math? Pi = "+ Pi
	case _=> "OK"
}

res10:java.lang.String=OK
```
E不会匹配Pi，因此“strange math"的情况不会发生。

Scala编译器如何知道Pi是从java.lang.Math对象中导入的常量，而不是一个变量呢？Scala使用了一个简单的规则来区分：以小写字母开头的名称将作为模式变量；其它情况将作为常量。上例如果改为小写的pi将出现不同的情况：
```scala
scala> val pi= Math.Pi
pi:Double=3.141592653589793

scala>E match {
        case pi=> "strangemath?Pi="+pi
}

res11:java.lang.String=strangemath?Pi=2.7182818...
```
这种情况下编译器将不会允许你添加default case。因为pi是变量模式，它将匹配所有输入，因此它后面的情况将不可达：
```scala
scala>E match {
	case pi=> "strangemath?Pi="+pi
	case _=> "OK"
}
<console>:9:error:unreachablecode
	case_=>"OK"
```
如有必要通过使用两个反单引号（~上的那个）你仍然可以使用小写的名称作为常量模式。比如常量是某些对象的字段时。例如，pi是一个变量模式，但是this.pi或obj.pi是常量。我们可以使用反单引号解决这个问题，通过使用`pi`，pi将被作为常量模式，而不是变量模式：
```scala
scala>E match {
      case `pi`=> "strangemath?Pi="+pi
      case _=> "OK"
}

res13:java.lang.String=OK
```
反单引号在Scala中被用于两种不同目的。前面已经介绍过使用它可以将关键字作为普通的标识符。比如`yield`()会将yield作为标识符而不是关键字。

###  构造器匹配模式
构造器匹配模式使得模式匹配变得真正强大。例如“BinOp("+", e, Number(0))”。这个匹配选检查Case class的名称是否为BinOp然后检查它的构造器参数是否匹配额外的模式。

这些额外的模式意味着Scala的模式支持深度匹配。这些模式不只是检查最顶级的对象，也检查这个对象的内容是否匹配额外的模式。由于这些额外的模式也可以是构造器模式，你可以使用它检查任意深度的对象。比如上面提到的例子先检查顶层的对象是否为BinOp，它的第三个构造器参数是否为Number，value字段是否为数字0。这个模式在一行中检查了三级深度的数据。

###  序列匹配模式
可以像匹配case class那样使用序列匹配模式来匹配List或Array这样的序列类型。使用的是同样的语法，但你可以在模式中指定任意数量的元素。比如，下例显示了如何匹配以0开头的含有3个元素的list：
```scala
expr match {
  case List(0,_,_)=>println("foundit")
  case _=>
}
```
如果需要匹配不指定长度的序列模式，可以在模式的最后一个元素使用`_*`。这个模式匹配序列中任意数量的元素，包括0个元素。下例将匹配任何以0开头的list，不管list有多长。
```scala
expr match {
  case List(0,_*)=>println("foundit")
  case _=>
}
```

###  元组匹配模式
也可以匹配元组。例如(a,b,c)匹配任意3元素的元组。
```scala
def tupleDemo(expr: Any)=
  expr match {
    case (a,b,c)=>println("matched"+a+b+c)
    case _=>
}
```

###  类型匹配模式
可以使用类型匹配模式来代替类型测试和类型转换。例如：
```scala
def generalSize(x: Any)=x match {
  case s: String =>s.length
  case m: Map[_,_] =>m.size
  case _=>-1
}
```
下面是使用generalSize的例子：
```scala
scala>generalSize("abc")
res14:Int=3

scala>generalSize(Map(1 -> 'a', 2 -> 'b'))
res15:Int=2

scala>generalSize(Math.Pi)
res16:Int=-1
```
在这里要注意，尽管s和x指的是同一个值，x的类型是Any，但是s的类型是具体类型。因此在调用具体类型的方法时不能直接使用x.method，而是要使用s.method。

如果不使用模式匹配，Scala中使用了不同于Java的方式进行进行类型测试和类型转换。例如测试expr是否为String：
```scala
expr.isInstanceOf[String]
```
将expr转换为String，使用：
```scala
expr.asInstanceOf[String]
```

操作符isInstanceOf和asInstanceOf是作为Any类的预定义函数，它们在方括号中接收一个类型参数。实际上，x.asInstanceOf[String]是参数String的隐式类型参数的方法调用的一个特殊情况。

从这里可以看出在Scala中进行类型测试和类型转换更繁锁。
```scala
if (x.isInstanceOf[String]){
  val s=x.asInstanceOf[String]
  s.length
} else ...
```

第二种类型匹配模式：“m: Map[_, _]”。这个匹配模式匹配任意Map类型的值，这个Map的key和value可以是任意类型的，m指向这个Map。因此，m.size将返回map的size。下划线与其它匹配模式中一样。

###  类型擦除
能测试Map元素的类型吗？例如测试map的key和value是否都为Int：
```scala
scala> def isIntIntMap(x: Any)=x match {
	 case m: Map[Int,Int] => true
	 case _=> false
}
warning:therewereuncheckedwarnings;re-runwith
   -uncheckedfordetails
isIntIntMap:(Any)Boolean
```
解释器给出了“unchecked warning.”。可以在启动解释器时添加-unchecked参数来了解详细信息：
```scala
scala>:quit
$scala-unchecked
WelcometoScalaversion2.7.2
(JavaHotSpot(TM)ClientVM,Java1.5.0_13).
Typeinexpressionstohavethemevaluated.
Type:helpformoreinformation.
scala> def isIntIntMap(x: Any)=x match {
	 case m: Map[Int,Int] => true
	 case _=> false
       }
<console>:5:warning:non variable type-argument Int in
type pattern is unchecked since it is eliminated by erasure
case m:Map[Int,Int]=>true
       ^
```
与Java泛型类型Scala使用了擦除模式。这意味着在运行时不会维护类型参数。因此，没有办法在运行时决定map对象在构建时是否使用了两个Int类型参数。系统可以做的只是检查值是否匹配带任意类型参数的Map。可以使用不同类型的参数调用isIntIntMap来验证这个问题：
```scala
scala>isIntIntMap(Map(1 -> 1))
res17:Boolean=true

scala>isIntIntMap(Map("abc" -> "abc"))
res18:Boolean=true
```

唯一的例外是数组，因为与Java中一样Scala对数组作了特殊处理。数组元素的类型被保存在数组中，因此可以进行模式匹配。例如：
```scala
scala> def isStringArray(x: Any)=x match {
	  case a: Array[String] => "yes"
	  case _=> "no"
       }
isStringArray:(Any)java.lang.String

scala> val as= Array("abc")
as:Array[java.lang.String]=Array(abc)

scala>isStringArray(as)
res19:java.lang.String=yes

scala> val ai= Array(1, 2, 3)
ai:Array[Int]=Array(1,2,3)

scala>isStringArray(ai)
res20:java.lang.String=no
```

###  变量绑定
对于变量匹配模式，你可以向任何匹配模式添加变量。只需要在匹配模式前添加@符号。这将会将匹配成功的变量绑定到变量上。
```scala
expr match {
  case UnOp("abs",e@ UnOp("abs",_))=>e
  case _=>
}
```
变量e被绑定到`UnOp("abs", _)`这个匹配模式上。如果整个模式匹配成功，则整个匹配的`UnOp("abs", _)`部分将被作为变量e。

###  Pattern guard
有些情况下，句法上的匹配并不够精确。比如，给你一个任务将
```scala
BinOp("+", Var("x"), Var("x"))
```
转换为
```scala
BinOp("*", Var("x"), Number(2))
```
你可能会写成
```scala
scala> def simplifyAdd(e: Expr)=e match {
	 case BinOp("+",x,x)=> BinOp("*",x, Number(2))
	 case _=>e
       }
<console>:10:error:x is already defined as value x
         caseBinOp("+",x,x)=>BinOp("*",x,Number(2))
```
这将会失败，因为Scala约束了模式匹配为线性的：模式变量在同一个匹配模式中只允许出现一次。但，你可以使用pattern guard重写为：
```scala
scala> def simplifyAdd(e: Expr)=e match {
	 case BinOp("+",x,y) if x==y=>
	   BinOp("*",x, Number(2))
	 case _=>e
       }
simplifyAdd:(Expr)Expr
```
Pattern guard是在匹配模式后添加if。Guard可以是任意类型的boolean表达式，它通常会引用模式变量。如果pattern guard存在，则匹配只在guard的if条件满足时才会成功。使用pattern guard的例子：
```scala
//match only positive integers
case n: Int if 0 <n=>...

//match only strings starting with the letter 'a'
case s: String if s(0)== 'a' =>...
```

##  匹配模式重叠
匹配模式将按书写次序依次尝试。例如：
```scala
def simplifyAll(expr: Expr): Expr =expr match {
  case UnOp("-", UnOp("-",e))=>
    simplifyAll(e) //‘-’isitsowninverse
  case BinOp("+",e, Number(0))=>
    simplifyAll(e) //‘0’isaneutralelementfor‘+’
  case BinOp("*",e, Number(1))=>
    simplifyAll(e) //‘1’isaneutralelementfor‘*’
  case UnOp(op,e)=>
    UnOp(op,simplifyAll(e))
  case BinOp(op,l,r)=>
    BinOp(op,simplifyAll(l),simplifyAll(r))
  case _=>expr
}
```
这个版本的simplify会将规则应用到表达式的任何位置，不管它是否是顶层对象。在这个例子中要注意catch-all的情况应该放在最后。否则下面的匹配模式将不可达，编译时将出现unreachable code错误。

##  Sealed classes
在编写模式匹配时，必要要保证能覆盖所有可能的情况。有些时候我们可以末尾处添加默认情况的匹配，但这只在存在合理的默认匹配的情况下才适合。如果没有默认匹配？你还会认为你安全的覆盖了所有可能的情况吗？

实际上，你可以从Scala编译器来获得支持来检测缺失的匹配模式。为了达到这个目的，编译器需要知道会有哪些可能的匹配。通常情况下这在Scala中是不可能的，因为我们可以任意的定义新的case class。比如，我们可以一个编译单元中在Expr的类继承结构中随意的定义5个case class，而在另一个编译单元中只定义4个。

可取的方法是使case class的超类为sealed class。Sealed class不允许在定义sealed class的文件之外定义新的子类。这对于使用模式匹配是非常重要的，因为这意味着你不需要考虑子类的问题，因为所有的子类类型你都已经知道了。sealed关键字通常用于模式匹配。

```scala
sealed abstract class Expr
case class Var(name: String) extends Expr
case class Number(num: Double) extends Expr
case class UnOp(operator: String,arg: Expr) extends Expr
case class BinOp(operator: String,
    left: Expr,right: Expr) extends Expr
```
现在定义模式匹配
```scala
def describe(e: Expr): String =e match {
  case Number(_)=> "anumber"
  case Var(_)=> "avariable"
}
```
在编译时Scala将检查缺失的匹配情况并给出警告信息。
```scala
warning: match is not exhaustive!
missing combination UnOp
missing combination BinOp
```

有时我们可能会遇到编译器发邮过多的这种警告。例于，你可以确保在某个环境下某些情况不可能会发生。我们能确保不会发生MatchError。为了避免出现这些警告，我们可以添加catch-all case：
```scala
def describe(e: Expr): String = e match {
case Number(_)=> "anumber"
  case Var(_)=> "avariable"
  case _=> throw new RuntimeException //Shouldnothappen
}
```

这种修改方式能工作，但未必是你所满意的，因为你被迫添加了不可能被执行的代码，我们也可以直接让编译器闭嘴。

即在模式匹配的selector上添加@unchecked注释：
```scala
def describe(e: Expr): String =(e:@unchecked) match {
  case Number(_)=> "anumber"
  case Var(_)=> "avariable"
}
```
通常你可以使用给添加注释的方式给selector表达式添加注释：在表达式后面加上冒号和注释。如上面的e:@unchecked。@unchecked对于模式匹配有特殊含义。如果selector表达式带有这个注释，则编译器将不会检查匹配模式是否覆盖所有可能。

##  Option
对于可选值Scala有一个标准类型Option。它的值只有两种情况。一种为Some(x)，x是实际的值。另一种为None对象，它表示没有值。

在对Scala的集合类型的一些操作会生成可选值。比如，Scala的Map的get方法将在key对应的值存在时将生成Some(value)，如果key对应的值不存在则返回None。例：
```scala
scala> val capitals=
         Map("France" -> "Paris", "Japan" -> "Tokyo")
capitals:
  scala.collection.immutable.Map[java.lang.String,
  java.lang.String]=Map(France->Paris,Japan->Tokyo)

scala>capitalsget "France"
res21:Option[java.lang.String]=Some(Paris)

scala>capitalsget "NorthPole"
res22:Option[java.lang.String]=None
```
最常见的获取可选值的方式是使用模式匹配。例如：
```scala
scala> def show(x: Option[String])=x match {
	 case Some(s)=>s
	 case None => "?"
       }
show:(Option[String])String

scala>show(capitalsget "Japan")
res23:String=Tokyo

scala>show(capitalsget "France")
res24:String=Paris

scala>show(capitalsget "NorthPole")
res25:String=?
```
Option类型在Scala程序中很常见。比较它与Java中使用null标识没有值。例如，java.util.HashMap的get方法将返回存储于HashMap中的值，在未找到值是返回null。这种方式使得HashMap中不能保存null值。如果某个变量允许为null，则你总是需要在使用它时检查它是否为null。如果你忘记检查就可能在运行时产生NullPointerException。由于这种异常并不是总会发生，因此难于发现和调试。而对于Scala而言则不会发生这种情况，因为它允许在hash map上存储值的类型，而null不是合法的类型。例如，HashMap[Int, Int]不能返回null来表示“没有这个元素”。

Scala鼓励使用Option来标识可选值。这与Java中直接使用类型有很多好处。首先，增加了可读性，Option[String]标明了变量可能为null的字符串。更重要的是，使用未检查的空值变量在Scala中变成了类型错误。如果将类型为Option[String]的变量用于String则编译将不能通过。

##  无处不在的匹配模式
匹配模式被用于Scala中的很多地方，而不仅仅是用于匹配表达式。

###  模式用于变量定义
当定义val或var时，你可以使用模式来代替标识符。例如，你可以使用下面的例子来提取元组中的数据，将元组的不同部分赋给不同的变量：
```scala
scala> val myTuple=(123, "abc")
myTuple:(Int,java.lang.String)=(123,abc)

scala> val (number,string)=myTuple
number:Int=123
string:java.lang.String=abc
```

在使用case class时，如果你明确的了解这个case class，则你可以使用模式来析构对象。例如：
```scala
scala> val exp= new BinOp("*", Number(5), Number(1))
exp:BinOp=BinOp(*,Number(5.0),Number(1.0))

scala> val BinOp(op,left,right)=exp
op:String= *
left:Expr=Number(5.0)
right:Expr=Number(1.0)
```

###  Case序列作为偏应用函数
大括号中的case序列可以用于任何允许使用function literal的地方。与只有一个入口点和参数列表的函数不同，case序列可以有多个入口，每个入口有自己的参数列表。每个case都有进入函数的入口，参数由模式来指定。函数在每个入口点case的右边。

例如：
```scala
val withDefault: Option[Int] => Int ={
  case Some(x)=>x
  case None => 0
}
```
这个函数休有两个case。第一个匹配Some，并返回Some内部的数值。第二个case匹配None，返回数值0。下面是使用这个函数的例子：
```scala
scala>withDefault(Some(10))
res25:Int=10

scala>withDefault(None)
res26:Int=0
```
这种机制对于actor库非常有用。下面是一些典型的actor的代码。它传递模式匹配到react方法中：
```scala
react{
  case (name: String,actor: Actor)=>{
    actor!getip(name)
    act()
  }
  case msg=>{
    println("Unhandledmessage:"+msg)
    act()
  }
}
```
Case序列的另一个应用是偏应用函数（partial function）。如果你将这个函数应用到一个值它将产生运行时错误。例如，下面是一个返回list中第二个元素中的整数的偏应用函数：
```scala
val second: List[Int] => Int ={
  case x::y::_=>y
}
```
当编译时这个函数时，编译器将产生下面的警告：
```scala
 <console>:17: warning: match is not exhaustive!
 missing combination Nil
```
如果传递空的list给它，它将产生错误：
```scala
scala>second(List(5,6,7))
res24:Int=6

scala>second(List())
scala.MatchError:List()
      at$anonfun$1.apply(<console>:17)
      at$anonfun$1.apply(<console>:17)
```
如果你需要检查某个偏应用函数是否定义，你必须先告诉编译器你需要使用偏应用函数。类型说明`List[Int] => Int`包含了整型List的所有函数，无论它是否是偏应用函数。只包含整型List的所有偏应用函数应该写作`PartialFunction[List[Int],Int]`。下面是新编写的函数：
```scala
val second: PartialFunction[List[Int],Int] = {
  case x :: y :: _ => y
}
```
可以使用偏应用函数的isDefinedAt测试是否定义了函数。在这里，可以测试到接收两个以上元素的List作为参数的second函数被定义了，而接收空List的second函数不存在：
```scala
scala>second.isDefinedAt(List(5,6,7))
res27:Boolean=true

scala>second.isDefinedAt(List())
res28:Boolean=false
```
实际上，上面的表达式被Scala编译器编译为偏应用函数是通过将模式进行了两次转换——一次是为了实现匹配函数，另一次是实现`isDefinedAt`函数。例如，`{case x :: y :: _ => y}`将被翻译为下面的偏应用函数：
```scala
new PartialFunction[List[Int],Int]{
  def apply(xs: List[Int]) = xs match {
    case x :: y :: _ => y
  }
  def isDefinedAt(xs: List[Int]) = xs match {
    case x :: y :: _ => true
    case _ => false
  }
}
```
当function literal被申明为PartialFunction时这个转换就产生。如果申明的类型为Function1，或未申明则将被转换为完整的函数。

通常，如果可能应该尽可能的使用完整的函数，因为使用偏应用函数时允许运行时错误，编译器无法给予帮助。尽管如此，但在有些时候偏应用函数确实有用。你可能确保不提供未被处理的值。其中一个办法是可以使用检查偏应用函数的框架，总是在调用函数前使用isDefinedAt进行检查。例如，上面的react中，参数是一个偏应用，它精确定义了调用都要处理的消息。

###  for表达式中的匹配模式
你也可以在for表达式中使用模式匹配。下例中的表达式遍历capitals map中的键/值对。每个键值对匹配(country, city)模式，这将会定义两个变量country和city。

键值对匹配模式在匹配时是一种特殊的模式，它永远不会失败。capitals是map它的的键值对总会匹配键值对模式。
```scala
scala> for ((country,city)<-capitals)
         println("The capital of"+country+"is"+city)
The capital of Franceis Paris
The capital of Japanis Tokyo
```

但是生成的数据也有可能不能匹配。例如下面的情况：
```scala
scala> val results= List(Some("apple"), None,
           Some("orange"))
results:List[Option[java.lang.String]]=List(Some(apple),
     None,Some(orange))
scala> for (Some(fruit)<-results)println(fruit)
apple
orange
```
这个例子中None元素不会匹配Some(fruit)，因此它不会显示出来。

##  一个大型的示例
