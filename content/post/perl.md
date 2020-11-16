---
title: "Programming Perl笔记"
date: 2007-12-02
modified: 2007-12-02
categories: ["开发"]
tags: ["perl"]
---

# OverView
## 自然的人工语言
### 变量语法
变量类型

类型 || 字符 || 例子 || 说明
标量 | $ | $cents | 单个的值（数字或字符串）
数组 | @ | @large | 值列表，键为数字
哈希表 | % | %interest | 一组值，键为字符串
子程序 | & | &how | 一块可被调用的代码
glob | <code>*</code> | <code>*</code>struck | 所有被命名为struck的东西

###  变量赋值

#### 单一变量
```perl
$answer = 42;                # 一个整数
$pi = 3.14159265;            # 一个实数
$avocados = 6.02e23;         # 科学计数法
$pet = "Camel";              # 字符串
$sign = "I love my $pet";    # 带插值的字符串
$cost = 'It costs $100';     # 无插值的字符串
$thence = $whence;           # 另一个变量的值
$salsa = $moles * $avocados; # 表达式
$exit = system("vi $file");  # 命令返回的数字值
$cwd = `pwd`;                # 命令输出的字符串
```

标量也可以引用其它数据结构，包括子程序和对象。

```perl
$ary = \@myarray;            # 一个命名数组的引用
$hsh = \%myhash;             # 一个命名哈希的引用
$sub = \&mysub;              # 一个命名子程序的引用

$ary = [1,2,3,4,5];          # 未命名数组的引用
$hsh = {Na => 19, Cl => 35}; # 未命名哈希的引用
$sub = sub { print $state }; # 未命名的子程序

$fido = new Camel "Amelia";  # 对象的引用
```

如果使用了一个未被赋值过的变量，这个未初始化过的变量将自动按需要产生。根据最小惊讶原则，变量创建时可能带的null值，或""或0，依赖于你在什么地方使用它们，变量将被自动解释为字符串，数字或"true"和"false"（布尔变量）。在人类语言中语言环境相当重要。在Perl中，多个操作符希望某一类厅异值作为参数。有时将更具体，将这些参数称作数字环境，字符串环境，或布尔环境。（后面也将谈及列表环境，它与标量环境是相对应的。）Perl将自根据当前环境的需要将数据进行转换。比如：
```perl
$camels = '123';
print $camels + 1, "\n";
```
$camels的初始值是一个字符串，但它被转换成数字后加1，然后转换回字符串被输出为124。"\n"换行符也处于字符串环境中，但由于它已经是一个字符串了，因此不需要转换。但主注意我们在它上面使用了双引号——使用单引号的'\n'将产生包含两个字符的字符串，内容为斜线和“n”，它不是一个换行符。

因此，在某种意义上来说，双引号和单引号也是另一种特殊的环境。对引号内的字符串的解释取决于你使用的引号类型。（双引号环境是Perl中的“内插（interpolative）”环境，它也被许多其它的与双引号不同的操作符支持。

类似地，当你给引用一个“解除引用（dereference）”环境时表示得像引用，但另一方面又表现得像一个标量。比如：
```perl
$fido = new Camel "Amelia";
if (not $fido) { die "dead camel"; }
$fido->saddle();
```
这里创建了一个Camel对象的引用并把它赋给变量$fido。在下一行，我们把$fido作为一个布尔型的标量来检查它是否为“true”，如果不为true抛出异常。但在最后一行，我们把$fido作为一个引用，并要求它在$fido中持有的对象中查找saddle()方法，这发生在Camel类，因此Perl在Camel对象上查找saddle()方法。

#### 复数变量
某些类型的变量持有逻辑上配合在一起的多个值。Perl有两种多值变量：数组和哈希。有些情况下，这些行为像标量——比如，他们在需要时被自动创建。但它们与标量不同，当你给它们赋值时，它们为右值提供了一个列表（list）环境而不是一个标量环境。

数组和哈布之间也不同。你需要使用数字来查找时应该使用数组。需要通过名称来查找时使用哈希。这是两个补充概念。

