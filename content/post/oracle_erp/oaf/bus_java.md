---
title: "实现服务端功能之——Java实体对象"
date: 2007-09-02
modified: 2007-09-02
categories: ["开发"]
tags: ["oracle","ebs","oaf"]
---
Slug: bus_java

# 关于实体对象
实体对象包含了业务逻辑和对表的DML操作。

## 对象模型和关键类
 - oracle.apps.fnd.framework.server.OAEntityCache：这个缓冲用于存储特殊实体的查询过的行。映射到同样的实体的多个视图对象共享相同的实体缓存。

 - <YourEntityName>EOImpl继承oracle.apps.fnd.framework.server.OAEntityImpl：这是实体对象本身。当实例化后，它代表数据中的一行。

 - oracle.apps.fnd.framework.server.OAEntityDefImpl：表示描述实体对象的元数据，包括属性（attributes）、事件、校验器、关联和属性（properties）。当实例化后，它描述了实体对象类的所有实例。实体定义类是一个单例类。

 - <YourEntityName>Expert继承oracle.apps.fnd.framework.server.OAEntityExpert：这是一个特殊的单例辅助类，它用于注册一个实体。

 - oracle.jbo.Key：这是一个不可变的主、外键或复合主键。

# 创建
为了创建实体对象，必须调用对应的上层视图对象中的createRow方法然后再调用insertRow方法。
```java
// In the application module; this example from the OA Framework
// ToolBox Tutorial will instantiate a SupplierEOImpl.

public void create()
{
  OAViewObject vo = getSuppliersVO();
  vo.insertRow(vo.createRow());

  // Always call this after you perform a row insert. See the Entity Object
  // New / Initial section below for additional information.
  vo.setNewRowState(Row.STATUS_INITIALIZED);
}
```
视图对象的createRow方法调用下层实体对象的create()方法。可以在实体的create()方法中添加初始化代码，可以参考oracle.apps.fnd.framework.toolbox.tutorial.server.SupplierEOImpl类。

**警告：** 不要将初始化逻辑放到实体对象的构造器中；总是应该将这些代码添加到create()方法中super.create(attributeList)方法调用的后面。

**技巧：** 如果默认值可以在设计时决定，并且是为特定的UI而决定的，也可以通过在设计器中设置item的Initial Value属性来指定默认值。这些值可以被用户个性化；而不需要创建实体你的对象的子类并覆盖create()方法来设置默认值。查看Defaulting章节查看细节信息。
```java
/**
 * In the SupplierEOImpl class; initialize a new supplier.
 */
Public void create(AttributeList attributeList)
{
  super.create(attributeList); 
  OADBTransaction transaction = getOADBTransaction();
   
  // Supplier id is obtained from the table's sequence
  Number supplierId = transaction.getSequenceValue("FWK_TBX_SUPPLIERS_S");
  setSupplierId(supplierId);
  
  // Start date should be set to sysdate
  setStartDate(transaction.getCurrentDBDate());
} // end create()
```
**技巧：** 当在实体对象中设置值时，总是使用set<AttributeName>(val)代替setAttribute("<AttributeName>", val)方法可以提高性能，因为前者跳过了查找字段的步骤。如果需要忽略编程方式实现的属性校验而仍需要执行设计时定义的校验时，可以直接调用setAttributeInternal()。查看Entity Object and View Object Attribute Setters以获取更多信息。

## 复合实体关联
在复合关联中BC4J将在设置父对象主键属性值时自动设置子实体对象。父对象主键值是在调用create()方法时通过attributeList参数传递进去的，并且在super.create(attributeList)被执行时被设置值。

不要尝试自己来处理主键值。

## 实体对象的Initial/New状态
缺省情况下，实体对象被创建时row状态为STATUS_NEW，并且BC4J将它们添加到它们的校验器中并且post监听。这时，任何事件触发校验或数据库提交sequence包括这些实体对象。（By default, entity objects are created with the     row state of STATUS_NEW, and BC4J adds them to its validation and post listener lists. In this case, any event that triggers a validation or database post sequence includes these entity objects.）

如OA Framework Model Coding Standards中的规定，应该将通过显式的在视图对象中调用创建新行的方法后立即调用ViewRowImpl对象的setNewRowState(STATE_INITIALIZED)方法。

