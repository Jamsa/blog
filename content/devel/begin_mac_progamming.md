Title: Begin Mac Programming 笔记
Date: 2015-06-29
Modified: 2015-06-29
Category: 开发
Tags: objective-c,mac

# 关于对象

## Objective-C 中的对象类型

Mac中使用苹果公司的的Cocoa框架。在Xcode中创建类都继承于NSObject这个基类。

当我们在Objective-c中实例化一个对象后，它立即会发送一个消息来初始化自己。这个消息被称为`init`，它通设置初始值。

类定义包括`.h`和`.m`两个文件。

## `.h`文件结构：
```objc
//
//  NotifyingClass.h
//  TextApp
//
//  Created by Tim Isted on 08/09/2009.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//
#import <Cocoa/Cocoa.h>
@interface NotifyingClass : NSObject {

}
@end
```

在Objective-c中，使用某个类具有某个`public interface`来描述哪些消息能发送给这个类。`@interface`这一行的冒号后面指定这个类的父类，这里指向的是NSObject，它是Cocoa框架的基类。

`@interface`段中的大括号用于指定类的属性。

右大括号和`@end`间的内容用于指定类可以接收的消息。

定义Interface的语法结构如下：

```
@interface «nameOfClass» : «nameOfClassToInheritFrom» {
    «attribute information»
}

«list of messages responded to»

@end
```

## `.m`文件结构：

`.m`文件包含对象的实现。编写的方法放在`@implementation`和`@end`之间。

用于响应`init`消息的初始化方法默认会调用NSObject基类中的实现。通过查看`NSObject.h`可以找到它定义的初始化消息。

```objc
- (id)init;
```

## NSLog日志类
```objc
@implementation NotifyingClass

- (id)init {

    NSLog(@"Hello World! I'm a new NotifyingClass instance!");

    return self;
}

@end
```

# 消息机制


## 消息的定义：

```objc
- (id) init;
+ (id) allocWithZone: (NSZone *)zone;
«+ or -» («word») «messageName » «some optional bits »;
```
`+`或`-`用于标明它是一个类方法或是实例方法。`«word»`指定方法的返回类型。在`.h`中的方法签名列表中，可以看到使用`void`或`id`作为返回类型。

## Target-Action机制

某些由Cocoa框架提供的对象允许你为他们提供`target`对象和指定`action`——发送给这个对象的消息。比如，在Xcode的界面设计器中创建NSButton实例后，我们可以指定这个按钮被点击时调用NotifyingClass实例（`target`）的displaySomeText方法（`action`）。

如果消息名称的右边有冒号，表明它接收一个或多个参数。例如：

```objc
- (void)buildHouse:(House *)houseToBeBuilt;
```

括号中内容（House*）用于指定参数类型，括号后面是参数名称。

## 发送消息

方法调用：
```objc
- (IBAction)displaySomeText:(id)sender
{
    [textView insertText:@"displaySomeText just got called!\n"];
}
```

# 变量与内存

类似C的变量指针。


# 对象和内存管理

## 对象内存分配

NSObject提供了类方法`alloc`用于分配内存。永远不需要重载这个方法。

```objc
NSObject *someNewObject = [NSObject alloc];
```

这将分配一块足够容纳NSObject实例的内存并将这块内存的地址返回给someNewObject指针。`alloc`方法将所有实例变量设置为零或nil（指针类型），但它不会进行更进一步的『设置』。在使用对象前应该先初始化它的属性。

### 对象初始化

```objc
- (id)init{
    NSLog(@"Hello world~");
    return self;
``` 

应该在使用对象前对它的属性进行初始化，因此应该在分配内存后立即调用`init`方法。

我们应该合并内存分配和初始化代码：

```objc
NotifyingClass *myFavoriteNotifier = [[NotifyingClass alloc] init];
```

由于我们嵌套的调用了`alloc`和`init`方法，因此需要让`init`方法返回初始化后的对象地址，并传递给指针。

继承时的初始化：

```objc
- (id) init{
    [super init];
    return self;
	}
```

当从NSObject继承时，不需要调用父类的`init`方法，因为NSObject不做任何的初始化，`isa`实例变量是在`alloc`中设置的。考虑到后期有可能修改父类型，比较好的实践方法是始终调用`[super init]`。

