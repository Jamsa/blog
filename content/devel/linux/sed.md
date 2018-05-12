Title: Sed Tips
Date: 2007-06-19
Modified: 2007-06-19
Category: 效率
Tags: linux,sed

# I介绍

## 1. sed可以完成的工作
sed最常用在编辑那些需要不断重复某些编辑动作的文件上。

可以用sed完成一些重复性的工作。

sed可以一次执行多个不同的编辑动作。

## 2. sed能做哪些编辑动作
删除、修改、添加、插入、合并文件中的资料行，或读入其它文件的资料到文件中，也可以替换其中的字符串、转换其中的字母等。

## 3. sed工作流程
从输入中读入内容，操作完毕后发送到标准输出。

# II使用sed
sed命令可以分成编辑指令与文件指令两部分。编辑指令负责控制所有编辑工作，文件指令处理文件。编辑指令由位址与函数两部分组件，位址指令用于定位对象，而编辑指令用于编辑对象。

## 1. 命令行上的编辑指令

在命令行上执行sed指令时用-e参数，如果sed指令在文件中用-f参数。
```
sed -e '编辑指令1' -e '编辑指令2' ...文件一 ...文件二
```
例
```
sed -e '1,10d' -e 's/yellow/black/g' yel.dat
```
在面的命令中'1,10d'执行删除1到10行，s/yellow/black/g'将yellow字符串替换成black字符串。

## 2. 编辑指令的格式如下：
```
[address1[,address2]]function[argument]
```
address1,address2为行数或者正则表达式，用于定位所编辑的对象。function[argument]为sed的内置函数，表示在对象上执行的动作。

## 3. 定位(address)参数的表示方法：

下面举例以使用函数参数d为例：

 a. 删除文件内第10行的内容，则指令为10d

 b. 删除含有'man'字符串的行，指令为/man/d

 c. 删除文件内第10行到第20行，为10,20d

 d. 删除第10行到含有'man'字符串的行，则指令为10,/man/d

定位参数的说明：

 a. 定位参数为十进制数字：此数字表示行数。

 b. 定位参数为正则表达式，当输入中有符合该表达式时，执行编辑动作。

## 4. 函数参数

函數參數	功能
```
: label 	建立 script file 內指令互相參考的位置。 
# 	建立註解 
{ } 	集合有相同位址參數的指令。 
! 	不執行函數參數。 
= 	印出資料行數( line number )。 
a\ 	添加使用者輸入的資料。 
b label 	將執行的指令跳至由 : 建立的參考位置。 
c\ 	以使用者輸入的資料取代資料。
d 	刪除資料。 
D 	刪除 pattern space 內第一個 newline 字母 \ 前的資料。 
g 	拷貝資料從 hold space。 
G 	添加資料從 hold space 至 pattern space 。 
h 	拷貝資料從 pattern space 至 hold space 。 
H 	添加資料從 pattern space 至 hold space 。 
l 	印出 l 資料中的 nonprinting character 用 ASCII 碼。 
i\ 	插入添加使用者輸入的資料行。 
n 	讀入下一筆資料。 
N 	添加下一筆資料到 pattern space。 
p 	印出資料。 
P 	印出 pattern space 內第一個 newline 字母 \ 前的資料。 
q 	跳出 sed 編輯。 
r 	讀入它檔內容。 
s 	替換字串。 
t label 	先執行一替換的編輯指令 , 如果替換成牛p>則將編輯指令跳至 : label 處執行。 
w 	寫資料到它檔內。 
x 	交換 hold space 與 pattern space 內容。 
y 	轉換(transform)字元。
```

## 5. 执行文件中的编辑指令

当执行的指令过多时，可以将指令放到文件中。用sed -f script_file执行。
```
	sed -f script_file ...文件
```
例如：
```
	sed -f ysb.scr yel.dat
```
其中，ysb.scr的内容如下：
```
1,10d
s/yellow/black/g
```

## 6. 执行多个文件的编辑

在sed命令行上，一次可以执行编辑多个文件，例如：
```
	sed -e 's/yellow/blue/g' white.dat red.dat black.dat
```
sed将从左至右依次处理各个文件。

## 7. 执行输出控制

默认情况下处理后的结果输出到标准输出。但通过-n，可以将输出的控制权交给sed，由编辑指令来决定结果是否输出。

例如：
```
	sed -n -e '/white/p' white.dat
```
上例中-n与编辑指令/white/p一起配合控制输出。-n将输出控制权交给编辑指令，/white/p将含有'white'的字符串打印出来。