当执行这个后，BC4J将从事务中和校验监听列表中移除对应的实体对象，这样它们将不会被校验或提交到数据库。当用户做出修改（属性的“setter”被调用后），实体对象的状态修改为STATUS_NEW，并且BC4J返回它到validation/post lists。你也可以在ViewRowImpl上调用setNewRowState(STATUS_NEW)在任何时候手工改变状态。

## 特殊“Create”的情况
**“Flattened”主／从处于单一行中**

在OA Framework ToolBox教程中，我们有主／从实体显示于同一行中，“flattened”行中。比如采购单包含了很多行，它们依次包含了多个供货商，在我们的UI中，我们将采购单的行和供货单实现为1:1的关系。

尽管BC4J可以很容易的为单个视图对象行创建多个不同类型的实体对象——这些实体对象是不相关的或是平等的——在一个对象是另一个对象子对象时需要你介入。在这种情况下，必须在你的视图对象行实现的create()方法中添加下面的代码，以确保正确的父对象的主键被设置到低层次的子对象的实体中：
```java
// The following is required to support the creating the master/detail line
// and shipment entities that have been "flattened" into a single row in
// POLineShipFullVO with a 1:1 join.
//
// If you don't do this, BC4J will automatically treat them like peers and
// try to set the po header id as the parent key for both entities.
   
protected void create(oracle.jbo.AttributeList nvp) 
{ 
  PurchaseOrderLineEOImpl lineEO = (PurchaseOrderLineEOImpl)getEntity(0); 
  PurchaseOrderShipmentEOImpl shipmentEO = (PurchaseOrderShipmentEOImpl)getEntity(1);    
   
  try 
  {
    // Create Lines EO 
    lineEO.create(nvp); 
   
    // Create Shipments EO 
    shipmentEO.create(lineEO); 

    // Calling this ensures that any personalization default values are
    // properly set since the OAF normally sets this in the super.create(), but
    // since this is not called in this workaround, we need another method
    // to ensure customer defaults are applied.
    setDefaultValue();
  } 
  catch (Exception ex) 
  { 
    lineEO.revert(); 
    shipmentEO.revert();
  
    if (ex instanceof oracle.jbo.JboException) 
    { 
      oracle.jbo.JboException jboEx = (oracle.jbo.JboException)ex; 
      // Developers have to do the mapping on their own because of the override. 
      jboEx.doEntityToVOMapping(getApplicationModule(), new oracle.jbo.ViewObject[]{getViewObject()});    
      throw jboEx; 
    } 
    throw OAException.wrapperException(ex); 
  }
} // end create() 
```

## 实体对象缓存
一旦被创建后，BC4J将实体对象因为各种原因被存储于特殊的事务缓冲区中，在JDeveloper BC4J文档中有完整的描述。两个重要的好处在于：

 - 处理同一个根应用模块中的多个视图对象可以共享同样的下层实体对象。这意味着在一个视图对象中修改实体后将立即反映到其它引用该实体对象的视图对象中。

 - 数据修改将被保留在缓冲区中即使视图对象的行集被刷新。比如，在主－从关系中，在 **从** 视图对象中由实体对象派生的属性值被保存在缓存中，即使用户从一个 **主** 视图对象转换到另一个。所有数据修改将原封不动的保存在事务生命中。

懂得这个缓冲区的存在是很重要的，因为你必须明确的执行某些验证，比如，当执行唯一性验证时你必须同时检查实体缓冲区和数据库。

有三种主要方式同时检查缓冲区和数据库：

 1. 使用findByPrimaryKey()方法

 2. 手工迭代缓冲区

 3. 使用关联对象迭代缓冲区

**findByPrimaryKey()方法**

findByPrimaryKey()方法确保先查询缓冲区中与给定的主键相匹配的实体对象，然后查找数据库。这是一个非常用有的方法，但它并不是一个轻量的方法，因为它为从数据库中找到的记录实例化实体对象。它将 **整个** 实体对象放入内存，而不只是主键。这个方法可以——也应该——被用于当你不需要查找一个匹配的情况——比如，当验证一个基于序列的主键。它也适合用于需要在查找到的目标上调用方法以便中间层访问的情况。

