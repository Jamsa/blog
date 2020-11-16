---
title: "Ext JS 5 手册 核心概念（四）数据包"
date: 2015-05-17
modified: 2015-05-17
categories: ["前端"]
tags: ["javascript","extjs"]
---

# Ext JS 5 手册 核心概念（四）数据包

## 核心概念
### 数据包
数据包是应用中处理数据加载和保存的。它包含了很多类，其中以下三个是最重要的：
 - Ext.data.Model
 - Store
 - Ext.data.proxy.Proxy

上面的类几乎在所有应用中都被用到。它们由一些卫星类支撑：

![数据包相关类](../extjs5_guide/data-model.png)

#### Model
类所包的中心是`Ext.data.Model`。`Model`用于描述应用中一个实体。
Model中的主要部分有：
 - Fields
 - Proxies
 - Validations
 - Associations

![Model 的主要组成部分](../extjs5_guide/model-breakdown.png)

##### 创建 Model
通常可以定义一个公用的基础类。这个基类能定义所有 Model 公用的属性。
Model 有两个重要的属性`fields`和`schema`。
```javascript
Ext.define('MyApp.model.Base', {
    extend: 'Ext.data.Model',

    fields: [{
        name: 'id',
        type: 'int'
    }],

    schema: {
        namespace: 'MyApp.model',  // generate auto entityName

        proxy: {     // Ext.util.ObjectTemplate
            type: ajax,
            url: '{entityName}.json',
            reader: {
                type: 'json',
                rootProperty: '{entityName:lowercase}'
            }
        }
    }
});
```

##### Proxy
Proxy 由 Model 和 Store 使用的，用于处理加载和保存 Model 数据的。有两种类型的 Proxy: Client 和 Server。
 - Client Proxy 包括 Memory 和 Local Storage两种。
 - Server Proxy 用于从远程服务端处理数据。例如：AJAX、JSONP、REST。

##### Schema
Schema 是一些有关联关系的实体的集合。当 Model 父类型指定了`schema`属性时，这个属性将会被子类模板继承。

`schema`的`namespace`属性能让所有 Model 得到一个缩短的`entityName`。这个名称主要用于定义 Model 之间的关联关系。

`schema`的`proxy`属性是一个对象模板它与基于 Ext.XTemplate 的文本模板是类似的。不同之处在于当给予对象模板数据时它将产生出来对象来。在上面的代码里，模板数据用于自动定义所有 Model 的`proxy`配置，而不需要显式的定义`proxy`。

这样每个 Model 实例将根据不同的值采用相同的方式来加载数据。可以避免了在不同的 Model 中重复定义 proxy。

#### Store
Model 通常与 Store 一起使用，Store 是记录（Model 子类的实例）的集合。创建 Store 并加载数据：
```javascript
var store = new Ext.data.Store ({
    model: 'MyApp.model.User'
});

store.load({
    callback:function(){
        var first_name = this.first().get('name');
       console.log(first_name);
    }
});
```

##### 内联数据
Store 可以加载内联数据。Store 将会将它的`data`属性中的对象转换成对应的 Model 类型的记录集。
```javascript
new Ext.data.Store({
    model: 'MyApp.model.User',
    data: [{
        id: 1,
        name: "Philip J. Fry"
    },{
        id: 2,
        name: "Hubert Farnsworth"
    },{
        id: 3,
        name: "Turanga Leela"
    },{
        id: 4,
        name: "Amy Wong"
    }]
});
```

##### 排序和分组
Store 可以在本地或远程执行排序、过滤和分组操作。
```javascript
new Ext.data.Store({
    model: 'MyApp.model.User',

    sorters: ['name','id'],
    filters: {
        property: 'name',
        value   : 'Philip J. Fry'
    }
});
```

#### Association
Model 可以通过 Association API 关联起来。多数应用都需要处理很多互相关联的 Model。

以下是一个多对一的关联示例：
```javascript
Ext.define('MyApp.model.User', {
    extend: 'MyApp.model.Base',

    fields: [{
        name: 'name',
        type: 'string'
    }]
});

Ext.define('MyApp.model.Post', {
    extend: 'MyApp.model.Base',

    fields: [{
        name: 'userId',
        reference: 'User', // the entityName for MyApp.model.User
        type: 'int'
    }, {
        name: 'title',
        type: 'string'
    }]
});
```
定义好关联关系之后，就可以很容易的访问关联的数据：
```javascript
// Loads User with ID 1 and related posts and comments
// using User's Proxy
MyApp.model.User.load(1, {
    callback: function(user) {
        console.log('User: ' + user.get('name'));

        user.posts(function(posts){
            posts.each(function(post) {
                console.log('Post: ' + post.get('title'));
            });
        });
    }
});

user.posts().add({
    userId: 1,
    title: 'Post 10'
});

user.posts().sync();

MyApp.model.Post.load(1, {
    callback: function(post) {

        post.getUser(function(user) {
            console.log('Got user from post: ' + user.get('name'));
        });                           
    }
});
MyApp.model.Post.load(2, {
    callback: function(post) {
        post.setUser(100);                         
    }
});
```

##### 加载嵌套数据
定义好关联关系之后，可以在单个请求中加载关联数据。例如，服务端的响应如下：
```javascript
{
    "success": true,
    "user": [{
        "id": 1,
        "name": "Philip J. Fry",
        "posts": [{
            "title": "Post 1"
        },{
            "title": "Post 2"
        },{
            "title": "Post 3"
        }]
    }]
}
```
这种情况下框架能自动解析出单个响应中的嵌套数据，而不需要发起两次请求，分别来获取 User 和 Post 的数据。

#### 验证
Model 提供了数据验证的支持。
```javascript
Ext.define('MyApp.model.User', {
    extend: 'Ext.data.Model',
    fields: ...,

    validators: {
        name: [
            'presence',
            { type: 'length', min: 7 },
            { type: 'exclusion', list: ['Bender'] }
        ]
    }
});
```
验证定义时是以字段名作为 key，值作为它的规则。这些规则由一个验证对象配置，或多个验证对象配置数组构成的。上面的这个验证规则验证了`name`字段，它的长度必须大于7，并且不能是`Bender`。
某些验证规则可能会包含不同的属性——比如`min`和`max`属性等等。Ext JS 有5种内置验证器并且易于添加自定义的规则。
 - presence 确保字段有值。
 - length 确保字符串的长度处于`min`和`max`之间，这两个选项都是可选的
 - format 确保字符串匹配某个正则表达式
 - inclusion 确保值匹配某个特定的值列表
 - exclusion 确保值不属于某个特定的值列表

```javascript
// now lets try to create a new user with as many validation
// errors as we can
var newUser = new MyApp.model.User({
    id: 10,
    name: 'Bender'
});

// run some validation on the new user we just created
console.log('Is User valid?', newUser.isValid());

//returns 'false' as there were validation errors

var errors = newUser.getValidation(),
    error  = errors.get('name');

console.log("Error is: " + error);

newUser.set('name', 'Bender Bending Rodriguez');
errors = newUser.getValidation();
```
