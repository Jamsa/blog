---
title: "Ext JS 5 手册 核心概念（三）组件"
date: 2015-05-17
modified: 2015-05-17
categories: ["前端"]
tags: ["javascript","extjs"]
---

# Ext JS 5 手册 核心概念（三）组件
## 核心概念
### 组件
Ext JS 应用中的 UI 是由一个或多个被称为`组件(Components)`的构件组成的。所有组件都是`Ext.Component`的子类，它能自动管理组件的生命周期，如：实例化、渲染、改变大小和位置、销毁。
#### 组件的层级
`Container`是一种特殊的能包含其它组件的组件。一个典型的应用是由一些树状嵌套的组件组成的，由`container`来负责管理组件和它们的子组件的生命周期，包括它们的：创建、渲染、改变大小和位置、销毁。一个典型应用的组件层级是由顶部的`Viewport`开始，它包含了其它`containers`和组件嵌套而成：
![组件层级](../extjs5_guide/component_heirarchy_5.png)
子组件通过`Container`的`items`配置属性添加到`Container`中。

`Containers`使用布局管理器来确定子组件的大小和位置。

#### XTypes和延时实例化
每个组件都有个被称为`xtype`的符号名称。比如`Ext.panel.Panel`的`xtype`是`panel`。在大型应用中，并不是所有界面上用到的组件都需要立即被实例化，某些组件在应用中可能永远都不会使用，因此不需要被实例化。这也是使用`xtype`的一个原因，它能让`Container`的子元素先进行配置，但是直到`Container`决定在必要时才进行实例化。

#### 显示和隐藏
所有组件都有内置的`show`和`hide`方法。默认使用的 CSS 的`display:none`来隐藏组件，但是也可以通过`hideMode`配置属性来进行控制：
```javascript
var panel = Ext.create('Ext.panel.Panel', {
        renderTo: Ext.getBody(),
        title: 'Test',
        html: 'Test Panel',
        hideMode: 'visibility' // 使用 CSS 的 visibility 属性来控制组件的显示和隐藏
    });

    panel.hide(); // hide the component

    panel.show(); // show the component
```
#### 浮动组件
浮动组件使用了 CSS 绝对定位，不参与它所属的`Container`的布局。像`Window`这样的组件默认就是浮动的，但是任何组件都可以通过`floating`配置项被设置为浮动组件。

通常的组件要么具有`renderTo`配置项，要么被添加为某个`Container`的子组件，但是浮动组件不需要这样。浮动组件在初次调用`show`方法时被自动渲染到`body`中。

其它几个与浮动组件相关的配置项和方法：
 - `draggable` 允许组件在屏幕上拖动
 - `shadow` 自定义浮动组件的阴影效果
 - `alignTo()` 将浮动组件对齐到某个特定的元素
 - `center()` 将浮动组件定位到`Container`的中心位置

#### 创建自定义组件
##### 组合或扩展
创建新的 UI 类时，可以使用组合或继承`Component`的方法。

推荐继承功能性最接近的类。因为它能使用 Ext JS 提供的自动化生命周期管理。

##### 子类化
`Ext.Base`是所有类型的基础，这个类的原型和静态成员被所有其它类所继承。

可以向这个`Ext.Base`中添加低层次的功能。

##### 模板方法
Ext JS 使用模板方法模式将行为委派给子类，行为只对子类型有效。

继承链中的每个类都可以向组件的生命周期的某个阶段“贡献”出额外的逻辑代码。每个类都实现了特定的行为并允许继承链中的其它类“贡献”它们的逻辑。

以`render`方法为例，它是`Component`中定义的方法。它的职责是启动组件的渲染阶段。`render`不允许被覆盖，但它会调用`onRender`来允许子类添加它们自己的处理过程。每个子类在`onRender`方法中必须先调用它们的父类的`onRender`方法。

下面的图描述了`onRender`模板方法的运行机制。

`Render`方法被调用时（通常由`Container`的布局管理器）。这个方法可能没有被覆盖，而是继承自`Ext.base`类。它调用当前的子类中实现的`this.onRender`（如果有）。这将调用父类型中的方法。最后，每个类中的功能都调用到了，控制权返回到render函数
![模板方法调用机制](../extjs5_guide/template_pattern.png)
以下是一个`Component`的子类实现的`onRender`方法：
```javascript
Ext.define('My.custom.Component', {
    extend: 'Ext.Component',
    onRender: function() {
        this.callParent(arguments); // call the superclass onRender method

        // perform additional rendering tasks here.
    }
});
```
需要注意的是很多模板方法也有对应的事件。比如`render`事件，它在组件被渲染之后触发。当进行子类化时，必须使用模板方法在生命周期的重要阶段执行它的逻辑，而不使用事件。事件可以以编程的方式挂起，或被事件处理器停止。

