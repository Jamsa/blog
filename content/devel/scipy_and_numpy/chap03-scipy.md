Title: Numpy And Scipy笔记（二）
Date: 2017-3-28
Modified: 2017-03-28
Category: 机器学习
Tags: python,machine learn,jupyter notebook


```python
#%matplotlib notebook
%matplotlib inline 
import matplotlib.pyplot as plt
```

# SciPy

`SciPy`以NumPy的数组计算处理功能为基础，提供了用于处理科学计算常用的方法：积分、取函数最大、最小值，取稀疏矩阵的特征向量，判断两个分布模式是否相同，等等。

## 最优化和最小化

SciPy提供的最优化处理包可以用于解决最小化的问题。典型的最小化问题是执行线性回归，查找函数的最小和最大值，取函数的根，判断两个函数是否相交。

`注意`：NumPy和SciPy提供的最优化和最小化工具中不含马尔可夫链蒙特卡罗(Markov Chain Monte Carlo (MCMC))功能——即，贝叶斯分析。

### 数据建模和拟合

有多种方式对数据进行线性回归拟合。如曲线拟合`curve_fit`，它是$ x^2 $的（即，最佳拟合方法）。下面示例数据用函数生成，并添加噪音，将这些带噪音的数据使用curve_fit进行拟合。用于拟合的线性方程是$ f(x) = ax + b $


```python
import numpy as np
from scipy.optimize import curve_fit

#实际模型和数据生成函数
def func(x,a,b):
    return a * x + b

#干净数据
x = np.linspace(0,10,100)
y = func(x,1,2)

#添加噪声
yn = y + 0.9 * np.random.normal(size=len(x))

#在噪声数据上进行拟合
popt, pcov = curve_fit(func,x,yn)

#popt是最佳拟合参数
print(popt)

#可以通过pcov检查拟合的质量，它的对角元素是每组参数的方差
print(pcov)
```

    [ 1.04801651  2.04198566]
    [[ 0.00075474 -0.0037737 ]
     [-0.0037737   0.02528505]]



```python
yt = func(x,popt[0],popt[1])
plt.figure(1)

#噪声数据
plt.plot(x,yn,'o',label="noisy data")

#拟合数据曲线
plt.plot(x,yt,label="fit line")

#干净数据直线
plt.plot(x,y,label="func line")

plt.title('curve_fit')
plt.legend(loc='best', shadow=True, fontsize='x-large')
plt.show()
```


![png]({attach}scipy_and_numpy/chap03-scipy_files/chap03-scipy_3_0.png)


`popt`保存有最佳拟合参数。通过`pcov`可以检测拟合质量，它的对角元素是每组参数的方差。

我们也可以使用最小二乘法拟合高斯分布，它是一个非线性函数：
$$
a * exp \left( \frac{- (x - \mu)^2}{2\sigma^2} \right)
$$


```python
#模型的数据生成函数
def func(x,a,b,c):
    return a*np.exp(-(x-b)**2/(2*c**2))

#生成干净数据
x = np.linspace(0,10,100)
y = func(x,1,5,2)

#添加噪声
yn = y + 0.2 * np.random.normal(size=len(x))

#进行拟合
popt,pcov = curve_fit(func,x,yn)

popt

```




    array([ 0.9371463 ,  5.11810165,  2.22927392])




```python
yt = func(x,popt[0],popt[1],popt[2])
plt.figure(1)

#噪声数据
plt.plot(x,yn,'o',label="noisy data")

#拟合数据曲线
plt.plot(x,yt,label="fit line")

#干净数据直线
plt.plot(x,y,label="func line")

plt.title('curve_fit')
plt.legend(loc='best', shadow=True, fontsize='x-large')
plt.show()
```


![png]({attach}scipy_and_numpy/chap03-scipy_files/chap03-scipy_6_0.png)


上面对高斯分布的拟合是在可接受范围之内的。

实际上我们可以使用一维数据，进行多次高斯分布。比如在func中进行两次高斯公式计算。


