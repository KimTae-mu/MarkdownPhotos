## RabbitMQ详解（一）------简介与安装(Docker) ##

刚刚进入实习,在学习过程中没有接触过MQ,RabbitMQ 这个消息中间件,正好公司最近的项目中有用到,学习了解一下.

**首先什么是MQ**:

​	MQ（*message queue*) : **MQ**是一种应用程序对应用程序的通信方法。应用程序通过写和检索出入列队的针对应用程序的数据（消息）来通信，而无需专用连接来链接它们.消息传递指的是程序之间通过在消息中发送数据进行通信，而不是通过直接调用彼此来通信，直接调用通常是用于诸如远程过程调用的技术。排队指的是应用程序通过队列来通信.队列的使用除去了接收和发送应用程序同时执行的要求。

**MQ基本概念**:

1. 消息(Message)

   消息是MQ中最小的概念,本质上就是*一段数据*,它能被一个或者多个应用程序所理解,是应用程序之间传递的信息载体.

2. 队列(Queue)

   1. 本地队列

      本地队列按照功能可划分为初始化队列,传输队列,目标队列和死信队列.

      1. 初始化队列用作消息触发功能.
      2. 传输队列只是暂存待传的消息,条件许可的情况下,通过管道将消息传送到其他队列管理器.
      3. 目标队列是消息的目的地,可以长期存放消息.
      4. 如果消息不能送达目标队列,也不能再路由出去,则被自动放入死信队列保存.

   2. 别名队列&amp;远程队列

      只是一个队列定义,用来指定远程队列管理器的队列.使用了远程队列,程序就不需要知道目标队列的位置.

   3. 模型队列

      模型队列定义了一套本地队列的属性结合,一旦打开模型队列,队列管理器会按照这些属性动态地创建出一个本地队列.

3. 队列管理器(Queue Manager)

   队列管理器是一个负责向应用程序提供消息服务的机构,如果把队列关系器比作数据库,那么队列就是其中的一张表.

4. 通道(Channel)

   通道是两个管理器之间的一种**单向**点对点的通信连接,如果需要双向交流,可以建立一对通道.

5. 监听器(Listener)

**MQ产品的特性**:

1. 可靠性传输

   对于应用来说,只要成功把数据提交给消息中间件,那么关于数据可靠传输的问题就由消息中间件来负责.

2. 不重复传输

   不重复传输就是断点续传的功能,特别适合网络不稳定的环境,节约网络资源.

3. 异步性传输

   异步性传输是指,接受消息双方不必同时在线,具有脱机能力和安全性.

4. 消息驱动

   接到消息后主动通知消息接收方.

5. 支持事务

   目前MQ也广泛被一些企业用于分布式事务的同步.

**常用的场景**:

1. 消息通道

2. 消息总线机制

   在如今的SOA架构或者微服务架构中,普遍使用.各个服务之间的通信,可以确保数据的一致性.

**常见的MQ对比**:

&emsp;&emsp;[见此处](www.baidu.com)

----



### RabbitMQ ###

​	话题回归.RabbitMQ是一个在**AMQP**协议标准基础上完整的,可复用的企业消息系统.它遵循**Mozilla Public License**开源协议,采用**Erlang**实现的工业级消息队列(MQ)服务器.

1. AMQP,即Advanced Message Queuing Protocol,一个提供统一消息服务的应用层标准高级消息队列协议,是应用层协议的一个开放标准,为面向消息的中间件设计.基于此协议的客户端与消息中间件可传递消息,并不受客户端/中间件不同产品,不同的开发语言等条件的限制.
2. 开源.
3. 使用Erlang语言编写,这是一种面向并发的编程语言,目的是创造一种可以应对大规模并发活动的编程语言和运行环境.

----



### 安装 ###

1. 安装[Docker](#).

2. Docker搜索Rabbitmq镜像.

   ```shell
   docker search rabbitmq
   ```

   ![image-docker-search-rabbitmq](https://raw.githubusercontent.com/KimTae-mu/MarkdownPhotos/master/RabbitMQ-1/docker-search.png)

   我们选择官方版本的,也就是第一个.*通过这个镜像创建的容器需要我们额外打开web management的插件,若不想手动开启,可下载 rabbitmq/management*

   ![image-docker-search-rabbitmq/management](https://raw.githubusercontent.com/KimTae-mu/MarkdownPhotos/master/RabbitMQ-1/docker-search2.png)

   ```shell
   docker pull rabbitmq
   ```

3. 镜像下载后,通过该镜像创建一个容器.

   ​	

   ```shell
   docker run -d --hostname my-rabbit -p 5671:5671 -p 5672:5672 -p 15671:15671 -p 15672:15672 -p 25672:25672 -p 4369:4369 -v $PWD/rabbitmq-data:/var/rabbitmq/lib --name my_rabbitmq rabbitmq:latest
   ```

   > 参数介绍:
   >
   > -d:后台运行容器.
   >
   > --hostname:指定主机名.
   >
   > -p:指定端口映射.
   >
   > -v:文件目录映射.
   >
   > --name:定义容器名称.

4. 查看日志.

   ​	

   ```shell
   docker logs my_rabbitmq
   ```

   ![image-docker-logs-rabbitmq](https://raw.githubusercontent.com/KimTae-mu/MarkdownPhotos/master/RabbitMQ-1/docker-logs-rabbitmq.png)

   

5. 如果使用的镜像为rabbitmq/management,到此步可直接浏览器访问[localhost:15672](http://localhost:15672);若使用rabbitmq镜像,我们需要进入docker,开启rabbitmq-management插件.

   ​	

   ```shell
   docker exec -it my_rabbitmq /bin/bash
   ls
   ```

   ![image-docker-rabbitmq-ls](https://raw.githubusercontent.com/KimTae-mu/MarkdownPhotos/master/RabbitMQ-1/rabbitmq-ls.png)

   可以看到有plugins插件的目录,我们需要用到的插件都在里面,使用命令即可开启插件.

   ​	

   ```shell
   cd plugins
   rabbitmq-plugins enable rabbitmq_management
   ```

   ![image-enable-webmanagement](https://raw.githubusercontent.com/KimTae-mu/MarkdownPhotos/master/RabbitMQ-1/enable-webmanagement.png)

6. 这样,我们在本地就可以打开浏览器访问[localhost:15672](http://localhost:15672),便可以看到RabbitMQ的页面了.其中用户名和密码都是guest.

![image-localhost-15672](https://raw.githubusercontent.com/KimTae-mu/MarkdownPhotos/master/RabbitMQ-1/localhost-15672.png)



