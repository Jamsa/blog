Title: 设计模式回顾
Date: 2014-11-04
Modified: 2014-11-04
Category: devel
Tags: java,design pattern

# 设计模式回顾

## 创建模式
### Simple Factory
工厂类提供静态方法来创建某一接口类型的具体实现，该方法根据传入的参数来决定需要创建哪种类型的实现，因此传入的参数一般带有具体的类型信息（ class 的完整名称，或在某个包下的简称等等）。
举例：音乐盒接口的实现有钢琴音乐盒，小提琴音乐盒，有一音乐盒工厂类，它的 createMusicBox 方法内部根据参数来创建钢琴音乐盒或小提琴音乐盒。

### Abstract Factory
抽象工厂模式一般用于创建一套对象，它将具体的某套对象的创建方法封装在对应的工厂类实现里。这些工厂类实现了同一接口（抽象工厂）。工厂类接口中的各个方法都返回接口类型。在具体工厂类的实现中它的各个方法能返回一套实现中不同类型的对象。
举例：多套 UI 组件具有不同的外观，每一套都由实现同一抽象工厂接口的具体工厂类型来创建。抽象工厂接口里规定了能创建哪些 UI 组件，各个组件的接口类型是什么。具体工厂实现里的各个方法会根据它的风格创建出对应的UI组件。

### Builder
当创建复杂的对象或结构时，需要一个负责指挥的的导演类对象，它根据传递给它的 IBuilder ，按某一步骤来进行对象的构建。IBuider中 的各个方法代表构建过程的不同步骤。IBuilder 可以有多个不同的实现。

### Factory Method
Factory Method 会在抽象类中留下某个创建 IProduct 类型对象的方法(即创建对象的工厂方法)没有实现，而抽象类中其它方法都使用 IProduct 接口来操作该对象。
通常抽象类自己会调用这个抽像方法，并将创建出来的对象保存在抽象类的某个属性中，抽象类的其它方法直接使用 IProduct 接口来操作这一对象实例。

### Prototype
通过 clone 原型对象来创建新的实例。

### Singleton
单例模式的观念简单但很多时候会根据具体的环境进行调整和变化，比如多线程，lazy 实例化等。

### Registry of Singleton
处理 Singleton 存在子类型的问题。
Singleton 的类型中定义一个 Map 保存 Singleton 各子类型的单实例对象，并提供一个 register 方法给 Singleton 的子类型注册其单实例。在 Singleton 的 getInstance 方法会根据当前的环境或配置到 map 中去 lookup 满足条件的实例。
在情况比较简单的情况下也可以不使用 register 方法，而直接根据当前的环境或配置通过反射获取类型并进行 Singleton 子类对象的实例化。

## 结构模式
### Default Adapter
继承实现了某一接口的类（实现的方法中几乎什么都不做），而不是直接实现该接口的所有方法。这个实现了接口的类就是这一接口的缺省适配器，它能避免实现接口时需要实现该接口所有方法的问题。

### Object Adapter
Adapter 通过实现目标 ITarget 接口，将被适配类型 Adaptee 的实例包装成 ITarget 类型。这一模式中 Adapter 类型不需要继承 Adaptee 类型，它只需要用一个实例变量来保存 Adaptee 类型的实例。

### Class Adapter
Adapter 直接继承被适配类型 Adaptee 和 Target 类型，这需要语言层面支持多继承。在 Java 中只能实现继承 Adaptee 类型和 实例 ITarget 接口，这一限制也导致它在 Java 中的使用场合较少。

### Bridget
GOF 中指出 Bridge 的目的是：“将抽象部分与它的实现部分分享，使它们都可以独立的变化。”，即将对象的行为定义与针对于特定类型的行为实现进行分离。这样可以让行为定义部分和行为实现两部分互不交错，都可以持续的扩充下去。

### Composite
使用 Composite 类型来定义树状组合结构。Composite 对象中可以添加其它的 Composite 对象，这样可以组合出更为复杂的大对象。而对 Composite 实例的方法调用，可以触发属于它的 Composite 实例的方法调用，保持整个 Composite 行为的一致。
举例：以绘图程序来说，定义一个图像 Component 为基础类型，直线、文字、矩形都是它的子类型，它们都实现了 Component 中定义的 draw 等基本接口，而图像容器 Container 则实现了 Component 的添加、删除、获取子图像的接口，它的 draw 方法会调用属于它的所有子元素的 draw 方法。这样就能通过将 Component 对象的嵌套，构造出复杂的结构。

