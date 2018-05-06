Title: 线性代数文摘
Date: 2016-09-22
Modified: 2016-09-22
Category: math
Tags: 线性代数

# 数量积与向量积
数量积即标量积、点积、点乘，是接受在实数 $\mathbb{R}$ 上两个矢量并返回一个实数值标量的二元运算。它是欧几里得空间的标准内积。
两个矢量 $\mathbf{a} = [a_1,a_2,\dots,a_n]$ 和 $\mathbf{b} = [b_1,b_2,\dots,b_n]$ 的点积定义为：
$$\mathbf{a} \cdot \mathbf{b} = a_1 b_1 + a_2 b_2 + \dots + a_n b_n$$
使用矩阵乘法并把（纵列）矢量当作 $n \times 1$ 矩阵，点积还可以写为：
$$\mathbf{a} \cdot \mathbf{b} = \mathbf{a} ^T \mathbf{b}$$
这里的 $\mathbf{a}^T\mathbf{b}$ 表示矩阵 $\mathbf{a}$ 的转置。

更准确的表达应该是以大写字母 $A$ 来表示这个只有一列的矩阵。

# 满秩矩阵
矩阵的秩: 用初等行变换将矩阵A化为阶梯形矩阵, 则矩阵中非零行的个数就定义为这个矩阵的秩, 记为r(A)。

满秩矩阵(non-singular matrix): 设A是n阶矩阵, 若r(A) = n, 则称A为满秩矩阵。但满秩不局限于n阶矩阵。若矩阵秩等于行数，称为行满秩;若矩阵秩等于列数，称为列满秩。既是行满秩又是列满秩则为n阶矩阵即n阶方阵。

满秩矩阵是一个很重要的概念, 它是判断一个矩阵是否可逆的充分必要条件

其中非奇异矩阵是满秩矩阵

# 协方差
[参考](https://www.zhihu.com/question/20852004)

通俗理解：两个变量在变化过程中是同方向变化还是反方向变化。同向变化时协方差为正，反向变化为负。从数值来看，协方差越大，同向程度越大，反之亦然。

公式：
$$Cov(X,Y) = E[(X - \mu_x)(Y - \mu_y)]$$
公式的解释：如果有X，Y两个变量，每个时刻的“X值与其均值之差”乘以“Y值与其均值之差”得到一个乘积，再对每个时刻的乘积求和并求平均值（其实是求“期望”，这里简单认为就是求均值）。

# 类内散度矩阵和类间散度矩阵
给定数据集 $D={(x_i,y_i)}_{i=1}^m, y_i \in \{0, 1\}$, 令 $\mathbf{X_i}, \mathbf{\mu_i}, \mathbf{\Sigma_i}$ 分别表示第 $ i \in \{0,1\}$ 类示例的集合、均值向量、协方差矩阵。若将数据投影到直线 $\mathbf{w}$ 上，则两类样本的中心在直线上的投影为分别为 $\mathbf{w^T\mu_0}$ 和 $\mathbf{w^T\mu_1}$ ；或将所有样本点都投影到直线上，则两类样本的协方差分别为 $\mathbf{w^T\Sigma_0w}$ 和 $\mathbf{w^T\Sigma_1w}$ 。由于直线是一维空间，因此 $\mathbf{w^T\mu_0}, \mathbf{w^T\mu_1}, \mathbf{w^T\Sigma_0w}, \mathbf{w^T\Sigma_1w}$ 均为实数。

类内散度矩阵
$$
\begin{align}
\mathbf{S_w} & = \mathbf{\Sigma_0 + \Sigma_1} \\
& = \mathbf{\sum_{x \in X_0}{(x-\mu_0)(x-\mu_0)^T} + \sum_{x \in X_1}{(x-\mu_1)(x-\mu_1)^T}}
\end{align}
$$

类间散度矩阵
$$
\mathbf{S_b = (\mu_0 - \mu_1)(\mu_0 - \mu_1)^T}
$$

全局散度矩阵
$$
\begin{align}
\mathbf{S_t} & = {S_b + S_w} \\
& = \mathbf{\sum_{i=1}^m(x_i - \mu)(x_i-\mu)^T}
\end{align}
$$
其中 $\mu$ 是所有示例的均值向量。

