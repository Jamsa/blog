Title: Ext JS 5 手册 应用程序架构（一）应用程序架构简介
Date: 2015-05-17
Modified: 2015-05-17
Category: devel
Tags: javascript,extjs

# Ext JS 5 手册 应用程序架构（一）应用程序架构简介

## 程序架构
### 应用程序架构简介
Ext JS 提供了对 MVC 和 MVVM 架构的支持。

#### MVC
在 MVC 架构中，用户与 View 交互，它显示 Model 中的数据。这些交互由 Controller 来处理，它负责修改 View 和 Model。

View 和 Model 互相是不知道的，因为 Controller 在直接处理更新。即，Controller 包含了 MVC 应用中大多数的程序逻辑。View 有可能也包含了少量业务逻辑。Model 则主要是提供了数据处理和业务逻辑处理的接口。

MVC 的目标是要清楚的区分应用程序中各个类的职责。这意味着在大型项目中能很好的解耦。让程序易于测试和维护，并且便于代码重用。

#### MVVM
MVC 和 MVVM 的区别在于 MVVM 突出了一个抽象的 ViewModel。它通过数据绑定技术来协调 Model 的数据和 View 展现时使用的数据。

这使得框架能处理更多的工作，能最小化或消除程序逻辑中直接处理 View。

#### 用户的使用
Ext JS 5 引入的 MVVM 构架中提升了 MVC 架构中的 C。并且能兼容 Ext JS 4 MVC 应用。

#### MVC 和 MVVM
为了了解哪个更适合你的应用，我们需要了解以下术语：
 - （M）Model 程序中的数据。它由一组定义了字段的构成。Model 知道如何使用 data package 对数据进行持久化，并且能通过 association 关联到其它的 model。Model 通常与 Store 一起使用，为 grid 或其它组件提供数据。Model 也适合进行验证、转换等数据逻辑处理。
 - （V）View 用于展现数据。
 - （C）Controller 用于处理视图中的逻辑。它可以渲染视图、控制路由、实例化 Model、进行其它的逻辑处理。
 - （VM）ViewModel 用于管理特定的 View 的数据。组件能绑定到它，在数据发生变化时组件会自动更新。

这些构架能提供非常好的结构和一致性。遵循以下约定能获取很多好处：
 - 每个应用都是以相同的方式工作的，因此只需要学习一个
 - 很容易在不同的应用间共享代码
 - Sencha Cmd 能为你的应用生成优化版

#### 创建一个示例应用
```sh
sencha generate app -ext MyApp ./app
cd app
sencha app watch
```
#### 应用程序概览
##### 目录结构
Ext JS 应用遵循统一的目录结构。在推荐的目录结构中所有类都放在 app 目录中。这个目录包含的子目录是 MVC 元素的命名空间。View，View Controller 和 ViewModel 都属于视图类元素。

##### 命名空间
每个类的第一行都是它的命名空间。格式为
```
<AppName>.<foldername>.<ClassAndFileName>
```
#### 应用程序
`index.html`中只引用了`bootstrap.js`，它用于加载`app.json`。`app.json`中定义了整个应用的元数据。

`app.json`中添加了大量的注释信息。

##### app.js
应用程序在`Application.js`中定义了应用类，在`app.js`中调用了这个类的实例：
```javascript
/*
 * This file is generated and updated by Sencha Cmd. You can edit this file as
 * needed for your application, but these edits will have to be merged by
 * Sencha Cmd when upgrading.
 */
Ext.application({
    name: 'MyApp',

    extend: 'MyApp.Application',

    autoCreateViewport: 'MyApp.view.main.Main'

    //-------------------------------------------------------------------------
    // Most customizations should be made to MyApp.Application. If you need to
    // customize this file, doing so below this section reduces the likelihood
    // of merge conflicts when upgrading to new versions of Sencha Cmd.
    //-------------------------------------------------------------------------
});
```
`autoCreateViewport`是 Ext JS 5 的一个新功能。通过为 container 类指定`autoCreateViewport`，你可以使用任何类作为你的 Viewport。在这个你还子中我们使用 MyApp.view.main.Main（它是一个 Container 类）作为 Viewport。