## 在代码中创建对象

### 分配内存

```objc
- (IBAction)displaySomeText:(id)sender
{
    WonderfulNumber *myWonderfulNumber = [[WonderfulNumber alloc] init];

    float wonderfulValue = [myWonderfulNumber storedNumber];

    [textView insertText:[NSString
        stringWithFormat:@"My Wonderful Value = %f\n", wonderfulValue]];
}
```

上面的代码中存在问题，通过查看NSObject文档中关于『Creating, Copying, and Deallocating Objects.』相关的内容，能找到NSObject有```dealloc`方法。文档中指出，『永远不要直接发送`dealloc`消息』。应该使用"release" NSObject protocol方法。

当对象从内存中删除时它会接收到`dealloc`消息。

可以在类的`init`和`dealloc`中输出日志，查看释放情况。

```objc
@implementation WonderfulNumber
- (id)init {
    [super init];
    storedNumber = 42;
    NSLog(@"A WonderfulNumber object was initialized!");
    return self;
}
- (void)dealloc
{
    NSLog(@"A WonderfulNumber object was deallocated!");
    [super dealloc];
}
- (void)setStoredNumber:(float)newNumber
«code continues»
```

回到之前displaySomeText的代码。添加上述日志后，再执行时会发现`dealloc`中的日志未被输出。myWonderfulNumber未被释放，会产生内存泄漏。

因此，我们需要某种方法来标明某个对象不再需要使用，可以被释放掉。

***需要重申的是，苹果建议永远不要直接调用`dealloc`。***

## 对象的生命周期

### 引用计数

假设某个程序需要在屏幕上显示一个数字。当点击菜单上的一个选项时，会创建一个WonderfulNumber对象，并将它显示在窗口中。用户可以打开多个窗口，每次新窗口将显示WonderfulNumber中数字。当所有窗口都被关闭时WonderfulNumber对象才不再被需要。

我们可能需要在创建WonderfulNumber代码的结尾处调用`removeYourselfFromMemory`方法。但是问题是我们不知道它被多少个其它的对象所需要。

我们需要某种方法来跟踪有多少个对象对这个实例『感兴趣』。

#### 引用计数的介绍

Cocoa框架使用了『引用计数』来处理这个问题。这项技术允许对象声明它们对某个对象感兴趣或不再对它感兴趣。

如果objectA要声明它对objectB感兴趣，objectA向objectB发送`retain`。当objectA决定不再需要objectB时，它向objectB发送`release`。

引用计数是通过在每个对象上维护一个`retain count`来工作的。在对象上调用`retain`后，计数加1，调用`releas`后，计数减1。当对象的引用计数为0时，它将自动从内存中释放。

比如前面提到的每个新窗口都显示那个WonderfulNumber对象，这些窗口都retain这个WonderfulNumber对象。任何一个窗口关闭时，窗口都release对象。当所有窗口都关闭时，引用计数为0，WonderFulNumber对象被释放。

#### 内存分配后的引用计数

因为引用计数为0时，对象会被释放。因此在对象分配内存后，它的计数初始为1。当我们编写下面这行代码时：
```objc
WonderfulNumber *myWonderfulNumber = [[WonderfulNumber alloc] init];
```
它不只是为对象分配了内存，同样它声明了我们对这个对象感兴趣，因此我们不需要显式的retain这个对象。

从另一个角度来看，使用了`alloc`来创建对象，就表示我们『同意』对它『负责』。即我们同意当我们不需要使用它时会`release`它。

因此完整的代码应该是：

```objc
- (IBAction)displaySomeText:(id)sender
{
    WonderfulNumber *myWonderfulNumber = [[WonderfulNumber alloc] init];

    [myWonderfulNumber setStoredNumber:pi];
    float wonderfulValue = [myWonderfulNumber storedNumber];
    [textView insertText:[NSString
	    stringWithFormat:@"My Wonderful Value = %f\n", wonderfulValue]];
	
    [myWonderfulNumber release];
}

```

## 拒绝对内存管理负责


上节提到需要对创建的对象负责。但在某些情况下『对对象负责的责任』并不是非常清析。