以下是`Component`的子类型可以实现的模板方法：
 - `initComponent` 这个方法由构造器调用。它用于初始化数据，设置配置项和添加事件处理器。
 - `beforeShow` 这个方法在组件显示前被调用。
 - `onShow` 在显示操作时添加行为。在调用父类的`onShow`之后，组件将被显示。
 - `afterShow` 这个方法在组件显示后被调用。
 - `onShowComplete` 这个方法在调用调用完`afterShow`之后执行。
 - `onHide` 在隐藏操作时添加行为。在调用你类的`onHide`之后，组件将被隐藏。
 - `onRender` 在渲染阶段添加行为。
 - `afterRender` 在渲染完成之后添加行为。在这个阶段组件的 DOM 元素将按配置被设置样式，会具有任何配置了的 CSS 类名称，并且会被按配置设置为显示和启用状态。
 - `onEnable` 在启用操作时添加行为。在调用父类的`onEnable`之后，组件被启用。
 - `onDisable` 在禁用操作时添加行为。在调用父类的`onDisable`之后，组件被禁用。
 - `onAdded` 在组件被添加到`Container`时添加行为。在这个阶段，组件已经存在于父`Container`的子项集合中。在调用父类的`onAdded`之后，`ownerCt`引用将会存在，如果配置了`ref`，`refOwner`将被设置。
 - `onRemoved` 在组件从`Container`中移除时添加行为。在这个阶段，组件已经被从父`Container`中移出，但是还未被销毁（它将在父`Container`的`autoDestroy`被设置为`true`或调用`remove`时传递的第二个参数为`true`时被销毁）。在调用完父类的`onRemoved`之后，`ownerCt`和`refOwner`将不再存在。
 - `onResize` 在改变大小时添加行为。
 - `onPosition` 在改变位置时添加行为。
 - `onDestroy` 在销毁操作时添加行为。在调用父类的`onDestroy`后，组件将被销毁。
 - `beforeDestroy` 在组件被销毁前执行。
 - `afterSetPosition` 在组件的位置被设置之后执行。
 - `afterComponentLayout` 在组件被布局之后执行。
 - `beforeComponentLayout` 在组件被布局之前执行。

##### 继承哪个类
无论 UI 组件是否需要被渲染和管理，总是倾向于继承`Ext.panel.Panel`。

`Panel`类有非常多的功能：
 - 边框
 - 头部
 - 头部工具条
 - 底部
 - 底部按钮
 - 顶部工具条
 - 底部工具条
 - 容纳和管理子组件

###### Component
如果需要的 UI 组件不需要包含其它组件，而只是一些 HTML，则继承`Ext.Component`也是合适的。

###### Container
如果需要的 UI 组件要能包含其它的组件，但是不需要`Panel`的其它功能，则可以继承`Ext.container.Container`。需要记住`Ext.layout.container.Container`用于渲染和管理子组件。

`Container`有下列额外的模板方法：
 - `onBeforeAdd` 这个方法在添加了新的子组件时被调用。它会传递这个新的组件，以便修改这个组件，或以其它方式准备`Container`。返回`false`时将中止添加操作。
 - `onAdd` 这个方法在添加了新的组件之后执行。它将会传递这个新添加的组件。这个方法可以用于根据子组件的状态更新内部结构。
 - `onRemove` 在子组件被删除时被调用。它将传递要被删除的组件。这个方法可以用于根据子组件的状态更新内部结构。
 - `beforeLayout` 这个方法在`Container`对它的子组件进布局（和渲染）之前执行。
 - `afterLayout` 这个方法在`Container`对它的子组件进行而已（和渲染）之后执行。

###### Panel
如果需要的 UI 组件需要头、尾或工具栏时，应该继承`Ext.panel.Panel`。

重点：`Panel`是一个`Container`。`Layout`是用于渲染和管理子组件的。

继承`Ext.panel.Panel`是应用中经常使用的，用于将 UI 组件进行布局的类，并能使用`tbar`和`bbar`来提供操作。

`Panel`有以下额外的模板方法：
 - `afterCollapse` 这个方法在`Panel`收缩时被调用。
 - `afterExpand` 这个方法在`Panel`展开时被调用。
 - `onDockedAdd` 这个方法在`Docked`项添加到`Panel`上后被调用。
 - `onDockedRemove` 这个方法在`Docked`项从`Panel`上删除后被调用。

