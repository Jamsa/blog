---
title: "gawk笔记"
date: 2007-06-19
modified: 2007-06-19
categories: ["效率"]
tags: ["awk","linux"]
---

# I.简介
gawk的主要功能是针对档案的第一行搜寻指令的patterns。当一行里有符合指定的patterns，gawk就会在此行执行指定的actions。gawk依此方式处理输入档案的每一行直到输入档案结束。
gawk程序由很多的pattern与action所组成，action写在大括号{}里面。一个pattern后面就跟着一个action。整个gawk程序像下面的样子：
pattern {action}
pattern {action}
在gawk程序里面，pattern和action都能被省略，但是不能两个同时省略。如果pattern被省略，对于文件中的每一行，action都会被执行。如果action被省略，内定的action则会打印出所有符合pattern的输入行。

## 1.执行gawk程序

有两种方式
### a.写在命令行
```
gawk 'program' input-file1 input-file2 ...
```
### b.写在单独的程序文件中
```
gawk -f program-file input-file1 input-file2 ...
```
当程序文件不止一个时，可以写成
```
gawk -f program-file1 -f program-file2 ... input-file1 input-file2 ...
```

## 2.一个简单的例子
```
gawk '/foo/{print $0}' BBS-list
```
实际的gawk程序为/foo/{print $0}，/foo/为pattern，意为搜索文件里的每一行是否含有子字串'foo'，如果含有'foo'则执行action。action为print $0，表示将现在这一行的内容打印出来。BBS-list是要处理的文件名。

## 3.一个较复杂的例子
```
gawk '$1 == "Feb" {sum=$2+$3}END{print sum}' shipped
```
这个例子会将输入文件shipped的第一个栏位与"Feb"做比较，如果相等，则其对应的第2栏位与第3栏位的值会被加到变量sum。对于输入文件中的每一行重复上述动作，直到输入文件的每一行都被处理过为止。最后将sum的值打印出来。END{print sum}的意思为在所有的输入读完之后，执行一次print sum的动作，也就是把sum的值打印出来。

# II.读入输入文件
gawk的输入可以从标准输入或指定的文件里读取。输入的读取单位被称为"记录"(records)，gawk在做处理时，是一个记录一个记录地处理。每个记录的内定值是一行(line)，一个记录又被分为多个栏位(fields)。

## 1.如何将输入分解成记录(records)
gawk语言会把输入分解成记录(records)。记录与记录之间是以record separator隔开，record separator的内定值是表示新一行的字符(newline character)，因此内定的record separator使得文字的每一行是一个记录。
record separator随着内置的缺省变量RS的改变而改变。RS是一个字符串，它的内定值是"\n"。仅有RS的第一个字符是有效的，它被当作record separator，而RS的其它字符将被忽略。
内置变量FNR会储存当前的输入文件已经被读取的记录数量。内置变量NR会存储
目前为止所有的输入文件
已经被读取的记录个数。

## 2.栏位(field)
gawk会自动将每个记录分解成多个栏位(field)。类似于字母在一行里面，gawk的内定动作会认为栏位之间是以whitespace分开。在gawk里，whitespace的意思是一个或多个空白或者tabs。
在gawk程序里面，以'$1'表示第一个栏位，'$2'表示第二个栏位，依次类推。举例来说：
```
This seems like a pretty nice example.
```
第一个栏位或$1是"This"，第二个栏位或$2是"seems"，依次类推。特别要注意的是第七个栏位或$7是'example.'，而非'example'。
不论有多少个栏位，$NF可以用来表示一个记录的最后一个栏位。上面的例子中$NF与$7相同，也就是'example.'。
NF是一个内置变量，它的值表示目前这个记录的栏位个数。
$0，是一个特例，它表示整个记录不。
一个比较复杂的例子：
```
gawk '$1~/foo/{print $0}' BBS-list
```
这个例子是把输入文件BBS-list的每个记录的第一个栏位检查，如果它含有字符串'foo'，则这一个记录会被打印出来。

## 3.如何将记录分解成栏位
gawk根据field separator将一个记录分解成栏位。field separator以内置变量FS表示。
举例来说，假如field separator是'foo'，则下面的行:
```
moo goo gai pan
```
会被分成三个栏位：'m'、'g'、'gai pan'。
在gawk程序里，可以使用`'='`来改变FS的值。例如：
```
gawk 'BEGIN{FS=","};{print $2}'
```
输入行如下：
```
John Q.Smith,29 Oak St.,Walamazoo,MI 42139
```
执行gawk的结果将打印出子串'29 Oak st.'。BEGIN后面的action会在第一个记录被读取之前执行一次。