# III范例
操作需求描述：
```
	将文件中...资料，执行...(动作)
```
当需要执行多个动作时，指令形式如下：
```
	位置参数{
		函数参数1
		函数参数2
		函数参数3
		 .
		 .
		}
```

## 1. 替换文件中的资料

 a. 将文件中含'machine'字符串的资料选中的'phi'字符串替换成'beta'字符串
```
	sed -e '/machine/s/phi/beta/g' input.dat
```

 b. 将文件中第5行资料，替换成'This is a test.'
```
	sed -e '5c\
	This is a test.
	' input.dat
```

 c. 将文件中1至100行的资料替换成如下两行：
```
	How are you?
	data be deleted!
```
则命令如下：
```
	sed -e '1,100c\
	How are you?\
	data be deleted!
	' input.dat
```

## 2. 移动文件中的资料

可以使用sed中的hold space暂存编辑中的资料，用函数w将文件资料搬到它档内存储，或者用函数r半它档内容搬到文件内。当执行函数参数h,H时会将pattern space资料暂存到hold space,当执行x,g,G时，会将暂存的资料取到pattern space

 a. 将文件中前100行，搬到文件第300行后。
```
	sed -f mov.src 文件
```
mov.src 内容如下：
```
1,100{
H
d
}
300G
```
其中
```
1,100{
H
d
}
```
表示将文件前100行，先储存在hold space之后删除。指令300G表示将hold space内的资料，添加在第300行后输出。

 b. 将文件中含'phi'字符串的行，搬至mach.inf中：
```
	sed -e '/phi/w mach.inf' 文件名
```

 c. 将mach.inf中的内容，移到文件中含'beta'字符串的行：
```
	sed -e '/beta/r march.inf' 文件名
```

另外由于sed是一个流编辑器，理论上输出后的文件资料不可能再搬回来编辑。

## 3. 删除文件中的资料

因为sed是行编辑器，所以sed很容易删除行，或者整个资料。一般用d或D来删除。

 a. 将文件内的所有空白行全部删除：
```
	sed -e '/^$/d' 文件名
```

正则表达式中'^$'表示空白，'^'表示行开头，'$'表示行结尾。

 b. 将文件内连续的空白行，删除成一行：
```
	sed -e '/^$/{
	N
	/^$/D
	}' 文件名
```

其中N表示将空白的下一行资料加至pattern space内。函数参数/^$/D表示，当添加的是空白行时，删除第一行空白行，而且剩下的空白行则再重新执行一次指令。如此反复，最后只留下一行空白行了。

## 4. 搜索文件中的资料
sed可以执行类似UNIX命令grep的功能。理论上可以用正则表达式将文件中匹配的内容输出。

例如将文件中包含'gamma'的内容输出
```
	sed -n -e '/gamma/p' 文件名
```

但sed是行编辑器，它搜寻基本上是以行为单位。因此，当一些字符串因换行被拆分成两部分时，一般的方法即不可行。此时，就必须以合并行的方式来搜寻这些资料。例：

将文件中仿'omega'字符串的资料输出。其命令如下：
```
	sed -f gp.scr 文件名
```

gp.scr内容如下：
```
/omega/b
N
h
s/.*\n//
/omega/b
g
D
```

在上述sed script中，因函数参数b形成类似C语言中的case结构，使得sed可以分别处理当资料内含'omega'字串，当'omega'字符串被拆成两行，以及资料内没有'omega'字串的情况。下面分三种情况讨论：

 a. 当资料内仿'omega'，则执行编辑指令
```
/omega/b
```

它表示当资料内含有'omega'字符串时，sed不再执行它后面的指令，而直接将它输出。

 b. 当资料内没有'omega'，则执行编辑指令如下：
```
N
h
s/.*\n//
/omega/b
```

其中，函数参数N，表示将下一行资料读入使得pattern space内含前后两行资料。函数参数h表示将pattern space内的前后两行资料存入hold space。函数参数s/.*\n//，它表示将pattern space内的前后两行资料进行合并成一行。/omega/b，它表示如果合并后的资料内含'omega'字符串，则不再执行后面的指令，而将此资料自动输出。

 c. 当合并后的资料依旧不含'omega'，则执行编辑指令如下
```
g
D
```

其中，函数参数g，它表示将hold space内合并前的两行资料放回pattern space。函数参数D，它表示删除两行资料中的第一行资料，并让剩下的那行资料，重新执行sed script。如此，无论是资料行内或行间的字符串都可以搜索到。
 