```python
#两次高斯模型
def func(x,a0,b0,c0,a1,b1,c1):
    return a0*np.exp(-(x-b0)**2/(2*c0**2)) + a1*np.exp(-(x-b1)**2/(2*c1**2))

#生成干净数据
x = np.linspace(0,20,200)
y = func(x,1,3,1,-2,15,0.5)

#添加噪声
yn = y + 0.2 * np.random.normal(size=len(x))

#由于我们进行的是复杂函数拟合，因此提供猜测值会让拟合效果更好
guesses = [1,3,1,1,15,1]
#进行拟合
popt,pcov = curve_fit(func,x,yn,p0=guesses)

yt = func(x,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5])
plt.figure(1)

#噪声数据
plt.plot(x,yn,'o',label="noisy data")

#拟合数据曲线
plt.plot(x,yt,label="fit line")

#干净数据直线
plt.plot(x,y,label="func line")

plt.title('curve_fit')
plt.legend(loc='best', shadow=True, fontsize='x-large')
plt.show()
```


![png]({attach}scipy_and_numpy/chap03-scipy_files/chap03-scipy_8_0.png)


### 解函数

Scipy的`optimze`模块中提供了一些工具处理“求函数的根？找出两个函数的交点？”之类的问题。

如：求等式的根：


```python
from scipy.optimize import fsolve

#解方程
line = lambda x: x + 3

#第二个参数是初始的猜测值
solution = fsolve(line,0)
print(solution)

#找出函数交点

def findIntersection(func1,func2,x0):
    return fsolve(lambda x: func1(x) - func2(x), x0)

funky = lambda x: np.cos(x/5) * np.sin(x/2)
line = lambda x: 0.01 * x - 0.5

x = np.linspace(0,45,10000)
#交点x
result = findIntersection(funky,line,[15,20,30,35,40,45])

plt.figure(1)

#曲线
plt.plot(x,funky(x),label="funky")

#直线
plt.plot(x,line(x),label="line")

#交点
plt.plot(result,line(result),'o',label="intersection")

plt.title('fresolve')
plt.legend(loc='best', shadow=True, fontsize='x-large')
plt.show()
```

    [-3.]



![png]({attach}scipy_and_numpy/chap03-scipy_files/chap03-scipy_10_1.png)


需要注意的是猜测值`[15,20,30,35,40,45]`是非常重要的，如果它们不正确，有可能获取不到希望的结果。

## 插值

包含信息的数据通常是函数形式的，作为分析者的我们想要对它进行建模。向给定的数据集中提供数据点的中间值有利于了解和预测非采样区域的数据。SciPy提供了很多用于插值处理的功能，从简单的单变量到复杂的多变量。单变量插值用于样本数据的受一个单独的变量影响，多变量插值则假设受到一个以上的变量的影响。

有两种类型的插值：

 - 使用单个函数拟合整个数据集
 - 使用多个函数拟合数据集的不同部分，函数间的连接点是平滑的
 
 第二种类型被称为“样条插值（spline interpolation）”，它在处理复杂数据时是非常强的。
 
示例：


```python
from scipy.interpolate import interp1d

#模拟数据
x = np.linspace(0,10*np.pi,20)
y = np.cos(x)

#插值数据
fl = interp1d(x,y,kind='linear')
fq = interp1d(x,y,kind='quadratic')

#x.min和x.max用于确定数据边界
xint = np.linspace(x.min(),x.max(),1000)
yintl = fl(xint)
yintq = fq(xint)

plt.figure(1)

#样本点
plt.plot(x,y,'o',label="sample data")

#线性
plt.plot(xint,yintl,label="linear",color="red")

#二次
plt.plot(xint,yintq,label="quadratic",color="blue")

plt.title('simple interpolate')
plt.legend(loc='best', shadow=True, fontsize='x-large')
plt.show()
```


![png]({attach}scipy_and_numpy/chap03-scipy_files/chap03-scipy_12_0.png)


二次拟合的情况明显更好一些，因此选择合适的插值参数（类型？）是非常重要的。

下例是针对噪声数据的插值，这里使用的函数是`scipy.interpolate.UnivariateSpline`。