# III.打印
在gawk程序里，actions最常做的事情就是打印(printing)。简单的打印，使用print。复杂格式的打印，使用printf。
a.print用在简单、标准的输出格式。格式如下：
```
print item1,item2,...
```
输出时，各个item之间会以一个空白分开，最后会换行(newline)。
如果'print'之后没有跟任务参数，它与'print $0'的效果一样，它会打印出现在的记录(record)。要打印出空白行可以使用'print ""'。打印出一段固定的文字，可以用双引号将文字的两边括起来，例如：
```
'print "Hello there"'。
```
下例，会把每个输入记录的前两个栏位打印出来：
```
gawk '{print $1,$2}' shipped
```

## 1.输出分隔符
前面说过如果print时包含有多个item，item之间用逗号分开，则打印出时各个item会被一个空白隔开。你可以使用任务字符串作为output field separator，可以经由内置参数OFS的设定值来更改output field separator。OFS的初始值为" "，即一个空格。
整个print的输出被称为output record。print输出output record之后，会接着输出一个之串，此字符串称为output record separator。内置参数ORS来指定此字符串。ORS的初始值为"\n"，也就是换行。
下面这个例子会打印出每个记录的第一个栏位和第二个栏位，此二个栏位之间以分号';'分开，每行输出之后会加入一个空白行。
```
gawk 'BEGIN {OFS=";"; ORS="\n\n"}{print $1,$2}' BBS-list
```

## 2.printf
printf会使得输出格式容易精确地控制。printf可以指定每个item打印出的宽度，也可以指定数字的各种型式。
printf的格式如下：
```
printf format,item1,item2,...
```
print与printf的差别是在于format，printf的参数比print多了字符串format。format的型式与ANSI C的printf的格式相同。
printf并不会做自动换行动作。内置变量OFS与ORS对printf无效。

# IV.pattern的种类
这里对gawk的各种pattern形式作一次整理：
```
/regular expression/
```
一个正则表达式当作一个pattern。每当输入记录(record)含有regulare expression就视为符合。

expression
一个单一的expression。当一个值不为0或者一个字符串不是空的则可视为符合。

pat1,pat2
一对patterns以逗号分开，指定记录的范围。

BEGIN
END
这是特别的pattern，gawk在开始执行或要结束时会分别执行相对就于BEGIN或END的action。

null
这是一个空的pattern，对于每个输入记录都视为符合pattern。

## 1.Regular Expression当作Patterns
一个regular expression可简写为regexp，是一种描述字串的方法。一个regular expression以斜线('/')包围当作gawk的pattern。
如果输入记录含有regexp就视为符合。例如：pattern为/foo/，对于任何输入记录含有'foo'则视为符合。
下例会将含有'foo'的输入记录的第2上栏位打印出来：
```
gawk '/foo/{print $2}' BBS-list
```
regexp也能使用在比较运算中
```
exp ~ /regexp/
```
如果exp符合regexp，则结果为真(true)。
```
exp !~ /regexp/
```
如果exp不符合regexp，则结果为真。

## 2.比较运算当作Patterns
比较的pattern用来测试两个数字或字符串的关系诸如大于、等于、小于。下面列出一些比较的pattern：
```
x<y
x<=y
x>y
x>=y
x==y
x!=y
x~y
x!~y
```
上面提到的x与y，如果二者皆是数字则视为数字之间的比较，否则它们会被转换成字符串且以字符串的形式做比较。两个字符串比较，会先比较第一个字符，然后比较第二个字符，依此类推，直到有不同的地方出现为止。如果两个字符串在较短的一个结束之前是相等，则视为长的字符串比短的字符串大。例如"10"比"9"小，"abc"比"abcd"小。

## 3.使用布尔运算的Patterns
一个布尔pattern是使用布尔运算"||"、"&&"、"!"来组合其它的pattern。
例如：
```
gawk '/2400/&&/foo/' BBS-list
gawk '/2400/||/foo/' BBS-list
gawk '! /foo/' BBS-list
```

