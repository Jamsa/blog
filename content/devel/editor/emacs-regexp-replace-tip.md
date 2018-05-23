Title: Emacs 正则表达式搜索替换的小技巧
Date: 2018-05-23
Modified: 2018-05-23
Category: 效率
Tags: emacs

- 交互式的使用正则表达替换

在Emacs中使用正则表达式替换时并不会像`isearch-forward-regexp`那么直观，无法查看到输入的正则表达式是否正确。之前我经常用`re-builder`进行表达式的测试，但是这样会打断当前的编辑工作。

经过验证发现可以使用`isearch-forward-regexp`代替`replace-regexp`，可以先用`isearch-forward-regexp`，它能交互式的验证所输入的表达式能否匹配，在匹配上第一个匹配位置时，输入`M-%`切换为`query-replace`模式，在输入要替换表达式后即可进行替换操作。

- 正则表达式替换重复内容
以将行首`*`、`**`、`***`替换为同样数量的`#`为例：

匹配表达式为：`^\(\*\)+`

替换表达式为：`\, (concat "#" (replace-regexp-in-string "\*" "#" \&))`

替换表达式中的`\,`表示后面的内容为`elisp`表达式，`\&`表示匹配表达式所匹配的所有内容，类似的还有`\n`,`n`为从 1 开始的数字，表示匹配上的分组内容。

- 替换`^M`字符

使用`M-%`调用`query-replace`，输入`C-q`表示要搜索的回车符。

- Emacs 正则表达中的反斜线

在`elisp`中使用正则式时，反斜杠有时候会让新手很迷惑。在遇到正则表达式本身的特殊符号时，要两个反斜杠，比如\\|、\\(等，但在字符转义时，只要一个，如\n、\t、\\(表示反斜杠本身)。

另可参考：[Emacs Regexp中文手册](http://dsec.pku.edu.cn/~rli/WiKi/EmacsRegexp.html)

在“关于反斜线”一节中出现的反斜线出现在elisp代码中时应该使用两个反斜线。 