```python
from scipy.interpolate import UnivariateSpline

#模拟30个样本数据
sample = 30
x = np.linspace(1,10*np.pi,sample)
y = np.cos(x) + np.log10(x) + np.random.randn(sample)/10

#多变量插值，s是平滑因子，如果它为0，则插值将经过所有的点
f = UnivariateSpline(x,y,s=1)

xint = np.linspace(x.min(),x.max(),1000)
yint = f(xint)

yorigin = np.cos(xint) + np.log10(xint) #+ np.random.randn(1000)/10


#样本点
plt.plot(x,y,'o',label="sample data")

plt.plot(xint,yorigin,label="origin no noisy",color="red")

plt.plot(xint,yint,label="interpolation",color="blue")

plt.title('simple interpolate')
plt.legend(loc='best', shadow=True, fontsize='x-large')
plt.show()
```


![png]({attach}scipy_and_numpy/chap03-scipy_files/chap03-scipy_14_0.png)


下例使用多变量插值，处理图像的重建，使用的`scipy.interpolate.griddata`函数，它用于处理多维非结构化数据。比如从 $1000 x 1000$的图像中，随机选择1000个点，重建图像。


```python
from scipy.interpolate import griddata
from scipy.misc import toimage

#希望插值的函数
ripple = lambda x,y: np.sqrt(x**2 + y**2) + np.sin(x**2 + y**2)

#生成用于插值的网格（向这个网格插值）。
#复数用于定义网格数据的步数。如果没有这个复数，
#mgrid方法将只创建一个5步的数据结构。
#下面创建两个1000x1000的grid，如果没有复数1000j，就会创建为5x5
grid_x,grid_y = np.mgrid[0:5:1000j,0:5:1000j]

#用于生成插值的样本数据（只有此部分的数据是已知的，需要通过插值还原出gird中的其它点）
xy = np.random.rand(1000,2) 
sample = ripple(xy[:,0]*5, xy[:,1]*5) 

#griddata?

#立方体插值
# xy*5 样本数据点坐标
# sample 样本数据点的值
# (grid_x,grid_y) 插值位置
# method 插值方法，cubic为立方体插值
grid_z0 = griddata(xy * 5,sample,(grid_x,grid_y),method='cubic')
grid_z1 = griddata(xy * 5,sample,(grid_x,grid_y),method='nearest')
grid_z2 = griddata(xy * 5,sample,(grid_x,grid_y),method='linear')

#10x8英寸
plt.figure(figsize=(10,8))
plt.title('griddata')

ax = plt.subplot(221)
ax.set_title('origin')
#使用原始函数生成的图像（即，原图）
plt.imshow(ripple(grid_x,grid_y))

ax = plt.subplot(222)
ax.set_title('cubic')
#插值所生成的图
plt.imshow(grid_z0)

ax = plt.subplot(223)
ax.set_title('nearest')
#插值所生成的图
plt.imshow(grid_z1)

ax = plt.subplot(224)
ax.set_title('linear')
#插值所生成的图
plt.imshow(grid_z2)
```




    <matplotlib.image.AxesImage at 0x13953ca10>




![png]({attach}scipy_and_numpy/chap03-scipy_files/chap03-scipy_16_1.png)


在图像处理中，采样越多，则还原效果越好。另一个插值函数是`scipy.interpolate.SmoothBivariateSpline`，但是它对样本数据也更敏感，griddata的可靠性则更好一些。

## 积分
SciPy提供的积分功能主要是针对数值计算的。如果需要处理的是不定积分，可以使用SymPy。

### 解析积分

下例计算 $\int_0^3 \cos^2 (e^x)\, dx $


```python
from scipy.integrate import quad,trapz

func = lambda x: np.cos(np.exp(x)) ** 2

#积分
solution = quad(func,0,3)
print(solution)

plt.figure(figsize=(10,8))
plt.title('integrate')
x = np.linspace(-3,5,100)
y = func(x)
plt.plot(x,y,'g-',label='func')

index = (x>=0) & (x<=3)
plt.fill_between(x[index],y[index],facecolor='green', interpolate=True)
#ax.fill_between(x, y1, y2, where=y2 >= y1, facecolor='green', interpolate=True)
#ax.fill_between(x, y1, y2, where=y2 <= y1, facecolor='red', interpolate=True)

#barx = np.linspace(0,3,50)
#bary = func(barx)
#plt.bar(barx,bary,width=0.04,linewidth=0.02)

plt.legend(loc='best', shadow=True, fontsize='x-large')
plt.show() 
```

    (1.296467785724373, 1.397797186265988e-09)



![png]({attach}scipy_and_numpy/chap03-scipy_files/chap03-scipy_18_1.png)


