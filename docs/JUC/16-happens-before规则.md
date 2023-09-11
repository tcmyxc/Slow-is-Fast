# happens-before规则

规定了对共享变量的写操作在何种条件下能够让其他线程看到

## 7大核心规则

- 写 volatile 变量
- 多个线程使用同一把锁 objLock，操作同一个共享变量 x，则线程 A 对 x 的写操作其他线程是可见的
- 线程在 start 之前对变量的写操作，线程运行之后，是可以看到该变量的
- 线程结束之前对变量的写操作，在结束之后对其他线程可见（类似于持久性）
- 线程 t1 写入变量 x，然后打断线程 t2，其他线程（包括 t2）如果得知了 t2 被打断了，则可以读取到 t1 对 x 的修改
- 对变量默认值（0，false，null）的写，其他线程是可见的
- 传递性，A线性发生于B，B先于C，则A先于C

> 变量都指的是成员变量或者是静态变量

## 带示例的规则总结

- 写 volatile 变量

- 多个线程使用同一把锁 objLock，操作同一个共享变量 x，则线程 A 对 x 的写操作其他线程是可见的

	```java
	static int x;
	static Object m = new Object();
	
	new Thread(()->{
	   synchronized (m){
	       x = 10;
	   } 
	}; "t1").start();
	
	new Thread(()->{
	   synchronized (m){
	       System.out.println(x);
	   } 
	}; "t2").start();
	```

	- 线程在 start 之前对变量的写操作，线程运行之后，是可以看到该变量的

		```java
		static int x;
		x = 10;
		new Thread(()->{
		    System.out.println(x);
		}; "t1").start();
		```

	- 线程结束之前对变量的写操作，在结束之后对其他线程可见（类似于持久性）

	- 线程 t1 写入变量 x，然后打断线程 t2，其他线程（包括 t2）如果得知了 t2 被打断了，则可以读取到 t1 对 x 的修改

		```java
		static int x;
		
		public static void main(String[] args) throws InterruptedException {
		    Thread t2 = new Thread(() -> {
		        while (true){
		            if (Thread.currentThread().isInterrupted()){
		                System.out.println("t2 is Interrupted, x = " + x);
		                break;
		            }
		        }
		    }, "t2");
		    t2.start();
		
		    new Thread(() -> {
		        try {
		            Thread.sleep(1000);
		            x = 101;
		            t2.interrupt();// 打断 t2
		        } catch (InterruptedException e) {
		            throw new RuntimeException(e);
		        }
		    }, "t1").start();
		
		    while (!t2.isInterrupted()){
		        Thread.yield();
		    }
		
		    System.out.println("x = " + x);
		
		}
		```

		- 对变量默认值（0，false，null）的写，其他线程是可见的
		- 传递性，A线性发生于B，B先于C，则A先于C