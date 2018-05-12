Title: Emacs Tips
Date: 2008-07-08
Modified: 2008-07-08
Category: 效率
Tags: emacs

# 一 基本概念
- 1.常见的按键组合：
    a.最常见的命令都被绑定到了"C-n"(n可以是任意符号)

    b.次常见的命令被绑定到了"ESC n"形式

    c.其它常见的命令被绑定到了"C-x something"

    d.某些特殊命令被绑定到了“C-c something"的形式。这些命令通常都与某些特殊的编辑模式有关

    e.有些命令没有被绑定到按钮上。而是通过"ESC x long-command-nam RETURN”命令方式执行

- 2.如果用F10无法打开菜单,可以用"ESC `"

- 3."C-x C-v"读错文件时修正

- 4."C-x i"插件文件

- 5.使用"C-s"保存时遇到麻烦时,试试使用"C-x C-w"

- 6.帮助系统：
    a."C-h t"启动教程

    b."C-h k"获取按键描述

    c."C-h f"获取函数的描述

    d."C=h"进入帮助系统

    e."C-h i"启动Info页阅读器

- 7.看不到菜单时可以使用"ESC x menu-bar-mode"

# 二 文件编辑
- 1."ESC x auto-fill-mode RETURN"切换自动换行模式

- 2."ESC G g"中转到指定的行号

- 3."ESC }"前一段,"ESC {"后一段。"ESC ]"前一页,"ESC ["后一页

- 4."ESC n"或"C-u n"重复执行命令

- 5."ESC DEL"向后删除一个单词

- 6."C-x C-x"在选择区首尾切换

- 7."ESC h"标记段落,"C-x h"标记整个文件,"C-x C-p"标记整页

- 8."ESC q"段落重排

- 9."C-t"交换两个字符的位置,"ESC t"交换两个单词的位置,"C-x C-t"交换两个文本行

- 10."ESC c"把单词的首字母改为大写,"ESC u"将整个单词修改为大写,"ESC l"将整个单词修改为小写

- 11."C-x u","C-_","C-/"都是撤销命令

- 12."ESC x recover-file RETURN"从自动保存的文件中恢复文本

- 13.Emacs的自动保存文件有一个重要的注意事项:如果在一个文件里进行了一次大规模的删除操作,Emacs将停止自动保存这个文件并显示一条消息通知用户,要想让Emacs再次开始自动保存这个文件,用"C-x C-s"保存一次,或者输入"ESC 1 ESC x auto-save RETURN"

- 14."ESC %"查找替换