##### Application.js
每个 Ext JS 应用都是从一个 Application 类的实例开始的。这个类由 app.js 调用。

```javascript
Ext.define('MyApp.Application', {
    extend: 'Ext.app.Application',

    name: 'MyApp',

    stores: [
        // TODO: add global/shared stores here
    ],

    launch: function () {
        // TODO - Launch the application
    }
});
```
Application 类包含了应用的命名空间、共享的 store 等全局设置。

#### View
View 都是 Ext.Component 的子类。View 包含了应用中所有可以看到的东西。

```javascript
Ext.define('MyApp.view.main.Main', {
    extend: 'Ext.container.Container',

    xtype: 'app-main',

    controller: 'main',
    viewModel: {
        type: 'main'
    },

    layout: {
        type: 'border'
    },

    items: [{
        xtype: 'panel',
        bind: {
            title: '{name}'
        },
        region: 'west',
        html: '<ul>...</ul>',
        width: 250,
        split: true,
        tbar: [{
            text: 'Button',
            handler: 'onClickButton'
        }]
    },{
        region: 'center',
        xtype: 'tabpanel',
        items:[{
            title: 'Tab 1',
            html: '<h2>Content ...</h2>'
        }]
    }]
});
```

View 并不包含任何程序逻辑。所有的 view 逻辑应该放在 ViewController 中。

View 中比较重要的是配置是 controller 和 viewModel。

##### Controller 配置
`controller`配置项可以指定 View 的 ViewController类，它是 View 的事件处理器的容器。

##### ViewModel 配置
`viewModel`配置项可以指定 View 的 ViewModel 类，它是组件的数据提供者。ViewModel 中的数据通常通过组件上的数据绑定来展现和编辑数据。如上例中的面板名称。

#### Controller
```javascript
Ext.define('MyApp.view.main.MainController', {
    extend: 'Ext.app.ViewController',

    requires: [
        'Ext.MessageBox'
    ],

    alias: 'controller.main',

    onClickButton: function () {
        Ext.Msg.confirm('Confirm', 'Are you sure?', 'onConfirm', this);
    },

    onConfirm: function (choice) {
        if (choice === 'yes') {
            //
        }
    }
});
```
查看之前的视图 Main.js，你可以看到 tbar 按钮事件的处理器 onClickButton 就定义在这个 Controller 中。

ViewController 主要用于：
 - 使用`listeners`和`reference`配置连接到 View。
 - View 的生命周期管理将自动管理相关联的 ViewController。从初始化到销毁，Ext.app.ViewController 总是与它相关的组件关联。
 - ViewController 与其管理的 View 是一对一关联的，减少了复杂性
 - 提供了支持 View 嵌套使用的封装
 - 能在关联的 View 的任意层级上选中组件并监听它的事件

#### ViewModel









































Ext JS 5 手册 应用程序架构（二）View Controller

##### 监听
在 Ext JS 5 中对`listeners`这个配置项进行了增强。
```javascript
Ext.define('MyApp.view.foo.Foo', {
    extend: 'Ext.panel.Panel',
    xtype: 'foo',
    controller: 'foo',

    items: [{
        xtype: 'textfield',
        fieldLabel: 'Bar',
        listeners: {
            change: 'onBarChange'  // no scope given here
        }
    }]
});

Ext.define('MyApp.view.foo.FooController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.foo',

    onBarChange: function (barTextField) {
        // called by 'change' event
    }
});
```
上例的`onBarChange`并未指定`scope`，事件系统默认会到 Bar 所属的 ViewController 中去找。

由于历史原因，组件的创建者可以使用`listeners`配置项，那么 View 是怎么监听到它自己的事件呢？答案是需要显式的配置`scope`：
```javascript
Ext.define('MyApp.view.foo.Foo', {
    extend: 'Ext.panel.Panel',
    xtype: 'foo',
    controller: 'foo',

    listeners: {
        collapse: 'onCollapse',
        scope: 'controller'
    },

    items: [{
        ...
    }]
});
```
`scope`选项有两个有效的值：`this`和`controller`。当编写 MVC 应用时通常总会是`controller`，即在 ViewController （不是创建 View 实例的 ViewController）中查找。

