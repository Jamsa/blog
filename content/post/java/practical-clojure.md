---
title: "Practical Clojure 记笔"
date: 2012-03-12
modified: 2010-07-30
categories: ["开发"]
tags: ["clojure"]
---

# 状态管理
Clojure主张消除状态管理。而现实世界仍要需要状态变化。

多数语言将事物（things）描述为变量或对象，并允许修改它们。这造成了对锁的需求。

## 状态和identity
Clojure引入新的思考事物的哲学。它将事物分解为2个独立的概念——状态和identity。状态是与identity关联的某一时间点的值，而identity是事物不会改变的那个部分，它会与不同时间的不同状态建立连接。每个状态下的值都是不可变的。改变通过将identity指向（refer）不同的状态入口而模拟产生的。

Clojure中的状态可以是任何Clojure中的数据类型。Identity是由三种引用类型（reference type）所表示的：ref、agent、atom和var。每种都描述了一个identity并指向一个状态。分别用于不同的情况：

 - ref管理同步的coordinated（协调）状态
 - agent管理异步的independent（独立，不受约束）状态
 - atom管理同步的independent状态

## Coordinated与Independent状态
许多系统都需要对identity的修改是以协调的方式进行以确保数据的完整性。Coordinated的修改方式下将管理多个独立的identities以确保所有修改都会同时进行。例如，在2个银行帐户间转帐操作时，钱存入一个帐号，必须也保证从另一个帐号减去相应的量，这两个动作必须同时发生。Clojure使用ref来提供这种coodinated状态。

与coordinated状态管理对应的是independent状态。Independent identity只处理自身，而不与其它identities相关联。这仍然需要以某种方式进行控制，但是这种处理方式比起由多个identities参与的coodinating修改会要高效一些。修改independent的identities通常比修改coordinated的identities要快。Clojure提供了agent和atom来处理independent identity。

## 同步和异步更新
同步更新会使identities的值在同一线程中立即被修改。在修改操作完成之前将不会继续向下执行，这与多数程序员的需求是一致的。在Clojure中修改ref和atom时都是同步的。

异步修改不会立即发生，但它会在未指定的将来（与修改点较近的）某个时间发生，通常是在另一线程中。代码将继续运行下去，而不等侍修改的完成。异步修改对于并行编程是非常有用的，特别对于基于事件的编程模型。但是Clojure并不保证异步更新具体在什么时候发生。Clojure中用agent来实现异步修改identities。

## Ref和事务
Ref是Clojure中实现同步coordinated identities的机制。对每个identity的操作能在事务中进行，由事务保证各个identities的值在整个事务中处于一致的状态（不会被其它线程修改）。即STM。

在事务之外修改ref将抛出错误。

### 修改ref
有多个函数可以修改ref的值，它们的区别是在于性能方面。

### 事务
Clojure的事务与数据库事务类似。同一事务中的修改操作是在同一时刻原子性地提交的。ref的值的一致性是有保证的。

事务也是隔离的，没有事务能看到其它事务正在运行时的值。事务开始时，它获取所有参与事务的ref的值的快照。随后在事务之外对些值的修改也不会被事务中的代码看到，就好像事务中的进行的修改对于外部的世界完全不可见，直到它完成和提交。当然，事务中进行的修改对于同一事务中的其它代码是可见的。对一个处于事务中的ref进行取值时返回的总是ref的“in-transaction”（从下面的章节看，这个值应该是初次进入事务时的快照值）值，which reflects any updates that have been made since the beginning of the transaction。（前面这句不懂，难道是指能获取到事务中已经修改，但还未提交的值？这样就没达到隔离效果啊？）

对于嵌套事务。内部的事务只是简单的变成外面事务的一部分，只到外面的事务提交了整个事务才提交。

Clojure中的事务是采用的乐观锁。这意味着事务不会等侍其它事务执行完才开始。事务永远不会在等侍另一个更新时阻塞线程。当一个事务发现状态已经被另一个事务修改时，事务将被重试，它重新获取到新的值的快照并重新运行自己。由系统来确定提交的顺序，它保证不管对ref有多少个争用都会执行完。

高并发的情况下将可能导致STM系统产生非常多的重试并导致它变慢。但是多数发问下它都比使用锁要快。在最坏的情况下设计完美的锁系统可能会比STM要快，但是Clojure还是认为STM所带来的认知负担的减轻和简单化的方案仍然是值得的。

很多人可能会认为STM会带来内存管理和垃圾收集方面的问题：但是多数情况下它还是表现得足够快。