下面的代码来自于oracle.apps.fnd.framework.toolbox.schema.server.SupplierEOImpl类，描述了这个方法的使用：
```java
public void setSupplierId(Number value)
{ 
  if (value != null)
  {
    // Supplier id must be unique. To verify this, you must check both the
    // entity cache and the database. In this case, it's appropriate
    // to use findByPrimaryKey( ) because you're unlikely to get a match, and
    // and are therefore unlikely to pull a bunch of large objects into memory.

    // Note that findByPrimaryKey() is guaranteed to check all suppliers. 
    // First it checks the entity cache, then it checks the database.

    OADBTransaction transaction = getOADBTransaction();
    Object[] supplierKey = {value};
    EntityDefImpl supplierDefinition = SupplierEOImpl.getDefinitionObject();
    SupplierEOImpl supplier = 
      (SupplierEOImpl)supplierDefinition.findByPrimaryKey(transaction, new Key(supplierKey));
    if (supplier != null)
    {
      throw new OAAttrValException(OAException.TYP_ENTITY_OBJECT,
             getEntityDef().getFullName(), // EO name
             getPrimaryKey(), // EO PK
             "SupplierId", // Attribute Name
             value, // Bad attribute value
             "ICX", // Message application short name
             "FWK_TBX_T_SUP_ID_UNIQUE"); // Message name 
    }
  }
  
  setAttributeInternal(SUPPLIERID, value);
} // end setSupplierId()
```

**手工迭代缓冲区**

可以通过手工的方式检查实体缓冲区，以执行与findByPrimaryKey()相同的检查。然后再在另一步中执行对数据库的检查。这种方式的好处是可以避免不必要的实例对象（译：实体）。

下面的例子也是来自于ToolBox教程中SupplierEOImpl类中：
```java
public void setName(String value)
{
  // Since this value is marked as "mandatory," the BC4J Framework will take
  // care of ensuring that it's a non-null value. However, if it is null, we
  // don't want to proceed with any validation that could result in a NPE.
   
  if ((value != null) || (!("".equals(value.trim()))))
  {
    // Verify that the name is unique. To do this, we must check both the entity
    // cache and the database. We begin with the entity cache.
    com.sun.java.util.collections.Iterator supplierIterator = 
      getEntityDef().getAllEntityInstancesIterator(getDBTransaction());
   
    Number currentId = getSupplierId();
   
    while ( supplierIterator.hasNext() )
    {
      SupplierEOImpl cachedSupplier = (SupplierEOImpl)supplierIterator.next();

      String cachedName = cachedSupplier.getName();
      Number cachedId = cachedSupplier.getSupplierId();
      
      // We found a match for the name we're trying to set, so throw an
      // exception. Note that we need to exclude this EO from our test.

      If (cachedName != null && value.equalsIgnoreCase(cachedName) &&    
        cachedId.compareTo(currentId) != 0 )
      {
        throw new OAAttrValException(OAException.TYP_ENTITY_OBJECT,
                               getEntityDef().getFullName(), // EO name
                               getPrimaryKey(), // EO PK
                               "Name", // Attribute Name
                               value, // Attribute value
                               "ICX", // Message product short name
                               "FWK_TBX_T_SUP_DUP_NAME"); // Message name 
      }
    }
     
    // Now we want to check the database for any occurrences of the supplier
    // name. The most efficient way to check this is with a validation view
    // object which we add to a special "Validation" application module.
    OADBTransaction transaction = getOADBTransaction();
    OAApplicationModule vam;
    // Look to see if the VAM has already been created in this transaction. If not,
    // create it.
    vam = (OAApplicationModule)transaction.findApplicationModule("supplierVAM");
    if (vam == null)
    { 
      vam = 
      (OAApplicationModule)transaction.createApplicationModule("supplierVAM",
         "oracle.apps.fnd.framework.toolbox.schema.server.SupplierVAM");
    }
   
    // Now, we use a lightweight "validation" view object to see if a supplier exists
    // with the given name.
    SupplierNameVVOImpl valNameVo = (SupplierNameVVOImpl)vam.findViewObject("SupplierNameVVO");
    valNameVo.initQuery(value);
    if (valNameVo.hasNext())
    {
      throw new OAAttrValException(OAException.TYP_ENTITY_OBJECT,
            getEntityDef().getFullName(), // EO name
            getPrimaryKey(), // EO PK
            "Name", // Attribute Name
            value, // Attribute value
            "ICX", // Message application short name
            "FWK_TBX_T_SUP_DUP_NAME"); // Message name
    }
  }
   
  setAttributeInternal(NAME, value);
} // end setName()
```

**关联对象迭代**

这与findByPrimaryKey()类似，它保证同时检查实体缓冲区和数据库。它也将会将找到的实体对象加载到内存，这用于需要调用实体中方法时。与findByPrimaryKey()方法不同，它可以通过任何key查找任何类型的实体对象，这只用于与当前对象间通过关联对象相关联的实体对象。

