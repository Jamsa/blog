Title: 使用PyQT开发巡更系统的总结
Date: 2016-04-16
Modified: 2017-01-16
Category: 开发
Tags: python,pyqt

# PyQT的内存管理模型：

`PyQT`中使用了两套内存管理模型，因此需要注意内存泄漏的问题。python对象会自动释放内存，但是Qt对象却不一定。Qt有自己的树状结构内存管理机制。每个Qt对象创建时，如果指定了parent（非继承结构上的父类，而是内存结构上）对象，则它是在父对象被销毁时才会被销毁。如果Qt对象创建时未指定父对象，则需要手动管理这个对象的销毁。这个销毁操作不能像销毁python对象一样使用del，而应该使用sip模块的delete方法。例如，在Python对象中包含Qt对象时，可以在`__del__`方法中处理Qt对象的销毁：

```python
class Job(object):
     def __init__(self):
          self.timer = QTimer()

     def __del__(self):
          sip.delete(self.timer)
```

# 线程模型：

在pyqt中使用Qt线程并不能避免GIL锁的问题。应该尽量使用Python线程来进行处理（我的实际使用中未遇到这类问题）。使用QThread有可能引发的问题：

[QThread的讨论链接](http://hgoldfish.com/blogs/article/80/)

尽量不要在非主线程使用QObject的对象。Qt的文档说，QObject与QThread有特别的关联。有以下几个注意事项：

1. 只有创建QObject的进程才能使用它。不能在一个线程里面创建QTimer，而在另外一个线程里面调用QTimer.start()。

2. 在一个线程里面创建的QObject不能在另外一个线程里面被销毁。

3. Qt的内存管理模型区别“父QObject”和“子QObject”。Qt要求“子QObject”必须和“父QObject”同一个线程。

很不幸的是，第2条和Python的GC有冲突。Python的GC不固定地在某个线程里面运行。如果刚好回收了一个不在当前线程里面创建的QObject，程序就有可能会崩溃。注：貌似PyQt的开发者提到会解决这个问题，不知道现在怎么样了。

# 信号/槽

PyQT  4.5以后的版本可以直接使用pyqtSignal和pyqtSlot来定义信号和槽。

pyqtSignal只能用于QObject的子类中。可以用pyqtSinagl产生的信号对象的connect方法将信号与槽连接起来。

pyqtSlot是一个decorator用于定义槽。
 
# PyQt中使用SQLDatabase连接sqlite3

使用过程中发现如果为tableView定义`QSqlQueryModel`，调用`QSqlQueryModel.setQuery`之后它会自动执行查询，不需要再执行`select`或`exec_()`方法，如果执行`exec_()`方法反而会导致锁库。

几个小技巧：

1\. 实现表格的实时刷新：通常要实现数据刷新需要调用QSqlQueryModel的setQuery方法重新执行查询。这个时候表格中选中的行或单元格会失去焦点。如果只是想根据内存中的数据实现实时的表格展现。可以通过在QSqlQueryModel的子类中添加定时器，该定时器定时产生QSqlQueryModel的layoutChanged信号。例：
```python
class TestQueryModel(QSqlQueryModel):
     def __init__(self,parent): 
        QSqlQueryModel.__init__(self,parent)
        self.db=QSqlDatabase.addDatabase("QSQLITE","MainTableModel")
        self.db.setDatabaseName(DB_FILE_NAME)
        self.db.open()
        self.setQuery(‘select …
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self.refreshTable)
     def refreshTable(self):
        self.layoutChanged.emit()
```

2\. 实现行变色或单元格变色：通过覆盖QSqlQueryModel中的data方法：
```python
   def data(self,index,role):
        if not index.isValid():
            return QVariant()
        elif role == Qt.BackgroundRole: # 变色
            if self.isRowTimeout(index):
                return QBrush(Qt.yellow)
            return QBrush()
            #if index.row() % 2 == 0:
            #    return QBrush(Qt.yellow)
            # delta = self.getDeltaSeconds(index)
            # if delta > 60: # 1分钟显示黄
            #     return QBrush(Qt.yellow)
            # else:
            #     return QBrush()
        elif role == Qt.DisplayRole: # 显示值
            variant = QSqlQueryModel.data(self,index,role) # 默认显示值
            if index.column()==6 and self.rpcServer:                          # 最后活动列
                delta = self.getDeltaSeconds(index)
                #return QVariant()
                if delta < 0:
                    return QVariant( u'未连接')
                elif delta > 0 and delta < 20:
                    return QVariant( u'在线')
                else:
                    return QVariant(u'离线')
            else:
                return variant
        elif role != Qt.DisplayRole:
            return QVariant()
        #return super(QSqlQueryModel,self).data(index,role)
        return QSqlQueryModel.data(self,index,role)
```

3\. 表头列名：通过覆盖QSqlQueryModel中的headerData方法：
```python
   header_labels = [u'主机识别码', u'别名',u'主机名', u'命令类型代码',u'命令类型', u'命令内容', u'超时',u'时间',u'是否定时',u'回应',u'回应时间',u'回应1',u'回应1时间']
   def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QSqlQueryModel.headerData(self,section, orientation, role)
```

# sqlite3相关

1\. ifnull、时间差、汉字的处理：
```python
sqlstr = "select t.client_id,h.name,h.host_name,t.command_type,case when t.command_type ='workCheck' then '"+u'巡查'+"' else '"+u'状态检查'+"' end as command_type_name,t.command_message,t.command_timeout,t.creation_time,case when ifnull(t.schedule_flag,'false')='true' then '"+u"是"+"' else '"+u"否"+"' end schedule_flag,t.reply_message,t.reply_time,t.reply1_message,t.reply1_time ,case when (strftime('%s',ifnull(t.reply_time,datetime('now','localtime'))) - strftime('%s',t.creation_time) - ifnull(t.command_timeout,"+str(globalConfig['timeout'])+"))>0 then '"+u'是'+"' else '"+u'否'+"' end as is_timeout from client_host_logs t,client_hosts h where t.client_id = h.id "
```

这里`datetime(‘now’,’localtime’)`，是用于当前时间的`localtime`表示，因为`datetime`默认取的是`utc`时间，而不是本地时间，这个sql中需要将它与`creation_time`和`reply_time`等字段进行计算，这两个字段中保存的都是本地时间，因此使用`datetime(‘now’)`取当前时间时需要传递`localtime`参数。

2\. QSqlDatabase的使用，`QSqlDatabase.database(dbname)`可以认为是创建数据库连接，不传`dbname`时认为是创建一个默认的连接。同一连接是会被复用的，如果不同的地方使用相同的`dbname`则认为会获取到同一个数据库连接进行操作。这时有可能会出现锁的情况。应该在不同的地方和线程中考虑使用不同的`dbname`，即不同的数据库连接来进行操作，防止出现锁表的问题。

# 使用pyinstaller打包pyqt程序

打包过程本身非常简单。如果程序需要uac权限运行，则需要在spec中指定uac信息，如：
```python
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='JKClient',
          debug=False,
          strip=False,
          upx=True,
          manifest='JKClient.exe.manifest',
          icon='res/icon.ico',
          console=False,
          uac_admin=True)
```

程序运行时目录下要有对应的manifest文件。

# 通过`_winreg`操作注册表

```python
def add_auto_run(valueName,absPath,addToMachineKey=False):
    """添加启动项"""
    pkey = _winreg.HKEY_CURRENT_USER
    if addToMachineKey:
        pkey = _winreg.HKEY_LOCAL_MACHINE

    try:
        key = _winreg.OpenKey(pkey, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run')
        (value, valuetype) = _winreg.QueryValueEx(key, valueName)
        if value == absPath:
            return
    except:
        pass
    key = _winreg.CreateKey(pkey,"Software\\Microsoft\\Windows\\CurrentVersion\\Run")
    _winreg.SetValueEx(key,valueName,0, _winreg.REG_SZ,absPath)
```

# 通过pywin32添加计划任务（win7）：

win7中有uac权限的程序无法通过添加注册表项进行启动。只能通过添加计划任务的方式进行启动。
代码如下：

```python
import win32com.client,sys
def add_schedule_run(valueName,absPath):
    """添加计划任务"""
    service = win32com.client.Dispatch('Schedule.Service')
    service.Connect()
    #service.getRunningTasks()
    rootFolder = service.GetFolder("\\")
    try:
        task = rootFolder.getTask(valueName)
        if task and task.Name == valueName:
            taskDef = task.Definition
            taskAction = taskDef.Actions[0]
            taskPath = taskAction.Path
            if taskPath == absPath:
                return
            else:               # 路径不同时删除原来的计划任务
                rootFolder.DeleteTask(valueName)
    except:
        pass                    # 任务不存在
    taskDef = service.NewTask(0)
    regInfo = taskDef.RegistrationInfo
    regInfo.Description = "JKClient"
    regInfo.Author = "JKClient"
    principal = taskDef.Principal
    principal.LogonType = 3     # 当任何用户登录时
    principal.RunLevel = 1      # 最高权限运行
    settings = taskDef.Settings
    settings.Enabled = True #启用
    settings.StartWhenAvailable = True
    settings.Hidden = False #If False, the task will be visible in the UI. The default is False.
    settings.MultipleInstances = 0 #单实例
    triggers = taskDef.Triggers
    trigger = triggers.Create(9) # TASK_TRIGGER_LOGON
    action = taskDef.Actions.Create(0) # 执行程序
    action.Path = absPath
    # 6：TASK_CREATE_OR_UPDATE，3：User must already be logged on. The task will be run only in an existing interactive session.
    rootFolder.RegisterTaskDefinition(valueName, taskDef, 6, None,None , 3)
```

该方法不能用于windowsxp。

# QString转Python str：

python2.7下需要对字符串进行转换。

```python
def qstr_to_utf8str(qt_str):
    """QString转utf8 str"""
    return str(qt_str.toUtf8())
```

# 多线程rpcServer:

```python
class ThreadingXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    def __init__(self,ip_port):
        SimpleXMLRPCServer.__init__(self,ip_port,allow_none=True)

class RPCServer(Thread):
    def __init__(self, ip, port):
        super(RPCServer, self).__init__()
        self.running = True
        self.server = ThreadingXMLRPCServer((ip, port))
        self.server.register_introspection_functions()
        self.server.register_function(self.updateClientState, "updateClientState")
        self.server.register_function(self.updateClientLog, "updateClientLog")
```

# PyQT加载国际化资源

Qt默认是支持国际化的，在PyQt安装好后也已经带了国际化资源，在模块目录下有pm资源文件。pyqt程序启动时如果不加载这些资源，那么默认情况下它是不会自动加载的。这会造成使用`QInputDialog.getText(self, u'发送指令', prompt_msg)`这类方法时，所产生的对话框等界面组件上出现“ok””cancel”，而不显示中文。

解决方法是直接从PyQt的资源路径上加载资源，或者从指定的目录上加载资源。

```python
     translator = QTranslator()
    #print(QLibraryInfo.location(QLibraryInfo.TranslationsPath)) #PyQt程序库所带的资源路径
    aa = translator.load("qt_zh_CN","./res”) #自定义的资源路径加载资源
    #translator.load("qt_zh_CN","c:/Python27/Lib/site-packages/PyQt4/translations")
    #print('##'+str(aa))
    app.installTranslator(translator)
```

当使用pyinstaller打包程序时，不会自动打包资源文件，因此应该像上面的代码一样把`PyQt/translations`目录下的资源复制到工程目录下。


c:\Python27\Scripts\pyinstaller.exe JKServer.spec