比如，在类的方法中返回字符串指针时，这个类并不应该对字符串对象的最终释放负责。

例如：

```objc
- (NSString *)storedNumberAsString
{
    NSString *stringToReturn = [[NSString alloc]
                                     initWithFormat:@"%f", storedNumber];
    return stringToReturn;
}
```

这个方法分配并初始化了一个新的的字符串并在方法结束的地方返回了这个字符串。在这里应该要意识到我们分配了新的对象但是并没有释放它——我们没有对我们创建的对象完全负责。

如果我们在返回对象前使用`[stringToReturn relaase]`释放它，那么它会立即被释放掉，方法的返回值将是个无效的对象。

我们也不希望在其它使用了`storedNumberAsString`这类方法的地方使用`release`——除非我们调用了`alloc] init]`或`retain`，否则我们不需要调用`release`，例如：

```objc
{
    WonderfulNumber *myWonderfulNumber = [[WonderfulNumber alloc] init];
    [myWonderfulNumber setStoredNumber:pi];
    NSString *numberString = [myWonderfulNumber storedNumberAsString];
    «do something with numberString»
    [numberString release]; // Uh-oh!
}
```

上在的代码并不是个好主意，我们需要的效果是提供某种机制使得使用WonderfulNumber对象的人总是会释放他们通过`storedNumberAsString`所得到的字符串。

我们需要某种方法将对象传递到其它地方，明确的解除我们对它的内存管理『责任』。

### autorelease

Cocoa提供了`autoreleasing`机制来处理这种情况。

通过在对象上调用`autorelease`而不是`release`，我们可以将对象的`release`延时至下一个事件循环。即它在当前执行的代码上会一直存在。一旦程序代码执行完毕，应用程序等侍用户输入时，这个对象就会被`release`。如果此时它的引用计数为0，则它被释放。

完整代码如下：

```objc
//WonderfulNumber.m
- (NSString *)storedNumberAsString
{
    NSString *stringToReturn = [[NSString alloc]
                                     initWithFormat:@"%f", storedNumber];
    return [stringToReturn autorelease];
}

//NotifyingClass.m
- (IBAction)displaySomeText:(id)sender
{
    WonderfulNumber *myWonderfulNumber = [[WonderfulNumber alloc] init];
    [myWonderfulNumber setStoredNumber:pi];
    NSString *numberString = [myWonderfulNumber storedNumberAsString];
	[textView insertText:numberString];
    [myWonderfulNumber release];
}
```

这里在WonderfulNumber对象创建之后，我们创建了一个指向字符串对象的指针`numberString`，并把它插入了textViewer中。

我们只需要对`myWonderfulNumber`对象调用`release`，因为它是在这方法中唯一一个使用`alloc`分配出来的对象。当`displaySomeText`方法结束后，`numberString`指针将不再处于作用范围，由于这里是当前的事件响应代码的『最后一行』，因此这个由`storedNumberAsString`所返回的字符串对象将在随后被释放（下一事件循环）。

***我的思考：autorelease的运行方式：执行autorelease时标记在下一事件循环中，需要对该对象进行release。当进入下一次事件循环后，先对这一对象进行release，发现引用计数为0时，进行释放。这样也能保证在当前这次事件循环中`[textView insertText`执行时，对象仍然存在***


## 对象初始化参数

类似于NSString中的`initWithFormat`方法

通过提供支持参数的`init`方法来初始化对象的属性。

```objc
- (id)initWithNumber:(float)newNumber {
    [super init];
    storedNumber = newNumber;
    NSLog(@"Object was initialized!");
    return self;
}

```

这样我们就可以编写下面这样支持初始化参数的代码了：

```objc
- (IBAction)displaySomeText:(id)sender
{
    WonderfulNumber *myWonderfulNumber = [[WonderfulNumber alloc] initWithNumber:pi];
    NSString *numberString = [myWonderfulNumber storedNumberAsString];
    [textView insertText:numberString];
    [myWonderfulNumber release];
}
```

如何避免用户直接调用`[[WonderfulNumber alloc] init]`而不提供初始化参数呢？我们可以在`init`中提供某些默认值：

