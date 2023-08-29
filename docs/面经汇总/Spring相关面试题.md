# Spring面试题

## 如何解决循环依赖

三级缓存、构造函数注入等

三级缓存的三个级别分别是：

1. **singletonObjects：** 这个缓存存储已经完全初始化的单例Bean对象。当一个Bean创建完成后，它会被放入这个缓存中，供其他Bean进行引用。如果其他Bean需要这个已初始化的Bean，Spring会直接从这个缓存中获取。
2. **earlySingletonObjects：** 这个缓存存储正在创建中的Bean实例，但是这些实例可能还没有完全初始化完成。当一个Bean开始创建时，它会被放入这个缓存中。其他需要引用该Bean的Bean在创建过程中可以使用这个尚未完全初始化的实例，从而避免循环依赖。
3. **singletonFactories：** 这个缓存存储Bean的工厂（Factory）对象。当一个Bean开始创建时，它的工厂对象会被放入这个缓存中。其他需要引用该Bean的Bean可以通过工厂来获取实例。

三级缓存的工作流程大致如下：

1. 当需要创建一个Bean时，Spring首先会检查singletonObjects缓存中是否已经存在该Bean的实例。如果存在，则直接返回。
2. 如果singletonObjects缓存中不存在该Bean的实例，Spring会检查earlySingletonObjects缓存，看是否有正在创建中的实例。如果有，它会直接返回这个尚未初始化完成的实例。
3. 如果既没有在singletonObjects缓存中找到实例，也没有在earlySingletonObjects缓存中找到正在创建中的实例，那么Spring会尝试从singletonFactories缓存中获取工厂对象，然后使用工厂来创建Bean的实例。同时，这个新创建的实例会被放入earlySingletonObjects缓存中，供其他需要引用的Bean使用。