### 更新ref的工具
最重要的是dosync宏，它初始化事务并接收任意数量的forms。事务中的form被依次执行。最后一个form的值被作为事务提交后的返回值。如果任何一个form发生异常则整个事务终止且不会被提交。

在dosync中使用ref-set来修改ref的状态。

另一个修改ref的函数是alter。它接收一个ref和一个函数和任意数量的参数。传给alter的函数要注意，因为它有可能会在事务重试时多次被执行。

最后一个函数是commute。它与alter用法类似，但有一个区别：在竟争性事务中，它也会重启整个事务，但它将会使用新值来进行重试，而不是使用in-transaction（in-transaction应该是表示初次执行事务时得到的快照）值。这意味着commute操作产生的争议会更少，在高竟态情况下能得到更好的性能。

这也意味着commute操作并不能完美的支持事务隔离。如果传递给commute的函数逻辑上或者在数学上是交替的，那将不会有区别。

交替函数是那些可能按任意顺序来调用而不会影响最终结果的函数

还有另一个用于操作ref的函数：ensure。它接收单个参数，一个ref。与其它ref函数类似，它也只能用于事务中。与其它ref函数不同的是，它并不实际修改ref。它所做的是在事务中ref被修改则强制事务重试。当然，你将不会在事务中看到这种修改，因为事务的隔离性。但是，如果你不在事务中修改ref，则这个ref将不会被包含在最终提交的一致性保证中（我的理解是如果你在事务中不修改某个ref，则这个ref可以被其它事务所修改，从而触发ensure）。如果在一个事务之后基于coordination的原因你想要确保一个ref在你没有修改时不允许被更新，则可以在事务中使用ensure。

## Atom
它是Clojure中的实现同步修改uncoordinated identities的实现。Atoms是基于java.util.concurrent.atomic中的Java类的。它提供了一种原子性的修改值的方法而不会被发生竞争条件下影响值修改的机制。但是与Java中的atomic包不同，Clojure中的atom是无锁的。读取atom是不会被阻塞的，而对atom的更新将会在atom正在进行更新操作之后重试，与ref类似。

实际上，atom与ref是类似的，只是它不需要与其它ref协调工作，因此不需要特殊的事务处理。

### 何时使用atom
对于独立的identity操作，它是最正确的选择。它是最轻量级的identity类型。

## 用于异步处理的agent
Agents是Clojure中独有的强大功能。对它的值的修改由专用的独立的由系统管理的线程池来异步的管理。

这意味着agent不只是一种在并发环境下存储和管理状态的手仙，它也是一种在程序中引入并发的工具。使用agent时，不需要手工产生线程，管理线程池或者用其它方法显式地来进行并发编程。


### 创建和使用agent
通过send或send-off向agent发送一个action函数来修改agent的值。

send-off与send有完全相同的签名。唯一不同的是这两个函数会导致不同的性能表现。send用于CPU密集型的操作，而send-off用于会进行IO阻塞的耗时的操作。

### 更新的语义
尽管agent不保证何时会执行更新，但是我们仍然可以使用下面的规则：

 - 传递给各个agent的actions是串行执行的，而不是并发的。在竟争条件下发送给同一agent的更新操作不会互相覆盖。
 - 由同一线程发送给同一agent的多个actions将会按发送的顺序被执行。但是对于由不同线程所发送的action则没有这种保证。
 - 如果一个action函数中包含了向其它agent或者自己发送action的代码。则这些agent具体发送会发生在action函数返回agent值已经被修改之后。这允许action触发其它action而不产生更新冲突。
 - 如果一个对agent发送的更新操作发生在STM事务之中，则发送动作在事务提交之前不会产生。这意味着在STM事务中可以安全将动作发送给atom（这里为什么是atom呢？）。

### Agent的错误处理
由于action是在独立线程中异步执行的，因此需要一个特殊的错误处理机制。

Agent有两种可能的失败处理模型:fail或者:continue。如果是:continue，则在调用错误处理函数之后，action会继续执行就像action导致的异常从来没发生过。如果是:fail，则agent会牌failed状态，并且不会再接收其它的action，直到它被重启（仍然会保留当前的action队列）。

通常agent会使用:continue模式，并且带有错误处理函数。否则就是默认的:fail模式。

### 处理Agent的failed状态
restart-agent

### 等侍agent
尽管agent是异步处理的，但是有时仍然可能需要等侍某个agent更新结果。可以用await和await-for来等侍agent的操作。

### 关闭agent
shutdown-agents应该在应用程序关闭之前执行，因为在这之后，所有send和send-off都将导致异常。