下面的代码描述了根复合实体对象使用关联对象查找它的所有子对象。
```java
private void checkLineExists()
{ 
  // A purchase order header must have at least 1 associated line.
  // To check this, we first do a manual check of the entity cache
  // If we find a line for this header, we're done (note that the entity cache won't
  // include EOs that are DELETED or DEAD).

  com.sun.java.util.collections.Iterator fastIterator = 
    PurchaseOrderLineEOImpl.getDefinitionObject().getAllEntityInstancesIterator(getDBTransaction());
 
  Number currentHeaderId = getHeaderId();
  while ( fastIterator.hasNext() )
  {
    PurchaseOrderLineEOImpl cachedLine = (PurchaseOrderLineEOImpl)fastIterator.next();

    Number cachedHeaderId = cachedLine.getHeaderId();

    // If we find a match, we're done. Don't forget to look ONLY for lines
    // for this header... The entity cache can include lines for other headers
    // also.
   
    If ((cachedHeaderId != null) && (cachedHeaderId.compareTo(currentHeaderId) == 0 ))
    {
      return;
    } 
  }

  // We haven't found any matches in the cache yet, so now we need to check
  // the database...    
  
  // In this example, we're illustrating the use of the association between the
  // header and its lines to iterate through all the shipments.  This will
  // check both the cache and the database, and will bring all the rows
  // into the middle tier.
  // Note that this looks only at lines for this
  // header so we don't need to filter our results, so it is convenient.
  RowIterator linesIterator = getPurchaseOrderLineEO();
   
  if (!(linesIterator.hasNext()))
  {
    throw new OARowValException(OARowValException.TYP_ENTITY_OBJECT,
                getEntityDef().getFullName(),
                getPrimaryKey(),
                "ICX", // Message product short name
                "FWK_TBX_T_PO_NO_LINES"); // Message name
  }
} // end checkLineExists()
```

## 实体状态
每个实体对象都有一个相关的“实体状态”它描述了实体的状态与下层数据库和事务关联。可以调用getEntityState()检查实体的状态。

**技巧：** BC4J从实体缓冲区中自动移除任何状态为STATUS_DEAD的实体对象，因此你不需要在查找“好”的实体对象时关心手工排除这些对象的问题。

 - STATUS_NEW 实体对象在当前事务中是新的

 - STATUS_DELETED 实体对象来自于数据库并且在当前事务中已经被删除

 - STATUS_MODIFIED 实体对象来自于数据库并且已经被改变了

 - STATUS_UNMODIFIED 实体对象来源于数据库并且没有被改变为，或者已经被改变过并且改变已经被提交

 - STATUS_DEAD 实体对象在当前事务中是新的并且已经被删除

 - STATUS_INITIALIZED 实体对象牌“临时（temporary）”状态并且将不会被提交或校验

# 修改／校验
这节描述如何正确执行属性级和实体级的校验。

## 属性级校验
如[实现视图](../build_view/)一章中描述的，当向页面发起HTTP POST请求时修改的值时，OA Framework将这些值回写到下层的视图对象，再通过调用实体对象的setter方法将这些值写入下层的实体对象。

因此每个属性的校验应该被添加到它的setter方法中（查看ToolBox的PurchaseOrderHeaderEOImpl的setHeaderId()方法，如下），调用实体对象的setter方法执行的是属性级的校验。

