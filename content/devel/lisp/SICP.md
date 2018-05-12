Title: SICP读书笔记
Date: 2010-08-31
Modified: 2010-08-31
Category: 开发
Tags: lisp,scheme

# Chap.1 Building Abstractions with Procedures

在思考活动中通过简单的想法尽力实现强大能量，首要有三： 1. 将多个简单的想法组合成单个的复杂的想法，因而可以完成所有复杂的想法。2. 将两个想法，不论它们是简单或复杂，放到一起，将他们彼此设置并立即观察他们，而不将它们组织成一个想法，通过这种方法可以得到想法之间的关系。3. 将他们从现实的已经存在的其它想法中分离出来：这称为抽象，这样可以构成这些想法的通用想法。

计算机语言完成任务的三个机制：

 - 原生表达式，它描述了语言所关心的最简单的实体。

 - 组合的方法，复合元素是从简单元素构成的。

 - 抽象的方法，通过抽象复合元素可以被命名和作为单元被处理。

在编程过程中，我们处理两种类型的元素：过程和数据。数据是要处理的“原材料”，而过程是处理数据的规则的描述。因此，任何一门强大的编程语言应该能够 描述原生数据类型和原生过程，应该有组合和抽象过程和数据的方法。

## Exercise 1.2 将下面的表达式转换为form

![ch1-z-g-3]({attach}SICP/ch1-z-g-3.gif)

```scheme
(/ (+ 5 4 (- 2 (- 3 (+ 6 (/ 4 3))))) (* 3 (- 6 2) (- 2 7)))
```

## Exercise 1.3 定义一个过程接收3个参数返回最大的两个参数的平方和

```scheme
(define (square a)
  (* a a))

(define (sum-max-square a b c)
  (+ (square (cond ((>= a b) a)
                   ((>= a c) a)
                   (else 0)))
     (square (cond ((>= b a) b)
                   ((>= b c) b)
                   (else 0)))
     (square (cond ((>= c a) c)
                   ((>= c b) c)
                   (else 0)))))
```

## Exercise 1.4 观察下面的求值模型它整合了操作符和表达式。

这个例子体现了 scheme 与 common lisp 的区别。
```scheme
(define (a-plus-abs-b a b)
  ((if (> b 0) + -) a b))
```
它将根据 b 是否大于 0 来决定对 a 和 b 进行加或减操作。

## Exercise 1.5 应用序或正则序测试

Ben Bitdiddle 发明了一种检测解释器是应用序还是正则序的方法。先定义两个过程：
```scheme
(define (p) (p))

(define (test x y)
  (if (= x 0)
      0
      y))
```
然后对下面的表达式求值：
```scheme
(test 0 (p))
```
很显然 p 的定义是不正确的，当解释器是应用序的时候会先对参数求值。因此对 (p) 求值时程序将出错。如果程序是正则序则 (p) 不会被立即求值，因为 (= x 0) 将返回真值，整个 test 表达式将返回 0 。

## Section 1.17 牛顿法求平方根

如果猜想y是x的平方，则下一个更接近x平方根的值是((y+x/y))/2
```scheme
(define (average x y)
  (/ (+ x y) 2))

(define (improve guess x)
  (average guess (/ x guess)))

(define (good-enough? guess x)
  (< (abs (- (square guess) x)) 0.001))

(define (sqrt-iter guess x)
  (if (good-enough? guess x)
      guess
      (sqrt-iter (improve guess x)
                 x)))

(print "第一种平方根算法：")
(sqrt-iter 1.0 9)
(sqrt-iter 1.0 21.0)
```



## Exercise 1.6 能否通过 cond 来定义 if

```scheme
(define (new-if predicate then-clause else-clause)
  (cond (predicate then-clause)
        (else else-clause)))
```
当测试用 new-if 来实现 Section 1.17 中的求平方根的方法时有可能会出现错误。因为通常 if 是一个特殊的 form 。它只会在条件为真时才对 then 子句求值。而 new-if 只是一个函数，它有可能会对所有参数都求值（比如解释器使用应用序）。在这用于 1.17 中的 sqrt-iter 中时将导致无限循环。

## Exercise 1.7
原来的 section 1.17 中的 good-enough? 是比较猜测值的平方与被开方数的差的绝对值小于某个值。这种方法在对那些很小的数求平方根时并不是很有效。一个更好的办法是将它改进成比较两次猜测值之差是否小于某个给定的值。
```scheme
(define last-value 0)
(define (average x y)
  (/ (+ x y) 2))

(define (improve guess x)
  (average guess (/ x guess)))

;last-guess表示上一次猜测的值
(define (good-enough? guess last-guess)
  (< (abs (- guess last-guess)) 0.000001))

;修改了这个递归计算过程的参数，添加了上次猜测结果
(define (sqrt-iter guess x last-guess)
  (if (good-enough? guess last-guess)
      guess
      (sqrt-iter (improve guess x)
                 x guess)))

;保证将猜测值设置为与上个猜测值之差的绝对值大于那个比较值0.000001
(print "第二种平方根算法：")
(sqrt-iter 1.0 9.0 100)
(sqrt-iter 1.0 21.0 100)
```




