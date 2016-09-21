Title: OA Framework应用构建之——错误处理
Date: 2007-08-21
Modified: 2007-08-21
Category: devel
Tags: oracle,ebs,oaf
Slug: build_error

# 异常类型
OA Framework处理三种基本类型的异常：通用、校验和严重。这些类型在这节中简单的描述；特殊异常的使用在下面介绍。

## 通用异常
BC4J框架中的错误是通过抛出类型为oracle.jbo.JBOException的隐式（runtime）异常。OA Framework中有自己的对应的版本为oracle.apps.fnd.framework.OAException。这个特殊化的版本提供了一种机制，可以将多个异常捆绑在一起，并使用Oracle应用消息字典（Oracle Applications Message Dictionary）翻译这些异常信息，以便显示出有用的信息。在任何代码中，通常可以抛出一个OAException类型的页面级别异常。

## 校验异常
校验异常是从实体对象和视图对象中抛出的，可以是由于属性级或行级的校验失败引起。

 - oracle.apps.fnd.framework.OAAttrValException 特殊版本的OAException，用于属性级校验失败。

 - oracle.apps.fnd.framework.OARowValException 特殊版本的OAException，用于行（row）（entity）级校验失败。

OA Framework使用下面的方式显示错误信息：

 - 属性级异常将在错误项目（item）和页面顶部标示出来

 - 行级异常将在错误行（row）和页面顶部标示出来

 - 页面级异常通常在页面顶部标示出来

## 严重异常
严重（severe）（或称为“毁灭（fatal）”）性的异常包括不希望出现的系统级的错误（比如NullPointerException）和所选的JBOException如：NoDefExcpetion。可以直接在代码中抛出严重异常。

如果严重异常发生，用户将被定向到OAErrorPage（异常被渲染在页面的中间，页面是区域渲染的，页面显示了用户友好的错误信息，并包含了一个指向堆栈跟踪细节的链接）。

**注意：** 这是一个未翻译过的信息客户可以在站点中修改。

## Oracle工作流通知

