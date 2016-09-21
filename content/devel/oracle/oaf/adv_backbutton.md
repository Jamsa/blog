Title: 高级OA Framework开发主题——支持浏览后退按钮
Date: 2008-07-04
Modified: 2008-07-04
Category: devel
Tags: oracle,ebs,oaf
Slug: adv_backbutton


# 概述
本文档提供了一组[目标](#goals)并描述了编码标准，你必须遵守以确保对浏览器后退按钮的支持。

可用性测试显示用户非常依赖于浏览器后退按钮。不幸的是，这个导航偏好在事务型的应用中将导致一系列潜在的故障点。例如，思考在OA Framework应用中在下面的场景中使用浏览器后退按钮将导致不可预料的问题。

<table class="table">
<tr>
<th>用户导航</th>
<th>问题</th>
</tr>
<tr>
<td>用户从表格中删除了一行数据页面被重绘并显示了提示信息标明数据行已经被删除（数据行不再显示在表格中）。然后用户按下浏览器后退按钮，页面将显示出数据行仍然在表格中时的页面。这时用户再次尝试删除数据行。</td>
<td>浏览器缓存了页面内容。如果用户执行的一个动作修改了数据状态，然后使用浏览器后退按钮，浏览的页面缓存没有反映出中间层的状态（在这里，是一个不存在的数据行）。当用户试图对缓存页面中被删除的行进行删除或其它处理时，将导致运行时错误。而支持浏览器后退按钮的页面将检测到这个错误并显示出用户友好的提示信息标明数据行已经被删除了。</td>
</tr>
<tr>
<td>在构物车结算处理时，用户选择了“提交定单”按钮购买端口。但不知什么原因，用户使用浏览器后退按钮从确认页面退回了定单提交页面并再次点击了“提交定单”按钮（可能她想修改定单数量）。</td>
<td>这个场景与前面描述的第一个场景类似，但未加保护的动作将导致“成功”执行两次交易。（定单可能会被创建两次，而这并不是用户期望的）。支持浏览器后退按钮的页面将可以检查到两次相同的提交并显示出用户友好的提示信息标明定单已经存在了。</td>
</tr>
<tr>
<td>用户从Page1导航到Page2，然后使用退出按钮返回Page1。然后在Page1中点击了一个表单提交组件，这将导致一个未处理的异常（NullPointerException, IndexOutOfBoundsException）。</td>
<td>OA Framework“Page 1”预期的web bean层级结构处理是处于某种状态的，和/或它预期的事务、session或BC4J对象状态值是存在的。当使用后退按钮导航时，这些状态可能丢失。如果页面不符合预期，则将显示unhandled exceptions给用户。支持浏览器后退的页面将预料到在这种场景中将丢失状态，它或者有能力重建状态并继续执行通常的功能，或显示用户友好的提示信息标题页面在使用浏览器后退按钮后不可以再被访问。</td>
</tr>
</table>

<a name="goals"></a>
## 目标
为避免出现上面类似问题的出现，使用这些目标来指导我们理解什么是“支持”浏览器后退按钮。

 1. [在处理浏览后退按钮时提供一致的行为](#goal1)
 2. [避免状态变更导致的严重的不可预知的异常](#goal2)

<a name="goal1"></a>
### 目标1：在处理浏览后退按钮时提供一致的行为
在处理浏览器后退按钮时保持一致性是很重要的。使用下面的子目标来保持一致性：

  - 允许简单的、直接的操作重复除非技术上存在限制。

    当用户执行查询或查看记录明细时使用调查流；当用户使用导航按钮并再次向前时，允许无缝的查询和查看明细，不显示错误。

   - 在逻辑事务活动时允许事务重复

    在这个上下文中的逻辑事务流指包含一个或多个页面的任务并带有决定性的结束点（事务提交）。例如对一行或多个选中数据行的单页面的update，多步的create和单个动作的删除（带commit）。。用户可以逻辑事务中使用浏览器后退按钮，并在逻辑事务执行过程上中执行操作而不出现错误。

  - 避免会引起歧义的事务、操作已经被删除的数据的事务或将导致无意识的用户操作的事务。

    为确保事务的完整性，如果可以则限制后退按钮后执行动作。例如，创建流（Create flow）在表单提交动作后点击浏览后退按钮应该不可重入。因为它不清楚用户是想要更新前面创建的记录还是创建一个新的重复记录。这种情况下应该显示错误对话框。操作于已经被删除的数据上时也需要显示明显的错误对话框。

    如果你在用户在一个页面选择一条记录后在另一个页面修改选中的数据行有特殊的更新流（Update flow）；则应选择与创建流（Create flow）类似的受限规则显示的告诉用户数据行正在被修改。或者，如果你没有记住选中数据行的机制则重复相同的更新操作。

    **Tip:** 为支持浏览器后退按钮，尽管更可取的办法是允许页面的重入，但有疑问的情况下，最好限制页面的重入，对用户来说这样也比显示unhandled exceptions或执行无意识的事务要好。

<a name="goal2"></a>
### 目标2：在状态改变时避免严重的Unexpected Exceptions
你的最小目标是应该避免严重的unexpected exception，如NullPointerExcpetion或IndexOutOfBoundException，它将显示不可读的信息给用户。应该用用户可读的文本信息对话框来取代异常信息。

参见 [Use Case-Specific General Standards]({filename}adv_back_use_cases.md#general) 了解这个目标的更多细节信息。

## 内容

## 需要阅读
本文档假定你已经阅读了下面的内容：
Anatomy of an OA Framework Page
OA Framework State Management
Implementing the Model
Implementing the View
Implementing the Controller


# 概述相关工具和行为
深入编码标准前，了解OA和BC4J frameworks提供的内置对象和工具的行为对于你编写支持浏览器后退按钮的页面是很重要的。下一节的[编码标准](#standards)提供了使用这些来处理后退按钮问题的介绍。

## 唯一的页面实例ID和页面状态缓存
OA Framework对于每个分离的页面请求——包括同一个页面的多次请求——都有一个唯一的页面实例ID（一个增长的页面计数参数被添加到form action URL和每个生成的页面链接）。。当form提交发生在用户点击浏览器后退按钮之后时，OA Framework使用页面计数器标识来检测浏览器后退按钮导航。

另外，新的方法被添加到oracle.apps.fnd.framework.webui.OAPageContext，它允许你保存和获取页面的状态：savePageState()，getPageState()和removePageState()。参见Javadoc了解其它的信息。

** 注意：** 如果异常发生在页面处理时，页面状态不会被保存并且它不会被钝化。

## 检查后退按钮导航的方法
OAPageContext.isBackNavigationFired()方法使你可以明确的检测到当前请求的浏览器后退按钮导航。这依赖于前面所讲的页面实例ID。

参见OAPageContext的Javadoc了解使用这个方法的其它信息。

## Web Bean层级结构的同步
在第2章和第3章中讲过，OA Framework在处理HTTP POST时，如果原来缓存的层级结构被丢失它将重建web bean层级结构。具体来说，它将在下面的情况下重新进入整个web bean层级结构的processRequest()。

恢复丢失的web bean层级结构：

 - POST请求激活了一个新的servlet session或一个被回收的应用模块实例（被钝化后）。

 - POST请求失败后转到了新的JVM。

   **注意：** 故障转移支持只在启用了请求级的钝化时才被支持。但是，这个功能目前还只处理测试阶段不被OA Framework所支持。

使用中间层web bean状态同步客户端UI状态：

 - POST请求是在用户使用浏览器后退按钮后的页面发起的。OA Framework通过调用OAPageContext.isBackNavigationFired()方法检查这种情况。

 - POST请求从oracle.apps.fnd.framework.webui.OADialogPage发起，请求目标为打开这个对话框的初始页面。

当form被提交时能重新创建web bean层级结构是一项重要的特性因为它确保了用户的工作可以在不被打断的并被保持一致的情况下被处理。但是，它不能强制要求代码规则确保任何支持后退按钮访问页面都可以在这种情况下被重建。。

## UI“事务单元（Transaction Unit）”
oracle.apps.fnd.framework.webui.TransactionUnitHelper类允许你描绘用户接口“事务单元”用于标识出在事务提交后不适当的导航。在这些情况下非常有用：当多个分离的UI任务（每个都有自己的提交点commit points）共享相同的根应用模块——因此是相同的数据库事务。通过事务单元标识器，你可以标明一个特定UI任务的开始和结束，并且如果用户意外导航比如浏览器后退按钮。你可以检查事务单元状态并作出反映确保不合适的动作不会执行BC4J缓存中的不需要的数据不会被提交。例如：

 1. 用户在Employee Summary页查找employees并选择 **Create Employee** 按钮。

    你可以开始一个create employee 事务单元。

 2. 用户在Create Employee页面输入一些数据然后点击 **Apply** 提交修改。

    结束create employee 事务单元。作为 **Apply** 按钮处理的一部分，Create Employee页面forward到summary Page并在那里显示一个确认信息。

 3. 用户点击浏览器后退按钮退回Create Employee页面然后再次修改数据并点击 **Apply** 按钮。

    通过检查事务单元的状态OA Framework显示一个出错对话框页面，因为在这个范例模块中修改一个新创建的数据行是不允许的。

    **注意：** 这里没有当前的create employee 事务单元，因为用户没有通过 **Create Employee** 按钮来导航，如果那样将触发创建一个新的事务单元。

下面的[Use Case-Specific Standards](#specific)提供了如何使用这个技巧的细节。

## 事务撤销（Transaction Undo）
在EBS 12版是不支持事务撤销的。

## 视图对象的主键比较（View Object Primary Key Comparison）
假定VO对象有一个主键或ROWID属性，OA Framwork将在处理processFormData()时自动检查从表单提交的数据，检查是否有“数据过期（stale data）”。如果页面数据行的主键或ROWID与VO中同一行（如果数据行的集合已经被修改或数据行已经被删除）数据的主键或ROWID不匹配，OA Framework将显示一个标准的“数据过期”的出错页面。

如果定义了主键，而不是依赖于ROWID属性，OA Framework将尝试在结果集中使用主键查找到匹配的数据行。如果找到了，则“数据过期”错误将被避免，并且用户继续工作。

**注意：** OA Framework只在VO对象当前的结果集（current view object result set）中查找匹配的数据行。如果VO对象的WHERE子句对结果集进行了限制，匹配有可能不能匹配，这也将产生“数据过期”的错误提示。

**使用笔记**

 - “数据过期”检测机制的设计目的主要是为了捕捉对已经被删除的数据行进行操作。

 - 为了优化性能，对于没有表单元素的只读表格OA Framework不会执行数据过期的检查。对于某些特殊情况需要对只读表格进行数据过期检查的，可以表格区域的最后添加一个虚拟的可更新隐藏字段（ **formValue** ）。

 - 为了获取“数据过期”错误的根本原因，可以启用开发模式（Developer Mode）或诊断模式（Diagnostic Mode）。当这两种模式启用时，面向开发者的附加内容将显示在对话框页面的消息中，帮助诊断代码错误。参见[测试OA Framework应用]({filename}test_test.md)以了解启用这些模式的信息。

 - “数据过期”错误的意外出现也有可能是与VO对象的初始值有关。参见下面的[避免无条件的VO对象/事务状态初始值](#uncond)以了解更多信息。

 - **已知问题：** 当前的VO对象主键比较逻辑趋向于过度保护；某些情况下，“数据过期”错误可能会出现在不需要的地方。例如，在通过浏览器后退按钮回退后以新的查询条件执行查询将导致“数据过期”的错误。为了在只读表格中避免这个问题，你可以在oracle.apps.fnd.framework.webui.beans.table.OATableBean或oracle.apps.fnd.framework.webui.beans.table.OAAdvancedTableBean上使用setSkipProcessFormData(pageContext,true)API。

## 在锁定过程中BC4J过期数据检查（BC4J Stale Data Check During Locking）
当BC4J试图在数据库提交操作之前锁定行时将使用默认的OA Framework锁方案，如果当前用户查询过的行已经被另一个用户删除或修改它将自动尝试并决定：

 - 如果行被删除了，BC4J将抛出oracle.jbo.RowAlreadyDeletedException。

 - 如果行已经被修改，BC4J将抛出oracle.jbo.RowInconsistentException。

在这两种情况下，OA Framework将自动将这些低级的异常转化为用户友好的错误信息。

这个检查在用户使用后退按钮并再次保存对过期数据的修改时也有好处。

关于BC4J锁的更多信息，参见第五章[实现Java实体对象]({filename}bus_java.md)。

## 标准错误对话框（Standard Error Dialogs）
OA Framework包含了一些标准错误对话框。

 - NAVIGATION_ERROR - 这个错误信息通知用户不能在点击浏览器后退按钮后继续。并指示用户回到全局主页（global Home page）恢复导航并重新启动事务。

 - FAILOVER_STATE_LOSS_ERROR - 这个错误信息通知用户在用户session或系统失效后不能继续。并指示用户回到全局主页恢复导航并重新启动事务。

 - STATE_LOSS_ERROR - 两个特殊错误信息的组合。指示用户在使用后退按钮、用户session过期或系统失效后不能继续。并指示用户回到全局主页恢复导航并重新启动事务。

```java
public void processRequest(OAPageContext pageContext, OAWebBean webBean)
{
  ...

  // Display a standard error message related to state loss due to Back button
  // navigation or failover as appropriate.
  if (pageContext.isBackNavigationFired(true))
  {
    pageContext.redirectToDialogPage(new OADialogPage(NAVIGATION_ERROR));
  }
  else
  {
    pageContext.redirectToDialogPage(new OADialogPage(FAILOVER_STATE_LOSS_ERROR));
  }
}
```
你也可以直接使用pageContext.redirectToDialogPage(new OADialogPage(STATE_LOSS_ERROR))。但是，我们强烈建议你创建怀具体环境相关的消息提高对客户的实用性。

## AM State Required 标识（AM State Required Flag）（Deprecated）
应用模块的AM State Required标识在新的开发中不再被推荐使用。如果你有页面使用了这个功能，并且它的表现与下面章节中的编码标准是一致的，则不需要修改你的实现。

# 编码标准（Coding Standards）
尽管在编码标准一章中所有的OA Framework编码标准都已经列出，但这一节提供了将每个标准应用到你的代码中的更多细节信息。

**注意：** 这些主题也链接到了第八章的摘要列表。

编码标准被分为两个大的分类：

 - [一般标准](#general)应用于所有的使用情况。

 - [特殊情况标准](#specific)描述了在特殊应用场景中如何处理后退按钮，如何在一个只读摘要页面中处理删除动作，或如何处理关联到一个可更新页面的多步创建动作。

<a name="general"></a>
## 一般标准

### 1. 定义VO对象的主键 (模型编码标准[M39]({filename}cs_mdlgeneral.md#M39))

为了使得上面所述的VO对象的主键可以进行比较，所有VO必须一个主键或以ROWID来代替。主键适合。

**例外：** 如果是一个不包含逻辑主键的简单只读VO对象，则不需要创建主键。比如，一个单列VO对象查询的是某列的合计值而并不包含逻辑主键。

如果你需要了解如何定义VO对象的主键，参见[实现模型]({filename}build_model.md)。如果没有主键则应该使用ROWID，只需要在VO对象的SQL中选择ROWID伪列对应的属性名称为 **Rowid** 或 **RowId** 。

### 2. 不要假设VO对象的状态（模型编码标准[M38]({filename}cs_mdlgeneral.md#M38)，[M37]({filename}cs_mdlgeneral.md#M37)）

对于VO对象的状态永远不要臆测：

 - 不要总是认为VO对象一定有数据行。对从VO对象中获取的数据行进行null检查。

 - 对于查询页面中使用动态WHERE子句的VO对象，在执行查询前总是清除先前在的WHERE子句参数。这确保了之前的设置不会影响当前的查询。

 - 对于动态创建的VO对象，在创建之前总是使用find进行检查。

下面的代码描述了这些规则：
```java
// Bad Code
Row[] rows = vo.getAllRowsInRange();
rows[0].getAttribute(...);   <-- assumes the rows exist
// Good Code
Row[] rows = vo.getAllRowsInRange();
if (rows == null)   <-- allows for the possibility that rows cannot be found
{
  // Take proper action.
}
rows[0].getAttribute(...);
```

在使动态设置WHERE子句（不管它是否为null）之前，总是先清空参数：
```java
// Bad Code

vo.setWhereClause("empno < 10");
vo.executeQuery();
...
vo.setWhereClause("empno = :1");
vo.setWhereClauseParam(0, <some value>);
vo.executeQuery();
...
vo.setWhereClause(null);
vo.executeQuery();
// Good Code
vo.setWhereClause("empno < 10");
vo.setWhereClauseParams(null);
vo.executeQuery();
...
vo.setWhereClause("empno = :1");
vo.setWhereClauseParams(null);
vo.setWhereClauseParam(0, <some value>);
vo.executeQuery();
...
vo.setWhereClause(null);
vo.setWhereClauseParams(null);
vo.executeQuery();
```

如果需要动态创建VO对象或VO对象的属性，在创建之前先检查同名的对象是否已经存在：
```java
// Bad Code
ViewObject vo = am.createViewObject("MyVO", ...);
vo.addDynamicAttribute("MyAttr");

// Good Code
// First check whether the VO with the same name exists or not.

ViewObject vo = am.findViewObject("MyVO");

if (vo == null)
{
  vo = am.createViewObject("MyVO", ...);
}

// Check whether the attribute with the same name exists or not.
// Note that for attributes, we need to use try-catch clause.

if (vo.lookupAttributeDef("MyAttr") == null)
{
  vo.addDynamicAttribute("MyAttr");
}
```

### 3. 在processRequest之外修改Web Bean属性（控制器编码标准[C16]({filename}cs_ctrlgeneral.md#C6)，[C15]({filename}cs_ctrlgeneral.md#C15)）
不要在processFormData()或processFormRequest()中添加修改web bean的逻辑。如果你需要在处理form提交请求过程中修改web bean层级结构或修改web bean属性，你可以：

 - 参见第四章[动态用户界面]({filename}feat_ppr.md)将属性绑定到SPEL上和使用页面区域渲染。

 - 使用OAPageContext.setForward*()方法退回页面，并半retainAM参数设置为true，然后在processRequest()中执行你的bean处理逻辑。

如果OA Framework由于上面描述过的原因需要重建web bean层级结构，所有相关逻辑必须包含在processRequest()方法中。而且，任何使得要修改web bean层级结构（包含web bean属性）的信息，必须被添加为 **URL参数（URL parameter）**。换言之，如果你需要以某种方式在页面跳转（forward）时以编程方式修改web bean属性或层级结构，则这些在你检查用用以决定是否修改web bean的信息必须在调用forward（OAPageContext.setForward*()）时通过“参数（parameter）”(com.sun.java.util.collections.HashMap)指定。例如：
```java
import com.sun.java.util.collections.HashMap;
...

// As a result of a button press, return to the current page setting
// a URL parameter value to be used to modify the page layout.

public void processFormRequest(OAPageContext pageContext, OAWebBean webBean)
{
  super.processFormRequest(pageContext, webBean);

  if (pageContext.getParameter("someButton") != null)
  {
    HashMap params = new HashMap(1);
    params.put("showRegion", "RegionA");
    pageContext.setForwardURLToCurrentPage(params, // added to the request as URL parameters
                                           true, // retain the AM
                                           OAWebBeanConstants.ADD_BREAD_CRUMB_NO,
                                           OAWebBeanConstants.IGNORE_MESSAGES);

  }
}


public void processRequest(OAPageContext pageContext, OAWebBean webBean){
  super.processRequest(pageContext, webBean);

  if ("RegionA".equals(pageContext.getParameter("showRegion")))
  {
    // Change your layout accordingly...
  }
}
```

**注意：** 使用OAPageContext.putParameter()或隐藏域在这种情况下不行，因为这些值不会被作为URL参数添加到请求。

下面的例子描述了一个主键值如何被传递到setForward*()方法的HashMap参数中并被用于重建合适的web bean层级结构：

 - Page A包含了一个动态部分，它根据用户从列表中的选择显示不同的区域。Page A默认显示 **Region1** 。

 - 用户在列表中选中了一个用于决定显示区域值。然后你跳转回页面，并将个值通过OAPageContext.setForwardURLToCurrentPaqge()方法设置到了“参数”HashMap中。这保证了这个值被作为URL参数添加到了请求。

 - 用户修改了她的主意从列表中选择了不同的项，这样你的代码将forward到页面并显示 **Region3** 。

 - 用户选择浏览器后退按钮退回Page A将显示Page 2。

   **注意：** 浏览器的HTML缓存，显示的是 **Region2** ，不再与中间层的web bean层级结构匹配，中间层包含的是 **Region3** 。

 - 用户在显示于 **Region2** 的字段中输入一些值然后点击 **Submit** 按钮。

   OA Framework检测到浏览器后退按钮，在响应时，重建web bean层级结构并包含了 **Region2** 和用户添加到请求的数据。这确保了中间层与浏览器缓存正确同步了动作处理没有出现错误。

### 4. 避免无条件VO/事务状态初始值（控制器编码标准[C32]({filename}cs_ctrlgeneral.md#C32)）

在上面的[Web Bean层级结构同步](#hier_synch)一节中描述过processRequest()方法可能重复的进入，避免无条件的VO对象和事务状态初始值。

初始操作包括下面的情况：

 - 在VO对象上调用executeQuery()从数据库中查询数据。

 - 在VO对象的insertRow(row)方法之后调用setMaxFetchSize(0)手工插入数据行，而不是从数据库查询。

 - 调用OAPageContext.putTransactionValue()，OAPageContext.putTransactionTransientValue()，OAViewObjectImpl.putValue()，OAApplicationModuleImpl.putValue()或OAPageContext.putSessionValue()来创建事务或session状态。

应该避免无条件初始化是因为下面两个原因：

 - 当processRequest()方法重入时，无条件初始将导致事务状态丢失。例如，用户对于transient VO属性的修改将丢失，VO对象的当前行数据行将重置。

 - 多余的执行查询和状态初始化性能上是不可取的（[performant](http://boulter.com/blog/2004/08/19/performant-is-not-a-word/)）。

参见[VO对象细节：初始化规则]({filename}bus_vo.md#init)了解如何对VO对象执行适当的初始化。

#### 事务状态

如果你使用OAPageContext.putTransactionValue()等方法管理事务状态，则总应该检查它是否已经存在。例如：
```java
if (pageContext.getTransactionValue("poTrxStep") == null){
    pageContext.putTransactioinValue("poTrxStep", "1");
}
```
**注意：** 如果事务值（transaction value）可以改变过程并且你只需要初始化这个值一次，则这个检查是很重要的。

### 5. 恰当的配置对话框页面（控制器编码标准[C30]({filename}cs_ctrlgeneral.md#C30)）
如果在导航到对话框页面时，需要根据用户对对话框页面问题的响应来交换数据，可以配置按钮来提交它的表单到调用页面。参见[对话框页面]({filename}ebs_feat_dialog.md)了解操作细节。OA Framework将在调用processFormData()和processFormRequest()之前重新进入processRequest()，以确保你的页面能预期到[无条件VO对象/事务初始化](#uncond)。

**注意：**

 - 通常，你不需要关心对话框页面的后退按钮的支持。在极少数情况下对话框页面提交表单到它自身而不是提交到调用它的页面，你必须确保对话框页面可以像其它页面一样被重建。换方言之，任何写在processRequest()和processFormRequest()中对话框控制器代码必须预料和处理可能的状态丢失。

 - 不要使用OADialogPage中的deprecated的方法setReleaseAllRootApplicationModules和setReleaseRootApplicationModule。如果使用了这些方法，则用户导航到OA Framework页面如Preference页，并用 **Cancel** 按钮返回对话框页面时对话框页面的状态时将失效。参见Javadoc以了解这些方法的更多信息。

### 6. 正确的通过页面与状态通讯（控制器编码标准[C20]({filename}cs_ctrlgeneral.md#C20)，[C17]({filename}cs_ctrlgeneral.md#C17)）
在考虑在特定情况下使用哪种通讯方法之前，先了解一下有哪些可用的选项。

 方法 | 描述
:---- | :---- 
URL 参数 | 你可以直接添加参数及其值到URL。
隐藏域OAFormValueBean | HTML页面隐藏域的值在form提交时将添加到请求中。
FormParameter OAFormParameterBean | HTML页面隐藏域的值在form提交时将添加到请求，与OAFormValueBean不同，这个值在每次form提交时会被清空（在fireAction或firePartialAction事件方法给它设置新值之前）。 **注意：** 这个组件的使用是保留的，是专门用于配置fireAction和firePartialAction事件的。参见第四章的[Declarative Form Submit]({filename}feat_submitform.md)和[动态用户界面]({filename}ebs_feat_ppr.md)以了解更多细节。不要直接在你的页面中添加FormParameter beans。
OAPageContext.putParameter() | 将参数值添加到特殊的页面缓存中，这个值在单个请求是持久化的。 **注意：** 如果，用户导航到个性化或首选项页面然后返回你的页面。如果你只依赖于putParameter()设置的值，则它将不能正确重建页面。这是因为导航流承担了多次请求。
Transaction Value OAPageContext.putTransactionValue() | 将值添加应用模块的事务中，它在应用模块被保留时将一直存在。
Application Module Value OAApplicationModuleImpl.putValue() | 将值添加到应用模块中，它在应用模块被保留时将一直存在。
View Object Value OAViewObjectImpl.putValue() | 将值添加VO对象，它将在应用模块被保留时一直存在。
Transient Transaction Value OAPageContext.putTransactionTransientValue() | 事务值存在于当前应用模块中，但仅限于当前JVM。 **注意：** 这些不会被钝化，因此如果当前的应用模块被钝化并因为其它原因被激活，这些值将会丢失。
Application Module Transient Value OAApplicationModuleImpl.putTransientValue() | 应用模块值存在于当前JVM中。 **注意：** 这些不会被钝化，因此如果当前的应用模块被钝化并因为其它原因被激活，这些值将会丢失。
ViewObjectTransientValue OAViewObjectImpl.putTransientValue() | VO对象值存在于当前JVM。 **注意：** 这些不会被钝化，因此如果当前的VO对象被钝化并因为其它原因被激活，这些值将会丢失。
Session Value OAPageContext.putSessionValue() | 添加到servlet session中的值生存于整个session周期。
TransientSessionValue OAPageContext.putTransientSessionValue() | Session值存在于当前JVM的session中。 **注意：** 这些值不会被钝化，因此如果当前的session的状态被钝化并因为其它原因被激活，这些值将会丢失。



浏览器cookie不包含在可用的通讯列表技术中。不要使用浏览器cookie来存储应用中的信息。浏览器可以拒绝cookie值，并且对于cookie的数量也有限制。浏览器cookie通常只在OA Framework内部使用。

**注意：** 这不适合于用自动强制页面刷新来解决后退问题。如果你因为其它原因需要使用页面刷新，请联系OA Framework团队。

#### 用法推荐
这节描述了正确的方法在可预期的游览后退按钮操作时与页面相关状态进行通讯。这些推荐方法包括启用“Return to”链接在不同的模块间导航并确保个性化和首选项模块能与你的页面无缝集成。例如，当用户在个性模块时选择“Cancel”按钮，你的页面应该能够正确的重建。

参见[OA Framework状态管理]({filename}ess_state.md)了解更多相关的技术细节。

<a name="intra-app-long"></a>
应用内导航

与用于构建目标页面的简单的状态值通讯时，使用URL参数（URL Parameters）。

 - 如果是在form提交的环境下与状态通讯，使用OAPageContext.setForward*()方法的“paramters”HashMap。如果可能，应该避免使用OAPageContext.putParameter()。

 - 如果是在GET请求中与状态通讯，直接添加组件的Destination URI的静态绑定值将变成URL参数。在选择菜单项时你也可以将URL参数添加到请求中。参见[Tabs/Navigation]({filename}feat_tabs.md)。

**技巧：** 通过浏览地址栏设置的值将显示给用户。用户通过查看页面源码也可以看到隐藏域值。在这两种情况下，敏感的数据值必须被如[实现视图：URL参数]({filename}build_view.md#urlparams)中描述的进行加密。

为了根据更复杂或长时间存在的状态值来构建目标页面，可以使用下面的与应用模块相关的缓存：

 - 在事务中缓存值，如果你不需要钝化支持可以使用OAPageContext.putTransactionValue()或OAPageContext.putTransactionTransientValue()。

 - 在应用模块中缓存值，如果不需要钝化支持可以调用oracle.apps.fnd.framework.server.OAApplicationModuleImpl.putValue()或OAApplicationModuleImple.putTransientValue()。

 - 在VO对象中缓存值，如果不需要钝化支持oracle.apps.fnd.framework.server.OAViewObjectImpl.putValue()或OAViewObjectImpl.putTransientValue()。

当使用这些缓存策略时，要记得在代码中处理潜在的状态丢失。换言之，在使用值之前总是需要检查所需要的值是否存在，如果它为null或为空，你可以选择重建并重新缓存这个值，如果不行则需要显示一个用户友好的状态丢失的对话框消息。

**例外：** 如果页面已经使用了如[Use Case-Specific Coding Standards](#specific)中的UI事务单元来保护，则你不需要检查这些值是否已经存在。

另外，为了使这个缓存策略能正确的工作，必须遵循下面的规则：

 - 不要为了省事而在只读页面中使用OAApplicationModule，总是使用自己的应用模块类。

 - 避免在页面被渲染前调用OAPageContext.releaseRootApplicationModule()来释放应用模块；这将导致过早的丢失页面状态。可以通过配置保留级别（retention levels）为 **CONNECTION_AGNOSTIC** 或 **MANAGE_STATE** 将你的根应用模块申明为无状态连接。参见[OA Framework State Persistence Model (Passivation)]({filename}adv_passive.md#ret_level)以了解更多信息。

应用间导航

应用内页面流上面已经讨论过了，在交叉页面流中导航最简单的方法是使用URL参数（URL parameters）。

当原页面和目标页面使用了不同的应用模块时如果需要使用复杂的或长时间存在的值来构建目标页面时，你不能依赖于上面描述过的应用内导航。而应该在原始页面调用OAPageContext.putParameter()或OAPageContext.putSessionValue()/OAPageContext.putTransientSessionValue()来传递值到目标模块，然后在它的应用模块中获取和缓存这些值。目标页面必须：

 1. 复制（“迁移（transition）”）参数/session值到根UI应用模块。换言之，获取参数或session值然后将它们存储于如[应用内导航](#intra-app-long)中描述的事务、应用模块或VO对象中。

 2. 如果输入值被缓存于session中，则在复制它们后应该将它从session中删除。

 3. 从应用模块缓存中读取值，总是要考虑应用模块的状态可能会丢失。

下面的例子描绘了目标页面控制器的processRequest()方法使用了一个私有的方法“迁移”传递的值到应用模块缓存中。（这里假定在原页面使用了OAPageContext.putParameter()方法）。

```java
public void processRequest(OAPageContext pageContext, OAWebBean webBean)
{
  // Always call this first.
  super.processRequest(pageContext, webBean);

  // Call this before trying to retrieve the value from the transaction.
  transitionPageState(pageContext);

  Object val = pageContext.getTransactionValue("<required page state 1>");

  // Handle the loss of page state values when the application module is
  // released. If one of the required page state values does not exist
  // redirect to a context-specific state loss error page.
  if (val == null)
  {
    // Note that you are strongly recommended to use context-specific message
    // instead of the following generic messages.
    if (pageContext.isBackNavigationFired(true))
    {
      pageContext.redirectToDialogPage(new OADialogPage(NAVIGATION_ERROR));
    }
    else
    {
      pageContext.redirectToDialogPage(new OADialogPage(FAILOVER_STATE_LOSS_ERROR));
    }
  }

  // Otherwise, use the page state and continue processing the request.
  ...

} // end processRequest()


private void transitionPageState(OAPageContext pageContext)
{
  // First inspect one of the required page state values.
  // Use getParameterObject() instead of getParameter() for
  // non-String object types.
  Object val = pageContext.getParameterObject("<required page state 1>");

  if (val != null)
  {
    // Transition the required value.
    pageContext.putTransactionValue("<required page state 1>", (Number)val);

    // If you used session values instead of OAPageContext.putParameter to transport
    // the values, then remove the values from session after each transition.

    // Transition other values.
    val = pageContext.getParameterObject("<required page state 2>");
    pageContext.putTransactionValue("<required page state 2>", (Number)val);

    // For optional values, if the value is not present, explicitly remove values
    // from the transaction.
    val = pageContext.getParameterObject("<optional page state 1>");

    if (val != null)
    {
      pageContext.putTransactionValue("<optional page state 1>", (Date)val);
    }
    else
    {
      pageContext.removeTransactionValue("<optional page state 1>");
    }
    ...
  }
} // end transitionPageState()
```

**技巧：** 你至少需要一个页面状态值来决定是否需要执行迁移操作。如果只需要一个被所有UI区域共享的session值，并且你决定在每个区域的控制器中都使用transitionPageState()方法，则你可以在最顶层的区域的控制器（page layout region's controller）中对session值执行迁移操作并立即调用OAPageContext.putParameter()传递个额外的标识来向当前请求中的子区域表示需要的值已经存在了。子区域可以直接检查这个额外的标识（译注：而不需要再去重复执行迁移操作）。

#### 隐藏域

隐藏域可以用于保存不应该显示于页面的应用数据，比如主键。它们不应该用于作为构建目标页面的条件而传递。这是因为当你的页面是通过另一个页面的 **返回（Return to）** 导航链接来访问时，例如个性化页面时，以前的请求值是放到OAPageContext.putParameter()中的，返回导航是一个新的请求原来的参数已经不再存在了。页面状态也已经丢失，并且存储于隐藏域中的值也已经不能在下面的请求被保存。因此，应该使用上面描述的方法来代替使用隐藏域的方法。

### 有条件的禁止表单提交动作

在某些情况下，在使用浏览后退按钮后用户不应该也不能提交表单。参见下面的[Use Case-Specific General Standards]({filename}adv_back_use_cases.md#general)指导方针对特殊情况进行处理。

## 使用特殊情况标准

除了上面的一般性规则，检查下面的列表看是否有相符合的特殊情况，如果有则应该遵循下面的规则。

 - 只读页面[只读页面单步创建]({filename}adv_back_use_cases.md#read_only_create)

 - 只读页面[只读页面多步创建]({filename}adv_back_use_cases.md#read_only_multistep_create)

 - 只读页面[只读页面删除]({filename}adv_back_use_cases.md#read_only_delet)

 - 只读页面[只读单页面修改（允许迭代修改）]({filename}adv_back_use_cases.md#read_only_update)

 - 只读页面[只读单页面修改（允许单次修改）]({filename}adv_back_use_cases.md#read_only_single_update)

 - 只读页面[只读页面多步修改]({filename}adv_back_use_cases.md#read_only_multistep_update)

 - 只读页面[可修改的摘要页面（Summary）单步或多步创建或修改]({filename}adv_back_use_cases.md#txn_all)

 - 只读页面[可修改的摘要页面（Summary）多步创建或修改和子事务]({filename}adv_back_use_cases.md#txn_sub)

 - 只读页面[摘要（Summary）和事务页面应用间（Inter-Application（Cross-Product））页面流]({filename}adv_back_use_cases.md#txn_crossprod)

 - 只读页面[可修改摘要页面（Summary）或表格中的动作（复制和移除）]({filename}adv_back_use_cases.md#txn_inline)

 - 只读页面[PPR页面刷新]({filename}adv_back_use_cases.md#ppr)

## 测试浏览器后退按钮

测试应用对浏览后退按钮的支持：

 1. 手工按[Use Case-Specific Standards]({filename}adv_back_use_cases.mdl)列表中的导航路径进行测试。除了通过后退按钮导航，也要尝试：

    在事务处理页面有意地输入无效的数据并执行表单提交动作以产生一个校验错误。并使用后退按钮退回摘要页面（Summary）。无效的对象不应该引起其它错误，在正确的重新输入数据后事务页面应该可以开始一个新的事务。

 2. 在每个页面，都选择全局的“首页”链接然后使用浏览后退按钮返回你的页面。再点击页面中的按钮或表单提交的链接。这可以检查你的页面在状态丢失时健壮性。你的页面应该能够正确的重建或显示一个客户化的用户友好的状态丢失错误对话框。

 3. 在每个页面中，选择“个性化”链接并使用个性化页面的返回链接返回你的页面。在首选项页面执行同样的操作并通过取消按钮返回你的页面。这些页面流将保存你的应用模块状态。因此，你的页面应该能够正确的重建。
