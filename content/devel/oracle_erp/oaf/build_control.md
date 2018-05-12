Title: OA Framework应用构建之——实现控制器
Date: 2008-08-06
Modified: 2008-08-06
Category: 开发
Tags: oracle,ebs,oaf
Slug: build_control

# 设计一个OA Controller
如[OA Framework Page解析]({filename}page.md)中所描述的，OA Controller定义了web beans的行为。具体来说，编写控制器代码的目的是：

 - 在运行时处理／初始化UI（包含那些通过编程方式添加的layout）

 - 拦截或响应按钮按下之类的用户事件

控制器不应该包含任何业务逻辑；这应该属于模型类。

## 必备知识
通常来说，在提出如何设计控制器之前，应该思考一下是否需要创建控制器。

作为一条规则，应该只在绝对必要的情况下才编写控制器。如果可以通过设计的方式创建页面，就不要通过编程的方式实现region和item。编程方式创建的web beans不能被个性化，重用或继承。而且，一些硬编码的layouts可能会丢失BLAF UI样式。

在[实现视图]({filename}build_view.md)中说过，所有位于共同组件中的顶级regions必须与一个控制器关联。

## 粒度
OA Controllers可以与任何region关联（任何实现oracle.apps.fnd.framework.webui.beans.OAWebBeanContainer接口的web beans）；不能将控制器与items关联。

许多OA Framework新手都想知道控制器应该是”多大“。应该一个页面一个，或一个功能region一个（比如“Search” region），或一个复合web bean（比如一个table）一个，或者？答案是要看情况。

最初，在一个非常简单的页面，你可能不需要任何控制器（如果没有工作要作就不需要创建控制器）。如果需要编写代码，你需要根据下面的条件决定创建什么样的控制器：

 - 利于封装，一个web bean实现了它自己的行为

 - 组件重用，如果组件被设置为重用，它必须是自包含，自已自足。

 - 代码实用性，尽管页面包含了8个regions时可以很容易的添加8个控制器（每个包含少量的代码），这种“纯”OO的观念可以导致代码维护困难，可能导致产品代码文件膨胀。

有一些方法可以帮助决定如何处理：

 - 永远不要从child bean中设置parent/grandparent web bean的属性。

 - 为相关联的region定义控制器来设置region和它的子孙region的属性。如果需要主控制器管理多个子／孙web bean，控制器应该与适当的父／祖父bean相关联。

 - 对于复杂的beans（比如OATableBean）应该将控制器关联到bean自身，或关联到一个简单的容器bean中（如果它实现功能逻辑单元）。

通常，应该为页面创建少于满足上面规则和考虑数量的控制器。对于非常简单的页面，通常是为pageLayout区域关联单个的控制器。对于更复杂的页面，应该为各个功能组件（比如，查询页面中典型的“Search”区域控制器和“Results”区域控制器）创建少量不同的控制器。共享区域应该拥有自己的适当的控制器。

## 模型性／重用
在同一组相关联的页面中，你有时将找到可以重用代码的机会。下面是创建模块性更强的控制器代码的方法：

 - 在控制器中添加私自己的私有方法。

 - 创建一个公用的控制器类（它是oracle.apps.fnd.framework.webui.OAControllerImpl），然后为有需要的页面／区域继承这个类。

 - 创建辅助的实用工具类，控制器中可以根据需要代理。这些类不需要实现任何OA Framework类或接口，应该被包含在与它们所辅助的控制器类所在的包中。注意，静态方法适合于在这些类中使用，当使用静态方法时，应该考虑下面的问题：

  - 不能影响子类中的静态方法。

  - 封装相关常量和静态方法。（There are packaging implications related to the use of constants and static methods ）

## 线程安全
OA Framework被设计为支持多线程web bean访问（尽管还没有实现）。大部分对于你的代码来说是透明的，只有少量规则必须在控制器代码中遵守：

 - 如果在控制器或辅助类中使用静态方法，则永远不要包含状态。

 - 总是将页面的OAPageContext传递给任何web bean存储器（如果需要可以带OAPageContext）。比如，使用setText(OAPageContext pageContext, String text)代替setText(String text)。

## 状态管理
不要在控制器中或你实例化的辅助类中添加非易失性成员变量。OA Framework不会钝化成员变量，因此一旦虚拟机失效被支持后将不能恢复这些值。可以添加static final成员变量。

## 编码规则

