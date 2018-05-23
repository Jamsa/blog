Title: Sklearn的基本使用(Jupyter Notebook)
Date: 2016-04-05
Modified: 2016-04-05
Category: 机器学习
Tags: python,machine learn


```python
from sklearn import datasets
# 样例数据:鸢尾花
iris = datasets.load_iris()
```


```python
# 150个鸢尾花观察值指定了一些测量：花萼宽带、花萼长度、花瓣宽度和花瓣长度，
# 以及对应的子类：Iris setosa、Iris versicolor和Iris virginica。
iris.data.shape
```




    (150, 4)




```python
iris.data[0] 
```




    array([ 5.1,  3.5,  1.4,  0.2])




```python
# 每个观察的类别
iris.target.shape
```




    (150,)




```python
iris.target[120] # 某个样例的类别
```




    0




```python
iris.target[122] # 某个样例的类别
```




    2




```python
iris.data[122] # 该样例的数据
```




    array([ 7.7,  2.8,  6.7,  2. ])




```python
import numpy as np
np.unique(iris.target) # 一共三种类型
```




    array([0, 1, 2])




```python
# 学习和预测
from sklearn import svm
clf = svm.LinearSVC()
clf.fit(iris.data, iris.target) # 从数据学习

# 预测一个数据
clf.predict([[ 5.0,  3.6,  1.3,  0.25]])
```




    array([0])




```python
# 预测数据
clf.predict([[7.7,  2.8,  6.7,  2.2]]) 
```




    array([2])




```python
# 训练之后的模型数据
clf.coef_
```




    array([[ 0.18424404,  0.45123269, -0.80794054, -0.45071332],
           [ 0.05184218, -0.89426264,  0.40510244, -0.93758469],
           [-0.85082544, -0.98673222,  1.38085117,  1.86541325]])


