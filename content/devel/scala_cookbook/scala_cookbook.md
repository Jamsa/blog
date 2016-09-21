Title: Scala Cookbook 笔记
Date: 2015-05-21
Modified: 2015-05-21
Category: java
Tags: scala

# Scala Cookbook 笔记
## String
### 简介
Scala String 是 Java String，可以使用 Java 中 String 对象的方法。由于 Scala 提供了隐式转换，因此 String（即使它是 final 的） 实例也可以使用 StringOps 类中的所有方法，因此你可以将字符串实例当作字符序列。对它使用 foreach 或使用 for 循环。字符串的另一些功能来自于 StringLike 和 WrappedString 等类。String 类至 StringOps 的隐式转换源于 Predef 对象。
```scala
"hello".getClass.getName
"hello".foreach(println)
for(c <- "hello") println(c)
"hello".filter(_ != 'l')
```
Scala String 同时拥有字符串和集合特性。
```scala
"scala".drop(2).take(2).capitalize
```
### 相等性
Scala 中直接使用 `==` 比较字符串。这个操作不会在对象为 `null` 时抛出空指针异常。如果在比较时要忽略大小写，则可以将要比较的字符串都转换为大写或小写。在 `null` 上调用大小写转换方法时是会产生空指针异常的。也可以直接使用 Java String 的`equalsIgnoreCase`。
```scala
val s3 = "hello"
val s4: String = null
s3 == s4
s4 == s3 //不产生异常
```
Scala 中使用`==`比较对象相等性，而不是使用`equals`方法。`==`定义在 AnyRef 中，它会先检查是否为 null，然后再调用`equal`方法。

### 多行字符串
```scala
val foo = """This is
a multiline
String"""
```
多行字符串的对齐
```scala
//默认按|对齐
val speech = """Four score and
|seven years ago""".stripMargin

val speech = """Four score and
#seven years ago""".stripMargin('#')

//多行转单行
val speech = """Four score and
#seven years ago""".stripMargin('#').replaceAll("\n", " ")
```

### 字符串分割
字符串分割时使用的`split`来自于 Java String 类型，如果传递的参数是字符则使用的是来自 StringLike 类的方法。两者不同的地方在于返回值的类型为 Array[java.lang.String] 和 Array[String]，一般情况下这一区别并不重要。
```scala
"hello world".split(" ")
//Array[java.lang.String] = Array(hello, world)
val s = "eggs, milk, butter, Coco Puffs"
s.split(",")
//Array[java.lang.String] = Array(eggs, " milk", " butter", " Coco Puffs")
s.split(",").map(_.trim)
//Array[java.lang.String] = Array(eggs, milk, butter, Coco Puffs)
```
### 替换字符串中的变量
Scala 2.10 开始你可以使用 string interpolation。使用时需要在字符串前加 `s` 前缀，在字符串中包含的变量名前添加 `$` 符号。表达式则需要嵌入在 `${}` 间。`s`是一种前缀，使用`f`时可以使用`printf`方式格式化显示内容。使用`raw`前缀时不会对内容进行转义。除了这3种 Scala 2.10 内置的解析器外，你也可以定义自己的解析器。
```scala
val name = "Fred"
val age = 33
val weight = 200.00
println(s"$name is $age years old, and weight $weight pounds.")
println(s"Age next years: ${age+1}")
println(s"You are 33 years old: ${age==33}")

case class Student(name:String, score:Int)
val hannah = Student("Hannah", 95)
println(s"${hannah.name} has a score of ${hannah.score}")

println(f"$name is $age years old, and weighs $weight%.2f pounds.")
//Fred is 33 years old, and weighs 200.00 pounds.

println(f"$name is $age years old, and weighs $weight%.0f pounds.")
//Fred is 33 years old, and weighs 200 pounds.

raw"foo\nbar"
//foo\nbar
```
2.10 之前的版本可以使用 string 的`format`方法。
```scala
val s = "%s is %d years old".format(name,age)
//Fred is 33 years old
```
可以在类的`toString`中使用这一方法来输出对象内容。

### 处理字符串中的字符
```scala
val upper = "hello world".map(c => c.toUpper)
val upper = "hello world".map(_.toUpper)
val upper = "hello, world".filter(_ != 'l').map(_.toUpper)
for(c <- "hello") println(c)
val upper = for(c <- "hello") yield c.toUpper
val result = for{
    c <- "hello, world"
    if c != 'l'
} yield c.toUpper

def toLower(c: Char): Char = (c.toByte+32).toChar
"HELLO".map(toLower)

val toLower = (c:Char) => (c.toByte+32).toChar
"HELLO".map(toLower)
```

### 字符串模式匹配
调用字符串的`.r`方法可以创建正则表达式对象，使用它的`findFirstIn`返回第一个匹配，使用`findAllIn`返回所有匹配。
```scala
val numPattern = "[0=9]+".r
val address = "123 Main Street Suite 101"
val match1 = numPattern.findFirstIn(address)
//match1: Option[String] = Some(123)

val matchs = numPattern.findAllIn(address)
//matches: scala.util.matching.Regex.MatchIterator = non-empty iterator
matches.foreach(println)
val matches = numPattern.findAllIn(address).toArray
//Array[String] = Array(123, 101)
```
创建`Regex`对象的另一方式是使用`scala.util.matching.Regex`类。
`findFirstIn`的结果是`Option[String]`，它可能的值为`Some(String)`或`None`。使用`Options`的几种方法：
 - 调用`getOrElse`获取值
 - 在`match`表达式中使用`Option`
 - 在`foreach`中使用`Option`

