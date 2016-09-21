Title: Emacs Lisp参考手册
Date: 2009-12-31
Modified: 2009-12-31
Category: emacs
Tags: emacs

# 介绍
介绍和约定

这是2.9版的GNU Emacs Lisp参考手册，适应于GNU Emacs 22.1。

## 警告
## Lisp历史
## 习惯约定
这节说明了手册中的符号约定。
### 一些术语
整个手册中，词Lisp阅读器（the Lisp reader）“和“Lisp打印机（the Lisp printer）”指那些Lisp例程包括将文本方式描述的Lisp对象转换为真实的Lisp对象，反之亦然。“你”，指阅读本手册的你，即“程序员”。“用户”指使用Lisp程序的人，包括你写的那些程序。

Lisp代码被格式化为：(list 1 2 3)。函数中不合法的变量或参数将被显示为斜体： ***first-number***.
### nil和t
Lisp中符号nil有三种含义：它是一个名为‘nil‘的符号；它是逻辑值false；它是空的list——有零个元素的list。当作为变量时，nil一直表示nil值。

对于Lisp阅读器来说‘()’和‘nil’是同等的：他们代表相同的对象，符号nil。这个符号的两种不同的写法只是对于用户阅读不同。对于Lisp阅读器来说读取‘()’或‘nil’之后是无法知道程序员编写的代码时的实际写法。

在本手册中，当我们要强调是空的list时我们写作()，当写为nil时表示我们要强调它表示 **false**。这也是Lisp程序中一个很好的约定。

```emacs-lisp
(con 'foo ())                   ; 强调为空的list
(setq foo-flag nil)             ; 强调为false
```

在希望得到true时，任何非nil值都将被作为 **true**。但是，用t是表示true的首选方式。当你需要用一个值描述true时，在没有其它较好选择时就使用t。符号t的值总是t。

在Emacs Lisp中，nil和t是特殊的符号，它们的值总是他们自己。这也是为什么在程序中你不需要使用引号把它们作为常量的原因。试图改变他们的值时将导致setting-constant错误。

- Function: `booleanp` object

如果object是两个布尔值（t或nil）中的一个则返回非nil值。

### 求值的表示方法
可求值的Lisp表达式被称为form。对一个form求值总会生成一个结果，它是一个lisp对象。本手册中的例子中，使用‘=>’标识求值的结果：
```emacs-lisp
(car '(1 2))
     ;=> 1
```

