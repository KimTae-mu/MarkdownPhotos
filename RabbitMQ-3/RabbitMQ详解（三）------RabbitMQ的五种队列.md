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

**竞争消费者模式.**

1. 生产者

   ```java
   package org.alva.RabbitMQ.WorkModel;
   
   import com.rabbitmq.client.Channel;
   import com.rabbitmq.client.Connection;
   import org.alva.Utils.ConnectionUtil;
   
   import java.io.IOException;
   import java.util.concurrent.TimeoutException;
   
   /**
    * <一句话描述>,生产者
    * <详细介绍>,Work模式下的生产者
    *
    */
   public class Producter {
       public static final String QUEUE_NAME = "work_queue";
   
       public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
           //1.获取连接
           Connection connection = ConnectionUtil.getConnection("localhost", 5672, "/", "guest", "guest");
           //2.声明信道
           Channel channel = connection.createChannel();
           //3.声明(创建)队列
           channel.queueDeclare(QUEUE_NAME, false, false, false, null);
           //4.定义消息内容,发布多条消息
           for (int i = 0; i < 10; i++) {
               String message = "hello rabbitmq " + i;
               //5.发布消息
               channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
               System.out.println("[x] send message is '" + message + "'");
               //6.模拟发送消息延时,便于展示多个消费者竞争接受消息
               Thread.sleep(i * 10);
           }
           //7.关闭信道
           channel.close();
           //8.关闭连接
           connection.close();
       }
   }
   
   ```

2. 消费者

   需要创建两个消费者.

   消费者1:每接收一条消息后休眠10毫秒.

   ```java
   package org.alva.RabbitMQ.WorkModel;
   
   import com.rabbitmq.client.Channel;
   import com.rabbitmq.client.Connection;
   import com.rabbitmq.client.QueueingConsumer;
   import org.alva.Utils.ConnectionUtil;
   
   import java.io.IOException;
   import java.util.concurrent.TimeoutException;
   
   /**
    * <一句话描述>,消费者
    * <详细介绍>,Work模式下的消费者
    *
    */
   public class Consumer1 {
       public static final String QUEUE_NAME = "work_queue";
   
       public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
           //1.获取连接
           Connection connection = ConnectionUtil.getConnection("localhost", 5672, "/", "guest", "guest");
           //2.声明通道
           Channel channel = connection.createChannel();
           //3.声明队列
           channel.queueDeclare(QUEUE_NAME,false,false,false,null);
           //同一时刻服务器只会发送一条消息给消费者
   //        channel.basicQos(1);
   
           //4.定义队列的消费者
           QueueingConsumer queueingConsumer = new QueueingConsumer(channel);
           //5.监听队列,手动返回完成状态
           channel.basicConsume(QUEUE_NAME,false,queueingConsumer);
           //6.获取消息
           while (true){
               QueueingConsumer.Delivery delivery = queueingConsumer.nextDelivery();
               String message = new String(delivery.getBody());
               System.out.println("[x] received message : '"+message+"'");
               //休眠10毫秒
               Thread.sleep(10);
               //返回确认状态
               channel.basicAck(delivery.getEnvelope().getDeliveryTag(),false);
           }
       }
   }
   
   ```

   消费者2:每接收一条消息后休眠1000毫秒

   ```java
   package org.alva.RabbitMQ.WorkModel;
   
   import com.rabbitmq.client.Channel;
   import com.rabbitmq.client.Connection;
   import com.rabbitmq.client.QueueingConsumer;
   import org.alva.Utils.ConnectionUtil;
   
   import java.io.IOException;
   import java.util.concurrent.TimeoutException;
   
   /**
    * <一句话描述>,
    * <详细介绍>,
    *
    */
   public class Consumer2 {
       public static final String QUEUE_NAME = "work_queue";
   
       public static void main(String[] args) throws IOException, TimeoutException, InterruptedException {
           Connection connection = ConnectionUtil.getConnection("localhost", 5672, "/", "guest", "guest");
           Channel channel = connection.createChannel();
           channel.queueDeclare(QUEUE_NAME, false, false, false, null);
   //        channel.basicQos(1);
           QueueingConsumer queueingConsumer = new QueueingConsumer(channel);
           channel.basicConsume(QUEUE_NAME,false,queueingConsumer);
           while (true){
               QueueingConsumer.Delivery delivery = queueingConsumer.nextDelivery();
               String message = new String(delivery.getBody());
               System.out.println("[x] received message : '" + message + "'");
               Thread.sleep(1000);
               channel.basicAck(delivery.getEnvelope().getDeliveryTag(),false);
           }
       }
   }
   
   ```

3. 测试结果

   1. 首先生产者一次打印从0-9条消息

      ![image-20180819000057095](https://raw.githubusercontent.com/KimTae-mu/MarkdownPhotos/master/RabbitMQ-3/Producter.png)

   2. 然后是消费者1:结果为打印偶数条消息(注:先启动的消费者为消费者1)

      ![image-20180819000259211](https://raw.githubusercontent.com/KimTae-mu/MarkdownPhotos/master/RabbitMQ-3/Consumer1-noQos.png)

   3. 消费者2:结果为打印奇数条消息

      ![image-20180819000335579](https://raw.githubusercontent.com/KimTae-mu/MarkdownPhotos/master/RabbitMQ-3/Consumer2-noQos.png)

   #### 结论: ####

   ​	**消费者1和消费者2获取到的消息内容是不同的,也就是说同一个消息只能被一个消费者获取.*

   ​	**消费者1和消费者2分别获取奇数条消息和偶数条消息,两种获取消息的条数是一样的.*

   ​	前面我们说这种模式是竞争消费者模式,一条队列被多个消费者监听,这里两个消费者,其中消费者1和消费者2在获取消息后分别休眠了10毫秒和1000毫秒,也就是说两个消费者获取消息的效率是不一样的,但是结果却是两者获得的消息条数是一样的,这根本不构成竞争关系,那么我们应该怎么办才能让工作效率更高的消费者获取消息更多,也就是消费者1获取消息更多呢?

   4. 能者多劳

      ```java
      channel.basicQos(1);
      ```

      增加如上代码,表示同一时刻服务器只会发送一条消息给消费者.消费者1和消费者2获取消息结果如下:

      ![image-20180819001133009](https://raw.githubusercontent.com/KimTae-mu/MarkdownPhotos/master/RabbitMQ-3/Consumer1-Qos.png)

      ![image-20180819001145486](https://raw.githubusercontent.com/KimTae-mu/MarkdownPhotos/master/RabbitMQ-3/Consumer2-noQos.png)

   5. 应用场景

      效率高的消费者消费消息多,可以用来进行负载均衡.

