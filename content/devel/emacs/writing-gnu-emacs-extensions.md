Title: Writing GNU Emacs Extensions笔记
Date: 2010-12-07
Modified: 2010-12-07
Category: emacs
Tags: emacs

# 定制Emacs

## 全局按键绑定
```emacs-lisp
(global-set-key keysequence command)
```
keysequence 中普通字符按键直接用相应的字符表示。`\`应该被写作`\\`。特殊字符如META-问号应该写作`\M-?`。CONTROL-x应该写作`\C-x` CONTROL META-x写作`\C-\M-x`。CONTROL-x在文档中也被缩写为`^x`，相应的应该表示为`\^x`。`\M-?`也可以表示为`\e?`字符串`\e`是转义字符。

## 查询按键绑定
C-h b命令来查询按键绑定信息，这个命令被绑定到了describe-bindings。
```emacs-lisp
(global-set-key "\M-?" 'help-command)
```

## 对Lisp表达式求值的方法
 - 将表达式放到文件中然后load这个一拥而入。M-x load-file RET rebind.el RET。
 - 使用eval-last-sexp，它被绑定到C-x C-e。
 - 使用eval-express，它被绑定到`M-:`。
 - 使用`*scratch*`缓冲构。在这个缓冲区处于Lisp Interaction模式。这个模式下，按C-j将调用eval-print-last-sexp，它与eval-lastsexp类似，但是它会将执行的结果插到光标位置。Lisp Interaction模式下的另一个作用是按M-TAB将能自动完成Lisp符号。

## Apropos
使用apropos来查找命令。
<example>
M-x apropos RET delete RET
</example>
查找符合"delete"的Emacs变量和函数。

可以给apropos传递前缀参数。在Emacs中，在执行一个命令前按C-u可以向命令传递特殊信息。C-u通常跟数字参数；例如，C-u 5 C-b表示将光标向左移动5个字符。有些情况下，这个额外信息只是表明你按过了C-u。当调用apropos时使用了前缀参数时，它不光会报告匹配到的函数和变量，还会报告每个命令所使用的按键绑定。

当知道要搜索的目标是Emacs命令时，可以直接使用command-apropos（M-? a）代替apropos。命令和函数的区别在于命令可以交互的执行。

## 想法

## 总结

# 简单的新命令