### 数值积分

给定的是数值而非公式时进行积分计算。`quad`可以处理函数积分，`trapz`用于处理数值积分。


```python
#模拟数据
x = np.sort(np.random.randn(150) * 4 + 4).clip(0,5)
func = lambda x: np.sin(x) * np.cos(x ** 2) + 1
y = func(x)

#0-5之间
fsolution = quad(func,0,5)
dsolution = trapz(y,x=x)

#解析积分和数值积分差值
print(str(np.abs(fsolution[0]-dsolution)))

plt.figure(figsize=(10,8))
plt.title('integrate')
plt.plot(x,y,'g-',label='fsolution')
plt.plot(x,y,'o',label='dsolution')

plt.fill_between(x,y,facecolor='green', interpolate=True)
plt.legend(loc='best', shadow=True, fontsize='x-large')
plt.show() 
```

    0.0385901320445



![png]({attach}scipy_and_numpy/chap03-scipy_files/chap03-scipy_20_1.png)


## 数据统计

NumPy提供了基础的统计功能如：`mean`，`std`，`median`，`argmax`，`argmin`。

SciPy提供了用于统计学的工具如：分布(连续和离散)和统计函数。


```python
x = np.random.randn(1000)
mean = x.mean()
print(mean)
std = x.std()
print(std)
var = x.var()
print(var)
```

    0.0580422470562
    0.998306098365
    0.996615066034


### 连续和离散分布

有大约80种连续分布和超过10种离散分布。在`scipy.stats`包中包含了20种概率密度函数（即PDF，都是连续函数）。这些分布函数用于随机数生成时非常有用。

![20种连续分布函数]({attach}scipy_and_numpy/figure3-12.png "20种连续分布函数")

从`scipy.stats`中调用分布函数时有几种方式：概率密度函数（PDF)、累积分布函数（CDF）、随机变量采样（RVS）、百分比点函数（PPF）。

例：$ PDF = e^{(-x^2/2)}\sqrt{2\pi} $


```python
#从统计学处理包中导入norm(普通连续随机变量)
from scipy.stats import norm

x = np.linspace(-5,5,1000)
 
# loc用于指定均值（mean），scale指定标准偏差（deviation）
dist = norm(loc=0, scale=1)

#获取PDF和CDF，norm.pdf(x) = exp(-x**2/2)/sqrt(2*pi)
pdf = dist.pdf(x)
cdf = dist.cdf(x)

#500随机样本
sample = dist.rvs(500)

#print sample

plt.title('norm')
plt.plot(x,pdf,'g-',label='PDF')
plt.plot(x,cdf,'b--',label='CDF')

plt.legend(loc='best', shadow=True, fontsize='x-large')
plt.show() 

```


![png]({attach}scipy_and_numpy/chap03-scipy_files/chap03-scipy_24_0.png)


### 统计函数（分布检测函数）

SciPy中有超过60种统计函数。统计函数通常用于描述和检测样本——比如：柯尔莫哥洛夫斯米尔诺夫的频率测试，等。

SciPy提供了大量的分布。在`stats`包中，可以使用`kstest`和`normaltest`等函数来对样本进行检测。这些分布检测函数可以检测样本是否为某个指定的分布类型，应该要确保你对数据的了解程度，以免错误的解读这些检测函数的结果。


```python
from scipy import stats

sample = np.random.randn(100)

out = stats.normaltest(sample)
print('normaltest output')
print('Z-score = ' + str(out[0]))
print('P-value = ' + str(out[1]))

# kstest is the Kolmogorov-Smirnov test for goodness of fit.
# Here its sample is being tested against the normal distribution.
# D is the KS statistic and the closer it is to 0 the better.
out = stats.kstest(sample, 'norm')
print('\nkstest output for the Normal distribution')
print('D = ' + str(out[0]))
print('P-value = ' + str(out[1]))

# Similarly, this can be easily tested against other distributions,
# like the Wald distribution.
out = stats.kstest(sample, 'wald')
print('\nkstest output for the Wald distribution')
print('D = ' + str(out[0]))
print('P-value = ' + str(out[1]))
```

    normaltest output
    Z-score = 3.30772551089
    P-value = 0.191309497725
    
    kstest output for the Normal distribution
    D = 0.0680837830281
    P-value = 0.757126631603
    
    kstest output for the Wald distribution
    D = 0.543010724508
    P-value = 0.0