### Decorator
装饰器模式能动态的为被装饰的对象添加新功能。
举例：Swing 中的 JTextArea 并没有带滚动条，只需要给它加上 JScrollPane 装饰器就可以实现滚动条的功能。抽象的装饰器与被装饰对象都实现了同样的接口，抽象装饰器中通常包含了一个被装饰的对象实例，对装饰器的调用会被转换为对被装饰对象的调用。包含其它功能的装饰器，可以继承自抽象装饰器，以实现更多的功能。
举例：GOF 中 Stream 抽象类和 StreamDecorator 类，Stream 的子类有 MemoryStream 和 FileStream，它们负责处理不同类型的流，但这些类都只负责最基本的字节处理。实现流压缩等功能则没有被编码到 Stream 子类，而是被实现为 StreamDecorator，由它们来提供这些额外的功能，由使用者来决定是否使用这些额外的功能。

### Adapter 与 Decorator 的比较
Adapter 与 Decorator 从定义上比较：
 - 都有个别名叫`包装模式`
 - 装饰模式以对客户端透明的方式扩展对象，是继承关系的替代方案，比继承提供更多的灵活性。使用装饰类的实例，把客户端的调用委派到被装饰类。
 - 适配器模式则是把一个类的接口变换为客户端所期侍的另一种接口，从而使原本类型不匹配的两个类能一起工作。

Adapter 与 Decorator 从使用条件上比较：
 - 装饰模式在需要扩展一个类的功能或者给这个类附加责任时使用；需要动态的给对象增加功能，这些附加的功能和责任可以撤销；所要增加的功能较多，并且排列组合量非常大，使用继承关系变得不现实
 - 适配器模式一般是新系统需要使用现有的类，但这个类已经不符合新系统的要求了。通常在系统升级时使用频率较高。

### Facade
门面模式用于隐藏各个组件之间的合作行为，以及组件本身的操作与设置细节。它会让门面类的使用者损失一些直接操作各个组件细节的方便性。
举例：邮件程序可能要使用 FileUpload, Calendar, SimpleSMTP 等组件，因此可以定义一个 IFacade 及其实现 ConcreteFacade ，由 ConcreteFacade 来调用各个合作组的工作，由 IFacade 向外部提供统一的接口。

### Flyweight
享元模式在描述数量多且性质接近的对象时将对象的信息分为两个部分：内部状态与外部状态。内部状态是对象的可共享部分，外部状态则依赖于具体的场景。
举例：Java 中的字符串使用的就是 Flyweight 模式，它维护了一个 String Pool，对于可共享的字符串对象，它会在 String Pool 中查找是否存在相同的内容，如果有就直接使用。两个指向相同内容的字符串使用 == 进行比较时，有可能返回的就是 true，因为它们可能引用的 String Pool 中的同一对象。

### Proxy
GOF 中给代理模式的目的定义是：给其它对象提供一种代理，以控制对这一对象的访问。
举例：文档中嵌入图片的例子，文档嵌入时并不直接加载图片，而是加载一个图片的代理，它代替图片被加载，以提升加载文档的速度。当文档滚动到图片所在的页数时，这时再加载图片。
代理的实现有两种：静态代理和动态代理：
 - 静态代理直接继承被代理对象的接口，并保存有一个被代理对象的实例。代理对象在调用被代理对象的方法前后加上需要的操作。
 - Java JDK 1.3 之后添加了 Dynamic Proxy 功能，定义一个实现 InvocationHandler 接口的类，它的bind方法将返回一个代理对象，它的 invoke 方法能捕捉到对被代理对象的方法调用。

### Proxy 与 Decorator 的区别
两者都能很容易的在真实对象的方法前后加上自定义的方法。
装饰器模式关注于在对象上动态的添加方法，而代理模式关注于控制对对象的方法。代理类对客户端隐藏对象的具体信息，因此通常在代理类中创建对象实例。而使用装假模式的时候，通常是装饰原始的对象作为参数传递给装饰器的构造器。

## 行为模式
### Chain of Responsibility
GOF 中的定义：使多个对象都有机会处理请求，以避免请求的发送者与接收者之间的耦合关系，将这些对象组合为一个链，并沿着这个链传递请求，直到有对象处理它为止。
因此链上的每个 Handler 都会有个类似于 successor 的对象，它是处理链上的下一个 Handler 。