```objc
@implementation WonderfulNumber
- (id)init {
    return [self initWithNumber:42];
}
- (id)initWithNumber:(float)newNumber
«code continues»
```

## 工具类类方法

在NSString中定义了很多类方法，例如：

```objc
+ stringWithFormat:
+ localizedStringWithFormat:
+ stringWithCharacters:length:
+ stringWithString:
```

这此工具方法可以直接在NSString类上调用，它们会返回一个初始化过的对象。使用这些方法的好处在于它们的返回值都是`autorelease`的。这意味着你可以不使用`alloc`来创建NSString的实例而不需要对它调用`release`。因为这些方法返回的是一个已经构建好的对象，因此它们经常被称为`factory`方法。

因此我们可以用这个方法来简化我们的`storedNumberAsString`方法：

```objc
- (NSString *)storedNumberAsString
{
    NSString *stringToReturn = [NSString stringWithFormat:@"%f", storedNumber];
    return stringToReturn;
}
```

因为NSString的类方法返回的是一个已经`autorelease`的字符串对象，因此我们不需要在返回前再对它调用`autorelease`了。

### 编写自己的类工厂方法

遵循习惯性约定，工厂方法的命名一般按下面的格式：

```
«objectType»With«optional arguments:»
```

WonderfulNumber的工厂方法：

```objc

+ (id)wonderfulNumberWithFloat:(float)newNumber
{
    WonderfulNumber *numberToReturn = [[WonderfulNumber alloc]
                                             initWithNumber:newNumber];
    return [numberToReturn autorelease];
}
```

### 类方法中的`self`

考虑到将来WonderfulNumber类可能会存在子类型EvenMoreWonderfulNumber。子类型会继承父类型的方法，当调用`[EvenMoreWonderfulNumber wonderfulNumberWithFloat:55.4]时，它将会返回一个新的WonderfulNumber类型的对象，而不是EvenMoreWonderfulNumber类型的对象。

为了确保这个方法返回正确的类型我们需要将方法修改为：

```objc

+ (id)wonderfulNumberWithFloat:(float)newNumber
{
    id numberToReturn = [[self alloc] initWithNumber:newNumber]; return [numberToReturn autorelease];
}
```

类方法中的`self`关键字指向的是类本身，而不是类的实例。这里返回的类型是`id`类型的，工厂方法基本上都是返回这一类型，这是因为我们不希望在工厂方法中对类型进行硬编码。

### 何时使用`alloc`，何时使用工厂方法

到目前为止似乎总是应该使用工厂方法。

但是有时我们会需要一个对象在内存中保留一段时间，在当前事件循环结束后能继续存在。比如，A对象的某个实例变量指向了B对象，在A对象的生命周期中它都需要B对象存在。那么我们应该在A对象的`init`方法中使用B对象的`alloc] init]`方法来初始化它，并在A对象的`dealloc`方法中`release`这个实例。


# 集合

## 数组

Cocoa提供了`NSArray`类。它的常用初始化方法：

```objc
- initWithArray:
- initWithArray:copyItems:
- initWithContentsOfFile:
- initWithContentsOfURL:
- initWithObjects:
- initWithObjects:count:
//工厂方法
+ array
+ arrayWithArray:
+ arrayWithContentsOfFile:
+ arrayWithContentsOfURL:
+ arrayWithObject:
+ arrayWithObjects:
+ arrayWithObjects:count:
```

可以认为类方法只是调用实例方法并返回一个autorelease的数组。


### 向方法传递多个参数

例：

```objc
+ (void)personWithFirstName:(NSString *)firstName lastName:(NSString *)lastName;

Person *somebody = [Person personWithFirstName:@"Jane" lastName:@"Doe"];
```

上面这个工厂方法的名称为`personWithFirstName:lastName:`。

NSArray的`arrayWithObjects`可以接收多个参数，但它并不是`arrayWithObject1:object2:object3:`，因为它需要接收任意数量的对象。

Objective-C支持可变长度参数，只需要在调用时在最后一个参数的后面提供一个`nil`。

```objc
+ (id)arrayWithObjects:(id)firstObj, ...