如果显示的指定了校验（比如，你在JDeveloper Entity Object Wizard中指定一个属性在它被保存后不能被更新），这个校验是在setAttributeInternal()方法中执行的，你应该将它放在你自己的校验逻辑的后面执行。它也将在validateEntity()中执行。
```java
/**
 * Sets the PO Header Id.
 *
 * Business Rules:
 * Required; cannot be null.
 * Cannot be updated on a committed row.
 */
public void setHeaderId(Number value)
{
  // BC4J validates that this can be updated only on a new line. This
  // adds the additional check of only allowing an update if the value
  // is null to prevent changes while the object is in memory.

  If (getHeaderId() != null)
  {
    throw new OAAttrValException(OAException.TYP_ENTITY_OBJECT,
                                 getEntityDef().getFullName(), // EO name
                                 getPrimaryKey(), // EO PK
                                 "HeaderId", // Attribute Name
                                 value, // Attribute value
                                 "ICX", // Message product short name
                                 "DEBUG -- need message name"); // Message name
  }
  if (value != null)
  {
    OADBTransaction transaction = (OADBTransaction)getOADBTransaction();
    
    // findByPrimaryKey() is guaranteed to first check the entity cache, then check
    // the database. This is an appropriate use of this method because finding a    
    // match would be the exception rather than the rule so we're not worried 
    // about pulling entities into the middle tier.
 
    Object[] headerKey = {value};
    EntityDefImpl hdrDef = PurchaseOrderHeaderEOImpl.getDefinitionObject();
    PurchaseOrderHeaderEOImpl hdrEO = 
      (PurchaseOrderHeaderEOImpl)hdrDef.findByPrimaryKey(transaction, new Key(headerKey));

    if (hdrEO != null)
    {
      throw new OAAttrValException(OAException.TYP_ENTITY_OBJECT,
                                   getEntityDef().getFullName(), // EO name
                                   getPrimaryKey(), // EO PK
                                   "HeaderId", // Attribute Name
                                   value, // Attribute value
                                   "ICX", // Message product short name
                                   "FWK_TBX_T_PO_ID_UNIQUE"); // Message name
    }
  }

  // Executes declarative validation, and finally sets the new value.
  setAttributeInternal(HEADERID, value);
} // end setHeaderId()
```

**不同的“Set”方法**

有多种方法可以设置实体变量的值。在编码中，通常调用set<AttributeName>()和setAttributeInternal()。查看Entity Object and View Object Attribute Setters获取更多的信息。

## 交叉属性校验
任何与两个个或更多属性值相关的校验应该被包含在validateEntity()方法中；不要将交叉属性校验放在单个属性的setter方法中，因为属性值的设置可能是无序的。

## 实体校验
当OA Framework在HTTP POST处理周期中设置实体对象值时，它总会校验它接触到的视图对象的行，它依次在下层的实体对象（一个或多个）上调用validateEntity()方法。而且，entities are validated again prior to posting (up to 10 times in a composition).

任何操作于行级的逻辑——且对被重复调用不是非常敏感的校验——应该被包含在validateEntity()方法中。

下面的PurchaseOrderHeaderEOImpl代码描述了实体级的校验：
```java
/**
 * Performs entity-level validation including cross-attribute validation that
 * is not appropriately performed in a single attribute setter.
 */
protected void validateEntity()
{
  super.validateEntity();
  
  // If our supplier value has changed, verify that the order is in an "IN_PROCESS"
  // or "REJECTED" state. Changes to the supplier in any other state are disallowed. 
  // Note that these checks for supplier and site are both performed here
  // because they are doing cross-attribute validation.

  String status = getStatusCode();

  if ((("APPROVED")Equals(status)) || ("COMPLETED"Equals(status)))
  {
    // Start by getting the original value and comparing it to the current
    // value. Changes at this point are invalid.
   
    Number oldSupplierId = (Number)getPostedAttribute(SUPPLIERID);
    Number currentSupplierId = getSupplierId();

    if (oldSupplierId.compareTo(currentSupplierId) != 0)
    {
      throw new OAAttrValException(OAException.TYP_ENTITY_OBJECT,
                                   getEntityDef().getFullName(), // EO name
                                   getPrimaryKey(), // EO PK
                                   "SupplierId", // Attribute Name
                                   currentSupplierId, // Attribute value
                                   "ICX", // Message product short name
                                   "FWK_TBX_T_PO_SUPPLIER_NOUPDATE"); // Message name
    }
    
    // If our supplier site has changed, verify that the order is in an "IN_PROCESS"
    // state. Changes to the supplier site in any other state are disallowed.
   
    Number oldSiteId = (Number)getPostedAttribute(SUPPLIERSITEID);
    Number currentSiteId = getSupplierSiteId();

    if (oldSiteId.compareTo(currentSiteId) != 0)
    {
      throw new OAAttrValException(OAException.TYP_ENTITY_OBJECT,
                                  getEntityDef().getFullName(), // EO name
                                  getPrimaryKey(), // EO PK
                                  "SupplierId", // Attribute Name
                                  currentSiteId, // Attribute value
                                  "ICX", // Message product short name
                                  "FWK_TBX_T_PO_SUPSITE_NOUPDATE"); // Message name
    }
  } 

  // Verify that our supplier site is valid for the supplier and make sure it is
  // an active "Purchasing" site.

  SupplierEntityExpert supplierExpert = 
    SupplierEOImpl.getSupplierEntityExpert(getOADBTransaction());

  if (!(supplierExpert.isSiteValidForPurchasing(getSupplierId(), getSupplierSiteId())))
  {
    throw new OAAttrValException(OAException.TYP_ENTITY_OBJECT,
                                 getEntityDef().getFullName(), // EO name
                                 getPrimaryKey(), // EO PK
                                 "SupplierSiteId", // Attribute Name
                                 getSupplierSiteId(), // Attribute value
                                 "ICX", // Message product short name
                                 "FWK_TBX_T_PO_SUPSITE_INVALID"); // Message name
  }
} // end validateEntity();
```

