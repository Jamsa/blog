Title: OAF开发笔记
Date: 2010-12-09
Modified: 2010-12-09
Category: 开发
Tags: oracle,ebs,oaf

# 开发advancedTable in advancedTable

 1. 配置两个VO，建立两个VO之间的View Link对象。在页面中以两个VO中的主VO创建outerTable，在outerTable上创建detail，在这个detail中再以主从关系中的从VO创建innerTable。outerTable和inerTable都为advancedTable类型。

 2. 主从关系中主VO需要增加一个属性用于标识下innerTable是否展开，它的值为字符串Y或N。将outerTable的Detail View Attribute设置为这个属性的名称。

 3. 将outterTable的Child View Attribute设置为关联字段的名称。

 4. 将outterTable的View Link Instance设置为主从关系的View Link实例名（不是类名）。

 5. 将innerTable和Detail View Attribute设置为对应的属性（如果有）。

 6. 将innerTable的View Link Instance设置为主从关系的View Link实例名（不是类名）。

 7. 这些设置与OAF Guide中下面这段代码起的作用是一样的，这样设置以后下面CO中的代码就不需要了。
```java
public void processRequest(...)
{
  OAWebBean outerTable = (OAWebBean)webBean.findChildRecursive("outerTable");
  OAWebBean innerTable = (OAWebBean)webBean.findChildRecursive("innerTable");
  if (outerTable != null)
  {
    outerTable.setAttributeValue(CHILD_VIEW_ATTRIBUTE_NAME,"Deptno");
    outerTable.setAttributeValue(VIEW_LINK_NAME,"DeptEmpVL");
  }
  if (innerTable != null)
  {
    innerTable.setAttributeValue(CHILD_VIEW_ATTRIBUTE_NAME,"Deptno");
    innerTable.setAttributeValue(VIEW_LINK_NAME,"DeptEmpVL");
  }
  ...
  ...
}
```

# 开发HGrid和Tree组件

 1. 以自关联的VO为例，添加一个VL以关联自身。但并不要求必须是自关联。

 2. 新建一个hGrid区域，在其中添加tree和其它的项。

 3. 在tree的nodeDef中设置好View Instance和View Attribute以作为节点的标题。

 4. 在tree和childNode中设置Ancestor Node为需要递归显示的区域，例如：/dtxxsoft/oracle/apps/cux/dpt/task/webui/DptTaskMainPG.TreeColumnRN。不要使用View Link Instance，它已经deprecated，只需要设置View Link Accessor，它的值为VL的定义中Destination一方的Accessor Name。

 5. HGrid的查询。多次尝试未成功。替代的方法是另做一个列表页面进行查询，在列表中选中节点后，计算出该节点在树中的路径，再转到HGrid页面，并Focus到这个节点。

 6. HGrid的初始焦点路径，例如设置到根节点的第5个子节点下的第2个节点上。查询时也是通过设置该属性来定位。
```java
int[] focusRootPath = {4, 1};
setInitialFocusPath(String[] focusRootPath)
```

 7. HGrid列表在数据库中的新数据时不能刷新，即使将HGrid对应的vo缓存清空也无效。只能在页面跳转时不保存am，或者手工调用pageContext.releaseRootApplicationModule方法让页面的AM失效，这样HGrid界面才能刷新。

 8. 如果设置焦点路径要注意HGrid根节点有多个节点和只有一个节点时的区别，如果只有一个节点则它将是根节点。如果有多个根极节点，则HGrid将自动产生一个根节点。如果只有一个根级节点，则计算路径时，不要将根节点自身计算进去。

# 关于RetainAM

开发手册中所说的RetainAM的情况必须是在两个页面使用相同类型的根应用模块时才能使用。而在实际使用过程中，我发现两个页面使用了不同的AM，在使用RetainAM=Y时同样有效。例如，从A页面Forward到B页面时RetainAM=Y，然后在B页面进行一些操作，此过程中总是使用RetainAM=Y，当从B页面回到A页面时仍然使用RetainAM=Y，这样A页面的AM的状态仍然能够保留。即使我在B页面中使用pageContext.releaseRootApplicationModule()，这时失效的也只是B页面自己的AM，回到A页面时，A页面的AM仍然有效。

# 基于SQL的只读VO的一个Bug

