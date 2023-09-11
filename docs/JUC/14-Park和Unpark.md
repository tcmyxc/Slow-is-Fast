# Park 和 Unpark

## 基本使用

park 和 unpark 是 LockSupport 类中的**静态**方法

```java
// 暂停当前线程
LockSupport.park();

// 恢复某个线程的运行
LockSupport.unpark();
```

示例：

```java
public class TestParkUnpark {

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(() -> {
            try {
                System.out.println("开始执行...");
                Thread.sleep(1000);
                System.out.println("park...");
                LockSupport.park();
                System.out.println("从 park 处继续执行...");
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }, "t1");
        t1.start();
        Thread.sleep(3000);
        System.out.println("unpark...");
        LockSupport.unpark(t1);
    }
}
```

```tex
14:07:48.762 [t1] INFO com.tcmyxc.juc.TestParkUnpark - 开始执行...
14:07:49.781 [t1] INFO com.tcmyxc.juc.TestParkUnpark - park...
14:07:51.770 [main] INFO com.tcmyxc.juc.TestParkUnpark - unpark...
14:07:51.770 [t1] INFO com.tcmyxc.juc.TestParkUnpark - 从 park 处继续执行...
```

park 之后的线程状态是 wait

如果先调用 unpark，再调用 park，那就会直接往下面执行（相当于运行需要满足一定的条件，调用的时候发现已经满足了，那就直接接着运行）

示例：

```java
public static void main(String[] args) throws InterruptedException {
    Thread t1 = new Thread(() -> {
        try {
            log.info("开始执行...");
            Thread.sleep(3000);
            log.info("park...");
            LockSupport.park();
            log.info("从 park 处继续执行...");
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }, "t1");
    t1.start();
    Thread.sleep(1000);
    log.info("unpark...");
    LockSupport.unpark(t1);// 主线程先 unpark
}
```

```tex
14:18:53.385 [t1] INFO com.tcmyxc.juc.TestParkUnpark - 开始执行...
14:18:54.384 [main] INFO com.tcmyxc.juc.TestParkUnpark - unpark...
14:18:56.390 [t1] INFO com.tcmyxc.juc.TestParkUnpark - park...
14:18:56.390 [t1] INFO com.tcmyxc.juc.TestParkUnpark - 从 park 处继续执行...
```

## 特点

- park & unpark 是以线程为单位来阻塞和唤醒线程的，精确到了具体的线程
- unpark 可以先于 park 使用

## 原理

每个线程都有自己的一个 Parker 对象，由三部分组成 `_counter`，`_cond` 和 `_mutex`

线程就像一个旅行者，Parker 就像他随身携带的背包，条件变量 `_mutex` 就好比背包中的帐篷。`_counter` 就好比背包中的备用干粮（0为耗尽，1为充足)

调用park就是累了吃备用干粮。如果备用干粮耗尽，那么钻进帐篷歇息；如果备用干粮充足，那么不需停留，继续前进

调用unpark，就好比别人送来了干粮。如果这时线程在帐篷休息，就唤醒让他继续前进；如果这时线程还在运行，那么下次他调用park时，仅是消耗掉备用干粮，不需停留继续前进。因为背包空间有限，**多次调用unpark仅会补充一份备用干粮**

> 类似0-1信号量

调用 park 设置 `_counter` 为0

调用 unpark 设置 `_counter` 为1