Title: MD测试页
Date: 2016-04-25
Modified: 2016-04-25
Category: misc
Tags: test
S_lug: URL中该文章的链接地址
Author: 作者

# 数学公式
包装在`\begin{foo}`和`\end{foo}`之间的内容不需要放在`$$`或`$`之间。
\begin{equation}
     x=\sqrt{b}
\end{equation}

包装在`$`间的行内公式和包装在`$$`之间的公式块。

If $a^2=b$ and \( b=2 \), then the solution must be either $$
a=+\sqrt{2} $$ or $$ a=-\sqrt{2} $$.

$$J(\theta) = \frac{1}{2m}\sum_{i=1}^{m}(\theta^{T}X_{i} - Y_{i})^2$$

$e=mc^2$

[MathJax快速参考](http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference)


# 代码块
```
@interface «nameOfClass» : «nameOfClassToInheritFrom» {
    «attribute information»
}

«list of messages responded to»

@end
```

# 表格扩展
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

# html表格
<table class="table table-condensed table-bordered table-hover">
  <thead>
    <tr>
      <th>First Header</th>
      <th>Second Header</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Content Cell</td>
      <td>Content Cell</td>
    </tr>
    <tr>
      <td>Content Cell</td>
      <td>Content Cell</td>
    </tr>
  </tbody>
</table>

# 链接
aa [a link relative to the current file]({filename}about.md) bb