## 交叉实体校验
开发者经常认为他们需要实现“交叉实体（cross-entity）”校验，一个实体对象在校验中调用另一个的方法。在OA Framework中，“交叉实体校验”意味着某些非常特殊的东西：

 - 实体A和实体B在执行validateEntity()方法时各自己引用对方（因为实体A需要从实体B获得一些属性，实体B需要从实体A获得一些属性）and...

 - 期望两个对象都是“脏（dirty）”对象（需要校验）在同一个事务中and...

 - 另一个实体对象必须是有效的，以便引用它的对象获取属性值用于自己的校验。这样问题就来了：哪个实体应该先校验？

**技巧：** 对于复合关联的主／从实体对象这不是个问题，因为子对象将会先于父对象被校验，且BC4J Framework将校验复合层级结构向上10次的校验，从底部到顶部直到所有实体都是有效的。

需要“交叉实体校验”的环境是非常少见的。如果你觉得需要，解决的办法是创建一个特殊的“调停者”对象实现BC4J的ValidationListener接口。简单来说，这个对象交叉实体中的哪个对象的校验先执行。

## 不妥当的校验失败处理
在实体级的校验方法（validateEntity()，set<AttributeName>()或其它）中调用Transaction.rollback()，Transaction.clearEntityCache()执行回滚或清除BC4J缓冲的操作。如果因为某些原因需要执行这些操作，你必须按下面的方法在 **应用模块／事务级（application module/transaction level）** 捕获校验异常，并执行你需要的方法。比如，在应用模块级执行回滚是安全的；在实体级执行回滚或清理实体缓冲区却不是，并且可能导致不可预知的行为。
```java
Bad Code:
---------
protected void validateEntity()
{
  ...
  DBTransaction txn = getDBTransaction();

  // Do not issue a rollback from within the EO.
  txn.rollback();
  throw OAException(...);
}

Good Code:
----------
protected void validateEntity()
{
  ...
  throw OAException(...);
}

// The following logic is written at the application-module level.

try
{
  txn.commit();
}
catch (OAException e)
{
  // Cache the exception thrown by the validation logic in the EO, 
  // and perform the rollback.
  txn.rollback();
} 
```

# 删除
为了删除实体对象，可以在对应的视图对象上调用remove()方法，如下面的应用模块中的代码所示。
```java
/**
 * Deletes a purchase order from the PoSimpleSummaryVO using the
 * poHeaderId parameter.
 */
public Boolean delete(String poHeaderId)
{
  // First, we need to find the selected purchase order in our VO.
  // When we find it, we call remove( ) on the row which in turn
  // calls remove on the associated PurchaseOrderHeaderEOImpl object.
  int poToDelete = Integer.parseInt(poHeaderId);
   
  OAViewObject vo = getPoSimpleSummaryVO(); 
  PoSimpleSummaryVORowImpl row = null;

  // This tells us the number of rows that have been fetched in the
  // row set, and will not pull additional rows in like some of the
  // other "get count" methods.
  int fetchedRowCount = vo.getFetchedRowCount();
  boolean rowFound = false;

  // We use a separate iterator -- even though we could step through the
  // rows without it -- because we don't want to affect row currency.
  RowSetIterator deleteIter = vo.createRowSetIterator("deleteIter");

  if (fetchedRowCount > 0) 
  { 
    deleteIter.setRangeStart(0); 
    deleteIter.setRangeSize(fetchedRowCount); 
    for (int i = 0; i < fetchedRowCount; i++) 
    { 
      row = (PoSimpleSummaryVORowImpl)deleteIter.getRowAtRangeIndex(i); 

      // For performance reasons, we generate ViewRowImpls for all
      // View Objects. When we need to obtain an attribute value,
      // we use the named accessors instead of a generic String lookup.
   
      // Number primaryKey = (Number)row.getAttribute("HeaderId");
      Number primaryKey = row.getHeaderId();

      if (primaryKey.compareTo(poToDelete) == 0)
      {
        row.remove();
        rowFound = true;
        getTransaction().commit();
        break; // only one possible selected row in this case
      } 
    } 
  } 

  // Always close iterators.
  deleteIter.closeRowSetIterator(); 
  return new Boolean(rowFound);
} // end delete()
```

