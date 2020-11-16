---
title: "Ext学习笔记"
date: 2008-03-19
modified: 2008-03-19
categories: ["前端"]
tags: ["extjs","javascript"]
---

# 基础

# Ext继承机制

# Ext对象
Ext.onReady()是Ext.EventManager.onDocumentReady()的速写方法。

# 布局管理
## Ext.Viewport
Ext.Viewport是一个特殊的容器它代表应用的可视区域（浏览器的Viewport）。

Viewport自动将自己渲染到document.body，因此不需要要调用render方法。它在浏览器的viewport调整大小时自动调整自己的大小并管理窗口（Ext的窗口）的大小改变。

## Ext.Component
Ext.Component是所有Ext组件的基类。所有Component的子类能被乍动
xtype用于标识所需要生成的组件的类型。
下面两个写法效果是一样的：
```javascript
    var viewport = new Ext.Viewport({
        layout:'border',
        items:[
            new Ext.BoxComponent({
                xtype:'box',
                region:'north',
                el: 'north',
                height:32
            }),
            new Ext.BoxComponent({
                region:'south',
                el: 'south',
                height:32
            }),
            new Ext.BoxComponent({
                xtype:'box',
                region:'center',
                el:'center'
            })
        ]
    });
```
```javascript
    var viewport = new Ext.Viewport({
        layout:'border',
        items:[
            {
                xtype:'box',
                region:'north',
                el: 'north',
                height:32
            },
            new Ext.BoxComponent({
                region:'south',
                el: 'south',
                height:32
            }),
            {
                xtype:'box',
                region:'center',
                el:'center'
            }
        ]
    });
```

# 其它

## ExtJS中FormPanel实现数据加载和提交
在使用使用FormPanel时我们通常需要使用它的form对象来加载数据或提交数据。FormPanel中的form对象为Ext.form.BasicForm类型的对象，它有load和submit方法分别用于加载数据和提交数据。而这两个方法都是通过调用Ext.form.BasicForm中的doAction方法来操作的。doAction方法带有两个参数，其中第二个参数为从load或submit方法传递过来的Ext.form.Action对象的配置数据（Config Options）。其中的success和failure属性是用于处理请求成功或失败的函数。但需要注意的是，文档中的说明是这个success或failure取决于Http请求过程是否出错。实际情况却并非这样，我在开发过程中发现HTTP响应代码一直都是200，但被调用的函数却一直都是failure属性对应的函数。通过查看Action.js可以发现响应过来的数据是需要符合一定格式的，Ext.form.Action.Load的API文档开头就说明了响应数据包必须类似下面的格式：
```javascript
{
    success: true,
    data: {
        clientName: "Fred. Olsen Lines",
        portOfLoading: "FXT",
        portOfDischarge: "OSL"
    }
}
```
这个说明在我使用ExtJS的时候再次误导了我。我认为只需要响应的数据为类似的格式就可以了。结果仍然出错，查看Action.js中的handleResponse方法可以看出，返回的数据为上面代码的格式，但并不是说从服务端发送过来的数据就是这样的格式，而是需要将Ext.form.Action.Load的result属性设置成上面的格式的数据。从handleResponse也可以看出，Action.js使用了form.reader属性来处理服务端数据。这个属性也可以在初始化FormPanel的时候传递给FormPanel，FormPanel将会把这个属性传递给它内置的BasicForm对象。怎样使用JsonReader来使提取响应数据来使它满足PanelForm的要求呢？再看handleResponse中的代码，在reader存在的情况下，它返回的是所需要的格式的数据，一个包含success属性和data属性的对象，而data属性来自于JsonReader的read方法处理后的结果。再查看JsonReader.js中的read方法，它调用的是readRecords来读取数据，而返回的值是由reader的root属性决定的，从JsonReader.js中还可以看出，root属性对应的JSON对象必须是集合类型的，因此我们在后台发送过来的数据必须也是集合类型，我在这里也出了错。一直认为加载数据到Form里，一次只加载一条，所以从服务端传递过来的数据都是单个的对象，而将JsonReader对象的root设置为单个对象的名称，结果Form中一直都加载不上数据。后来将服务端传递过来的数据修改为集合数型问题解决了。

小结：

 1.ExtJS中JsonReader对于数据的处理总是一致的，不管你需要的是单条记录还是多条记录，它总是通过total属性判断记录数，通过root属性对应的名称来取记录集合。

 2.FormPanel中处理数据的为内置的BasicForm类型的对象，它通过load和submit方法来加载或提交数据。而这两个方法是通过Ext.form.Action的两个子类Ext.form.Action.Load、Ext.form.Action.Submit来提交请求和调用用户的success和failure方法。决定调用success和failure的并非Http请求是否出错，而是决定于Action.js中handleResponse的处理结果。我们可以通过设置FormPanel的reader配置对象来干预handleResponse对数据的处理。而这个reader也可设置响应数据与FormPanel中字段的对应关系。

 3.多看源码，可以获取更多。

附：

表格中双击进行编辑的JS源码，这个代码比官方文档中的处理方式简单一些，觉得官方文档中的edit中加载数据的处理是一种hack的方式，并不太适合实际应用。