##### 数组
数组是一个标量的列表，通过标量在列表中的位置来访问。列表中可以包含数字，字符串，或两者都有。（它也可以包含子数组或子哈希的引用）给数组赋值：
```perl
@home = ("couch", "chair", "table", "stove");
```
反过来，你在列表环境中使用@home，比如在列表赋值的右边，你将得到同样的值。因此你可以像下面这样从数组中设置四个标量：
```perl
($potato, $lift, $tennis, $pipe) = @home;
```
这被称为列表赋值。理论上它们是并行发生的，因此你可以像下面这样交换变量：
```perl
($alpha,$omega) = ($omega,$alpha);
```
与C里一样，数组下标从0开始，通过方括号访问。因为处理的元素是标量，因此你需要在前面加$。
```perl
$home[0] = "couch";
$home[1] = "chair";
$home[2] = "table";
$home[3] = "stove";
```
由于数组是有序的，你可以在上面做更多复杂的操作，比如作为堆栈执行push和pop操作。毕竟堆栈也只是一个有序的列表，有一个开始的结束。特别是结束。Perl把数组的结束作为栈顶。（尽管多数Perl程序员把数组当作是水平的，栈顶在右边。）

##### 哈希
哈希是一组无序标量的集合，通过关联到每个标量的字符串值来访问。由于这个原因哈希经常被叫作关联数组。
由于哈希中的key不能由它们的位置自动提供，你必须提供key。你可以像数组一样提供一个列表给哈希，但列表中的项将作为键值对分割。哈希使用%来标识。
```perl
%longday = ("Sun", "Sunday", "Mon", "Monday", "Tue", "Tuesday",
            "Wed", "Wednesday", "Thu", "Thursday", "Fri",
            "Friday", "Sat", "Saturday");
```
这难于阅读perl提供了=>，使得更容易区分哈希中的键和值。
```perl
%longday = (
    "Sun" => "Sunday",
    "Mon" => "Monday",
    "Tue" => "Tuesday",
    "Wed" => "Wednesday",
    "Thu" => "Thursday",
    "Fri" => "Friday",
    "Sat" => "Saturday",
);
```

哈希的排序，可以使用keys函数获取哈希的key列表然后用sort函数进行排序。

由于哈希是一种奇怪的数组，你必须使用大括号来选择其中的元素。需要再次注意的是你处理的元素是标量，因此应该在它的前面使用$而不是%。
```perl
$wife{"Adam"} = "Eve";
```

#### 复杂数据结构
在hash元素中保存list时等号右边应该使用方括号，因为在Perl中小括号和其中逗号不足以将list保存到标量中（小括号用于分组，逗号用于分隔）。下面的写法是错误的：
```perl
$wife{"Jacob"} = ("Leah", "Rachel", "Bilhah", "Zilpah");        # WRONG
```
正确写法如下：
```perl
$wife{"Jacob"} = ["Leah", "Rachel", "Bilhah", "Zilpah"];        # ok
```
这个语句创建了一个未命名的array并将它的引用放到hash元素<code>$wife{"Jacob"}</code>中。这种方式也是Perl处理多维数组和嵌套数据结构的方式。与使用普通array和hash一样，也可以按下面的方式赋值：
```perl
$wife{"Jacob"}[0] = "Leah";
$wife{"Jacob"}[1] = "Rachel";
$wife{"Jacob"}[2] = "Bilhah";
$wife{"Jacob"}[3] = "Zilpah";
```
哈希中的元素为另一个哈希，而这个哈希中的元素为数组：
```perl
$kids_of_wife{"Jacob"} = {
    "Leah"   => ["Reuben", "Simeon", "Levi", "Judah", "Issachar", "Zebulun"],
    "Rachel" => ["Joseph", "Benjamin"],
    "Bilhah" => ["Dan", "Naphtali"],
    "Zilpah" => ["Gad", "Asher"],
};
```
它比下面的方式简洁多了：
```perl
$kids_of_wife{"Jacob"}{"Leah"}[0]   = "Reuben";
$kids_of_wife{"Jacob"}{"Leah"}[1]   = "Simeon";
$kids_of_wife{"Jacob"}{"Leah"}[2]   = "Levi";
$kids_of_wife{"Jacob"}{"Leah"}[3]   = "Judah";
$kids_of_wife{"Jacob"}{"Leah"}[4]   = "Issachar";
$kids_of_wife{"Jacob"}{"Leah"}[5]   = "Zebulun";
$kids_of_wife{"Jacob"}{"Rachel"}[0] = "Joseph";
$kids_of_wife{"Jacob"}{"Rachel"}[1] = "Benjamin";
$kids_of_wife{"Jacob"}{"Bilhah"}[0] = "Dan";
$kids_of_wife{"Jacob"}{"Bilhah"}[1] = "Naphtali";
$kids_of_wife{"Jacob"}{"Zilpah"}[0] = "Gad";
$kids_of_wife{"Jacob"}{"Zilpah"}[1] = "Asher";
```
可以使用这种方式添加更多的层，但在内部的描述方式是一样的。