# 创建一个控制器
为一个区域创建控制器：

 1. 在JDeveloper Structure页面中选择区域

 2. 右键选择Set New Controller...

 3. 在New Controller对话框中，输入包和类名。选择OK创建与选择区域关联的控制器。注意Inspector中的Controller Class属性值是类的全名，如：oracle.apps.fnd.framework.toolbox.tutorial.webui.HomeSearchCO。

JDeveloper将创建控制器模板。
```java
/*===========================================================================+
 | Copyright (c) 2001, 2003 Oracle Corporation, Redwood Shores, CA, USA      |
 | All rights reserved.                                                      |
 +===========================================================================+
 | HISTORY                                                                   |
 +===========================================================================*/
package oracle.apps.fnd.framework.toolbox.tutorial.webui;

import oracle.apps.fnd.common.VersionInfo;
import oracle.apps.fnd.framework.webui.OAControllerImpl;
import oracle.apps.fnd.framework.webui.OAPageContext;
import oracle.apps.fnd.framework.webui.beans.OAWebBean;

/**
  * Controller for ...
  */
public class OrderSummaryCO extends OAControllerImpl
{
   public static final String RCS_ID="$Header$";
   public static final boolean RCS_ID_RECORDED =
   VersionInfo.recordClassVersion(RCS_ID, "%packagename%");

 /**
   * Layout and page setup logic for a region.
   * @param pageContext the current OA page context
   * @param webBean the web bean corresponding to the region
   */
   public void processRequest(OAPageContext pageContext, OAWebBean webBean)
   {
     super.processRequest(pageContext, webBean);
   }

 /**
   * Procedure to handle form submissions for form elements in
   * a region.
   * @param pageContext the current OA page context
   * @param webBean the web bean corresponding to the region
   */
   public void processFormRequest(OAPageContext pageContext, OAWebBean webBean)
   {
     super.processFormRequest(pageContext, webBean);
   }

}
```

**注意：** 缺省的模板内容不包含processFormData(OAPageContext pageContext, OAWebBean webBean)方法，这个方法在POST处理的第一个阶段被调用。如果需要（非常少见），可以将它加到控制器中。

**注意：** 也可以通过编程的方式将控制器与区域关联。查看OAWebBeanContainer中的setControllerClass(String javaClass)方法。

# 处理HTTP GET
在GET处理过程中，每个控制器的processRequest(OAPageContext pageContext, OAWebBean webBean)方法被按照它们被实例化时的层级结构而依次被调用。处理从pageLayout bean开始，然后递归处理整个层级结构。初始化页面——或影响层级结构中的web bean（通过设置属性，创建web bean等等）——属于processRequest()方法。

**注意：** 传递到processRequest()方法中的oracle.apps.fnd.framework.webui.OAWebBean参数是与当前控制器关联的区域。

下面是一个典型的processRequet的代码。它描绘的是根据从“search”页面传递过来的参数，初始化用于查看的“detail”页面。
```java
/**
 * Layout and page setup logic for region.
 * @param pageContext the current OA page context
 * @param webBean the web bean corresponding to the region
 */
public void processRequest(OAPageContext pageContext, OAWebBean webBean)
{
   // Always call this before adding your own code.
   super.processRequest(pageContext, webBean);

   // Get the purchase order number from the request.
   String orderNumber = pageContext.getParameter("headerId");

   // We need to set the page header text to include the PO order number for reference.
   MessageToken[] tokens = { new MessageToken("PO_NUMBER", orderNumber) };

   // Always use a translated value from Message Dictionary when setting strings in
   // your controllers.
   String pageHeaderText = pageContext.getMessage("ICX", "FWK_TBX_T_PO_HEADER_TEXT", tokens);

   // Set the po-specific page title (which also appears in the breadcrumbs. Since this
   // controller is associated with the page layout region, simply cast the webBean
   // parameter to the right type and set the title.

   ((OAPageLayoutBean)webBean).setTitle(pageHeaderText);

   // Now we want to initialize the query for our single purchase order with all of its
   // details.
   OAApplicationModule am = pageContext.getApplicationModule(webBean);
   Serializable[] parameters = { orderNumber };
   am.invokeMethod("initDetails", parameters);

} // end processRequest()
```
在调用super.processRequest(pageContxt, webBean)后，范例中的代码从request参数中获取名为“headerId（从Search页面传递过来的参数）”。这个值被显示在页面标题和breadcrumbs上，并且它被传递给模型以便查询。

