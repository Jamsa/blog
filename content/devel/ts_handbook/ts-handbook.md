Title: TypeScript Handbook笔记
Date: 2020-02-13
Modified: 2020-02-13
Category: 开发
Tags: typescript

[toc]

# 基础类型

* 数字

与js一样ts中所有数字都是浮点，类型是`number`，除十进制、十六进制字面量外，还支持ES2015中的八进制和二进制字面量。

* 字符串 

支持反引号模板字符串。

* 数组

两种形式定义`T[]`和`Array<T>`。

* 元组

定义形式与数组类似，元素可以使用不同的数据类型。

```typescript
let x:[string, number];
x = ['hello', 10];
x[0] //下标从0开始
x[3] //越界访问会使用联合类型替代，但元素的类型只能为string或number
```

* any

用于处理动态内容和第三方的代码。

与`object`类型的区别在于`object`类型上无法调用方法，`any`类型可以。

* void

与`any`相反，表示没有任何类型。

用于函数时，表示没有返回值。用于变量时，只能赋值为`undefined`或`null`。

* undefined和null

是所有类型的子类。但在启用`--strictNullChecks`后，`null`和`undefined`只能赋值给自己或`void`。

* never

永不存在的类型。`never`是任何类型的子类，可以赋值给任何类型。但没有类型是`never`的子类中可以赋值给`never`。即使`any`也不能赋给`never`。

用于函数返回值时，表示函数总会抛出异常，或永远不返回。用于变量时，永远不为真的类型所约束。

* object

非原始类型。除`number`、`string`、`boolean`、`symbol`、`null`或`undefined`之外的类型。

* 类型断言

```typescript
let somestr = "hello";
let strlen1:number = (<string>somestr).length;
let strlen2:number = (somstr as string).length;
```
在tsx中只能使用`as`语法。

# 变量声明

## 变量

*  var存在的问题

`var`声明可以在包含它的函数、模块、命名空间或全局作用域内部的任何位置被访问。

* let声明

`let`使用的是词法作用域或块作用域。

`let`不允许重复定义，`var`是允许的。

嵌套作用域里引入同名定义会屏蔽外层的定义。

* const声明

与`let`类似，只是值不可改变。

## 解构

支持ES2015特性。

* 解构数组

```typescript
let [first, second] = [1,2];

//用于函数参数
function f([first, second]: [number, number]){
    console.log(first);
}

//剩余参数
let [first, ...rest] = [1,2,3,4];
```

* 解析对象

```typescript
let o = {
    a: "foo",
    b: 12,
    c: "bar
};
let {a, b} = o;

//剩余参数
let {a, ...passthrough} = o;

//默认值
let {a, b = 1001} = o;

//属性重命名
let {a: newName1, b: newName2} = o;
```

* 函数声明

```typescript
type C = {a:string, b?: number}

//参数解构及参数默认值
function f({a,b=0}: C):void {
    //...
}

```

## 展开

展开与解构相反。

展开仅包含自身可枚举属性，不包含对象实例中的方法。

TS当前版本不允许展开泛型函数上的类型参数。

# 接口

TypeScript的核心原则之一是对值所具有的结构进行类型检查。“鸭式辨型法”或“结构性子类型化”。

## 可选属性
属性名后添加`?`号。

## 只读属性
属性名前添加`readonly`标识。只读数组，可以使用`ReadonlyArray<T>`类型声明。

`readonly`和`const`的区别：作为变量用`const`，作为属性使用`readonly`。

## 额外的属性检查

TypeScript中传递额外参数给接口时，会因为参数名不匹配而被拒绝，这种情况下要通过以下三种方式才能绕开检查：

 * 类型断言

```typescript
interface SquareConfig {
    color?: string;
    width?: number;
}

function createSquare(config:SquareConfig):{color: string; area: number} {
    // ...
}

// 参数检查失败
// let mySquare = createSquare({colour: "red", width: 100});

let mySquare = createSquare({width: 100, opacity: 0.5} as SquareConfig);
```

 * 或者通过字符串索引签名
```typescript
interface SquareConfig{
    color?: string;
    width?: number;
    [propName: string]: any;
}
```

 * 赋值给另一个变量
 
 这种方式会导致下面的squareOptions不会经过额外属性检查。
 
 ```typescript
 let squareOptions = {colour: "red", width: 100};
 let mySquare = createSquare(squareOptions);
  ```

## 函数类型

接口可以描述函数类型。

```typescript
interface SearchFunc {
    (source: string, subString: string): boolean;
}

let mySearch: SerchFunction;
mySearch = function(source: string, subString: string){
    let result = source.search(subString);
    return result > -1;
}

```

## 可索引的类型

TypeScript支持两种索引签名：字符串和数字。可以同时使用，但是数字索引返回的值必须是字符串的索引返回值的子类型。因为用`number`检索时，会被转化为`string`再进行检索。

```typescript
class Animal{
    name: string;
}

class Dog extends Animal{
    breed: string;
}

interface Okay{
    [x: number]: Dog;
    [x: string]: Animal;
}
```

可以在索引前添加`readonly`，防止赋值。

字符串引声明了`obj.property`和`obj["property"]`这两种形式。

## 类类型

### 实现接口
与Java或C#中类实现接口的方式类似。

### 类静态部分与实现部分的区别
类有两个类型：静态部分类型和实例部分类型。

