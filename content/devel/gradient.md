Title: 梯度的理解
Date: 2018-05-12
Modified: 2018-05-15
Category: 机器学习
Tags: python,machine learn

# 梯度的理解

参考以下两篇文章:

[如何直观形象的理解方向导数与梯度以及它们之间的关系？](https://www.zhihu.com/question/36301367)对导数和梯度的解释最为简明。

[WangBo的机器学习乐园的博文](https://blog.csdn.net/walilk/article/details/50978864)

总结以下内容：

- 导数：

导数指的是一元函数在某点经轴正方向的变化率。

$$f'(x) = \lim_{\Delta x \to 0} \frac{\Delta y}{\Delta x} = \lim_{\Delta x \to 0} \frac{f(x_0 + \Delta x) - f(x_0)}{\Delta x}$$

- 偏导数：

偏导数是多元函数在某点沿某个轴正方向的变化率。

$$\frac{\partial f(x_0,x_1, \ldots, x_n) }{\partial x_j} = \lim_{\Delta x \to 0} \frac{\Delta y}{\Delta x} = \lim_{\Delta x \to 0} \frac{f(x_0, \ldots, x_j + \Delta x, \ldots, x_n) - f(x_0, \ldots, x_j, \ldots, x_n)}{\Delta x}$$

- 方向导数：

层数和偏导数都是沿某轴的正方向变化。任意方向变化率就是方向层数。即：某一点在某一趋近方向上的层数值。

$$\frac{\partial f(x_0,x_1, \ldots, x_n) }{\partial l } = \lim_{\rho x \to 0} \frac{\Delta y}{\Delta x} = \lim_{\rho x \to 0} \frac{f(x_0, \ldots, x_j + \Delta x, \ldots, x_n) - f(x_0, \ldots, x_j, \ldots, x_n)}{\rho}$$


- 梯度

函数在某点的梯度是一个向量，它的方向与取得最大方向导数的方向一致，而它的模为方向导数的最大值。

$$gradf(x_0, x_1, \ldots, x_n) = (\frac{\partial f}{\partial x_0}, \ldots, \frac{\partial f}{\partial x_j}, \ldots, \frac{\partial f}{\partial x_n})$$

梯度是偏导的集合。

- 梯度下降

在每个变量轴减小对应的变量值（学习率*轴的偏导值），可描述为：

\begin{equation} 
x_0 = x_0 - \alpha \frac{\partial f}{\partial x_0} \\\\
\ldots \ldots \ldots \\\\
x_j = x_j - \alpha \frac{\partial f}{\partial x_j} \\\\
\ldots \ldots \ldots \\\\
x_n = x_n - \alpha \frac{\partial f}{\partial x_n} \\\\
\end{equation}

# 一元情况下的示例

以这段简单的[手动求导的pytorch代码](https://github.com/hunkim/PyTorchZeroToAll/blob/master/02_manual_gradient.py)为例:
```python
x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 4.0, 6.0]

w = 1.0  # a random guess: random value

def forward(x):
    return x * w


# Loss function
def loss(x, y):
    y_pred = forward(x)
    return (y_pred - y) * (y_pred - y)


# compute gradient
def gradient(x, y):  # d_loss/d_w
    return 2 * x * (x * w - y)
```

代码中 $x$ 为输入 $y$ 为输出，权值为 $w$ 没有偏值项 $b$ 。网络的前向传播公式为 $xw$ 。损失函数`loss`为 $f(x,y) = (xw -y)^2$ ，即取误差平方。由于w是标量，梯度计算就变成对 $w$ 求偏导，即为一元函数的求导:

$$f(w) = (xw)^2 + y^2 - 2(xw)y$$
$${\partial f(w) \over \partial w} = 2xw - 2xy = 2x(xw-y)$$

即代码中的`gradient`函数。
