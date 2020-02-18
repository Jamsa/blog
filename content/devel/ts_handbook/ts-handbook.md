Title: TypeScript Handbook笔记
Date: 2020-02-13
Modified: 2020-02-13
Category: 开发
Tags: typescript

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
 