[[http://extjs.com/learn/Tutorial:Using_Ext_grid_form_dialog_to_achieve_paging_list,_create,_edit,_delete_function][ExtJS网站上的CRUD的文章，其中包含有加载数据进行编辑的例子]]
```javascript

Ext.onReady(function(){
var newFormWin;
var form1;

    //表格处理
    //Ext.BLANK_IMAGE_URL = 'extjs/resources/images/default/s.gif';
    Ext.QuickTips.init();
    var sm = new Ext.grid.CheckboxSelectionModel(); //CheckBox选择列

    var cm = new Ext.grid.ColumnModel([
        new Ext.grid.RowNumberer(), //行号列
        sm,
        {header:'编号',dataIndex:'id'},
        {header:'性别',dataIndex:'sex',renderer:function(value){
            if(value=='1'){
                return "男";
            }else{
                return "女";
            }
        }}, //增加性别，自定义renderer，即显示的样式，可以加html代码，来显示图片等。
        {header:'名称',dataIndex:'name'},
        {header:'描述',dataIndex:'memo'}
    ]);

    var ds = new Ext.data.Store({
        proxy: new Ext.data.HttpProxy({url:ACTION_URL}),//调用的动作
        reader: new Ext.data.JsonReader({
            totalProperty: 'total',
            root: 'list',
            successProperty :'success'
        },
                                        [{name: 'id',mapping:'id',type:'string'},
                                         {name: 'sex',mapping:'sex',type:'string'},
                                         {name: 'name',mapping:'name',type:'string'},
                                         {name: 'memo',mapping:'memo',type:'string'} //列的映射
                                        ])
    });


    var grid = new Ext.grid.GridPanel({
        id: 'grid',
        el: 'center',
        region:'center',
        title:'用户',
        ds: ds,
        sm: sm,
        cm: cm,
        bbar: new Ext.PagingToolbar({
            pageSize: 10,
            store: ds,
            displayInfo: true,
            displayMsg: '显示第 {0} 条到 {1} 条记录，一共 {2} 条',
            emptyMsg: "没有记录"
        }) //页脚显示分页
    });


    //布局处理
    Ext.state.Manager.setProvider(new Ext.state.CookieProvider());
    new Ext.Viewport({
        layout:'border',
        items:[
            {
                xtype:'box',
                region:'north',
                el: 'north',
                height:32,
                title:'north'
            },{
                region:'south',
                contentEl: 'south',
                split:true,
                height: 100,
                minSize: 100,
                maxSize: 200,
                collapsible: true,
                title:'South',
                margins:'0 0 0 0'
            },
            grid
        ]
    });

    //el:指定html元素用于显示grid
    grid.render();//Ext.getCmp('grid').render();//渲染表格
    ds.load({params:{start:0, limit:10}}); //加载数据

    grid.on("rowdblclick", function(grid) {
        loadFormData(grid);
        //alert(form1.reader);
    });

    // 载入被选择的数据行的表单数据
    var loadFormData = function(grid) {
        var _record = grid.getSelectionModel().getSelected();
        if (!_record) {
            Ext.example.msg('修改操作', '请选择要修改的一项！');
        } else {
            myFormWin();
            form1.form.load( {
                url : EDIT_ACTION_URL+'?sid='+ _record.get('id'),
                waitMsg : '正在载入数据...',
                success : function(form,action) {
                    Ext.example.msg('编辑', '载入成功！');
                },
                failure : function(form,action) {
                    Ext.example.msg('编辑', '载入失败');
                }
            });
        }
    };




    var myFormWin = function() {
        // create the window on the first click and reuse on subsequent
        // clicks

        if (!newFormWin) {
            newFormWin = new Ext.Window( {
                el : 'topic-win',
                layout : 'fit',
                width : 400,
                height : 300,
                closeAction : 'hide',
                plain : true,
                title : '窗口',
                items : form1
            });
        }
        newFormWin.show('New1');
    };



    form1 = new Ext.FormPanel( {
        // collapsible : true,// 是否可以展开
        labelWidth : 75, // label settings here cascade unless overridden
        url : 'AddLevel.action',
        frame : true,
        title : '修改',
        bodyStyle : 'padding:5px 5px 0',
        width : 350,
        waitMsgTarget : true,
        //这个属性决定了load和submit中对数据的处理，list必须是一个集合类型，json格式应该是[]包含的一个数组
        reader: new Ext.data.JsonReader({root:'list'},
                                        [{name: 'id',mapping:'id',type:'string'},
                                         {name: 'sex',mapping:'sex',type:'string'},
                                         {name: 'memo',mapping:'memo',type:'string'}
                                        ]),
        defaults : {
            width : 230
        },
        defaultType : 'textfield',
        items : [ {
            fieldLabel : '编号',
            name : 'id',
            allowBlank : false
        }, {
            fieldLabel : '性别',
            name : 'sex',
            allowBlank : false
        }, new Ext.form.TextArea( {
            fieldLabel : '备注',
            name : 'memo',
            growMin : 234
        })],

        buttons : [ {
            text : '保存',
            disabled : false,
            handler : function() {
                if (form1.form.isValid()) {
                    form1.form.submit( {
                        url : 'AddLevel.action',
                        success : function(from, action) {
                            Ext.example.msg('保存成功', '添加级别成功！');
                            ds.load( {
                                params : {
                                    start : 0,
                                    limit : 30,
                                    forumId : 4
                                }
                            });
                        },
                        failure : function(form, action) {
                            Ext.example.msg('保存失败', '添加级别失败！');
                        },
                        waitMsg : '正在保存数据，稍后...'
                    });
                    dialog.hide();
                } else {
                    Ext.Msg.alert('信息', '请填写完成再提交!');
                }
            }
        }, {
            text : '取消',
            handler : function() {
                newFormWin.hide();
            }
        }]
    });



});

```

