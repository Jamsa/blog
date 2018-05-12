Title: Android Dev Guide学习笔记 User Interface
Date: 2010-08-20
Modified: 2010-08-20
Category: 移动
Tags: android

# 用户界面

在Android应用程序中，用户界面是使用View和ViewGroup对象构造的。有许多类型的view和viewgroup，它们都是View类的子类。

View对象是Android平台表达用户界面的基本单元。View class作为被称作“构件（widget）”的基类，这些构件实现UI对象，如文本域和按钮。ViewGroup类被作为“布局（layout）”类的基类，它用于描述不同的布局方式，如线型、页签等。

View对象的属性中存储了布局参数和屏幕中特定的矩形框中的内容。View对象自己处理自己的度量、布局、绘制、焦点变化、滚动、和在它的矩形范围内的按键/手势交互。用户界面中的View对象也是用户和交互事件接收器的交互点。

# View层级结构
在Android平台上，你可以用一组包含View和ViewGroup节点的层级结构来定义Activity的UI，如下图。这个层级树根据需要可以很简单也可以很复杂，你可以使用Android中预定义的构件和布局来构建它，也可以用自定义的View来构建。

![ViewGroup]({attach}android-dev-guide/viewgroup.png)


为了让view层级树渲染到屏幕上，你的Activity必须调用setContentView()方法并传递一个根节点的引用。Android系统接收到这个引用来废止、度量和绘制这个树。根节点请求它的子节点绘制自己——每个view group节点负责调用它自己的子节点绘制自己。子节点可能会从父节点中请求得到某个位置的一块区块，但是父节点有最终决定分配哪个位置的多大的区域给子节点。Android从树的顶部开始解析布局元素，并实例华它们并将它们添加到它们的父节点。由于这些元素的绘制是按顺序进行的，如果出现元素重叠，则最后绘制的元素将位于先前绘制的元素的上面。

要了解View层级结构的度量和绘制，参见How Android Draws Views。

# 布局
最常见的定义布局和表达view层次结构的是使用XML布局文件。XML布局文件提供了类似HTML的可读性。每个元素表示一个View或ViewGroup对象。View对象是树中的叶节点，ViewGroup对象是树中的分支节点。

XML中的元素代表各自的Java类。因此`<TextView>`元素将在UI中创建一个TextView，`<LinearLayout>`元素将创建一个LinearLayout view group。当加载布局资源时，Android系统将初始化这些运行时对象，并将它们与布局中的元素对应。

例如，一个简单的virtical类型的布局中有一个text view和一个按钮：
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
              android:layout_width="fill_parent" 
              android:layout_height="fill_parent"
              android:orientation="vertical" >
    <TextView android:id="@+id/text"
              android:layout_width="wrap_content"
              android:layout_height="wrap_content"
              android:text="Hello, I am a TextView" />
    <Button android:id="@+id/button"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Hello, I am a Button" />
</LinearLayout>
```
注意这里的LinearLayout元素包含了TextView和Button。你可以在其中嵌套一另一个LinearLayout（或其它类型的ViewGroup），来创建更加复杂的布局。

关于创建UI布局，请参见Declaring Layout。

有多种方法可以进行布局。使用不同类型的view group，你可以构建不限数量的子类型的view和view group。Android系统提供了大量预定义的布局类型，包括：LinearLayout，RelativeLayout，TableLayout，GridLayout等等。每个布局都提供了一套独特的定义子view和布局结构位置的参数。

要了解用于布局的各种view groups，参见Common Layout Objects。

 - Tips：你也可以在Java代码中使用addView(View)方法绘制View和ViewGroups，它可以动态的插入新的View和ViewGroup对象。

# 构件
构件是作为界面与用户交互的View对象。Android提供了一套完整的构件实现，如：按钮、复选框、文本域等，以便快速构建UI。某些Android提供的构件更加复杂，如日期选择、时钟、缩放控件等。但是你并不需要受限于Android平台提供的这些构件。如果你想要进行一些个性化和创建自己的动作元素，你可以通过扩展或组合已有的构件定义自己的View对象。

请阅读Building Custom Components以了解更多。

Android提供的构件位于android.widget包中。

# UI事件
一旦你添加了某些Views（构件）到UI中，你就会需要知道用户与它们的交互，以便执行一些操作。为了得到UI事件通知，你需要做两件事：

 - 定义一个事件监听器并注册到View中。这是如何监听事件的方法。View类包含了一个`<something>Listener`接口的集合，每个里面都有一个名为`On<something>()`的回调方法。例如，View.OnClickListener（用于在处理View中的“click”），View.OnTouchListener（用于处理View中触屏幕事件），View.OnKeyListener（用于处理View中的按键）。因此如果你希望在View中发生“click”（比如按钮被选中）动作时得到通知，应该实现OnClickListener并定义它的onClick()回调方法（在这里执行你的点击动作），并用setOnClickListener()方法将它注册到View。

 - 覆盖View中已存在的回调方法。这在你实现自己的View类并且需要监听某些特定动作时需要进行。例如这些事件：屏幕被接触时（onTouchEvent()），轨迹球动作时（onTrackballEvent()），或当设备上的按键被按下时（onKeyDown()）。这能让你定义在你的自定义View中对于这些事件的默认行为并决定这些事件是否被传递到其它子View。同样，这些都是View类的回调，只在建立自定义组件时才需要定义。

了解关于处理View用户交互的详情请参考Handling UI Events。

# 菜单


# 高级主题

## 适配器

## 风格和主题