NSString *firstObject = @"Milk";
NSString *secondObject = @"Eggs";
NSString *thirdObject = @"Butter";
NSArray *shoppingListArray =
    [NSArray arrayWithObjects:firstObject, secondObject, thirdObject, nil];

NSString *stringToOutput = [NSString stringWithFormat:@"shoppingListArray = %@",shoppingListArray];//%@用于显示数组

[textView insertText:stringToOutput];

 stringToOutput = [stringToOutput
           stringByAppendingString:[shoppingListArray
                                      componentsJoinedByString:@", "]];//拼接数组
[textView insertText:stringToOutput];

```

### 数组元素索引

```objc
stringToOutput = [stringToOutput
        stringByAppendingString:[shoppingListArray objectAtIndex:0]];//第二个元素
int indexOfObject = [shoppingListArray indexOfObject:secondObject];//元素索引
```

Objective-C中数组索引是从0开始的。

### 数组元素数量

```objc
int nmberOfItems = [shoppingListArray count];
```

## 对象可变性

NSString和NSArray都是不可变对象。

NSString类的`stringByAppendingString`不是修改已有的字符串，而是返回一个包含旧内容和新内容的字符串。

NSArray提供了类似的方法`arrayByAddingObject`。

### 可变的数组和字符串

如果一个对象是可变(`mutable`)的，则它的内容可以动态的修改。

Cocoa提供了多个可变类，它们是是基于不可变类型的。如：NSMutableString、NSMutableArray等。

NSMutableArray提供了额外的方法，如`addObject`或`insertObject:atIndex:`等可以在数组的中间位置插入新元素。也提供了对应的方法从数组中删除元素。

创建NSMutableArray对象：

```objc
NSMutableArray *changingArray = [NSMutableArray array];
// changingArray is currently an empty array
// calling [changingArray count] at this point would return 0
NSString *firstObject = @"The first string"; [changingArray addObject:firstObject];
NSString *secondObject = @"The second string"; [changingArray addObject:secondObject];
```

### 数组的效率

如果知道最终要保存在数组中的元素数量，我们可以使用`initWithCapacity`或`arrayWithCapacity`工厂方法来初始化数组。这样在存储元素时速度会更快。超出初始容量时，仍然可以存储，效率比在初始容量中存储差一些。

这是因为在没有能容纳所有元素的大块内存或我们在原始容量之外添加添加新元素时，数组对象会需要跟踪多个内存块来维护它所保存的对象指针。

### 修改数组元素内容

NSArray数组虽然是不可变的，但它的元素内容是可变的。

```objc
NSString *firstObject = @"Milk"; NSString *secondObject = @"Eggs";
NSArray *fixedArray = [NSArray arrayWithObjects:firstObject, secondObject, nil];
secondObject = @"Bread";
NSLog(@"Contents of Array = %@", fixedArray);
```

这段代码输出的内容是：

```
Contents of Array = (
    Milk,
Eggs )
```

而不是

```
Contents of Array = (
    Milk,
Bread )
```

这是因为数组会`retain`添加到其中的元素。当给`secondObject`重新赋值时，是让它指向一个新的内存地址，之前它与数组元素所指向的内存地址相同，重新赋值后，它指向了一个新地址，这对于数组里的内容没有影响。

如果我们在不可变数组中保存可变字符串，那么数组元素中的内容仍然是可以修改的：

```objc
NSMutableString *firstObject = [NSMutableString stringWithString:@"Milk"];
NSMutableString *secondObject = [NSMutableString stringWithString:@"Eggs"];
NSArray *fixedArray = [NSArray arrayWithObjects:firstObject, secondObject, nil];
[secondObject setString:@"Bread"];
NSLog(@"Contents of Array = %@", fixedArray);
```

将输出：

```objc
Contents of Array = (
    Milk,
Bread )
```

这种方式虽然可以修改数组元素的内容，但是并不能向数组中添加、删除元素。

### 字符串的高级特性

构建NSString时使用的`@"string"`格式与上面的代码是等效的：

```objc
NSString *string = [NSString stringWithCString:"this is a C string" encoding:«some encoding»];
```

### 添加数组元素

```objc
NSString *typedValue = [textField stringValue];
shoppingListArray = [shoppingListArray arrayByAddingObject:typedValue];
```

## 创建新应用