# V.表达式(Expression)作为Action
表达式(Expression)是gawk程序里action的基本构成者。

## 1.算术运算
gawk里的算术运算如下所示：
```
x+y
x-y
-x
+x
x*y
x/y
x%y
x^y
x**y
```

## 2.比较表达式与布尔运算
比较运算(Comparison expression)用来比较字符串或数字的关系，运算符号与C语言相同。列表如下：
```
x<y
x<=y
x>=y
x==y
x!=y
x~y
x!~y
```
比较结果为真(true)则其值是1，否则为0。
布尔运算(boolean expression)有下面三种：
```
boolean1 && boolean2
boolean1 || boolean2
! boolean
```

## 3.条件表达式(Conditional Expressions)
一个条件运算式是一种特别的算式，它含有3个运算符，条件式运算与C语言的三目运算相同：
```
selector ? if-true-exp : if-flase-exp
```

# VI.Actions里面的流程控制
在gawk程序里，流程控制如：if、while等与C语言类似。
很多的控制语句会包括其它的语句，被包括的语句被称为body。假如body里包括一个以上的语句，必须以大括号{}将这些语句括冬候鸟来，而各个语句之间需要以换行(newline)或分号隔开。

## 1.if语句
```
if (condition) then-body [else else-body]
```
如果condition为真，则执行then-body，否则执行else-body
例：
```
if(x % 2 == 0)
print "x is even"
else
print "x is odd"
```

## 2.while语句
```
while(condition)
body
```
while语句做的第一件事就是测试condition，假如condition为真则执行body中的语句，执行完后再测试condition，直到为false。如果第一次测试时condition就为false，则body中的语句从不会被执行。
下面的例子打印出每个输入记录(record)的前三个栏位。
```
gawk '{i=1
while(i<=3){
print $i
i++
}
}'
```

## 3.do-while语句
```
do
body
while(condition)
```
这个do loop执行body一次，然后只要condition是true则会重复执行body。即使开始时conditon为false，body也会执行一次。
```
gawk '{i=1
do{
print $0
i++
}while(i<=10)
}'
```

## 4.for语句
```
for(initialization;condition;increment)
body
```
此语句开始时会执行initialization，然后只要condition是true，它会重复执行body与做increment。
下面的例子会打印出每个输入记录的前三个栏位：
```
gawk '{for(i=1;i<=3;i++)
print $i
}'
```

## 5.break语句
break语句会跳出包含它的for,while,do-while循环的最内层。
下面的例子会找出任何整数的最小除数，它也会判断是否为质数。
```
gawk '# find smallest divisor of num
{ num=$1
for(div=2;div*div<num;div++)
if(num % div == 0)
break
if(num % div == 0)
printf "Smallest divisor of %d is %d\n",num,div
else
printf "%d is prime\n",num}'
```

## 6.continue语句
continue语句用于for,while,do-while循环内部，它会跳过循环body中其余的部分，使得它立即进入下一次循环。
下面的例子会打印出0至20的全部数字，但是5并不会被打印出来。
```
gawk 'BEGIN{
for(x=0;x<=20;x++){
if(x==5)
continue
printf ("%d",x)
}
print ""
}'
```

## 7.next，next file，exit语句
next语句强迫gawk立即停止处理目前的记录(record)而继续下一个记录。
next file语句类似next。然而，它强迫gawk立即停止处理当前的文件。
exit语句会使得gawk程序立即停止执行而跳出。而且如果END出现，它会去执行END的actions。

# VII.内置函数
内置函数是gawk内置的函数，可以在gawk程序的任何地方调用内置函数。

## 1.数值方面的内置函数
int(x)求x的整数部分，朝向0的方向做舍去。例如:int(3.9)是3，int(-3.9)是-3。

sqrt(x)求x的平方根值。

exp(x)求x的次方。

log(x)求x的自然对数。

sin(x)求x的sine值，x是经度量。

cos(x)求x的cosine值，x是经度量。

atan2(y,x)求y/x的arctangent值，所求出的值其单位是经度量。

rand()得出一个伪随机数。此数值在0和1之间，但不等于0或1。
每次执行gawk，rand开始产生数字从相同点或seed。

srand(x)设定产生随机数的开始点或者seed为x。如果在第二次你设定相同的seed值，你将再度得到相同序列的随机数。如果参数x被省略，则现在日期、时间会被当成seed。这个方法可以使得产生的随机数是真正不可预测的。srand的返回值是前次所设定的seed值。

