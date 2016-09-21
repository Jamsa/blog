Title: Ext JS 5 手册 核心概念（五）事件
Date: 2015-05-17
Modified: 2015-05-17
Category: devel
Tags: javascript,extjs

# Ext JS 5 手册 核心概念（五）事件

## 核心概念
### 使用事件
Ext JS 中的组件和类在其生命周期中会产生大量的事件。事件能让你的代码响应程序的变化。
#### 什么是事件
以 Ext.Component 渲染到屏幕上为例，Ext JS 会在渲染完成后产生事件。我们可以配置一个`listeners`对象来监听这个事件：
```javascript
Ext.create('Ext.Panel', {
    html: 'My Panel',
    renderTo: Ext.getBody(),
    listeners: {
        afterrender: function() {
            Ext.Msg.alert('We have been rendered');
        }
    }
});
```

#### 监听事件
```javascript
Ext.create('Ext.Button', {
    renderTo: Ext.getBody(),
    text: 'My Button',
    listeners: {
        mouseover: function() {
            this.hide();
        },
        hide: function() {
            // Waits 1 second (1000ms), then shows the button again
            Ext.defer(function() {
                this.show();
            }, 1000, this);
        }
    }
 });
```

#### 在后期添加监听器
可以使用`on`函数来给组件添加监听器：
```javascript
var button = Ext.create('Ext.Button', {
    renderTo: Ext.getBody(),
    text: 'My Button'
});

button.on('click', function() {
    Ext.Msg.alert('Event listener attached by .on');
});

button.on({
    mouseover: function() {
        this.hide();
    },
    hide: function() {
        Ext.defer(function() {
            this.show();
        }, 1000, this);
    }
});
```

#### 移除监听器
使用`un`函数可以移除监听器：
```javascript
var doSomething = function() {
    Ext.Msg.alert('listener called');
};

var button = Ext.create('Ext.Button', {
    renderTo: Ext.getBody(),
    text: 'My Button',
    listeners: {
        click: doSomething,
    }
});

Ext.defer(function() {
    button.un('click', doSomething);
}, 3000);
```

#### 监听器的作用域
作用域限定了监听处理器的取值范围。默认情况下，这个范围限定在触发事件的对象实例上。但是可以通过`scope`属性指定作用域：
```javascript
var panel = Ext.create('Ext.Panel', {
    html: 'Panel HTML'
});

var button = Ext.create('Ext.Button', {
    renderTo: Ext.getBody(),
    text: 'Click Me'
});

button.on({
    click: {
        scope: panel,
        fn: function() {
            Ext.Msg.alert(this.getXType());
        }
    }
});
```
这个例子中的`this`指向 Panel。运行这个例子将看到弹出了 Panel 的 xtype。

#### 只监听一次
```javascript
var button = Ext.create('Ext.Button', {
    renderTo: Ext.getBody(),
    text: 'Click Me',
    listeners: {
        click: {
            single: true,
            fn: function() {
                Ext.Msg.alert('I will say this only once');
            }
        }
    }
});
```

#### 使用缓存配置
对于那些发生频率很高的事件，我们可以使用`buffer`重新配置发生的次数。在下例中我们只需要让按钮每2秒才触发一次，而不管点击了多少次：
```javascript
var button = Ext.create('Ext.Button', {
    renderTo: Ext.getBody(),
    text: 'Click Me',
    listeners: {
        click: {
            buffer: 200,
            fn: function() {
                Ext.Msg.alert('I say this only once every 2 seconds');
            }
        }
    }
});
```

#### 产生自定义事件
可以调用`fireEvent`来产生自定义事件。下例产生了名为`myEvent`的事件，并传递了两个参数——按钮自身和一个 1 至 100 之间的随机数：
```javascript   
var button = Ext.create('Ext.Button', {
    renderTo: Ext.getBody(),
    text: "Just wait 2 seconds",
    listeners: {
        myEvent: function(button, points) {
            Ext.Msg.alert('myEvent fired! You score ' + points + ' points');
        }
    }
});

Ext.defer(function() {
    var number = Math.ceil(Math.random() * 100);

    button.fireEvent('myEvent', button, number);
}, 2000);
```
这里使用了`Ext.defer`延时 2 秒来触发自定义事件。

#### 监听 DOM 事件
不是每个 Ext JS 组件都会抛出所有事件。但是通过定位 container 上的元素，我们可以产生原生事件并监听它们。以 Ext.container.Container 为例，它并没有 click 事件，但是我们可以给它一个：
```javascript
var container = Ext.create('Ext.Container', {
    renderTo: Ext.getBody(),
    html: 'Click Me!',
    listeners: {
        click: function(){
            Ext.Msg.alert('I have been clicked!')  
        }
    }
});

container.getEl().on('click', function(){ 
    this.fireEvent('click', container); 
}, container);
```
如果不添加第二段代码，container 的 click 监听器不会被触发。

#### 事件标准化（Event Normalization）
事件标准化是 Ext JS 5 应用支持触屏设备的关键。它能将标准的鼠标事件转换成触摸和点击事件（Pointer event）。

Pointer 事件是 w3c 标准中用来处理坐标系事件的，它与输入设备无关（鼠标、触控、触控笔等等）。

当你的代码需要监听一个鼠标事件时，框架会附加到一个对应的触控或点击事件上。比如应用程序需要监听`mousedown`时：
```javascript
myElement.on('mousedown', someFunction);
```
事件系统在某些设备上会将它转换到`touchstart`事件上：
```javascript
myElement.on('touchstart', someFunction');
```
而在某些系统上会将它转换到`pointerdown`事件上：
```javascript
myElement.on('pointerdown', someFunction);
```
这个转换的发生是`in place`的，因此不需要为不同设备编写不同的代码。

在多数情况下框架能无缝的进行鼠标、触控、点击之间的转换。但是某些鼠标交互（如`mouseover`）无法转换成对应的触控动作。这些事件的处理需要使用下一节中提到的方式进行处理。

#### 手势
除标准的 DOM 事件之外，元素也可以产生合成的`gesture`事件。

从浏览器的角度来看，主要有 3 种类型的点击、触控和鼠标事件——开始、移动和结束：

|| *Event* || *Touch*    ||   *Pointer*   ||   *Mouse*   ||

|| *Start* || touchstart ||  pointerdown  ||  mousedown  || 

|| *Move*  || touchmove  ||  pointermove  ||  mousemove  ||

|| *Stop*  || touchend   ||  pointerup    ||             ||

根据解释这些事件发生的时间和顺序，框架能合成更复杂的事件，比如：`drag`,`swipe`,`longpress`,`pinch`,`rotate`和`tap`。Ext JS 应用可以像监听普通事件一样监听这些事件。

Sencha 触控事件系统主要是为触控事件来设计的。通过添加对点击和鼠标事件的完全支持，Ext JS 5 允许手势系统响应任何类型的输入。这意味着你不光可以使用触控输入设备来产生手势事件，也可以使用鼠标来产生单点触控事件。这使得手势系统在不同的设备和输入类型上是无缝切换的。