使用页面的title值定义页面标题和breadcrumbs：

![page_title]({attach}oaf_build_control/page_title.gif)


由于显示于页面中的值必须被翻译，我们在Oracle应用消息字典（Oracle Application Message Dictionary）中创建了一个名为FWK_TBX_T_PO_HEADER_TEXT的消息，消息内容为“Purchase Order: &PO_NUMBER”。这个代码定义了以令牌PO_NUMBER作为Purchase Order Number的占位符，然后从oracle.apps.fnd.framework.webui.OAPageContext（它将操作委派给AOL/J）中提取翻译后的版本。然后将翻译后的字符串作为页面标题。

**警告：** 不要在用户界面中使用硬编码的文本值。所有以编程方式显示的文本值必须来源于消息字典（Message Dictionary）。也可以在设计时在web bean中使用这种方式（所有显示的bean属性都是被翻译的），或者也可以从多国语言表中查询出值来显示。

最后，这个只读的”details“页面自动按给定的编号进行查询而不管它是否会被渲染。它通过将编号传递给页面根应用模块的initDetails()方法。然后应用模块将参数传递给适当的视图对象，在那里将参数与WHERE子句绑定并执行查询。

## 修改Bean属性
**注意：** 作为规则来说，更好的修改web bean属性的方法是使用局部页面渲染（partial page rendering （PPR））和SPEL，在Dynamic User Interface中有描述。在不能通过PPR和SPEL的环境下，也必须在processRequest()方法中修改web bean层级结构（这节被包含在GET处理一章中，也是由于只能在processRequest()方法中才允许修改web bean层级结构）。

如果需要以编程方式在响应表单提交的事件中修改层级结构，必须forward到同一个页面的processRequest()方法（见下面POST事件处理）。作出这个限制的原因有：

 - 确保web bean层级结构能在需要的时候被正确的重建。

 - Beans被适当的初始化。主要是Rendered属性，或影响复杂组件渲染的prepareForRendering()方法。

 - Bean层级结构被放在同一个方法中维护。

修改web bean的属性时，只需要简单的根据它的名称（在JDeveloper中赋给它的ID）查找到正确的bean，然后按下面的方法调用适当的方法。

**警告：** 当获得web bean时，在调用它的任何方法前都需要检查对象是否为空。即使你认为bean被包含于web bean层级结构中，但也有可能在用户使用个性化定制时半它隐藏了。
```java
processRequest(OAPageContext pageContext, OAWebBean webBean)
{
  // Always call this before adding your own code.
  super.processRequest(pageContext, webBean);

  OATableBean table = (OATableBean)webBean.findIndexedChildRecursive("OrdersTable");

  if (table == null)
  {
     MessageToken[] tokens = { new MessageToken("OBJECT_NAME", "OrdersTable")};
     throw new OAException("ICX", "FWK_TBX_OBJECT_NOT_FOUND", tokens);
  }

  // Set the purchase-order specific "control bar" select text:
  // "Select Purchase Order(s) and..."

  String selectPOText = pageContext.getMessage("ICX", "FWK_TBX_T_SELECT_PO", null);
  table.setTableSelectionText(selectPOText);

}
```
使用findIndexedChildRecursive(String name)方法可以在整个web bean层级结构中查找到第一个与名称匹配的被索引的子对象。如果如果要修改的web bean是一个被命名的UIX子对象（或，如果你不确定它是否“被命名（named）“或”被索引（indexed）“），则使用findChildRecursive(String name)方法。

如果需要修改控制器区域的属性，只需要将processRequest()的OAWebBean参数转换为正确的类型并调用需要的方法。

## 编程的方式创建Bean
**注意：** 本节包含于GET处理部分，因为只允许在processRequest()方法中修改web bean层级结构。

如果需要在响应表单提交事件中添加web bean到层级结构中，必须forward到同一个页面的processRequest()代码中执行。

作为规则，如果你可以通过设计的方式产生web bean就不应该通过编程的方式产生web beans。另外，如果你的页面与局部页面渲染相关，则也不能在运行时修改web bean层级结构。

对于那些极少见的必须手工实例化web bean的情况，则使用OAControllerImpl类中的createWebBean()工厂方法。不要直接使用web bean的构造器，不必担心要直接创建oracle.apps.fnd.framework.webui.OAWebBeanFactory，因为控制器的createWebBean()方法代理了OAWebBeanFactory。

