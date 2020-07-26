## ThreadLocal 应用场景及使用方式及原理 ##

### ThreadLocal 是什么呢? ###

ThreadLocal本身是为线程安全和某些特定场景的问题而设计的.

每一个ThreadLocal能够放一个线程级别的变量,可是它本身能够被多个线程共享使用,并且又能够达到线程安全的目的,且绝对安全.

比如:

```java
public static final ThreadLocal<String> RESOURCE = new ThreadLocal<>();
```

RESOURCE代表一个能够存放String类型的ThreadLocal对象,此时不论什么一个线程能够并发访问这个变量,对他进行写入,读取操作,都是线程安全的.比方一个线程通过**RESOURCE.set("aaaa");**将数据写入ThreadLocal中,在不论什么一个地方,都能够通过**RESOURCE.get();**将值获取出来.



### 应用场景及使用方式 ###

ThreadLocal适用于每个线程需要自己独立的实例且该实例需要在做个方法中被使用,也即变量在线程间隔离而在方法或类间共享的场景.另外,该场景下并非必须使用ThreadLocal,其他方式完全可以实现同样的效果,只是ThreadLocal使得实现更简洁.



### ThreadLocal原理 ###

既然每个访问ThreadLocal变量的线程都有自己的一个"本地"实例副本.一个可能的方案是ThreadLocal维护一个Map,键是Thread,值是它在该Thread内的实例.线程通过该ThreadLocal的get()方法获取实例时,只需要以线程为键,从Map中找出对应的实例即可.

该方案可满足上文提到的每个线程内一个独立备份的要求,每个新线程访问该ThreadLocal时,需要向Map中添加一个映射,而每个线程结束时,应该清除该映射.



### 总结 ###

> * ThreadLocal并不解决线程间共享数据的问题
> * ThreadLocal通过隐式的在不同线程内创建独立实例副本避免了实例线程安全的问题
> * 每个线程持有一个Map并维护了ThreadLocal对象与具体实例的映射,该Map由于只被持有它的线程访问,故不存在线程安全以及锁的问题
> * ThreadLocal的Entry对ThreadLocal的引用为***弱引用***,避免了ThreadLocal对象无法被回收的问题
> * ThreadLocal的set方法通过调用***replaceStaleEntry***方法回收键为**null**的Entry对象的值(即为具体实例)以及Entry对象本身从而防止内存泄漏
> * ThreadLocal使用与变量在线程间隔离且在方法间共享的场景