### 字符串模式替换
```scala
val address = "123 Main Street".replaceAll("[0-9]","x")

val regex = "[0-9]".r
val newAddress = regex.replaceAllIn("123 Main Street", "x")

val result = "123".replaceFirst("[0-9]","x")

val regex = "H".r
val result = regex.replaceFirstIn("Hello world", "J")
```

### 字符串模式提取
```scala
val pattern = "([0-9]+) ([A-Za-z]+)".r
val pattern(count,fruit) = "100 Bananas"
//count: String = 100
//fruit: String = Bananas
```
语法看起来有些奇怪像是将`pattern`定义了两次。

### 访问字符串中的字符
使用 Java 中的`charAt`方法，或是像 Scala 的数组那样使用字符串：
```scala
"hello".charAt(0)
"hello"(0)
```
通常可以用`map`或`foreach`来遍历字符串中的字符，也可以把字符串当作数组。

### 向 String 类中添加方法
从 Scala 2.10，你可以定义隐式类，通过这个类里的方法来增加你需要的功能。
```scala
implicit class StringImprovements(val s: String) {
    def increment = s.map(c => (c+1).toChar)
}
```
隐式类必须定义在类、对象或包对象里。然后在需要使用的地方导入这个类。
对于 Scala 2.10 之前的版本可以通过隐式转换的方式向类中添加方法。
```scala
class StringImprovements(val s:String){
    def increment = s.map(c => (c+1).toChar)
}
implicit def stringToString(s: String) = new StringImprovements(s)
```
建议在隐式转换类中定义的方法应该注明返回值。特别是在遇到编译器找不到你的隐式类中的方法时：
```scala
implicit class StringImprovements(val s: String) {
    // 显式的标明每个方法都返回一个字符串
    def increment:String = s.map(c==> (c + 1).toChar)
    def decrement:String = s.map(c==> (c -1 ).toChar)
    def hideAll:String = s.replaceAll(".","*")
}
```
尽管上面的例子都是返回的字符串，但是你可以在这些方法中返回任何类型。

## 数字
### 介绍
Scala 中所有数值类型都是对象。获取表达范围：
```scala
Short.MinValue
Short.MaxValue
Int.MinValue
Float.MinValue
```
对于*复数和日期*等复杂类型来说，有很多第三方项目提供了支持。如`Spire project`提供了有理数、复数、实数等类型，而`nscala-time`则提供了对`Joda Time`的封装。
### 从文本中解析数字
`StringLike`trait 提供了`to*`方法用于将字符串转换成数字。
```scala
"1".toInt
"1".toByte
"foo".toInt //出错
````
如果想要标明转换时可能发生异常可以使用`@throws`注解，特别是给 Java 调用时。
```scala
//不需要添加 throws 
def toInt(s:String) = s.toInt

@throws(classOf[NumberFormatException])
def toInt(s:String) s.toInt
```
或者使用`Option/Some/None`：
```scala
def toInt(s: String):Optiion[Int] = {
    try{
        Some(s.toInt)
    } catch {
        case e: NumberFormatException => None
    }
}
```
然后使用`getOrElse`或`match`来取值：
```scala
println(toInt("1").getOrElse(0))

toInt(aString) match {
    case Some(n) => println(n)
    case None => println("Boom! That wasn't a number.")
}

var result = toInt(aString) match {
    case Some(x) => x
    case None => 0
}
```

#### 在数值类型间转换
```scala
19.45.toInt     // 19
19.toFloat      // 19.0
```
不能像在 Java 中那样进行数值类型间的转换，而应该使用`to*`方法。
为了避免转换失败，可以使用`isValid`方法进行类型的检查：
```scala
val a = 100L
a.isValidByte       // false
a.isValidShort      // true
```

#### 覆盖默认的数值类型
Scala 会在定义数值型变量时给予默认的数据类型。也可以覆盖默认的类型。
```scala
val a = 1       //Int
val a = 1d      //Double
val a = 1f      //Float
val a = 1000L   //Long
```
另一种方式
```scala
val a = 0:Byte
val a = 0:Int
val a = 0x20    //Int 32
val a = 0x20L   //Long 32
```

#### 代替`++`和`--`
`val`是不可变的，因此不能使用自增和自减。但是`var Int`是可以使用`+=`和`-=`来修改的，同样也可以使`*=`和`/=`。

#### 比较浮点数值
与在 Java 和其它语言类似，通过一个方法来指定需要比较的精度：
```scala
def ~=(x: Double, y: Double, precision: Double) ={
    if ((x - y).abs < precision) true else false
}
```
另外还可以结合隐式转换和工具类来处理。

#### 处理非常大的数值
使用 Scala 提供的`BigInt`和`BigDecimal`来处理大数值。与 Java 中不同的是这两个类支持其它数值类型的所有操作符，它们的底层仍然是 Java 中的`BigInteger`和`BigDecimal`。

#### 生成随机数字
使用`scala.util.Random`生成随机数。这个类可以处理所有常见的用例，也可以用它来生成随机字符。

#### 创建`Rang`、`List`或数字数组
```scala
val r = 1 to 10 by 2            //Range(1,3,5,7,9)
for (i <- 1 to 5) yield i*2     //Vector(2,4,6,8,10)
```

#### 格式化数字和金额
```scala
val pi = scala.Math.Pi
println("$p%1.5f")      //3.14159
f"$pi%1.5f"             //3.14159
```
Scala 2.10 之前的版本可以使用format方法。

## 控制结构