**注意：** 对于这些手工创建的beans，使用工厂方法时可以指定bean的“name”（JDeveloper中的ID属性）。避免使用deprecated的方法，它允许你在创建web bean时不指定name。web bean的名称（name）在同一个页面中必须是一个唯一标识。另外，bean的名称可能被OA Framework用于BC4J对象实例名（比如应用模块实例），因此不应该包含Java命名中规定的无效字符。

比如，下面的代码描述了如何创建两个web bean并将它们添加到父区域中。
```java
OATableLayoutBean tableLayout = (OATableLayoutBean)findIndexedChildRecursive("tableLayout");

// Create a row layout and give it the unique ID "topRow"
OARowLayoutBean row = (OARowLayoutBean)createWebBean(pageContext,
                                                     OAWebBeanConstants.ROW_LAYOUT_BEAN,
                                                     null, // no need to specify a data type
                                                     "topRow");

// Create a row layout and give it the unique ID "bottomRow"
OARowLayoutBean anotherRow = (OARowLayoutBean)createWebBean(pageContext,
                                                            OAWebBeanConstants.ROW_LAYOUT_BEAN,
                                                            null, // no need to specify a data type
                                                            "bottomRow");

// Always check to see if a web bean exists.
if (tableLayout != null)
{

   // Add the two row layout beans to the table so the "topRow" renders above
   // the "bottomRow"
   tableLayout.addIndexedChild(row);
   tableLayout.addIndexedChild(anotherRow);
}
```

也可以通过编程的方式将设计时定制的web bean关联到父区域中。比如，在下面的代码中，名为“HomeSearchRN”的stackLayout区域是在JDeveloper中定义的，但它必须通过编程的方式创建side navigation component。
```java
OASideNavBean sideNav = (OASideNavBean)createWebBean(pageContext,
                                                     OAWebBeanConstants.SIDE_NAV_BEAN,
                                                     null, // no need to specify a data type
                                                     "sideNav" // always specify name);

OAStackLayoutBean search =
   (OAStackLayoutBean)createWebBean(pageContext,
                                    "/oracle/apps/fnd/framework/toolbox/tutorial/webui/HomeSearchRN",
                                    "HomeSearchRN", // always specify name
                                     true); // region created in Oracle JDeveloper OA Extension

sideNav.addIndexedChild(search);
```

**约束**

OA Framework并不能很容易的支持通过编程的方式添加、删除、替换任何“默认（default）”区域中的子对象（比如OA Extension中的defaultSingleColumn区域是oracle.apps.fnd.framework.webui.beans.layout.OADefaultSingleColumnBean的实例）。这些区域应该通过设计的方式定义。如果绝对必须替换或删除“默认（default）”区域（不能添加item），则要遵循下面的步骤：

 1. 调用webBean.findIndexedChildRecursive()获得要被移除或替换的子web bean。

 2. 通过调用子web bean的childWebBean.getAttribute(OAWebBeanConstants.PARENT)方法获取子web bean的父对象。

**注意：** OAWebBeanConstants.PARENT属性被用作OA Framework内部开发使用（如果查看OAWebBeanConstants的Javadoc将看到警告信息）。只可以对缺省区域使用这个入口。另外，缺省区域已经不被推荐使用（deprecated），因此不应该在新的开发中使用这这些。

 3. 执行从父bean中替换或移除自己的操作。

# 处理HTTP POST（表单提交）
在HTTP POST处理过程中，OA Framework首先检查页面的web bean层级结构是否位于它的缓存中。如果没有（资源被限制或者用户使用了浏览器的后退按钮），则OA Framework必须在处理前重新创建web bean层级结构。这意味着processRequest()中的代码被重新执行，就好像浏览器发出了一个HTTP GET请求。

**注意：** 可能发生的重建web bean层级结构将导致产生了大量编码上的考虑，这些在Chapter 6: Supporting the Brower Back Button和OA Framework View和Controller编码规范中有完整的描述。

POST的主要处理过程发生在整个web bean层级结构中的两个分开的途径中：

 - 首先，OA Framework将在整个web bean层级结构中递归调用web bean的processFormData()方法将form的数据写入模型。任何需要在这个处理阶段执行的代码应该添加到控制器的processFormData(OAPageContext pageContext, OAWebBean webBean)方法。

 - 假设第一阶段的处理过程中没有发生异常，OA Framework处理第二阶段，在每个web bean上调用processFormRequest(OAPageContext pageContext, OAWebBean webBean)。

