Title: Emacs Muse标记规则学习
Date: 2007-06-19
Modified: 2007-06-19
Category: emacs
Tags: emacs

```
* 段落
在Muse中段落必须通过一个空行来隔开

这是一个新段落

      六个或更多空白字元(tab或空格)开始的一行表示一个居中的段落

* 标题
<example>
* First level

** Second level

*** Third level
</example>
* 水平线
四个或者更多破折号表示一个水平线，确保其前后都是空行，否则它将被段看作段落的一部分

----


* 强调文本

使用某些特别地认可的字符包围文本以强调文本：

<example>
*emphasis*
**strong emphasis**
***very strong emphasis***
_underlined_
=verbatim and monospace=
</example>

上面的列表生成：
*emphasis*

**strong emphasis**

***very strong emphasis***

_underlined_

=verbatim and monospace=

* 添加脚注

A footnote reference is simply a number in square
brackets<verbatim>[1]</verbatim>.[1] To define the footnote, place
this definition at the bottom of your file.  =footnote-mode= can be
used to greatly facilitate the creation of these kinds of footnotes.

<example>
 Footnotes:
 [1]  Footnotes are defined by the same number in brackets
      occurring at the beginning of a line.  Use footnote-mode's
      C-c ! a command, to very easily insert footnotes while
      typing.  Use C-x C-x to return to the point of insertion.
</example>

* 诗章
诗要求空白字符被保留，使用下面的格式
<example>
>A line of Emacs verse;
>   forgive its being so terse.
</example>

> A line of Emacs verse;
>   forgive its being so terse.

* 抄录段落

脚注:
[1]这是一条脚注
```
