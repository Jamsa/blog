Title: Emacs Dired Tip
Date: 2018-05-12
Modified: 2018-05-12
Category: 效率
Tags: emacs



 - 批量mark文件
 
在dired下 `% m regexp`可批量mark文件。

更多mark方式可参照[手册](https://www.gnu.org/software/emacs/manual/html_node/emacs/Marks-vs-Flags.html){:target="_blank"}。

 - 批量替换文件内容
 
 对mark的文件可使用`dired-do-find-regexp-and-replace`做文件内容的批量替换。
 
 - 批量修改文件名
 
 在dired模式下可以`dired-toggle-readonly`切换为编辑模式，编辑模式下可以直接修改buffer中的文件名，使用`wdired-finish-edit (C-x C-s)`像保存文件一样，保存对文件名的修改。