如果使用<code>select t.* from aaa t</code>之类的SQL来创建VO，当aaa表中添加了新的字段后，VO不能自动同步，页面中的项有可能出现与VO的属性不匹配的情况。

# 取库存组织
```
select oav.organization_id org_id,
       oav.organization_code org_code,
       oav.organization_name org_name,
       oav.responsibility_id resp_id,
       oav.resp_application_id resp_app_id
from   org_access_view oav,
       mtl_parameters mp,
       wip_eam_parameters wep
where  oav.organization_id = mp.organization_id
and    NVL(mp.eam_enabled_flag,'N') = 'Y'
and    oav.organization_id = wep.organization_id
order by org_code
```

# 日志
OAF日志不支持日志级别的处理。没有日志的优先级。日志级别的有效值是OAFwkConstant中的UNEXPECTED, ERROR, EXCEPTION, EVENT, ROCEDURE, STATEMENT, PERFORMANCE。

# 开发包含train的多步处理页面
开发文档中有个错误：

Step CE-5.3 Add Links to the navigationBar中Destination URI /<yourname>/oracle/apps/ak/employee/webui/ EmpUpdatePG的Destination URI的值应该与应该包含OA.jsp?page=。该值应该与Step CE-4.2 Add Three Train Nodes to the EmpTrainRN Region中设置的Destination URI的值保持一致。

该错误将导致点击“下一步”时train最多只能到第二步，NavButtonBar中的下拉列表中的当前步骤始终显示为第一步。

# OAF页面缓存

## 清除高速缓存
页面缓存将被清理
Functional Adminstrator > Core services > Caching Framework > Clear cache.

## 开发中的页面缓存
在JSP页面中使用oracle.apps.jtf.cache.CacheManager.invalidate()方法可以清空页面缓存。

# 由链接弹出的页面
将链接的target属性为_blank时页面将在弹出窗口中打开。这时要注意，链接上要加上retainAM=Y否则在窗口弹出后，在原页面中进行操作时将出错。

有可能是因为oaf中的am实际是与用户session关联的，当与服务器有交互时，如果没有retainAM则上一个am将丢失。ebs中除了lov之类的弹出页面外，也没有其它的弹出页面。估计也是因为这个原因，oaf不能维护在同一个http session中进行两个AM相关的操作。这是根据以下分析得来的：

在弹出的窗口中，如果所有操作都是post或retainAM=Y的操作，则原窗口中仍可继续操作。如果在弹出窗口中点击了“主页”等会让AM失效的链接时，则父窗口的AM也将失效。

# JSP相关

## 在JSP中获取JDBC连接
来源：http://www.itjaj.com/thread-3994-1-1.html

方法一：使用FWAppsContext获取连接
```
<%@page import="java.sql.Connection"%>
<%@page import="oracle.apps.jtf.base.session.FWAppsContext"%>
<%@page import="oracle.apps.jtf.base.session.ServletSessionManager"%>
<%@page import="oracle.apps.jtf.base.session.FWSession"%>

String appName = request.getParameter("appName");
String stateless = request.getParameter("stateless");

if (appName == null) appName = "JTF";
if (stateless == null) stateless = "T";

FWSession _fwSession;
try {
  _fwSession = oracle.apps.jtf.base.session.ServletSessionManager.startRequest(request,response,appName,statelessB);
} catch(oracle.apps.jtf.base.session.ServletSessionManagerException e) {
  throw e;
}
FWAppsContext cont = _fwSession.getFWAppsContext();
Connection conn = cont.getJDBCConnection();

try {
  // 程序代码逻辑
  
}
finally {
  if (conn != null)
    conn.close();
}

/**** End Request ****/
try {
  oracle.apps.jtf.base.session.ServletSessionManager.endRequest(request, false);
} catch(oracle.apps.jtf.base.session.ServletSessionManagerException e) {
  throw e;
}
```

FWAppsContext可以获取很多环境数据，如UserID、RespId、RespApplId等，还可以设置和获取Session值。

方法二：使用EBS的SSO类库获取数据库连接
```
<%@page import="oracle.apps.fnd.common.WebAppsContext"%>
<%@page import="oracle.apps.fnd.common.ProfileStore"%>
<%@ page import="oracle.apps.fnd.sso.*" %>

boolean isCtxAvailable = false;
WebAppsContext wctx = null;

if (Utils.isAppsContextAvailable())
{
  isCtxAvailable = true;
}
wctx = Utils.getAppsContext();
Connection conn = Utils.getConnection();
ProfileStore profilestore = wctx.getProfileStore();

try
{
  // 程序代码逻辑

}
finally
{
  conn.close();
  if (!isCtxAvailable)
  {
    Utils.releaseAppsContext();
  }
}
%>
```