### Command
以 Swing 中的菜单为例，每个菜单项都有一个 Command 与它对应，actionListener 根据点击的项，获取到对应的 Command 并调用它的方法进行处理。
很多 Web  MVC 框架也是使用这种方式来设计 Controller，由 Invoker 根据客户端请求的路径信息来决定调用某个具体的 Controller。
在使用中通常会将所有 ICommand 接口的实现注册到 Invoker 的一个集合属性中，客户端代码通过调用 Invoker.request 发起请求时，Invoker 根据请求信息（或参数），从集合中获取相应的 ICommand 对象，并调用它实现的 ICommand.execute 方法。

### Interpreter
用于处理层次节点关系中解析每一个节点。（ AST？）

### Iterator
与期在集合对象上直接设计遍历的方法，不如设计为一个 Iterator 接口。当需要对它进行遍历时，将对象包装为一个 Iterator 后返回给客户端。
Iterator 模式可以简化集合对象的使用。

### Mediator
使用一个中间对象来封装对象之间的交互，对象之间不需要知道对方的存在，这样可以降低对象之间的耦合。当某个对象的状态发生变化时，它只需要通知 Mediator，由 Mediator 来处理与之相关的其它对象的状态。如果要改变对象之间的交互行为，也只需要对 Mediator 进行修改。

### Memento
它为对象提供恢复机制。将对象的状态恢复机制放在对象之外，可以减轻对象本身的职责。
Memento 模式中，在 Originator 中有两个方法，一个方法用于获取代表它当前状态的 Memento 对象，另一个方法接收一个 Menento 对象，并将自己恢复为与它相同的状态。Memento 可能包含有 Originator 的所有属性。在外部有一个 Caretaker 来对 Memento 进行维护，每对 Originator 进行一个操作，Caretaker 就将操作前 Originator 的状态保存到它的 Memento 属性中，如果要恢复 Originator 的状态，就只要由 Caretaker 取得 Memento 属性，并对 Originator 进行状态恢复。

### Observer
Observer 模式中的主角为主题（Subject）和观察者（Observer），观察者订阅它感兴趣的主题，一个主题可以被多个观察者订阅，当主题的状态发生变化时，它必须通知（notify）所有订阅它的观察者，观察者检查主题的状态变化，并作出对应的动作，因此 Observer 模式也被称为 Publish - Subscribe 模式。
举例：Java 中实现 Observer 接口的是观察者，这个接口定义了 update 方法，这个方法会在主题对象发生变化时被调用。主题是 Observable 的子类，这个类中有两个重要的方法： setChanged() 和 notifyObserver()。setChanged() 方法用于标明主题对象已经被修改，而 notifyObserver() 方法会通知所有订阅主题对象的观察者，并调用它们的 update() 方法。

### State
状态模式中 IObject 的每个可能的状态都实现 IState 接口。IObject 中的 current 属性是 IState 类型的，用于描述 IObject 的当前状态。当 IObject 的状态需要修改时，则它会调用 current 中的相关方法，并将自己传递给该方法，current 的这个方法会调用这个 IObject 的 setCurrentState() 方法来更新状态。
这样处理的好处是，当状态迁移关系是复杂的网状结构时，各个 IState 的实现可以根据传递进来的 IObject 的属性和自身的信息，决定 IObject 的下一个状态。即在设置下一个合理的状态时，只需要考虑当前的状态值，而不需要从整个状态迁移网来判断下一状态，避免大量的判断和检查。

### Strategy
将策略封装成对象，而不是将策略写死在某个类中，这样策略可以独立于客户端运行，随时可以增加新策略，减少策略，即使是修改某个策略也不会对客户端造成影响。
举例：在 CMS 区块内容的设置时，不应该根据区块内容的类型写死每个类型的处理策略。而应该将不同的类型包装为多个单独的策略（将所有策略注册为字典），这样就可以很方便的增加新策略。
```Java
public interface IState{
    public void switchFire(FireSwitch sw);
}
public class OffState implements IState{
    public void switchFire(FireSwitch sw){
        sw.setState(new SmallState());
    }
}
public class SmallState implements IState{
    public void switchFire(FireSwitch sw){
        sw.setState(new OffState());
    }
}
public class FireSwitch{
    private IState current = new OffState();
    //状态设置方法
    public void setState(IState s){
        current = s;
    }
    
    //状态切换接口
    public void switchFire(){
        current.switchFire(this);
    }
}
```