## Exercise 1.8 牛顿法求立方根

如果 y 接近 x 的立方根，那么更接近的值是 (x/y*y+2y)/3 。对应的求立方根的程序为：
```scheme
;逼近算法
(define (improve guess x)
  (/ (+ (/ x (square guess)) (* 2 guess)) 3))
;精度检查
(define (good-enough? guess last-guess)
  (< (abs (- guess last-guess)) 0.000001))
;迭代过程
(define (cube-iter guess x last-guess)
  (if (good-enough? guess last-guess)
      guess
      (cube-iter (improve guess x) x guess)))

(print "求立方根算法求27的立方根:")
(cube-iter 1.0 27 100)

```
只是在 exercise 1.7 的基础上替换了 improve 方法。

## Section 1.2 过程和它们所产生的计算

### Section 1.2.2 线性递归和迭代

#### Exercise 1.9 描绘线性迭代和线性递归的计算过程
```scheme
(define (add-rec a b)
  (if (= a 0)
      b
      (inc (add-rec (dec a) b))))
;(add-rec 4 5)
;(inc (add-rec 3 5))
;(inc (inc (add-rec 2 5)))
;(inc (inc (inc (add-rec 1 5))))
;(inc (inc (inc (inc (add-rec 0 5)))))
;(inc (inc (inc (inc 5))))
;(inc (inc (inc 6)))
;(inc (inc (7)))
;(inc 8)
;9

(define (add-iter a b)
  (if (= a 0)
      b
      (add-iter (dec a) (inc b))))

;(add-iter 4 5)
;(add-iter 3 6)
;(add-iter 2 7)
;(add-iter 1 8)
;(add-iter 0 9)
;9
```

#### Exercise 1.10 阿克曼函数
```scheme
(define (A x y)
  (cond ((= y 0 ) 0)
        ((= x 0) (* 2 y))
        ((= y 1) 2)
        (else (A (- x 1)
                 (A x (- y 1))))))

(define (f n) (A 0 n))
(define (g n) (A 1 n))
(define (h n) (A 2 n))
(define (k n) (* 5 n n))

```
通过使用 f,g,h 和正整数 n ，给出计算 5 乘以 n 的 2 次方的函数 `(k n)` 的定义。
 - TODO:

### Section 1.2.2 树形递归
树形递归也是一种常见的计算模式。例如Fibonacci数的计算。
```
Fib(n) = 0                   if n = 0
Fib(n) = 1                   if n = 1
Fib(n) = Fib(n-1) + Fib(n-2) otherwise
```
```scheme
(define (fib n)
  (cond ((= n 0) 0)
        ((= n 1) 1)
        (else (+ (fib (- n 1))
                 (fib (- n 2))))))
```
它所产生的计算过程是树状的。会随着n的变大计算规模也逐渐变大。并且在计算过程中间会产生许多重复的计算。例如，计算Fib(3)和Fib(4)时都会需要计算Fib(2)和Fib(1)，这样随着n变大会产生许多重复的计算。

如果将它转换成递归方式计算规模就不会随n变大而变大。计算的方法是引入两个中间变量a和b，将它们初始化为Fib(0)和Fib(1)，然后a=a+b，b=a，进而计算出Fib(2)，如此递归直至计算出Fib(n)。
```scheme
(define (fib n)
  (fib-iter 1 0 n))

(define (fib_iter a b count)
  (if (= count 0)
      b
      (fib-iter (+ a b) a (- count 1))))
```

 - TODO:找零钱的算法

#### Exercise 1.11 分别以递归和迭代的方式编写f(n)
```
f(n)=n if n<3 and f(n) = f(n-1)+2f(n-2)+3f(n-3) if n >=3
```

递归方式
```scheme
(define (f n)
  (if (< n 3) 
      n
      (+ (f (- n 1)) 
         (* 2 (f (- n 2))) 
         (* 3 (f (- n 3))))))
```

迭代方式。这里我引入了3个变量a、b和c分别代表f(n-1)、f(n-2)和f(n-3)
```scheme
(define (f1 n)
  (f1-iter 2 1 0 n))

(define (f1-iter a b c count)
  (if (= count 0) 
      c
      (f1-iter (+ a (* 2 b) (* 3 c)) a b (- count 1))))
```

#### Exercise 1.12 帕斯卡三角
编写递归过程计算帕斯卡三角的元素。

我首先归纳帕斯卡三角的元素的计算方法：
```
f(n,level) = 1                              如果n=1或n=level
f(n,level) = 0                              如果n<1或n>level则元素不存在
f(n,level) = f(n,level-1) + f(n-1,level-1)  otherswise
```
其中level为层次，n为在某层中的位置。

转换成函数定义
```scheme
(define (pascal-triangle n level)
  (cond ((= n 1) 1)
        ((= n level) 1)
        ((or (< n 1) (> n level)) 0)
        (else (+ (pascal-triangle n (- level 1)) (pascal-triangle (- n 1) (- level 1))))))
```

#### Exercise 1.13 证明Fib(n)是最接近某数的整数
<literal style="html">HTML</literal>

 - TODO:

