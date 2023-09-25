# Map相关面试题

## 1、HashMap的key和value是否可以为null？

可以，两者都可以为`null`值

`get`操作返回`null`二义性：无法区分是把key映射成了null，还是不存在这个key。可以通过`containsKey`辅助判断

## 2、ConcurrentHashMap的key和value是否可以为null？

两者都不可以为`null`

