## RabbitMQ详解（三）------RabbitMQ的五种模式 ##

### 1.简单队列(模式) ###

上一篇文章末尾的[实例]()给出的代码就是简单模式.

***一个生产者对应一个消费者!!!***

pom.xml

​	必须导入RabbitMQ依赖包

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
        /*
            true:表示自动确认,只要消息从队列中获取,无论消费者获取到消息后是否成功消费,都会认为消息成功消费.
            false:表示手动确认,消费者获取消息后,服务器会将该消息标记为不可用状态,等待消费者的反馈,
            如果消费者一直没有反馈,那么该消息将一直处于不可用状态,并且服务器会认为该消费者已经挂掉,不会再给其发送消息,
            直到该消费者反馈.
        */
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

Productor.java

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

----

### 2.work模式 ###

***一个生产者对应多个消费者,但是只能有一个消费者获得消息!!!***

竞争消费者模式.