研究人员通常使用描述性函数来进行统计。`stats`包中有一些描述性函数，包括几何平均数（geometric mean）`gmean`，样本偏态（skewness）`skew`，和频繁项集`itemfreq`。


```python
sample = np.random.randn(100)

out = stats.hmean(sample[sample > 0])
#调和平均数()
print ('Harmonic mean = '+str(out))

out = stats.tmean(sample,limits=(-1,1))
print('\nTrimmed mean= '+str(out))

out = stats.skew(sample)
print('\nSkewness = ' + str(out))

#样本描述信息
out = stats.describe(sample)
print('\nSize = ' + str(out[0]))
print('Min = ' + str(out[1][0]))
print('Max = ' + str(out[1][1]))
print('Mean = ' + str(out[2]))
print('Variance = ' + str(out[3]))
print('Skewness = ' + str(out[4]))
print('Kurtosis = ' + str(out[5]))
```

    Harmonic mean = 0.172810517039
    
    Trimmed mean= 0.0522147469768
    
    Skewness = -0.0500228673165
    
    Size = 100
    Min = -2.50308583453
    Max = 2.18483187013
    Mean = 0.0537000701222
    Variance = 0.91800078091
    Skewness = -0.0500228673165
    Kurtosis = -0.290299005483


如果需要更强的统计工具可以了解`RPy`。如果SciPy和NumPy需要的统计功能能满足要求，但需要更强的自动分析能力，则可以了解`Pandas`。

## 空间和聚类分析
空间和聚类分析用于模式识别、分组、聚簇。

SciPy中提供了空间分析类`scipy.spatial`和聚类分析类`scipy.cluster`。空间分析类中包括了用于分析点距离（如k-d tree）的函数。聚类分析类则提供了两个子类：矢量量化（`vq`）和分层聚类（`hierarchy`）。矢量量化使用重心对数据点（向量）进行分组。分层聚类则包含了构造聚簇和分析其子结构的功能。

### 矢量量化
矢量量化这是个一般化的术语，它通常与信号处理、数据压缩、聚类相关。这里只关注聚类，将数据发送给`vq`包，然后标识出聚簇。


```python
from scipy.cluster import vq

# 数据
c1 = np.random.randn(100,2) + 5
c2 = np.random.randn(30,2) - 5
c3 = np.random.randn(50,2)

# 将数据堆叠为180 x 2的数组，100+30+50
data = np.vstack([c1,c2,c3])

# 使用kmeans计算聚类中心(cluster centroid)和方差(variance)
centroids, variance = vq.kmeans(data,3)

print(variance)

# identified变量包含用于分隔数据点的信息
identified, distance = vq.vq(data, centroids)

vqc1 = data[identified == 0]
vqc2 = data[identified == 1]
vqc3 = data[identified == 2]

# 看是否覆盖所有点
print(vqc1.shape+vqc2.shape+vqc3.shape)

plt.title('vq')
plt.plot(vqc1[:,0],vqc1[:,1],'go',label='vqc1')
plt.plot(vqc2[:,0],vqc2[:,1],'bo',label='vqc2')
plt.plot(vqc3[:,0],vqc3[:,1],'yo',label='vqc3')

plt.legend(loc='best', shadow=True, fontsize='x-large')
plt.show() 
```

    1.32493830505
    (50, 2, 100, 2, 30, 2)



![png]({attach}scipy_and_numpy/chap03-scipy_files/chap03-scipy_30_1.png)


上图中针对的是干净的数据，对于有噪声的数据（部分类型的数据是均匀分布的）的处理是`vq.kmeans`的弱项。

### 分层聚类

分层聚类在标识嵌入在大型结构中的子结构时非常强大。但处理它的结果是非常棘手的，因为它并不能像`kmeans`地样清楚的标示出聚类。

下例中生成了一个包含多个聚类的系统。为使用分层聚类功能，我们构造了一个距离矩阵，并输出了系统树图。