**校验和级联删除**

row.remove()方法依次调用下层实体对象的remove()方法。为实现特殊的删除行为，比如，检查删除操作是否被允许，或实现级联删除，应该在实体的remove()方法中添加代码，如下所描述的TooBox中的PurchaseOrderHeaderEOImpl。

**注意：** 由于Oracle Applications编码规范禁止使用数据库的级联删除功能。BC4J Framework需要我们手工为多层的purchase order业务对象实现自己的级联删除，每个实体对象在在执行super.remove()之前，先删除它自己的直接子对象。如下所示：
```java
/**
 * Marks all the lines for deletion, then mark the header for deletion.
 * You can delete a purchase order only if it is "In Process" or "Rejected."
 */
public void remove()
{
  String status = getStatusCode();
   
  if (("IN_PROCESS"Equals(status)) || ("REJECTED"Equals(status)))
  {

    // Note this is a good use of the header -> lines association since we
    // want to call remove( ) on each line.
    RowIterator linesIterator = getPurchaseOrderLineEO();

    if (linesIterator != null)
    {
      PurchaseOrderLineEOImpl line = null;
   
      while (linesIterator.hasNext())
      {
        line = (PurchaseOrderLineEOImpl)linesIterator.next();
        line.remove();
      }
    } 
    super.remove(); // Must be called last in this case.
  }
  else 
  {
    throw new OARowValException(OARowValException.TYP_ENTITY_OBJECT,
                                getEntityDef().getFullName(),
                                getPrimaryKey(),
                                "ICX", // Message product short name
                                "FWK_TBX_T_PO_NO_DELETE"); // Message name
  }
} // end remove()
```

# 锁
BC4J支持下面的锁技术：

 - 悲观锁 BC4J在执行setAttribute()方法时锁定实体对象对应的数据库行（在做出任何修改之前）。如果行已经被锁，BC4J将招聘一个AlreadyLockedException异常。这也是BC4J缺省的锁模式。

 - 乐观锁 BC4J在执行数据库post处理逻辑时锁定实体对象对应的数据库行。如果行已经被锁，BC4J将抛出AlreadyLockedException异常。

**注意：** OA Framework默认使用乐观锁并且推荐使用，由于连接池使传统的悲观锁不能实行。但是对于基于Form的应用是使用悲观锁的。

如果你需要悲观锁，你必须改变事务的行为：
```java
// In the application module...

OADBTransaction txn = getOADBTransaction();
txn.setLockingMode(Transaction.LOCK_PESSIMISTIC);
```

## 过期数据侦测
当BC4J锁定一行时，它试着决定行对象是否被其它用户删除或修改，因为它是为当前用户而查询的。

 - 如果行已经被删除了，BC4J抛出RowAlreadyDeletedException。

 - 如果行已经被修改，BC4J抛出RowInconsistentException。

为覆盖缺省的逐行比较的检测行为，可以在实体对象属性定义向导中使用属性级的Chage Indicator标志。如果某个属性的这个标志被选中，BC4J限制对这个属性的比较。Oracle Application PL/SQL API通常使用OBJECT_VERSION_NUMBER表列检查数据的改变，这列也可以影响实体对象。查看下面的Object Version Number Column。

# 提交
当准备提交实体对象的修改时，只要简单的从应用模块中调用getTransaction()Commit()。当调用这个方法时，你的对象被校验（如果需要），posted和committed。

 1. commit()方法调用oracle.apps.fnd.framework.OADBTransaction.validate()方法。

 2. validate()方法检查所有需要校验的根实体对象的“Validation Listener“。（在多个实体组成的复合对象，只有根实体对象被添加到Validation list）。校验完成后在commit前，它将不会存在于list中，因为当对象校验成功后，BC4J将会从validation list中移除它。

**技巧：** 也可以调用OADBTransaction.validate()方法在任何地方强制进行校验。它执行相同的功能。

 3. 对象位于validation list中，OADBTransaction validate()方法将调用实体的final viladate()方法，现依次调用validateEntity()执行你的校验逻辑。

