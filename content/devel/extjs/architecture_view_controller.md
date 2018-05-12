Title: Ext JS5 手册 应用程序架构（二） View Controller
Date: 2015-05-17
Modified: 2015-05-17
Category: 前端
Tags: javascript,extjs

## Ext JS5 手册 应用程序架构（二） View Controller
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
change: 'onBarChange' // no scope given here
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
'#': { // 匹配当前 View 自己
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