```python
%matplotlib notebook
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.distance import pdist, squareform
import scipy.cluster.hierarchy as hy

# 创建包含多个簇的簇的函数
def clusters(number = 20, cnumber = 5, csize = 10):
    # Note that the way the clusters are positioned is Gaussian randomness.
    rnum = np.random.rand(cnumber, 2)
    rn = rnum[:,0] * number
    rn = rn.astype(int)
    rn[np.where(rn < 5 )] = 5
    rn[np.where(rn > number/2. )] = round(number / 2., 0)
    ra = rnum[:,1] * 2.9
    ra[np.where(ra < 1.5)] = 1.5
    
    # cls是额外的离散点
    cls = np.random.randn(number, 3) * csize
    
    # rxyz用于计算每个簇的中心，减1应该是为了保留一个位置随机的簇
    # csize应该是为了扩大簇心之间的距离，因为tmp中的值没有经过csize放大，对坐标值的影响较小
    # Random multipliers for central point of cluster
    rxyz = np.random.randn(cnumber-1, 3) 
    for i in xrange(cnumber-1):
        tmp = np.random.randn(rn[i+1], 3) #一簇数据
        #print rn[i+1],":",tmp
        x = tmp[:,0] + ( rxyz[i,0] * csize )
        y = tmp[:,1] + ( rxyz[i,1] * csize )
        z = tmp[:,2] + ( rxyz[i,2] * csize )
        
        tmp = np.column_stack([x,y,z])
        
        cls = np.vstack([cls,tmp])
        #如果不使用初始的cls离散点，则可以清晰的看到各个簇
        #print 'i=',str(i),str(len(tmp)),tmp
        #if i > 0:
        #    cls = np.vstack([cls,tmp])
        #else:
        #    cls = np.vstack([tmp])
    return cls

# Generate a cluster of clusters and distance matrix.
cls = clusters()

#绘制3D图
fig = plt.figure(1)
ax = Axes3D(fig)
ax.scatter(cls[:,0],cls[:,1],cls[:,2])
plt.show()


#绘制距离矩阵

D = pdist(cls[:,0:2])

D = squareform(D)

# Compute and plot first dendrogram.
fig = plt.figure(2,figsize=(8,8))
ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
Y1 = hy.linkage(D, method='complete')
cutoff = 0.3 * np.max(Y1[:, 2])
Z1 = hy.dendrogram(Y1, orientation='right', color_threshold=cutoff)
ax1.xaxis.set_visible(False)
ax1.yaxis.set_visible(False)

# Compute and plot second dendrogram.
ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
Y2 = hy.linkage(D, method='average')
cutoff = 0.3 * np.max(Y2[:, 2])
Z2 = hy.dendrogram(Y2, color_threshold=cutoff)
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)

# Plot distance matrix.
ax3 = fig.add_axes([0.3,0.1,0.6,0.6])
idx1 = Z1['leaves']
idx2 = Z2['leaves']
D = D[idx1,:]
D = D[:,idx2]
ax3.matshow(D, aspect='auto', origin='lower', cmap=plt.cm.YlGnBu)
ax3.xaxis.set_visible(False)
ax3.yaxis.set_visible(False)
plt.show()

```


    <IPython.core.display.Javascript object>



