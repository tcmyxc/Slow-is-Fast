## Java接口变化历史

1、jdk8 之前，接口的方法都是 `public abstract` 的，而且接口里面的数据字段都是静态常量

> 所以 jdk8 及以前，接口的修饰符可以不写，直接写返回值类型即可。因为都是 `public abstract` 
>
> 

2、jdk8 开始，接口的方法可以是 `default` 和 `static` 的

> `default` 方法意味着提供了默认的实现，但是实现类仍然可以重写该方法

3、jdk9 开始，接口的方法可以是 `private` 的