## processFormData()
多数情况（并非所有情况）下没有理由要覆盖这个方法。实际上，使用这种方法只会在极端的情况下，而不像是在OA Framework应用中：如果区域的数据源不是一个视图对象，因此没有为各个web bean定义视图实例和属性，这时你可以在区域的processFormData()方法中编码将子web bean的数据写入适当的数据源。

**注意：** OA Framework在item级实现了processFormData()，但你只能在region级别覆盖它，因此如果你实现了这个方法则必须处理region中的所有item。如果是有选择性的修改，则要记得先要调用super.processFormData(OAPageContext pageContext, OAWebBean webBean)。

## processFormRequest()
任何处理用户表单提交的动作属于processFormRequest()方法。

下面是一个典型的processFormRequest()的代码。它描述了好何决定是哪个组件的区域表单提交（在这里是“Go“按钮），如果开始在模型中查询，如何执行一个JSP Forward回到同一个页面以便在processRequest()方法中修改web bean的属性。
```java
public void processFormRequest(OAPageContext pageContext, OAWebBean webBean)
{
   // Always call this before adding your code
   super.processFormRequest(pageContext, webBean);

   // Pressing the Go button causes the search to be executed.
   If (pageContext.getParameter("Go") != null)
   {
     String orderNumber = pageContext.getParameter("SearchOrder");
     String created = pageContext.getParameter("Created");
     String showMyOrders = pageContext.getParameter("MyOrders");

     OAApplicationModule am = pageContext.getApplicationModule(webBean);

     // All parameters passed using invokeMethod() must be serializable.

     Serializable[] parameters = { orderNumber, created, showMyOrders };
     am.invokeMethod("search", parameters);

     // Now forward back to this page so we can implement UI changes as a
     // consequence of the query in processRequest(). NEVER make UI changes in
     // processFormRequest().

     pageContext.setForwardURLToCurrentPage(null, // no parameters to pass
                                            true, // retain the AM
                                            OAWebBeanConstants.ADD_BREAD_CRUMB_NO,
                                            OAWebBeanConstants.IGNORE_MESSAGES);
  }
} // end processFormRequest();
```
这个例子展示了如何使用setForwardUrl()方法传递请求参数，包括了如休替换一个已经存在的参数值（在这里，“X”将成为目标页面被“忽略（ignore）“的值）。
```java

import com.sun.java.util.collections.HashMap;
import oracle.bali.share.util.IntegerUtils;

...

processFormRequest(OAPageContext pageContext, OAWebBean webBean)
{
   // Always call this before adding your code
   super.processFormRequest(pageContext, webBean);

   String poEvent = pageContext.getParameter("poEvent");

   HashMap params = new HashMap(2);

   // Replace the current poEvent request parameter value with "X"
   params.put("poEvent", "X");

   // IntegerUtils is a handy utility
   params.put("poStep", IntegerUtils.getInteger(5));

   pageContext.setForwardURL("OA.jsp?page=/oracle/apps/dem/employee/webui/EmpDetailsPG", // target page
                             null, // not necessary with KEEP_MENU_CONTEXT
                             OAWebBeanConstants.KEEP_MENU_CONTEXT, // no change to menu context
                             null, // No need to specify since we're keeping menu context
                             params, // request parameters
                             true, // retain the root application module
                             OAWebBeanConstants.ADD_BREAD_CRUMB_YES, // display breadcrumbs
                             OAException.ERROR); // do not forward w/ errors
}
```

**注意：** 如果视图对象被作为被显示的web bean的数据源，则不要移除视图对象和它的行，以及嵌套包含的应用模块。如果你需要在定向到页面之前移除这些对象，则将不会显示视图对象中数据（出于性能优化的原因），在作出移除的调用后，确保使用oracle.apps.fnd.framework.webui.OAPageContext.forwardImmediatelyOAPageContext.setforwardURL方法定向到新页面。这保证了forward动作将立即发生，当前页面中forward调用后其它的web bean将不会处理；否则，移除视图对象或行实例将导致后续处理产生不良影响。

## 使用不同的技术POST到OA Framework页面
如果你使用不同的技术（比如JTT页面）POST到OA Framework页面，OA Framework只会执行目录页面的processRequest段。它不执行processFormData和processFormRequest段。