在这里最重要的一点是Perl允许你将复杂的数据结构描述为一个简单的标量。通过这种简单的封装，Perl构建了面向对象结构。例如前面调用的Camel构造器：
```perl
$fido = new Camel "Amelia";
```
我们创建了一个Camel对象它被描述为一个标量$fido。但在Camel的内部它更复杂一些。对于面向对象的程序员，我们不需要了解Camel的内部（除非我们是实现Camel类方法的人）。但通常，类似Camel的类是由一个包含Camel的各个属性的hash构成，比如它的名称（在这里是”Amelia"，而不是“fido”），和hump（驼峰）的数量。

#### 简单数据结构
与真实的语言环境中单词依据不同的环境有不同的含义一样。Perl使用了多种方式来标明当前的环境。其中一个重要的局部环境申明就是package。假设你要在Perl中谈论Camel。你可以这样开始你的模块：
```perl
package Camel;
```
这将产生多个值得注意的影响。其一就是Perl将假定从这个点开始任何未指明的动词或名词都是关于Camel的。它将自动为任何全局名称前面添加模块名作为前缀“Camel::”。因此代码：
```perl
package Camel;
$fido = &fetch();
```
这样$fido的真实名称为$Camel::fido（&fetch的真实名称为&Camel::fetch，但我们先不谈论动词）。这表示如果另一个模块为：
```perl
package Dog;
$fido = &fetch();
```
Perl不会迷惑，因为$fido的真实名称为$Dog::fido，而不是$Camel::fido。包只是建立了一个命名空间。你可以创建任意多个命名空间，但由于同一时间只处于其中一个，你可以假设其它命名空间不存在。这种简单是基于假设的。（当然，这过于简单化了，这只是我们在这章所做的。）

命名空间使得&Camel::fetch和&Dog::fetch不会迷惑，但包真正好的地方在于它对你的动作进行了分类以便其它包使用它们。当我们说：
```perl
$fido = new Camel "Amelia";
```
我们实际调用了Camel包的&new动作，它的全名为&Camel:new。前面所说的：
```perl
$fido->saddle();
```
调用的是&Camel::saddle子程序，因为$dido知道它指向的是Camel类型的数据。这就是面向对象编程的工作方式。

使用已经存在的包时，使用<code>use</code>申明，这不仅是为了调用另一个包中的动作，也将检查那个模块是否已经从磁盘加载过了。实际上，你必须在使用
```perl
$fido = new Camel "Amelia";
```
前，使用
```perl
use Camel;
```
否则，Perl不知道Camel的定义。

事实上一些内置模块不需要实际引入它们的动词。这些特殊模块被称为<code>pragmas</code>。比如，你经常可以看到人们使用<code>strict</code>：
```perl
use strict;
```
strict模块将使Perl加强对程序的检查，你对一些事务必须更加显式的指定，比如变量的作用范围等。这对于大型项目是很有帮助的。默认情况下Perl为小型项目而优化，但使用strict模块，Perl也能用于需要更多可维护性的大项目。

### 动词
与其它命令式计算机语言一样，Perl中的动作是命令：它们告诉Perl解释器做什么。另一方面与自然语言一样，Perl动词的含义也依赖于具体的环境。以动词开头的语句通常是纯命令，被整个执行。（有时称这些动词为子程序，特别是当他们是用户定义的时候。）一个常用的内置命令是print命令：
```perl
print "Adam's wif is $wife{'Adam'}.\n";
```
这将产生下面输出：
<example>
Adam's wife is Eve.
</example>
但在某些祈使语句内包含有”语气“。一些动词是用于提问的，对于条件语句非常有用，比如if语句。其它动词将它们的输入参数轮换为返回值，我们称这些动词为函数。

比如内置的exp函数：
```perl
$e = exp(1);   # 2.718281828459 or thereabouts
```

但Perl中子程序和函数没有明确区别。动词有时也被称作操作符（当内置时），或子过程。可以按你的喜好来叫——他们都返回一个值，它可能是一个没有意义的值，你可以或使用或忽略它。