<img src="data:image/png;base64,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SJbAlKbZ2rloNWghpZjWWGQepGlregw18fc7b4p+P03j1u4hrTFpMtJCSlU+d9FWtTXHRm9bk20R/IviIe/Xa0ALu/IcLbjJ+pB9oe49K7aHCUYxfzL784cffpi89tpryXvvvZf88MMPCWe6b7XVVuHI2i222CJU19I4cqLT/PnzQ7GlQbtaI2DMCAImIG+66abhBCRMxRDwM888kzz55JN943n55ZcnyyyzTHLQQQeFZzHAsnmIlqsHUxaw3ujblKhjpGb9tbK50A8hljrM2THysJuilqh1xHZTJiwbwGKtFlYQKBtk0+uELGIa1Xj1ulFbAUVrjmKhsWREn/TGze9VCUz94JWlrWWZt4sKKNZyUMTfnCYE5AUp9opDke/pPcKakq2JWoQrnms15yLBpUXaI/fETMp6bnHf119/nbzxxhvhyFgslKQTbbnllsnWW28dCHf11VcPitOwXq0RsAV0ww03TG666aZku+22CwTMCUZPPfVU37ife+65wVxxyimnBMlJQucxSy+//PLh+TrwJ7bxVCkxZ3VIT1i90PshtSKmXGvGtea6LPIYBA1SFrDFN0tr1kJN2UnYFNmWbZclNBFA9XO0OVJj0KtAUKSNeRp3v4E/aYKjFTpEWIv5l2U9xtZiW1pkzJRcJIVLCyjaeiLCmiVna0nJctvZLAreJd//66+/wil4c+fODdot5mP2fciWH5Qw8obrnGtF5mOT93SCgPHTkq+LY50cXQh41qxZycorrxwOXT7ttNMSKlr1cmHq5jQk/AR///13iJ6TEmmvvPJK8AUTwi6LT5tvdYBE1SSct0nX7a/VmpINBJMFqCVZfhf/eRWaWtmxzMOr10CkIgKKDZTRG25d7SqLj71ftysWzarxku/G/KyWlGL+5jJtlXbZIwm7pHFLlLS1nsgaiMVf1EUaWXhpsq1KCIiRs81akL1QC7bWLQeG+Gxff/315O233044A36llVYKpmQhXA7IqQu3MnOyzXtrI+CJEycm8+bNW6RvYgLDWc5gcH388cfJtGnTkkceeSSYHLj++OOPEFKONPTZZ58lnB/8+OOPjxXTKAvYlClTgha88cYbJ6usskoIyOIdTBB8xL///nuy3HLLJeuuu26oGS0//E20JN5pF55M+rxJlCbhyzN7JY+yOMQ26bS8X60FyyaQJhkXxaFoe7uAlxZQrO84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">



    <IPython.core.display.Javascript object>



<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAoAAAAKACAYAAAAMzckjAAAgAElEQVR4Xuy9e5QlyV3fGffWrVvVXV1VXf2YV0+N5iEk1CAJgSRadAM2whISWryHh8B4j49Zs/axDdgyxyAd21j2YRFYu7K9x2t2/VwWo921sQVoJCQjYzj0MI0QEh6kluYlzUzNaGa6p7v61qvrcavunqia2/WIjN8v8mZm3cyMT/3hkcmMuBHf+GXkp38R8c2G4Q8FUAAFUAAFUAAFUCAqBRpR9ZbOogAKoAAKoAAKoAAKGACQIEABFEABFEABFECByBQAACMbcLqLAiiAAiiAAiiAAgAgMYACKIACKIACKIACkSkAAEY24HQXBVAABVAABVAABQBAYgAFUAAFUAAFUAAFIlMAAIxswOkuCqAACqAACqAACgCAxAAKoAAKoAAKoAAKRKYAABjZgNNdFEABFEABFEABFAAAiQEUQAEUQAEUQAEUiEwBADCyAae7KIACKIACKIACKAAAEgMogAIogAIogAIoEJkCAGBkA053UQAFUAAFUAAFUAAAJAZQAAVQAAVQAAVQIDIFAMDIBpzuogAKoAAKoAAKoAAASAygAAqgAAqgAAqgQGQKAICRDTjdRQEUQAEUQAEUQAEAkBhAARRAARRAARRAgcgUAAAjG3C6iwIogAIogAIogAIAIDGAAiiAAiiAAiiAApEpAABGNuB0FwVQAAVQAAVQAAUAQGIABVAABVAABVAABSJTAACMbMDpLgqgAAqgAAqgAAoAgMQACqAACqAACqAACkSmAAAY2YDTXRRAARRAARRAARQAAIkBFEABFEABFEABFIhMAQAwsgGnuyiAAiiAAiiAAigAABIDKIACKIACKIACKBCZAgBgZANOd1EABVAABVAABVAAACQGUAAFUAAFUAAFUCAyBQDAyAac7qIACqAACqAACqAAAEgMoAAKoAAKoAAKoEBkCgCAkQ043UUBFEABFEABFEABAJAYQAEUQAEUQAEUQIHIFAAAIxtwuosCKIACKIACKIACACAxgAIogAIogAIogAKRKQAARjbgdBcFUAAFUAAFUAAFAEBiAAVQAAVQAAVQAAUiUwAAjGzA6S4KoAAKoAAKoAAKAIDEAAqgAAqgAAqgAApEpgAAGNmA010UQAEUQAEUQAEUAACJARRAARRAARRAARSITAEAMLIB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">