由于 View 可能通过 xtype 来创建：
```javascript
Ext.define('MyApp.view.bar.Bar', {
    extend: 'Ext.panel.Panel',
    xtype: 'bar',
    controller: 'bar',

    items: [{
        xtype: 'foo',
        listeners: {
            collapse: 'onCollapse'
        }
    }]
});
```
在这种情况下，Foo 是由 Bar 创建的。它能像 Foo 一样 去监听 collapse 事件。在之前的版本的 Ext JS 中，这种声明方式会导致冲突。在 Ext JS 5 中，解决了这一问题。在 Foo 中声明的事件将会触发在 Foo 的 ViewController 中的监听中。在 Bar 中声明的事件将会触发在 Bar 的 ViewController 中。

##### Reference
我们经常会在编写 controller 时获取某个组件然后对它进行某些操作。比如获取某个表格，然后向表格中添加一行新记录。

但是如何能获取到组件呢？在 Ext JS 4 中，需要使用`refs`配置项或其它的方式查找组件。所有这些技术都需要你在要获取的组件上放置一个特殊的唯一属性来进行标识。旧的技术手段使用`id`配置项（和 Ext.getCmp）或使用`itemId`配置项（使用`refs`或其它组件查询方法）。使用`id`的好处是查询速度快，但是它要求这标识符必须在整个应用程序的 DOM 结构中是唯一的，这通常不方便。使用`itemId`和其它查询方法要更灵活一些，但是也需要执行一些查询才能获取相应的组件。

Ext JS 5 提供了`reference`配置项，可以通过`lookupReference`来获取组件：
```javascript
Ext.define('MyApp.view.foo.Foo', {
    extend: 'Ext.panel.Panel',
    xtype: 'foo',
    controller: 'foo',

    tbar: [{
        xtype: 'button',
        text: 'Add',
        handler: 'onAdd'
    }],

    items: [{
        xtype: 'grid',
        reference: 'fooGrid'
        ...
    }]
});

Ext.define('MyApp.view.foo.FooController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.foo',

    onAdd: function () {
        var grid = this.lookupReference('fooGrid');
    }
});
```
这类似于将`itemId`设置成"fooGrid"并执行“this.down('#fooGrid')”。区别在于`reference`配置项会将自己注册到它所属的 View 中；`lookupReference`方法通过查询缓存来检查 refrence 是否需要刷新。当缓存成功后会从缓存中加载对象。

##### 封装
在 Ext JS 4 MVC 实现中使用选择器非常灵活，但是有时会存在一些风险。这些选择器能“看到”所有的组件。

这个问题可能通过遵循某些最佳实践来解决，但是在 ViewController 中使用`listeners`和`references`会变得简单。因为它们只会在它所属的 ViewController 间建立连接。View 可以使用任何的 reference 值，只要保证所属的 view 中是唯一的，这些名称不会被 view 的创建者暴露出去。

同样，View 会在所属的 ViewController 中查找监听器，而不会将事件分发到由于不正确的选择器所选中的组件的 controller 上。

##### 监听器和事件域
在 Ext JS 4.2中，MVC的事件分发器引入了事件域。事件域在事件发生时拦截事件，并通过选器来匹配并分发到 controller。“组件”事件域有整个组件的选择器，其它域具有限制性的选择器。

在 Ext JS 5 中，每个 ViewController 创建一个被称为“View”事件域的新类型的事件域实例。这下事件域允许 ViewController 使用标准的`listen`和`control`方法限定在它们所属的 View。它也提供了一个特殊的选择器匹配 View 本身：
```javascript
Ext.define('MyApp.view.foo.FooController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.foo',

    control: {
        '#': {  // 匹配当前 View 自己
            collapse: 'onCollapse'
        },
        button: {
            click: 'onAnyButtonClick'
        }
    }
});
```
主要的区别在于上面的监听和选择器。“button”选择器将匹配这个 view 或子 view 中任何的按钮。

最后，这些事件域会向上层的 view 结构 “冒泡”。当事件发生时，首先会投递到标准监听器。然后是投递到它所属的 ViewController，然后是它所属的 view 的父 view 的 ViewController。最后，事件被投递到标准的“component'事件域，被 Ext.app.Controller 派生的控制器处理。

##### 生命周期
   





