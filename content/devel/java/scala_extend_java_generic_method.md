Title: Scala继承Java泛型方法的问题
Date: 2018-07-23
Modified: 2018-07-23
Category: 开发
Tags: scala, jtv

# 问题

在使用Scala实现[JTV]({filename}jtv4.md)客户端界面程序时，我遇到了Scala重载Java类中的泛型方法的问题。

因为界面上的`JList`使用了自定义的元素类型，我需要自定义`ListCellRender`来列表对象中元素行的显示。最简单的方法就是直接继承`DefaultListCellRenderer`，它会将`JList`中的数据元素渲染为`JLabel`，我只需要覆盖其`getListCellRendererComponent`实现元素转`JLabel`的逻辑即可。

自定义类的结构如下：

```scala
class FileRender extends DefaultListCellRenderer{
    override def getListCellRendererComponent(list: JList[_], value: scala.Any, index: Int, isSelected: Boolean, cellHasFocus: Boolean): Component = super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus)
  }
```

编译时会产生错误：

```
Error:(441, 9) class FileRender needs to be abstract, since method getListCellRendererComponent in trait ListCellRenderer of type (x$1: javax.swing.JList[_ <: Object], x$2: Object, x$3: Int, x$4: Boolean, x$5: Boolean)java.awt.Component is not defined
  class FileRender extends DefaultListCellRenderer{
```

# 原因分析

查看`DefaultListCellRender`和`ListCellRender`

```java

public class DefaultListCellRenderer extends JLabel
    implements ListCellRenderer<Object>, Serializable
{
    public Component getListCellRendererComponent(
        JList<?> list,
        Object value,
        int index,
        boolean isSelected,
        boolean cellHasFocus)
    {
    ...
    }
...
}

public interface ListCellRenderer<E>
{
    Component getListCellRendererComponent(
        JList<? extends E> list,
        E value,
        int index,
        boolean isSelected,
        boolean cellHasFocus);
}
```

从错误信息中可以看到，错误的原因在于我们的实现与`ListCellRender`中方法的泛型参数不匹配。先把第一个参数的泛型参数按错误提示进行修正：

```scala
class FileRender extends DefaultListCellRenderer{
    override def getListCellRendererComponent(list: JList[_ <: Object], value: scala.Any, index: Int, isSelected: Boolean, cellHasFocus: Boolean): Component = super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus)
  }
```

再编译时，编译器会提示`getListCellRendererComponent`未覆盖任何方法。

从错误信息中可以了解到，应该是由于Scala对于Java实现对接口中的泛型参数无法理解。而我们编写的Scala继承Java类之后，Scala编译器不认为Java实现类与接口中的两个方法具有相同的方法签名。无论我们按接口的签名编写，还是按Java实现类的编译都会导致编译失败。

# 解决

在网上搜索这个问题找到了几篇有价值的贴子：

[类似问题](https://stackoverflow.com/questions/6440176/scala-overriding-generic-java-methods-ii)

[Martin Odersky对这类问题的回复](https://issues.scala-lang.org/browse/SI-1737?focusedCommentId=44321&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-44321)

在这个贴子中，Martin Odersky对这类问题的建议是用Java编写一个实现类，之后再用Scala继承。

[同一个问题](https://www.scala-lang.org/old/node/10687)

而针对我们这个具体的问题，上面这个篇贴子给出的方法更简单。它直接用Scala编写`ListCellRender`的实现，用它作为`DefaultListCellRender`的代理类。

```scala
class FileRender extends ListCellRenderer[FileInfo]{
  val render = (new DefaultListCellRenderer).asInstanceOf[ListCellRenderer[FileInfo]]

  override def getListCellRendererComponent(list: JList[_ <: FileInfo], value: FileInfo, index: Int, isSelected: Boolean, cellHasFocus: Boolean): Component = {
    val result = render.getListCellRendererComponent(list,value,index,isSelected,cellHasFocus)
    val label = result.asInstanceOf[JLabel]
    label.setText(value.file.getName)
    label.setIcon(ImageUtils.toImageIcon(value.icon))
    label
  }
}
```