可以把这读作“(car '(1 2))的值为1。”

当form是一个宏调用时，它将被展开为一个新的form被Lisp求值。我们使用‘==>’标识展开的结果。我们将有可能不显示展开的form的值。
```emacs-lisp
(third '(a b c))
     ;==> (car (cdr (cdr '(a b c))))
     ;=> c
```

有时为了帮助描述一个form与另一个form产生同样的值。将使用等价符号。
```emacs-lisp
(make-sparse-keymap) == (list 'keymap)
```

### 打印的表示方法
本手册中的许多例子在被求值时将打印文本。如果你在Lisp交互缓冲区（比如‘*scratch*’）中执行示例，打印的文本被插入到缓冲区中。如果你通过其它方法执行例子（比如使用函数eval-region求值），打印的文本将显示在回显区（echo area）。

本手册中的例子使用‘-|‘标识打印的文本，而不关心文本被输出到哪里。对form求值的结果显示在单独的一行上。
```emacs-lisp
(progn (prinl 'foo)(princ "\n") (prinl 'bar))
     ;-| foo
     ;-| bar
     ;=> bar
```

### 错误信息
有些例子将产生错误。通常错误信息显示在回显区域。我们将错误信息显示在以‘error-->’开头的行上。注意‘error-->’自身并不会显示在回显区。
```
(+ 23 'x)
error--> Wrong type argument: number-or-marker-p, x
```

### 缓冲区文本附注
有些例子可能会修改缓冲区的内容，本手册将使用“before”和“after”标识文本的版本。这些例子将缓冲区的内容显示在包含缓冲区名称的短划线之间。另外，将使用‘-|-’标识point的位置。（这个符号当然也不是缓冲区中文本的一部分；它标明当前point的位置。）
```
     ---------- Buffer: foo ----------
     This is the -!-contents of foo.
     ---------- Buffer: foo ----------

     (insert "changed ")
          => nil
     ---------- Buffer: foo ----------
     This is the changed -!-contents of foo.
     ---------- Buffer: foo ----------
```

### 描述的格式
函数、变量、宏、命令、用户属性和特殊的form的描述在手册中都有统一的格式。描述的第一行包括项的名称和它的参数（如果有）。项类型可以是函数，变量或其它内容——显示在行的开头位置。项的描述显示在余下的行中，有时带有示例。

#### 一个简单的函数的描述
在函数描述中，函数名称最先显示。在同一行上跟着参数名的列表。这些名称将用于在描述体中使用，代表参数的值。

参数列表中的关键字&optional标明subsequent参数可以被忽略（被忽略的参数默认为nil）。在调用函数时不要写&optional。

关键字&rest（它必须出现在单个变量的后面）标明后面可以带任意数量的参数。单一参数名后的&rest将被接收，它的值将作为其它参数传递给函数。在调用函数时不要写&rest。

下面是一个虚拟的函数foo的描述：

- Function: `foo` integer1 &optional integer2 &rest integers

这个函数foo将从integer2中减integer1，然后加上其它参数。如果integer2不存在，则将使用19作为默认值。

```emacs-lisp
(foo 1 5 3 9)
     ;=> 16
(foo 5)
     ;=> 14
```

更通俗的表达方式，
```
(foo w x y...)
==
(+ (- x w) y...)
```

任何参数名包含类型描述（例如，integer，integer1或buffer）表示它需要那种类型的值。复数形式（比如buffers）通常表示包含那一类型的list对象。参数名为object表示可以为任何类型。参数名有其它名称的（比如，new-file）将在函数的描述中论述。在有些情况下，多个具有类似功能的函数的通用参数将在开始的位置进行描述。

参见Lambda表达式，详细了解optional和rest参数。

命令，宏和特殊form的描述具有相同的格式，只是将‘Function’分别替换为’Command‘，‘Macro’或‘Special Form’。命令与函数相比只是可以交互式的被调用；宏处理参数的方式与函数不同（参数不会被求值），但可以以相同的方式描述。

特殊form的描述使用了更复杂的标记方法来指定optional和repeated参数，因为它们可以以更复杂的方式将参数列表分解为独立的参数。‘[optional-arg]‘表示optional-arg是可选的，‘repeated-args...’表示零个或多个参数。圆括号用于将多个参数分组到辅助的list结构。例如：

- Special Form: **count-loop** (var [from to [inc]]) body...

这个虚拟的特殊form实现了循环执行body form然后在每次迭代时将变量var自增。在第一次迭代时，变量的值为from的值；在后面的迭代中，它每次加1（或增加由inc指定的值）。如果var等于to则这个循环在执行body之前退出。下面是使用它的一个例子：
```emacs-lisp
(count-loop (i 0 10)
            (printl i) (princ " ")
            (ptinl (aref vector i))
            (terpri))
```
如果from和to被忽略，var将在循环开始时被设置为nil，如果在迭代开始时var是非nil值则循环退出。例如：
```emacs-lisp
(count-loop (done)
            (if (pending)
                (fixit)
              (setq done t)))
```
在这个特殊的form中，参数from和to是可选的，但必须同时存在或不存在。如果都存在，inc是可选的。这些变量被参数var分组到一个list中，为了将他们区别于body，它将包括form中的其它元素。

#### 一个简单的变量的描述
变量是可以保存值的对象的名字。尽管几乎所有变量都可以被用户设置，某些变量将明确用户可以修改它们；它们被称为用户选项（user options）。变通变量和用户选项的描述格式与函数是相同的只是它们没有参数。

下面是一个虚拟的变量electric-future-map。

- Variable: `electric-future-map`

变量的值是用于Electric Command Future mode的keymap。这个map中的函数允许你编辑还没有想过执行的命令。

用户选项的描述具有相同的格式，只是将‘Variable‘替换为’User Option‘。

## 版本信息
下面的设施提供了当前使用的Emacs的版本信息。

- Command: `emacs-version` &optional here

这个函数返回一个字符串描述当前运行的Emacs的版本信息。报告bug时将它包含进去非常有用。
```emacs-lisp
(emacs-version)
  ;=> "GNU Emacs 20.3.5 (i486-pc-linux-gnulibc1, X toolkit) of Sat Feb 14 1998 on psilocin.gnu.org"
```

如果here是非nil值，它将在缓冲区的point的前面插入文本，并返回nil。交互式调用时，函数将在回显区显示相同的信息，但需要通过前缀参数使用here为非nil值（译注：M-2 M-x emacs-version）。

- Variable: `emacs-build-time`

这个变量的值标明Emacs是在当前站点何时构建的。它是一个包含三个整数的list，类似current-time的值（参见Time of Day）。
```emacs-lisp
emacs-build-time
     ;=> (13623 62065 344633)
```

- Variable: `emacs-version`

这个变量的值是当前运行的Emacs的版本。它是一个类似“20.3.1”的字符串。字符串的最后一个数字并不真是Emacs release 版本的版本号的一部分；它将在你每次构建时自动加一。由四个数字组成的类似“20.3.9.1”的值，表明是一个unrelease的test版本。

下面两个变量从Emacs 19.23版开始存在。

- Variable: `emacs-major-version`

Emacs的主版本号，是一个整数。对于Emacs 20.3，它的值为20。

- Variable: `emacs-minor-version`

Emacs的次版本号，是一个整数。对于Emacs 20.3，它的值为3。

## 感谢

# Lisp数据类型
一个Lisp对象（object）是一块数据可以被Lisp程序使用和操作。对于我们来说，类型或者说数据类型是一组可能的对象。

每个对象至少属于一个类型。相同的对象有类似的结构通常可以在相同的上下文使用。类型可以被覆盖，对象可以属于两个或更多类型。因此，我们可以询问某个对象是否属于某个特殊类型，但不是”那个“个类型的一个对象。

一些基本对象类型是Emacs内置的。其它所有类型都是由这些类型构建起来的，这些基本对象类型被称为原生类型（primitive types）。每个对象有且只能属于一个原生类型。这些类型包括integer、float、cons、symbol、string、vector、hash-table、subr和byte-code函数，加上一些特殊类型，比如buffer，它与编辑相关。（参见Editing Types。）

每个原生类型有相应的Lisp函数用于检查某个对象是否是那种类型的成员。

注意Lisp不像其它语言，在Lisp中对象是类型是自描述的（self-typing）：原生类型的对象的对象类型被隐式包含在对象自身中。比如，如果对象是一个vector，则不能将它作为一个数字；Lisp知道它是一个vector而不是数字。

在多数语言中，程序员必须申明每个变量的类型，编译器知道变量的类型但不会描述在数据自身中。这样的对象申明不存在于Emacs Lisp中。Lisp变量可以有任何类型的值，它记得你存储于它里面的任何值，类型和其它所有信息。（实际上，少数Emacs Lisp变量只能用于保存某些类型的值。参考Variables with Restricted Values。）

在这章的目的是描述GNU Emacs Lisp中每个标准类型的打印表示方法和读取格式。使用这些类型的细节可以在后续章节找到。

## 打印表示方法和读取语法
对象的打印表示方法（printed representation）指由Lisp打印机（prinl函数）产生的那个对象的输出。每个数据类型有唯一的打印表示方法。对象的读取语法（read syntax）指可以被Lisp阅读器（read函数）读取的对象格式。这不需要是唯一的；很多对象类型可以有一个或多个语法。参考Read和Print。

在多数情况下，一个对象的打印表示方法也是这个对象的读取语法。然而，某些类型没有读取语法，因为在Lisp程序中输入这些类型的对象作为常量没有意义。这些对象被打印为hash notation，由字符‘#<’，一个描述字符串（通常是类型的名称跟在对象名称后面），和‘>’组成。例如：
```emacs-lisp
(current-buffer)
     ;=> #<buffer objects.texi>
```

Hash notation根本不能被读取，因此Lisp阅读器将在它遇到‘#<’时报错invalid-read-syntax。在其它语言中，一个表达式是文本；它没有其它form。在Lisp中，一个表达式首先是一个Lisp对象第二才可被读取的文本格式的对象。通常这不需要强调他们的区别，但你必须在大脑中保持清析的概念，否则有时会非常迷惑。

当你交互式的执行表达式时，Lisp解释器首先读取它的文本化描述，生成Lisp对象，然后对那个对象求值（参考Evaluation）。但，求值和读取是分开的活动。读取将返回读取的文本描述的Lisp对象；这个对象可能会被求值也可能不会。参考Input Functions，获取read的描述和读取对象的基本函数。

## 注释
注释写在程序中是为了让人们能读懂程序，对于程序本身没有作用。在Lisp中，不存在于字符串或字符常量中的分号（‘;’）标明注释的开始。注释直到行尾结束。Lisp阅读器忽略注释；他们不会变成Lisp系统中的Lisp对象。

‘#@count‘结构，用于忽略下面的count个字符，它对于程序生成的包含二进制数据的注释非常有用。

参考Comment Tips，了解注释的格式约定。

## 编程类型
在Emacs Lisp中只有两类通用类型：与Lisp编程有关，另一些与编辑有关。前者存在于很多Lisp实现中。后者是Emacs Lisp特有的。

### 整型
Emacs Lisp整型值在多数机器上的范围为-268435456至268435455（29位；例如，-2**28至2**28-1）。（某些机器可以提供更大的范围。）记得Emacs Lisp数学函数不检查溢出是很重要的。因此在多数机器上(1+ 268435455)为-268435456。

整型的读取表达式为一串十进制的数字可带正负号和后面的小数点。由Lisp解释器打印出来的打印格式不会包含前面的‘+’或最后的‘.‘。
```emacs-lisp
-1                              ; 整数-1。
1                               ; 整数1。
1.                              ; 也是整数1。
+1                              ; 也是整数1。
536870913                       ; 在29-bit的实现上也是整数1。
```
参考Numbers，获取更多信息。

### 浮点类型
浮点数相当于计算机科学计数法；你可以把浮点数当作十进制分数的集合。浮点数的精度与具体的机器有关；Emacs使用C的双精度类型存储浮点值，在内部它被表示为二进制而不是十进制。

浮点数的打印表示法可以是十进制小数，或指数形式，或两者都用。例如：‘1500.0’，‘15e2’，‘25.0e2’，‘1.5e3’，‘.15e4’五种方法都表示值为1500的浮点数。这些表示法都是等价的。

参考Numbers，获取更多信息。

### 字符类型
Emacs Lisp中的字符不过是整型。换言之，字符是使用他们的代码来描述的。比如字符A被描述为整数65。

单独的字符偶尔会用于程序中，但更常见的情况是与字符串一起工作，字符串是由有序的字符组成的。参见String Type。

字符串，缓冲区和文件中了字符被限制在0至52487-19的范围。但不是所有在这个范围的字符都是有效的字符编码。0至127为ASCII码；其它的为非ASCII字符（参考Non-ASCII Characters）。用于描述键盘输入的字符范围更宽，以编码Control，Meta和Shift等修饰符。

有一些特殊的函数可以生成字符的可阅读的文本化的描述。见Describing Characters。

### 符号类型
GNU Emacs Lisp中的符号（symbol）是一个有名称的对象。符号名被作为符号的打印表示方法。经常用于Lisp中，（参见Creating symbols），符号的名称是唯一的－没有两个符号具有相同的名称。

符号可以作为变量或函数名，或用于保存属性列表（property list）。或它只是作为区别于其它Ｌisp对象的标识，以便于它在一个数据结构中能被可靠的识别。在一个具体的上下文中，通常只有一种类型（符号作为变量名、函数名、属性列表、区别于其它对象的标识）有意义。但是可以将符号独立的用作所有的用途。

符号名称以冒号（‘:’）开头称为键盘符号（keyword symbol）。这些符号自动地作为常量，通常只被用于与未知的符号比较具有少量特殊的选择。

符号名可以包括任何字符。多数符号由字母，数字和标点符号‘-+=*/’组成。名称不需要特殊的标点符号；组成名称的字符应该足够长以使它看起来不像是一个数字。（如果不是这样，则要在开如的位置添加‘\’强制解释器将它作为符号。）‘_~!@$%^&:<>{}?’这些字符很少使用但是并不需要的标点符号。其它字符可以通过使用反斜线转义字符将其包含在符号名称中。对比用于字符串中，符号中的反斜线只会简单的引用后面的单个字符。比如，在字符串中’\t‘表示一个tab字符；在符号中，’\t‘只是表示字母’t‘。要在符号名称中使用tab字符，必须真正的使用tab（以反斜线为前缀）。但这对于字符串是非常少见的。

**Common Lisp注意：** 在Common Lisp中，小写字母总是被“folded”为大写字母，除非显式的转义。在Emacs Lisp中，字母大小写字母是敏感的。

下面是一些符号名称的例子。注意第五个例子中的‘+’例子使用转义字符防止它被作为数字。这在第四个例子中是不需要的，因为其它部分使它不成为一个有效的数字。
```emacs-lisp
foo                             ; 符号名称为’foo‘
FOO                             ; 符号名称为’FOO‘，与’foo‘不同
char-to-string                  ; 符号名称为‘char-to-string’
1+                              ; 符号名称为’1+‘
                                ; （不是’+1‘，那是一个整数）
\+1                             ; 符号名称为’+1‘
\(*\1\2)                        ; 符号名称为’(*12)’（一个更差的名称）

+-*/_~!@$%^&=:<>{}              ; 符号名称为‘+-*/_~!@$%^&=:<>{}’
                                ; 这些字符不需要转义
```
通常Lisp阅读器保留所有符号（参见Creating Symbols）。为防止被保留，你可以在符号名前面添加‘#:’。

### 序列类型
序列（sequence）是一个Lisp对象用于描述有序的元素集合。在Emacs Lisp中有两种类型的序列，list和array。因此，list或array类型的对象也被作为序列。

数组可以再细分为string，vector，char-table和bool-vector。Vector可以保存任何类型的元素，但是string中的元素必须是字符，Bool-vector元素必须是t或nil。Char-table与vector类似除了他们可以被任何有效字符代码索引。String中的字符与buffer的字符类似可以有文本属性（text properties）（参见Text Properties），但vector不支持text properties，即使当它的元素是字符时也不支持。

List，string和其它数组类型也不同，但他们有重要的相似点。比如，都有长度l，都有可以从０到l索引访问的元素。一些函数被称为sequence函数，可以接收任何类型的sequence。比如，可以向函数elt传递索引值从sequence中获得元素（译注：类似从数组中获取元素，索引类似于下标）。参见Sequences Arrays Vectors。

通常不能对同一个sequence读取两次，因为序列都是建立后，重新读取。如果你用读取sequence的语法读取两次，将会获得两个内容相同的sequence。有一个例外的就是空list()，它总是表示nil对象。

### Cons Cell和List类型
cons cell是一个对象由两个slot组成，称为CAR slot和CDR slot。每个slot可以保存或指向任何Lisp 对象。我们也可以说“cons cell的CAR是”whatever object its car slot currently holds, and likewise for the cdr.

C程序员要注意：　在Lisp中，对于“holding”一个值和“pointing to”一个值是不区分的，因为Lisp中的指针是隐式使用的。

list是一连串的cons cells，每个cons cell的CDR slot保存下一个cons cell或为空的list。空的list实际上是符号nil。参见Lists，了解工作于list的函数。因为多数cons cells被用于list的一部分，术语list结构（list structure）指向任何由con cells构成的结构。

Cons cells对于Lisp是如此重要，因此们也需要了解“不是cons cell的对象”。这些对象被称为原子（atoms）。

list的读取语法和打印描述方法是相同的，由左括，任意数量的元素和右括号组成。下面是list的一些例子：
```emacs-lisp
(A 2 "A")                       ; 有三个元素的list
()                              ; 没有元素的list（空list）
nil                             ; 没有元素的list（空list）
("A ()")                        ; 有一个元素的list，字符串"A()"
(A ())                          ; list有两个元素：A和一个空的list
(A nil)                         ; 等同于前一个例子
((A B C))                       ; 有一个元素的list
                                ; （它是一个包含三个元素的list）
```

括号内的每个对象都会变成list中的一个元素。每个元素被构造为一个cons cell。cons cell的CAR slot保存元素本身，CDR slot保存list中下一个cons cell，它保存了list中的下一个元素。最后一个cons cell的CDR slot被设置为nil。

CAR和CDR这两个名称源自于Lisp的历史。原始的Lisp实现运行在IBM 704计算机上它将words（译注：从下文看寄存器）分为两个部分，称为“address”部分和“decrement”部分；CAR指令是用于获取寄存器address部分的内容，CDR指令用于获取decrement的内容。对比来看， “cons cells”的命名来自于创建他们的函数cons，函数的命名来自于它的目的，即cells的构造器（construction）。

#### List的盒状图
list可以使用盒状图描绘，在盒状图中cons cells被显示为成对的盒，像多米诺骨牌。（Lisp阅读器不能读取这种图表；它与文本化的表示方法不同，文本化的方法即可以被人读懂也可以被机器阅读，盒状图只能被人类理解。）这张图描绘了有三个元素的list(rose violet buttercup)：
```
         --- ---      --- ---      --- ---
        |   |   |--> |   |   |--> |   |   |--> nil
         --- ---      --- ---      --- ---
          |            |            |
          |            |            |
           --> rose     --> violet   --> buttercup
```
在这张图中，每个盒表示一个可以保存或指向任何Lisp对象的slot。每对盒子表示表示一个cons cell。每个箭头表示引用一个Lisp对象，可以是atom或其它cons cell。

在这个例子中，第一个盒子，保存第一个cons cell的CAR部分，指向（refers to）或保存（holds）rose（一个符号）。第二个盒子，保存第一个cons cell的CDR部分，指向下一对盒子，即第二个cons cell。第二个cons cell的CAR是violet，它的CDR是第三个cons cell。第三个cons cell（最后一个）的CDR为nil。

下面是同一个list的另一个图表，(rose violet buttercup)，在某种意义是另一个补充：
```
      ---------------       ----------------       -------------------
     | car   | cdr   |     | car    | cdr   |     | car       | cdr   |
     | rose  |   o-------->| violet |   o-------->| buttercup |  nil  |
     |       |       |     |        |       |     |           |       |
      ---------------       ----------------       -------------------
```
没有元素的list是空list（empty list）；它等同于符号nil。换言之，nil既是符号也是一个list。

下面是list (A ())，等同于(A nil)，描述成盒状图如下：
```
         --- ---      --- ---
        |   |   |--> |   |   |--> nil
         --- ---      --- ---
          |            |
          |            |
           --> A        --> nil
```
下面是一个更复杂的图例，展示了三个元素的list，((pine needles) oak maple)，第一个元素是一个有两个元素的list：
```
         --- ---      --- ---      --- ---
        |   |   |--> |   |   |--> |   |   |--> nil
         --- ---      --- ---      --- ---
          |            |            |
          |            |            |
          |             --> oak      --> maple
          |
          |     --- ---      --- ---
           --> |   |   |--> |   |   |--> nil
                --- ---      --- ---
                 |            |
                 |            |
                  --> pine     --> needles
```
表示成第二种盒状图如下：
```
      --------------       --------------       --------------
     | car   | cdr  |     | car   | cdr  |     | car   | cdr  |
     |   o   |   o------->| oak   |   o------->| maple |  nil |
     |   |   |      |     |       |      |     |       |      |
      -- | ---------       --------------       --------------
         |
         |
         |        --------------       ----------------
         |       | car   | cdr  |     | car     | cdr  |
          ------>| pine  |   o------->| needles |  nil |
                 |       |      |     |         |      |
                  --------------       ----------------
```

#### 点对标记法（Dotted Pair Notation）
Dotted pair表示法是cons cells的一般语法，用于显式的描述CAR和CDR。在这种语法中，(a . b)表示cons cell的CAR是对象a它的CDR是对象b。Dotted pair表示法比list表示法更通用因为CDR可以不必要是list。但，如果list语法能工作的时候，这种方式更加笨重。在Dotted pair表示法中，list‘(1 2 3)’可以被写作‘(1 . (2 . (3 . nil)))’。对于以nil结尾的list，你可以任意的使用这两种表示方法，但list表式方法更加清析和方便。当打印list时，dotted paire表示法只用于cons cell的CDR不是list时。

下面使用盒状图描述了dotted pair表示法。这个例子展示了(rose . violet)：
```
         --- ---
        |   |   |--> violet
         --- ---
          |
          |
           --> rose
```
也可以组合使用dotted pair表达方式和list表达方式，以便于链接以非nil结束的CDR。你可以在list的最后一个元素后写一个点，后面跟最后的cons cell的CDR。例如，(rose violet . buttercup)等同于(rose . (violet . buttercup))。这个对象看起来如下：
```
         --- ---      --- ---
        |   |   |--> |   |   |--> buttercup
         --- ---      --- ---
          |            |
          |            |
           --> rose     --> violet
```
表达式(rose . violet . buttercup)是无效的因为它不能表达任何东西。它将buttercup放到cons cell的CDR而它的CDR已经用于violet了。

list (rose violet)等同于(rose . (violet))，看起来如下：
```
         --- ---      --- ---
        |   |   |--> |   |   |--> nil
         --- ---      --- ---
          |            |
          |            |
           --> rose     --> violet
```
类似地，包含三个元素的list(rose violet buttercup)等同于(rose . (violet . (buttercup)))。它的结构如下：
```
         --- ---      --- ---      --- ---
        |   |   |--> |   |   |--> |   |   |--> nil
         --- ---      --- ---      --- ---
          |            |            |
          |            |            |
           --> rose     --> violet   --> buttercup
```

#### 关联list类型（Association List Type）
association list或alist是一种特殊结构的list它的元素是cons cells。每个元素中，CAR被作为key，CDR作为关联的值（associated value）。（某些情况下，关联值被存在CDR的CAR中）Association list通常用作栈，因为它很容易从list的前面添加或移除关联对象。

例如：
```emacs-lisp
     (setq alist-of-colors
           '((rose . red) (lily . white) (buttercup . yellow)))
```

将变量alist-of-colors设置了包含三个元素的alist。在第一个元素中，rose是key，red是值。

参见Association Lists，了解更多关于alist及作用于alist的函数。参见Hash Tables，了解另一种lookup table，它在处理大量keys的时候更加快。

### 数组类型（Array Type）
array由任意数量的slots以保存或引用其它Lisp对象，存储在一块连续的内存中。访问数组中的任何元素所花的时间大致是相同的。相反，访问list中的一个元素所花的时间与他们存储在list中的位置成比例。（访问list结束位置的元素所花的时间比访问list开始位置的元素所花的时间更长。）

Emacs定义了四种类型的array：strings，vectors，bool-vectors和char-tables。

string是一个字符的数组，vector是任意类型对象的数组。bool-vector只可以保存t或nil。这些类型的数组的长度可以达到整型的最大值。Char-tables是稀疏的数组可以使用任意有效的字符代码作为索引；他可以保存任意的对象。

数组的第一个元素的索引为0，第二个元素索引为1，以些类推。这称为zero-origin索引。例如，数组有四个元素则有索引0，1，2和3。最大可能的索引值比数组长度小1。一旦数组被创建，它的长度就是固定的。

所有Emacs Lisp数组都是一维的。（多数其它语言支持多维数组，但他们并不是必需的；可以通过嵌套的一维数组来达到相同的效果。）每种类型的数组有其自己的读取语法；参见下面的章节了解细节。

数组类型是sequence类型的子类型，包括string，vector，bool-vector和char-table类型。

### 字符串类型
string是字符的数组。在Emacs中字符串有很多用途，例如，作为Lisp符号名，作为显示给用户的信息，作为从缓冲区中提取的文本。Lisp中的字符串是不可变的：对字符串求值返回相同的字符串。

参见Strings and Characters，了解操作字符串的函数。

#### 字符串语法
字符串的读取语法是双引号，任意数量的字符，另一个双引号，例如"like this"。为了在字符串中包含双引号，可以在双引号前添加反斜线；因而，"\""是一个字符串包含了单个双引号字符。同样，也可以使用两个双斜线表示斜线符号，如"this \\ is a single embedded backslash"。

换行符不是字符串的特殊读取语法；如果你需要在双引号间添加换行符，它将变成字符串中的一个字符。但如果换行符前有转义字符‘\’则换行符不会变成字符串的一部分；例如，Lisp阅读器在读取字符串时将忽被转义的换行符。转义符后面的空格‘\ ’也将被忽略。
```
     "It is useful to include newlines
     in documentation strings,
     but the newline is \
     ignored if escaped."
          => "It is useful to include newlines
     in documentation strings,
     but the newline is ignored if escaped."
```

#### 字符串中的非ASCII字符
可以在字符串常量书写时添加非ASCII的国际化字符。在Emacs字符串（和缓冲区中）有两种非ASCII文本描述方法：单字节（unibyte）和多字节（multibyte）。如果字符串常量是从一个多字节的源码中读取的，比如多字节的缓冲区或字符串，或以多字节方式访问的文件，这时字符被以多字节字符读取，并且将生成多字节的字符串。如果字符串常量是从多字节的源码中读取的，则字符将被以多字节的方式读取并且生成多字节的字符串。

你也可以以多字节的非ASCII字符的代码来表示字符：使用十六进制前缀，‘\xnnnnnnn’，可以带有多个数字。（多字节非ASCII字符编码都会大于256。）任何无效的十六朝向数字将结束这个结构。如果字符串中的下一个字符可以被解释为十六进制数字，则以‘\ ’（转义字符和空格）来结束十六进制转义——比如，‘\x8e0’表示一个字符，带重音符号的‘a’。字符串常量中的‘\ ’与斜线-换行符类似；它不会添加任何字符到字符串，但它会终结前面的十六进制转义。

你可以字符的编码来描述多字节的非ASCII字符，它必须在128（八进制的0200）到255（八进制的0377）之间。如果你以八进制书写所有那些字符的代码并且字符串不包含其它字符强制字符串为多字节，则将产生一个单字节的字符串。但是，在字符串中使用十六进制黑底（即使是使用在ASCII字符上）将强制字符串为多字节。

你也可以在字符串中使用字符的Unicode数字编号，使用‘\u’和‘\U’（参见Character Type）。

参见Text Representations，了解这两种文本描述方式的更多信息。

#### 字符串中的非打印字符
你可以在字符串常量中使用反斜线的转义字符序列（但不要以问号开始字符常量）。比如，你可以写一个字符串包括非打印字符tab和C-a，在他们之间添加逗号和空格："\t, C-a"。参见Character Type，了解字符读取语法的描述。

但是，并不是所有使用转义字符的字符都是有效的字符串字符。只有控制字符，ASCII控制字符可以保存在字符串中。字符串不会区别ASCII控制字符的大小写。

确切的说，字符串不能保存meta字符；但当字符串用作按键序列（key sequence）时，有一个特殊的约定提供了一个方法可以在字符串中描述meta版的ASCII字符。如果你使用‘\M-’语法标明字符串常量中的meta字符，这将设置字符串中的字符的2**7bit。如果字符串用于define-key或lookup-key，这个数字代码将被转译为相当于meta字符。参见Character Type。

字符串不能保存修饰字符hyper，super和alt。

#### 字符串中的文本属性（Text Properties）
字符串可以保存它包含的字符的文本属性。这使程序在string和buffer中复制文本和文本属性时不需要特殊的工作。参见Text Properties，以了解什么是文本属性。带文本属性的字符串使用特殊的读取和打印语法：
```emacs-lisp
#("characters" property-data...)
```
当属性数据由0个或多个元素组成时，可以用三个参数来分组：
```
beg end plist
```
元素beg和end是整数，一起指定字符串中文本的范围；plist是属性列表。例如：
```emacs-lisp
#("foo bar" 0 3 (face bold) 3 4 nil 4 7 (face italic))
```
描述了一个字符串，它的文本内容为‘foo bar’，它的前三个字符有一个face属性，属性的值为bold，后三个字符的face属性值为italic。（第四个字符没有文本属性，因此它的属性列表为nil。实际上不需要论及以nil作为属性列表的范围，因为任何不在范围中的字符默认都没有属性。）

### Vector类型
vector是一个元素可以为任何类型的一维数组。花相同的时间可以访问任何vector中的任何元素。（在List中，访问时间与元素离list开始位置的距离成正比。）

vector的打印描述方法由一个左方括号，元素和右方括号组成。这也是它的读取语法。与数字和字符串类似，vector对于求值来说是常量。
```emacs-lisp
[1 "two" (three)]               ; 有三个元素的vector
     ;=> [1 "two " (three)]
```
参见Vectors，了解工作于vector的函数。

### Char-Table类型
char-table是一个元素可以是任何类型的一维数组，通过字符代码进行索引。Char-table有某些特殊的功能使它们对于很多与设置字符代码信息相关的工作时非常有用——比如，char-table可以从父对象继承，默认值，和少量用于特目的的额外的slot。char-table也可以为整个字符集合指定单个值。

char-table的打印描述方法与vector类似，只是在开始位置添加了额外的‘#^’。

参见Char-Tables，了解操作char-tables的特殊函数。使用char-tables的包括：

  - Case tables
  - Character category tables
  - Display tables
  - Syntax tables

### Bool-Vector类型
bool-vector是一个一维数组，它的元素必须是t或nil。

bool-vector的打印描述方法像一个字符串，但它以‘#&’开头后面跟长度。这个字符串常量后面的bool-vector内容实际上看像一个bitmap——这个字符串中的每个字符包含8bits，它指定了bool-vector后面的8个元素（1表示t，0表示nil）。字符的其它的有效位对应于bool-vector底部。
```emacs-lisp
     (make-bool-vector 3 t)
          ;=> #&3"^G"
     (make-bool-vector 3 nil)
          ;=> #&3"^@"
```
这些结果很有意义，因为‘C-g’的二进制代码为111，‘C-@’的字符代码为0。

如果长度不是8的倍数，则打印描述将显示额外的元素，但这些额外的内容不会产生差异。比如，在下面的例子中，两个bool-vector是相等的，因为只有前三个bit被使用了：
```emacs-lisp
     (equal #&3"\377" #&3"\007")
          ;=> t
```

### 哈希表类型（Hash Table Type）
哈希表是一种非常快的lookup table，有点像alist，alist将key映射到对应的值，但哈希表更快。哈希表没有读取语法，打印的时候使用哈希表示法。参见Hash Tables，了解操作哈希表的函数。
```emacs-lisp
     (make-hash-table)
          ;=> #<hash-table 'eql nil 0/65 0x83af980>
```

### 函数类型（Function Type）
Lisp函数是可执行的代码，与其它编程语言中的函数类似。在Lisp中，与某些语言不同的是函数也是Lisp对象。一个不编译的Lisp函数是一个lambda表达式：它也是一个list，它的第一个元素是符号lambda（参见Lambda Expressions）。

多数编程语言不允许函数没有名称。在Lisp中函数没有内部名称。Lambda表达式可以在没有名称的情况下被函数调用；为强调这一点，我们也称它为匿名函数（ananymous function参见Anonymous Function）。命名的Lisp函数也只是一个符号它的function cell有一个有效的函数（参见Defining Function）。

多数情况下，函数将在Lisp程序的Lisp表达式中出现它的名称时被调用。但你可以在运行时构造或得到一个函数对象，并使用原生函数（primitive function）funcall和apply调用它。参见Calling Functions。

### 宏类型（Macro Type）
Lisp宏是用户定义的扩展Lisp语言的结构。将作为对象更像函数，但具有不同的参数传递语义。Lisp宏具有form list，它的第一个元素是符号macro它的CDR是一个Lisp函数对象，包括lambda符号。

Lisp宏对象通常使用内置函数defmacro来定义，but any list that begins with macro is a macro as far as Emacs is concerned。参见Macros，它说明了如何编写宏。

**警告：**Lisp宏和键盘宏（参见Keyboard Macros）是完全不同的事情。当我们使用不带限定词的单词“macro”时，表示是Lisp宏，而不是键盘宏。

### 原生函数类型（Primitive Function Type）
原生函数（primitive function）是可以从Lisp调用的函数但它是用C语言编写的。原生函数也称为subrs或built-in functions。（subr源自于subroutine）多数原生函数在他们被调用时对他们的所有参数求值。不对它的参数求值的原生函数被称为 special form（参见Special Forms）。

对于调用者来说并不关心它调用的函数是否为原生的。但如果你使用Lisp代码重新定义原生函数会产生麻烦因为原生函数可以直接被C代码调用。在Lisp代码中调用重定义的函数将使用新的定义，但如果从C代码中调用将仍然使用内置的定义。因此， **我们不推荐重新定义原生函数。**

术语function指Emacs中的所有函数，不论是用Lisp或C编写的。参见Function Type了解使用Lisp编写函数。

Primitive functions have no read syntax and print in hash notation with the name of the subroutine.

例：
```emacs-lisp
     (symbol-function 'car)          ; 访问符号的function cell
          ;=> #<subr car>
     (subrp (symbol-function 'car))  ; 是否为一个原生函数？
          ;=> t                       ; 是的
```

### Byte-Code函数类型
byte compiler生成byte-code函数对象。在内部，byte-code函数对象更象vector；但是，当它出现为一个被调用的函数时求值器将特殊地处理这种数据类型。参见Bypte Compilation，了解关于byte compiler的相关信息。

byte-code函数对象的打印和读取格式类似于vector，在‘[’前添加了‘#’。

### Autoload类型
autoload对象是一个list它的第一个元素是符号autoload。它像符号的函数定义一样被存储，它作为真实定义的占位符。autoload对象表明真实的函数定义可以在Lisp代码的文件中找到，可以在需要时加载。它包括文件的名称，和一些关于实际定义的相关信息。

当文件被加载后，符号将有一个新的函数定义而不再是一个autoload对象。这时新的定义可以被调用就像它一开始就存在于那里一样。从用户的观点来看，函数调用工作起来和预期的一样，可以使用被加载的文件中定义的函数。

autoload对象通常使用autoload函数创建，它将这个对象存储于符号的function cell区域。参见Autoload，了解更多细节。

## 编辑类型（Editing Types）
前一节讲述的类型用于通用编程目的，它们中的大多数也用于大多数的Lisp方言中。Emacs Lisp提供了几个特殊的类型用于连接编辑处理。

### 缓冲区类型
buffer是一个对象用于保存可编辑的文本（参见Buffers）。多数缓冲区用于保存磁盘文件的内容（参见Files）以便于被编辑，但另一些用于其它目的。有时，在一个窗口中（参见Windows），一些缓冲区只用于显示给用户查看。但缓冲区不必要一定显示在窗口中。

缓冲区的内容更像一个字符串，但缓冲区在Emacs Lisp中不能用作字符串，它们的操作也是不同的。例发，你可以在一个缓冲区中插入文本更改缓冲区的内容，但是“插入”文本到字符串中需要连接子字符串（concatenating substring），其结果是一个全新的新字符串对象。

每个缓冲区都有一个指定的位置称为point（参见Positions）。在任何时候，有一个缓冲区是当前缓冲区。多数编辑命令操作当前缓冲区中邻近point的内容。许多标准Emacs函数操作或测试当前缓冲区中的字符；这个手册中有一整章用于描述这些函数（参见Text）。

有几个其它的数据结构与每个缓冲区关联

  - 本地语法表（local syntax）（参见Syntax Tables）；

  - 本地按键映射（local keymap）（参见Keymaps）；

  - 缓冲区局部绑定的变量的list（参见Buffer-Local Variables）

  - overlays（参见Overlays）

  - 缓冲区的文本属性（参见Text Properties）

局部按键映射和变量列表包含了覆盖全局按键绑定的值或新值的入口。这些用于在不同的缓冲区自定义程序的行为，而不会改变程序本身。

缓冲区可能是indirect的，这与另一个缓冲区共享文本，但用它的不同的方式呈现内容。参见Indirect Buffers。

缓冲区没有读取语法。打印时将显示缓冲区的名称。
```emacs-lisp
     (current-buffer)
          ;=> #<buffer objects.texi>
```

### Marker类型
marker指示了具体缓冲区的位置。markers有个组件：一个用于缓冲区，另一个用于位置。修改缓冲区的文本将自动重新定位位置的值以确保marker总是指向缓冲区中的两个字符之间的位置。

markers没有读取语法。打印为hash表示法时，将显示当前字符的位置和缓冲区的名称。
```emacs-lisp
     (point-marker)
          ;=> #<marker at 10779 in objects.texi>
```

参见Markers，了解如何测试，创建，复制和移动markers。

### Window类型
window表示终端屏幕的一部分，Emacs用它显示一个缓冲区。每个window有一个相关的缓冲区，它的内容显示在窗口中。相反，一个缓冲区可以显示在一个窗口中，或不显示在窗口中，或显示在多个窗口中。

尽管可以同时存在很多窗口，同一时候只有一个窗口是当前选中窗口（selected window）。这是当前光标停留的窗口，在这个窗口中Emacs等侍命令输入。选中的窗口通常显示当前缓冲区（current buffer），但这并不是必需的情况。

窗口在屏幕上被组织到frames中；每个窗口属于一个并且只能属于一个frame。参见Frame Type。

窗口没有读取语法。打印为hash表示法时，将显示窗口号和显示的缓冲区的名称。窗口号用于唯一标识窗口，因为显示在窗口中的缓冲区可能会改变。
```emacs-lisp
     (selected-window)
          ;=> #<window 1 on objects.texi>
```

参见Windows，了解工作于窗口的函数。

### Frame类型
frame是一个屏幕区域包含一个或多个Emacs窗口；我们也使用术语“frame”指向Lisp对象，Emacs使用它指向屏幕区域。

Frames没有读取语法。它们打印为哈希标记法，frame标题加它在核心中的的地址（用于唯一标识frame）。
```emacs-lisp
     (selected-frame)
          ;=> #<frame emacs@psilocin.gnu.org 0xdac80>
```

参见Frames，了解工作于frames的函数。

### 窗口配置类型（Window Configuration Type）
window configuration存储frame中的窗口的位置，尺寸，内容相关的信息，因此你可以重新组织窗口的位置。

Window configurations没有读取语法；它的打印语法格式如“#<window-configuration>”。参见Window Configurations，了解与window configurations相关的函数。

### Frame Configuration类型
Frame configuration存储了所有frame中的窗口的位置，大小和内容等信息。它实际上是一个list，它的CAR是frame-configuration它的CDR是一个alist。每个alist元素描述一个frame，它作为那个元素的CAR出现。

参见Frame Configurations，了解与frame configurations相关的函数。

### 进程类型
单词“进程”通常表示运行的程序。Emacs自己也是那样一个运行的进程。在Emacs Lisp中，进程是一个Lisp对象，表示由Emacs进程创建的子进程。shell，GDB，ftp和编译器等程序作为Emacs子进程运行，扩展了Emacs的能力。

Emacs子进程从Emacs接收文本化输入并返回文本化的输出到Emacs中以便处理。Emacs也可以发送信号到子进程。

进程对象没有读取语法。它使用哈希表示法打印，显示进的名称：
```emacs-lisp
     (process-list)
          ;=> (#<process shell>)
```

参见[[#Processes][Processes]]，了解关于进程创建，删除，返回信息，发送输入或信号和接收输出到进程的函数。

### Stream类型
stream是一个对象流可以提供字符作为输入或输出。很多不同的类型可以使用这种方式，比如：marks，buffers，strings和functions。通常，输入流（字符源）可以从键盘、缓冲区或文件获得，输出流可以发送到缓冲区，例如*Help*缓冲区或回显区。

nil对象，用于流有其它的含义。它表示变量standard-input或standard-output。对象t作为流指定使用minibuffer作为输入（参见MiniBuffers）或输出到回显区（参见The Echo Area）。

参见Read and Print，了解与流相关的函数，包括解析和打印函数。

### Keymap类型
keymap将按键映射到用户命令。这个映射控制了用户命令如何被输入执行。按键映射实际上是一个list，它的CAR是keymap符号。

参见[[#Keymaps][Keymaps]]，了解创建keymaps，处理前缀参数，局部和全局映射，修改按键组合。

### Overlay类型
overlay指定了将应用到缓冲区的属性。每个overlay将应用到缓冲区的指定范围，包括了一个属性列表（一个包含将要修改的属性和值的list）。overlay属性用于将当前缓冲区临时设置为不同的显示风格。Overlay没有读取语法，在打印为哈希表达方式时，将显示缓冲区的名称和位置范围。

参见[[#Overlays][Overlays]]，了解如何创建和使用overlays。

## 环状对象的读取语法（Read Syntax for Circular Objects）
为在一个复杂的Lisp对象中描述共享或通知结构时，你可以使用读取结构‘#n=’和‘#n#’。

在一个对象前使用#n=标明它是一个延时的引用；在后面，你可以在另一个地方使用#n#来引用同一个对象。在这里，n是个整数。比如，下面的例子产生了一个list，在这里第一个元素在第三个元素处重现了：
```emacs-lisp
     (#1=(a) b #1#)
```
这不同于普通的表达式：
```emacs-lisp
     ((a) b (a))
```
在这个表达式生成的list中第一个和第三个元素看起来相同，但他们不是同一个Lisp对象。下面显示了他们的不同：
```emacs-lisp
     (prog1 nil
       (setq x '(#1=(a) b #1#)))
     (eq (nth 0 x) (nth 2 x))
          ;=> t
     (setq x '((a) b (a)))
     (eq (nth 0 x) (nth 2 x))
          ;=> nil
```
你也可以使用相同的语法产生一个环状结构，它表现了一个元素处理它自己内部。这里有一个例子：
```emacs-lisp
     #1=(a #1#)
```
这样生成的list的第二个元素是list自身。这里展示了它是如何工作的：
```emacs-lisp
     (prog1 nil
       (setq x '#1=(a #1#)))
     (eq x (cadr x))
          ;=> t
```
如果将变量print-circle设置成了非nil值Lisp打印器可以按这种语法在Lisp对象中生成环状和共享结构。参见[[#Output_Variables][Output Variables]]。

## 类型判定（Type Predicates）
Emacs Lisp解释器对于传递给被调用的函数的参数并不会对参数执行类型检查。它也做不到这一点，因为Lisp中的函数参数并没有申明数据类型，这与其它编程语言不同。对此可以使用检查参数属于哪种类型的函数。

所有内置函数都会检查他们的实参是否适当，如果参数类型错误将生成wrong-type-arguemnt错误。例如，下面展示了如果传递不能处理的参数给+将产生错误：
```emacs-lisp
     (+ 2 'a)
          error--> Wrong type argument: number-or-marker-p, a
```
如果你希望程序可以用不同的方式处理不同的类型，则必须显式的进行类型检查。通常检查对象的类型的方法是调用类型判定（type predicate）函数。Emacs对于每个类型都有类型判定函数，对于一些组合类型也有类型判定函数。

类型判定函数接收一个参数；如果参数属于相应的类型则返回t，否则返回nil。按Lisp对于类型判定函数的的习惯，多数类型判定函数名称心‘p’结束。

下面的例子使用了listp检查是list，使用symbolp检查symbol。
```emacs-lisp
     (defun add-on (x)
       (cond ((symbolp x)
              ;; If X is a symbol, put it on LIST.
              (setq list (cons x list)))
             ((listp x)
              ;; If X is a list, add its elements to LIST.
              (setq list (append x list)))
             (t
              ;; We handle only symbols and lists.
              (error "Invalid argument %s in add-on" x))))
```
下表列举了预定义的类型判定函数，按字母顺序排列。

atom

    参见[[#atom][atom]]

arrayp

    参见[[#arrayp][arrayp]]

bool-vector-p

    参见[[#bool-vector-p][bool-vector-p]]

bufferp
    参见[[#bufferp][bufferp]]

byte-code-function-p
    参见[[#byte-code-function-p][byte-code-function-p]]

case-table-p
    参见[[#case-table-p][case-table-p]]

char-or-string-p
    参见[[#char-or-string-p][char-or-string-p]]

char-table-p
    参见 char-table-p.

commandp
    参见 commandp.

consp
    参见 consp.

display-table-p
    参见 display-table-p.

floatp
    参见 floatp.

frame-configuration-p
    参见 frame-configuration-p.

frame-live-p
    参见 frame-live-p.

framep
    参见 framep.

functionp
    参见 functionp.

hash-table-p
    参见 hash-table-p.

integer-or-marker-p
    参见 integer-or-marker-p.

integerp
    参见 integerp.

keymapp
    参见 keymapp.

keywordp
    参见 Constant Variables.

listp
    参见 listp.

markerp
    参见 markerp.

wholenump
    参见 wholenump.

nlistp
    参见 nlistp.

numberp
    参见 numberp.

number-or-marker-p
    参见 number-or-marker-p.

overlayp
    参见 overlayp.

processp
    参见 processp.

sequencep
    参见 sequencep.

stringp
    参见 stringp.

subrp
    参见 subrp.

symbolp
    参见 symbolp.

syntax-table-p
    参见 syntax-table-p.

user-variable-p
    参见 user-variable-p.

vectorp
    参见 vectorp.

window-configuration-p
    参见 window-configuration-p.

window-live-p
    参见 window-live-p.

windowp
    参见 windowp.

booleanp
    参见 booleanp.

string-or-null-p
    参见 string-or-null-p.

最通用的检查对象类型的方法是调用type-of函数。再次强调每个对象只属于且仅能属于一个原生类型；type-of可以告诉你它属于哪种类型（参见[[#Lisp_Data_Types][Lisp Data Types]]）。但是type-of不了解非原生类型的信息。在多数情况下，更方便的是使用类型判定函数type-of。

- Function: `type-off` object

这个函数返回object的原生类型的名称的符号。返回值可能是下面的一个符号：symbol，integer，float，string，cons，vector，char-table，bool-vectorhash-table，subr，compiled-function，marker，overlay，window，buffer，frame，或window-configuration。
```emacs-lisp
          (type-of 1)
               ;=> integer
          (type-of 'nil)
               ;=> symbol
          (type-of '())    ; () is nil.
               ;=> symbol
          (type-of '(x))
               ;=> cons
```

## 相等判定（Equality Predicates）
这里我们讲述两个用于测试两个对象的相等性的函数。其它函数测试特定类型的对象的相等性，比如，string。对于这些判定，可以参见相应的章节描述。

- Function: `eq` object1 object2

如果object1和object2是相同的对象，则返回t，否则返回nil。

如果object1和object2是整数并有相同的值eq将返回t。因为符号名通常是唯一的，如果参数是符号并有相同的名字，则它们相等。对于其它类型（比如，lists，vectors，strings），两个参数有相同的同内容或元素不必要每个都相等：它们是同样的对象时相等，这意味着改变一个的内容将影响反映到另一个上产生同样的变化。
```emacs-lisp
         (eq 'foo 'foo)
               ;=> t

         (eq 456 456)
               ;=> t

         (eq "asdf" "asdf")
               ;=> nil

         (eq '(1 (2 (3))) '(1 (2 (3))))
               ;=> nil

         (setq foo '(1 (2 (3))))
               ;=> (1 (2 (3)))
         (eq foo foo)
               ;=> t
         (eq foo '(1 (2 (3))))
               ;=> nil

         (eq [(1 2) 3] [(1 2) 3])
               ;=> nil

         (eq (point-marker) (point-marker))
               ;=> nil
```
make-symbol函数返国 个uninterned符号，这有别于你编写在Lisp表达式的符号。这两种不同的符号有相同的名称但不相等（eq）。参见[[Creating_Symbols][Creating Symbols]]。
```emacs-lisp
          (eq (make-symbol "foo") 'foo)
               ;=> nil
```

- Function: `eqal` object1 object2

如果object1和object2有相等的内容则返回t，否则返回nil。eq检查它的参数是否为相同的对象，equal检查它的参数内部的元素或内容是否一样。因此，如果两个对象eq则他们equal，反之则不一定。
```emacs-lisp
          (equal 'foo 'foo)
               ;=> t

          (equal 456 456)
               ;=> t

          (equal "asdf" "asdf")
               ;=> t
          (eq "asdf" "asdf")
               ;=> nil

          (equal '(1 (2 (3))) '(1 (2 (3))))
               ;=> t
          (eq '(1 (2 (3))) '(1 (2 (3))))
               ;=> nil

          (equal [(1 2) 3] [(1 2) 3])
               ;=> t
          (eq [(1 2) 3] [(1 2) 3])
               ;=> nil

          (equal (point-marker) (point-marker))
               ;=> t

          (eq (point-marker) (point-marker))
               ;=> nil
```
字符串比较时是大小写敏感的，但不会考虑文本属性（）text properties），它只会比较字符串中的字符。因为技术原因，单字节字符串和多字节字符串比较时，如果他们包含相同的字符代码序列并且所有这些代码都处于0至127（ASCII）之间或160至255（八bit图元），则两个字符串equal。（参见[[#Text_Representations][Text Representations]]）。
```emacs-lisp
          (equal "asdf" "ASDF")
               ;=> nil
```

两个不同的buffer总不会equal，即使他们的文本内容是相同和。

相等性的测试是通过递归实现的：例如，两个cons cells分别为x和y，在下面的两个表达式都返回t时(equal x y)返回t。
```emacs-lisp
     (equal (car x) (car y))
     (equal (cdr x) (cdr y))
```

因为这是一个递归方法，circular list将会至进入无限递归（导致产生错误）。

# 数字（Numbers）
GNU Emacs支持两种数字类型：整形（integer）和浮点（floating point)类型。Integer值如－3，0，7，13和511。他们的值是精确的。Floating point数字是带有小数部分的数字，比如－4.5，0.0或2.71828。他们也可以表示为科学计数法：1.5e2等于150；在这个例子中，‘e2’表示10的2次方，乘1.5。Floating point值是不精确的；他们有一个固定的有限的精度。

## 整数基础（Integer Basics）
Integer的范围依赖于具体的机器类型。最小范围是-268435456至268435455（29位；-2**28至2**28-1），但有些机器可以提供更宽的范围。这章中的许多例子都假设整数为29bits。Lisp阅读器将整数当作数字序列读取，前面可以带有符号后面可以带有小数点。
```emacs-lisp
      1               ; The integer 1.
      1.              ; The integer 1.
     +1               ; Also the integer 1.
     -1               ; The integer ?1.
      536870913       ; Also the integer 1, due to overflow.
      0               ; The integer 0.
     -0               ; The integer 0.
```

十进制以外的其它整数表示方法使用‘#’后跟一个字母指定进制：‘b’表示二进制，‘o’表示八进制，‘x’表示十六进制，或‘radixr’以指明进制。指定进制的字母的大小写无关。因此，‘#binteger’将以二进制读取整数，‘#radixrinteger’将以指定的进制读取整数。进制指定的范围为2至36。例如：
```emacs-lisp
     #b101100 ;=> 44
     #o54 ;=> 44
     #x2c ;=> 44
     #24r1k ;=> 44
```

了解整数处理相关的函数，特别是位操作（参见[[#Bitwise_Operations][Bitwise Operations]]），它对于了解数字的二进制处理很有帮助。

在29bit的二进制中，数字5看起来如下：
```
     0 0000  0000 0000  0000 0000  0000 0101
```
（我们在以4bits为一组插入了一个空格，8bits一组插入了两个空格，以便阅读。）

整数-1看起来如下：
```
     1 1111  1111 1111  1111 1111  1111 1111
```
-1被描述为29个1。（This is called two's complement notation.）

在这种实现方式中，最大的29bit的二进制整数值为268,435,455。它的二进制形式如下：
```
     0 1111  1111 1111  1111 1111  1111 1111
```
由于算术函数不会检查整数是否溢出，当你将1和268,435,455相加后将得到负整数-268,435,456：
```emacs-lisp
     (+ 1 268435455)
          ;=> -268435456
          ;=> 1 0000  0000 0000  0000 0000  0000 0000
```

这章中介绍的许多函数在接收number的地方都可以接收marker。（参见[[#Markers][Markers]]。）因为这些函数的实参可以是numbers或markers，我们通常将这些参数称为number-or-marker。当参数值是marker时，将使用它的位置信息而它的buffer信息将被忽略。

- Variable: `most-positive-fixnum`

这个变量的值是Emscs Lisp可以处理的最大的整数值。

- Variable: `most-negative-fixnum`

这个变量的值是Emacs Lisp可以处理的最小的整数值。它是一个负数。

## 浮点数基础（Floating Point Basics）
Floating point用于描述非整型的数字。Floating point的精度范围与具体机器相关；它的范围与你使用的机器的C语言double类型的精度范围相同。

Floating point的读取语法需要一个小数点（后面至少有一个小数），一个整数部分，或者两者都有。例如，‘1500.0’、‘15e2’、‘15.0e2’、‘1.5e3’和‘.15e4’这5种写法都是表示1500。它们都是相等的。你也可以使用减号写floating point的负数，‘-1.0’。

多数现代的计算机都支持IEEE floating point标准，它提供正负无穷大的floating point值。它也提供了一个值类型NaN或称为“not-a-number”；算术函数函数在不能正确响应时返回这个类型的值。例如，(/ 0.0 0.0)将返回NaN。在实际应用中，Emacs Lisp中不同的NaN值之间的区别并没有实际意义，没有规则表明在某个特殊情况下需要使用哪个NaN，因此Emacs Lisp不会去区分它们（但它在打印时不会报告出标记）。下面是特殊的floating point值的读取语法：

正无穷大
```emacs-lisp
`1.0e+INF'
```

负无穷大
```emacs-lisp
`-1.0e+INF'
```

Not-a-number
```
`0.0e+NaN' 或 `-0.0e+NaN'
```

为了测试一个floating point值是否为NaN，可以将它与自身使用=比较。如果是NaN则返回nil，其它floating point值将返回t。

在IEEE的floating point中-0.0与普通的0是有区别的，但是Emacs Lisp中equal和=都把他们当作相等的值。

你可以使用logb提取二进制数的浮点数值（或取整数的对数）：

- Function: `logb` number

这个函数返回number的二进制数。更精确的讲，返回值是number的以2为底的对数四舍五入的值。
```emacs-lisp
          (logb 10)
               ;=> 3
          (logb 10.0e20)
               ;=> 69
```

## 数字的类型判定（Type Predicates for Numbers）
这节中的函数用于测试数字，或指定数字的类型。函数intergerp和floatp可以接收任何类型的Lisp对象作为参数（否则它们将没有多大作用），但zerop判定需要一个数字作为参数。参见[[#Predicates_on_Markers][Predicates on Markers]]中的integer-or-marker-p和number-or-marker-p。

－ Function: `floatp` object

这个判定测试它的参数是否为一个floating point数，如果是则返回t，否则返回nil。

floatp在Emacs 18版或更早的版本中不存在。

- Function: `integrep` object

这个判定测试它的参数是束为一个integer，如果是则返回t，否则返回nil。

- Funtion: `numberp` object

这个判定测试它是参数是否为数字（integer或floating point），如果是则返回t，否则返回nil。

- Function: `wholenump` object

wholenump判定（它的名称来自于短语“whole-number-p”）测试它的参数是否为一个非负的整数，如果是则返回t，否则返回nil。0被作为非负。

natnump是wholenump被废弃的同义词。

- Function `zerop` number

这个判定测试它的参数是否为0，如果是则返回t，否则返回nil。参数必须是一个数字。
```
(zerop x) 等同于 (= x 0)
```

#Comparison-of-Numbers
## 数字的比较（Comparision of Numbers）
测试数字的数值相等性，通常应该使用=，而不是eq。具有相同的数值的floating point数字对象可能是截然不同。如果使用eq比较他们，则你在测试两个值是否为相同的对象。相反，=只比较对象的数值。

目前，在Emacs Lisp中每个integer值有一个唯一的Lisp对象。因此，在处理integer时eq等同于=。某些情况下使用eq比较一个未知的值和一个integer比较方便，因为如果这个未知值不是数字时eq不会产生错误——它可以接收任何类型的参数。相反，如果参数不是numbers或markers，则=号将产生错误。但是，如果可以则使用=号是一个好主意，即使是在比较integers时，以防我们在将来的Emacs版本中修改integers的表示方法。

有时使用equal比较两个number也比较有用；如果两个number有相同的数据类型（都是integer或都是floating point）它将两个number当作equal。相反，=可以将integer和floating point当作相等。参见[[#Equality_Predicates][EqualityPredicates]]。

另一个小问题：因为floating point的数学运算是不精确的，检查两个floating point的相等性不是个好主意。通常较好的方法是比较他们的相似性。有一个函数可以完成这个比较：
```emacs-lisp
     (defvar fuzz-factor 1.0e-6)
     (defun approx-equal (x y)
       (or (and (= x 0) (= y 0))
           (< (/ (abs (- x y))
                 (max (abs x) (abs y)))
              fuzz-factor)))
```

**Common Lisp注意：**在Common Lisp中比较number总是需要=因为Common Lisp实现了multi-word integers，两个不同的integer对象可以有相同的数值。Emacs Lisp对于给定的值只有一个integer对象，因为它的integer值的范围是有限的。

- Function: `=` number-or-marker1 number-or-marker2

检查它的参数的数字是否相等，如果是则返回t，否则返回nil。

- Function: `eql` value1 value2

的行为类似eq，除了在两个参数都是number时。它比较number的类型的数值，因此(eql 1.0 1)返回nil，但(eql 1.0 1.0)和(eql 1 1)都返回t。

- Function: `/=` number-or-marker1 number-or-marker2

检查它的参数的数字是否相等（numerically equal），如果不是则返回t，如果是则返回nil。

- Function: `<` number-or-marker1 number-or-marker2

检查它的第一个参数是否严格地（strictly）小于第二个参数。如果是则返回t，否则返回nil。

- Function: `<=` number-or-marker1 number-or-marker2

检查它的第一个参数是否小于或等于它的第二个参数。如果是则返回t，否则返回nil。

- Function: `>` number-or-marker1 number-or-marker2

检查它的第一个参数是否大于第二个参数。如果是则返回t，否则返回nil。

- Function: `>=` number-or-marker1 number-or-marker2

测试第一个参数是否大于或等于第二个参数。如果是则返回t，否则返回nil。

- Function: `max` number-or-marker &rest numbers-or-markers

返回参数列表中的最大值。如果参数中的任何一个值为float型，则返回值也为float型，即使这个最大的参数是以整型传入的。

- Function: `min` numbers-or-markers &rest numbers-or-markers


返回参数列表中的最小值。如果参数中的任何一个值为float型，则返回值也为float型，即使这个最小的参数是以整型传入的。

- Function: `abs` number

返回参数的绝对值。

#Numeric-Conversions
## 数值转换（Numeric Conversions）

- Function: `float` number

将number转换为浮点类型。如果number本身就是浮点型的则返回它自身。

有四个函数用于将浮点类型转变为整数；他们的区别在于进位处理上。它们都接收number型参数和可选的divisor参数。这两个参数都可以是整数或浮点数。divisor也可以是nil。如果divisor为nil或被忽略，则这些函数将number参数转化为整型，如果number原来是整型则返回原来的整数。如果divisor是非nil值，则将number除以divisor将并将结果转换为整数。如果divisor为0则返回arith-error。

- Function: `truncate` number &optional divisor










#Processes
# 进程
执行子进程并与其通讯。

在操作系统术语中，进程是程序可以执行的的一块区域。Emacs是作为一个进程进行的。Emacs Lisp程序可以调用其它进程。这些被称为Emacs进程的子进程（subprocesses或processes），Emacs进程是它们的父进程。

Emacs的子进程可以是同步或异步的，这取决于怎样子进程如何被创建。当创建同步子进程时，Lisp程序在继续执行之前将等侍子进程结束。当创建异步子进程时，它将与Lisp程序并行的运行。这些子进程类型在Emacs内部被描述为Lisp对象，它也被称为“进程（process）”。Lisp程序可以使用这个对象与子进程通讯或控制它。比如，你可以向它发送信号，获取状态信息，接收进程的输出，或向它发送输入。

- Function: `processp` object

这个函数返回t如果object是一个进程，否则返回nil。

## 子进程的创建
启动子进程的函数。

有三个函数创建新的子进程来运行程序。start-process，创建一个异步进程并返回一个process对象。call-process和call-process-region，创建一个同步进程并且它不会返回一个process对象。

同步和异步进程将在后面的章节解释。由于这三个函数的调用方式是类似的，它们的公共参数在这里描述。

在所有的情况下，函数的program参数指定要被运行的程序。如果文件未找到或不能被执行将显示错误。如果文件名是相对路径，变量exec-path包含了将搜索的目录的列表。Emacs在它启动时初始化exec-path，它的值基于环境变量PATH。标准文件名结构‘~‘，‘.‘和‘..‘，在exec-path中被正确的解释，但环境变量代入（比如，‘$HOME‘）将不被识别；使用substitute-in-file-name来处理它们。这个list中的nil指向default-directory。

执行程序时将尝试在名称后添加指定的后缀：

- Variable: `exec-suffixes`

这个变量是一个将添加到指定程序名后的后缀名的列表。这个list应该包含”“，如果你需要使用完整的执行文件名时。这个变量的默认值是与平台相关的。

注意：包含参数的程序应该只使用程序的名称；不可以包含命令行参数。应该使用 args 来提供参数。

每个用于创建子进程的函数都有一个 buffer-or-name 参数用于指定程序的标准输出。它可以是一个缓冲区或缓冲区名称；如果它是一个缓冲区名称，则将在缓冲区不存在时创建这个缓冲区。它也可以是 nil，在没有过虑处理函数时这表示忽略输出。通常，应该避免将多个进程的输出发送到同一个缓冲区因为它们的输出将被随机的混合在一起。

所有这三个创建子进程的函数都有一个 &rest 参数，args 。args 必须都是都是字符串，它们被提供给程序作为独立的命令行参数。这个字符串中的通配符和其它shell中的字符将没有特殊意义，因为字符串将被直接传递给程序。

子进程将获取 default-directory 的值作为它的当前目录。

子进程从 Emacs 中继承环境变量，但你指定 process-environment 来覆盖这个值。

- Variable: `exec-directory`

这个变量的值是一个字符串，包含 GNU Emacs 所包含的程序的目录名称。例如 movemail ；Rmail 使用它从收件箱中获取新邮件。

- User Option: `exec-path`

这个变量的值是一个目录的 list ，它用于搜索作为子进程运行的程序。每个元素可以是一个目录名或 nil ，nil 表示缺省目录（变量 default-directory 的值）。exec-path 将在 program 参数不是绝对路径时被用于 call-process 和 start-process 。

## Shell 参数
Lisp 程序有时需要运行 shell 并给它一个包含用户指定的文件名称的命令。这个程序应该能处理任何有效的文件名。但 shell 将对特殊字符作特殊的处理，如果这些字符包含在文件名中，将会导致 shell 迷惑。为了处理这些字符，可以使用 shell-quote-argument 函数。

- Function: `shell-quote-argument` argument

#Variables
# 变量

Lisp中符号名为变量名，符号的value cell存储的是变量的值。同一个符号既可以作为变量名又可以作为函数名。参见[[#Symbol Components][Symbol Components]]

#Global Variable
## 全局变量：变量值在任何地方都存在。

通常创建的变量都是全局变量，在整个Lisp系统中都有效。

通过setq来指定符号的值。



# Major和Minor Modes

## Font Lock Mode
Font Lock mode是用于根据缓冲区的语法规则自动设置某些部分的face属性的一项功能。它如何来解析缓冲区依赖于major mode；多数major mode都为自己定义了基于语法规则的face。

Font Lock mode查找文本并高亮有两个方法：根据语法表通过语法解析或通过搜索（通常是正则表达式）。基于语法的方式先进行；它找出注释和字符串常量并高亮它们。然后再进行基于搜索的操作。

### Font Lock Basics
有多个变量可以控制Font Lock mode对文本进行高亮显示。但major modes不应该直接设置其它变量。它应该设置buffer-local变量font-lock-defaults。当Font Lock mode被开启时，将使用这个变量。

- Variable: `font-lock-defaults`

这个变量由major mode设置为buffer-local变量，用于指定在那种mode下如何显示文本。当设置它时它将自动变为buffer-local变量。如果它的值为nil，Font Lock mode不会高亮，你可以使用‘Edit’下的‘Text Properties’中的‘Faces’菜单显式的设置缓冲区中文本的外观。

如果它为非nil值，它的值应该类似下面：
```
(keywords [keywords-only [case-fold
           [syntax-alist [syntax-begin other-vars...]]]])
```
第一个元素，keywords间接指定font-lock-keywords的值，它导致基于查询的字体设置。它可以是符号，变量或函数（值是一个用于font-lock-keywords的list）。