通过上面的系统树图中的距离矩阵能区分出大小不同的子结构。通过`cluster`函数可以通过一个阀值来指示出各个簇。`fcuster`的输出依赖于调用`linkage`方法使用的`method`参数（如：`complete`或`single`）。上图中的作为阀值传递给`fcluster`的第二个参数的取值为`0.7 * np.max(Y[:,2])`。下面使用0.3。


```python
%matplotlib inline
#对点数据进行分组的函数
def group(data, index):
    number = np.unique(index)
    groups = []
    for i in number:
        groups.append(data[index == i])
    return groups

cls = clusters()

#只取了2列，2维点？
Y = hy.linkage(cls[:,0:2],method='complete')

cutoff = 0.3 * np.max(Y[:,2])
index = hy.fcluster(Y, cutoff,'distance')

groups = group(cls,index)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
colors = ['r','c','b','g','orange','k','y','gray']
for i,g in enumerate(groups):
    i = np.mod(i,len(colors))
    ax.scatter(g[:,0],g[:,1],c=colors[i],edgecolor='none',s=50)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    
plt.show()
```


![png]({attach}scipy_and_numpy/chap03-scipy_files/chap03-scipy_34_0.png)


### 信号和图像处理
SciPy可以读写JPEG和PNG图像，不需要了解太多的图像文件本身的结构。下例使用多张国际空间站，图片进行叠加。


```python
#没有找到图
if False:"""

from scipy.misc import imread,imsave
from glob import glob

files = glob('space/*.JPG')
im1 = imread(files[0].astype(np.float32))

for i in xrange(1,len(files)):
    print(i)
    im1 += imread(files[i]).astype(np.float32)

imsave('stacked_image.jpg',im1)


#下面的修改是为了让在接近地球表面时，仍然可以看到星球轨迹

# 类比较图像点的亮度，使用较亮的那个点，与PIL中的ImageChop.Lighter函数类似
def chop_lighter(image1,image2):
    s1 = np.sum(image1,axis=2)
    s2 = np.sum(image2,axis=2)
    index = s1 < s2
    image1[index,0] = image2[index,0]
    image1[index,1] = image2[index,1]
    image1[index,2] = image2[index,2]
    return image1

files = glob('space/*.JPG')
im1 = imread(files[0]).astype(np.float32)
im2 = np.copy(im1)

for i in xrange(1,len(files)):
    print(i)
    im = imread(files[i].astype(np.float32))
    im1 += im
    im2 = chop_lighter(im2,im)

imsave('stacked_image.jpg',im1/im1.max() + im2/im2.max() * 0.2)
"""
```

## 稀疏矩阵

NumPy能够以合理的速度处理包含 $ 10^6 $ 个元素的数组。但是一旦达到 $ 10^7 $ 个元素，则速度会变慢，并且会受限于系统的可用内存。如果这些巨大的数组中包含了0，则则可以使用稀疏矩阵。合理的使用稀疏矩阵能让内在消耗和处理时间显著的下降。

`注意`：使用ndarray和稀疏矩阵时都可以使用`nbytes`来检查它的内存占用。

使用`scipy.io`可以读写常见的稀疏矩阵文件，如：Matrix Market和HarwellBoeing或或加载MatLab文件。


```python
from scipy.sparse.linalg import eigsh
from scipy.linalg import eigh
import scipy.sparse

N = 3000
m = scipy.sparse.rand(N,N)
a = m.toarray()

print('ndarray size:'+str(a.nbytes)+'bytes')
print('sparse matrix size:'+str(m.data.nbytes)+'bytes')

%timeit eigh(a)
%timeit eigsh(m)
```

    ndarray size:72000000bytes
    sparse matrix size:720000bytes
    1 loops, best of 3: 6.89 s per loop
    10 loops, best of 3: 56 ms per loop


## 在NumPy中读写文件

使用`scipy.io.loadmat`和`scipy.savemat`可以读写Matlab的文件格式。

在天文、几何和医学领域中使用的IDL编程语言，它保存的二进制文件也可以用NumPy提供的`scipy.io.readsav`进行读写。

至少可以使用Matrix Market格式的文件来读写矩阵数据结构。这个格式是非常通用的ASCII格式。非常多的语言（C、Fortran和Matlab）都支持这种格式。