方法三：其它方法
上面两种方法是我常用的方法，除此之外，还可以使用以下任一种方法来获取连接，其实每种方式最终都是调用AppsContext来获取数据库连接的
1、调用oracle.apps.jtf.aom.transaction.TransactionScope.getConnection();

2、使用WebRequestUtil来获取WebAppsContext，并最终获取数据库连接
```
<%@ page import="oracle.apps.fnd.common.WebAppsContext" %>
<%@ page import="oracle.apps.fnd.common.WebRequestUtil" %>

<%
WebAppsContext ctx = WebRequestUtil.validateContext(request, response);
WebRequestUtil.setClientEncoding(response, ctx);
Connection conn = ctx.getJDBCConnection();
...
%>
```


## JSP文件编译
相关环境变量：
 - $FND_TOP/patch/115/bin/ojspCompile.pl JSP编译脚本

 - $OA_HTML JSP保存目录

 - $OAD_TOP/_pages JSP编译为class后的保存目录

编译命令：

 - 强制重新编译所有JSP文件
```sh
ojspCompile.pl –compile –flush -p
```

 - 编译单个文件
```sh
ojspCompile.pl --compile -s a.jsp
```
a.jsp为文件名匹配表达式。

# 设置表格中汇总数据的值
```java
OAMessageStyledTextBean salaryBean = 
    (OAMessageStyledTextBean)webBean.findChildRecursive("item1");

salaryBean.setAttributeValue(TABULAR_FUNCTION_VALUE_ATTR, "123");
```
上例中iem1为，设置了Total Value为True的列。

# UI控制

## 不同UI效果的例子

对于不同的UI效果可以参考范例包oracle.apps.fnd.framework.toolbox.samplelib中的例子。

## 自定义xss文件来设置CSS定义
```
  <style selector=".CuxIssueLevel02">
    <property name="color">#ff6600</property>
  </style>
```
修改OA_HTML/cabo/custom.xss或者添加新的xss文件然后在custom.xss中引用。然后通过设置WebBean的CSSClass属性来使用所定义的样式。

使用中发现有bug，在其中定义颜色使用"orange"时不能正确生成到css文件中去，而使用rgb方法来表示则正常。

## 使用UrlInclude引入CSS定义
使用UrlInclude组件包含CSS文件或包含带样式定义的文件。然后通过设置WebBean的CSSClass属性来使用所定义的样式。

## 设置内联样式
直接设置WebBean的InlineStyle来设置内联样式：
```java
CSSStyle cellStyle = new CSSStyle();
cellStyle.setProperty("border", "#cc0000 solid");
cellStyle.setProperty("border-width", "0 1 1 0");
cellFormatBean.setInlineStyle(cellStyle);
```

## 编程方式实现动态绑定属性
默认情况下Required, Rendered, Disabled, and Read Only的值可以设置为SPEL表达式。如果有其它属性需要动态绑定则要使用动态绑定技术。OAF提供了三种类型的绑定：
```java
oracle.apps.fnd.framework.webui.OADataBoundValueViewObject
oracle.apps.fnd.framework.webui.OADataBoundValueAppModule
oracle.apps.fnd.framework.webui.OAFunctionSecurityBoundValue
```

## 使用动态绑定控制组件样式
通过使用OADataBoundValueViewObject将组件的style Class绑定到VO属性上来控制颜色。
```java
OAWebBean bean = webBean.findChildRecursive("bean");
if (bean != null)
    bean.setAttributeValue(OAMessageStyledTextBean.STYLE_CLASS_ATTR, 
                           new OADataBoundValueViewObject(bean, 
                                                          "ViewAttrName"));
```
样式可以使用上节中介绍的方法进行定义。

# 新建记录后在保存后，部分LOV带出来的只读字段丢失
这是因为只读字段的数据不会被保存到VO中，因此需要在保存完后刷新一次当前的VO，让数据重新加载一次，这通常可以调用AM中编辑记录的方法，让它重新执行一次查询，使VO中的只读字段重新从数据库加载。