## 2.字符串方面的内置函数
index(in,find)
它会在字符串in里面，寻找字符串find第一次出现的地方，返回值是字符串find出现在字符串in里面的位置。如果在in里找不到find，则返回0。
例如：
print index("prenut","an")
将打印出3。

length(string)
求出string有几个字符。

match(string,regexp)
在字符串string里找到符合regexp的最长的最靠左边的子字符串。返回值是regexp在string的开始位置，即index值。match函数会设置内置变量RSTART等于index，它也会设置内置变量RLENGTH等于符合的字符个数。如果不符合，则会设定RSTART为0、RLENGTH为-1。

sprintf(fomat,expression,...)
举printf类似，但是sprintf并不打印出来，而是返回字符串。
例如：
sprintf("pi = %.2f(approx.)',22/7)
返回的字符串为"pi = 3.14(approx.)"

sub(regexp,replacement,target)
在字符串target里面，寻找符合regexp的最长、最靠左边的地方，以字符串replacement代替最左边的regexp。
例如：
str = "water,water,everywhere"
sub(/at/,"ith",str)
结果字符串str会变成
"wither,water,everywhere"

gsub(regexp,replacement,target)
gsub与前面的sub类似。在字符串target里面，寻找符合regexp的所有地方，以字符串replacement代替所有的regexp。
例如：
str="water,water,everywhere"
gsub(/at/,"ith",str)
结果字串str变成
"wither,wither,everywhere"

substr(string,start,length)
传回字符串string的子串，这个字串的长度为length个字符。
从第start个位置开始。
例如：
substr("washington",5,3)
返回值为"ing"
如果length没有出现，则返回的字符串是从第start个位置开始至结束。
substr("washington",5)
返回值为"ington"

tolower(string)
将字符串string的大写字母改为小写字母。

toupper(string)
将字符串string的小写字母改为大写字母。

## 3.输入输出的内置函数
close(filename)
将输入或输出的文件关闭

system(command)
执行操作系统命令，执行完毕后返回gawk

# VIII.用户定义的函数
复杂的gawk程序常常可以使用自己定义的函数来简化。调用自定义的函数与调用内置函数的方法一样。

## 1.函数定义的格式
函数的定义可以放在gawk程序的任何地方。
一个自定义函数的格式如下：
```
function name(parameter-list){
body-of-function
}
```
name是所定义的函数名称，名称可以是字母、数字、下划线，但不能以数字开头。
parameter-list是函数参数，以逗号分开。
body-of-function包含gawk的语句。

## 2.函数定义的例子
下面这个例子，将每个记录的第一个栏位之值的平方与第二个栏位之值的平方加起来。
```
{print "sum =",SquareSum($1,$2)}
function SquareSum(x,y){
sum=x*x+y*y
return sum
}
```

# IX.范例
一些gawk程序的例子：

```
gawk '{if(NF>max)max=NF}
END {print max}
```
打印出所有输入行中，栏位的最大个数。

```
gawk 'length($0)>80'
```
打印出超过80个字符的一行。此处只有pattern被列出，action是采用内置的print。

```
gawk 'NF > 0'
```
打印至少有一个栏位的所有行。这是一个简单的方法，将一个文件中的空白行删除。

```
gawk '{if(NF >0)print}'
```
与上例相同

```
gawk 'BEGIN {for (i=0;i<7;i++)
print int(101 * rand())}
```
此程序会打印出范围在0-100之间的7个随机数值。

```
ls -l files | gawk '{x+=$4};END{print "total bytes:" x}'
```
打印出所有指定文件之bytes数目的总和。

```
expand file | gawk '{if(x<length()) x = length()}}
END{print "maxinum line length is " x}'
```
将指定文件里最长一行的长度打印出来。expand会将tab改成space，所以是用实际的右边界来做长度的比较。

```
gawk 'BEGIN {FS=":"}
{print $1 | "sort"} /etc/password
```
此程序会将所有用户的登录名称，按字母顺序打印出。

```
gawk '{nlines++}
END {print nlines}'
```
将文件的总行数打印出来

```
gawk 'END {print NR}'
```
同上例

```
gawk '{print NR,$0}'
```
打印文件的内容时，会在每行的最前面打印出行号，它的功能与'cat -n'类似
 
