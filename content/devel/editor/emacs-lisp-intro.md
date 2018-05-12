Title: Programming in Emacs Lisp笔记
Date: 2008-07-16
Modified: 2008-07-16
Category: 效率
Tags: emacs

# 序

# 表处理
## Lisp列表
### 数字，列表中的列表
列表里也可以包含数字：(+ 2 2)。

Lisp里的数据和程序都是相同的方式实现的，他们都是在括号中由单词、数字或者其它列表组成的用空白分隔的列表。因为程序看起来像数据，所以一个程序可以当作数据传递给另一个程序，这是lisp一强非常强大的功能。

### Lisp原子
Lisp列表中的单词叫原子（意为原子在Lisp列表中不可再分割成更小的单位）。与原子不同，list可以分隔成更小的单位（car cdr & cons）。

空的列表：()，被称作空列表。与其它的数据类型不同，空列表被同时看作原子和列表。

与自然界的原子一样,Lisp中的原子这个名称来出现得太早（意指与自然界的原子一样，原子还可以再分割）。Lisp中部分原子，比如数组就可以进行分割。但是这种机制与列表的分隔是不同的。如果依据对列表的分隔方式来说，列表中原子就是不可分隔的了。

### 列表中的空白
额外的空白被用来提高代码的可读性。
```emacs-lisp
'(this list
   looks like this)
```
与
```emacs-lisp
'(this list looks like this)
```
是相同的。

### 列表排版
在Emacs Lisp mode下，有多种方法来对Lisp语句进行排版。比如，按<TAB>键将自动缩进当前光标所在行到正确的位置。M-C-\可以格式化当前所选区域中的代码。

## 运行一个程序
执行Lisp程序时，将执行下列三者之一：
 1. 什么都不做，返回列表本身
 2. 返回错误信息
 3. 把列表中的第一个符号当作命令执行一些操作

放在列表前的单引号被称作引用（quote）；当用它来处理列表时，它告诉Lisp不要对列表进行处理。但如果列表前没有单引号，则列表前的第一个元素是特殊的，它被当作命令被执行（Lisp中这些命令被称作函数）。列表(+ 2 2)显示也与加引号的列表的不同，Lisp知道需要用+来处理列表中的其它元素：把后面的数字相加。

## 生成错误信息
错误信息是由内置的GNU Emacs debugger生成的。进入debugger后，可以用按键q退出debugger。

## 符号名称和函数定义
Lisp中同一指令可以被绑定到多个名称。

另一方面,在同一时刻一个符号只允许绑定到一个函数定义上。

由于Emacs Lisp的庞大，它有一套按照不同函数功能分类的符号命名规则。如：所有处理Texinfo的函数都心textinfo-开头，而处理邮件的函数以rmail-开头。

## Lisp解释器
Lisp的工作方式：首先，它查看列表前是否有单引号，如果有则解释器给出这个列表。如果没有引号，解释器检查列表中的第一个元素是否有对应的函数定义，如果找到则解释器调用函数定义的指令。否则，解释器将打印出错误信息。

### 复杂一点的内容
Lisp解释器可以对没有单引号且不被括号包围的符号。Lisp解释器将检测符号是否为一个变量。

一些函数不是普通的方法。被用来处理一些特殊的工作，比如定义一个函数。

Lisp求值时，将先对列表内部嵌入的列表进行求值，从内向外。

Lisp解释器工作时从左向右，从一个语句到另一个语句（从上至下）。

### 编译（Byte Compiling）
Lisp解释器可以解释两种类型的代码：人可以读的代码和另一种被你为byte compiled code的代码。编译过的代码执行更快。

可以用byte-compile-file编译代码。被编译好的字节码文件扩展名为.elc。

## 求值
当Lisp解释器工作于一个语句上时，这个活动的过程被称为求值（evaluation）。求值完成后解释器将返回函数定义的执行结果，或者在函数出错时给出错误信息。

### 对内部列表求值
可以把光标停留在内部列表右括号的后面，按C-x C-e执行。
```emacs-lisp
(+ 2 (+ 3 3))
```
把光标放在括号后面，或者把光标放在代码下面的空行的行首，都可以得到8。如果用C-x C-e对一个数字求值将得到数字自身，这也是数字与符号的不同。

## 变量
Emacs Lisp中符号可以有一个值绑定到它或者一个函数定义绑定到它。两者不同在于，函数定义是指令的集合。值是可以修改的数字或者其它。符号的值可以是任意的Lisp表达式，比如符号、数字、列表、字符串等。有值的符号通常被称作变量。

符号可以同时有一个函数定义和值。两个是分开的。例：
```emacs-lisp
(defun test_f ()
"test2"
(message "bbb"))

(setq test_f "124")

test_f          -> 变量值"124"
(test_f)        -> 函数调用显示"bbb"
```

### fill-column一个变量的例子
变量fill-column，每个Emacs缓冲区，这个符号通常被设置成72或70,但也可能有不同的值。可以用C-x C-e对fill-column这个符号求值。

符号可以有值绑定到上面，我们可以绑定变量到值、数字、字符串、列表甚至是函数定义。

### 函数符号未定义时的错误信息
当我们对fill-column求值时将得到变量的值时并没有在符号外面添加括号。这是因为我们不打算将符号当作函数的名称。

如果fill-column是列表中的第一个元素或者唯一的元素，Lisp解释器将查找绑定到符号上的函数定义。但fill-column不是一个函数定义。当我们对
```emacs-lisp
(fill-column)
```
求值时将产生错误信息：
```
---------- Buffer: *Backtrace* ----------
Debugger entered--Lisp error: (void-function fill-column)
  (fill-column)
  eval((fill-column))
  eval-last-sexp-1(nil)
  eval-last-sexp(nil)
  call-interactively(eval-last-sexp)
---------- Buffer: *Backtrace* ----------
```
函数fill-column未定义。

按q退出调试器。

### 符号没有值时的错误信息
例如对
```emacs-lisp
(+ 2 2)
```
中的+号求值（光标停留在+的后面，按C-x C-e）时将产生错误信息：
```
---------- Buffer: *Backtrace* ----------
Debugger entered--Lisp error: (void-variable +)
  eval(+)
  eval-last-sexp-1(nil)
  eval-last-sexp(nil)
  call-interactively(eval-last-sexp)
---------- Buffer: *Backtrace* ----------
```
这个错误信息与上节函数未定义时的不同。表示变量+未定义。

## 参数
### 参数类型
传递给函数的数据类型依赖于函数需要使用何种信息。比如+函数需要数字类型的参数。concat需要字符串类型的参数。substring是一个特殊一点的函数（称作原子粉碎机），它能把从原子类型中解析出一部分数据。
```emacs-lisp
(substring "The quick brown fox jumped." 16 19)
```

### 变量值或者列表当作参数
例：
```emacs-lisp
(+ 2 fill-column)
(concat "The " (number-to-string (+ 2 fill-column)) " red foxes.")
```

### 参数数量
一些函数可以带多个参数，例如：+、*。
```emacs-lisp
(+)       ; => 0

(*)       ; => 1

(+ 3)     ; => 3

(* 3)     ; => 3

(+ 3 4 5) ; => 12

(* 3 4 5) ; ==> 60

```