历史上的，Perl需要在任何用户定义的子过程前面加一个<code>&</code>符号。但从Perl 5开始，&符号变为可选项，因此用户定义的动词与内置动词有相同的语法。当我们谈论子程序的名称时，我们仍将使用&符号，比如当我们获取它的引用时（$fetcher = \&fetch;）。从语言上来说，你可以把&符号当作不定词，“to fetch“或类似”do fetch“。但我们说”do fetch“时我们可以只说”fetch“。这也是我们在Perl5中抛弃强制使用&符号的实际原因。

## 一个求平均值的例子
这个例子用于求数据平均值，数据：
<example>
No&#235;l 25
Ben 76
Clementine 49
Norm 66
Chris 92
Doug 42
Carol 25
Ben 12
Clementine 0
Norm 66
...
</example>
它保存于名为grades的文件中。

程序如下：
```perl
 1  #!/usr/bin/perl
 2  
 3  open(GRADES, "grades") or die "Can't open grades: $!\n";
 4  while ($line = <GRADES>) {
 5      ($student, $grade) = split(" ", $line);
 6      $grades{$student} .= $grade . " ";
 7  }
 8 
 9  foreach $student (sort keys %grades) {
10      $scores = 0;
11      $total = 0;    
12      @grades = split(" ", $grades{$student});
13      foreach $grade (@grades) {
14          $total += $grade;
15          $scores++;
16      }
17      $average = $total / $scores;
18      print "$student: $grades{$student}\tAverage: $average\n";
19  }
```

执行时使用-w开关以获取警告信息。

## 文件句柄
在求平均值的例子中的GRADES是Perl中的另一种数据类型，文件句柄（filehandle）。文件句柄是你给一个文件，设备，socket或管道起的名字，帮助你记得他们是做什么的，隐藏了如缓冲等复杂的东西。（在内部文件句柄像C++等语言中的流。）

文件句柄使用很容易在不同的地方读写数据。这部分使得Perl成为了一种非常好的脱水语言，它可以在同一时间处理很多文件和操作。

使用open创建文件句柄并将它绑定到文件。open函数至少需要两个参数：文件句柄和要关联的文件名。Perl也提供了一些预定义的文件句柄。标准输入STDIN，标准输出STDOUT和STDERR，STDERR允许你和程序伪造输出到你的输出中。

由于你可以使用open创建用于多种目的的文件句柄（输入，输出，管道），因此需要指定你需要的是哪种行为。你可以在命令行上，在文件句前添加字符，
```perl
open(SESAME, "filename")               # read from existing file
open(SESAME, "<filename")              #   (same thing, explicitly)
open(SESAME, ">filename")              # create file and write to it
open(SESAME, ">>filename")             # append to existing file
open(SESAME, "| output-pipe-command")  # set up an output filter
open(SESAME, "input-pipe-command |")   # set up an input filter
```

文件句柄的命名是任意的。一旦打开，文件句柄SESAME就可以使用，直到显式的关闭它（close(SESAME)），或直到在后面的程序中使了open将这个句柄指向了另一个文件。打开一个已经打开的句柄将隐式的关闭先前打开的文件，使用它变为不可达的句柄，并打开一个不同的文件。对于这个操作要小心。有时会出现意外，比如使用<code>open($handle,$file)</code>时，$handle包含了一个constant的字符串。确保$handle的唯一性，否则你将在同一个句柄上打开新文件。或者$handle未定义，Perl将填充它。

可以用<>操作符读取文件中的行。尖括号包含文件句柄（<SESAME>）。空的操作符<>将从命令行上指定的所有文件中读入行，或从STDIN中读入。（这是许多过滤程序的标准行为。）一个使用STDIN文件句柄的例子：
```perl
print STDOUT "Enter a number: ";          # ask for a number
$number = <STDIN>;                        # input the number
print STDOUT "The number is $number.\n";  # print the number
```
STDIN是缺省输入，STDOUT是缺省输出。

行读入操作符不会自动移除换行符需要使用chop移除它。通常可以这样做：
```perl
chop($number = <STDIN>);
```

## 操作符

## 控制结构
### True的定义

 1. 非""和非"0"的字符串为true。

 2. 除0外的任何数字为true。

 3. 任何引用都为true。

 4. 任何未定义的值都为false。

## 正则表达式

## 列表处理
Perl中有两个重要的环境，标量环境（处理单一的东西）和列表环境（处理复数的东西）。
