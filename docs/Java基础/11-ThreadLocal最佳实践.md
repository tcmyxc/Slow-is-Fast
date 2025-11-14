# ThreadLocal最佳实践

1、使用完必须 `remove()`

ThreadLocalMap 的 key 是弱引用，value 却是强引用。如果不 remove()，value 会因为 key 被垃圾回收而成为 “陈旧 Entry（Stale Entry）”，会导致内存泄漏（尤其是大对象）

```java
ThreadLocal<List<String>> local = new ThreadLocal<>();

try {
    local.set(data);
    // do something
} finally {
    local.remove();   // 必须！
}

```



2、不要把大对象放进 ThreadLocal

ThreadLocal 最终是存在线程对象中的，线程不结束，数据就不会被释放。



3、使用 `ThreadLocal.withInitial()` 简化初始化逻辑

```java
ThreadLocal<DateFormat> df = ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));

```



4、尽量声明为 `static final` 

```java
private static final ThreadLocal<SimpleDateFormat> sdf =
        ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));

```

ThreadLocal 是 key，多实例会造成线程内 Map 存多条 Entry；static 让所有线程复用同一个 ThreadLocal“变量定义”，但数据仍然隔离