### 使用错误类型的参数
当传递了错误的参数类型时Lisp解释器将产生错误信息。例如对
```emacs-lisp
(+ 2 'hello)
```
求值的结果：
```
---------- Buffer: *Backtrace* ----------
Debugger entered--Lisp error:
         (wrong-type-argument number-or-marker-p hello)
  +(2 hello)
  eval((+ 2 (quote hello)))
  eval-last-sexp-1(nil)
  eval-last-sexp(nil)
  call-interactively(eval-last-sexp)
---------- Buffer: *Backtrace* ----------
```
错误信息的第一部分直截告诉我们参数类型错误(wrong-type-argument。第二个部分看起来有些迷惑number-or-marker-p，这部分告诉了我们+函数所需要的参数类型。

符号number-or-marker-p说明Lisp解释器检查提供给函数的信息（参数的值）是否是数字或marker（C-@或C-<SPC>设置的位置，mark可以被当作数字进行处理－mark在缓冲区中的字符位置）。Emacs Lisp中+可以将数字和作为数字的marker位置相加。

number-of-marker-p中的p是早期Lisp程序中的用法。p是'predicate'的简写。是早期Lisp研究者所使用的术语，predicate指明了函数用于决定一些属性是true还是false。因此p告诉我们number-or-marker-p是一个根据参数是否为数字或者marker而返回true或者false的函数。另一个以p结尾的Lisp符号包括zerop，这是一个检查参数值是否为0的函数，listp则是一个检测参数是否为一个列表（list）的函数。

最后，错误信息的其它部分将显示出符号hello。这是传递给+的参数值。

### message函数
message函数显示信息到回显区。占位符%s表示字符串，%d为整数。例子：
```emacs-lisp
(message "This message appears in the echo area!")
(message "The name of this buffer is: %s." (buffer-name))
(message "The value of fill-column is %d." fill-column)
(message "There are %d %s in the office!"
         (- fill-column 14) "pink elephants")
(message "He saw %d %s"
         (- fill-column 34)
         (concat "red "
                 (substring
                  "The quick brown foxes jumped." 16 21)
                 " leaping."))
```

## 设置变量值
有几种方法给变量赋值。set或setq函数，let函数。

### 使用set
要把符号flowers的值设置为列表'(rose violet daisy buttercup)，可以执行下面的语句：
```emacs-lisp
(set 'flowers '(rose violet daisy buttercup))
```
列表(rose violet daisy buttercup)将显示在回显区。这是set函数的返回值。另一方面符号flowers被绑定到列表；这样符号flower可以看作一个变量，它具有那个列表值。

在对set语句求值后，就可以对符号flowers求值，它将返回set设置的值。
当对：
```emacs-lisp
flowers
```
求值时，回显区将显示(ros violet daisy buttercup)。

这时如果对'flowers求值，将在回显区看到符号自身flowers。

当使用set时，需要在两个参数前加单引号，除非你想对它们进行求值。如果没有加单引号，则解释器将先对参数进行求值，例如对flowers求值，如果flowers之前未赋过值，则将报错，如果对flowers的求值返回了值，则后面的变量值将赋给对flowers求值所返回的值上。这种情况非常少见。
```emacs-lisp
(set 'flowers 'aaa)
(set flowers "123")
(message aaa)       ->显示"123"
```

### 使用setq
setq与set类似，但setq将自动给第一个参数前加单引号。另一方面，setq允许在一条语句中同时设置多个不同的变量值。例：
```emacs-lisp
(setq carnivores '(lion tiger leopard))
```
与
```emacs-lisp
(set 'carnivores '(lion tiger leopard))
```
相同。

setq可以给多个变量赋值，例：
```emacs-lisp
(setq trees '(pine fir oak maple)
      herbivores '(gazelle antelope zebra))
```
尽管我们一直在用赋值（'assign'），但有另一种方式思考set和setq；即set和setq使一个符号指向（point）一个列表。

### 计数器
这是一个在计数器中使用setq的例子。
```emacs-lisp
(setq counter 0)                ; 初始化
(setq counter (+ counter 1))    ; 增加
counter
```

## 小结
 - Lisp程序由表达式组成，表达式可以是列表或者原子。
 - 列表由零个或者多个原子或内部列表组成，各元素由空白分隔，被括号包括。列表可以为空。
 - 原子是多个字符符号，比如：forward-paragraph，单字符比如+，双引号间的字符串，数字。
 - 对自身求值的数字。
 - 双引号间的字符串也将对自身求值。
 - 当对符号自身求值时，将返回它指向的值。
 - 当对列表求值时，Lisp解释器查看列表中的第一个符号所绑定的函数定义。然后按定义的指令执行。
 - 单引号，'，告诉Lisp解释器应该把后面的表达式按原样返回，不对它进行求值。
 - 参数是传递给函数的信息。函数是列表中的第一个元素，其它元素被求值并作为参数传递给函数。

# 实践
## 执行代码
通过C-x C-e执行代码

## 缓冲区名称
buffer-name和buffer-file-name这两个函数用于区分文件和缓冲区。

如果是在*scratch*缓冲区中，可以用C-u C-x C-e运行代码，这样运行结果会显示在表达式的后面。

## 获取缓冲区
buffer-name可以获取缓冲区名称，current-buffer可以返回缓冲区本身。

other-buffer可以获得上一次访问过的缓冲区。

## 切换缓冲区
switch-to-buffer可以切换当前缓冲区。产生与按C-x b类似的效果。
下面的代码将切换当前缓冲区到上次访问过的缓冲区：
```emacs-lisp
(switch-to-buffer (other-buffer))
```

另一个函数set-buffer也是用于切换缓冲区的，但与switch-to-buffer不同在于它只改变程序处理的缓冲区，并不改变当前屏幕显示的缓冲区。

## 缓冲区大小和光标位置
几个简单的函数用于缓冲区大小和检测光标位置：buffer-size,point,point-min,point-max。

# 编写函数
## 关于基本函数(Primitive Function)
除了少数C编写的基本函数外，所有的函数都是由其它函数语句定义的。当编写自己函数时，C所编写的函数与Emacs Lisp编写的函数看起来是一样的。

除非你想去考究，否则不需要知道知道一个函数是用Emacs Lisp编写的还是C编写的。

## defun
在一个函数的定义中，在defun关键字后面有5个部分：
 1. 函数符号的名称
 2. 传递给函数的参数列表,如果没有参数则传递给函数的是一个空列表,()
 3. 描述函数的文档字符串。（可选）
 4. 当用户按M-x func_name以交互方式运行函数时的提示信息;或按键组合。（可选）
 5. 函数体

模板
```emacs-lisp
(defun function-name (arguments...)
    "optional-documentation..."
    (interactive argument-passing-info) ; optional
    body...)
```
一个实例（非交互）
```emacs-lisp
(defun multiply-by-seven (number)
  "Multiply NUMBER by seven."
  (* 7 number))
```
函数参数列表中的变量名对每个函数是私有的，不同函数的参数名可以相同。

参数列表后面是描述函数功能的文档字符串。也就是按C-h f name_of_function时所看到的信息。

在调用的时候使用
```emacs-lisp
(multiply-by-seven 3)
```
尽管传递给函数的参数外面没有加括号。但函数能计算出来。

当对这个表达式求值时将出错。这是因为我们只编写了函数定义，但并未告诉机器在Emacs中安装(install/load)这个函数定义。

## 安装函数定义
将光标停留上节所写的函数定义的最后一个括号后面，按C-x C-e。这时回显区将显示multiply-by-seven(这表示函数定义被计算，计算的返回值是所定义的函数的名字)。这时函数就已经安装好，可以在像使用Emacs中其它函数一样使用了。

### 安装后的效果
可以在
```emacs-lisp
(multiply-by-seven 3)
```
的最后一个括号后按C-x C-e，回显区将显示计算结果21。
还可以查看函数帮助文档。按C-h f(describe-function) function_name，multiply-by-seven。y

### 修改函数定义
可以直接修改函数的定义，然后重新把光标停留在在函数定义的最后一个括号后面按C-x C-e。

## 制作交互式函数
用户可以通过按键或者M-x 函数名来调用。

### 交互式函数multiply-by-seven预览
交互式版本的multiply-by-seven：
```emacs-lisp
(defun multiply-by-seven (number)
  "Multiply NUMBER by seven."
  (interactive "p")
  (message "The result is %d" (* 7 number)))
```
安装上面的函数后，可以使用C-u number参数，然后输入M-x multiply-by-seven然后回车。回显区将显示计算结果。

调用这个函数的两种方法：
 1. 输入前缀参数，然后输入M-x和函数名，比如C-u 3 M-x forward-sentence
 2. 输入任意按键绑定例如：C-u 3 M-e

输入C-u不带数字，则参数默认为4。

### 交互式函数multiply-by-seven
在上节所写的函数中,表达式(interactive "p")中的"p"告诉Emacs把前缀参数(C-u后带的参数)作为函数参数(number)传递给函数。

message是一个Emacs Lisp函数，用于显示信息给用户。

## 不同的interactive选项
emacs有超过20过的选项可以传递给interactive。具体可以查阅elisp手册。

例如，字符r，Emacs将把当前选中区域作为两个参数传递给函数。
```emacs-lisp
(interactive "r")
```
B告诉Emacs提示用户输入缓冲区名称，并把该缓冲区作为参数传递给函数。例如：
```emacs-lisp
(interactive "BAppend to buffer:")
```
当函数需要2个或更多参数时，可以在interactive中添加新的部分。每个部分用\n分隔。例如：
```emacs-lisp
(defun name-of-function (buffer start end)
  "documentation..."
  (interactive "BAppend to buffer: \nr")
  body-of-function...)
```
如果一个函数不需要参数，可以直接使用
```emacs-lisp
(interactive)
```

## 永久的安装函数
安装函数的几种方法：
 1. 把代码放在.emacs文件中。
 2. 把代码放在其它文件中，使用load函数装载文件。
 3. 如果所有用户都要使用可以把代码放在site-init.el文件中

## let
let表达式是在多数函数中都要用到的一个Lisp表。

let用于修改或者绑定值到符号上。

### let 可以防止混乱
let创建的是本地变量，作用范围止于let表达式范围内，不影响let外部的变量。let可以一次创建多个变量，并给每个变量赋值，初始值也可以是nil。在let执行完后，将返回最后一个语句的值。

### let表达式的组成
let表达式分为3个部分，第一部分是符号"let"。第二个部分被称为变量列表（varlist），每个元素都一个符号或者包含二个元素的列表，每个列表中的一个元素是一个符号。第三部分是let的体（body）。
```emacs-lisp
(let ((variable value)
      (variable value)
      ...)
  body...)
```

### let表达式举例
```emacs-lisp
(let ((zebra 'stripes)
      (tiger 'fierce))
  (message "One kind of animal has %s and another is %s."
           zebra tiger))
```

### let语句中的未初始化变量
```emacs-lisp
(let ((birch 3)
      pine
      fir
      (oak 'some))
  (message
   "Here are %d variables with %s, %s, and %s value."
   birch pine fir oak))
```
这里的pine、fir的值都是nil。

## if语句
if的基本理念就是，如果if测试为真则表达式被执行。

### if 细节
```emacs-lisp
(if true-or-false-test
    action-to-carry-out-if-test-is-true)
```
例：
```emacs-lisp
(defun type-of-animal (characteristic)
  "Print message in echo area depending on CHARACTERISTIC.
If the CHARACTERISTIC is the symbol `fierce',
then warn of a tiger."
  (if (equal characteristic 'fierce)
      (message "It's a tiger!")))
```
```emacs-lisp
(type-of-animal 'fierce)
(type-of-animal 'zebra)
```
(type-of-animal 'fierce)将在回显区显示"It's a tiger!"，第二行将返回nil。

## if-then-else语句
```emacs-lisp
(if true-or-false-test
    action-to-carry-out-if-the-test-returns-true
  action-to-carry-out-if-the-test-returns-false)
```
例：
```emacs-lisp
(defun type-of-animal (characteristic)  ; Second version.
  "Print message in echo area depending on CHARACTERISTIC.
If the CHARACTERISTIC is the symbol `fierce',
then warn of a tiger;
else say it's not fierce."
  (if (equal characteristic 'fierce)
      (message "It's a tiger!")
    (message "It's not fierce!")))
```

## Emacs Lisp中的真值与假值
符号nil作为假值，nil外的其它值都为真。
### 对nil的解释
在Emacs Lisp中对符号nil有两种解释。一种代表空的列表，另一种为真假判断中的假值。nil可以被写作：()、nil。对Lisp解释器来说两种写法是相同的。推荐用nil表示false，()表示空的列表。

在Emacs lisp里，任何非nil非空列表的值都被当作真。

## save-excursion
save-excursion函数保存当前的point和mark，然后执行函数体，然后恢复point和mark的位置。它的主要目的是为了保存用户在调用函数前所设置的point和mark。

### point和mark
Point指当前光标之前的一个位置。在Emacs Lisp中，point是一个整数。缓冲区中第一个字符的point数字是1，函数point返回当前光标位置。

Mark是缓冲区中的另一个位置。其值是通过C-<SPC>（set-mark-command）设置的。通过C-x C-x（exchange-point-and-mark）可以在point和mark间跳转。如果设置了另一个mark，前一个mark被保存到mark ring里去。可以通过C-u C-<SPC>将光标跳转到被保存的mark。

缓冲区中point和mark之间的区域叫作region。大量命令用于region上，例：center-region，count-lines-region，kill-region和print-region。

Emacs里函数工作时经常移动point尽管用户感觉不到这一点。例如：count-lines-region。为防止用户的point被移动到非预期的位置（相对于执行函数之前），save-excursion常用于保存point的位置，使用save-excursion是一个好的习惯。

不论代码运行是否成功（非正常结束），save-execursion总是恢复point和mark的位置。

另外，save-excursion也将记录当前所在的缓冲区，并恢复它。这意味着可以在代码中修改当前缓冲区，结果后save-excursion将切换回原来的缓冲区。

### save-excursion语句模板
```emacs-lisp
(save-excursion
  body...)
```
更详细一些的模板：
```emacs-lisp
(save-excursion
  first-expression-in-body
  second-expression-in-body
  third-expression-in-body
   ...
  last-expression-in-body)
```
在Emacs Lisp代码中，save-excursion语句通常放在let语句中：
```emacs-lisp
(let varlist
  (save-excursion
    body...))
```

## 回顾
部分函数

 - eval-last-sexp

对当前poing前的表达式求值。通常被绑定到C-x C-e上。

 - defun

定义函数。这个表(form)有5个部分：名称、参数定义、文档字符串、可选的交互式描述，函数体定义。例：
```emacs-lisp
(defun back-to-indentation ()
  "Move point to first visible character on line."
  (interactive)
  (beginning-of-line 1)
  (skip-chars-forward " \t"))
```

 - interactive

告诉解释器函数可以交互。跟在字符串后的特殊的表（form）可以作为参数传递给函数。多个部分之间用\n分隔。常用的字符代码如下：
b | 一个buffer的名称
f | 一个文件名
p | 数字前缀（按C-u时输入的数字，默认为4）
r | 传递poing和mark两个数字参数，小的数字在前。这是唯一一个传递两个参数的字符代码。

 - let

申明并初始化作用于let函数体的局部变量，变量值可以为nil。在let内部，Lisp解释器对外部的同名变量不可见。例：
```emacs-lisp
(let ((foo (buffer-name))
      (bar (buffer-size)))
  (message
   "This buffer is %s and has %d characters."
   foo bar))
```

 - save-excursion

记录当前point、mark和当前所在缓冲区，在函数体执行完后恢复这些值。例：
```emacs-lisp
(message "We are %d characters into this buffer."
         (- (point)
            (save-excursion
              (goto-char (point-min)) (point))))

```

 - if

对第一个参数求值；如果返回的为true，则对第二个参数求值；否则如果第三个参数存在，则对第三个参数求值。if被称作条件语句。Emacs Lisp也有其它的条件语句，但if是最常用的。例：
```emacs-lisp
(if (string-equal
     (number-to-string 21)
     (substring (emacs-version) 10 12))
    (message "This is version 21 Emacs")
  (message "This is not version 21 Emacs"))
```

 - equal

 - eq

检查两个对象是否相同。equal检测是否”相同（same）“，如果两个对象有相似的结构和内容就返回true。eq则需要两个参数指向同一个对象才返回true。

 - <

 - >

 - <=

 - >=

上面的比较函数的参数都必须是数字或者mark（C-<SPC>产生的）。

 - string<

 - string-lessp

 - string=

 - string-equal

string-lessp函数检测第一个参数是否小于第二个参数。string<是它的简写。传递给string-lessp的参数必须是字符串或者符号（symbols）。空字符串""小于任何其它字符串。

string-equal用于检查字符串的一致性。string=是它的简写。没有针对字符串>、>=或`<=`的函数定义。

 - message

在回显区显示消息。第一个参数是一个字符串，它可以包含%s，%d或%c这些占位符。%s必须对应于字符串或符号。%d对应于整数。%c必须是一个ascii编码数字。

 - setq

 - set

setq函数设置第一个变量的值为第二个变量。第一个变量自动被加上单引号。setq可以同时对多个变量赋值。set只能给带两个参数。

 - buffer-name

不需要参数，返回缓冲区的名字。

 - buffer-file-name

不需要参数，返回缓冲区所对应的文件名。

 - current-buffer

返回当前活动的缓冲区；它可以不是当前屏幕上显示的缓冲区（编程时使用）。

 - other-buffer

返回最近访问过的访问区。

 - switch-to-buffer

选择一个缓冲区显示到当前用户窗口。磁盘被绑定到C-x b。

 - set-buffer

在程序运行时切换Emacs的焦点到某个缓冲区。并不会改变当前窗口中显示的内容。

 - buffer-size

返回当前缓冲区的字符数。

 - point

返回当前光标所在位置，返回值是从缓冲区开始处到光标位置的字符数。

 - point-min

返回当前缓冲区的开始位置。默认为1。

 - point-max

返回当前缓冲区的结束位置。

# 部分与缓冲区有关的函数

## 查找更多信息
可以通过C-h f查看函数的说明，C-h v查看变量的说明，这些说明就是Emacs Lisp代码中的文档字符串。

在20或更高版本以后，可以用describe-function（C-h f）将告诉你函数定义的位置。在文件名上按回车（这个操作是help-follow函数调用）将打开函数定义。

etags：在代码中如果想要查看函数源文件，可以使用find-tags函数跳转到源文件上去。find-tags可以处理多种语法，不限于Lisp和C，也可以工作于非编程语言如Texinfo文档。在Texinfo文档里调用find-tags将跳转到对应的文件节点。

find-tags函数依赖于标签表'tags tables'，它记录了函数、变量和其它信息的位置。

使用M-.调用find-tags函数，然后在提示符后要查找的函数名，比如mark-whole-buffer。Emacs将转到显示该函数源码缓冲区。

符号表'tags table'通常是一个名为TAGS的文件。Emacs源码的TAGS存储在/usr/local/share/emacs目录中。但可以通过M-x visit-tags-table命令指定一个符号表。

通过etags命令可以创建符号表。使用M-x cd命令或C-x d（dired）切换到要建立符号表的目录，然后运行编译命令执行`etags *.el`命令。例：

```emacs-lisp
M-x compile RET etags *.el RET
```

文件中的代码通常称为库。通过C-h p可以查看Emacs Lisp的标准库。

## 简化版的beginning-of-buffer函数定义
beginning-of-buffer命令将把光标移动到缓冲区起始位置，并把mark设置在前一个位置。通常被绑定到M-<上。

简化版本的函数具有与标准库版本类似的功能，但不包含完整的功能。

设想一下该函数的定义应包括：包含能让用户交互的表达式，比如按M-x beginning-of-buffer或按键C-<；必须包含能在原位置设置mark的代码；必须包含让光标移动到缓冲区起始位置的代码。

简化版本的代码：
```emacs-lisp
(defun simplified-beginning-of-buffer ()
  "Move point to the beginning of the buffer;
leave mark at previous position."
  (interactive)
  (push-mark)
  (goto-char (point-min)))
```

与其它函数一样，这个函数也包含了defun需要的五个部分：
 1. 函数名，这里使用的：simplified-beginning-of-buffer。
 2. 参数列表：这里是一个空列表()。
 3. 文档字符串。
 4. 交互表达式。
 5. 函数体。

这个函数定义中，参数列表为空，意味着函数不需要任何参数。（查看完整函数定义时，我们可以看到它可能传递了可选的参数）。

interactive语句告诉Emacs函数允许交互。这个例子中interactive没有参数，因此调用simplified-beginning-of-buffer时也不需要参数。

函数体由两行代码组成：
```emacs-lisp
(push-mark)
(goto-char (point-min))
```
(push-mark)执行时将在当前光标所在位置设置mark，之前的mark被保存到mark ring上。

(goto-char (point-min))将光标转移到缓冲区起始位置。

在阅读这些代码遇到陌生的函数时，比如goto-char，可以使用describe-function命令，按C-h f然后输入函数名。describe-function将在一个*Help*窗口打印出函数的帮助文档。

调用describe-function时，如果光标停留在函数名上，describe-function默认将把光标所在位置的函数名作为参数。

end-of-buffer的函数定义与beginning-of-buffer类似，只是用(goto-char (point-max))替换(goto-char (point-min))。

## mark-whole-buffer的定义
mark-whole-buffer函数标把整个缓冲区标记为区域。把point设置在缓冲区开始位置，mark设置在缓冲区结束位置。通常被绑定到C-x h上。

### mark-whole-buffer预览
在Emacs 20中，完整的函数代码如下：
```emacs-lisp
(defun mark-whole-buffer ()
  "Put point at beginning and mark at end of buffer."
  (interactive)
  (push-mark (point))
  (push-mark (point-max))
  (goto-char (point-min)))
```
与函数定义模板类似：
```emacs-lisp
(defun name-of-function (argument-list)
  "documentation..."
  (interactive-expression...)
  body...)
```

### mark-whole-buffer的函数体
mark-whole-buffer的函数体仅有3行：
```emacs-lisp
(push-mark (point))
(push-mark (point-max))
(goto-char (point-min))
```
第一行(push-mark (point))与simplified-beginning-of-bufer函数相同，那里写的是(push-mark。两种写法都是告诉解释器在当前光标所在位置设置mark。

下一行(push-mark (point-max))在缓冲区结尾设置mark。设置这个mark后，前一行设置的mark将进入mark ring。这意味着你可以通过按两次C-u C-<SPC>重新回到那个位置。

在Emacs 21里，(push-mark (point-max))看起来更复杂：
```emacs-lisp
(push-mark (point-max) nil t)
```
这个函数增加了两上参数，第二个参数为nil。这告诉函数，在设置mark后，需要显示消息：'Mark set'。第三个参数t，它告诉push-mark如果当Transient Mark mode是开启状态，则应该将mark设置为活动状态。Transient Mark mode将高亮显示当前活动的区域，它默认是关闭的。

最后一行(goto-char (point-min))与beginning-of-buffer完全一样。这个语句将光标移动到缓冲区开始位置。运行的结果：point被设置到缓冲区开始位置，mark被设置为缓冲区结束位置。整个缓冲区被标记为区域（region）。

## append-to-buffer的定义
append-to-buffer函数从当前缓冲区中拷贝选中区域到指定的缓冲区中。
### append-to-buffer函数预览
append-to-buffer命令使用insert-buffer-substring函数来拷贝区域。insert-buffer-substring函数将缓冲区的一部分作为字符串（substring）插入到另一个缓冲区。完整的函数代码如下：
```emacs-lisp
(defun append-to-buffer (buffer start end)
  "Append to specified buffer the text of the region.
It is inserted into that buffer before its point.

When calling from a program, give three arguments:
a buffer or the name of one, and two character numbers
specifying the portion of the current buffer to be copied."
  (interactive "BAppend to buffer: \nr")
  (let ((oldbuf (current-buffer)))
    (save-excursion
      (set-buffer (get-buffer-create buffer))
      (insert-buffer-substring oldbuf start end))))
```

### append-to-buffer函数中的交互表达式
append-to-buffer函数需要与用户交互，因此函数使用了interactive表达式。
```emacs-lisp
(interactive "BAppend to buffer: \nr")
```
这个语句有一个双引号包含的字符串，该字符串被\n分隔为两部分。

第一部分BAppend to bufefer：这里的B告诉Emacs传递一个缓冲区给函数。Emacs将在回显区用B后面的字符串（Append to buffer:）提示用户输入缓冲区名称。然后Emacs将该缓冲区到参数buffer上。

\n分隔了交互表达式中的字符串。\n后的r告诉Emacs将point和mark的值分别绑定到参数buffer后面的两个参数上。

### append-to-buffer的函数体
函数体是以let开头的。定义了局部变量，在函数中let将(current-buffer)的返回值绑定到oldbuf上。这个变量用于跟踪当前工作的缓冲区。

单独来看let语句：
```emacs-lisp
(defun append-to-buffer (buffer start end)
  "documentation..."
  (interactive "BAppend to buffer: \nr")
  (let ((variable value))
        body...)
```

let语句包含三个元素：
 1. 符号let。
 2. 变量列表，列表中的元素是只含有两个元素的列表。
 3. let语句体。

### append-to-buffer中的save-excursion
let语句的body部分是一个save-excursion语句。它用于在执行完代码后恢复point，mark和buffer的值。

使用save-excursion函数处理过程与下面的模板类似：
```emacs-lisp
(save-excursion
  first-expression-in-body
  second-expression-in-body
   ...
  last-expression-in-body)
```

在函数定义中，save-excursion只包含了两个语句：
```emacs-lisp
(set-buffer (get-buffer-create buffer))
(insert-buffer-substring oldbuf start end)
```

save-excursion依次执行这两条语句，save-excursion函数执行的最后一条语句被作为该次函数调用的返回值。

save-excursion的body部分的第一条语句set-buffer函数用于改变当前缓冲区到append-to-buffer函数调用时第一个参数所指定的缓冲区。（set-buffer变不改当前屏幕显示的内容，只在Lisp程序内部改变当前处理的缓冲区）。第二条语句执行了函数的主要工作。

(get-buffer-create buffer)语句根据名称获取缓冲区，如果缓冲区不存在，就创建一个同名的缓冲区。这意味着可以用append-to-buffer将文本放到一个之前不存在的缓冲区上。

get-buffer-create也使set-buffer可以从错误中恢复：set-buffer需要一个缓冲区才能工作；如果传递给它的缓冲区不存在，Emacs将报错。get-buffer-create将在缓冲区不存在时创建一个，因此set-buffer将总能获取到一个缓冲区。

最后一行append-to-buffer执行追加文本的工作：
```emacs-lisp
(insert-buffer-substring oldbuf start end)
```
insert-buffer-substring函数从指定的缓冲区中拷贝字符串到当前缓冲区。在这里，传递给inset-buffer-substring的参数值是由let绑定的，并被命名为oldbuf，它是开始执行append-to-buffer时的当前缓冲区（执行命令时屏幕上显示的缓冲区）。

在insert-buffer-substring执行完后，save-excursion将恢复原缓冲区，append-to-buffer工作完成。

append-to-buffer的函数体工作骨架：
```emacs-lisp
(let (bind-oldbuf-to-value-of-current-buffer)
  (save-excursion                       ; Keep track of buffer.
    change-buffer
    insert-substring-from-oldbuf-into-buffer)

  change-back-to-original-buffer-when-finished
let-the-local-meaning-of-oldbuf-disappear-when-finished
```

总结append-to-buffer的工作方式：它保存当前缓冲区到变量oldbuf。获取或者新建一个缓冲区并让Emacs切换到那个缓冲区（非屏幕上显示的缓冲区）。使用oldbuf变量从旧缓冲区中获取文本区域插入到新缓冲区；然后使用save-excursion函数回到最初的缓冲区。

查看append-to-buffer代码，探究了复杂的函数。它展示了如何使用let和save-excursion，如何从另一个缓冲区回到原来的缓冲区。许多函数定义中以这种方式使用了let、save-excursion和set-buffer。

## 回顾
 - describe-function

 - describe-variable

打印函数或变量文档字符串。通常被绑定到C-h f和C-h v。

 - find-tag

查找包含函数或变量的源码，并在缓冲区打开，并定位到对应的位置。通常绑定到M-.上。

 - save-excursion

保存当前的point和mark，在传递给save-excursion的参数执行完后恢复这两个值。它也会记录下当前的缓冲区并重新回到这个缓冲区。

 - push-mark

在某个位置设置mark并将之前的mark保存到mark ring里面去。mark是缓冲区中的一个位置，不管缓冲区中的文本添加或者删除，它都将保持它的相对位置。

 - goto-char

设置point到参数指定的位置，参数可以是数字、mark或者返回位置数据的表达式，例如：(point-min).

 - insert-buffer-substring

从传递给它的第一个参数（缓冲区）对应的缓冲区拷贝区域中的文本到当前缓冲区。

 - mark-whole-buffer

把整个缓冲区标记为一个区域。通常绑定到C-x h上。

 - get-buffer-create

 - get-buffer

按名称查找缓冲区，如果缓冲区不存在就创建一个。get-buffer函数在查找不到缓冲区后将返回nil。

# 一些更复杂的函数
## copy-to-buffer的函数定义
这个函数拷贝文本到缓冲区，但它不是追加到第二个缓冲区，而是替换第二个缓冲区之前的文本。copy-to-buffer函数与append-to-buffer代码很类似，但它使用了erase-buffer和二个save-excursion。

该函数的函数体如下：
```emacs-lisp
...
(interactive "BCopy to buffer: \nr")
  (let ((oldbuf (current-buffer)))
    (save-excursion
      (set-buffer (get-buffer-create buffer))
      (erase-buffer)
      (save-excursion
        (insert-buffer-substring oldbuf start end)))))
```
代码与append-to-buffer类似：不同处在于，改变buffer后append-to-buffer添加文本到缓冲区；而copy-to-buffer函数先删除缓冲区的内容。在删除之前的缓冲区的内容后，第二次使用了save-excursion，并且插入了新的文本。

为什么需要执行save-excursion两次？

单独提取copy-to-buffer函数体如下：
```emacs-lisp
(let (bind-oldbuf-to-value-of-current-buffer)
  (save-excursion         ; First use of save-excursion.
    change-buffer
      (erase-buffer)
      (save-excursion     ; Second use of save-excursion.
        insert-substring-from-oldbuf-into-buffer)))
```

第一个save-excursion让Emacs返回被复制文本的缓冲区。很清楚，这与append-to-buffer函数中的使用是一致的。为什么要使用第二个save-excursion呢？原因在于insert-buffer-substring总是将point设置在被插入的区块（region）的结束位置。第二个save-excursion将使用Emacs将point设置在被插入区块的开始位置。多数情况下，用户喜欢看到point停留在被插入文本的开始位置。（copy-to-buffer函数将返回用户最初所在的缓冲区，当用户切换到拷贝的目标缓冲区时，point停留在缓冲区开始的位置）。

## insert-buffer的函数定义
与append-to-buffer和copy-to-buffer相反，这个命令拷贝另一个缓冲区到当前缓冲区。

## insert-buffer的代码
```emacs-lisp
(defun insert-buffer (buffer)
  "Insert after point the contents of BUFFER.
Puts mark after the inserted text.
BUFFER may be a buffer or a buffer name."
  (interactive "*bInsert buffer: ")
  (or (bufferp buffer)
      (setq buffer (get-buffer buffer)))
  (let (start end newmark)
    (save-excursion
      (save-excursion
        (set-buffer buffer)
        (setq start (point-min) end (point-max)))
      (insert-buffer-substring buffer start end)
      (setq newmark (point)))
    (push-mark newmark)))
```

### insert-buffer中的交互
insert-buffer中的interactive有两个部分，*号和bInsert buffer:
#### 只读缓冲区
星号用于只读缓冲区。如果insert-buffer是在一个只读缓冲区上被调用，提示信息将在回显区显示提示不允许插入到当前的缓冲区。星号不需要使用\n与下一个参数分隔。

#### 交互表达式b
交互表达式的第二个参数是小写b开头的（append-to-buffer中是大写的B）。小写b告诉Lisp解释器，insert-buffer需要一个已存在的缓冲区或者已存在的缓冲区名称作为参数。（大写的B可以使用一个不存在的缓冲区）Emacs将提示输入缓冲区名称，并提供了默认的缓冲区，输入时可以使用自动完成功能。如果缓冲区不存在，将给出"No match"的提示。

### insert-buffer函数体
insert-buffer函数有两个主要部分：or语句和let语句。or语句用于确保参数buffer参数不仅仅只是被绑定到缓冲区的名字上。let语句包含复制其它缓冲区到当前缓冲区的代码。
```emacs-lisp
(defun insert-buffer (buffer)
  "documentation..."
  (interactive "*bInsert buffer: ")
  (or ...
      ...
  (let (varlist)
      body-of-let... )
```
要明白or如何确保参数buffer不只是被绑定到缓冲区名称上，先要清楚or函数。

### 在insert-buffer用if替代or
主要工作在于确保buffer变量值是一个缓冲区，而不是缓冲区的名字。如果变量值是名字，则需要获取对对应的缓冲区。

通过if来实现：如果没有获取到buffer就获取它。

这里使用了bufferp函数，这个函数检查参数是否为一个缓冲区（或者缓冲区的名字），我们可以如下编码：
```emacs-lisp
(if (not (bufferp buffer))              ; if-part
    (setq buffer (get-buffer buffer)))  ; then-part
```
前面说过bufferp中的字符p是一个约定的函数描述，它意味着函数用于决定某些属性为true或false。这里bufferp就是用于检查参数是否为一个缓冲区。

not函数用于取逻辑值的反值。

当buffer参数不是一个缓冲区但它是一个缓冲区名称时，true-or-false-test返回true。这时(set q buffer (get-buffer buffer))被执行。语句使用get-buffer函数获取缓冲区名称所对应的缓冲区。setq将buffer绑定到缓冲区上。

### 函数体中的or
insert-buffer函数中使用or语句的目的在于确保buffer被绑定到缓冲区。上一节用if实现了这个功能。但在insert-buffer函数中实际使用的却是or函数。

or函数可以接收任何意数量的参数。它依次对每个参数求值并返回第一个结果不为nil的值。or并不会对第一个返回值不为nil的参数的后面的参数求值。

or语句如下：
```emacs-lisp
(or (bufferp buffer)
    (setq buffer (get-buffer buffer)))
```
该语句中or的第一个参数为(bufferp buffer)。如果buffer参数是一个缓冲区则返回true（一个非nil值）。在or语句中，这种情况下or将返回true，并且不执行后面的语句。

如果(bufferp buffer)返回值为nil，即buffer是一个缓冲区的名字，Lisp解释器将执行or语句的下一个元素：(setq buffer (get-buffer buffer))。这个语句将返回一个非nil值，这个值为绑定到buffer变量上的缓冲区而不是缓冲区的名字。

使用or的情况：
```emacs-lisp
(or (holding-on-to-guest) (find-and-take-arm-of-guest))
```

### insert-buffer中的let语句
确保了buffer变量绑定到缓冲区后，insert-buffer函数中接下来是一个let语句。它设置了3个局部变量start、end和newmark并初始化为nil。这些变量是let语句中的临时变量。

let语句体包含了两个save-excursion语句。内部的那个save-excursion如下：
```emacs-lisp
(save-excursion
  (set-buffer buffer)
  (setq start (point-min) end (point-max)))
```
(set-buffer buffer)将将当前缓冲区设置为将要复制文本的缓冲区。在那个缓冲区中将start和end分别设置为缓冲区开始位置和结束位置。这里可以看到setq可以在一个语句中设置多个变量。第一个参数值设置为第二个参数，第三个参数值为第四个参数。

外部的那个save-excursion表达式结构如下：
```emacs-lisp
(save-excursion
  (inner-save-excursion-expression
     (go-to-new-buffer-and-set-start-and-end)
  (insert-buffer-substring buffer start end)
  (setq newmark (point)))
```

insert-buffer-substring函数从原缓冲区中把start和end所定义的区域中的文本拷贝到buffer中。第二个缓冲区所有内容都处于start和end之间，因此整个缓冲区都将被拷贝到当前编辑的缓冲区中。这时，point位于被插入的文本的结束位置，被保存到newmark变量中。

在执行外部的save-excursion语句后，point和mark将回到原来的位置。

然而，合适的mark位置应该被设置在被插入的文本块的结束位置，而point应当被设置在这个文本块的开始位置。newmark记录了被插入文本的结束位置。let语句的最后一行(push-mark newmark)语句将mark设置到了那个位置。（前一个mark仍然可以访问，它被保存在mark ring里面，可以用C-u C-<SPC>回到那个位置）。同时，point被设置到被插入文本的开始位置，这也是函数调用前point所在的位置。

## 完整的beginning-of-buffer函数的定义
前面讨论过"简化版的beginning-of-buffer函数定义"。在那个版本中，调用的时候没有传递参数。Emacs中的beginning-of-buffer将光标移到缓冲区开始位置，并将mark设置在之前光标所在位置。调用的时候可以传递1-10之间的数字给这个命令，函数将把参数当作移动的百分比：整个缓冲区当作10份，C-u 7 M-<将跳转到整个缓冲区70%的位置。M-<将中跳转到缓冲区的开始位置。如果传递的参数大于10，则将移动到缓冲区的结束位置。

beginning-of-buffer的参数是可选的，可以不带参数调用。

### 可选参数
在调用需要参数的函数时，如果没有设置参数Lisp解释器将报错：Wrong number of arguments。

但Lisp提供了可选参数的功能：用&optional（&是这个关键字的一部分）关键字告诉解释器参数是可选的，如果参数跟在&optional的后面，则在调用函数时可以不传递这个参数

beginning-of-buffer函数定义的第一行：
```emacs-lisp
(defun beginning-of-buffer (&optional arg)
```
整个函数看起来如下：
```emacs-lisp
(defun beginning-of-buffer (&optional arg)
  "documentation..."
  (interactive "P")
  (push-mark)
  (goto-char
    (if-there-is-an-argument
        figure-out-where-to-go
      else-go-to
      (point-min))))
```

整个函数与simplified-beginning-of-buffer函数类似，除了interactive语句用了"P"参数和goto-char函数跟了一个用于在传递了参数时计算光标位置if-then-else语句。

"P" interactive语句告诉Emacs传递一个前缀参数，这个参数来自于按<META>键前输入的数字。或者输入C-u时输入的数字。(如果不输入数字，C-u缺省为4）

if语句部分比较简单：如果参数arg的值不为nil，即调用beginning-of-buffer时有带参数，则true-or-false-test返回true，if语句的then部分将被执行。如果beginning-of-buffer调用时没有带参数则if语句将被执行。else部分(goto-char (point-min))被执行。

### 带参数执行beginning-of-buffer
当带参数执行时，用于计算传递给goto-char的参数值的语句被执行。这个语句初看起来比较复杂。它内部包含了一个if语句和更多的数学计算。
```emacs-lisp
(if (> (buffer-size) 10000)
    ;; Avoid overflow for large buffer sizes!
    (* (prefix-numeric-value arg) (/ (buffer-size) 10))
  (/
   (+ 10
      (*
       (buffer-size) (prefix-numeric-value arg))) 10))
```

#### 解开beginning-of-buffer
解开上面的条件语句如下：
```emacs-lisp
(if (buffer-is-large
    divide-buffer-size-by-10-and-multiply-by-arg
  else-use-alternate-calculation
```
if语句检查缓冲区的大小。这样做主要是由于在由的Emacs 18版本中计算出来的数字不允许大于8百万，Emacs怕缓冲区太大，后面的计算结果超过上限而溢出。在Emacs 21中使用大数字，但这个代码没被改动。

#### 缓冲区很大时的情况
在beginning-of-buffer中，内部的if语句为了检查缓冲区是否大于1000个字符使用了>函数和buffer-size函数。
```emacs-lisp
(if (> (buffer-size) 10000)
```
如果超过了if语句的then部分将执行：
```emacs-lisp
(*
  (prefix-numeric-value arg)
  (/ (buffer-size) 10))
```
语句使用*函数将两个参数相乘。

第一个参数(prefix-number-value arg)。当使用"P"作为interactive时，传递给函数的参数值是一个"raw prefix argument"，不是一个数字（是一个包含了一个数字的列表）。为了执行数字运行，需要通过prefix-number-value来做转换。

第二个参数是(/ (buffer-size) 10)。这个语句将数值与十相除。这计算出了缓冲区中1/10有多少个字符。

在整个相乘的语句如下：
```emacs-lisp
(* numeric-value-of-prefix-arg
   number-of-characters-in-one-tenth-of-the-buffer)
```
如果传递的参数是7，计算出的位置就是缓冲区70%的位置。

缓冲区很大的时候，goto-char语句的情况：
```emacs-lisp
(goto-char (* (prefix-numeric-value arg)
              (/ (buffer-size) 10)))
```

#### 缓冲区较小时的情况
如果缓冲区包含的字符数量小于10000，计算上有些不同。也许你会认为这没有必要，因为第一个计算方式（大于10000时的情况）也能工作。然而在小型缓冲区中，第一种方法不能将光标放在需要位置；第二种方法则工作得好一些：
```emacs-lisp
(/ (+ 10 (* (buffer-size) (prefix-numeric-value arg))) 10))
```
格式化后看得更清楚一些：
```emacs-lisp
(/
   (+ 10
      (*
       (buffer-size)
       (prefix-numeric-value arg)))
   10))
```
看最内部的括号(prefix-numberic-value arg)，它将raw argument转换为数字。然后将数字与缓冲区大小相乘。
<src lang="emacs-lisp"
(* (buffer-size) (prefix-numeric-value arg)
```
这个操作将得到一个大于缓冲区几倍的数字。然后用这个数字加上10最后再除以10得到一个大于百分比位置的值。

这个结果被传递给goto-char将光标移到那个点。

### beginning-of-buffer的完整代码
```emacs-lisp
(defun beginning-of-buffer (&optional arg)
  "Move point to the beginning of the buffer;
leave mark at previous position.
With arg N, put point N/10 of the way
from the true beginning.
Don't use this in Lisp programs!
\(goto-char (point-min)) is faster
and does not set the mark."
  (interactive "P")
  (push-mark)
  (goto-char
   (if arg
       (if (> (buffer-size) 10000)
           ;; Avoid overflow for large buffer sizes!
           (* (prefix-numeric-value arg)
              (/ (buffer-size) 10))
         (/ (+ 10 (* (buffer-size)
                     (prefix-numeric-value arg)))
            10))
     (point-min)))
  (if arg (forward-line 1)))
```

代码中的文档字符串中使用了一个语句：
```emacs-lisp
\(goto-char (point-min))
```
语句第一个括号前的\告诉Lisp解释器应该打印这个表达式而不是对它求值。

beginning-of-buffer的最后一行代码：如果执行命令时带了参数，则移动point到下一行的起始位置。
```emacs-lisp
(if arg (forward-line 1)))
```
这行代码将光标移动到了计算位置的下一行的起始位置。(这行代码并非必要的，只是为了看起来更好）

## 回顾
 - or

依次执行各个参数直到遇到一个返回值不为nil的值。如果没有返回值为nil的参数，则返回nil，否则返回第一个返回值不为nil的值。简单来说就是：返回参数中第一个为true的值。

 - and

依次执行各个参数，直到遇到返回值为nil时，返回nil；如果没有nil则返回最后一个参数的值。简单来说就是：如果所有参数都为true就返回true；

 - &optional

这个关键字用于标明函数定义中的参数是可选的参数。意味着调用函数时可以不传递这个参数。

 - prefix-numeric-value

将从(interactive "P")获取到的"raw prefix argument'转换为数字。

 - forward-line

将point移到下一行的行首，如果参数大于1，则向下移动多行。如果不能移动那么多行，则forward-line尽量移动到能到达的位置，并返回没有进行操作的多余次数。

 - erase-buffer

删除当前整个缓冲区中的内容。

 - bufferp

如果参数是一个缓冲区，则返回t，否则返回nil。

# Narrowing and Widening
Narrowing是Emacs的一项功能，它使你可以将焦点集中在缓冲区的某个部分上，而不用担心意外的修改了其它部分。Narrowing通常被禁用，因为它可能会使新手觉得迷惑。

## Narrowing的优点
使用narrowing时，缓冲区的其它部分不可见，看起来就像其它部分不存在一样。利用这点你可以只在缓冲区中的某个部分进行查找或替换操作，而不会影响缓冲区的其它部分。narrow-to-region被绑定到C-x n n。

narrowing将使缓冲区的其它部分不可见，如果用户在无意中执行了narrowing命令时他们有可能会认为其它部分被删除了。而且，在这里用undo命令也不（C-x u）也不能关闭narrowing。这时可以使用widen（C-x n w）命令让其它部分重新显示出来。

Narrowing对于Lisp解释器或者用户都是很有用的。Emacs Lisp函数通常被设计为工作于缓冲区的一部分，或者工作于被narrow处理的整个缓冲区。比如：what-line函数（这个函数存在narrow时将显示两两个行号narrowing情况时的行数和非narrowing时的行数），从缓冲区中移除narrowing，工作完成后恢复narrowing。另一个函数count-lines，它被what-line调用，它使用narrowing将工作范围限定在需要处理的区域，在处理完成后再恢复。


## 特殊的save-restriction表(form)
在Emacs Lisp中，可以使用save-restriction保持对所有narrowing操作的跟踪。当Lisp解释器遇到save-restriction时，它执行save-restriction语句的body部分，然后撤消在body部分代码执行中的所有narrowing相关的操作。比如：缓冲区当前是narrowed状态，save-restriction中的代码删除了narrowing，save-restriction返回时将回到narrorwed的状态。在what-line命令中，所有的narrowing缓冲区都可能被save-restriction后面的widen命令撤消。所有原始的narrowing将在函数完成后被恢复。

使用save-restriction语句的简单模板如下：
```emacs-lisp
(save-restriction
  body... )
```

save-restriction函数的body部分是一个或多个将被依序执行的语句。

注意：同时使用save-excursion和save-restriction时，应该将save-excursion放在外部。如果放反了顺序，就有可能使Emacs在调用save-excursion后无法记录当前的narrowing信息。因此，这两个函数同时使用应该写成下面的结构：
```emacs-lisp
(save-excursion
  (save-restriction
    body...))
```

如果这两个函数不紧挨在一起，也必须按顺序使用：
```emacs-lisp
(save-restriction
    (widen)
    (save-excursion
    body...))
```

## what-line
what-line命令告诉你当前光标所在行的行号。这个命令个使用了save-restriction和save-excursion函数的例子。函数如下：
```emacs-lisp
(defun what-line ()
  "Print the current line number (in the buffer) of point."
  (interactive)
  (save-restriction
    (widen)
    (save-excursion
      (beginning-of-line)
      (message "Line %d"
               (1+ (count-lines 1 (point)))))))
```
这个函数有一个文档字符串和交互语句。接下来的两行使用了save-restriction和widen。

save-restriction将在其body部分的代码执行完后恢复narrowing。

save-restriction下面的widen撤消调用what-line时缓冲区中的所有narrowing（这些narrowing就save-restriction所记录的那些）。widen使得可以从缓冲区的开始位置计数。否则，它将只能对可访问区域进行计数。在save-restriction执行完成后将恢复原来的narrowing。

widen后面是save-excursion语句，它将保存当前光标位置（mark point等），在执行完成后恢复。在save-excursion的body部分使用了beginning-of-line函数移动poing。

注意：这里的widen语句在save-restriction和save-excursion之间。当同时使用时save-excursion应该在最外面。

what-line函数的最后两行用于统计缓冲区中的行数，并显示在回显区。
```emacs-lisp
(message "Line %d"
         (1+ (count-lines 1 (point)))))))
```
message函数在Emacs回显区显示了一行消息。第一个参数是一个双引号单间的字符串。字符串中可以包含%d，%s或%c来打印参数。%d用于打印数字。

所打印的数字%d是最后一行函数计算出来的：
```emacs-lisp
(1+ (count-lines 1 (point)))
```
它从缓冲区中的第一行统计，从1开始计数直到(poing)，并在这个数字上加1。（1+是一个自增加1的函数。）这里加1是因为在第2行的前面只有一行，count-lines计数时只计算到当前所在行的前一行。

在count-lines执行完后，将显示消息在回显区，save-excrusion恢复point和mark；save-restriction恢复原来的narrowing。

# 基础函数:car, cdr, cons
Lisp中car，cdr和cons都是基础函数。cons用于构造lists，car和cdr用于分割lisp。

## 奇怪的命名
cons函数的名称并非没有含意：它是单词'construct'的缩写。car是短语'Contents of the Address part of the Register'；cdr（'could-er'）是短语'Contents of the Decrement part of the Register'。这些短语说明了Lisp是在多么原始的机器上被开发的。

## car和cdr
一个list的CAR是list中的第一个元素。(rose violet daisy buttercup)的CAR就是rose。

执行下面的代码：
```emacs-lisp
(car '(rose violet daisy buttercup))
```
执行这个语句后，回显区将显示rose。

有一个更合理的car函数：first。

car并不从list移除第一个元素；它只返回第一个元素。car执行完后list并没有发生改变。car是一个无害的函数（'non-destructive'）。

CDR是list中的其余部分，cdr函数返回list中首元素后面的其它元素。因此'(rose violet daisy buttercup)的CDR部分是(violet daisy buttercup)。

对：
```emacs-lisp
(cdr '(rose violet daisy buttercup))
```
求值将在回显区显示(violet daisy butercup)

cdr也不从列表中移除元素。

附带说明一下：在这个例子中list前面加了单引号。如果不加，Lisp解释器把rose当作函数执行。在这个例子中我们并不需要那样。

cdr的一个更合理的名称是：rest。

当car和cdr应用于符号组成的列表时，比如(pine fir oak maple)，函数car将返回列表中的pine元素，并且pine不会被括号包含。这个list的CDR也是一个list，(fir oak maple)。

如果car和cdr应用于包含list的list，第一个元素也是list。car将返回list中的第一个list元素。

car和cdr是无害的，它们不修改list中的数据。这是非常重要的一点。

在第一章中曾说过：“在Lisp中某些原子类型，比如数组，可以被分隔成更小的部分；但这种机制与分割list的机制是不同的。这与Lisp的早期概念有关，list中的原子是不可分隔的。”（car和cdr也并不修改list。）car和cdr是用于分割list的基础函数。但它们不能用于分割数组或者访问数组中的一部分。数组被看作原子类型。另一个基础函数cons可以用于构造列表，但也不能用于数组。

## cons
cons函数是构造list的函数。例：
```emacs-lisp
(cons 'pine '(fir oak maple))
```
执行时回显区将显示(pine fir oak maple)。cons将新的元素放到列表的开头，它将新元素推入list中。

### 构造一个list
cons函数必须要有一个可以被插入的list参数。构造一个list时，至少要提供一个空的list。下面是一些构造list的语句：
```emacs-lisp
(cons 'buttercup ())
     ;=> (buttercup)

(cons 'daisy '(buttercup))
     ;=> (daisy buttercup)

(cons 'violet '(daisy buttercup))
     ;=> (violet daisy buttercup)

(cons 'rose '(violet daisy buttercup))
     ;=> (rose violet daisy buttercup)
```
在第一个例子中，()是一个空的list并且用空list和buttercup构造了一个list。可以看到空list并没有显示在被构造的list中。只能看到(buttercup)。空list不会被当作一个list元素，因为空list中没有任何元素。空list是不可见的。

### 检查list的长度：length
可以用函数length检查list中的元素数量：
```emacs-lisp
(length '(buttercup))
     ;=> 1

(length '(daisy buttercup))
     ;=> 2

(length (cons 'violet '(daisy buttercup)))
     ;=> 3
```

也可以将length应用于空list上：
```emacs-lisp
(length ())
     ;=> 0
```

当调用length函数而不传递参数给它时：
```emacs-lisp
(length)
```
你将得到一个错误信息：
```
Wrong number of arguments: #<subr length>, 0
```
这表示函数接收到了错误的参数个数，0，函数需要一定数量的参数。在这里length需要一个参数，参数应该是一个list。（一个list也是一个参数而不管list中有多少元素）

错误信息中的#<sub length>是函数的名称。#<subr，标明函数length是用C写的原生函数而不是用Emacs Lisp编写的。（subr是'subroutine'的缩写）

## nthcdr
nthcdr是一个与cdr相关的函数。它用于多次获取list的CDR部分。

如果获取(pine fir oak maple)的CDR部分，将得到(fir oak maple)。如果在这个结果上再重复操作将得到(oak maple)。（如果你在原来的list上取CDR，将一直得到同样的结果，因为原来的list并没有被修改）如果继续下去，将得到一个空的list，这时将不会显示为()，而是显示为nil。
例：
```emacs-lisp
(cdr '(pine fir oak maple))
     ;=>(fir oak maple)

(cdr '(fir oak maple))
     ;=> (oak maple)

(cdr '(oak maple))
     ;=>(maple)

(cdr '(maple))
     ;=> nil

(cdr 'nil)
     ;=> nil

(cdr ())
     ;=> nil
```

或者用下面的方式：
```emacs-lisp
(cdr (cdr '(pine fir oak maple)))
     ;=> (oak maple)
```

nthcdr函数与多次调用cdr类似。下面的例子中，参数2和一个list被传递给nthcdr，返回的值与原list相比，不含前面两个元素，相当于在list上执行了两次cdr。
```emacs-lisp
(nthcdr 2 '(pine fir oak maple))
     ;=> (oak maple)
```

```emacs-lisp
;; Leave the list as it was.
(nthcdr 0 '(pine fir oak maple))
     ;=> (pine fir oak maple)

;; Return a copy without the first element.
(nthcdr 1 '(pine fir oak maple))
     ;=> (fir oak maple)

;; Return a copy of the list without three elements.
(nthcdr 3 '(pine fir oak maple))
     ;=> (maple)

;; Return a copy lacking all four elements.
(nthcdr 4 '(pine fir oak maple))
     ;=> nil

;; Return a copy lacking all elements.
(nthcdr 5 '(pine fir oak maple))
     ;=> nil
```

## nth
nthcdr重复取list的CDR部分。nth函数取nthcdr返回值的CAR部分。它返回list中的Nth元素。

如果nth没有被因为效率原因而用C定义，那么nth的定义将会是下面的样子：
```emacs-lisp
(defun nth (n list)
  "Returns the Nth element of LIST.
N counts from zero.  If LIST is not that long, nil is returned."
  (car (nthcdr n list)))
```
（最初的nth在定义在Emacs Lisp文件subr.el中，但后来在1980年被重新用C实现。）

元素计数从0开始而不是1。这就是说list的第一个元素CAR是第零个元素。
```emacs-lisp
(nth 0 '("one" "two" "three"))
    ;=> "one"

(nth 1 '("one" "two" "three"))
    ;=> "two"
```

注意：nth与nthcdr和cdr一样，也不修改原来的list，也是一个无害函数。

## setcar
从命名上就可以猜想到，setcdr和setcar函数用于设置list的CAR或CDR部分为一个新值。与car和cdr不同，它们将修改原始的list。

例：
```emacs-lisp
(setq animals '(antelope giraffe lion tiger))

animals
     ;=> (antelope giraffe lion tiger)

(setcar animals 'hippopotamus)

animals
     ;=> (hippopotamus giraffe lion tiger)
```

可以看到setcar函数并非像cons那样向list中添加元素；它将giraffe替换为hippopotamus；它修改了list。

## setcdr
setcdr与setcar函数类似，它用于替换list中除首元素外的其它元素。

例：
```emacs-lisp
(setq domesticated-animals '(horse cow sheep goat))

domesticated-animals
     ;=> (horse cow sheep goat)

(setcdr domesticated-animals '(cat dog))

domesticated-animals
     ;=> (horse cat dog)

```

# 剪切和存储文本
当使用'kill'命令剪切文本时，Emacs将它存储到一个列表中，可以用'yank'命令重新获取到。

## 存储文本到列表
当文本被剪切出缓冲区时，它将被存储到一个list中。文本块连续的存储在list中，这个列表看如下面的形式：
<src lang="emacs-lisp"
("a piece of text" "previous piece")
```
函数cons可以添加文本块到list，如：
```emacs-lisp
(cons "another piece"
      '("a piece of text" "previous piece"))
```
执行上面的语句，回显区将显示
```emacs-lisp
("another piece" "a piece of text" "previous piece")
```
使用car和nthcdr函数，可以获取到list中任意的一个文本块。。例：
```emacs-lisp
(car (nthcdr 1 '("another piece"
                 "a piece of text"
                 "previous piece")))
     ;=> "a piece of text"
```

当然，Emacs中实际处理这些时更复杂一些。Emacs中编写的剪切函数能猜想出你需要的是list的哪个元素。

包含这些文本块的list被称作kill ring。

## zap-to-char
### 完整的zap-to-char实现
这个函数将移除光标和指定的字符之间的文本。被移除的文本被放入kill ring中，可以用C-y（yank）获取到。如果命令带了数字前缀参数n(C-u)，它将移除当前光标位置至遇到的第n个字符之间的文本。

如果指定的字符不存在，zap-to-char将显示"Search failed"。

为了决定要移除多少文本，zap-to-char使用了search函数。搜索在文本处理代码中使用得非常广泛。

下面是zap-to-char在Emacs 19中的完整代码：
```emacs-lisp
(defun zap-to-char (arg char)  ; version 19 implementation
  "Kill up to and including ARG'th occurrence of CHAR.
Goes backward if ARG is negative; error if CHAR not found."
  (interactive "*p\ncZap to char: ")
  (kill-region (point)
               (progn
                 (search-forward
                  (char-to-string char) nil nil arg)
                 (point)))
```

### interactive语句
zap-to-char的interactive语句如下：
```emacs-lisp
(interactive "*p\ncZap to char: ")
```
引号中的部分"*p\ncZap to char: "，指定了3个不同的东西。第一，星号，如果当前缓冲区是只读缓冲区将产生一个错误信息。这意味着如果将zap-to-char用于只读缓冲将得到错误信息"Buffer is read-only"。

在Emacs21的实现中没有包含星号。函数与Emacs19中一样能工作，但在只读缓冲区中它不会移除文本，它将复制文本并将文本放到kill ring中。在这种情况下，两个版本中都将显示错误信息。

在Emacs19中的实现也能从只读缓冲区中复制文本，这只是interactive的一个Bug。interactive的文档中说明了，星号将阻止zap-to-char函数对只读缓冲区做任何操作，这个函数不应该复制文本到kill ring中。

在Emacs21中interactive的实现是正确的。因此星号不得不被移除。如果你在这个这个函数的定义中插入了星号，并重新执行函数定义，下次你再在只读缓冲区上运行zap-to-char时，将不能再复制文本到kill ring里。

从这点来看，两个版本中的zap-to-char是一致的。

"`*p\ncZap to char: `"中的第二个部分是p。这个部分与下一部分用\n分隔了。p表示参数应该是一个前缀参数'processed prefix'，这个参数是用C-u加数字或者M-加数字传递的。如果调用时没有加参数，1将作为默认的参数值。

"`*p\ncZap to char: `"中的第三个部分是"cZap to char: "，小写的c指定了参数必须是一个字符。c后面的字符串Zap to char: 是提示字符串。

### zap-to-char的函数体
zap-to-char函数体包含kill当前光标位置至指定字符之间文本的代码。代码的第一部分如下：
```emacs-lisp
(kill-region (point) ...
```
(point)是光标的当前位置

代码的下一个部分是一个progn语句。progn的body部分由search-forward和point组成。

在学习完search-forward后，很容易懂progn。

### search-forward函数
search-forward函数被用于定位字符（zapped-for-character）。如果查找成功，search-forward会将point设置在要查找的目标字符串的最后一个字符的后面。（zap-to-char中目标字符串只有一个字符）如果是向后查找，则search-forward会将point设置在查找目标字符串第一个字符的前面。查找成功后，search-forward将返回t。

在zap-to-char中，search-forward函数部分如下：
```emacs-lisp
(search-forward (char-to-string char) nil nil arg)
```
search-forward函数包含四个参数：

 1. 第一个参数是要查询目标，必须是一个字符串，比如"z"。

传递给zap-to-char是一个字符。Lisp解释器对字符串和字符的处理是不同的。因为search-forward函数查询的是一个字符串，传递给zap-to-char函数接收到的是一个字符，因此参数必须被转换为字符串，否则search-forward将报错。char-to-string用于处理这种转换。

 2. 第二个参数限制查询的范围；它是一个缓冲区位置。在这里，可以查询到缓冲区的结束位置，因此第二个参数为nil。

 3. 第三个参数告诉函数如果查询失败该如何做：比如打印错误信息或者返回nil。第三个参数为nil将在查询失败时显示错误信息。

 4. search-forward的第四个参数用于指定重复查询的次数。这个参数是可选，如果没有传递，则默认为1.如果参数是一个负数，查询将向后查询。

使用search-forward语句的模板：
```emacs-lisp
(search-forward "target-string"
                limit-of-search
                what-to-do-if-search-fails
                repeat-count)
```

### progn
progn是一个特殊的form。它使传递给它的参数依次被执行，并返回最后一个值。前面部分只是被执行，它们的返回值被丢弃。

progn语句的模板：
```emacs-lisp
(progn
  body...)
```
zap-to-char中的progn语句做了两件事：将point设置到正确的位置；返回point的位置以便kill-region知道要操作的范围。

progn的第一个参数是search-forward。当search-forward找到了字符串，它会将point设置在查找目标字符串的最后一个字符的后面。（这里目标字符串只有一个字符长）如果是向后查找，search-forward会将poing设置在查找目标的第一个字符的前面。point的移动是side effect（单方面的，不影响界面）。

progn的第二个参数是表达式(point)。这个表达式返回point的值，即search-forward设置的那个值。这个值被作为progn语句的返回值将作为kill-region的第二个参数传递给kill-region函数。

### zap-to-char的总结
前面了解了search-forward和progn是如何工作的，我们可以看到整个zap-to-char函数是如何工作的。

kill-region的第一个参数是执行zap-to-char命令时的光标位置。在progn的内部，查找函数将poing移动到要查找目标（zapped-to-character）的后面。kill-region函数将这两个point中的第一个作为操作区域（region）的开始位置，第二个参数作为结束位置，然后移除这个区域。

progn是必需的，因为kill-region命令需要两个参数；如果把search-forward和point语句直接作为kill-region的参数将报错。progn语句是一个单独的参数，它的返回值将作为传递给kill-region的第二个参数。

## kill-region
zap-to-char函数使用了kill-region函数。函数将从一个region中clip文本到kill ring中。

在Emacs 21中这个函数使用了condition-case和copy-region-as-kill，这两个函数都将在后面解释，confition-case是一个特别重要的form。

实际上，kill-region函数调用了condition-case，它需要3个参数。第一个参数不做什么，第二个参数包含了正常工作时需要执行的代码。第三个参数包含了出错时需要执行的代码。

### 完整的kill-region定义
下面将介绍condition-case。首先来看kill-region的完整定义：
```emacs-lisp
(defun kill-region (beg end)
  "Kill between point and mark.
The text is deleted but saved in the kill ring."
  (interactive "r")

  ;; 1. `condition-case' takes three arguments.
  ;;    If the first argument is nil, as it is here,
  ;;    information about the error signal is not
  ;;    stored for use by another function.
  (condition-case nil

      ;; 2. The second argument to `condition-case'
      ;;    tells the Lisp interpreter what to do when all goes well.

      ;;    The `delete-and-extract-region' function usually does the
      ;;    work.  If the beginning and ending of the region are both
      ;;    the same, then the variable `string' will be empty, or nil
      (let ((string (delete-and-extract-region beg end)))

        ;; `when' is an `if' clause that cannot take an `else-part'.
        ;; Emacs normally sets the value of `last-command' to the
        ;; previous command.
        ;; `kill-append' concatenates the new string and the old.
        ;; `kill-new' inserts text into a new item in the kill ring.
        (when string
          (if (eq last-command 'kill-region)
              ;; if true, prepend string
              (kill-append string (< end beg))
            (kill-new string)))
        (setq this-command 'kill-region))

    ;; 3. The third argument to `condition-case' tells the interpreter
    ;;    what to do with an error.
    ;;    The third argument has a conditions part and a body part.
    ;;    If the conditions are met (in this case,
    ;;             if text or buffer is read-only)
    ;;    then the body is executed.
    ((buffer-read-only text-read-only) ;; this is the if-part
     ;; then...
     (copy-region-as-kill beg end)
     (if kill-read-only-ok            ;; usually this variable is nil
         (message "Read only text copied to kill ring")
       ;; or else, signal an error if the buffer is read-only;
       (barf-if-buffer-read-only)
       ;; and, in any case, signal that the text is read-only.
       (signal 'text-read-only (list (current-buffer)))))))
```

### condition-case
前面说过，当Emacs Lisp解释器在执行语句发生错误时，它将提供帮助信息，这被称为"signaling a error"。通常，程序将停止执行并显示错误信息。

然而在一些复杂的情况下。程序不应该在出错的时候只是简单的停止程序执行。在kill-region函数中，一个典型的错误是，如果在只读缓冲区中删除文本时，文本将不会被删除。因此kill-region函数包含了处理这种情况的代码。这些代码在kill-region函数中condition-case语句的内部。

condition-case的模板如下：
```emacs-lisp
(condition-case
  var
  bodyform
  error-handler...)
```
如果没有发生错误，解释器将执行bodyform语句。

错误发生时，函数将产生错误信息，定义一个或者多个错误条件名称（condition name）。

condition-case的第三个参数是一个错误处理器。一个错误处理器包含了两个部分，一个condition-name和一个body。如果错误处理器的condition-name与发生错误时的condition-name匹配，错误处理器的body部分将执行。

错误处理器中的错误条件名称（condition-name）可以是一个单一的condition name也可以是包含多个condition name的list。

condition-case语句可以包含一个或多个错误处理器。当错误发生时，第一个被匹配的处理器被执行。

最后，condition-case语句的第一个参数var，有时被绑定到包含错误信息的变量上。如果它为nil，比如在kill-region中，错误消息将被丢弃。

简单来说，在kill-region函数中，condition-case的工作如下：
```
If no errors, run only this code
    but, if errors, run this other code.
```

### delete-and-extract-region
一个condition-case语句有二个部分，一个是正常时执行的，但它有可能会产生错误。另一个部分用于出错时执行。

先来看kill-region中正常运行的代码：
```emacs-lisp
(let ((string (delete-and-extract-region beg end)))
  (when string
    (if (eq last-command 'kill-region)
        (kill-append string (< end beg))
      (kill-new string)))
  (setq this-command 'kill-region))
```
看起来比较复杂，使用了新的函数：delete-and-extract-region，kill-append和kill-new，和新的变量last-command和this-command。

delete-and-extract-region函数是一个内置函数，它删除region中的文本并返回这些文本。这个函数实际上是移除（removes）文本。（当不能移除时，它给出错误信号）

这里的let语句将delete-and-extract-region的返回值赋给局部变量string中。这也就是从缓冲区中删除的文本。

如果变量string指向了文本，那些文本就被添加到kill ring，如果变量值为nil则表示没有文本被删除。

这里使用了when来检查变量string是否指向了文本块。when语句是程序员的一种简便写法。when语句是没有else部分的if语句。可以把when理解为if。

技术上来说，when是一个Lisp宏。Lisp宏允许你定义新的控制结构和其它语言功能。它告诉解释器如何计算另一个Lisp语句的值，并返回计算的结果。这里的'另一个表达式'就是一个if表达式。C语言里也提供了宏。但这是不同的，但它们同样很有用。

如果string变量有内容，另一个条件表达式被执行。这是一个包含了then部分和else部分的if语句。
```emacs-lisp
(if (eq last-command 'kill-region)
    (kill-append string (< end beg))
  (kill-new string)))
```

如果前一个命令是kill-region，then部分被执行。如果不是，else部分将被执行。

last-command是一个Emacs变量。通常，当一个函数被执行，Emacs将设置last-command的值为前一个命令。

在这段定义中，if语句检查前一个命令是否为kill-region。

```emacs-lisp
(kill-append string (< end beg))
```
连续拷贝新文本到kill ring中前一个clipped的文本块中。如果(< end beg)表达式为true，kill-append添加文本到前一个被clipped的文本块中。

如果yank文本，比如'粘贴'，将一次得到整个文本块。用这种方式，你可以删除一行中的两个单词，然后使用一次yank操作，重新得到这两个单词，（(< end beg)语句保持单词的顺序是正确的）

如果前一个命令不是kill-region，kill-new函数将被执行，它将文本作为kill ring中的最后一个元素添加进去，然后将变量kill-ring-yank-pointer设置到上面。

## delete-and-extract-region
zap-to-char命令使用了delete-and-extract-region函数，它使用了另外两个函数，copy-region-as-kill和del_range_1。copy-region-as-kill函数将在下节讨论；它复制了region的一份拷贝到kill ring中，因此内容可以yanked回来。

delete-and-extract-region函数移除region中的内容且不能恢复。

与其它代码不同，delete-and-extract-region不是用Emacs Lisp编写的；它是用C编写的，这也是Emacs的一个基础系统。

与其它Emacs原生函数一样，delete-and-extract=region是C宏，宏是一个代码模板。完整宏如下：
```emacs-lisp
DEFUN ("delete-and-extract-region", Fdelete_and_extract_region,
       Sdelete_and_extract_region, 2, 2, 0,
  "Delete the text between START and END and return it.")
  (start, end)
     Lisp_Object start, end;
{
  validate_region (&start, &end);
  return del_range_1 (XINT (start), XINT (end), 1, 1);
}
```
DEFUN与Lisp中的defun是同样的用途。DEFUN后面括号中有七个部分：

 - 第一个部分给出了Lisp函数的名称，delete-and-extract-region

 - 第二部分是C函数的名称，Fdelete_and_extract_region。习惯上以F开头。因为C不能在函数名中使用连字符，因此用下划线替代了。

 - 第三个部分是记录了供函数内部使用的信息的C常量结构。它的名称与C函数名一致但它以S开头。

 - 第四和第五个部分指定了最小和最大的参数个数。这个函数需要2个参数。

 - 第六部分与Lisp编写的函数中的交互式语句类似：一个字符后跟着可选的提示信息。两者不同之处在于Lisp没有参数时不需要写参数。在这个宏里需要写成0（null string）。

 - 第七个部分是文档字符串与Lisp编写的函数中的相同。不同之处在于换行时，需要在\n后面添加一个反斜线并添加回车。

因此，goto-char的文档字符串的前两行如下：
```
        "Set point to POSITION, a number or marker.\n\
      Beginning of buffer is position (point-min), end is (point-max).
```

在C宏中，紧接在后面是正式的参数，和参数类型语句，接下来就是宏的'body'部分。delete-and-extract-region的'body'包含了两行：
```
validate_region (&start, &end);
return del_range_1 (XINT (start), XINT (end), 1, 1);
```
第一个函数validate_region检查传递的区域起始位置和结束位置是否是在规定的范围内，检查参数类型是否正确。第二个函数del_range_1，执行删除文本的操作。

del_range_1是一个复杂的函数我们不深入研究。它修改缓冲区并执行其它操作。

传递给del_range的两个参数XINT (start) and XINT (end)值得研究一下。

C语言中，start和end是标记了被删除区域的开始位置和结束位置的两个整数。

早期版本的Emacs中，这两个数字是32bits长，但这个代码运行比较慢。三个bit被用于指定类型信息，四个bit被用于处理内存；其它bits被作为'content'。

XINT是一个C宏它从bits集合中解析出相关的数字；4个bits被丢弃。

delete-and-extract-region命令看起来如下：
```emacs-lisp
del_range_1 (XINT (start), XINT (end), 1, 1);
```

它删除start和end之间的region。

从这点来看Emacs Lisp很简单；它隐藏了大量复杂的工作。

## 使用用defvar初始化变量
与delete-and-extract-region函数不同，copy-region-as-kill函数是用Emacs Lisp编写的。它内部有两个函数kill-append和kill-new，复制缓冲区区域中的信息到变量kill-ring中。这节讨论kill-ring变量是如何被defvar创建和初始化的。

在Emacs Lisp中kill-ring之类的变量是用defvar创建和初始化的。这个名称来源于"define variable"。

defvar与setq设置变量类似。与setq不同的两点：第一，它只给未赋值的变量赋值，如果变量已经有值，defvar将不会覆盖已经存在的值。第二，defvar有一个文档字符串。

（另一个特别的form是defcustom，被设计为可以让用户自定义。它比defvar有更多的功能。）

### 查看变量的当前值
可以使用describe-variable函数查看任何变量的当前值，通常可以用C-h v来调用。比如可以C-h v然后输入kill-ring将看到 当前kill ring的值，同时也能看到kill-ring的文档字符串：
```
Documentation:
List of killed text sequences.
Since the kill ring is supposed to interact nicely with cut-and-paste
facilities offered by window systems, use of this variable should
interact nicely with `interprogram-cut-function' and
`interprogram-paste-function'.  The functions `kill-new',
`kill-append', and `current-kill' are supposed to implement this
interaction; you may want to use them instead of manipulating the kill
ring directly.
```
kill ring是使用defvar按下面的方法定义的：
```emacs-lisp
(defvar kill-ring nil
  "List of killed text sequences.
...")
```
这个变量定义中，变量初始化为nil。这意味着如果没有保存任何东西，使用yank时将不会获取到任何信息。文档字符串的写法与使用defun时的文档字符串是一样的，文档字符串的第一行必须是一个完整的语句，因为一些命令，比如apropos只打印文档字符串的第一行。后面的行不应该使用缩进；否则如果用C-h v(describe-variable)查看时将会混乱。

### defvar时使用星号
以前，Emacs使用defvar来定义希望被用户修改的变量和不希望被用户修改的变量。尽管你可以用defvar定义自定义变量，但是请使用defcustom来代替。

当使用defvar设定变量时，可以在文档字符串的第一个位置添加*号来来区分变量是否为可以设值的变量。比如：
```emacs-lisp
(defvar shell-command-default-error-buffer nil
  "*Buffer name for `shell-command' ... error output.
... ")
```
这表示你可以使用edit-options命令临时修改shell-command-default-error-buffer的值。

edit-options设置的值只在当前编辑会话中有用。新值并不会被保存。每次Emacs启动时它将读取原始值，除非你在.emacs文件中设定它。

## copy-region-as-kill
这个函数从缓冲区中复制区域中的内容（使用kill-append或kill-new）并保存到kill-ring上。

如果在调用kill-region后立即调用copy-region-as-kill，Emacs会将新的文本追加到前一个复制的文本中。这意味着你使用yank时将得前面两次操作的所有文本。另一方面，如果在copy-region-as-kill之前执行了一些命令，则函数复制的文本块将不会放在一起。

### 完整的copy-region-as-kill函数定义
下面是Emacs 21中copy-region-as-kill函数定义：
```emacs-lisp
(defun copy-region-as-kill (beg end)
  "Save the region as if killed, but don't kill it.
In Transient Mark mode, deactivate the mark.
If `interprogram-cut-function' is non-nil, also save
the text for a window system cut and paste."
  (interactive "r")
  (if (eq last-command 'kill-region)
      (kill-append (buffer-substring beg end) (< end beg))
    (kill-new (buffer-substring beg end)))
  (if transient-mark-mode
      (setq deactivate-mark t))
  nil)
```

这个函数也可以拆分成多个部分：
```emacs-lisp
(defun copy-region-as-kill (argument-list)
  "documentation..."
  (interactive "r")
  body...)
```

参数是beg、end和参数为"r"的交互式函数，因此这两个参数将指向region的开始位置和结束位置。

一旦设置了一个mark，缓冲区就总会包含一个region。可以使用Transient Mark模式来高亮显示region。（没人会希望region一直处理于高亮状态，因此Transient Mark模式下只会在适当的时候才会高亮显示。许多人都关掉了Transient Mark模式，因此region从不会高亮显示）

copy-region-as-kill函数体是一个以if开头的子句。这个子句区分了两种情况：这个命令的前一个命令是否是kill-region命令。第一种情况，新的region被追加到前一个被复制的文本块中。否则，它将插入一个新的文本块到kill ring中。

### copy-region-as-kill的body部分
copy-region-as-kill函数和kill-function的工作很相似。两者都是为了将同一行中的两次或多次kill操作合并到同一个块中。如果用yank回来，将一次获得所有的文本块。并且，不管是向前删除还是向后删除，文本块都保持了正确的位置。

与kill-region相同，copy-region-as-kill函数也使用了last-command（它保持了对次Emacs命令调用的跟踪）变量。

#### last-command和this-command

通常，任何一个函数被执行，Emacs将在函数被挪时设置this-command为被执行的函数。同时，Emacs将last-command的值设置为this-command的前一个值。

在copy-region-as-kill函数的body部分，一个if语句检查了last-command的值是否为kill-region。如果是，则if语句被执行；它使用kill-append函数将本次函数调用复制的文本合并到kill ring的第一个元素（CAR）中。如果last-command不为kill-region，则copy-region-as-kill函数将使用kill-new函数在kill ring中添加一个新的元素。

这个if语句如下，它使用了eq函数：
```emacs-lisp
  (if (eq last-command 'kill-region)
      ;; then-part
      (kill-append (buffer-substring beg end) (< end beg))
    ;; else-part
    (kill-new (buffer-substring beg end)))
```
eq函数测试它的第二个参数与第一个参数是否为相同的Lisp对象。eq函数与用于测试相等的equal函数类似，不同之处在于：eq测试两个对象是否为指向同一个对象，而equal则检查两个参数的结构和同容是否相同。

如果前一个命令是kill-region，则Emacs Lisp解释器将调用kill-append函数。

#### kill-append函数
kill-append函数如下：
```emacs-lisp
(defun kill-append (string before-p)
  "Append STRING to the end of the latest kill in the kill ring.
If BEFORE-P is non-nil, prepend STRING to the kill.
If `interprogram-cut-function' is set, pass the resulting kill to
it."
  (kill-new (if before-p
                (concat string (car kill-ring))
              (concat (car kill-ring) string))
            t))
```
kill-append函数使用了kill-new函数。

首先来看传递给kill-new的参数。它使用了concat连接新文本和kill ring的CAR。是合并到CAR元素的前面还是合并到CAR元素后面取决于if语句：
```emacs-lisp
(if before-p                            ; if-part
    (concat string (car kill-ring))     ; then-part
  (concat (car kill-ring) string))      ; else-part
```
如果被kill的region位于前一个命令kill的region的前面，那么它将被合并到前一次删除的资源的前面，如果被删除的文本在前次删除文本的后面，那它将被合并到前次删除资源的后面。if语句使用before-p决定如何放置。

符号before-p是kill-append的参数。当kill-append被执行时，它被绑定到实际参数计算出来的值上。在这里是表达式(< end beg)。这个表达式并不能直接决定被删除的文本应该放在上个命令删除的文本的前面还是后面，它决定的是end是否小于beg。意味着用户是向前删除还是向后删除。如果(< end beg)则文本应该加有前一次文本的前面，否则文本应该加在前次文本的后面。

新文本加到前面时，执行：
```emacs-lisp
(concat string (car kill-ring))
```
新文本加到后面时，执行：
```emacs-lisp
(concat (car kill-ring) string))
```
我们可以意识到kill-append修改了kill ring。kill ring是一个list，它的每个元素保存了文本。kill-append函数使用kill-new函数，kill-new函数使用了setcar函数。

#### kill-new函数
```emacs-lisp
(defun kill-new (string &optional replace)
  "Make STRING the latest kill in the kill ring.
Set the kill-ring-yank pointer to point to it.
If `interprogram-cut-function' is non-nil, apply it to STRING.
Optional second argument REPLACE non-nil means that STRING will replace
the front of the kill ring, rather than being added to the list."
  (and (fboundp 'menu-bar-update-yank-menu)
       (menu-bar-update-yank-menu string (and replace (car kill-ring))))
  (if (and replace kill-ring)
      (setcar kill-ring string)
    (setq kill-ring (cons string kill-ring))
    (if (> (length kill-ring) kill-ring-max)
        (setcdr (nthcdr (1- kill-ring-max) kill-ring) nil)))
  (setq kill-ring-yank-pointer kill-ring)
  (if interprogram-cut-function
      (funcall interprogram-cut-function string (not replace))))
```

先看下面的部分：
```emacs-lisp
  (if (and replace kill-ring)
      ;; then
      (setcar kill-ring string)
    ;; else
    (setq kill-ring (cons string kill-ring))
    (if (> (length kill-ring) kill-ring-max)
        ;; avoid overly long kill ring
        (setcdr (nthcdr (1- kill-ring-max) kill-ring) nil)))
  (setq kill-ring-yank-pointer kill-ring)
  (if interprogram-cut-function
      (funcall interprogram-cut-function string (not replace))))
```

条件测试(and replace kill-ring)，如果两个kill ring中有内容，并且replace变量为true则返回true。

kill-append函数将replace设置为true；然后当kill ring至少有一个元素时，setcar语句被执行：
```emacs-lisp
(setcar kill-ring string)
```
setcar函数将kill-ring的第一个元素修改为string的值。它替换了原来的元素。

如果kill ring为空，或者replace为false，则条件语句的else部分将执行：
```emacs-lisp
(setq kill-ring (cons string kill-ring))
(if (> (length kill-ring) kill-ring-max)
    (setcdr (nthcdr (1- kill-ring-max) kill-ring) nil))
```
语句先通过在原来的kill ring前添加新元素string，而构造了一个新的kill ring。然后执行了第二个if子句。第二个if子名防止了kill ring增长过大。

依次来看这两个语句。

setq的这行将string添加到旧的kill ring组成的新list重新设置给kill-ring。

第二个if子名，防止了kill ring增长得过长。
```emacs-lisp
(if (> (length kill-ring) kill-ring-max)
    (setcdr (nthcdr (1- kill-ring-max) kill-ring) nil))
```
这段代码检查kill ring的长度是否已经超过了允许的最大长度——kill-ring-max（默认为60）。如果kill ring过长，则将kill ring的最后一个元素设置为nil。执行这个操作使用了两个函数：nthcdr和setcdr。

setcdr设置list的CDR部分，setcar设置list的CAR部分。在这里，setcdr不会设置kill ring的CDR部分；nthcdr函数限制了设置CDR的位置。

例：
```emacs-lisp
(setq trees '(maple oak pine birch))
     ;=> (maple oak pine birch)

(setcdr (nthcdr 2 trees) nil)
     ;=> nil

trees
     ;=> (maple oak pine)
```

setcdr返回值为nil，是因为它设置的CDR是nil。

kill-new函数中的下一行语句是：
```emacs-lisp
(setq kill-ring-yank-pointer kill-ring)
```
kill-ring-yank-pointer也是一个全局变量，它被设置为kill-ring。

尽管kill-ring-yank-pointer被称为pointer，实际上却是kill ring变量。但选用名字是为了帮助人们懂得这个变量起的作用。这个变量用于yank和yank-pop等函数。

现在，回到函数的最前面的两行：
```emacs-lisp
  (and (fboundp 'menu-bar-update-yank-menu)
       (menu-bar-update-yank-menu string (and replace (car kill-ring))))
```
这个语句第一个元素是函数and。

and将依次对每个参数求值只到某个参数返回值为nil，这种情况下and语句将返回nil；如果没有参数返回值为nil，返回值将是最后一个参数的值。（这种情况下返回值不会为nil，在Emacs Lisp里可以作为true）。换言之，and语句只有在所有参数都返回true的情况下才返回true。

在这里，语句测试了menu-bar-update-yank-menu是否是一个函数，如果是则调用它。如果测试的参数符号是一个函数定义而不是'is not void'，则fboundp返回true，如果函数未定义则我们将得到错误信息。

这个and和if语句效果如下：
```emacs-lisp
if the-menu-bar-function-exists
  then execute-it
```

menu-bar-update-yank-menu函数允许用户使用'Select and Paste'菜单操作，并且可以在菜单上看到文本块。

最后一个语句kill-new函数添加新的文本到窗口系统中，以便在不同的程序中进行复制粘贴操作。比如：在XWindow系统中x-select-text函数将文本存储在X系统操作的内存中，你可以在另一个程序中粘贴。

语句结构如下：
```emacs-lisp
  (if interprogram-cut-function
      (funcall interprogram-cut-function string (not replace))))
```

如果interprogram-cut-function存在，则Emacs执行funcall，它将第一个参数作为函数，并将其它参数传递给这个函数。

## 回顾
 - car

 - cdr

car返回list的第一个元素；cdr返回list中从第二个元素开始的list。

例：
```emacs-lisp
(car '(1 2 3 4 5 6 7))
     ;=> 1
(cdr '(1 2 3 4 5 6 7))
     ;=> (2 3 4 5 6 7)
```

 - cons

cons将第一个参数添加到第二个参数前面。

例：
```emacs-lisp
(cons 1 '(2 3 4))
     ;=> (1 2 3 4)
```

 - nthcdr

返回对list求'n'次CDR的值。

例：
```emacs-lisp
(nthcdr 3 '(1 2 3 4 5 6 7))
     ;=> (4 5 6 7)
```

 - setcar

 - setcdr

setcar修改list中的第一个元素；setcdr修改list中第二个元素开始的list。

例：
```emacs-lisp
(setq triple '(1 2 3))

(setcar triple '37)

triple
     ;=> (37 2 3)

(setcdr triple '("foo" "bar"))

triple
     ;=> (37 "foo" "bar")
```

 - progn

依次执行各个参数并返回最后一个参数的值。

例：
```emacs-lisp
(progn 1 2 3 4)
     ;=> 4
```

 - save-restriction

记录当前缓冲区的任何narrowing，在执行完它的参数后，恢复narrowing。

 - search-forward

查找字符串，如果找到则将point设置到那个位置。

它接收4个参数：

  1. 要查找的字符串

  2. 可选参数，是一个缓冲区位置，它用于限制查询范围

  3. 可选参数，查询失败执行的代码，返回nil或者显示错误信息

  4. 查询的次数，如果为负数则向前查找

 - kill-region

 - delete-region

 - copy-region-as-kill

  1. kill-region剪切point和mark间的文本到kill ring上，可以用yanking恢复。

  2. delete-and-extract-region移除point和mark间的文本并丢弃。不能恢复。

  3. copy-region-as-kill复制point和mark间的文本到kill ring，可以用yanking恢复。这个函数并不移除原来的文本。

# List的实现
Lisp中list使用了连续的指针对来保存数据，指针对的第一个指针指向一个原子或者另一个list，指针对的第二个指针指向另一个指针对，或者指向nil，以表明list的结束。

## List图示
举例来说，list(rose violet buttercup)有3个元素，rose，violet和buttercup。在计算机中，rose的地址被保存在计算机内存中，通过这个地址可以知道原子violet被分配在了哪个位置；通过这个地址又可以知道原子buttercup的地址。

听起来比较复杂，看图就简单多了：
```
    ___ ___      ___ ___      ___ ___
   |___|___|--> |___|___|--> |___|___|--> nil
     |            |            |
     |            |            |
      --> rose     --> violet   --> buttercup

```
这个图中，每个方框代表一个保存了Lisp对象的内存块，这通常是一个内存地址。在方框中的地址是成对的。每个箭头指向了这个地址的内容，它可能是一个原子也可能是另一个地址对。第一个方框是rose的地址；第二个方框保存了下一个方框对的地址，这个地址的第一个部分指向violet第二个部分指向下一个方框对。最后一个方框指向符号nil，标明list的结束。

当执行一个设置函数时比如setq，它将第一个方框的地址保存到变量中。比如：
```emacs-lisp
(setq bouquet '(rose violet buttercup))
```
产生的情况如下：
```
bouquet
     |
     |     ___ ___      ___ ___      ___ ___
      --> |___|___|--> |___|___|--> |___|___|--> nil
            |            |            |
            |            |            |
             --> rose     --> violet   --> buttercup

```
在这个例子中符号bouquet保存了第一个方框对的地址。

同样，list也可以被成有序的方框：
```
bouquet
 |
 |    --------------       ---------------       ----------------
 |   | car   | cdr  |     | car    | cdr  |     | car     | cdr  |
  -->| rose  |   o------->| violet |   o------->| butter- |  nil |
     |       |      |     |        |      |     | cup     |      |
      --------------       ---------------       ----------------

```
（符号是由地址组成的。实际上bouquet包含了一组地址，一个地址指向可打印的单词bouquet，第二个是地址绑定到该符号上的函数定义（如果存在），第三个地址是list(rose violet buttercup)的第一个地址对的地址，等等。这里只显示了第三个地址的情况。）

如果符号指向list的CDR部分，这个list本身不会改变；符号将拥有从那个位置开始的list。（CAR和CDR是'non-destructive'的）因此执行下面的语句：
```emacs-lisp
(setq flowers (cdr bouquet))
```
将产生下面的结果：
```
bouquet        flowers
  |              |
  |     ___ ___  |     ___ ___      ___ ___
   --> |   |   |  --> |   |   |    |   |   |
       |___|___|----> |___|___|--> |___|___|--> nil
         |              |            |
         |              |            |
          --> rose       --> violet   --> buttercup

```

flowers的值是(violet buttercup)，这就是说符号flowers拥有了一个地址对的地址。

这种地址对被称为cons cell或者dotted pair。

函数cons添加一个新的地址对到一连串地址对的前面。例如，执行下面的语句：
```emacs-lisp
(setq bouquet (cons 'lily bouquet))
```
产生的效果如下：
```
bouquet                       flowers
  |                             |
  |     ___ ___        ___ ___  |     ___ ___       ___ ___
   --> |   |   |      |   |   |  --> |   |   |     |   |   |
       |___|___|----> |___|___|----> |___|___|---->|___|___|--> nil
         |              |              |             |
         |              |              |             |
          --> lily      --> rose       --> violet    --> buttercup

```
而这并不会改变flowers的值，你可以看到：
```emacs-lisp
(eq (cdr (cdr bouquet)) flowers)
```
将返回t。

到现在为止，flowers的值仍是(violet buttercup)；它拥有violet的cons cell地址。这也不会改变任何之前的cons cells；他们仍然在那里。

就这样，在Lisp里获取list的CDR，将获取到连续的cons cell串中的第二个；获取list的CAR，将得到第一个。将cons将一个新元素连接到list上，你将会把新元素的cons cell添加到list的前面。

cons cell串的最后一个指向什么？它指向空list，nil。

## 把符号看作抽屉柜
前面章节曾提示过把符号（symbol）想像成抽屉柜。函数定义放到一个抽屉里，变量放到了另一个，等等。

实际上放在各个抽屉里的是值或函数定义的地址。

（另外，符号有一个抽屉存放属性列表（property list），它用于记录其它信息。）
```
            Chest of Drawers            Contents of Drawers

            __   o0O0o   __
          /                 \
         ---------------------
        |    directions to    |            [map to]
        |     symbol name     |             bouquet
        |                     |
        +---------------------+
        |    directions to    |
        |  symbol definition  |             [none]
        |                     |
        +---------------------+
        |    directions to    |            [map to]
        |    variable value   |             (rose violet buttercup)
        |                     |
        +---------------------+
        |    directions to    |
        |    property list    |             [not described here]
        |                     |
        +---------------------+
        |/                   \|

```

# Yanking Text Back
当使用'kill'命令剪切文本时，可以用'yank'命令恢复它。被剪切的文本被放到kill ring，yank命令可以将文本恢复。

C-y（yank）命令插入kill ring中的第一个元素到缓冲区。如果C-y命令后立即跟一个M-y，则插入的文本将被替换为kill ring的第二个元素。连续的按M-y，将使用kill ring中更靠后的文本替换前一次操作插入的文本。当到达最后一个元素时，又将从第一个元素开始。（这也是kill ring被称作ring而不是list的原因）然而实际上保存了文本的数据结构是list。

## Kill Ring Overview
kill ring是被删除字符串的列表。例如：
```emacs-lisp
("some text" "a different piece of text" "yet more text")
```
按C-y字符串some text将插入当前缓冲区的光标位置。

yank命令也可以用于复制文本。复制文本而不从缓冲区剪切文本，文本被复制一份放到kill ring中。

有三个函数可以将文本从kill ring上恢复：yank，通常被绑定在C-y上；yank-pop，通常绑定在M-y；rotate-yank-pointer它使用了另外两个函数。

这些函数通过变量kill-ring-yank-pointer指向kill ring。实际上yank和yank-pop插入文本的代码都是：
```emacs-lisp
(insert (car kill-ring-yank-pointer))
```
为了弄清楚yank和yank-pop是如何工作的，先需要了解kill-ring-yank-pointer变量和rotate-yank-pointer函数。

## 变量kill-ring-yank-pointer
kill-ring-yank-pointer是与kill-ring类似的变量。

如果kill ring的内容如下：
```emacs-lisp
("some text" "a different piece of text" "yet more text")
```
kill-ring-yank-pointer将指向list第二个部分开始的list，kill-ring-yank-pointer是：
```emacs-lisp
("a different piece of text" "yet more text")
```
前面关于List实现的章节曾说过：计算机并不会为kill-ring和kill-ring-yank-pointer分别保存拷贝。两个Lisp变量指向同一片文本，下面是图示：
```
kill-ring     kill-ring-yank-pointer
    |               |
    |      ___ ___  |     ___ ___      ___ ___
     ---> |   |   |  --> |   |   |    |   |   |
          |___|___|----> |___|___|--> |___|___|--> nil
            |              |            |
            |              |            |
            |              |             --> "yet more text"
            |              |
            |               --> "a different piece of text
            |
             --> "some text"

```
变量kill-ring和kill-ring-yank-pointer都是指针。kill-ring常被称作列表而不是说指向列表，而kill-ring-yank-pointer被称为指向列表。

rotate-yank-pointer函数修改kill-ring-yank-pointer指向的元素；当指针指向元素的第二个元素为kill ring的结束位置时，它将自动指向kill ring的第一个元素。这也展示了如何将一个list转变为ring。rotate-yank-pointer函数虽然看起来不复杂，但它实际包含了很多细节。

# 循环和递归
Emacs Lisp有两种方式循环执行语句：使用while循环，或者使用递归。

## while
while测试它的第一个参数的值，如果为false，解释器将不会执行语句的body部分。如果为true，解释器将执行语句的body部分，然后重新测试第一个参数的值，开始下一轮循环。

while语句模板如下：
```emacs-lisp
(while true-or-false-test
  body...)
```

### 使用while循环
如果while语句的true-or-false返回为true则body部分被执行。

对while求值的返回值是true-or-false-test的值。有趣的是while循环执行时如果没有发生错误将返回nil或false，而不管循环执行了多少次。while语句执行成功也不会返回true。

### while循环和list
通常使用while循环来测试一个list是否包含了元素。如果有循环就执行，如果没有了循环就结束。这是一项重要的技术，下面将举例说明。

最简单的测试list是否有元素的方法是执行这个list：如果没有元素，则会返回空list，()，它与nil或false同义。如果有元素则将返回这些元素。因为Emacs Lisp把任何蜚nil值当作true，如果把有元素的list作为while的判断条件，将使循环执行。

例：
```emacs-lisp
(setq empty-list ())
```
对empty-list求值将返回nil。

```emacs-lisp
(setq animals '(gazelle giraffe lion tiger))
```
如果把animals作为while循环的条件，如：
```emacs-lisp
(while animals
       ...
```
当while检查它的第一个参数时，变量animals被执行，它将返回一个list。由于这个list不为nil，while将把这个值当作true。

为了防止while进入无限循环，需要一些机制来逐渐的清空list。一个常用的方法就是将传递给while语句的list替换为原来的list的CDR。每次都使用cdr函数，这样list将变短，最后list将变为空的list。这时while循环结束。

例如，上面的绑定到animals变量可以用下面的语句设置为原始list的CDR。
```emacs-lisp
(setq animals (cdr animals))
```

使用while和cdr函数的模板如下：
```emacs-lisp
(while test-whether-list-is-empty
  body...
  set-list-to-cdr-of-list)
```

### 例：print-elements-of-list
```emacs-lisp
(setq animals '(gazelle giraffe lion tiger))

(defun print-elements-of-list (list)
  "Print each element of LIST on a line of its own."
  (while list
    (print (car list))
    (setq list (cdr list))))

(print-elements-of-list animals)
```
执行上面的代码，回显区将显示：
```
giraffe

gazelle

lion

tiger
nil
```

### 在循环中使用自增计数器
模板：
```emacs-lisp
set-count-to-initial-value
(while (< count desired-number)         ; true-or-false-test
  body...
  (setq count (1+ count)))              ; incrementer
```

#### 自增计数的例子
计算三角型中星号的数量，参数为层数，比如四层的三角型：
```
               *
              * *
             * * *
            * * * *
```
函数定义如下：
```emacs-lisp
(defun triangle (number-of-rows)    ; Version with
                                    ;   incrementing counter.
  "Add up the number of pebbles in a triangle.
The first row has one pebble, the second row two pebbles,
the third row three pebbles, and so on.
The argument is NUMBER-OF-ROWS."
  (let ((total 0)
        (row-number 1))
    (while (<= row-number number-of-rows)
      (setq total (+ total row-number))
      (setq row-number (1+ row-number)))
    total))
```
使用：
```emacs-lisp
(triangle 4)

(triangle 7)
```
第一行的结果为10，第二行的结果为28。

### 在循环中使用自减计数器
模板：
```emacs-lisp
(while (> counter 0)                    ; true-or-false-test
  body...
  (setq counter (1- counter)))          ; decrementer
```

### 自减计数的例子
仍以上面的三角型为例，计算1到任意层的星号总数。

函数定义的第一版：
```emacs-lisp
;;; First subtractive version.
(defun triangle (number-of-rows)
  "Add up the number of pebbles in a triangle."
  (let ((total 0)
        (number-of-pebbles-in-row number-of-rows))
    (while (> number-of-pebbles-in-row 0)
      (setq total (+ total number-of-pebbles-in-row))
      (setq number-of-pebbles-in-row
            (1- number-of-pebbles-in-row)))
    total))
```
然而，我们并不需要number-of-pebbles-in-row。

当执行triangle函数时，符号number-of-rows将被绑定到初始的值上。这个数值可以在函数体内作为局部变量被修改，而不用担心会影响函数外部的值。这是Lisp中一个非常重要的特性；这意味着变量number-of-rows可以用于任何使用了number-of-pebbles-in-row的地方。

函数第二版如下：
```emacs-lisp
(defun triangle (number)                ; Second version.
  "Return sum of numbers 1 through NUMBER inclusive."
  (let ((total 0))
    (while (> number 0)
      (setq total (+ total number))
      (setq number (1- number)))
    total))
```

简单来说，正常情况下while循环包含三个部分：
 1. 在循环执行正确的次数后，while循环的判断语句将返回false。
 2. 被循环执行的语句，它将返回需要的值。
 3. 修改true-or-false-test返回值的语句，以便循环在执行正确的次数后停止。

## 使用dolist和dotimes节约时间
dolist和dotimes都是为循环提供的宏。在某些情况下比直接使用while循环简单一些。

dolist与在while中循环取list的CDR的方法类似，它在每次循环中自动取CDR截短list，并将截短后的list的CAR绑定到它的第一个参数上。

dotimes循环可以指定循环的次数。

### dolist宏
举例来说，如果你想将一个list倒序排列，可以用reverse函数，例如：
```emacs-lisp
(setq animals '(gazelle giraffe lion tiger))

(reverse animals)
```

这里演示了如何使用while循环实现倒序：
```emacs-lisp
(setq animals '(gazelle giraffe lion tiger))

(defun reverse-list-with-while (list)
  "Using while, reverse the order of LIST."
  (let (value)  ; make sure list starts empty
    (while list
      (setq value (cons (car list) value))
      (setq list (cdr list)))
    value))

(reverse-list-with-while animals)
```

也可以用dolist宏实现：
```emacs-lisp
(setq animals '(gazelle giraffe lion tiger))

(defun reverse-list-with-dolist (list)
  "Using dolist, reverse the order of LIST."
  (let (value)  ; make sure list starts empty
    (dolist (element list value)
      (setq value (cons element value)))))

(reverse-list-with-dolist animals)
```

在这个例子中，使用已存的reverse函数当然是最好的。第一个使用while循环的例子里。while先检查list是否有元素；如果有，它将list的第一个元素添加到另一个list（它的第一个元素是nil）的第一个位置。由于添加元素的顺序是反的，因此原来的list被倒序排列了。

在使用while循环的语句中，(setq list (cdr list))语句截短了list，因此while循环最后停止了。在循环体中用cons语句创建了一个新的list。

dolist语句与while语句类似，dolist宏自动完成了在while语句中所写的一些工作。

while循环与dolist实现的两个方法不同之处在于dolist自动截短了list。'CDRs down the list'。并且它自动将CAR截短了的list的CAR赋给dolist的第一个参数。

### dotimes宏
dotimes宏与dolist类似，但它可以指定循环次数。

dotimes的第一个参数是每次循环的计数器，第二个参数是循环次数，第三个参数是返回值。

举例来说，下例将number绑定到从0开始的数字，但不包含3，然后构造出一个包含3个数字的list。
```emacs-lisp
(let (value)      ; otherwise a value is a void variable
  (dotimes (number 3 value)
    (setq value (cons number value))))

;=> (2 1 0)
```

dotimes的返回值是value。

下面是一个使用defun和dotimes实现的triangle函数：
```emacs-lisp
(defun triangle-using-dotimes (number-of-rows)
  "Using dotimes, add up the number of pebbles in a triangle."
(let ((total 0))  ; otherwise a total is a void variable
  (dotimes (number number-of-rows total)
    (setq total (+ total (1+ number))))))

(triangle-using-dotimes 4)
```

## 递归
递归函数使用不同的参数来调用自身。尽管执行的代码是相同的，但它们不是在同一线程执行。（不是同一个实例）

### 递归的组成
一个递归函数通常包含下面三个部分：

1. 一个true-or-false-test决定是否再次调用函数，在这里被称为do-again-test。

2. 函数名称。当这个函数被调用时，一个新的函数实例产生了，并被分配任务。

3. 一个函数语句，它在每次执行时返回不同的值。这里称为next-step-expression。这样，传递到新的函数实例的参数前与传递给前一个函数实例的参数不同。这将使得在执行了正确有循环次数后，条件语句do-again-test的值为false。

使用递归函数的简单模式如下：
```emacs-lisp
(defun name-of-recursive-function (argument-list)
  "documentation..."
  (if do-again-test
    body...
    (name-of-recursive-function
         next-step-expression)))
```

递归函数每次执行时将产生一个新的函数实例，参数告诉了实例要做什么。一个参数被绑定到next-step-expression。每个实例执行时都有一个不同的next-step-expression。

next-step-expression的值被用于do-again-text。

next-step-expression的返回值被传递给新的函数实例，由它来决定是否停止或继续。next-step-expression被设计为在不需要循环后它能使do-again-test返回false。

do-again-test有时被称为停止条件（stop condition），因为它将在测试值为false时停止循环。

### 在list上使用递归
下面的例子使用了递归打印list中的各个元素。
```emacs-lisp
(setq animals '(gazelle giraffe lion tiger))

(defun print-elements-recursively (list)
  "Print each element of LIST on a line of its own.
Uses recursion."
  (if list                              ; do-again-test
      (progn
        (print (car list))              ; body
        (print-elements-recursively     ; recursive call
         (cdr list)))))                 ; next-step-expression

(print-elements-recursively animals)
```

### 用递归代替计数器
前面章节说过的triangle函数可以用递归修改为：
```emacs-lisp
(defun triangle-recursively (number)
  "Return the sum of the numbers 1 through NUMBER inclusive.
Uses recursion."
  (if (= number 1)                    ; do-again-test
      1                               ; then-part
    (+ number                         ; else-part
       (triangle-recursively          ; recursive call
        (1- number)))))               ; next-step-expression

(triangle-recursively 7)
```

### 在递归中使用cond
前一节中的triangle-recursively使用了if。它也可以使用cond，cond是conditional的缩写。

尽管cond不像if那样使用得很普遍，但它还是比较常见的。

使用cond的模板如下：
```emacs-lisp
(cond
 body...)
```
body部分是一连串的list。

更完整的模板如下：
```emacs-lisp
(cond
 (first-true-or-false-test first-consequent)
 (second-true-or-false-test second-consequent)
 (third-true-or-false-test third-consequent)
  ...)
```

当解释器执行cond语句时，它先执行body区的第一个语句的第一个元素。

如果true-or-false-test返回nil，则那个list的其它部分将不会执行。程序转到list串中的下一个list。当一个true-or-false-test的返回值不为nil，则那条语句的其它部分将会执行。如果list串包含多个list，则它们依次执行并返回最后一个语句的值被返回。

如果没有一个true-or-false-test的返回值为true，则cond语句返回nil。

使用cond实现的triangle函数：
```emacs-lisp
(defun triangle-using-cond (number)
  (cond ((<= number 0) 0)
        ((= number 1) 1)
        ((> number 1)
         (+ number (triangle-using-cond (1- number))))))
```

### 递归模式
下面是3个常用的递归模式。

#### every
在every模式的递归中，动作将在list的每个元素上执行。

基本模型如下：

 - 如果list为空，则返回nil。

 - 否则，在list的首元素（list的CAR）上执行动作。

  - 通过递归在list的其它部分（CDR）上执行相同的操作。

  - 这步是可选的使用cons将正在操作的元素和已经操作过的元素列表合并。

例如：
```emacs-lisp
(defun square-each (numbers-list)
  "Square each of a NUMBERS LIST, recursively."
  (if (not numbers-list)                ; do-again-test
      nil
    (cons
     (* (car numbers-list) (car numbers-list))
     (square-each (cdr numbers-list))))) ; next-step-expression

(square-each '(1 2 3))
    ;=> (1 4 9)
```
如果number-list为空，则什么也不做。如果它有内容，则通过递归构造一个list各个元素乘方值的list。

前面介绍过的print-elements-recursively函数，是另一个every模式的递归，不同的是这里使用了cons合并元素。

```emacs-lisp
(setq animals '(gazelle giraffe lion tiger))

(defun print-elements-recursively (list)
  "Print each element of LIST on a line of its own.
Uses recursion."
  (if list                              ; do-again-test
      (progn
        (print (car list))              ; body
        (print-elements-recursively     ; recursive call
         (cdr list)))))                 ; next-step-expression

(print-elements-recursively animals)
```
print-elements-recursively函数的处理流程：

 - 如果list为空，不执行操作。

 - 如果list含有至少一个元素，

  - 在list的首元素（CAR）上执行操作。

  - 通过递归调用在其它的元素上执行操作。


#### accumulate
accumulate递归模式，在每个元素上都执行动作，动作的执行结果与对下一个元素执行操作的结果进行累积。

这与在every模式中使用cons类似，只是不是使用cons，而是使用其它的方式合并。

工作模式如下：

 - 如果list为空，返回0或其它常量

 - 否则，在list的CAR上执行动作

  - 使用+或其它操作合并当前操作的元素和已经操作过的元素

  - 递归方式在list的其它部分执行

例如：
```emacs-lisp
(defun add-elements (numbers-list)
  "Add the elements of NUMBERS-LIST together."
  (if (not numbers-list)
      0
    (+ (car numbers-list) (add-elements (cdr numbers-list)))))

(add-elements '(1 2 3 4))
   ;=> 10
```

#### keep
在keep递归模式中，list中的每个元素被测试，如果被操作的元素符合要求或者对元素的计算结果符合要求则保存该元素。

这与every模式也很类似，只是在这里如果元素不符合要求则被忽略。

这种模式的三个部分：

 - 如果list为空，则返回nil

 - 如果list的CAR符合要求

  - 在元素上执行操作，并使用cons合并它

  - 递归调用处理list中的其它元素

 - 如果list的CAR不符合要求

  - 忽略这个元素

  - 递归调用处理list中的其它元素

例如：
```emacs-lisp
(defun keep-three-letter-words (word-list)
  "Keep three letter words in WORD-LIST."
  (cond
   ;; First do-again-test: stop-condition
   ((not word-list) nil)

   ;; Second do-again-test: when to act
   ((eq 3 (length (symbol-name (car word-list))))
    ;; combine acted-on element with recursive call on shorter list
    (cons (car word-list) (keep-three-letter-words (cdr word-list))))

   ;; Third do-again-test: when to skip element;
   ;;   recursively call shorter list with next-step expression
   (t  (keep-three-letter-words (cdr word-list)))))

(keep-three-letter-words '(one two three four five six))
    ;=> (one two six)
```

### 无延时的递归
这部分讲解了如何将递归函数拆分成多个函数部分（比如：初始化函数、辅助函数），减少递归函数body部分的判断，使得递归函数本身只需要处理好递归操作，提高了递归函数的执行速度。

这部分显得过于详细，这里省略了该部分。

# 正则表达式查询
在Emacs中正则表达式查询使用得很广泛。在forward-sentence和forward-paragraph中使用了正则表达式查找定位。正则表达式'regular expression'常被写作'regexp'。

## sentence-end的正则表达式
符号sentence-end被绑定到匹配名末的正则式上。

句末通常是用一个句号、问号或者叹号结束的。那么这个正则表达式应该包含下面的字符：
```
[.?!]
```
然而，在有些时候句号、问号或叹号也有可能在某个语句的中间，我们并不想在使用forward-sentence的时候跳转到这些符号上去。

习惯上，你可能会在每个句子后面添加空格或者tab等等。我们可以用下面的表达式来匹配：
```
\\($\\| \\|  \\)
       ^   ^^
      TAB  SPC
```
$标明行末，括号前面的两个反斜线和竖线前面的两个反斜线中第一个反斜线是转义符。

语句的结束位置也可能跟了一个或者多个回车，如下：
```
[
]*
```
星号表明可以有零个或者多个回车。

一个语句的结束位置可能不只是句号、问号或叹号。它也可能是：一个回括号或其它：
```
[]\"')}]*
```
在这个表达式中，第一个`]`是表达式的第一个字符；第二个字符是`"`，综前面加了一个转义符。最后三个字符是`',),}`。

前面的表达式都是用于匹配一个语句的，如果我们对sentence-end求值，将返回下面的结果：
```
sentence-end
     => "[.?!][]\"')}]*\\($\\|     \\|  \\)[
]*"
```

## re-search-forward函数
re-search-forward函数与search-forward函数很相似。

re-search-forward函数搜索一个正则表达式。如果查找成功，它将point设置在匹配目标的最后一个字符的后面。如果是向后查找，它将point设置在匹配目标的第一个字符的前面。

与search-forward一样，re-search-forward函数接收四个参数：

 1. 第一个参数是要查找的正则表达式。表达式是一个被引号包括的字符串。

 2. 第二个参数是可选参数，限制搜索的范围，它是当前缓冲区中的某个位置（point）。

 3. 第二个可选参数指定搜索失败时如何处理：如果第三个参数为nil，则导致函数在搜索失败时显示错误信息；其它值将使函数失败时返回nil，搜索成功时返回t。

 4. 可选参数，用于指定重复次数。负数表示重复的向后搜索。

re-search-forward使用模板如下：
```emacs-lisp
(re-search-forward "regular-expression"
                limit-of-search
                what-to-do-if-search-fails
                repeat-count)
```
第二、三、四个参数是可选的。如果你想传递给最后两个参数，则必须也给前面的参数全传值。否则解释器将出错。

在forward-sentence函数中，sentence-end正则表达式如下：
```
"[.?!][]\"')}]*\\($\\|  \\|  \\)[
]*"
```
这限制了查询范围只到当前段落的结束位置（一个句子不可能超过段落）。如果查询失败，函数将返回nil；查询的次数可以由传递给forward-sentence函数的参数来提供。

## forward-sentence函数
这个命令将光标移到下一句，是在Emacs Lisp中使用正则表达式的很好的例子。实际这个函数看起来很长很复杂；这是因为函数被设计为能向前也能向后移动。该函数通常被绑定到M-e上。

### forward-sentence了函数定义
```emacs-lisp
(defun forward-sentence (&optional arg)
  "Move forward to next sentence-end.  With argument, repeat.
With negative argument, move backward repeatedly to sentence-beginning.
Sentence ends are identified by the value of sentence-end
treated as a regular expression.  Also, every paragraph boundary
terminates sentences as well."
  (interactive "p")
  (or arg (setq arg 1))
  (while (< arg 0)
    (let ((par-beg
           (save-excursion (start-of-paragraph-text) (point))))
      (if (re-search-backward
           (concat sentence-end "[^ \t\n]") par-beg t)
          (goto-char (1- (match-end 0)))
        (goto-char par-beg)))
    (setq arg (1+ arg)))
  (while (> arg 0)
    (let ((par-end
           (save-excursion (end-of-paragraph-text) (point))))
      (if (re-search-forward sentence-end par-end t)
          (skip-chars-backward " \t\n")
        (goto-char par-end)))
    (setq arg (1- arg))))
```

这个函数看起来太长了，最好是先弄清楚它的骨架，然后再了解细节。我们先从最左边开始看：
```emacs-lisp
(defun forward-sentence (&optional arg)
  "documentation..."
  (interactive "p")
  (or arg (setq arg 1))
  (while (< arg 0)
    body-of-while-loop
  (while (> arg 0)
    body-of-while-loop
```
这样看起来简单多了。函数定义由文档字符串，一个interactive语句，一个or语句和while循环组成。

依次来看看各个部分。

文档简单易懂。

interactive函数有一个"p"参数。这表示处理前缀参（C-u）。如果没有传递这个参数将被设置为1。如果在调用forward-sentence时，不是使用的交互式模式并且没有带参数，arg将被设置为nil。

### while循环部分
or语句后面有两个while循环。第一个while循环的true-or-false-test测试前缀参数是否为负数。这决定是否向后查询。循环体与第二个while的循环体类似，但不完全相同。我们跳过第一个while循环，集中看第二个循环

第二个循环将向前移动point。代码骨架如下：
```emacs-lisp
(while (> arg 0)            ; true-or-false-test
  (let varlist
    (if (true-or-false-test)
        then-part
      else-part
  (setq arg (1- arg))))     ; while loop decrementer
```
这个while循环是一个递减循环。它的true-or-false-test检查计数器（arg）是否大于0；并每次循环中将计数器减1。

如果没有前缀参数传递给forward-sentence，arg将被设置为1，while循环将只运行一次。

while循环体如下：
```emacs-lisp
(let ((par-end
       (save-excursion (end-of-paragraph-text) (point))))
  (if (re-search-forward sentence-end par-end t)
      (skip-chars-backward " \t\n")
    (goto-char par-end)))
```
let语句创建了一个局部变量par-end。前面我们看过，这局部变量用于限制正则表达式搜索的范围。如果它没有找到段落中的语句的结束位置，它将段落结束位置前停止搜索。

首先，我们来研究一下par-end是如何被绑定到段落结束位置的。程序使用了let语句将下面语句的结果赋给了par-end变量。
```emacs-lisp
(save-excursion (end-of-paragraph-text) (point))
```
在这个语句中，(end-of-paragraph-text)将point移动到段落的结束位置，(point)返回当前的point，然后用save-excursion恢复point到原来的位置。因此，let将par-end绑定到了save-excursion的返回值，即段落的结束位置。（(end-of-paragraph-text)函数使用了forward-paragraph函数）

接下来Emacs继续执行let的body部分，一个if语句：
```emacs-lisp
(if (re-search-forward sentence-end par-end t) ; if-part
    (skip-chars-backward " \t\n")              ; then-part
  (goto-char par-end)))                        ; else-part
```

### 正则表达式查询
re-search-forward函数根据sentence-end定义的正则表达式查找名末。如果找到，re-search-forward函数将做两件事：

 1. re-search-forward函数将point移到找到的目标的结束位置。

 2. re-search-forward函数返回true。这个值被if接收，表明查找成功。

当查找成功后，if语句执行then部分，这部分表达式`(skip-chars-backward "\t\n")`这个语句向后移过任何空白字符直到遇到一个可打印字符，然后把point设置在这个字符的后面。

如果re-search-forward函数找不到句末位置，则函数返回false。false将使if语句执行它的第三个参数，(goto-char par-end)：它将point移到段落末尾。

## forward-paragraph函数
forward-paragraph函数将point移到段落结束位置。通常被绑定到M-}上，它使用了大量重要的函数，包括：let*，match-beginning和looking-at。

forward-paragraph函数定义比forward-sentence的长很多，因为它工作于段落上，段落的每行可能以是填充前缀开头。

填充前缀是放在行的开头，通常是由一些重复的字符组成的字符串。比如，在Lisp代码中通常在一大段注释的每行前面添加;;;。在文本模式下(Text mode)，四个空格标明了一个段落的缩进。

这意味着在查找段落时，需要查找那些最左边的列有填充前缀的行。

有些情况下需要忽略这些前缀，特别是在使用空行来分隔段落时。这更增加了这个函数的复杂性。

### forward-paragraph函数定义的骨架
```emacs-lisp
(defun forward-paragraph (&optional arg)
  "documentation..."
  (interactive "p")
  (or arg (setq arg 1))
  (let*
      varlist
    (while (< arg 0)        ; backward-moving-code
      ...
      (setq arg (1+ arg)))
    (while (> arg 0)        ; forward-moving-code
      ...
      (setq arg (1- arg)))))
```
第一部分是常见部分：参数列表，包含一个可选参数。而后是文档字符串。

interactive的参数p表示可以处理前缀参数（C-u）。这是一个数字，用于设置执行的次数。or语句处理没有传递参数时的情况。

### let*语句
符号let*不是let。

let*与let类似，不同之处在于Emacs将依次给各个变量赋值，给后面的变量赋值语句可以使用前面已经赋值的变量。

在这个let*语句中，Emacs设置了两个变量：fill-prefix-regexp和paragraph-separate。变量fill-paragraph-separate的值，依赖于fill-prefix-regexp的值。

依次来看，符号fill-prefix-regexp的值被设置为下面的list的返回值：
```emacs-lisp
(and fill-prefix
     (not (equal fill-prefix ""))
     (not paragraph-ignore-fill-prefix)
     (regexp-quote fill-prefix))
```
在前面学习kill-new函数时，我们知道and将执行传递给它的每个参数直到有一个参数的返回值为nil，这种情况下and语句返回nil；如果没有参数返回nil，and语句将返回最后一个参数的值。简单来说，and语句在所有参数都为true时返回true。

变量fill-prefix-regexp只有在上面四个语句都为true时，才会设置为一个非nil值，否则fill-prefix-regexp将被设置为nil。

```emacs-lisp
fill-prefix
```
当这个变量被执行时，如果没有填充前缀，变量返回nil。
```emacs-lisp
(not (equal fill-prefix "")
```
这个语句检查填充字符串是否为一个空字符串。
```emacs-lisp
(not paragraph-ignore-fill-prefix)
```
如果paragraph-ignore-fill-prefix设了值（比如t），这个表达式将返回nil。
```emacs-lisp
(regexp-quote fill-prefix)
```
这是and语句的最后一个语句。如果and中所有的语句都为true，这条语句的返回值将作为and语句的返回值，这个返回值被设置到变量fill-prefix-regexp。

and语句的将fill-prefix-regexp设置为被regexp-quote函数修改过的fill-prefix上。regexp-quote函数读取一个字符串并返回能精确匹配这个字符串的正则表达式。这意味着fill-prefix-regexp将被设置为通匹配填充前缀的正则表达式。

let*语句设置的第二个局部变量是paragraph-separate。它被设置为下面语句的返回值：
```emacs-lisp
(if fill-prefix-regexp
    (concat paragraph-separate
            "\\|^" fill-prefix-regexp "[ \t]*$")
  paragraph-separate)))
```
这个语句显示了let*与let的区别。if语句的true-or-false-test检查fill-prefix-regexp是否为nil。

如果fill-prefix-regexp没有值，Emacs将执行if语句的else部分，将paragraph-separate设置为它的原始值。（paragraph-separate是一个匹配段落分隔的正则表达式）

如果fill-prefix-regexp有值，Emacs将执行if语句的then部分并将paragraph-separate设置为包含fill-prefix-regepx的正则表达式。

特别的是，paragraph-separate被设置为由它的原始值与fill-prefix-regexp组成的新值上。`^`表示fill-prefix-regexp必须在行首，行末可以是空白字符，这由`"[ \t]*$"`来定义。`\\|`表示"或"关系。

接下来进入let*语句的body部分。let*语句的第一部分处理给定的参数为负数，需要向后移动的情况。我们跳过这一部分。

### while循环中的向前移动
let*的body的第二部分处理向前移动。由于个while循环执行arg参数指定的循环次数。通常情况下参数被设置为1，循环只执行一次，光标向前移动一个段落。

这个部分共处理了三种情况：当point在段落中间时，当point在有填充前缀的段落内部时，当point在没有段落前缀的段落内部时。

while循环部分如下：
```emacs-lisp
(while (> arg 0)
  (beginning-of-line)

  ;; between paragraphs
  (while (prog1 (and (not (eobp))
                     (looking-at paragraph-separate))
           (forward-line 1)))

  ;; within paragraphs, with a fill prefix
  (if fill-prefix-regexp
      ;; There is a fill prefix; it overrides paragraph-start.
      (while (and (not (eobp))
                  (not (looking-at paragraph-separate))
                  (looking-at fill-prefix-regexp))
        (forward-line 1))

    ;; within paragraphs, no fill prefix
    (if (re-search-forward paragraph-start nil t)
        (goto-char (match-beginning 0))
      (goto-char (point-max))))

  (setq arg (1- arg)))
```
我们马上就可以看出这是一个递减的while循环，使用了`(setq arg (1- arg))`作为递减语句。

循环体包含了三个语句：
```emacs-lisp
;; between paragraphs
(beginning-of-line)
(while
    body-of-while)

;; within paragraphs, with fill prefix
(if true-or-false-test
    then-part

;; within paragraphs, no fill prefix
  else-part
```
当解释器执行while循环体时，第一件事就是执行(begion-of-line)语句将point移到行首位置。接下来是一个内部的while循环。这个while循环被设计为将光标从段落间的空白部分移出。最后是一个if语句将point移到段落的结束位置。

### 段落之间
首先，我们来看内部的while循环。这个循环处理point位于段落之间的情况；它使用了三个新的函数：prog1, eobp 和 looking-at。

 - prog1与progn类似，但是progn1返回的是它的第一个参数的值。（progn返回它的最后一个参数的值）后面的语句也将被执行。

 - eobp是End Of Buffer P的缩写，检查point是否在缓冲区的结束位置。

 - looking-at函数检查point后面的文本是否与传递给它的正则表达式参数匹配。

这个while循环部分如下：
```emacs-lisp
(while (prog1 (and (not (eobp))
                   (looking-at paragraph-separate))
              (forward-line 1)))
```
这是一个没有循环体的while循环！true-or-false-test部分如下：
```emacs-lisp
(prog1 (and (not (eobp))
            (looking-at paragraph-separate))
       (forward-line 1))
```
prog1的第一个参数是一个and语句。它检查point是否到了缓冲区的结束位置，也检查point后面的文本是否与正则表达式paragraph-separate匹配。

如果光标不在缓冲区结束位置且光标后面的文本是一个段落分隔，则and语句返回true。执行完and语句后，解释器执行prog1的第二个参数forward-line。它将光标向前移动一行。由于prog1的返回值是它的第一个参数，因此while循环将在point不在缓冲区结束位置或位于段落之间时继续执行。最后，point将在and语句测试为false时被移到一个新段落，由于这时forward-line已经被执行了。这意味着point已经从段落之间的位置移到了段落中，它停留在新段落第二行的开始位置。

### 段落内部
外部while循环的第二个部分是一个if语句。解释器将在fill-prefix-regexp不为nil时执行它的then部分，如果fill-prefix-regexp为nil，它将执行else部分（当段落没有填充前缀时）。

### 没有填充前缀
代码包含了一个if语句：
```emacs-lisp
(if (re-search-forward paragraph-start nil t)
    (goto-char (match-beginning 0))
  (goto-char (point-max)))
```
它查找一个正则表达式，直到下一个段落的开始位置，如果找到，就将point设置到那时在，如果下一个段落的开始位置未找到，则将point移到当前缓冲区可访问区域的结束位置。

这段代码里只有match-beginning比较陌生。它返回一个数字，这个数字标明了上一个正则表达式所匹配位置。

在这里使用match-beginning函数是由于forward search的一个特性：forward search查找成功时不管理普通查找还是正则表达式查找，它都会将point移到查找到的文本的结束位置。在这里，这样操作将使point移动到下一个段落的开始位置，而不是当前段落的结束位置。而这两个位置可能是不同的，因为段落之间可能有空行

当传的参数为0时，match-beginning函数返回的位置是最近一次匹配正则表达式的文本的开始位置。在这里，最近一次使用正则表达式查找的就是paragraph-start，因此match-begnning返回匹配的开始位置，而不是匹配的结束位置。这个开始位置即段落的结束位置。

### 有填充前缀时的情况
前面讨论了if语句的else部分。如果if语句检测到有填充前缀，它将执行then部分：
```emacs-lisp
(while (and (not (eobp))
            (not (looking-at paragraph-separate))
            (looking-at fill-prefix-regexp))
  (forward-line 1))
```
当下面三个条件都为true时，它将point向前移动一行：

 1. point不是位于缓冲区结束位置

 2. point后面的文本不是段落分隔符

 3. point后面的文本与填充前缀的正则表达式匹配

## 小结
在向前移动时，forward-paragraph函数执行了下面三个操作：

 - 将point移到行首

 - 忽略段落之间的行

 - 检查是否有填充前缀，如果有：

  - 向前移动一行直到该行不为段落分隔行

 - 如果没有填充前缀：

  - 查找下个段落的开始位置

  - 转到下个段落的开始位置，也就是前一个段落的结束位置

  - 或者转到缓冲区的结束的位置

下面是格式化过的代码：
```emacs-lisp
(interactive "p")
(or arg (setq arg 1))
(let* (
       (fill-prefix-regexp
        (and fill-prefix (not (equal fill-prefix ""))
             (not paragraph-ignore-fill-prefix)
             (regexp-quote fill-prefix)))

       (paragraph-separate
        (if fill-prefix-regexp
            (concat paragraph-separate
                    "\\|^"
                    fill-prefix-regexp
                    "[ \t]*$")
          paragraph-separate)))

  omitted-backward-moving-code ...

  (while (> arg 0)                ; forward-moving-code
    (beginning-of-line)

    (while (prog1 (and (not (eobp))
                       (looking-at paragraph-separate))
             (forward-line 1)))

    (if fill-prefix-regexp
        (while (and (not (eobp))  ; then-part
                    (not (looking-at paragraph-separate))
                    (looking-at fill-prefix-regexp))
          (forward-line 1))
                                  ; else-part: the inner-if
      (if (re-search-forward paragraph-start nil t)
          (goto-char (match-beginning 0))
        (goto-char (point-max))))

    (setq arg (1- arg)))))        ; decrementer
```
完整的代码不光有向前移动的代码，也包括了向后移动的代码。

在Emacs中可以用C-h f(describe-function)和函数名来查看整个函数。

可以使用M-.(find-tag)并输入函数名来查找函数定义。

## 创建自己的TAGS文件
M-.命令可以查看函数源码，变量或其它的源码。这个函数依赖于tags表告诉他该到哪里查找源码。

经常会需要自己创建tags表。tags表被称为TAGS文件。

可以用Emacs发行版中的etags程序来创建TAGS文件。通常etags不是Emacs Lisp函数，而是一个C程序。

创建TAGS文件前，先进入要创建这个文件的目录。在Emacs中可以用M-x cd命令，或者直接访问某个目录C-x d(dired)。然后运行编译命令并执行etags *.el。
```
M-x compile RET etags *.el RET
```
etags命令支持通配符。如果你有两个目录，你可以使用一个TAGS文件，输入`*.el ../elisp/*.el`，在这里`../elisp/`是第二个目录：
```
M-x compile RET etags *.el ../elisp/*.el RET
```
输入
```
M-x compile RET etags --help RET
```
查看etags支持的选项列表。

etags程序支持20多种语言，包括：Emacs Lisp、Common Lisp、Scheme、C、C++、Ada、Fortran、Java、Latex、Pascal、Perl、Python、Texinfo、makefiles等等。程序没有开关指定语言；它会根据输入的文件名和文件内容来识别语言的种类。

使用：`M-x locate RET TAGS RET`Emacs将列出你的所有TAGS文件的完整路径。

如果你想访问你创建的TAGS文件，可以使用`M-x visit-tags-table`命令。

### 创建Emacs源码的TAGS文件
GNU Emacs的源码中的Makefile文件包含了复杂的etags命令，它创建，合并所有Emacs源码中的tags放到src顶层目录中的一个TAGS文件中。

你可以在Emacs源码的顶层目录中执行下面的命令来创建TAGS文件：
```
M-x compile RET make tags RET
```

## 回顾
 - while
循环执行直到传递给它的第一个参数为true。然后返回nil。
例：
```emacs-lisp
(let ((foo 2))
  (while (> foo 0)
    (insert (format "foo is %d.\n" foo))
    (setq foo (1- foo))))

     ;=>      foo is 2.
             foo is 1.
             nil
```
（insert函数插入它的参数到point所在的位置；format函数格式化它的参数；`\n`产生新行。
）

 - re-search-forward

查找一个正则表达式，如果找到了就将point设置到目标位置的后面。

与search-forward类似，它接收四个参数：

  1. 要查找的正则表达式

  2. 可选参数，限制查询范围

  3. 可选参数，查找失败时如何处理，返回nil或者显示错误信息

  4. 可选参数，查找的重复数次；如果为负数，则向后查找

 - let*

将变量值绑定到各个变量上，并执行其它的参数，返回最后一个的值。在设置变量时，可以使用前面已经设置过的局部变量。

例：
```emacs-lisp
(let* ((foo 7)
      (bar (* 3 foo)))
  (message "`bar' is %d." bar))
     ;=> `bar' is 21.
```

 - match-beginning

返回上一次正则表达式查找时查找的文本的开始位置。

 - looking-at

如果point后面的文本与函数的参数（是一个正则表达式）匹配则返回t。

 - eobp

如果point在可访问的缓冲区的结束位置则返回t。如果缓冲区未被narrowed，则可访问缓冲区结束位置是缓冲区的结束位置。如果缓冲区被narrowed，则结束位置为narrowed部分的结束位置。

 - prog1

依次执行各个参数并返回第一个参数的值。

例：
```emacs-lisp
(prog1 1 2 3 4)
     ;=> 1
```

# 计数：重复和正则表达式

重复执行和正则表达式是Emacs Lisp中非常强大的工具。这章讲解使用while循环和递归结合正则表达式进行查找进行字数统计。

## 字数统计
标准的Emacs发行版中包含了一个统计region中行数的函数。但没有统计字数的函数。

## count-words-region 函数
字数统计函数可以统计行、段落、region、或者整个缓冲区。到覆盖范围该多大？Emacs的鼓励使用弹性的方式。可以将函数设计为处理region。这样即使需要统计整个缓冲区，也可以先用C-x h(mark-whole-buffer)先选定整个缓冲区。


统计字数是一个重复的动作：从region的开始位置，开始统计第一个词，然后是第二个，然后第三个，如此继续直到缓冲区的结束位置。这意味着单词统计的工作适合于使用递归或者while循环。

### 设计count-words-region函数
首先，我们将使用while循环实现单词统计，然后是递归。当然，这个命令需要交互。

交互式函数定义如下：
```emacs-lisp
(defun name-of-function (argument-list)
  "documentation..."
  (interactive-expression...)
  body...)
```

我们所要做的就是填空。

函数名应该是自描述的与已存在的count-lines-region类似。这可以让命令名容易被记住。count-words-region是一个较好的名称。

这个函数统计region中的字数。这说明参数列表中需要两个符号，分别绑定到region的开始位置和结束位置。这两个位置可以被称为beginning和end。文档字符串的第一行必须是一个完整的句子，因为有些命令将只打印文档的第一行，比如apropos命令。交互式语句(interactive "r")将把缓冲区开始位置和结束位置放到参数列表中。


函数体需要完成三个任务：第一，设置条件，在这个条件下while循环可以统计字数。第二，执行while循环。第三，向用户显示信息。

当用户调用count-words-region时point可能位于region的开始位置或结束位置。但是，计数处理只能从region的开始位置到结束位置计数。这意味着如果point没有在region的开始位置，则我们需要将point设置到region的开始位置，执行(goto-char beginning)。为了保证在函数执行完后，point可以恢复原来的位置，将需要用到save-excursion语句。

函数体的中心部分是由一个while循环组成，它内部有一个每次向前跳转一个单词的语句，另一个语句负责计数。while语句的true-or-false-test应该在point达到region结束位置时返回false，在此之前返回true。

我们可以使用(forward-word 1)作为向前移动一个单词的语句，如果我们使用正则表达式搜索就很容易明白Emacs中对于'word'的界定。

通过一个正则表达式查找到那个位置并把point设置在最后一个字符的后面。这表示成功的向前移了一个单词。

实际上还有一个问题，我们需要这个正则表达式跳过单词间的空格和标点符号。这表明正则表达式需要能匹配单词后面的空白和标点符号。（一个单词后面也可能没有空白和标点,因此正则表达式的这一部分应该是可选的）

因此，我们需要的正则表达式，要能匹配一个或多个构词字符（能构成单词的字符），后面跟一个可选的由一个或多个非构词字符（不能用于构成单词的字符）。正则表达式如下：
```
\w+\W*
```

缓冲区的语法表决定了哪些是构词字符。

查找语句如下：
```emacs-lisp
(re-search-forward "\\w+\\W*")
```

（注意w和W前面的双斜线。单个斜线对于Emacs Lisp解释器来说有特殊意义。它表明后面一个字符需要不同的处理。比如，`\n`表示换行。两个斜线表示斜线）

我们还需要一个计数器用于计数；这个变量初始时必须为0，然后在每次执行while循环体时增加。这个语句如下：
```emacs-lisp
(setq count (1+ count))
```

最后我们需要告诉用户region中有多少个字符。message函数用于向用户显示信息。显示信息只需要一个短语，我们并不需要很复杂。到底是简单还是复杂。我们可以用一个条件语句来解决定个问题。共有三种可能：region中没有单词，region只有一个单词，或者有多个单词。这时crond比较合适。

初步的函数定义如下：
```emacs-lisp
;;; First version; has bugs!
(defun count-words-region (beginning end)
  "Print number of words in the region.
Words are defined as at least one word-constituent
character followed by at least one character that
is not a word-constituent.  The buffer's syntax
table determines which characters these are."
  (interactive "r")
  (message "Counting words in region ... ")

;;; 1. Set up appropriate conditions.
  (save-excursion
    (goto-char beginning)
    (let ((count 0))

;;; 2. Run the while loop.
      (while (< (point) end)
        (re-search-forward "\\w+\\W*")
        (setq count (1+ count)))

;;; 3. Send a message to the user.
      (cond ((zerop count)
             (message
              "The region does NOT have any words."))
            ((= 1 count)
             (message
              "The region has 1 word."))
            (t
             (message
              "The region has %d words." count))))))
```
这个函数能够工作，但并不是在所有的情况下。

### count-words-region函数中空白处理的Bug
前面描述的count-words-region命令有两个Bug，或者说一个Bug的两个表现。首先，如果region中只在某些文本间有空白，count-words-region命令将告诉你region中只包含了一个单词。第二，如果region中只有缓冲区结束位置或者narrowed缓冲区的可访问域的结束位置有空白，命令在执行时将显示错误信息：
```
Search failed: "\\w+\\W*"
```

可以在Emacs中先安装这个函数，然后将它绑定到按键上：
```emacs-lisp
(global-set-key "\C-c=" 'count-words-region)
```
可以在设置region后按`C-c =`执行（如果没有绑定按键，可以用M-x count-words-region执行）。

对下面的内容执行时Emacs将告诉你，region有3个单词。
```
    one   two  three
```

如果把mark设置在这行的开头位置，point放在`one`的前面。重新执行`C-c =`。Emacs应该要告诉你region中没有单词，因为region只有空白。但是，Emacs告诉你region中只有一个单词。

第三个测试，复制上面例的整行到*scratch*缓冲区中并在行的结束位置输入一些空格。将mark设置在单词`three`的后面，然后point设置在行的结束位置（在这里即缓冲区的结束位置）。输入`C-c =`。这次Emacs应该告诉你region中没有单词。但是Emacs这次却显示了一个错误信息`Search failed`。

这两个bug来自于同一个问题。

思考这个Bug的第一个表现，命令告诉你行的开始位置的空白包含一个单词。它是这样产生的：count-words-region命令先将point移到region的开始位置。然后测试当前point的位置是否小于end变量的值。结果为true。接下来，通过表达式查找第一个单词。它将point设置在第一个单词的后面。count被设置为1。while循环重复，但这时point已经大于end的值了，循环退出；函数显示信息说在region中有一个单词。简单来说就是由于正则表达式查询时，它查找到的单词的结束位置超过了region的区域。

Bug的第二个表现中，region是缓冲区结束位置的空白。Emacs说Search failed。这是由于在while的true-or-false-test返回true，search语句被执行。但是由于没找到匹配项，因此查询失败。

这两种情况都是由于查询时扩展或者试图扩展到region的外部。

解决办法就是限制查询的区域，一个很简单的动作，但并没有想像的那么简单。

前面在讲re-search-forward函数时，它接收四个参数。第一个参数是必需的，其它三个是可选参数。它的第二个参数是用于限定查询范围的。第三个可选参数，如果为t，则函数将在查询失败时返回nil，而不显示错误信息。第四个可选参数是重复次数。（可以用C-h f查找函数的文档）

在count-words-region函数定义中，region的结束位置被以设置到end参数上，它将作为函数参数传入。因此我们可以把end作为正则表达式查询时的参数。
```emacs-lisp
(re-search-forward "\\w+\\W*" end)
```
如果只对count-words-region的定义作上面的修改，在遇到一些空白字符时，仍将得到Search failed的错误。

这是因为，有可能在限制的范围内，搜索不到构词字符。搜索将失败，并显示错误信息。但我们在这时并不想要获取错误信息，我们需要显示"The region does NOT have any words."。

解决这一问题的办法就是将re-search-forward的第三个参数设置为t，这样在函数在搜索失败时将返回nil。

如果你尝试运行程序，你将看到信息"Couting words in region..."并一直看到这条消息，直到你输入C-g(keyboard-quit)。

当在限制查询范围的region中搜索时，和前面一样，如果region中没有构词字符，搜索将失败。re-search-forward语句返回nil。这时point也不会被移动，而循环中的下一条语句将被执行。这条语句将计数增加。然后循环继续。true-or-false-test将一直返回true，因为point仍小于end参数，程序将陷入死循环。

count-words-region的定义还需要一些修改，以便在搜索失败时让true-or-false-test返回false。可以在true-or-false-test中增加一个条件，true-or-false-test在增加计数前需要满足下面的条件：point必须在region之内，且查询的语句必须找到了一个单词。

因为两个条件都必须为true。所以区域范围检查和搜索语句可以用and连接起来，都作为while循环的true-or-false-test：
```emacs-lisp
(and (< (point) end) (re-search-forward "\\w+\\W*" end t))
```
re-search-forward在成功搜索到单词后将返回t，并移动point，只要能找到单词，point将继续移动。当搜索失败或者point达到region的结束位置时，true-or-false-test将返回false。while循环退出，count-words-region函数显示一个或多个信息。

修改完后的count-words-region函数如下：
```emacs-lisp
;;; Final version: while
(defun count-words-region (beginning end)
  "Print number of words in the region."
  (interactive "r")
  (message "Counting words in region ... ")

;;; 1. Set up appropriate conditions.
  (save-excursion
    (let ((count 0))
      (goto-char beginning)

;;; 2. Run the while loop.
      (while (and (< (point) end)
                  (re-search-forward "\\w+\\W*" end t))
        (setq count (1+ count)))

;;; 3. Send a message to the user.
      (cond ((zerop count)
             (message
              "The region does NOT have any words."))
            ((= 1 count)
             (message
              "The region has 1 word."))
            (t
             (message
              "The region has %d words." count))))))
```

## 递归方式统计单词数量
上一节已经编写过了通过while循环进行计数的函数。

在这个函数中，count-words-region函数完成了三个工作：为计数设置适当的条件；计算region中的字数；将字数显示给用户。

如果我们在一个递归函数中执行所有的操作，则我们将在每次递归调用时都会得到字数的消息。如果region中包含了13个单词，消息将显示13次。这并不是我们需要的，我们需要写两个函数来做这个工作，一个函数（递归函数）将在另一个函数内部被使用。一个设置条件和显示信息，国一个返回字数。

开始编写函数。我们仍把这个函数叫作count-words-region。

根据前一个版本，我们可以描述出这个程序的结构：
```emacs-lisp
;; Recursive version; uses regular expression search
(defun count-words-region (beginning end)
  "documentation..."
  (interactive-expression...)

;;; 1. Set up appropriate conditions.
  (explanatory message)
  (set-up functions...

;;; 2. Count the words.
    recursive call

;;; 3. Send a message to the user.
    message providing word count))
```
定义很直接，不同的地方是递返回的数字必须传递给message来显示。这可以用let语句来完成：我们可以用let语句把字数赋给一个变量，并把这个值作为递归部分的返回值。使用cond语句，用于设置变量和显示信息给用户。

通常let语句总被作为函数的'次要工作'。但在这里，let将作为函数的主要工作，统计字数的工作就是在let语句中。

使用let时函数定义如下：
```emacs-lisp
(defun count-words-region (beginning end)
  "Print number of words in the region."
  (interactive "r")

;;; 1. Set up appropriate conditions.
  (message "Counting words in region ... ")
  (save-excursion
    (goto-char beginning)

;;; 2. Count the words.
    (let ((count (recursive-count-words end)))

;;; 3. Send a message to the user.
      (cond ((zerop count)
             (message
              "The region does NOT have any words."))
            ((= 1 count)
             (message
              "The region has 1 word."))
            (t
             (message
              "The region has %d words." count))))))
```

接下来我们需要编写递归计数函数。

递归函数至少有三个部分：'do-again-test'，'next-step-expresssion'和递归调用。

do-again-test决定函数是否继续调用。因为我们在统计region中的单词时我们使用了移动point的函数，do-again-test可以检查point是否位于region中。do-again-test需要检查point是位于region结束位置的前面还是后面。我们可以使用point函数获取point的位置信息，我们还需要传递将region的结束位置作为参数传递到递归计数函数里。

另外，do-again-test还需要检查是否找到了一个单词。如果没有，函数就不再需要继续调用它自己了。

next-step-expression修改某个值以便递归函数能在适当的时候停止递归调用。在这里next-step-expression可以是移动point的语句。

递归函数的第三个部分是递归调用。

在这个函数中我们也需要在某个地方执行计数工作。

这样，我们有了一个递归计数函数的原型：
```emacs-lisp
(defun recursive-count-words (region-end)
  "documentation..."
   do-again-test
   next-step-expression
   recursive call)
```
现在我们需要填空。首先我们从最简单的一种情况开始：point位于region结束位置或位于region之外，region中没有单词，因此函数需要返回0。同样，如果搜索失败，函数也需要返回0。

另一方面，如果point在region内部，并且搜索成功，函数应该再次调用它自己。

这样，do-again-test应该如下：
```emacs-lisp
(and (< (point) region-end)
     (re-search-forward "\\w+\\W*" region-end t))
```
注意，查找语句是do-again-test函数的一部分，在搜索成功时返回t，失败时返回nil。

do-again-test是if语句的true-or-false子句。如果do-again-test成功，则if语句的then部分执行，如果失败，则应该返回0，因为不管point是位于region的外面还是搜索失败都表示region中没有单词。

另外，do-again-test返回t或nil时，re-search-forward将在搜索成功时移动point。这是修改point的值并让递归函数在point移出region后停止递归调用的操作。因此，re-earch-foreard语句就是next-step-expression。

recursive-count-words函数如下：
```emacs-lisp
(if do-again-test-and-next-step-combined
    ;; then
    recursive-call-returning-count
  ;; else
  return-zero)
```

怎样加入计数机制呢？

我们知道计数机制应该与递归调用联合起来。由于next-step-expression将point一个个单词的移动，因此，针对每个单词都会调用一次递归函数，计数机制必须有一个语句将recursive-count-words的返回值加1。

思考下面几种情况：

 - 如果region中有两个单词，函数在遇到第一个单词时，需要返回region中其它单词数量（这里为1）加1的值。

 - 如果region中只有一个单词，函数在遇到第一个单词时，需要返回region中其它单词数量（这里为0）加1的值。

 - 如果region中没有单词，函数需要返回0。

从上面的描述中可以看出if语句的else部分在没有单词时返回0。而if语句的then部分必须返回1加上region中其它单词数量的值。

语句如下，使用了函数1+使它的参数加1。
```emacs-lisp
(1+ (recursive-count-words region-end))
```
整个recursive-count-words函数如下：
```emacs-lisp
(defun recursive-count-words (region-end)
  "documentation..."

;;; 1. do-again-test
  (if (and (< (point) region-end)
           (re-search-forward "\\w+\\W*" region-end t))

;;; 2. then-part: the recursive call
      (1+ (recursive-count-words region-end))

;;; 3. else-part
    0))
```

研究一下它是如何工作的：

当region中没有单词时，if语句的else部分被执行，函数返回0。

如果region中有一个单词，point的值小于region-end并且搜索成功。这时，if语句的true-or-false-test为true，if语句的then部分被执行。计数语句被执行。这个语句将返回（整个函数的返回值）递归调用的返回值加1的结果。

与此同时，next-step-expression将使point跳过region中的第一个单词。这表示当(recursive-count-words region-end)在第二次时被执行，并作为递归调用的结果，point的值将等于或大于region的结束位置。这样，recursive-count-words将返回0。最初的recursive-count-words将返回0+1，计数正确。

如果region中有两个单词，第一次调用recursive-count-words将返回1加上在包含其它单词的region上调用recursive-count-words的返回值，这里将是1加1，2是正确的返回值。

类似地，如果region中包含有3个单词，第一次调用recursive-count-words将返回1加上在包含其它单词的region上调用recursive-count-words的返回值，如此继继续。

整个程序包含了两个函数：

递归函数：
```emacs-lisp
(defun recursive-count-words (region-end)
  "Number of words between point and REGION-END."

;;; 1. do-again-test
  (if (and (< (point) region-end)
           (re-search-forward "\\w+\\W*" region-end t))

;;; 2. then-part: the recursive call
      (1+ (recursive-count-words region-end))

;;; 3. else-part
    0))
```

包装函数：
```emacs-lisp
;;; Recursive version
(defun count-words-region (beginning end)
  "Print number of words in the region.

Words are defined as at least one word-constituent
character followed by at least one character that is
not a word-constituent.  The buffer's syntax table
determines which characters these are."
  (interactive "r")
  (message "Counting words in region ... ")
  (save-excursion
    (goto-char beginning)
    (let ((count (recursive-count-words end)))
      (cond ((zerop count)
             (message
              "The region does NOT have any words."))
            ((= 1 count)
             (message "The region has 1 word."))
            (t
             (message
              "The region has %d words." count))))))
```

# 统计defun中的单词数量
我们的下一个计划是统计函数定义中的单词数量。我们可以使用count-word-region函数的一些变种（正则表达式方式）来完成这个工作。如果我们只是需要统计定义中的单词数量的话，可以简单的使用C-M-h(mark-defun)命令，然后调用count-word-region。

但我们要进行的是一项雄心勃勃的计划：我们需要统计Emacs源码中所有的函数和符号并打印出各个长度的函数分别有多少个：包含40至49个单词或符号的有多少，包含50到59个单词或符号的有多少，等等。

## 分割任务
这个任务目标使人畏惧；但如果将它分割成多个小的步骤，每次我们只处理其中的一部分，这样这个目标将不那么令人畏惧。先来思考一下有哪些步骤：

 1. 编写一个用于统计函数定义中字数的函数。这也包括了把符号当作单词的处理。

 2. 编写一个能列出一个文件中各个函数各有多少单词的函数。这个函数将调用count-words-in-defun函数（第1中定义的）。

 3. 编写一个能列出多个文件中各个函数各有多少单词的函数。负责自动查找多个文件，然后切换到这些文件中，并统计这些文件内的函数定义中的单词数量。

 4. 编写一个函数将第3步中得到的数据列表转换为适合打印的形式。

 5. 编写函数打印结果。

## 统计什么？
在上节所说的几个步骤中，首先就是需要决定哪些是需要进行统计的？当我们针对Lisp函数定义说'单词'('word')时，我们实际上很大程序上是在说'符号'（'symbols'）。举例来说，multiply-by-seven函数包含了5个符号defun,multiply-by-seven,number,*,和7。另外，文档字符串包含了四个单词Multiply,Number,by,和seven。符号number是重复的，因此定义包含了十个单词和符号。
```emacs-lisp
(defun multiply-by-seven (number)
  "Multiply NUMBER by seven."
  (* 7 number))
```
但是，如果我们对上面的函数定义执行C-M-h(mark-defun)，然后调用count-words-region，count-words-region将报告定义中有11个单词，而不是10。哪里出错了！

原因有两个：count-words-region不把*当作一个单词。把符号multiply-by-seven当作三个单词。连字符被作为单词间的空白。

这是由于count-words-region定义中的正则表达式引起的。在一个典型的count-words-region函数定义中，正则表达式如下：
```
"\\w+\\W*"
```
这个正则表达式匹配一个或多个构词字符被一个或多个非构词字符包围。

## 单词和符号由什么组成？
Emacs把不同的字符归属到不同的语法分类中。比如，正则表达式`\\w+`匹配一个或多个构词字符。构词字符是一个语法分类中的成员。另一个语法分类包含了标点符号，例如：句号和逗号，空白符号，空白字符和tab。

语法名指定了字符属于哪个分类。通常，连字符号不被当作构词字符。而是被作为'符号的一部分但不是单词'('class of characters that are part of symbol names but not words.')的一类。这意味着count-words-region函数将把它当作词间的空白一样对侍，这也说明了为什么count-words-region会把multiply-by-seven当作3个单词处理。

有两种办法让Emacs把multiply-by-sevn当作一个符号来处理：修改语法表或修改正则表达式。

我们可以重新在语法表中将连字符定义为构词字符，Emacs将在每个mode中保持这个设置。这个操作能达到我们的目的，除了连字符不是一个典型的构词字符外..

另外，我们也可以重新定义count-words函数中的正则表达式以包含连字符。这种处理的优点是比较明确，但任务有点刁。

这个正则表达式的第一个部分简单：必须匹配"至少由一个字符或符号构成"：
```
"\\(\\w\\|\\s_\\)+"
```

表达式的第一部分是`\\(`,括号中包含了两个部分`\\w`和`\\s_`，两者之间用`\\|`分隔表示或关系。`\\w`匹配任何构词字符，`\\s_`符号中的所有非构词字符。括号外面的+号表示单词或者构成符号的字符至少要出现一次。

表达式的第二个部分更难设计。我们需要在第一个部分后可以有一个非构词字符。首先，我想可以定义成下面的形式：
```
"\\(\\W\\|\\S_\\)*"
```
大写的W和S匹配非构词和非符号字符。

然后我们注意到region中每个单词或符号后面有空白字符（空格、tab、或空行）。因此我们需要让表达式匹配一个或多个构词（或构成符号）字符后面跟一个或多个空白字符，但实际单词和符号有可能紧跟在括号或标点的后面。最后，我们设计的正则表达式匹配将单词或符号后面跟有可选的非空白字符，然后跟可选的空白。

完整的表达式如下：
```
"\\(\\w\\|\\s_\\)+[^ \t\n]*[ \t\n]*"
```

## count-words-in-defun函数
前面已经看到过，有多个方法实现count-word-region函数。我们只选用其中一个合适的方式来实现count-words-in-defun。

使用while循环的版本容易理解，因此我们准备采用。因为count-words-in-defun函数将变成更复杂的函数的一部分，它不需要交互也不要显示信息，只需要返回数量。

另外，count-words-in-defun将被用于包含函数定义的缓冲区。因此，需要函数决定当point位于函数定义内部时是否能被调用，如果point位于函数定义内，它需要返回当前所在的函数定义的单词数量。这增加了这个函数的性。

根据上面的需求，我们准备了下面的模板：
```emacs-lisp
(defun count-words-in-defun ()
  "documentation..."
  (set up...
     (while loop...)
   return count)
```

与之前一样，我们的工作就是填空。

函数有可能在包含函数定义的缓冲区中。Point有可能位于某个函数定义的内部。count-words-in-defun必须先将point移到这个函数定义的起始位置，计数器置0，计数循环必须在到达函数定义结束位置时停止。

beginning-of-defun函数向后查找左括号。比如行开始位置的`(`，并将point移到那个位置或到达查询的限制的边界。实际上，beginning-of-defun将point移到左括号前面或者函数定义的前面，或者缓冲区的开始位置。我们可以使用beginning-of-defun将point放到我们希望有开始位置。

while循环部分需要一个计数器来保存计数。可以使用let语句创建局部变量，并将局部变量初始化为0，来达到这个目的。

end-of-defun函数与beginning-of-defun类似，它将point移到定义的结束位置。end-of-defun可以用于检查是否位于函数定义的结束位置。

count-words-in-defun的开始部分：首先，将point移到定义的开始位置，然后创建一个局部变量保存计数器，最后，记录下定义结束的位置以便while循环知道什么时候停止循环。

代码结构如下：
```emacs-lisp
(beginning-of-defun)
(let ((count 0)
      (end (save-excursion (end-of-defun) (point))))
```
代码比较简单，唯一复杂点的是"end"部分：它将end设置为save-excursion语句的返回值，这个语句返回end-of-defun（它将point移到定义的结束位置）执行后point的位置。

在初始化工作完成后，count-words-in-defun的第二个部分就是while循环。

这个循环必须包含按单词或符号向前移动的语句，另一个语句则用于统计移动的次数。while循环的true-or-false-test应该跳到定义结束位置时返回false。在这里我们可以使用前面讨论过的正则表达式：
```emacs-lisp
(while (and (< (point) end)
            (re-search-forward
             "\\(\\w\\|\\s_\\)+[^ \t\n]*[ \t\n]*" end t)
  (setq count (1+ count)))
```

函数定义的第三个部分返回符号或单词的数量。这个部分是函数内部的let语句的最后一个表达式。很简单，返回局部变量count。

这几个部分放在一起就构成了count-words-in-defun：
```emacs-lisp
(defun count-words-in-defun ()
  "Return the number of words and symbols in a defun."
  (beginning-of-defun)
  (let ((count 0)
        (end (save-excursion (end-of-defun) (point))))
    (while
        (and (< (point) end)
             (re-search-forward
              "\\(\\w\\|\\s_\\)+[^ \t\n]*[ \t\n]*"
              end t))
      (setq count (1+ count)))
    count))
```

怎样测试它呢？这个函数是非交互式的函数，但我们可以很容易的将它包装成一个交互式的函数；可以使用与count-words-region中类似的方式：
```emacs-lisp
;;; Interactive version.
(defun count-words-defun ()
  "Number of words and symbols in a function definition."
  (interactive)
  (message
   "Counting words and symbols in function definition ... ")
  (let ((count (count-words-in-defun)))
    (cond
     ((zerop count)
      (message
       "The definition does NOT have any words or symbols."))
     ((= 1 count)
      (message
       "The definition has 1 word or symbol."))
     (t
      (message
       "The definition has %d words or symbols." count)))))
```

我们可以将它绑定到`C-c =`上：
```emacs-lisp
(global-set-key "\C-c=" 'count-words-defun)
```

现在我们可以试试count-words-defun：安装count-words-in-defun和count-words-defun，设置按键绑定，然后将光标放到下面的定义中：
```emacs-lisp
(defun multiply-by-seven (number)
  "Multiply NUMBER by seven."
  (* 7 number))
     ;=> 10
```
将显示：
```
Success! The definition has 10 words and symbols.
```

下一个问题就是如何统计同一个文件中的多个定义中的单词和符号。

## 统计一个文件中的多个defun
文件simple.el可能包含超过80个函数定义。我们的终极目标是要对很多的文件进行统计，但第一步，我们当前的目标是要对一个文件进行统计。

这个信息将会是一连串的数字，每个数字是一个函数定义的长度。我们可以将这些数字保存到一个list中。

我们需要将多个文件的信息合并到一起，因此统计对一个文件进行统计时不需要显示信息，只需要返回长度信息。

在字数统计命令包含了一个语句用于按单词向前移动另一个语句计数。这个返回函数定义长度的函数同样可以使用这种方式，一个语句用于向前跳转一个函数定义，另一个语句用于计数。

编写函数字义。我们需要从文件开始位置计数，因此第一个命令使用(goto-char (point-min))。接下来，我们开始while循环，循环的true-or-false-test可以是一个查询下一个函数定义的正则表达式查询，如果查询成功，则将point向前移动，循环体被执行。循环体需要一个语句构造包含长度的list。

代码片段如下：
```emacs-lisp
(goto-char (point-min))
(while (re-search-forward "^(defun" nil t)
  (setq lengths-list
        (cons (count-words-in-defun) lengths-list)))
```
我们还少了缺少查找函数定义文件的机制。

## 查找文件
在Emacs中可以使用C-x C-f(find-file)命令。这个命令并不是很符合处理当前问题。

先来看find-file的源码（可以使用find-tag命令C-h f(describe-functin)来查找源文件）：
```emacs-lisp
(defun find-file (filename)
  "Edit file FILENAME.
Switch to a buffer visiting file FILENAME,
creating one if none already exists."
  (interactive "FFind file: ")
  (switch-to-buffer (find-file-noselect filename)))
```
定义很短，一个interactive用于执行命令时的交互。定义的body部分包含个函数，find-file-noselect和switch-to-buffer。

使用C-h f（describe-function命令）查看find-file-noselect函数的文档，这个函数读取指定的文件到缓冲区中，并返回这个缓冲区。但是这个缓冲区未被选中。Emacs并不会将焦点转移到它。这个工作由switch-to-buffer完成，它将Emacs焦点转到指定的缓冲区，并将这个缓冲区在窗口中显示出来。

在这个工程中，我们并不需要在屏幕上显示每个文件。因此我们使用set-buffer来替代switch-to-buffer，它将程序的焦点转移到另一个缓冲区，但不会改变屏幕显示。因此，我们不调用find-file，而是需要自己编写一个。

可以使用find-file-noselect和set-buffer来完成这个工作。

## lengths-list-file函数的细节
lengths-list-file函数的核心是一个while循环，它包含了将point向前（'defun by defun'）移动的函数和用于统计每个defun中符号或单词数量的函数。这个核心将被包含在执行各种任务的函数中，包括文件查找，确保point位于文件的开始位置。这个函数定义如下：
```emacs-lisp
(defun lengths-list-file (filename)
  "Return list of definitions' lengths within FILE.
The returned list is a list of numbers.
Each number is the number of words or
symbols in one function definition."
  (message "Working on `%s' ... " filename)
  (save-excursion
    (let ((buffer (find-file-noselect filename))
          (lengths-list))
      (set-buffer buffer)
      (setq buffer-read-only t)
      (widen)
      (goto-char (point-min))
      (while (re-search-forward "^(defun" nil t)
        (setq lengths-list
              (cons (count-words-in-defun) lengths-list)))
      (kill-buffer buffer)
      lengths-list)))
```
这个函数有一个参数，需要处理的文件名。有4行文档字符串，但没有交互式语句。body部分的第一行是一个message，用于提示用户机器正在执行操作。

下一行包括了一个save-excursion它将在函数结束时，将Emacs焦点恢复到当前缓冲区。这通常用于将一个函数嵌入另一个函数时，可以恢复原缓冲区中的point。

在let语句的变量列表中，Emacs打开文件，并将包含该文件缓冲区设置到buffer变量。同时，Emacs创建了局部变量lengths-list。

接下来，Emacs将焦点转到这个缓冲区。

在下一行中，Emacs将缓冲区设置为只读。理想情况下，这行是不必要的。没有哪个计数函数需要修改缓冲区。并且，即使我们修改了缓冲区，缓冲区也不会被保存。这主要是防止不小心修改了Emacs的源码造成麻烦。

接下来，如果缓冲区被narrowed，则调用widen。这个函数在Emacs创建一个新的缓冲区时不需要，但如果文件已经在缓冲区中时，有可能缓冲区被narrowed了，这时必须调用widen。如果我们要完全的"user-friendly"，我们还需要保存point的位置，但我们不需要。

(goto-char (point-min))语句将point移到缓冲区的开始位置。

后面的while循环中，Emacs决定每个定义的长度并构造一个包含长度信息的列表。

然后，Emacs关闭缓冲区，继续后面的操作。这是为了保存Emacs的空间。在Emacs 19中包含了超过300个源码文件；Emacs 21包含了超过800个源码文件。另一个函数将在每个文件上执行length-list-file。

你可以安装并测试一下这个文件。将光标放在下面的语句的后面，执行C-x C-e(eval-last-sexp)：
```emacs-lisp
(lengths-list-file
 "/usr/local/share/emacs/21.0.100/lisp/emacs-lisp/debug.el")
```

## 统计不同文件中的defun中的单词
前一节，我们创建了一个可以返回单个文件中各个函数长度列表的函数。现在我们需要定一个函数返回文件列表中所有定义长度的函数。

使用while循环或递归在每个文件上执行相同的操作。

### 决定defun的长度
使用while循环作为程序主干。传递给函数的是一个文件列表。前面看过，可以写一个while循环，如果列表中包含了元素，则执行循环，否则退出循环。循环体必须在每次执行时缩短list的长度，直到list为空退出循环。通常的技巧是将list设置为原来的list的CDR。

模板如下：
```emacs-lisp
(while test-whether-list-is-empty
  body...
  set-list-to-cdr-of-list)
```

while循环将返回nil（true-or-false-test的返回值），而不是循环体的执行结果。因此我们需要将while循环包含在let语句中，并让let语句的最后一个语句包含要返回的list。

代码如下：
```emacs-lisp
;;; Use while loop.
(defun lengths-list-many-files (list-of-files)
  "Return list of lengths of defuns in LIST-OF-FILES."
  (let (lengths-list)

;;; true-or-false-test
    (while list-of-files
      (setq lengths-list
            (append
             lengths-list

;;; Generate a lengths' list.
             (lengths-list-file
              (expand-file-name (car list-of-files)))))

;;; Make files' list shorter.
      (setq list-of-files (cdr list-of-files)))

;;; Return final value of lengths' list.
    lengths-list))
```

expand-file-name是一个内置函数，它将文件名转换为绝对路径。

如果在debug.el上执行expand-file-nameEmacs将得到
```
/usr/local/share/emacs/21.0.100/lisp/emacs-lisp/debug.el
```
函数定义的中的另一个新元素是未学习过的函数append。

### append函数
append函数将一个list添加到另一个list，如下，
```emacs-lisp
(append '(1 2 3 4) '(5 6 7 8))
```
将产生list
```emacs-lisp
(1 2 3 4 5 6 7 8)
```
这恰好是我们需要结果。如果使用cons，
<src lang="emacs-lisp"
(cons '(1 2 3 4) '(5 6 7 8))
```
则，将得到：
```emacs-lisp
((1 2 3 4) 5 6 7 8)
```

## 递归统计不同文件中的单词数量
除了while循环，你可以在文件列表中使用递归处理。递归版本的lengths-list-many-files简洁一些。

递归函数通常有这些部分：'do-again-test'，'next-step-expression'和递归调用。'do-again-test'决定是否再次调用自身，它需要检查list-of-files是否还包含有元素；'next-step-expression'将list-of-files重新设置为它的CDR部分，因此，最后这个list将变为空；递归调用则在缩短后的list上调用它自身。代码如下：
```emacs-lisp
(defun recursive-lengths-list-many-files (list-of-files)
  "Return list of lengths of each defun in LIST-OF-FILES."
  (if list-of-files                     ; do-again-test
      (append
       (lengths-list-file
        (expand-file-name (car list-of-files)))
       (recursive-lengths-list-many-files
        (cdr list-of-files)))))
```
简单来说，函数将第一次返回的list-of-files追加到其它次调用返回的list-of-files中。

这里是一个recursive-lengths-list-many-files的测试。

安装recursive-lengths-list-many-files和lengths-list-file。
```emacs-lisp
(cd "/usr/local/share/emacs/21.0.100/")

(lengths-list-file "./lisp/macros.el")
     ;=> (273 263 456 90)

(lengths-list-file "./lisp/mail/mailalias.el")
     ;=> (38 32 26 77 174 180 321 198 324)

(lengths-list-file "./lisp/makesum.el")
     ;=> (85 181)

(recursive-lengths-list-many-files
 '("./lisp/macros.el"
   "./lisp/mail/mailalias.el"
   "./lisp/makesum.el"))
       ;=> (273 263 456 90 38 32 26 77 174 180 321 198 324 85 181)
```
recursive-lengths-list-many-files函数产生了我们想要的输出。

下一步是准备显示图表的数据。

## 准备显示图表的数据
recursive-lengths-list-many-files函数返回了一个包含计数的列表。每个数字记录了一个函数定义的长度。我们需要将数据转换到适于生成图表的list中。新的list将告诉我们有多少个定义包含少于10个单词或符号，多少个处于10到19个单词或符号之间，等等。

我们需要遍历recursive-lengths-list-many-files函数返回的list中的值，并计算处于各个范围中的数量，并产生包含这些数量的list。

基于之前我们所做的，我们可以预想到编写这个函数并不难。可以用截取CDR的方式遍历各个元素，决定这个长度位于哪个范围，并增加这个范围的计数。

但是，在编写这个函数前，我们需要思考对list排序的优点，数字按从小到大的顺序排列。首先，排序将使计数容易一些，因为相信的数字将会处于同一个范围中。第二，检查排序后的list，可以知道最大的数字和最小的数字，便于决定我们所需要的最大和最小的范围。

### List排序
Emacs包含了一个排序函数sort。sort带两个参数，被排序的list和一个决定list元素大小关系的参数。

sort函数可以基于任意的属性进行排序；这意味着sort可以用于对非数字进行排序，比如按字母。

`<`函数用于对数字类型的list排序。例：
```emacs-lisp
(sort '(4 8 21 17 33 7 21 7) '<)

produces this:

(4 7 7 8 17 21 21 33)
```
注意，两个参数前都使用了单引号，表示不需要对它们求值。

也可以使用`<`对recursive-lengths-list-many-files函数的返回值排序：
```emacs-lisp
(sort
 (recursive-lengths-list-many-files
  '("../lisp/macros.el"
    "../lisp/mailalias.el"
    "../lisp/makesum.el"))
 '<

which produces:

(85 86 116 122 154 176 179 265)
```
（注意，这个例子中第一个参数没加单引号，因为它在传递给sort前需要被执行。）

### 产生文件列表
recursive-lengths-list-many-files函数需要一个文件列表作为参数。在测试的例子中，我们手工构造了一个文件列表；但Emacs List源码目录太大了。我们需要编写函数来完成这个工作。在这个函数中，我们将要同时使用while循环和递归调用。

在旧版本的GNU Emacs中我们不需要编写这样的函数，因为它将所有的.el文件放在同一个目录中。我们可以使用directory-files函数，它将返回单个目录中匹配指定表达式的文件名的列表。

但是，在新版本的Emacs中Emacs将Lisp文件放到了顶级lisp目录的子目录中。比如所有mail相关的文件放到了mail子目录中。

我们可以创建函数files-in-below-directory，使用car，nthcdr和substring连接已经存在的函数调用directory-files-and-attributes。这个函数不只是返回目录中的文件名列表，还将返回子目录的名称，和它们的属性。

重新描述我们的目标：创建一个函数能传递下面结构的参数给recursive-lengths-list-many-files函数：
```emacs-lisp
("../lisp/macros.el"
 "../lisp/mail/rmail.el"
 "../lisp/makesum.el")
```

directory-files-and-attributes函数返回包含list的list。list中的每个元素是一个包含了13的元素的子list。第一个元素是包含了文件名，在GNU/Linux中，它可能是一个'directory file'，也就是说，它是一个有特殊属性的目录文件。第二个元素为t的表示是一个目录，为字符串时表示是一个符号文件（该字符串表示连接的目标文件），或者为nil。

比如，`lisp/`目录中第一个`.el`文件是abbrev.el。它的文件名是`/usr/local/share/emacs/21.0.100/lisp/abbrev.el`它不是一个目录也不是一个链接。

下面是directory-files-and-attributes返回的值：
```emacs-lisp
("/usr/local/share/emacs/21.0.100/lisp/abbrev.el"
nil
1
1000
100
(15019 32380)
(14883 48041)
(15214 49336)
11583
"-rw-rw-r--"
t
341385
776)
```
而表示`mail/`目录下的`mail/`目录的list如下：
```emacs-lisp
("/usr/local/share/emacs/21.0.100/lisp/mail"
t
...
)
```
（查看file-attributes的文档可以了解这些属性。记住，file-attributes函数不会列出文件名，它的第一个元素是directory-files-and-attributes的第二个元素。）

我们需要让新函数，files-in-below-directory列出目录及其子目录中的`.el`文件。

这为我们构造files-in-below-directory给出了提示：在一个目录中，函数需要添加`.el`文件名到一个list中；如果是一个目录，则要进入这个子目录重复上面的操作。

但是，我们不需要进入表示目录自身的"."目录，也不需要进入上级目录".."。

因此，我们的files-in-below-directory函数必须完成这些任务：

 - 检查是否有文件以.el尾；如果是则添加到list。

 - 检查是否有文件名是一个目录，如果是，

  - 检查它是否为`.`或`..`；如果是则跳过，

  - 如果不是则进入那个目录重复上面的操作。

我们将使用while循环在同一个目录中从一个文件移到另一个文件，检查文件是否是需要的；如果是一个子目录则递归调用。递归使用"acumulate"模式，使用append合并结果。

这里是函数定义：
```emacs-lisp
(defun files-in-below-directory (directory)
  "List the .el files in DIRECTORY and in its sub-directories."
  ;; Although the function will be used non-interactively,
  ;; it will be easier to test if we make it interactive.
  ;; The directory will have a name such as
  ;;  "/usr/local/share/emacs/21.0.100/lisp/"
  (interactive "DDirectory name: ")
  (let (el-files-list
        (current-directory-list
         (directory-files-and-attributes directory t)))
    ;; while we are in the current directory
    (while current-directory-list
      (cond
       ;; check to see whether filename ends in `.el'
       ;; and if so, append its name to a list.
       ((equal ".el" (substring (car (car current-directory-list)) -3))
        (setq el-files-list
              (cons (car (car current-directory-list)) el-files-list)))
       ;; check whether filename is that of a directory
       ((eq t (car (cdr (car current-directory-list))))
        ;; decide whether to skip or recurse
        (if
            (equal (or "." "..")
                   (substring (car (car current-directory-list)) -1))
            ;; then do nothing if filename is that of
            ;;   current directory or parent
            ()
          ;; else descend into the directory and repeat the process
          (setq el-files-list
                (append
                 (files-in-below-directory
                  (car (car current-directory-list)))
                 el-files-list)))))
      ;; move to the next filename in the list; this also
      ;; shortens the list so the while loop eventually comes to an end
      (setq current-directory-list (cdr current-directory-list)))
    ;; return the filenames
    el-files-list))
```

files-in-below-directory directory-files函数需要一个参数，目录名称。

在我的系统上，
```emacs-lisp
(length
 (files-in-below-directory "/usr/local/share/emacs/21.0.100/lisp/"))
```
我的版本是12.0.100，Lisp源码目录包含754个`.el`文件。

files-in-below-directory返回的list是按字母逆序排列的，可以用一个语句来按字母顺序排列：
```emacs-lisp
(sort
 (files-in-below-directory "/usr/local/share/emacs/21.0.100/lisp/")
 'string-lessp)
```

### 统计函数定义的数量
我们当前的目标是产生一个list告诉我们有多少个函数定义包含少于10个单词和符号，多少个函数包含10到19个单词和符号，等等。

对于一个排了序的list这很简单：统计list中有多少个元素小于10，然后计算有多少个小于20，如些继续。每个范围的数字，我们可以用一个列表top-of-ranges来定义。

如果需要，我们可以自动生成这个list，手写也比较简单。例如：
```emacs-lisp
(defvar top-of-ranges
 '(10  20  30  40  50
   60  70  80  90 100
  110 120 130 140 150
  160 170 180 190 200
  210 220 230 240 250
  260 270 280 290 300)
 "List specifying ranges for `defuns-per-range'.")
```

要修改范围，我们只需要编辑这个list。

接下来我们需要编写函数创建一个包含各个范围数量的列表。这个函数必须传递两个参数，sorted-lengths和top-of-ranges。

defuns-per-range函数必须重复做两件事：它必须统计当前top-of-range值范围内的数字的数量；在一个范围内的数字统计完成后，它必须移到top-of-ranges的下一个值。由于，每个操作都是重复的，我们可以使用while循环来完成这个工作。一个循环统计一个top-of-ranges中当前范围中定义的数量，另一个循环依次取top-of-range的下一个值。

sorted-lengths列表需要在各个范围内进行多次计数，因此处理sorted-lengths的循环应该在处理top-of-ranges列表的循环的内部。

内部的循环统计一定范围内的数量。可以用一个简单的循环。循环的true-or-false-test检查sorted-lengths列表是否小于top-of-range的当前值。如果是，则函数将计数器加1，然后检查sorted-lengths列表的下一个值。

内部的循环如下：
```emacs-lisp
(while length-element-smaller-than-top-of-range
  (setq number-within-range (1+ number-within-range))
  (setq sorted-lengths (cdr sorted-lengths)))
```

外部的循环从top-of-ranges列表的最小值开始，依次设置为更大的值。循环如下：
```emacs-lisp
(while top-of-ranges
  body-of-loop...
  (setq top-of-ranges (cdr top-of-ranges)))
```

两个循环放在一起如下：
```emacs-lisp
(while top-of-ranges

  ;; Count the number of elements within the current range.
  (while length-element-smaller-than-top-of-range
    (setq number-within-range (1+ number-within-range))
    (setq sorted-lengths (cdr sorted-lengths)))

  ;; Move to next range.
  (setq top-of-ranges (cdr top-of-ranges)))
```

另外，每上外部循环，Emacs都要在一个list中记录这个范围内的数量(number-within-range)。我们可以使用cons来达到这个目的。

cons函数工作得很好，它构造的list中，最大范围的将位于开始位置，小范围的位于结束位置。这是因为cons将新元素添加到list的开始位置，在两个循环中将从小到大的顺序执行，defuns-per-range-list将以最大的数字开始。但我们打印的图表需要以小数字开始。解决的办法是逆序排列。使用nreverse函数。

举例来说：
```emacs-lisp
(nreverse '(1 2 3 4))

produces:

(4 3 2 1)
```

注意，nreverse函数是一个"destructive"（破坏性的函数）类型的函数，它将修改所操作的list；相反的函数是car和cdr函数，它们是"非破坏性的"。在这里，我们不需要原始的defun-per-range-list，因此不必担心破坏性的问题。（reverse函数担任了逆序复制list的功能，它也不修改原始的list。）

整个defuns-per-range函数如下：
```emacs-lisp
(defun defuns-per-range (sorted-lengths top-of-ranges)
  "SORTED-LENGTHS defuns in each TOP-OF-RANGES range."
  (let ((top-of-range (car top-of-ranges))
        (number-within-range 0)
        defuns-per-range-list)

    ;; Outer loop.
    (while top-of-ranges

      ;; Inner loop.
      (while (and
              ;; Need number for numeric test.
              (car sorted-lengths)
              (< (car sorted-lengths) top-of-range))

        ;; Count number of definitions within current range.
        (setq number-within-range (1+ number-within-range))
        (setq sorted-lengths (cdr sorted-lengths)))

      ;; Exit inner loop but remain within outer loop.

      (setq defuns-per-range-list
            (cons number-within-range defuns-per-range-list))
      (setq number-within-range 0)      ; Reset count to zero.

      ;; Move to next range.
      (setq top-of-ranges (cdr top-of-ranges))
      ;; Specify next top of range value.
      (setq top-of-range (car top-of-ranges)))

    ;; Exit outer loop and count the number of defuns larger than
    ;;   the largest top-of-range value.
    (setq defuns-per-range-list
          (cons
           (length sorted-lengths)
           defuns-per-range-list))

    ;; Return a list of the number of definitions within each range,
    ;;   smallest to largest.
    (nreverse defuns-per-range-list)))
```

整个函数很直观，除了一个地方。内部循环的true-or-false-test：
```emacs-lisp
(and (car sorted-lengths)
     (< (car sorted-lengths) top-of-range))
```
被替换为了
<src lang="emacs-lisp"
(and (car sorted-lengths)
     (< (car sorted-lengths) top-of-range))
```
这个测试的目的是为了决定sorted-lengths列表的第一个元素是否小于范围的值。

简单版本的test在sorted-lengthslist有一个nil值时可以工作。在那种情况下，(car sorted-lengths)将返回nil。而`<`函数不能比较数字和nil，因此Emacs将产生错误信息并停止执行。

在统计到list的结束位置时，sorted-lengths列表将变为nil。这样如果使用简单版本的函数在test时也将出错。

解决这个问题的办法就是使用(car sorted-length)语句和and语句。(car sorted-lengths)语句在list中有至少一个值时，会返回一个non-nil值，但如果list为空时将返回nil。and语句先执行(car sorted-lengths)，如果它返回nil，则返回false而不执行`<`语句。如果(car sorteed-lengths)语句返回的是non-nil值，and语句将执行`<`语句，返回值将是and语句的值。

这样，我们避免了一个错误。

这里有一个简短版本的defuns-per-range函数。首先，将top-of-ranges设置为一个list，然后设置sorted-lengths，执行defuns-per-range函数
```emacs-lisp
;; (Shorter list than we will use later.)
(setq top-of-ranges
 '(110 120 130 140 150
   160 170 180 190 200))

(setq sorted-lengths
      '(85 86 110 116 122 129 154 176 179 200 265 300 300))

(defuns-per-range sorted-lengths top-of-ranges)
```
返回的list如下：
```emacs-lisp
(2 2 2 0 0 1 0 2 0 0 4)
```
实际上，sorted-lengths中有两个元素小于110，两个元素在110和119之间，两个元素在120和129之间，等等。有四个元素大于或等于200。

# 准备图表
我们的目标是构造一个图表显示Emacs lisp源码中所有函数定义的长度范围。

在实际应用中，如果你要创建一个图表，你可能会使用gnuplot之类的程序来完成这个工作。（gnuplot与GNU Emacs集成得很好。）但在这里，我们将使用前面我们所学的知识来完成这个工作。

在这章，我们将先编写一个简单的图表打印函数。第一个版本将作为原型，在此基础上来增强。

## 打印图表列
由于Emacs被设计为能在各种终端上工作，包括字符终端，图表需要是可打印字符。我们可以使用星号来打印图表。

我们把这个函数命名为graph-body-print；它使用numbers-list作为参数。

graph-body-print函数根据numbers-list中的每个原素，分别插入垂直方向的星号列。每一列的高度取决于numbers-list上元素值的大小。

插入列是一个重复动作，因此函数可以用while循环或递归实现。

我们面临的第一个挑战就是如何打印星号列。通常，在Emacs我们打印字符的时候是横向打印的，一行一行的打印。我们有两个办法来实现：编写我们自己的列插入函数或者查找Emacs中是否有现成的方法。

为查找Emacs中的函数，我们可以使用M-x apropos命令。这个命令与C-h a(command-apropos)命令类似，但后者只查找作为命令的函数。而M-x apropos命令将列出所有匹配正则表达式的符号，包括那些非交互式的函数。

我们想找到那些可以打印或插入纵向列的命令。这个函数的名称肯定包含有'print'或'insert'或'column'等单词。因此，我们只要输入`M-x apropos RET print\|insert\|column RET`并查看结果。在我们系统上，这个命令执行需要一些时间，结果包含有79个函数和变量。查找这个列表，我们看到有个insert-rectangle函数有可能能完成这个工作。

这个函数文档如下：
```
insert-rectangle:
Insert text of RECTANGLE with upper left corner at point.
RECTANGLE's first line is inserted at point,
its second line is inserted at a point vertically under point, etc.
RECTANGLE should be a list of strings.
```

我们可以测试一下，以确认它是否如我们期望的那样工作。

把光标放在insert-rectange语句的后面按C-u C-x C-e(eval-last-sexp)。这个函数将在point的下面插入"first","second","third"。函数返回值为nil。
```emacs-lisp
(insert-rectangle '("first" "second" "third"))first
                                              second
                                              third
nil
```
在绘制图表的程序中使用这上函数。我们需要先确保point位于需要插入的位置，然后用insert-rectangle函数插入列。

如果你是在Info中读取这个文档，你可以切换到另一个缓冲区，比如`*scratch*`，将point放在任何地方，输入`M-:`，在提示区输入insert-rectangle语句，然后回车。Emacs将执行输入的语句，交把`*scratch*`缓冲区中的point位置作为point的值。（`M-:`被绑定到eval-expression上。）

我们将发现当执行完成插入后，point被设置在了最后插入的那行，也就是说这个函数移动了point。如果我们重复执行这个命令，下次插入的内容将在上次插入内容的下面。我们并不需要这样，我们需要的是一个柱状图表，一列挨着一列。

我们看出每次while循环插入列时必须重新设置point的位置，这个位置必须在列的顶部，而不是在底部。并且，我们打印图表时，并不需要每个列都一样高。这意味着每个列的顶部并不是一样高的。我们不能简单在一同一行上执行同一个操作，而是需要先将point移到正确的位置。

我们准备用星号来描述柱状图。星号的数量取决于当前numbers-list中元素的值。我们需要构造一个包含星号的列表以便insert-rectangle来画出正确高度的列。如果这个list只包含一定数量的星号，那我们就必须在绘制前将point设置到正确的高度。这比较困难。

我们可以想出另外一种方式，每次传递给insert-rectangle一个同样长度的list，它们可以在同一行插入，每次插入时只需要向右移动一列。比如，如果最高的高度为5，但实际高度只有3，则insert-rectangle需要的参数如下：
```emacs-lisp
(" " " " "*" "*" "*")
```

最后一个需求不是很难，我们需要决定列的高度。有两种方法：我们可以使用任意的值或使用整个list中最大的数字作为最大高度值。Emacs中提供了内置的函数检查参数中的最大值。我们可以使用这个函数。这个函数被称为max它返回它所有参数中的最大值。例：
```emacs-lisp
(max  3 4 6 5 7 3)
```

将返回7。（相反的函数是min它返回参数中最小的值）

但是，我们不能简单的在numbers-list上调用max；max函数需要数字类型的参数，而不是包含数字的list。因此，下面的语句：
```emacs-lisp
(max  '(3 4 6 5 7 3))
```
将出错：
```
Wrong type of argument:  number-or-marker-p, (3 4 6 5 7 3)
```

我们需要一个函数将list拆开作为参数传递给函数。这个函数是apply。这个函数将其它的参数传递给它的第一个参数，它的最后一个参数可以是一个list。

例如：
```emacs-lisp
(apply 'max 3 4 7 3 '(4 8 5))
```
将返回8。

（顺便说一句，我不知道你如何学习书本上没有介绍过的函数。可以根据函数名称，比如search-forward或insert-rectangle，根据他们的部分名称使用apropos查找函数的相关信息。）

传递给apply的第二个参数是可选参数，我们可以使用aplly调用一个函数并将list中的元素传递给这个函数，比如下面的代码也将返回8：
```emacs-lisp
(apply 'max '(4 8 5))
```
后面我们将使用apply。函数recursive-lengths-list-many-files返回包含数字的list，我们对其调用max。

这样，查找图表中的最大数量的代码如下：
```emacs-lisp
(setq max-graph-height (apply 'max numbers-list))
```

现在我们回到如何构造包含列图表字符串的list的问题上。知道图表的最大高度和星号的数量后，函数应该可以返回一个传递给insert-rectangle的list了。

每一列由星号或空格构成。因为函数传递了列高度和列中的星号数量两个参数，空白的数量应该是高度减去星号数量。给出空白数量和星号数量后，两个循环可以构造出这个list：
```emacs-lisp
;;; First version.
(defun column-of-graph (max-graph-height actual-height)
  "Return list of strings that is one column of a graph."
  (let ((insert-list nil)
        (number-of-top-blanks
         (- max-graph-height actual-height)))

    ;; Fill in asterisks.
    (while (> actual-height 0)
      (setq insert-list (cons "*" insert-list))
      (setq actual-height (1- actual-height)))

    ;; Fill in blanks.
    (while (> number-of-top-blanks 0)
      (setq insert-list (cons " " insert-list))
      (setq number-of-top-blanks
            (1- number-of-top-blanks)))

    ;; Return whole list.
    insert-list))
```
安装这个函数后，执行下面的代码：
```emacs-lisp
(column-of-graph 5 3)
```
将返回：
```emacs-lisp
(" " " " "*" "*" "*")
```

如上面所写，column-of-graph包含一个瑕疵：用于标识空白和列的符号是硬编码的，使用了空白和星号。这是一个很好的原型，如果其它人想换成其它的符号。比如用逗号代替空白，用加号代替星号等。程序应该更具弹性一些。应该使用两个变量来代替空白和星号：将graph-blank和graph-symbol定义为两个独立的变量。

上面也没有编写文档。我们可以编写这个函数的第二个版本：
```emacs-lisp
(defvar graph-symbol "*"
  "String used as symbol in graph, usually an asterisk.")

(defvar graph-blank " "
  "String used as blank in graph, usually a blank space.
graph-blank must be the same number of columns wide
as graph-symbol.")

;;(For an explanation of defvar, see Initializing a Variable with defvar.)

;;; Second version.
(defun column-of-graph (max-graph-height actual-height)
  "Return MAX-GRAPH-HEIGHT strings; ACTUAL-HEIGHT are graph-symbols.
The graph-symbols are contiguous entries at the end
of the list.
The list will be inserted as one column of a graph.
The strings are either graph-blank or graph-symbol."

  (let ((insert-list nil)
        (number-of-top-blanks
         (- max-graph-height actual-height)))

    ;; Fill in graph-symbols.
    (while (> actual-height 0)
      (setq insert-list (cons graph-symbol insert-list))
      (setq actual-height (1- actual-height)))

    ;; Fill in graph-blanks.
    (while (> number-of-top-blanks 0)
      (setq insert-list (cons graph-blank insert-list))
      (setq number-of-top-blanks
            (1- number-of-top-blanks)))

    ;; Return whole list.
    insert-list))

```
如果需要，我们可以再次重写column-of-graph，使用线型图表代替柱状图表。这不会很困难。其中一个办法就是让柱状图中第一个星号以下的显示为空白。在构造线型图表的一个列时，函数首先构造一个空的list，长度比元素的值小1，然后用cons将符号和列表连接；然后再次使用cons将顶部用空白填充。

现在，我们终于完成第一个打印图表的函数。它只打印了图表的body部分，而没有水平和垂直方向的轴，因此我们把这个函数称为graph-body-print。

## graph-body-print函数
上一节，graph-body-print函数完成了打印图表列的功能。这应该是一个重复执行的动作。我们可以使用递减的while循环或递归函数来完成这些操作。这节，我们使用while循环来编写函数定义。

column-of-graph函数需要图表高度作为参数，因此我们需要决定图表高度并将它保存到一个局部变量中。

我们的使用while循环的函数模板如下：
```emacs-lisp
(defun graph-body-print (numbers-list)
  "documentation..."
  (let ((height  ...
         ...))

    (while numbers-list
      insert-columns-and-reposition-point
      (setq numbers-list (cdr numbers-list))))
```

我们需要填空。

我们可以用`(apply 'max numbers-list) `获取图表的高度。

while循环遍历numbers-list。并用`(setq numbers-list (cdr numbers-list))`截短它。每次list的CAR值，就是传递给column-of-graph的参数。

每个循环周期中，insert-rectangle函数使用column-of-graph插入list。由于insert-rectangle函数将point移到了插入的矩形区域的右下解，我们需要保存当前point的位置，在插入矩形区域后恢复point的位置，然后将point水平移动到下一个列，并再次调用insert-rectangle。

如果被插入的列是一个字符宽（比如星号或一个空格），这个命令比较简单`(forward-char 1)`；但如果列宽超过1。这时命令需要写为`(forward-char symbol-width)`symbol-width是graph-blank的长度，可以使用`(length graph-blank)`。可以在let语句的变量列表中设置symbol-width变量。

函数定义如下：
```emacs-lisp
(defun graph-body-print (numbers-list)
  "Print a bar graph of the NUMBERS-LIST.
The numbers-list consists of the Y-axis values."

  (let ((height (apply 'max numbers-list))
        (symbol-width (length graph-blank))
        from-position)

    (while numbers-list
      (setq from-position (point))
      (insert-rectangle
       (column-of-graph height (car numbers-list)))
      (goto-char from-position)
      (forward-char symbol-width)
      ;; Draw graph column by column.
      (sit-for 0)
      (setq numbers-list (cdr numbers-list)))
    ;; Place point for X axis labels.
    (forward-line height)
    (insert "\n")
))
```

这里出现了一个新的函数`(sit-for 0)`。这个语句将使Emacs重绘屏幕。放在这里，Emacs将一列列的绘制。如果没有，Emacs在函数退出前都不会绘制。

我们可以使用一个较短的包含数字的list来测试graph-body-print。

 1. 安装graph-symbol,graph-blank,column-of-graph，graph-body-print。

 2. 复制下面的语句：
```emacs-lisp
(graph-body-print '(1 2 3 4 6 4 3 5 7 6 5 2 3))
```

 3. 切换到`*scratch*`缓冲区并把光标放置在要绘制的开始位置。

 4. 输入`M-:(eval-expresion)`

 5. Yank(C-Y) graph-body-print语句到缓冲区中。

 6.　回车执行graph-body-print语句。

Emacs将打印出下面的图表：
```
                    *
                *   **
                *  ****
               *** ****
              ********* *
             ************
            *************
```

## recursive-graph-body-print函数
graph-body-print函数也可以用递归来编写。递归分解为两个部分：外部使用let包装，决定几个变量的值，比如图表最大高度，内部的函数调用是递归调用，用于打印图表，

包装部分不复杂：
```emacs-lisp
(defun recursive-graph-body-print (numbers-list)
  "Print a bar graph of the NUMBERS-LIST.
The numbers-list consists of the Y-axis values."
  (let ((height (apply 'max numbers-list))
        (symbol-width (length graph-blank))
        from-position)
    (recursive-graph-body-print-internal
     numbers-list
     height
     symbol-width)))
```

递归函数部分有点复杂。它有四个部分：'do-again-test'打印操作的代码，递归调用，'next-step-expression'。'do-again-test'是一个if语句用于检查numbers-list是否还有元素，如果有函数将使用打印操作的代码打印一个列，并再次调用自身。函数调用自身时'next-step-expressin'将截短numbers-list。

```emacs-lisp
(defun recursive-graph-body-print-internal
  (numbers-list height symbol-width)
  "Print a bar graph.
Used within recursive-graph-body-print function."

  (if numbers-list
      (progn
        (setq from-position (point))
        (insert-rectangle
         (column-of-graph height (car numbers-list)))
        (goto-char from-position)
        (forward-char symbol-width)
        (sit-for 0)     ; Draw graph column by column.
        (recursive-graph-body-print-internal
         (cdr numbers-list) height symbol-width))))
```

在安装这个函数后，可以用下面的例子测试：
```emacs-lisp
(recursive-graph-body-print '(3 2 5 6 7 5 3 4 6 4 3 2 1))
```
结果如下：
```
                *
               **   *
              ****  *
              **** ***
            * *********
            ************
            *************
```

# .emacs文件

## Emacs的缺省配置
Emacs缺省配置的优点。Emacs在你编辑C文件时将启动C mod，编写Fortan源文件时启动Fortran mode，编写未知文件时使用Fundamental mod。这些都是自动检测的，不需要干预。

可以通过~/.emacs对Emacs进行定制。这是你个人的初始化文件；它的内容是Emacs Lisp代码。

## 全局初始化文件
除了个人初始化文件外，Emacs将自动加载全局初始化文件，这与.emacs文件一样，但它将被所有的用户加载。

有两个全局初始化文件site-load.el和site-init.el，在被加载到Emacs后被'dumped'（如果Emacs 'dumped'版本被创建，Dumped的Emacs复制版本加载更快）。但是，一旦文件被加载并被dumped，对文件的修改将不会影响Emacs除非你re-dump Emacs（详情，请查找INSTALL文件）。

有3个全局文件在每次启动Emacs时被执行（如果他们存在）。site-start.el在.emacs文件执行前执行，default.el和终端类型文件，这两上在.emacs加载后执行。

.emacs中的设置将覆盖site-start.el中的设置。default.el或终端类型文件将覆盖.emacs文件。（可以通过设置term-file-prefix为nil来防止与终端类型文件冲突）

发行版本中的INSTALL文件描述了site-init.el和site-load.el文件。

loadup.el,startup.el,loaddefs.el文件控制加载的过程。这些文件在Emacs发行版本的lisp目录中，值得精读。

loaddefs.el包含了大量设置.emacs文件或全局初始化文件的建议。

## 使用defcustom设置变量
可以使用defcustom以使用使用Emacs的customize功能设置变量的值。（不可以将customize用于函数定义；但可以在.emacs中使用defuns）实际上，可以在.emacs中写任何的Lisp语句。

customize功能取决于defcustom。忙乎你可以使用defvar或setq来设置变量，但defcustom是被设计为做此项工作的。

你可以将defvar的知识运用到defcustom的3个参数中。第一个参数是变量名称。第二个参数如果存在则表示变量实始值，并且这个值只会在变量未设置值时设置。第三个参数是文档字符串。

第四个和后面的参数是为defcustom设置类型和选项的；这些是defvar所没有的功能。(这些参数是可选的)

这些参数的每个值由键值对组成。每个键以一个字母开头：

举例来说，用户自定义变量text-mode-hook如下：
```emacs-lisp
(defcustom text-mode-hook nil
  "Normal hook run when entering Text mode and many related modes."
  :type 'hook
  :options '(turn-on-auto-fill flyspell-mode)
  :group 'data)
```
变量text-mode-hook；没有缺省值；并且它的文档字符串告诉你它起什么作用。

:type关键字告诉Emacs应该给text-mode-hook设置什么样的数据，在一个自定义缓冲区中如何显示它的值。

:options关键词，指定了一个备选值的列表。可以用于这个hook的:options。列表中的仅是建议值，并不是唯一备选值；人们可以设置为其它的任意值；:options关键字给用户提出了最合适的建议。

最后是:group关键字，它告诉Emacs的自定义命令将这个变量分到哪个组，以便于查找这个变量。

以text-mode-hook为例。

有两种方式来定制这个变量。你可以使用自定义变量的命令或者编写适当的语句。

使用自定义变量命令，可以输入：
```
M-x customize
```
找到对就的分组'data'。进入这个分组。TextMode Hook是第一个成员。你可以点击它的选项来设置它的值。最后点击下面的按钮
```
Save for Future Sessions
```
Emacs将会向.emacs文件中写入下面的语句：
```emacs-lisp
(custom-set-variables
  ;; custom-set-variables was added by Custom --
  ;;                           don't edit or cut/paste it!
  ;; Your init file should contain only one such instance.
 '(text-mode-hook (quote (turn-on-auto-fill text-mode-hook-identify))))
```
（text-mode-hook-identify函数告诉toggle-text-mode-auto-fill哪个缓冲区处于Text mode。）

你可以不用管警告信息来修改这些语句。警告的目的是为了恐吓那些不明白自己在做什么的人。

custom-set-variables的工作与setq不同。我从不去了解这些不同，我不手工修改.emacs中的custom-set-variables语句。

另一个custom-set-...函数是custom-set-faces。这个函数设置字体外观。

第二种定制text-mode-hook的方法是在.emacs中编写代码，与custom-set-...函数无关。

## 开始编写一个.emacs文件
启动Emacs时，将加载你的.emacs文件，除非你在命令行使用了-q命令（emacs -q）。

.emacs文件包含了Lisp语句。通常是设值语句，有时有函数定义。

这章将以作者的.emacs文件为例。

文件的第一个部分是注释：
```emacs-lisp
;;;; Bob's .emacs file
;; Robert J. Chassell
;; 26 September 1985
```
看看时间，在很久以前加的。

```emacs-lisp
;; Each section in this file is introduced by a
;; line beginning with four semicolons; and each
;; entry is introduced by a line beginning with
;; three semicolons.
```
这段描述是Emacs Lisp的习惯性注释方式。分号后面是注释。两个、三个或四个分号用于区分章节。

```emacs-lisp
;;;; The Help Key
;; Control-h is the help key;
;; after typing control-h, type a letter to
;; indicate the subject about which you want help.
;; For an explanation of the help facility,
;; type control-h two times in a row.
```
记住：输入C-h两次显示帮助。

```emacs-lisp
;; To find out about any mode, type control-h m
;; while in that mode.  For example, to find out
;; about mail mode, enter mail mode and then type
;; control-h m.
```
'Mode help'非常有用，它告诉你所有你需要知道的。

当然你不需要在你的.emacs文件包含这些。我添加这些只是为了记住Model help或者注释约定。

## Text 和 Auto Fill Mode
接下来到'tuns on' Text mode和Auto Fill mode。
```emacs-lisp
;;; Text mode and Auto Fill mode
;; The next three lines put Emacs into Text mode
;; and Auto Fill mode, and are for writers who
;; want to start writing prose rather than code.

(setq default-major-mode 'text-mode)
(add-hook 'text-mode-hook 'text-mode-hook-identify)
(add-hook 'text-mode-hook 'turn-on-auto-fill)
```

前面两行告诉Emacs在打开文件时，如果找不到对应的mode就打开Text mode。

当Emacs读取一个文件时，它查找文件的扩展名，如果有，如果以.c或.h结尾，Emacs开启C mode。Emacs也会检查文件的第一个非空白行；如果行上有`-*- C -*-`，Emacs也会开启C mode。Emacs处理了一个扩展名列表。In addition, Emacs looks near the last page for a per-buffer, "local variables list",if any.

现在，回到.emacs文件。

又出现了这行；它是如何工作的？
```emacs-lisp
(setq default-major-mode 'text-mode)
```
这行是一个完整的Emacs Lisp语句。

它使用了我们早已经熟悉的setq。它设置变量default-major-mode为text-mode。单引号告诉Emacs把text-mode直接作为变量。

接下来的两行是：
```emacs-lisp
(add-hook 'text-mode-hook 'text-mode-hook-identify)
(add-hook 'text-mode-hook 'turn-on-auto-fill)
```
这两行中，add-hook首先添加了text-mode-hook-identify到变量text-mode-hook中，然后添加了turn-on-auto-fill到这个变量中。

turn-on-auto-fill是程序名称，它开启Auto Fill mode。text-mode-hook-identify是一个函数，它告诉toggle-text-mode-auto-fill哪个缓冲区处于Text mode。

每次Emacs进入Text mode，Emacs将会执行'hooked'命令。因此，每次Emacs开启Text mode时，Emacs也将开启Auto Fill mode。

简单来说，第一行让Emacs在编辑文件时自动进入Text mode，除非文件扩展名或第一个非空行或局部变量能告诉Emacs该进入哪种mode。

Text mode中有其它动作，设置语法表以便于编写。在Text mode中，Emacs像处理信件一样把省略号当作单词的一部分；但Emacs不会把逗号或空白当作单词的一部分。因此M-f将移过it's。另一方面，在C mode中，M-f将在it's中t的后面停止。

第二和第三行将使Emacs在进入Text mode时开启Auto Fill mode。在Auto Fill mode中，Emacs自动换行，并将过长的部分移到下一行。Emacs会在单词之间换行，而不会把单词截断。

当Auto Fill mode关闭时，文件中的行将与输入时保持一致。取决于trucate-lines变量的值，你输入的单词有可能消失在屏幕的右边，也有可以显示以非常乱的方式显示，也有可能显示为一个非常长的行。

另外，在我的.emacs文件的这一部分，我告诉Emacs在分号后添加两个空格：
```emacs-lisp
(setq colon-double-space t)
```

## 邮件别名
这里使用setq开启邮件别名，也有一些用于提醒的注释。
```emacs-lisp
;;; Mail mode
;; To enter mail mode, type `C-x m'
;; To enter RMAIL (for reading mail),
;; type `M-x rmail'

(setq mail-aliases t)
```
setq命令设置变量mail-aliases为t。因为t表示true，这行就是在说"Yes,use mail aliases."

邮件别名是一种email地址的缩写。别名保存在~/.mailrc中。你可以这样书写：
```
alias geo george@foobar.wiz.edu
```
当你给George发邮件时，地址可以输入geo；邮件发送者将自动将geo展开为完整的邮箱地址。

## Indent Tabs Mode
缺省情况下，Emacs在格式化一个区域时会在需要空白的位置插入tab。（比如在需要缩进时）。Tab在使用终端或普通打印机时看起来很正常，但如果是在TeX或Texinfo中就会不正常。因为TeX将忽略tab。

下面的代码关闭Tabs mode：
```emacs-lisp
;;; Prevent Extraneous Tabs
(setq-default indent-tabs-mode nil)
```
注意，这里使用了setq-default而不是使用setq。setq-default命令只会在局部变量没有值时设置这个变量的值。

## 一些按键绑定
下面是一些个性化的按键绑定：
```emacs-lisp
;;; Compare windows
(global-set-key "\C-cw" 'compare-windows)
```
compare-window将比较当前窗口中的文本和下一个窗口中的文本。

这里也显示了如何设置一个全局按键绑定，它在任何mode下都有效。

命令global-set-key后面跟按键绑定。在.emacs文件中，按键绑定被书写为：`\C-c`表示'control-c'，表示'按住control键的同时按c键'。w表示'按w键'。按键设置用双引号包含。在编写文档的时候，你可以写成C-c w。（如果绑定的键是<META>键，比如M-c则书写为`\M-c`）

这个按键组成将调用compare-windows命令。注意，compare-windows前面有一个单引号；如果不加Emacs将对它求值。

三件事：双引号，C前面的反余线和单引号。

这里还有另一个按键绑定：
```emacs-lisp
;;; Keybinding for `occur'
;; I use occur a lot, so let's bind it to a key:
(global-set-key "\C-co" 'occur)
```
occur命令显示当前缓冲区中匹配某个正则表达式的所有行。匹配的行被显示在`*Occur*`缓冲区中。

下面演示了如何取消一个按键绑定：
```emacs-lisp
;;; Unbind `C-x f'
(global-unset-key "\C-xf")
```
取消这个绑定的原因是：我经常在需要输入C-x C-f时输入了C-x f。

下面的语句重新设置了一个已经存在的绑定：
```emacs-lisp
;;; Rebind `C-x C-b' for `buffer-menu'
(global-set-key "\C-x\C-b" 'buffer-menu)
```
缺省情况下C-x C-b执行list-buffer命令。这个命令在另一个window中列出缓冲区。因为我几乎一直都需要在那个窗口中做一些操作，我比较喜欢buffer-menu命令，它不只是列出缓冲区，也会将point移到那个窗口中。

## Keymaps
Emacs使用keymaps记录按键与命令的对应关系。当使用global-set-key设置按键绑定时，就是在current-global-map中指定了一个按键绑定。

特殊的模式下，比如C mode或Text mode，有他们自己的按键绑定；它将覆盖全局keymap。

global-set-key函数用于绑定或重新绑定全局keymap。比如，下面的代码将C-x C-b绑定到buffer-menu函数：
```emacs-lisp
(global-set-key "\C-x\C-b" 'buffer-menu)
```

特殊模式下的keymap用defin-key设置，它接收一个指定的keymap作为参数，还有按键组合和命令。比如，我的.emacs文件包含下面的语句绑定textinfo-insert-@group命令到C-c C-c g：
```emacs-lisp
(define-key texinfo-mode-map "\C-c\C-cg" 'texinfo-insert-@group)
```
text-info-insert-@group函数是一个Texinfo mode下的扩展，它用于在Texinfo文件中插入@group标记。我可以用三次按键C-c C-c g来输入，而不需要按六个键@ g r o u p。（@group与@end匹配，group命令用于保持它所包含的文本被放在同一页上）

下面是texinfo-insert-@group函数的定义：
```emacs-lisp
(defun texinfo-insert-@group ()
  "Insert the string @group in a Texinfo buffer."
  (interactive)
  (beginning-of-line)
  (insert "@group\n"))
```
（当然，我也可以用Abbrev来完成类似工作，而不需要编写一个函数来插入单词；但是我更喜欢与Texinfo mode的其它按键保持一致。）

在loaddefs.el中你可以在各种mode中看到无数多的define-key语句，比如cc-mode.el和lisp-mode.el中。

## 加载文件
很多GNU Emacs社区的人们都自己编写Emacs的扩展。随着时间的推移，这些扩展通常都会出现新的版本。比如，Calendar和Diary包现在已经变成了GNU Emacs标准发行包中的一部分了。

可以使用load命令来执行整个文件，而将文件中的函数和变量设置安装到Emacs中。比如：
```emacs-lisp
(load "~/emacs/slowsplit")
```

它个语句执行，或者说加载了slowsplit.el这个文件（如果文件存在），或者加载编译过的slowsplit.elc文件。这个文件包含了split-window-quietly函数，它是John Robinson于1989年编写的。

split-window-quietly函数在分隔窗口时，只使用了少量的重绘。我在1989年安装了它因为它与当时我使用的慢速的1200 baud终端工作得很好。现在很少遇到这种慢速连接了，但我仍然使用这个函数，因为我喜欢这种方式：缓冲区的下半部分在下面的新窗口中，而缓冲区的上半部分在上面的窗口中。

为了替换split-window-vertically的缺省按键绑定，你需要先取消split-window-quietly的按键绑定，如下：
```emacs-lisp
(global-unset-key "\C-x2")
(global-set-key "\C-x2" 'split-window-quietly)
```

如果要加载很多扩展，你需要指定扩展文件所在的位置，需要将扩展所在目录添加到Emacs的load-path中。在Emacs加载文件时，它将搜索这个目录列表中的目录。（缺省的列表在Emacs构建时在paths.h中指定。）

下面的命令将你的~/emacs目录添加到load-path中：
```emacs-lisp
;;; Emacs Load Path
(setq load-path (cons "~/emacs" load-path))
```

load-library是一个交互式的load函数。完整的函数如下：
```emacs-lisp
(defun load-library (library)
  "Load the library named LIBRARY.
This is an interface to the function `load'."
  (interactive "sLoad library: ")
  (load library))
```
load-library函数的名称来自于将'file'称为'library'。load-library命令在files.el中。

另一个交互式命令load-file完成的工作有些许不同。

## 自动加载
与通过加载文件的方式或者执行函数定义等方式加载函数不同，可以使用函数在被调用时自动加载。这被称作自动加载（autoloading）。

当执行自动加载函数时，Emacs自动执行文件中包含定义然后调用这个函数。

使用自动加载可以使Emacs启动得更快一些，因为库没有被立即加载；但是在第一次执行函数时，在加载对应的文件时需要稍等一下。

那些使用得较少的函数通常使用自动加载。loaddefs.el库包含了数百个自动加载函数，从bookmark-set到wordstar-mode。当然，如果有可能经常需要使用一些'罕见'的函数，可以在.emacs文件中使用load语句加载它。

autoload是一个内置函数可以传递5个参数，最后三个是可选的。第一个参数是需要自动加载的函数名称；第二个参数是要加载的文件名。第三个参数是函数的文档，第四个用于说明这个函数是否可以以交互的方式运行。第五个参数说明对象的类型——autoload可以处理按键或者宏或者函数（缺省是函数）。

下面是一个典型的例子：
```emacs-lisp
(autoload 'html-helper-mode
  "html-helper-mode" "Edit HTML documents" t)
```
（html-helper-mode是html-mode的另一选择，它是标准发行版的一部分）

自动加载html-helper-mode函数。它将从html-helper-mode.el（或从编译过的html-helper-mode.elc）加载。这个文件必须位于load-path指定的目录列表中。文档字符串说明这个mode是用于编辑html文件的。你可以以交互的方式输入M-x html-helper-mode来执行。（你需要在这里提供文档字符串，虽然函数定义中有，但在这里函数还没有加载，它的文档字符串还不可用）

## 一个简单的扩展：line-to-top-of-window
这里是一个简单的Emacs扩展它将point移到窗口的顶部。

你可以将下面的代码放到独立的文件中，然后在.emacs文件中加载，或者你可以在.emacs文件中直接包含这些代码。

定义如下：
```emacs-lisp
;;; Line to top of window;
;;; replace three keystroke sequence  C-u 0 C-l
(defun line-to-top-of-window ()
  "Move the line point is on to top of window."
  (interactive)
  (recenter 0))
```

现在设置按键绑定。

现在，功能键和鼠标按键事件和非ASCII字符写在方括号中，不需要使用引号。（在Emacs 18或以前的版本中，你需要为不同的终端编写不同的功能键绑定）

我们将line-to-top-of-window绑定到<F6>功能键上。
```emacs-lisp
(global-set-key [f6] 'line-to-top-of-window)
```

如果你运行有两个版本的GNU Emacs，比如20和21，并使用同一个.emacs文件，你可以使用下面的方法选择执行不同的代码：
```emacs-lisp
(cond
 ((string-equal (number-to-string 20) (substring (emacs-version) 10 12))
  ;; evaluate version 20 code
  ( ... ))
 ((string-equal (number-to-string 21) (substring (emacs-version) 10 12))
  ;; evaluate version 21 code
  ( ... )))
```
比如，在21版中光标缺省是闪烁的。我不喜欢这种效果。
```emacs-lisp
(if (string-equal "21" (substring (emacs-version) 10 12))
    (progn
      (blink-cursor-mode 0)
      ;; Insert newline when you press `C-n' (next-line)
      ;; at the end of the buffer
      (setq next-line-add-newlines t)
      ;; Turn on image viewing
      (auto-image-file-mode t)
      ;; Turn on menu bar (this bar has text)
      ;; (Use numeric argument to turn on)
      (menu-bar-mode 1)
      ;; Turn off tool bar (this bar has icons)
      ;; (Use numeric argument to turn on)
      (tool-bar-mode nil)
      ;; Turn off tooltip mode for tool bar
      ;; (This mode causes icon explanations to pop up)
      ;; (Use numeric argument to turn on)
      (tooltip-mode nil)
      ;; If tooltips turned on, make tips appear promptly
      (setq tooltip-delay 0.1)  ; default is one second
       ))
```
（注意这里没有使用`(number-to-string 21)`，没有使用函数将整数转化为字符串。短的表达式比长的更好，但`(number-to-string 21)`更通用。然而如果你不知道前面返回值的类型时，就需要使用number-to-string函数了。）

## X11颜色
在MIT X Windowing系统上使用Emacs时可以指定颜色。

我不喜欢缺省的颜色而指定了自己的颜色。

.emacs中的这些语句指定了这些值：
```emacs-lisp
;; Set cursor color
(set-cursor-color "white")

;; Set mouse color
(set-mouse-color "white")

;; Set foreground and background
(set-foreground-color "white")
(set-background-color "darkblue")

;;; Set highlighting colors for isearch and drag
(set-face-foreground 'highlight "white")
(set-face-background 'highlight "blue")

(set-face-foreground 'region "cyan")
(set-face-background 'region "blue")

(set-face-foreground 'secondary-selection "skyblue")
(set-face-background 'secondary-selection "darkblue")

;; Set calendar highlighting colors
(setq calendar-load-hook
      '(lambda ()
         (set-face-foreground 'diary-face   "skyblue")
         (set-face-background 'holiday-face "slate blue")
         (set-face-foreground 'holiday-face "white")))
```

不同色调的蓝色防止人感觉屏幕的闪烁。

另一种选择是在X初始化文件中指定彩色。比如，可以在~/.Xresources文件中设置前景色、背景色、光标和指针颜色等：
```
Emacs*foreground:   white
Emacs*background:   darkblue
Emacs*cursorColor:  white
Emacs*pointerColor: white
```

这并不是Emacs的一部分，还可以在~/.xinitrc文件中指定X window根窗口的颜色：
```
# I use TWM for window manager.
xsetroot -solid Navy -fg white &
```

## .emacs中的杂项设置
一些杂项设置：

 - 设置鼠标光标的颜色和外观：
```emacs-lisp
;; Cursor shapes are defined in
;; `/usr/include/X11/cursorfont.h';
;; for example, the `target' cursor is number 128;
;; the `top_left_arrow' cursor is number 132.

(let ((mpointer (x-get-resource "*mpointer"
                                "*emacs*mpointer")))
  ;; If you have not set your mouse pointer
  ;;     then set it, otherwise leave as is:
  (if (eq mpointer nil)
      (setq mpointer "132")) ; top_left_arrow
  (setq x-pointer-shape (string-to-int mpointer))
  (set-mouse-color "white"))
```

## 状态栏(Modified Mode Line)
当我在网络中工作时，会忘记使用的是哪台机器。也有可能忘记point位于什么位置。

因此我重置了mode line：
```
-:-- foo.texi   rattlesnake:/home/bob/  Line 1  (Texinfo Fill) Top
```
表示访问的文件名为foo.texi，在rattlesnake这台机器的/home/bob缓冲区中。位于第一行，处于Texinfo mode，位于缓冲区的顶部。

.emacs文件中有如下的部分：
```emacs-lisp
;; Set a Mode Line that tells me which machine, which directory,
;; and which line I am on, plus the other customary information.
(setq default-mode-line-format
 (quote
  (#("-" 0 1
     (help-echo
      "mouse-1: select window, mouse-2: delete others ..."))
   mode-line-mule-info
   mode-line-modified
   mode-line-frame-identification
   "    "
   mode-line-buffer-identification
   "    "
   (:eval (substring
           (system-name) 0 (string-match "\\..+" (system-name))))
   ":"
   default-directory
   #(" " 0 1
     (help-echo
      "mouse-1: select window, mouse-2: delete others ..."))
   (line-number-mode " Line %l ")
   global-mode-string
   #("   %[(" 0 6
     (help-echo
      "mouse-1: select window, mouse-2: delete others ..."))
   (:eval (mode-line-mode-name))
   mode-line-process
   minor-mode-alist
   #("%n" 0 2 (help-echo "mouse-2: widen" local-map (keymap ...)))
   ")%] "
   (-3 . "%P")
   ;;   "-%-"
   )))
```

这里重定义了缺省的mode line。多数设置来自于原始值；但作了一些修改。设置了default mode line format以便支持多种mode，比如Info。

列表中的很多元素是自描述的：mode-line-modified是一个变量，它说明了缓冲区是否被修改了，mode-name说明mode的名称，等等。format看起来复杂一些，因为它使用了两个我们没有讨论过的功能。

mode line字符串的第一行是一个短线-。在原来，它只能是一个简单的"-"。但现在，Emacs允许给字符串添加属性，比如高亮，或者像这里一样，是一个帮助功能。如果你将鼠标光标放在短线上，一些帮助信息将会显示出来。（缺省情况下，你需要等1秒。你也可以通过修改tooltip-delay变量来修改这个时间。）

新的字符串有一个特定的格式：
```
#("-" 0 1 (help-echo "mouse-1: select window, ..."))
```
`#(`开头的list。第一个元素是字符串本身，只有一个"-"。第二个和第三个元素指定第四个元素的应用范围。范围从一个字符后面开始，0表示从第一个字符之前开始；1表示范围在第一个字符后面结束。第三个元素是范围的属性。它包含了一个属性列表，属性名help-echo，后面跟了一个属性值，是一个字符串。第二、三和四个元素可以重复出现。

mode-line-buffer-identification显示当前缓冲区名称。它是以`(#("%12b" 0 4 .... `开头的list。

"%12b"显示缓冲区的名称，使用buffer-name函数；'12'设置了最大显示的字符数量。当名称的长度小于这个长度时会将空白添加到字符串中。（缓冲区名称通常大于12个字符，这个长度在典型的80列的窗口中工作得很好）

:eval是GNU Emacs 21中的新功能。它执行后面的语句交把结果作为字符串显示。在这里，这个语句显示完整的系统名称的第一个部分。第一个部分的结束位置是一个'.'，因此使用了string-match函数计算第一个部分的长度。substring取从0到那个位置的字符串。

语句如下：
```emacs-lisp
(:eval (substring
        (system-name) 0 (string-match "\\..+" (system-name))))
```

%[和%]这对括号显示每个递归编辑的层次。%n表示'Narrow'（在narrowed时）。%P表示窗口底部上缓冲区的百分比，或者'Top'或'Bottom'或'All'。（小写的p表示离窗口顶部上的百分比。）%-插入用于填充的连字符。

如果想要在启动时不加载~/.emacs，可以使用：
```
emacs -q
```

# 调试
GNU Emacs中有两个高度器，debug和edebug。第一个是Emacs内建的可以随时使用它；第二个需要借助一些函数才能使用。

## debug
假设你编写了用于加1的函数。但函数有个bug。你误将1-输入为1=了。函数定义如下：
```emacs-lisp
(defun triangle-bugged (number)
  "Return sum of numbers 1 through NUMBER inclusive."
  (let ((total 0))
    (while (> number 0)
      (setq total (+ total number))
      (setq number (1= number)))      ; Error here.
    total))
```
当传递4给这个函数时：
```emacs-lisp
(triangle-bugged 4)
```
在Emacs 21中，将产生一个*Backtrace*缓冲区，并进入这个缓冲区：
```
---------- Buffer: *Backtrace* ----------
Debugger entered--Lisp error: (void-function 1=)
  (1= number)
  (setq number (1= number))
  (while (> number 0) (setq total (+ total number))
        (setq number (1= number)))
  (let ((total 0)) (while (> number 0) (setq total ...)
    (setq number ...)) total)
  triangle-bugged(4)
  eval((triangle-bugged 4))
  eval-last-sexp-1(nil)
  eval-last-sexp(nil)
  call-interactively(eval-last-sexp)
---------- Buffer: *Backtrace* ----------
```
（重新格式化了一下；调试不会自动折行。可以用q退出调试器）

实际上，像这样简单的bug，'Lisp error'这行告诉了我们如何修改定义。函数1=为'void'。

在Emacs 20中，你将看到：
```
Symbol's function definition is void: 1=
```
这与21版中的*Backtrace*缓冲区中的意思是一样的。

假设你还不是很清楚要如何做？你可以阅读完整的回溯信息。

在GNU Emacs 21中，它将自动启动调试器，并将信息放到*Backtrace*缓冲区中；如果有使用Emacs21，可能需要按下面的方法手工启动调试器。

在*Backtrace*中从下向上读；它说明了Emacs是如何出错的。Emacs执行了一个交互式命令C-x C-e(eval-last-sexp)，它执行了triangle-bugged语句。上面的每一行显示了Lisp解释器执行内容。

缓冲区的顶部是:
```emacs-lisp
(setq number (1= number))
```

Emacs试图执行这个语句；依次来执行，它首先执行内部的语句：
```emacs-lisp
(1= number)
```

这里发生了错误，如错误信息所说：
```
Debugger entered--Lisp error: (void-function 1=)
```

你可以修正这个错误，然后重新执行函数定义，再运行测试代码。

## debug-on-entry
GNU Emacs 21在函数出错时自动启动了调试器。GNU Emacs 20不会这样做；它只显示一条出错信息。你需要手工启动调试器。

手工启动的好处是在程序没有bug的时候也可以调试。

你可以调用debug-on-entry函数进入调试器。

输入:
```
M-x debug-on-entry RET triangle-bugged RET
```

然后，执行下面的语句：
```emacs-lisp
(triangle-bugged 5)
```
所有版本的Emacs都将产生一个*Backtrace*缓冲区告诉你它将执行triangle-debugged函数：
```
---------- Buffer: *Backtrace* ----------
Debugger entered--entering a function:
* triangle-bugged(5)
  eval((triangle-bugged 5))
  eval-last-sexp-1(nil)
  eval-last-sexp(nil)
  call-interactively(eval-last-sexp)
---------- Buffer: *Backtrace* ----------
```
在*Backtrace*缓冲区中输入d。Emacs将执行triangle-bugged的第一行语句；缓冲区看起来如下：
```
---------- Buffer: *Backtrace* ----------
Debugger entered--beginning evaluation of function call form:
* (let ((total 0)) (while (> number 0) (setq total ...)
        (setq number ...)) total)
* triangle-bugged(5)
  eval((triangle-bugged 5))
  eval-last-sexp-1(nil)
  eval-last-sexp(nil)
  call-interactively(eval-last-sexp)
---------- Buffer: *Backtrace* ----------
```

现在，再次输入d，连续8次慢慢的输入d，Emacs将执行函数定义的另一个语句。

最后缓冲区看起来如下：
```
---------- Buffer: *Backtrace* ----------
Debugger entered--beginning evaluation of function call form:
* (setq number (1= number))
* (while (> number 0) (setq total (+ total number))
        (setq number (1= number)))
* (let ((total 0)) (while (> number 0) (setq total ...)
        (setq number ...)) total)
* triangle-bugged(5)
  eval((triangle-bugged 5))
  eval-last-sexp-1(nil)
  eval-last-sexp(nil)
  call-interactively(eval-last-sexp)
---------- Buffer: *Backtrace* ----------
```
最后再输入两次d，Emacs将到达错误的位置，*Backtrace*缓冲区顶部的两行将显示：
```
---------- Buffer: *Backtrace* ----------
Debugger entered--Lisp error: (void-function 1=)
* (1= number)
...
---------- Buffer: *Backtrace* ----------
```

输入d可以单步执行函数。

可以输入q退出*Backtrace*缓冲区；这将退出跟踪，但并不会退出debug-on-entry。

要退出debug-on-entry，需要调用cancel-debug-on-entry并输入函数名称：
```
M-x cancel-debug-on-entry RET triangle-bugged RET
```

## debug-on-quit和(debug)
除了debug-on-error或调用debug-on-entry，还有另外两种方法启动debug。

可以通过将变量debug-on-quit设置为t，随时输入C-g(keyboard-quit)来启动debug。这在调试无限循环时很用效。

或者，你可以在代码中插入(debug)以启动调试器，比如：
```emacs-lisp
(defun triangle-bugged (number)
  "Return sum of numbers 1 through NUMBER inclusive."
  (let ((total 0))
    (while (> number 0)
      (setq total (+ total number))
      (debug)                         ; Start debugger.
      (setq number (1= number)))      ; Error here.
    total))
```

## edebug源码级的调试器
Edebug是一个源码级的调试器。Edebug通常显示你要调试的源码，并在左边用箭头指出当前执行的行。

你可以单步执行函数，或者快速的执行到断点位置。

下面是tringle-recursively的调试函数：
```emacs-lisp
(defun triangle-recursively-bugged (number)
  "Return sum of numbers 1 through NUMBER inclusive.
Uses recursion."
  (if (= number 1)
      1
    (+ number
       (triangle-recursively-bugged
        (1= number)))))               ; Error here.
```
同样，你可以在函数定义后面使用C-x C-e(eval-last-sexp)安装函数，或者将光标放到定义的内部输入C-M-x(eval-defun)。（缺省情况下，eval-defun命令只在Emacs Lisp或Lisp交互模式下才可以工作。）

但是，为了使用Edebug调试函数，你必须使用另一个命令。可以将停留在函数内部然后输入
```
M-x edebug-defun RET
```

这将使Emacs自动加载Edebug。在加载完成后，可以将光标放在下面语句的后面输入C-x C-e(eval-last-sexp):
```emacs-lisp
(triangle-recursively-bugged 3)
```
将跳到triangle-recursively-bugged的源码，光标被设置在函数if语句所在的开始行。并且，可以在这行的左边看到一个箭头。箭头标明了函数当前执行的位置。（在例子中，我们使用=>代替；在窗口系统中，你可以看到一个实心的三角形）
```
=>-!-(if (= number 1)
```
在这里，point的位置显示为-!-。

如果你输入<SPC>，point将移到下一个语句；这行将显示如下：
```
=>(if -!-(= number 1)
```

如果继续输入<SPC>，point将继续从一个语句移到另一个语句。每次只要语句返回了值，它都会显示到回显区。比如，在point移过number时，你将看到：
```
Result: 3 = C-c
```
这表示number的值为3，它的ASCII值是'control-c'。

你可以继续执行，直到错误的位置。在执行之前，这行如下：
```
=>        -!-(1= number)))))               ; Error here.
```

当再次输入<SPC>时，将产生错误信息：
```
Symbol's function definition is void: 1=
```

输入q退出Edebug。

要从函数上移除调试的机制，可以重新使用C-x C-e执行函数定义。

Edebug除了跟踪执行外可以做更多的工作。你可以设置它在遇到错误时停止；可以让它显示或修改变量的值；你可以查找出函数被执行了多少次，等等。

# 终结