### Template Method
举例：比如在需要按一定的流程规则处理一些步骤时，可以在抽像类中将处理流程规划好，而具体流程中的各个步骤留给具体的实现类来处理。
Factory Method 可以将对象的创建推迟至子类来决定，而 Template Method 则是将流程中各步骤的具体实现推迟至子类来实现。

### Visitor
当集合中保存有实现了同一接口的多种类型的对象，而在遍历这些对象时，需要调用这些元素的具体类型上的方法时，可以使用 IVisitor 来实现，IVisitor 中的 visit 方法通过方法重载能处理集合中的各种类型。
Visitor 是基于方法重载而实现的。
```Java
public interface IElement{
    public void accept(IVisitor visitor);
}
//或
public abstract AbstractElement{
    public void accept(IVisitor visitor){
        visitor.visit(this);
    }
}

public interface IVisitor{
    public void visit(ElementA element);
    public void visit(ElementB element);
    public void visit(ElementC element);
}
```

## 多线程相关
### Guarded Suspension
举例：服务器需要处理来自多个客户端的请求，为了不丢失客户端的请求，它需要维持一个缓冲区，客户端的请求先被保存在缓冲区，服务器从缓冲区中读取请求并执行，如果缓冲区没有请求，服务器就一直等侍，直到有新的请求存入缓冲区。
```Java
public class RequestQueue{
    private java.util.LinkedList queue = new java.util.LinkedList();
    public synchronized Request getRequest(){
        while(queue.size()<=0){
            try{
                wait();
            }catch(InterruptedException e){}
        }
        return (Request)queue.removeFirst();
    }
    
    public synchronized void putRequest(Request request){
        queue.addLast(request);
        notifyAll();
    }
}
```

### Producer Consumer
它与 Guarded Suspension 是类似的，只不过 Guarded Suspension 模式并不限制缓冲区的长度，Producer Consumer 模式假设所生产的产品旋转在一个长度有限的缓冲区中。缓冲区满了，则生产者必须停止继续将产品放入缓冲区，直到消费者取走了产品而有了空间，如果缓冲区中没有产品，则消费者必须等侍，直到有新的产品放入缓冲区。

### Worker Thread
它对于 Request 的管理上像是 Producer Consumer 模式，而在 Request 的行为上像上 Command 模式。Consumer 取得 Request 之后，执行 Request 中指定的请求方法，也就是使用 Command 模式。
在这一模式下，通常 Request 缓冲区还管理了 Consumer，即在 Request 中有一个 WorkerThread 池，Consumer 初始化时会启动这个池中的所有线程，这些线程自己从 Consumer 中获取 Request（Command）, 并调用它的 exeucute 方法。当 Request 缓冲区中没有新的 Request 时，线程从缓冲区获取 Reuqest 的操作会被阻塞。

### Thread-Per-Message
简单来说就是在某个请求发生时，生成一个执行线程来执行该请求，而主线程继续向下执行。

### Future
Future 模式可以看成 Proxy 模式与 Thread-Per-Message 模式的结合。Future 模式中在请求发生时，会先产生一个 Future 对象给发出请求的客户，它的作用就像是 Proxy 对象，与此同时，客户端真正需要的目标对象在一个新的线程（Thread-Per-Message）中开始创建，等到创建过程结束，就将它放入 Future 之中，当客户端真正需要该对象时，它就已经准备好了，可以让客户端提取。

### Read-Write-Lock
简单来说就是读取和写入某个文件或对象时都需要先取得锁。这样可以保证读取方始终得到的是最新的数据。
可以在处理过程中添加类似 writeFirst 的标记，确保在读写请求都存在时写入请求先被执行。

### Two-phase Termination
两阶段终止，在线程的终止时使用两阶段终止，可以尽量让线程完成当前周期的工作。
```Java
public class SomeThread extends Thread{
    private boolean isContinue = false;
    public void terminate(){
        isTerminated = true;
        interrupt();
    }
    
    private void beforeShutdown(){}
    
    public void run(){
        try{
            while(!isTerminated){
                
            }
        }catch(IterruptedException e){
        }finally{
            beforeShutdown();
        }
    }
}
```

### Thread-Specific Storage
各个线程之间不共享资源，而是各自使用一个资源的副本，将每个线程的数据存储行为加以隔离。
举例：Java 中的 ThreadLocal。
