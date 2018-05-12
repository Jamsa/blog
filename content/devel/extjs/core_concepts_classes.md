Title: Ext JS 5 手册 核心概念（二）类型系统
Date: 2015-05-17
Modified: 2015-05-17
Category: 前端
Tags: javascript,extjs

# Ext JS 5 手册 核心概念（二）类型系统
## 核心概念
### 类型系统
#### 命名约定
##### 类
类名只允许包含字母和数字。数字是允许使用的，但只在必要时使用。不使用下划线、连字符和其它非数字字母。
类名应该按包分类。至少应该使用唯一的顶级命名空间。
顶级命名字音和类名应该使用驼峰式命名规则，其它部分都使用小写。
非`Sencha`提供的类不应该使用`Ext`作为顶级命名空间。

##### 源文件
类文件名按包路径保存。一个文件中只有一个类。
所有的类都应该放在同一个根目录下。

##### 方法和变量
 - 方法和变量只使用字母和数字。只在必要时使用数字字符。不要使用下划线、连字符和其它非数字字母。
 - 方法和变量名应该使用驼峰式命名。这一规则同样适用于缩略词。

##### 属性
 - 类属性名遵循相同的命名规则
 - 类的静态属性应该全部使用大写

#### 声明
##### Ext JS 4 之前的方式
```javascript
Ext.ns('My.cool');
My.cool.Window = Ext.extend(Ext.Window, { ... });
```
##### 新的方式
```javascript
Ext.define(className, members, onClassCreated);
```

#### 配置
在 Ext JS 4 中使用`config`属性，它由`Ext.Class`前置处理器在类创建前进行处理，它包含以下功能：
 - 配置和封装类专员
 - 自动在类原型中生成属性的`getter`和`setter`方法
 - 为每个属性生成`apply`方法。自动生成的`setter`方法将会在设置值之前调用`apply`方法。可以覆盖属性的`apply`方法来添加自己的逻辑。如果`apply`方法无返回值，则`setter`将不会设置这个值。

在 Ext JS 5 中对于使用`config`的类来说，不再需要手动调用`initConfig()`方法。但是如果你的类继承自`Ext.Base`，则仍要调用`initConfig()`方法。

#### 静态成员
可以使用`statics`来进行配置：
```javascript
Ext.define('Computer', {
    statics: {
        instanceCount: 0,
        factory: function(brand) {
            // 'this' in static methods refer to the class itself
            return new this({brand: brand});
        }
    },

    config: {
        brand: null
    }
});

var dellComputer = Computer.factory('Dell');
var appleComputer = Computer.factory('Mac');

alert(appleComputer.getBrand()); // using the auto-generated getter to get the value of a config property. Alerts "Mac"
```

#### 错误处理和调试
Ext JS 包含了有效的调试和错误处理功能。
 - 可以使用`Ext.getDisplayName()`来获取方法的显示名称。这在发生异常时显示类名和方法名时非常有用。`throw new Error('['+ Ext.getDisplayName(arguments.callee) +'] Some message here');`
 - 当使用`Ext.define()`定义的任何类方法抛出错误时，你可以在基于 WebKit 的浏览器的调用栈中看到方法和类名。
