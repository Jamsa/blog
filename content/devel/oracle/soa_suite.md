Title: SOA Suite培训
Date: 2010-07-13
Modified: 2010-07-13
Category: devel
Tags: oracle,ebs

# 介绍
 - 配置EBS启用SOA Suite
 - Native interface开放为WebService接口
 - 通过ISG调用外部系统提供的WebService

# EBS的配置
Native Service Enablement Of EBS

参考Metalink Note:556540.1

# ISG的设置

# Native Interface开放为WebService

## 开放系统标准接口为WebService
通过“集成SOA网关”这个职责为标准接口授权、生成WSDL、部署或卸载WebService

## 开放自己开发的接口为WebService
通过Perl工具程序将自己的接口注册到Repository里



## 外部系统异步调用EBS发布的WebService

# ISG调用外部的WebService
不支持RPC格式的SOAP消息，只支持Document格式的。

## Business Event驱动对外部系统WebService的调用
 - Create/Use Invoker Event
  1. 选Workflow Administrator WebApplications职责
  2. 点击“Business Events”
  3. 点击“Create Event”
  4. 填写Name，Display Name和Description选择状态为“Enabled”
  5. 输入Owner Name和Tag（通常都填FND/FND）
  6. 点击“Apply”保存

 - Native Service Invocation Process
  1. Search Invoker Business Event.
  2. Select to view its subscriptions
  3. Click "Create Subscription"
  4. Enter local Subscriber System,Phase(<100 for synchronous response).
  5. Select Rule Data as "Message".
  6. Select Action Type "Invoke Web Service".
  7. Click "Next".
  8. Follow wizard based WSDL parser UI:
  9. Enter WSDL URL and click "Next".
  10. Select Service and click "Next".
  11. Select Service Port and click "Next".
  12. Select Service Operation and click "Next".
  13. Use seeded Java Rule Function - oracle.apps.fnd.wf.bes.WebServiceInvokerSubscription or custom extended class.
  14. Optionally enter WS Security parameters:WFBES_SOAP_USERNAME,WEBES_SOAP_PASSWORD_MOD,WEBES_SOAP_PASSWORD_KEY as 

 - Create Receive Event
  1. navigate to "Events" tab in Workflow 

## 自定义的Business Event驱动对外部系统的WebService的调用

## 直接调用外部的WebService

## 异步调用外部的WebService
由Create Subscription时的Phase决定，大于100时为异步调用

# 问题
 - 如何开放自己开发的接口为WebService

 - 与其它系统集成时如何解决人员、权限、登录等方面的问题

 - 没有BPEL的情况下（不能通过接口表和多次WebService调用处理）如何处理大数据量的问题

   通过接口表的方式，多次调用方法写入数据到接口表，再调用其它方法进行验证，然后再调用方法提交请求。

 - SOAP头的问题，如何在SOAP头设置相关的用户、职责等信息

 - AQ自动触发对外部系统WebService的调用，还是需要轮询AQ


异步调用时需要运行工作流background engine 的请求

测试WebService
http://www.ignyte.com/webservices/ignyte.whatsshowing.webservice/moviefunctions.asmx?wsdl
参数 88052 18




