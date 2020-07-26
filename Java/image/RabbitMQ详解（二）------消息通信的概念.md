## RabbitMQ详解（二）------消息通信的概念 ##

消息通信,有很多种,邮箱 qq 微信 短信等,这些通信方式都有发送者,接受者,还有一个中间存储离线消息的容器.但是这些通信方式和**RabbitMQ**的通信模型是不一样的,比如邮件,邮件服务器基于*POP3/SMTP*协议,通信双方需要明确指定,并且发送的邮件内容有固定的结构.而RabbitMQ服务器基于[*AMQP*](https://baike.baidu.com/item/AMQP/8354716?fr=aladdin)协议,这个协议是不需要明确指定发送方和接受方的,而且发送的消息也没有固定的结构,甚至可直接存储二进制数据,并且和邮件服务器一样,也能存储离线消息,最关键的是*RabbitMQ*既能够以一对一的方式进行路由,还能够以一对多的方式进行广播.

----

### 生产者和消费者 ###

在RabbitMQ的通信过程中,有两个主要的角色:生产者和消费者.类比于邮件通信的发送方和接收方.

首先我们需要明确RabbitMQ服务器是不能够产生数据的,它是——消息中间件,是一个用来传递消息的中间商.生产者产生创建消息,然后发布到代理服务器(*RabbitMQ*),而消费者则从代理服务器获取消息(不是直接找生产者要消息),而且在实际应用中,生产者和消费者也是可以角色互相转换的,所以当我们应用程序连接到RabbitMQ服务器时,必须要明确我是生产者还是消费者.

----

### 消息 ###

生产者创建消息,然后发布到RabbitMQ服务器中.

这里的消息分为两部分:***有效内容***和***内容标签***.

1. 有效内容:可以是任何内容,一个数组,一个集合,甚至二进制数据都可以.RabbitMQ不会在意你发什么数据,尽管发就可以了.
2. 内容标签:描述有效内容,是RabbitMQ用来决定谁将获得消息.前面说的邮件通信,必须明确指定发送方地址和收件方地址,而基于AMQP协议的RabbitMQ则是通过生产者发送消息附带的内容标签将消息发送给感兴趣的消费者.

***一般来说生产者创建消息会设置标签,但是传输到消费者那里就没有标签了,除非在有效内容中说明谁是生产者,一般消费者是不知道谁产生的消息的.***

----

### 信道 ###

生产者产生了消息,然后发布到RabbitMQ服务器,发布之前肯定要先连接上服务器,也就是要在应用程序和RabbitMQ服务器之间建立一条TCP连接,一旦连接建立,应用程序就可以创建一条AMQP信道.

***信道是建立在"真实的TCP"连接内的虚拟连接,AMQP命令都是通过信道发送出去的,每条信道都会被指派一个唯一的ID(AMQP库会帮你记住ID),不论是发布消息,订阅队列或者接受消息,这些动作都是通过信道来完成的.***

#### 为什么不直接通过TCP连接来发送AMQP命令呢? ####

这是因为效率问题,对于操作系统来说,每次建立和销毁TCP会话是非常昂贵的开销,而实际系统中,比如电商双十一,每秒钟高峰期成千上万条连接,一般来说操作系统建立TCP连接是有数量限制的,那这就会遇到瓶颈.

引入信道的概念,我们可以在一条TCP连接上创建N多个信道,这样既能发送命令,也能够保证每条信道的私密性,我们可以将其想象为光纤电缆.

----

### 交换器和队列 ###

交换器和队列都是RabbitMQ服务器的一部分,我们知道生产者会将消息发送到RabbitMQ服务器,而进入该服务器后,***首先进入交换器部分***,然后交换器根据消息附带的**内容标签**,将消息绑定到相应的**队列**.什么是队列?

1. 容纳消息的场所,生产者发送到RabbitMQ服务器的消息会在队列中等待消费者消费.
2. 队列是RabbitMQ服务器的终点(除非消息进入了[黑洞](#)).
3. 队列可以实现负载均衡,我们可以增加一堆消费者,然后让RabbitMQ以循环的方式来均匀的分配消息.

消息进入RabbitMQ服务器时,会首先将消息发送到交换器,然后交换器会根据特定的路由算法以及消息的内容标签将消息绑定到相应的队列.在AMQP协议中有四种交换器:***direct、fanout、topic、headers***,每种交换器都实现了不同的路由算法,这也对应RabbitMQ工作的几种不同工作方式.

----

### 虚拟主机 ###

首先我们抛出一个问题,一个RabbitMQ肯定不是只服务一个应用程序,那么多个应用程序同时使用RabbitMQ服务器,如何保证彼此之间不会冲突?

答案就是虚拟主机,虚拟主机其实就是一个迷你版的RabbitMQ服务器,它拥有自己的交换器和队列,更重要的是虚拟主机拥有自己的权限机制,一个服务器能够创建多个虚拟主机.那么我们在使用RabbitMQ服务器的时候,只需要讲一个应用程序对应一个虚拟主机,这种各个实例间逻辑上的分离就能够保证不同的应用程序安全的传递信息.

***默认的虚拟主机是"/".***

----

### 简单实例 ###

开启RabbitMQ服务,这里使用的是docker,具体安装可看[上篇博文](https://www.cnblogs.com/Alva-mu/p/9487459.html).

pom.xml

```xml
<!--RabbitMQ-client-->
        <dependency>
            <groupId>com.rabbitmq</groupId>
            <artifactId>amqp-client</artifactId>
            <version>3.6.2</version>
        </dependency>
```

ConnectionUtil.java	

```java
package org.alva.Utils;

import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

/**
 * <一句话描述>,RabbitMQ的连接工具类
 * <详细介绍>,
 *
 */
public class ConnectionUtil {
    public static Connection getConnection(String host, int port, String vhost, String username, String password) throws IOException, TimeoutException {
        //1.定义连接工厂
        ConnectionFactory connectionFactory = new ConnectionFactory();
        //2.设置服务器地址
        connectionFactory.setHost(host);
        //3.设置端口
        connectionFactory.setPort(port);
        //4.设置虚拟主机,用户名,密码
        connectionFactory.setVirtualHost(vhost);
        connectionFactory.setUsername(username);
        connectionFactory.setPassword(password);

        //5.通过连接工厂获取连接
        Connection connection = connectionFactory.newConnection();
        return connection;
    }
}
```

Producer.java

```java
package org.alva.RabbitMQ;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import org.alva.Utils.ConnectionUtil;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

/**
 * <一句话描述>,生产者
 * <详细介绍>,
 *
 */
public class Producer {
    private final static String QUEUE_NAME = "hello";

    public static void main(String[] args) throws IOException, TimeoutException {
        //1.获取连接
        Connection connection = ConnectionUtil.getConnection("localhost", 5672, "/", "guest", "guest");
        //2.声明通道
        Channel channel = connection.createChannel();
        //3.声明(创建)队列
        channel.queueDeclare(QUEUE_NAME,false,false,false,null);
        //4.定义消息内容
        String message = "hello rabbitmq";
        //5.发布消息
        channel.basicPublish("",QUEUE_NAME,null,message.getBytes());
        System.out.println("[x] send'"+message+"'");
        //6.关闭通道和连接
        channel.close();
        connection.close();

    }
}

```

Consumer.java

```java
package org.alva.RabbitMQ;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.QueueingConsumer;
import org.alva.Utils.ConnectionUtil;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

/**
 * <一句话描述>,消费者
 * <详细介绍>,
 *
 */
public class Consumer {
    private final static String QUEUE_NAME = "hello";

    public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
        //1.获取连接
        Connection connection = ConnectionUtil.getConnection("localhost", 5672, "/", "guest", "guest");
        //2.声明通道
        Channel channel = connection.createChannel();
        //3.声明队列
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);
        //4.定义队列的消费者
        QueueingConsumer queueingConsumer = new QueueingConsumer(channel);
        //5.监听队列
        channel.basicConsume(QUEUE_NAME,true,queueingConsumer);
        //6.获取消息
        while (true){
            QueueingConsumer.Delivery delivery = queueingConsumer.nextDelivery();
            String message = new String(delivery.getBody());
            System.out.println("[x] Received '" + message + "'");
        }
    }
}

```