**注意：** 在BC4J中对于list中各个实体的校验顺序是随机的。但是，在一个复合对象中，比如一个采购单有多个供货商。BC4J总是在校验父对象前校验子对象。BC4J只会将复合对象的根实体放入validation list中（子对象不会被包含进来）。当根实体对象调用super.validateEntity时，BC4J调用它的子对象的validate，直到遍历整个层级结构。由于这个原因，你应该在你的校验逻辑之前调用super.validateEntity以保证父对象在校验子对象后才校验自己。

 4. commit方法调用OADBTransaction postChanges方法。

 5. postChanges方法检查“Post Listener”获得实体对象中哪些数据需要被提交（posted）到数据库。

 6. 对于post list中的任何对象，OADBTransaction postChanges方法调用实体的postChanges方法。当对象被提交（posted），BC4J将它从post list中移除。

 7. 如果没有错误发生，数据库commit被发出，任何数据库锁被释放。

# 回滚
OA Framework为post和commit动作实现了一个“all or nothing“的事务处理方式。不管错误是否严重，如果数据库post或commit失败，OA Framework：

 - 发起JDBC rollback释放数据库锁。

**注意：** 这不会影响中间层的状态。

 - 恢复视图行对象的状态以便于事务发起第二次尝试。

**注意：** 这意味着你不需要显式的rollback失败的实体对象事务；OA Framework将在post或commit失败后自动显示出用户友好的错误信息。下面的例子描述了用户按下Apply按钮后commit和后来显示“Confirmation“对话框的情况。
```java
// In the root application module

public void apply()
{
  getTransaction()Commit();
} 

// In the controller
public void processFormData(OAPageContext pageContext, OAWebBean webBean)
{
  super.processFormRequest(webBean);

  // Handle the user pressing the "Apply" button
  if (pageContext.getParameter("Apply") != null)
  {
    OAApplicationModule am = pageContext.getRootApplicationModule();

    // No need for any special exception handling.  You can just display the
    // confirmation message because the OAF won't reach this code if the post/commit
    // fails.
    am.invokeMethod("apply");
    OAException confirmMessage = 
      new OAException("ICX", "FWK_TBX_T_SUPPLIER_CREATE_CONF", null,
                       OAException.CONFIRMATION, null);
    pageContext.putDialogMessage(confirmMessage);

  }
}
```

## 回滚方法
手工清除中间层视图对象和实体对象缓冲，可以从应用模块中调用getTransaction().rollback()。这也将roll back任何数据库修改并清除任何缓存于事务中的值。查找Support the Browser Back Button了解这对于创建实体对象的作用。

如果执行PL/SQL过程需要显式的roll back数据库而不影响中间层，可以在应用模块中调用getTransaction().executeCommand("rollback")。

**注意：** 如BC4J Native JDBC Statement Management中说过的。Transaction.rollback()会调用vo.clearCache()关闭相关的视图对象的JDBC结果集（游标）。比如，如果按下面的顺序执行：
```java
vo.executeQuery();
Transaction.rollback();
vo.next();
```
SQL异常“ORA-01002: fetch out of sequence”（这通常是由于在数据库中执行rollback使打开的cursors失效）将不会发生，因为Transaction.rollback()关闭了游标，强制vo.next()重新执行视图对象的查询并打开一个新的有效游标。

当Transaction.rollback() roll back 数据库状态和中间层业务对象状态，下层直接JDBC调用并不会有意识的rollback任何中间层业务对象的状态，因此不要关闭JDBC游标。

 i. Transaction.executeCommand("rollback")调用或

 ii. BC4J的“rollback to savepoint”数据库调用是在Transaction.postChanges()或Transaction.commit()方法调用时validation或post出错时，由内部发出的的。尽管实体对象或视图对象中用户修改的数据仍然存在，实体的post state已经变回modified state以便用户可以再次发起post/commit。

BC4J Framework不会补偿JDBC或数据库的rollback，无效的JDBC和数据库游标中的结果集（当数据库执行rollback调用后，游标被打开）。因此，如果你需要使用Transaction.executeCommand("rollback")，请先查看M52 model coding standards。

如果需要覆盖post处理或EntityImpl中的beforeCommid，请先参考下节不当的Post处理。

## 不当的Post处理
在下面的情况下避免调用executeQuery()：

 - 在视图对象的EntityImpl的post处理器方法（postChanges，beforePost，afterPost）中。

 - 在beforeCommit中并且随后试图在相同的视图对象中使用vo.next()，vo.first()等方法获取行。


未完成！！
