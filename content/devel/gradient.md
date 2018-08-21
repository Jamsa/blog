Title: 梯度的理解
Date: 2018-05-12
Modified: 2018-05-27
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

导数和偏导数都是沿某轴的正方向变化。任意方向变化率就是方向导数。即：某一点在某一趋近方向上的导数值。

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

## 一元情况下的示例

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

# 梯度下降算法

## 数学推导

[参考](https://blog.csdn.net/yhao2014/article/details/51554910)

设拟合函数或神经网络的前向传播函数为$h(\theta)$:

$$h(\theta) = \theta_0 + \theta_1 x_1 + \ldots + \theta_n x_n = \sum_{j=0}^n \theta_n x_n$$

其向量形式：

$$h_\theta (x) = \theta^T X$$

损失函数为：

$$J(\theta) = \frac{1}{2m} \sum_{i=1}^m (h_\theta (x^i) - y^i)^2$$

优化目标为最小化损失函数。

### 批量梯度下降BGD算法推导

对每个$\theta_j$求偏导，得到每个$\theta_j$的梯度：

$$\frac{\partial J(\theta)}{\partial \theta_j} = \frac{1}{m} \sum_{i = 1}^m (h_\theta (x^i) - y^i) x_j^i$$

优化参数的过程就是按每个参数的负梯度方向方向来更新每个$\theta_j$，其中的$\alpha$表示步长（学习率）：

$$\theta_j = \theta_j - \alpha \frac{\partial J(\theta)}{\partial \theta_j} = \theta_j - \frac{\alpha}{m} \sum_{i=1}^m (h_\theta (x^i) - y^i) x_j^i$$

由于BGD算法需要使用所有训练集数据，如果样本数量很多（即m很大），这种计算会非常耗时。所以就引入了随机梯度下降SGD算法。

### 随机梯度下降SGD

先将损失函数进行改写：

$$J(\theta) = \frac{1}{2m} \sum_{i=1}^m (h_\theta (x^i) - y^i)^2 = \frac{1}{m} \sum_{i=1}^m cost(\theta , (x^i,y^i))$$

其中的$cost(\theta , (x^i, y^i)) = \frac{1}{2}(h_\theta (x^i) - y^i)^2$称为样本点$(x^i, y^i)$的损失函数。这样就将问题转化为了对单个样本点的优化问题。

对这个新的损失函数求偏导，得到每个$\theta_j$的梯度

$$\frac{\partial cost(\theta, (x^i, y^i))}{\partial \theta_j} = (h_\theta (x^i) - y^i)x^i$$

然后根据这个梯度的负方向来更新每个$\theta_j$

$$\theta_j = \theta_j - \alpha \frac{\partial cost(\theta , (x^i, y^i))}{\partial \theta_j} = \theta_j - \alpha (h_\theta (x^i) - y^i) x^i$$

随机梯度下降每次迭代只计算一个柆，能大大减少计算量。缺点是SGD并不是每次迭代都会向着整体最优化方向，并且最终得到的解不一定是全局最优解，而只是局部最优解。最终结果往往是在全局最优解附近。

# 求导与神经网络的反向传播

[参考](https://www.cnblogs.com/charlotte77/p/5629865.html)

即采用链式求导法逐层求导。

## pytorch中的自动求导功能

[参考](https://blog.csdn.net/manong_wxd/article/details/78734358)

pytorch中的自动求导机制是因为它对历史信息保存了记录。每个变更都有一个`.creator`属性，它指向把它作为输出的函数。这是一个由`Function`对象作为节点组成的有向无环图（DAG）的入口点，它们之间的引用就是图的边。每次执行一个操作时，一个表示它的新`Function`对象就被实例化，它的`forward()`方法被调用，并且它输出的`Variable`的创建者被设置为这个函数。然后，通过跟踪从任何变量到叶节点的路径，可以重建创建数据的操作序列，并自动计算梯度。




