# Java反射

## 反射定义

JAVA反射机制是在运行状态中，对于任意一个类，都能够知道这个类的所有属性和方法；对于任意一个对象，都能够调用它的任意方法和属性；这种动态获取信息以及动态调用对象方法的功能称为java语言的反射机制。

## 反射的作用

-   运行时分析类
-   运行时查看对象
-   编写泛型数组代码
-   利用`Method`对象的`invoke`方法调用任意方法
    -   `Method`对象是你想要的调用的方法的对象
    -   `invoke`方法调用包装在当前`Method`对象中的方法

## 反射相关类

### `Class`类

-   **所有反射 API 的入口点**
-   保存类的所有信息

-   没有 public 类型的构造器。

-   每个类都有一个 Class 类型的对象，当类被加载时，由 Java 虚拟机调用类加载器的 defineClass 方法构造

-   一个 Class 对象实际上表示的是一个类型，而这个类型不一定是类，比如 int 等基本类型不是类，但是 int.class 是一个 Class 类型的对象

#### 获取 Class类对象的三种方法

1、 `对象名.getClass()`

2、`Class.forName(className)`：调用 Class 类的 forName 静态方法

3、`T.class`：T 是任意的 Java 类型或 void 关键字

Class类常用方法

-   `getName()`：返回类的全限定名

-   静态方法 `forName(className)`：获取类名对应的 Class 对象
    -   className 必须是类名或者接口名，而且必须是全限定名

-   `newInstance()`：创建一个类的实例，调用的是无参构造函数，如果没有无参构造，会抛异常
-   `getFields`、`getMethods`、`getConstructors`：返回类的 publis 域，方法和构造器数组，包括父类的
-   `getDeclareFields`、`getDeclareMethods`、`getDeclareConstructors`：返回类的全部域，方法和构造器数组，但是不包括父类的

### `Field`、`Method`、`Constructor`类

查看对象域的关键方法是 `Field`类的各种 get 方法

设置域的值是`Field`类各种 set 方法，最常用的是`set(obj, value)`



**几个共有的方法：**

`getName()` 方法：返回项目的名称

`getModifier()`：返回一个整数值，代表不同的修饰符，结合`Modifier`类的静态方法`isPublic`等可以判断修饰符类型

`setAccessible()`：只需在括号里给个 true，就可以为所以为，想拿到哪个属性就拿哪个 

### `Modifier`类

有检测各种修饰符的方法，如`isPublic`等

## 使用反射编写泛型数组代码（扩展任意类型的数组）

1、获取数组的类对象

2、确认它是个数组

3、确定数组类型和长度

4、复制数组

```java
public static Object goodArrayCopyOf(Object a, int newLength){
    Class cl = a.getClass();
    if(!cl.isArray())  return null;
    Class componentType = cl.getComponentType();
    int length = Array.getLength(a);
    Object newArray = Array.newInstance(componentType, newLength);
    System.arraycopy(a, 0, newArray, 0, Math.min(length, newLength));
    return newArray;
}
```