# 与模型交互
简单来说，应该只从OA Controller中直接访问应用模块。换言之，在控制器中唯一有效的模型导入代码如下：
```java
import oracle.apps.fnd.framework.OAApplicationModule;
```
不应该访问视图对象直接执行查询、迭代行集或与下层的实体交互。比如，下面的代码（尽管技术上是可行的）是不符合OA Framework Controller Coding Starndards的。
```java
import oracle.apps.fnd.framework.OAViewObject;
   ...

   // Get the root application module
   OAApplicationModule am = pageContext.getRootApplicationModule();

   // Find the view object you want to query
   OAViewObject vo = (OAViewObject)am.findViewObject("<instanceName>");

   ...
```
如果需要执行视图对象查询，应该按下面在“Search”区域中按下“Go”按钮的事件处理的例子的方式。

首先，添加方法到应用模块中（这个例子中，它是页面的根应用模块）它接收查询，然后将它委派给视图对象执行查询（查看[实现模型]({filename}build_model.md)获取关于查询的信息）。
```java
public void search(String orderNumber, String created, String showMyOrders)
{
  PoSummarySimpleExpVOImpl vo = getPoSummarySimpleExpVO();

  // Always check for the null condition if the VO cannot be found/created
  if (vo == null)
  {
    MessageToken[] tokens = { new MessageToken("OBJECT_NAME", "PoSummarySimpleExpVO")};
    throw new OAException("ICX", "FWK_TBX_OBJECT_NOT_FOUND", tokens);
  }

  vo.initQuery(orderNumber, created, showMyOrders);

} // end search()
```
然后，添加如下的按钮处理代码到控制器中，它调用应用模块中对应的方法。

注意，总是应该在processFormRequest()的代码中检查事件源；不要假设浏览器发送的POST请求是由于你的item被选中了（即使是一个只有一个按钮的简单页面）。在后台，OA Framework经常提交页面的表单，而这可能是不是你所期望的。
```java
processFormRequest(OAPageContext pageContext, OAWebBean webBean)
{

  // Check to see if the "Go" button was pressed...
  if (pageContext.getParameter("gButton") != null)
  {
    // Get the search criteria
    String orderNumber = pageContext.getParameter("SearchOrder");
    String created = pageContext.getParameter("Created");
    String showMyOrders = pageContext.getParameter("MyOrders");

    OAApplicationModule am = pageContext.getApplicationModule(webBean);

    // All parameters passed using invokeMethod() must be serializable.
    Serializable[] parameters = { orderNumber, created, showMyOrders };
    am.invokeMethod("search", parameters);
  }
}
```

**技巧：** 不要在服务端BC4J组件中调用invokeMethod()，任何你传递的参数必须是Serializable类型的。上例中展示的的invokeMethod()方法需要的参数都是字符串。如果需要传递其它对象类型，可以使用带一个类型数组参数版本的invokeMethod()。比如：
```java
Class[] parameterTypes = { String.class, Hashtable.class, Number.class ...};
am.invokeMethod("search", parameters, parameterTypes);
```
类似地，由于视图对象是实体对象的导管——不应该在控制器中直接与视图对象交互——也应该通过应用模块来处理实体操作。

**注意：** 如[实现模型]({filename}build_model.md)中描述的，添加到应用模块中的方法命名应该与UI“事件（events）“对应。比如，如果用户按了“Create”按钮，应用模块方法应该命名为“create”等等。

**创建的实例**

```java
processFormRequest(OAPageContext pageContext, OAWebBean webBean)
{
  OAApplicationModule am = pageContext.getApplicationModule(webBean);
  am.invokeMethod("create", null);
}
```

**删除的实例**

这个例子展示了调用共享区域中的嵌套应用模块中的delete方法而不是调用页面根应用模块中的方法。
```java
processFormRequest(OAPageContext pageContext, OAWebBean webBean)
{

 if (pageContext.getParameter("DeleteYesButton") != null)
 {
   // User has confirmed that she wants to delete this purchase order.
   // Invoke a method on the AM to set the current row in the VO and
   // call remove() on this row.

   String poHeaderId = pageContext.getParameter("poHeaderId");
   Serializable[] parameters = { poHeaderId };

   OAApplicationModule am = pageContext.getApplicationModule(webBean);
   am.invokeMethod("delete", parameters);
  }

 ...
```