此部分官方文档描述并不明确，以下内容参考[这篇文章](https://juejin.im/post/5d217c8e518825701d6a4baf)。

实例类型通常是指通过类实例化出来的对象要满足的部分，如属性和方法。例：
```typescript
interface ClockInterface{
    currentTime: Date;
    setTime(d: Date);
}
```

静态部分类型：构造器就是静态类型，例：
```typescript
class Clock implements ClockInterface {
    currentTime: Date;
    setTime(d: Date) {
        this.currentTime = d;
    }
    constructor(h: number, m: number) { }
}
```
中的`constructor`。

当我们的类，去实现一个构造器的接口（静态类型的接口中的`new`方法）时，会报错。

即，类`不能`直接去实现静态部分的接口，但可以直接实现实例类型的接口。

```typescript
interface ClockConstructor{
    new (hour: number, minute: number);
}
class Clock implements ClockConstructor{
    currentTime: Date;
    constructor(h: number, m: number){}
}
```
这段代码报错是因为，类实现接口时，它实际上是对实例部分做类型检查，如上面的：`currentTime`属性。而构造器存在于类的静态部分，所以是不会做检查 。所以一个类相关的接口，就是实例部分的接口和构造器接口（静态部分接口）。

如果要对静态部分做检查，如何实现？

```typescript
// 静态部分接口
interface ClockConstructor {
    new (hour: number, minute: number): ClockInterface;
}
// 实例部分接口
interface ClockInterface {
    tick();
}

// 第一个参数ctor的类型是接口 ClockConstructor，在这里就为类的静态部分指定需要实现的接口
function createClock(ctor: ClockConstructor, hour: number, minute: number): ClockInterface {
    return new ctor(hour, minute);
}

class DigitalClock implements ClockInterface {
    constructor(h: number, m: number) { }
    tick() {
        console.log("beep beep");
    }
}
class AnalogClock implements ClockInterface {
    constructor(h: number, m: number) { }
    tick() {
        console.log("tick toc");
    }
}

let digital = createClock(DigitalClock, 12, 17);
let analog = createClock(AnalogClock, 7, 32);
```

## 继承接口

与类一样，接口可以互相继承。

## 混合类型

一个对象可以同时作为函数和对象使用。
```typescript
interface Counter {
    (start: number): string; //函数
    interval: number; //对象属性
    reset(): void; //方法
}

function getCounter(): Counter {
    let counter = <Counter>function (start: number) { };
    counter.interval = 123;
    counter.reset = function () { };
    return counter;
}

let c = getCounter();
c(10);
c.reset();
c.interval = 5.0;
```

## 接口继承类
接口继承类类型时，它会继承类的成员，但不包括其实现。接口同样会继承到类的`private`和`protected`成员。

# 类

## 类
与Java或C#中的类类似。

## 继承
可以用`super()`调用父类构造器。

## 公共、私有与受保护修饰符

 * `public` 为默认范围。
 * `private` 类型私有成员。
 * `protected` 类型及其子类型可访问。

即使两个实例中的`private`和`protected`属性的名称和数据类型都一致，它们也不会被认为是同一实例类型。

```typescript
class Animal {
    private name: string;
    constructor(theName: string) { this.name = theName; }
}

class Rhino extends Animal {
    constructor() { super("Rhino"); }
}

class Employee {
    private name: string;
    constructor(theName: string) { this.name = theName; }
}

let animal = new Animal("Goat");
let rhino = new Rhino();
let employee = new Employee("Bob");

animal = rhino;
animal = employee; // 错误: Animal 与 Employee 不兼容.
```

## readonly修饰符
可以将属性设置为只读。

## 参数属性
可以在构造函数中直接定义并初始化成员属性。参数属性通过给构造函数参数前面添加一个访问限定符来声明。如readonly、private、public和protected都可以。

## 存取器
使用`get`和`set`将属性改写为存取器。

存取器只支持ES5，不能降级至ES3。

## 静态属性
`static`创建类的静态成员。访问时需要通过类名进行访问。

## 抽象类
`abstract`关键字。可包含成员的实现细节。

## 高级技巧

### 构造函数

声明一个类的时候，声明了实例的类型和构造函数。

可以用变量保存类的或者说构造函数。
```typescript
class Greeter {
    greeting: string;
}

let greeterMaker: typeof Greeter = Greeter;

let greeter:Greeter = new greeterMaker();
```

### 把类当作接口使用
接口可以继承类。


# 函数
TypeScript中的函数可以创建有名字的函数和匿名函数。

## 函数类型
TypeScript能根据返回语句推断返回值类型，因此通常可以省略返回值。

函数的类型包含参数类型和返回值类型。参数类型匹配时，只检查参数类型，不检查参数名。

如果函数没有返回值，也必须指定返回值为`void`。

函数中使用的捕获变量不会体现在类型上。

TypeScript里每个函数参数都是必须的。编译器检查用户是否为每个参数都传入了值。即参
数个数必须与函数期望的参数个数一致。JavaScript里每个参数都是可选的。

## 可选参数和默认值
可选参数必须跟在必须参数的后面。

可以为参数定义默认值。带有默认值的必须参数都是可选的，与可选参数一样，在调用时可
省略。即：可选参数与末尾的默认参数共享参数类型。下面的两个函数
```typescript
function buildName(firstName: string, lastName?: string){
}
function buildName(firstName: string, lastName = "Smith"){
}
```
这两个函数共享同样的类型`(firstName: string, lastName?: string)=>string`。默认参
数的默认值消失了，只保留了它是一个可选参数的信息。两种函数的不同之处是，带默认值的参数不需要放在必须参数的后面。如果带默认值的参数出现在必须参数前面，用户必须明确传入`undefined`来获取默认值。

```typescript
function buildName(firstName = "Will", lastName: string) {
    return firstName + " " + lastName;
}

let result1 = buildName("Bob");                  // error, too few parameters
let result2 = buildName("Bob", "Adams", "Sr.");  // error, too many parameters
let result3 = buildName("Bob", "Adams");         // okay and returns "Bob Adams"
let result4 = buildName(undefined, "Adams");     // okay and returns "Will Adams"
```

## 剩余参数

在JavaScript里，可以使用`arguments`来访问所有传入的参数。

在TypeScript里，可以把所有参数收集到一个变量里。编译器创建参数数组，名字在省略号（`...`）后面给定的名字，可以在函数体内使用这个数组。
```typescript
function buildName(firstName: string, ...restOfName: string[]){}
```
## this

`this`的值在函数被调用的时候才会指定。可通过箭头函数在函数被创建时就绑定好正确的`this`。

### this参数
在箭头函数时使用`this`访问属性时，由于`this`是来自于字面量的函数表达式，得到的类型依旧会为`any`。修改的方法是为方法提供一个显示的`this`，这个参数是个假参数，它出现在参数列表的最前面。

```typescript
let deck: Deck = {
    suits: ["hearts", "spades", "clubs", "diamonds"],
    cards: Array(52),
    // NOTE: The function now explicitly specifies that its callee must be of type Deck
    createCardPicker: function(this: Deck) {
        return () => {
            let pickedCard = Math.floor(Math.random() * 52);
            let pickedSuit = Math.floor(pickedCard / 13);

            return {suit: this.suits[pickedSuit], card: pickedCard % 13};
        }
    }
}

let cardPicker = deck.createCardPicker();
let pickedCard = cardPicker();
```
这里`pickedCard`这种调用方式，函数内`this`的指向仍然是正确的。

### this参数在回调函数里

在回调函数里使用`this`时，为了让`this`能正确指向调用者。调用者提供的回调方法中，应将第一个参数指定为`this`。

 * todo: 侍补充

## 重载

为了让编译器能够正确的检查类型，它与JavaScript里的处理流程类似。它查找重载列表，尝试使用第一个重载定义。如果匹配的话就使用这个定义。因此，定义重载的时候，一定要把最精确的定义放在最前面。

# 泛型

## hello world
函数上的泛型参数并不一定要在调用时传入，也可以利用类型推断，编译器根据传入参数的类型自动确定泛型参数类型。

## 泛型变量
使用数组泛型变量时，可以直接调用泛型变量的方法。
 
## 泛型类型
可创建泛型接口、泛型函数接口、泛型类。但是无法创建泛型枚举和泛型命名空间。
```typescript
interface GenericIdentityFn{
    <T>(arg: T): T;
}
function identity<T>(arg: T): T {
    return arg;
}
let myIdentity: GenericIdentityFn = identity; 
let myIdentity1: GenericIdentityFn<number> = identity; 
```

## 泛型类
与泛型接口类似。但要注意类的两部分：静态部分和实例部分。泛型类指的是实例部分的类型，所以类的静态属性不能使用泛型类型。

## 泛型约束
可定义接口类型作为泛型参数的父类来约束泛型类型，或限定泛型类型必须具备的方法和属性。

在泛型约束中，通过类型参数间的引用关系来约束类型参数。如：Map的类型和Key类型间的约束关系。

泛型创建工厂中引用构造函数的类类型的方法：
```typescript
function create<T>(c: {new(): T;}): T{
    return new c();
}
```

# 枚举

枚举可以定义带名字的常量。

## 数字枚举

与其他编程语言的枚举类似，可指定成员的下标，不指定时下标值从0开始，下标值必须为常量。

## 字符串枚举

每个成员都必须用字符串字面量，或另外一个字符串枚举成员进行初始化。

## 异构枚举

可混合使用字符串和数字成员。不推荐使用。

## 计算和常量成员

枚举成员的值可以是常量或计算出来的。被当作常量：

 - 它是枚举的第一个成员且没有初始化，它的值会被设置为0。
 
 - 它不带有初始化器且它之前的枚举成员是一个数字常量。当前枚举成员为前一成员的值加1。
 
 - 成员使用`常量枚举表达式`初始化。它是TypeScript表达式的子集，可以在编译阶段求值。

## 联合枚举与成员的类型

当所有成员都拥有字面量值时，它就带有特殊的语义：

  - 枚举成员成为了类型，可以在定义类型时，指定某些成员只能是枚举成员的值。（固定值，不能初始化为其他值）
  
  - 枚举类型本身变成了每个枚举成员的`联合`。类型系统能知道枚举里的值的集合。能在进行比较值的时候，捕获所有条件都无法满足的情况。（因为编译器可以穷举所有成员，发现没有哪个枚举成员能满足条件）
  
## 运行时的枚举
  
枚举是在运行时真实存在的对象。

```typescript
enum E{
    X,Y,Z
}

function f(obj:{X: number}){
    return obj.X;
}

f(E)
```
这个调用可以成功，因为`E`有`number`型的数值属性`X`。

## 反向映射

用于从枚举值得到枚举名字。

```typescript
enum Enum{
    A
}
let a = Enum.A;
let nameOfA = Enum[a];//得到"A"
```
字符串枚举成员不会生成反向映射。

## const 枚举

`enum`前添加`const`，这类枚举不允许包含计算成员。

## 外部枚举

添加`declare`关键字，用来描述已经存在的枚举类型的形状。


# 类型推论

* 根据值类型推断。

* 不能根据值推断出的需要明确指定类型。

* 可根据上下文推断类型，比如：根据回调函数的签名，推断参数类型。


# 类型兼容性

类型兼容性是基于结构子类型的。结构类型是一种只使用其成员来描述类型的方式。与名义（nominal）类型形成对比，名义类型（Java/C#）是基于声明/类型名称来决定的。结构类型不要求明确的类型声明。

TypeScript类型系统允许某些在编译阶段无法确认其安全性的操作。

## 开始
基本规则：如果x要兼容y，y至少具有与x相同的属性（但是可以有多于x的属性）。

## 函数比较 
函数比较：函数x能否赋值给函数y，x的每个参数必须能在y里找到对应类型的参数，参数的名字是否相同无所谓，但是类型必须相同。y的参数多于x是允许的。

```typescript
let x = (a: number) => 0;
let y = (b: number, s: string) => 0;

y = x; // OK
x = y; // Error
```
允许`y=x`主要是因为JavaScript里允许忽略参数。

### 函数参数双向协变

当比较函数参数时，只有当源函数参数能够赋值给目标函数或者反过来时才能赋值成功。这是不稳定的，因为调用者可能传入了一个具有更精确类型信息的函数，但是调用这个传入的函数的时候却使用了不是那么精确的类型信息。

### 可选参数及剩余参数

比较函数时，可选参数与必须参数是可互换的。源类型上有额外的可选参数不是错误，目标类型的可选参数在源类型里没有对应的参数也不是错误。

当一个函数有剩余参数时，它被当做无限个可选参数。

### 函数重载

对于有重载的函数，源函数的每个重载都要在目标函数上找到对应的函数签名。这确保了目标函数可以在所有源函数可调用的地方调用。

## 枚举

枚举类型与数字类型兼容，数字类型与枚举类型歉。不同枚举类型间不兼容。

## 类

类与对象字面量和接口差不多，不同的是类的静态部分和实例部分。比较两个类类型的对象时，只有实例的成员会被比较。静态成员和构造函数不在比较的范围内。

### 类的私有和受保护成员

私有成员和受保护成员会影响兼容性。检查类实例兼容性时，如果目标类型包含一个私有成员，那么源类型必须包含来自同一个类的这个私有成员。这个规则同样适用于受保护成员。

## 泛型

TypeScript是结构性的类型系统，类型参数只影响使用其做为类型一部分的结果类型（传入泛型参数后的实例属性的类型）。

对于指定了泛型参数时，会比较泛型参数类型。没有指定泛型参数时，会把所有泛型参数当作`any`比较。然后用结果类型进行比较。


## 子类型与赋值

TypeScript里有两种兼容性：子类型和赋值。赋值扩展了子类型兼容性，增加了一些规则，允许和`any`来回赋值，以及`enum`和对应数字值之间的来回赋值。实际上类型兼容性是由赋值兼容性来控制的，即使在`implements`和`extends`语句也不例外。

# 高级类型

## 交叉与联合类型
交叉类型使用`&`，联合类型使用`|`。

## 类型区分和保护
如果想通过属性来判断是否为某种类型时，不能像JavaScript那样编写，会因为类型不确定而无法编译。应该先使用类型断言，再判断属性是否存在。
```typescript
let pet = getSmallPet();
if ((<Fish>pet).swim){
    (<Fish>pet).swim();
}else{
    (<Bird>pet).fly();
}
```

自定义`类型保护`，可以在运行期检查以保证某个作用域里的类型。要定义一个类型保护， 要简单的定义一个函数，它的返回值是一个`类型谓词`。
```typescript
function isFish(pet: Fish | Bird): pet is Fish {
    return (<Fish>pet).swim !== undefined;
}

if (isFish(pet)){
    pet.swim();
}else{
    pet.fly();
}
```
这里的`pet is Fish`就是`类型谓词`。在`if`分支里，TypeScript知道pet是`Fish`类型，在`else`里一定不是`Fish`。

`typeof`和`instanceof`都类型保护。`typeof`类型保护只能使用`!==`或`===`与`string`、`number`、`boolean`、`symbol`进行比较，但是TypeScript并不会阻止你与其它字符串比较，但是这种情况下语言不会将与这些字符串的比较识别为类型保护。`instanceof`的右边要求是一个构造函数。TypeScript将细化为：
 
    1. 此构造函数的`prototype`属性的类型，如果它不是`any`。
    
    1. 构造签名所返回的类型的联合
    
## 可以为null的类型

类检查器认为`null`和`undefined`可以赋值给任何类型。添加`--strictNullChecks`标记可以解决此错误：当声明一个变量时，它不会自动的包含`null`或`undefined`。也可以使用联合类型明确的包含它们。

## 可选参数和可选属性

添加了`--strictNullChecks`后，可选参数和可选属性会自动地加上`|undefined`。

## 类型保护和类型断言

可以像JavaScript里那样用`==null`排除`null`值，也可以用`||'default'`去除`null`值。当不能去除`null`或`undefined`时，可以在变量后添加`!`用`类型断言`方式去除。

## 类型别名

用`type`创建类型的别名。类型别名也可以是泛型的。类型别名可以在属性里引用自己，来定义嵌套结构。也可以与类型交叉一起使用，创建出奇怪的类型。

接口与类型别名的区别是，接口会创建新的类型名字，类型别名不创建新的类型名字。别名不能被`extends`和`implements`。

如果无法通过接口来描述一个类型，并且需要使用联合类型或元组类型，这时通常会使用别名。

## 字符串字面量类型

允许你指定字符串必须为固定的值。字符串字面量类型可以与联合类型、类型保护和类型别名很好的配合。例：
```typescript
type Easing = "ease-in"|"ease-out"|"ease-in-out";
```
字符串字面量还可以用于区分函数重载：
```typescript
function createElement(tagName: "img"): HTMLImageElement;
function createElement(tagName: "input"): HTMLInputElement;
// ... more overloads ...
function createElement(tagName: string): Element {
    // ... code goes here ...
}
```

## 数字字面量类型

较少使用。

## 枚举成员类型

枚举一节中提到过。

## 可辨识联合

特点：
    1. 具有普通的单例类型属性——可辨识的特征。kind属性
    1. 一个类型别名包含了那些类型的联合——联合。Shape
    1. 此属性上的类型保护。switch
    
```typescript
interface Square {
    kind: "square";
    size: number;
}
interface Rectangle {
    kind: "rectangle";
    width: number;
    height: number;
}
interface Circle {
    kind: "circle";
    radius: number;
}
type Shape = Square | Rectangle | Circle;
function area(s: Shape) {
    switch (s.kind) {
        case "square": return s.size * s.size;
        case "rectangle": return s.height * s.width;
        case "circle": return Math.PI * s.radius ** 2;
    }
}
```

### 完整性检查

当上例中的`Shape`中增加了新的类型后，如果想让TypeScript检查出`switch`中未完全覆盖，则需要做两个调整：

 1. 启用`--strictNullChecks`，如果不启用，遇到不匹配的类型时，将返回`undefined`。
 
 1. `area`增加明确的返回值类型，返回`undefined`就会变成非法。
 
 1. 使用`never`类型，在类型不匹配抛出异常。
 
```typescript

function assertNever(x: never): never {
    throw new Error("Unexpected object: " + x);
}
function area(s: Shape) {
    switch (s.kind) {
        case "square": return s.size * s.size;
        case "rectangle": return s.height * s.width;
        case "circle": return Math.PI * s.radius ** 2;
        default: return assertNever(s); // error here if there are missing cases
    }
}

```

## 多态的this类型

多态的`this`类型表示的是某个包含类或接口的`子类型`，这被称为`F-bounded`多态。它容易实现连贯接口间的继承，如：
```typescript
class BasicCalculator {
    public constructor(protected value: number = 0) { }
    public currentValue(): number {
        return this.value;
    }
    public add(operand: number): this {
        this.value += operand;
        return this;
    }
    public multiply(operand: number): this {
        this.value *= operand;
        return this;
    }
    // ... other operations go here ...
}

let v = new BasicCalculator(2)
            .multiply(5)
            .add(1)
            .currentValue();
```

返回类型是`this`，使用也继承也同样会有效。

## 索引类型

使用索引类型，编译器能检查使用动态性名的代码。常见于人对象中选取属性的子集。

```typescript
function pluck<T, K extends keyof T>(o: T, names: K[]): T[K][] {
  return names.map(n => o[n]);
}

interface Person {
    name: string;
    age: number;
}
let person: Person = {
    name: 'Jarid',
    age: 35
};
let strings: string[] = pluck(person, ['name']); // ok, string[]
```

`keyof T`是`索引类型查询操作符`。对任何类型`T`，`keyof T`的结果是`T`上已知公共属性名的联合。

`T[K]`是`索引说操作符`。

### 索引类型和字符串索引签名

```typescript
interface Map<T> {
    [key: string]: T;
}
let keys: keyof Map<number>; // string
let value: Map<number>['foo']; // number
```

## 映射类型

`类型映射`是TypeScript里提供的从旧类型创建新类型的方式。在映射类型里，新类型以相同的形式去转换旧类型里的每个属性。

将所一个类型的所有属性变成只读：
```typescript
type Readonly<T> = {
    readonly [P in keyof T]: T[P];
}
```

将属性变为可选属性：
```typescript
type Partial<T> = {
    [P in keyof T]?: T[P];
}
```

Nullable:
```typescript
type Nullable<T> = { [P in keyof T]: T[P] | null }
```

这些例子中属性列表是`keyof T`且结果类型是`T[P]`的变体。

映射类型的理解：
```typescript
type Keys = 'option1'|'options2';
type Flags = { K in Keys] : boolean};
```
等效于
```typescript
type Flags = {
    option1: boolean;
    option2: boolean;
}
```
我的理解：看起来像是整个大括号中的内容是一个联合类型。

属性代理：
```typescript
type Proxy<T> = {
    get(): T;
    set(value: T): void;
}

type Proxify<T> = {
    [P in keyof T]: Proxy<T[P]>;
}
function proxify<T>(o:T):Proxify<T>{
    //代理包装
}
let proxyProps = proxify(props);
```
将`T`的所有属性变成包含了`get`、`set`方法的代理类型。

标准库里的还有：
```typescript
type Pick<T, K extends keyof T> = {
    [P in K]: T[P];
}
type Record<K extends string, T> = {
    [P in K]: T;
}
```

`Readonly`、`Partial`、`Pick`是同态的，但是`Record`不是。`Record`并不需要输入类型来拷贝属性，所以它不属于同态：
```typescript
type ThreeStringProps = Record<'prop1' | 'prop2' | 'prop3', string>
```

非同态类型本质上会创建新的属性，因此它们不会从它处拷贝属性修饰符。（`readonly`等？）

### 由映射类型进行推断

包装类型的拆包：
```typescript
function unproxify<T>(t: Proxify<T>): T {
    let result = {} as T;
    for (const k in t) {
        result[k] = t[k].get();
    }
    return result;
}

let originalProps = unproxify(proxyProps);
```
拆包推断只适用于同态映射类型。

### 预定义的有条件类型

TypeScript 2.8的lib.d.ts里预定义的条件类型：

 - `Exclude<T, U>` 从T中剔除可赋值给U的类型。
 - `Extract<T, U>` 提取T中可以赋值给U的类型。
 - `NonNullable<T>` 从T中剔除null和undefined。
 - `ReturnType<T>` 获取函数返回值类型。
 - `InstanceType<T>` 获取构造函数类型的实例类型。



# Symbols

ES2015开始，`symbol`成为了原生类型。

`symbol`类型的值是通过`Symbol`构造函数创建的。

* 构造

```typescript
let sym1 = Symbol();
let sym2 = Symbol("key");
```

* 不可变且唯一

```typescript
let sym2 = Symbol("key");
let sym2 = Symbol("key");
sym2 === sym3; //false
```

* 作为对象属性的键
```typescript
let sym = Symbol();
let obj = {
    [sym]: "value"
};
obj[sym]; //"value"
```

* 与计算出的属性名声明相结合来声明对象的属性和类成员

```typescript
const getClassNameSymbol = Symbol();

class C {
    [getClassNameSymbol](){
        return "C";
    }
}
```

## 内置`symbols`

内置的`symbols`用来表示语言内啊的行为。在`Symbol`对象内定义。



# 迭代器和生成器

## 可迭代性

当一个对象实现了`Symbol.iterator`属性时，它就是可迭代的。

* `for..of`语句，遍历可迭代对象，调用对象上的`Symbol.iterator`方法。

* `for..of`和`for..in`的区别是`for..in`迭代的是键列表，而`for..of`迭代对象的键对应的值。`for..in`可操作任何对象。`for..of`关注于可迭代对象的值。

* 生成目标为ES5或ES3时，迭代器只允许在`Array`类型上使用。在非数组值上使用`for..of`语句会出错，即使这些非数组值实现了`Symbol.iterator`属性。

* 目标为兼容ES2015的引擎时，编译器会生成相应引擎的`for..of`内置迭代器实现方式。



# 模块

ES2015开始，JavaScript引入了模块概念，TypeScript沿用了这个概念。

模块在其自身作用域里执行，而不是在全局作用域里；即一个模块里的变量、函数、类等在模块外部是不可见的，除非你明确的使用`export`形式之一导出它们。如果要使用其他模块导出的变量、函数、类、接口等，你必须要导入它们，可以使用`import`形式之一。

模块是自声明的：两个模块之间的关系是通过在文件级别上使用`imports`和`exports`建立的。

模块使用模块加载器去导入其它模块。在支持时，模块加载器的作用是在执行此模块代码前查找和执行这个模块的所有依赖。

TypeScript与ES2015一样，任何包含顶级`import`和`export`的文件都被当成一个模块。相反地，如果一个文件不带有顶级的`import`或者`export`声明，那么它的内容被视为全局可见的（因此对模块也是可见的）。

## 导出

`export`关键字导出，`export { Aa as a}`可对导出重命名。

重新导出

```typescript
export {ZipCodeValidator as RegExpBasedZipCodeValidator} from "./ZipCodeValidator";
export * from "./StringValidator";
```

## 导入

`import`关键字导入，通过`as`对导入进行重命名。

`import * as aa from "./aa"`将整个模块导入到一个变量。

`import "./my-module.js";`有副作用的导入模块，这些模块会设置一些全局状态供其它模块使用，但是这些模块可能没有任何导出或用户不关注它的导出。

默认导出使用`default`标记，一个模块只能有一个。

## `export =`和`import = require()`

`export default`并不能兼容CommonJS和AMD的`exports`。TypeScript通过`export =`语法来支持CommonJS和AMD的exports。

`import zip = require('./ZipCodeValidator');`

## 生成模块代码

根据编译时指定的模块目标参数，编译器会生成相应的供Node.js(CommonJS、Require.js(AMD)、UMD、SystemJS或ES2015 native modules(ES6)模块加载系统使用的代码。`define`、`require`、`register`的意义需要参考相应模块加载器的文档。

## 可选的模块加载和其它高级加载场景

在不同模块加载系统下实现条件化加载。

## 使用其它JavaScript库

要描述TypeScript编写的库的类型时需要声明类库所暴露的API。

通常是在`.d.ts`文件里定义。作用类似`C/C++`中的`.h`文件。

## 创建模块结构指导

 - 尽可能在顶层导出
 
 - 如果仅导出单个`class`或`function`，使用`export default`
 
 - 如果要导出多个对象，把它们放在顶层里导出
 
 - 明确地列出导入的名字
 
 - 当你要导出大量内容的时候使用命名空间导入模式`import * as ... from `
 
 - 使用重新导出进行扩展
 
 - 模块里不要使用命名空间
 
模块结构上的危险信号：

 - 文件顶层声明是`export namespace Foo { ... }`，可删除`Foo`并把所有内容向上移一层。
 
 - 文件只有一个`export class`或者`export function`，可考虑使用`export default`。
 
 - 多个文件的顶层具有同样的`export namespace Foo {`，这些不会合并到同一个`Foo`中。



# 命名空间

使用`namespace`代替原来的`module`。

使用`namespace`将相关的类型放在同一命名空间里。通过`export`导出。

把`namespace`分割成多个文件时。它们仍然是同一个命名空间，使用的时候就如同它们在同一个文件中定义的一样。因为不同文件间存在依赖关系，所以我们需要加入引用标签（`/// <reference path="Validation.ts" />`）来告诉编译器文件之间的关联。

涉及多个文件时，我们必须确保所有编译后的代码都被加载。有两种方式实现：

 - `tsc --outFile`将多个输入文件编译为一个输出文件。
 
 - 将每个文件编译为单独的文件，通过`<script>`标签按正确的顺序引进来。
 
使用`import q = x.y.z`可以给命名空间取别名。这个语法与`import x = require('name')`语法是不同的。

使用`.d.ts`声明上部程序库的命名空间。


# 命名空间和模块

命名空间和模块不同的是，模块可以声明它的依赖。

`Node.js`默认并推荐使用模块组织代码。ES2015中模块是语言内置的部分。

推荐使用模块作为组织代码的方式。

## 命名空间和模块的陷阱

 - 对模块使用`/// <reference>`
 
 - 使用不必要的命名空间，比如导入了`namespace`，使用的时候需要增加额外`.`来引用命名空间内的类型。
 
## 模块的取舍

TypeScript里模块文件与生成的JS文件是一一对应的。模拟目标模块化系统的不同，可能会导致无法连接多个模块源文件。



# 模块解析

模块解析是指编译器在查找导入模块内容时所遵循的流程。

## 相对 vs 非相对模块导入

相对导入是以`/`、`./`或`../`开头的。

其它形式的导入被当作非相对导入，如：

 - `import * as $ from "jQuery";`
 
 - `import { Component } from "@angular/core";`
 
相对导入在解析时是相对于导入它的文件，并且不能解析为一个外部模块声明。

非相对模块的导入可以相对于`baseUrl`或者通过路径映射来进行解析。它们还可以被解析成外部模块声明。使用非相对路径来导入你的外部依赖。

## 模块解析策略

两种：`Node`和`Classic`。可使用`--moduleResolution`标记来指定。未指定时，`--module AMD | System | ES2015`时的默认值为`Classic`，其它情况时则为`Node`。`Classic`是以前TypeScript的默认解析策略，现在还存在只是为了向后兼容。Node是模仿`Node.js`的模块解析机制。

## 附加的模块解析标记

在`tsconfig.json`里进行配置，主要有以下几种配置

 - Base URL
 
 - 路径映射
 
 - 利用`rootDirs`指定虚拟目录
 
## 跟踪模块解析
 
 当模块没有被解析时，可通过`--traceResolution`启用编译器的模块解析跟踪，它会告诉我们在模块解析过程中发生了什么。
 
## 使用`--noResolve`
 
 这个编译选项告诉编译器不要添加任何不是在命令行传入的文件到编译列表。
 



# 声明合并

编译器将针对同一个名字的两个独立声明合并为单一声明。合并后的声明同时拥有原先两个声明的特征。任何数量的声明都可以被合并；不限于两个声明。

## 基础概念

TypeScript中的声明会创建以下三种实体之一：命名空间、类型或值。创建命名空间的声明会新建一个命名空间，它包含了用点符号来访问时使用的名字。创建类型的声明是用声明的模型创建一个类型并绑定到给定的名字上。创建值的声明会创建在JavaScript输出中看得到的值。

## 合并接口

合并的机制就是把双方的成员放到一个同名的接口里。

两个接口中声明了同名的非函数成员且它们的类型不同时，编译器会报错。

每个同名函数成员都会被当成这个函数的一个重载。需要注意的是后面定义的接口具备更高的优先级。例外的情况是当出现特殊的函数签名时（签名里有一个参数的类型是单一的字符串字面量），它将会被提升到重载列表的最顶端。

```typescript
interface Document {
    createElement(tagName: any): Element;
}
interface Document {
    createElement(tagName: "div"): HTMLDivElement;
    createElement(tagName: "span"): HTMLSpanElement;
}
interface Document {
    createElement(tagName: string): HTMLElement;
    createElement(tagName: "canvas"): HTMLCanvasElement;
}
//合并后
interface Document {
    createElement(tagName: "canvas"): HTMLCanvasElement; //特殊函数
    createElement(tagName: "div"): HTMLDivElement; //同一段定义的先定义的优先级高
    createElement(tagName: "span"): HTMLSpanElement;
    createElement(tagName: string): HTMLElement; //后定义
    createElement(tagName: any): Element; //最先定义
}
```

## 合并命名空间

同名命名空间也会合并其成员。命名空间会创建出命名空间和值，两者合并规则不同。

命名空间合并时，模块导出的同名接口进行合并，构成单一命名空间内含合并后的接口。

命名空间里值的合并：如果当前已经存在给定名字的命名空间，那么后来的命名空间的导出成员会被加到已经存在的那个模块里。

非导出成员仅在其原有的（合并前的）命名空间内可见。即，合并之后，从其它命名空间合并进来的成员无法访问非导出成员。

## 命名空间与类和函数和枚举类型合并

命名空间可以与其它类型的声明进行合并。只要命名空间的定义符合将要合并类型的定义。合并结果包含两者的声明类型。TypeScript使用这个功能去实现一些JavaScript里的设计模式。

### 合并命名空间和类

```typescript
class Album {
    label: Album.AlbumLabel;
}
namespace Album {
    export class AlbumLabel { }
}
```

上面代码合并的结果是一个类并且带有一个内部类。也可以使用命名空间为类增加一些静态属性。

命名空和函数合并：

```typescript
function buildLabel(name: string): string {
    return buildLabel.prefix + name + buildLabel.suffix;
}

namespace buildLabel {
    export let suffix = "";
    export let prefix = "Hello, ";
}

console.log(buildLabel("Sam Smith"));
```

命名空间和枚举合并：

```typescript
enum Color {
    red = 1,
    green = 2,
    blue = 4
}

namespace Color {
    export function mixColor(colorName: string) {
        if (colorName == "yellow") {
            return Color.red + Color.green;
        }
        else if (colorName == "white") {
            return Color.red + Color.green + Color.blue;
        }
        else if (colorName == "magenta") {
            return Color.red + Color.blue;
        }
        else if (colorName == "cyan") {
            return Color.green + Color.blue;
        }
    }
}
```

## 非法的合并

类不能与其它类或变量合并。

## 模块扩展

与JS可通过修改类型的`prototype`来扩展，TypeScript也可以采用这种方式。

## 全局扩展

可以通过`declare global`的方式在模块内部添加声明到全局作用域中。



# JSX

TypeScript支持内嵌，类型检查以及将JSX直接编译为JavaScript。

TypeScript具有三种JSX模式：`preserve`, `react`和`react-native`。这些模式只在代码生成阶段起作用，类型检查并不受影响。可以在命令行使用`--jsx`来指定模式。

## as操作符

在`.tsx`文件里禁用使用尖括号的类型断言，只能使用`as`操作符。

## 类型检查

JSX的类型检查是区分固有元素与基于值的元素的，区别对侍的原因有两点：

 - 对于React，固有元素会生成字符串（React.createElement("div")），而自定义组件不会生成（React.createElement(MyComponent）。
 
 - 传入JSX元素里的属性类型的查找方式不同。固有元素本身就支持，自定义的组件会自己指定它们具有哪些属性。

### 固有元素

固有元素使用特殊的接口`JSX.IntrinsicElements`来查找。默认地，如果这个接口没有指定，会全部通过，不对固有元素进行类型检查。然而，如果这个接口存在，那么固有元素的名字需要在`JSX.IntrinsicElements`接口的属性里查找。如：

```typescript
declare namespace JSX {
    interface IntrinsicElements {
        foo: any
    }
}

<foo />; // 正确
<bar />; // 错误
```
也可以在`JSX.IntrinsicElements`上指定一个用来捕获所有字符串的索引类型。

### 基于值的元素

根据作用域里按标识符查找组件定义，基于值的元素有两种：无状态函数组件（SFC）和类组件。

由于两者在JSX表达式里无法区分，因此TypeScript会先尝试将表达式做为无状态函数组件进行解析，如果失败再尝试以类组件的形式进行解析。如果依旧失败就输出错误。

#### 无状态函数组件

它的第一个参数是`props`对象。TypeScript会强制它的返回值可以赋值给`JSX.Element`。由于这种组件是函数，还可以利用函数重载。

#### 类组件

元素的类型和元素实例类型是两个不同的概念。以`<Expr />`为例，元素类的类型为`Expr`类型。如果`MyComponent`是ES6的类，那么类类型就是类的构造函数和静态部分。如果`MyComponent`是一个工厂函数，类类型为这个函数。

一旦建立起了类类型，实例类型由类构造器或调用签名（如果存在的话）的返回值的联合构成。在ES6类的情况下，实例类型为这个类的实例的类型，并且如果是工厂函数，实例类型为这个函数返回值类型。

元素的实例类型必须赋值给`JSX.ElementClass`。默认的`JSX.ElementClas`为`{}`，但是可以被扩展来限制JSX的类型以符合相应的接口。

### 属性类型检查

对固有元素，这是`JSX.IntrinsicElements`属性的类型。

基于值的元素，稍复杂些。它取决于先前确定在元素实例类型上的某个属性的类型。至于该使用哪个属性来确定类型取决于`JSX.ElementAttributesProperty`。它应该使用单一的属性来定义。

元素属性类型用于在JSX里进行属性的类型检查，支持可选和必须属性。JSX还会使用`JSX.IntrinsicAttributes`接口来指定额外的属性，这些额外的属性通常不会被组件的`props`或`arguments`使用——如React里的`key`。在React里，它用来允许`Ref<T>`类型的`ref`属性。通常来讲，这些接口上的所有属性都是可选的，除非你想要用户在每个JSX标签上都提供一些属性。

### 子孙类型检查

此部分未完成，文档描述不清晰。




# 装饰器

能被附加到类声明、方法、访问符、属性或参数上。使用`@expression`这种形式，`expression`求值后必须为一个函数，它会在运行时被调用，被装饰的声明信息作为参数传入。

## 装饰器工厂

它是一个函数，返回一个表达式（函数），供装饰器在运行时调用。即，普通装饰器用`@sealed`，装饰器工厂使用`@value('arg')`形式，`value`是一个返回装饰器函数的工厂函数。

## 装饰器组合

多个装饰器可书写在同一行或多行上。多个装饰器用于一个声明上时，求值方式与复合函数的相似：

 1. 由上至下（左至右）依次对装饰器表达式求值。（调用工厂方法获得装饰器函数）
 
 1. 求值的结果会被当作函数，由下至上（右至左）依次调用。（执行装饰器函数）
 
## 装饰器求值

类中不同声明的装饰器按以下规定的顺序应用：

 1. 参数装饰器-方法装饰器-访问符装饰器或属性装饰器应用到每个实例成员。
 
 1. 参数装饰器-方法装饰器-访问符装饰器或属性装饰器应用到每个静态成员。
 
 1. 参数装饰器应用到构造函数。
 
 1. 类装饰器应用到类。
 
## 类装饰器

类装饰器应用于类构造函数，可以来监视、修改或替换类定义。

它在运行时被当作函数调用，类的构造函数作为其唯一的参数。

如果类装饰器返回一个值，它会使用提供的构造函数来替换类的声明。

```typescript
function classDecorator<T extends {new(...args:any[]):{}}>(constructor:T) {
    return class extends constructor {
        newProperty = "new property";
        hello = "override";
    }
}

@classDecorator
class Greeter {
    property = "property";
    hello: string;
    constructor(m: string) {
        this.hello = m;
    }
}

console.log(new Greeter("world"));
```

## 方法装饰器

它会被应用到方法的属性描述符上，可以用来监视、修改或者替换方法定义。

它在运行时被调用，传入3个参数：

 1. 对于静态成员来说是类的构造函数，对于实例成员是类的原型对象。
 
 1. 成员的名字。
 
 1. 成员的属性描述符。
 
输出目标版本小于ES5时，属性描述符会是`undefined`。

## 访问器装饰器

声明在一个访问器的声明之前（紧靠着访问器声明）。访问器装饰应用于访问器的属性描述符并且可以用来监视、修改或替换一个访问器的定义。

TypeScript不允许同时装饰一个成员的`get`和`set`访问器。取而代之的是，一个成员的所有装饰器必须应用在文档顺序的第一个访问器上。这是因为，在装饰器应用于一个属性描述符时，它联合了`get`和`set`访问器，而不是分开声明的。

访问器装饰器表达式在运行时当作函数被调用，传入下列3个参数：

 1. 对于静态成员来说是类的构造函数，对于实例成员是类的原型对象。
 
 1. 成员的名字
 
 1. 成员的属性描述符
 
如果访问器装饰器返回一个值，它会被用作方法的属性描述符。

如果代码输出目标版本小于ES5返回值会被忽略。

## 属性装饰器

声明在属性声明之前。在运行时被调用，传入2个参数：

 1. 对于静态成员来说是类的构造函数，对于实例成员是类的原型对象。
 
 1. 成员的名字
 

## 参数装饰器

声明在参数声明之前。参数装饰器应用于类构造函数或方法声明。

在运行是当作函数被调用，传入3个参数：

 1. 对于静态成员来说是类的构造函数，对于实例成员是类的原型对象。
 
 1. 成员的名字。
 
 1. 参数在函数参数列表中的索引。
 
参数装饰器的返回值会被忽略。

## 元数据
`reflect-metadata`库来支持实验性的metadata API。



# Mixins

例：
```typescript
// Disposable Mixin
class Disposable {
    isDisposed: boolean;
    dispose() {
        this.isDisposed = true;
    }

}

// Activatable Mixin
class Activatable {
    isActive: boolean;
    activate() {
        this.isActive = true;
    }
    deactivate() {
        this.isActive = false;
    }
}

class SmartObject implements Disposable, Activatable {
    constructor() {
        setInterval(() => console.log(this.isActive + " : " + this.isDisposed), 500);
    }

    interact() {
        this.activate();
    }

    // Disposable
    isDisposed: boolean = false;
    dispose: () => void;
    // Activatable
    isActive: boolean = false;
    activate: () => void;
    deactivate: () => void;
}
applyMixins(SmartObject, [Disposable, Activatable]);

let smartObj = new SmartObject();
setTimeout(() => smartObj.interact(), 1000);

////////////////////////////////////////
// In your runtime library somewhere
////////////////////////////////////////
function applyMixins(derivedCtor: any, baseCtors: any[]) {
    baseCtors.forEach(baseCtor => {
        Object.getOwnPropertyNames(baseCtor.prototype).forEach(name => {
            derivedCtor.prototype[name] = baseCtor.prototype[name];
        });
    });
}
```

`applyMixins`函数将所有属性，复制到目标上去。




# 三斜线指令

包含单个XML标签的单行注释。注释的内容会做为编译器指令使用。

三斜线指令仅可放在包含它的文件的最顶端。一个三斜线指令的前面只能出现单行或多行注释，这包括其它三斜线指令。如果它们出现在一个语句或声明之后，它们会被当作普通的单行注释。