**自定义动作实例（“Approve”）**

```java
processFormRequest(OAPageContext pageContext, OAWebBean webBean)
{
  if (pageContext.getParameter("Approve") != null)
  {
    OAApplicationModule am = pageContext.getApplicationModule(webBean);
    am.invokeMethod("approve");
  }
}
```

**提交操作实例**

```java
processFormRequest(OAPageContext pageContext, OAWebBean webBean)
{
   // Simply telling the transaction to commit will cause all the Entity Object validation
   // to fire.
   //
   // Note: there's no reason for a developer to perform a rollback. This is handled by
   // the OA Framework if errors are encountered during the processFormData phase.

   OAApplicationModule am = pageContext.getApplicationModule(webBean);
   am.invokeMethod("apply");
}
```

# 禁用校验
有多个机会可以屏蔽在处理OA Framework HTTP POST过程中的校验。比如，实现表格中的”Add Another Row“中，在用户添加新行的操作时，可能不需要因为未填写完整的行数据而显示错误信息。同样，你可能在一个多步骤的页面流中想要将校验延时到最后一个预览提交页面，或者通过tabs导航到同一个下层对象的不同视图上时。

## 禁用服务端校验
为了阻止从模型校验逻辑中抛出异常，在页面中与下面列表对应的bean上调用setServerUnvalidated(true)方法（记住在processRequest()方法中添加修改web bean的代码）：

 - OASubmitButtonBean

 - OATableBean

 - OAAdvancedTableBean

 - OASubTabLayoutBean

 - OANavigationBarBean

 - OADefaultHideShowBean

 - OAHideShowHeaderBean

**注意：** 也可以在设计时设置组件的Disable Server Side Validation属性为True，也可以为那些配置为提交表单的链接或图标设置禁用校验。查看下面的Javascript URL一节获得更多信息。

当用户执行一个由这些bean导致的表单提交时，OA Framework按上面描述的方式执行所有的HTTP POST处理——包括执行属性级别的校验逻辑（实体级别的校验没有被执行）。如果在处理processFormData()过程中抛出了oracle.apps.fnd.framework.OARowValException或oracle.apps.fnd.framework.OAAttrValException异常（功它们被deprecated的子类），OA Framework只是简单的忽略这些异常，并继续执行就像没有遇到异常一样。

**注意：** OA Framework不会忽略processFormData()中的严重异常（比如NullPointerException）。这些会按正常的方式显示出来，并且不会继续处理processFormRequest()。而且processFormRequest()中由你或者由BC4J抛出的异常都会被正常的显示出来。

## 禁用客户端校验
当一个带的客户输入的数据的表单提交时，UIX执行一些基础的onSubmit JavaScript校验（它校验必填字段，数据类型和格式），如果校验通过就提交表单。为了屏蔽校验，也需要在上节“禁用服务端校验”中的bean列表中的bean上调用setUnvalidated(true)方法。

**注意：** 也可以在设计时设置组件的Disable Server Side Validation属性为True，也可以为那些配置为提交表单的链接或图标设置禁用校验。查看下面的Javascript URL一节获得更多信息。

**技巧：** 对于tables和HGrid组件，必须通过设置table和HGrid区域自己的属性启用／禁用客户端校验，因为你不能直接访问OANavigationBarBean的用作数据集导航的子web bean。注意，现在不能禁用这些组件的服务端校验。

# 错误处理
OA Framework自动显示模型层抛出的任何错误信息；不需要在控制器中做什么就能处理。

 - 查看Error Handling获取更多关于在控制器中抛出异常和在页面顶端显示错误、警告、确认信息。

 - 查看Chapter 4: Dialog Pages获取关于显示模型错误、警告、确认和信息的对话框页面。

# JavaScript
UIX和OA Framework正在快速的添加新的功能以提供更好的用户体验（区域页面渲染、自动的表格统计等等）。当这些功能发布后，你将受益于这些功能，但是，在这之前你不应该自己实现这些功能。

简单来说，Javascript在OA Framework开发团队外是被禁止的。

## JavaScript URL
以前，如果需要配置链接或图像来提交页面表单（由于你需要在导航到新页面前处理事件），可以将它设置在UIX submitForm Javascript函数中。

现在，应该配置fireAction事件来代替使用Javascript URL。查看Declarative Submit Form文档获取其它信息。

