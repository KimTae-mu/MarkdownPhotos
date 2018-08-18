## Docker搭建RabbitMQ集群 ##

### Docker安装 ###

见[官网]()

----

### RabbitMQ镜像下载及配置 ###

见[此博文](https://www.cnblogs.com/Alva-mu/p/9487459.html)

----

### 集群搭建 ###

1. 首先,我们需要启动运行RabbitMQ

   ```shell
   docker run -d --hostname my-rabbit -p 5671:5671 -p 5672:5672 -p 15671:15671 -p 15672:15672 -p 25672:25672 -p 4369:4369 -v $PWD/rabbitmq-data:/var/rabbitmq/lib --name my_rabbitmq rabbitmq:latest
   ```

   参数说明:

   ​	-d:后台进程运行

   ​	--hostname:主机名称

   ​	-p:端口映射

   ​		15672:http访问端口

   ​		5672:AMQP访问端口

   ​	-v:文件映射

   ​	--name:容器名称

2. 启动多个RabbitMQ

   ```shell
   docker run -d --hostname my-rabbit -p 5671:5671 -p 5672:5672 -p 15671:15671 -p 15672:15672 -p 25672:25672 -p 4369:4369 -v $PWD/rabbitmq-data:/var/rabbitmq/lib --name my_rabbitmq1 rabbitmq:latest
   ```

   

   ```shell
   docker run -d --hostname my-rabbit -p 5673:5672 -p 15673:15672 -v $PWD/rabbitmq-data:/var/rabbitmq/lib --name my_rabbitmq2 rabbitmq:latest
   ```

   这样我们就可以使用*http://ip:15672* 和 *http://ip:15673* 进行访问,默认账号密码均为**guest**.

   ----

   ### 搭建RabbitMQ集群 ###

   步骤一:安装RabbitMQ;

   ```shell
   docker run -d --hostname my-rabbit1 --name my_rabbitmq1 -p 15672:15672 -p 5672:5672 -e RABBITMQ_ERLANG_COOKIE='rabbitcookie' rabbitmq:latest
   ```

   参数说明:

   ​	-e:设置环境变量

   ```shell
   docker run -d --hostname my-rabbit2 --name my_rabbitmq2 -p 5673:5672 --link my_rabbitmq1:my-rabbit1 -e RABBITMQ_ERLANG_COOKIE='rabbitcookie' rabbitmq:latest
   ```

   ```shell
   docker run -d --hostname my-rabbit3 --name my_rabbitmq3 -p 5674:5672 --link my_rabbitmq1:my-rabbit1 --link my_rabbitmq2:my-rabbit2 -e RABBITMQ_ERLANG_COOKIE='rabbitcookie' rabbitmq:latest
   ```

   参数说明:

   ​	--link:添加链接到另一个容器

   ***注意点:

   ​	多个容器之间使用"--link"连接,此属性不能少;

   ​	Erlang Cookie值必须相同,也就是RABBITMQ_ERLANG_COOKIE参数的值必须相同,原因见下文.

   步骤二:加入RabbitMQ节点到集群;

   设置节点1:

   ```shell
   docker exec -it my_rabbitmq1 /bin/bash
   rabbitmqctl stop_app
   rabbitmqctl reset
   rabbitmqctl start_app
   exit
   ```

   设置节点2:

   ```shell
   docker exec -it my_rabbitmq2 /bin/bash
   rabbitmqctl stop_app
   rabbitmqctl reset
   rabbitmqctl join_cluster --ram rabbit@my-rabbit1
   rabbitmqctl start_app
   exit
   ```

   设置节点3:

   ```shell
   docker exec -it my_rabbitmq3 /bin/bash
   rabbitmqctl stop_app
   rabbitmqctl reset
   rabbitmqctl join_cluster --ram rabbit@my-rabbit1
   rabbitmqctl start_app
   exit
   ```

   参数说明:

   ​	--ram:表示设置为内存节点,忽略次参数默认为磁盘节点.

   设置好之后,使用 *http://ip:15672* 进行访问,默认账号密码是guest/guest.

   ----

   ### 配置相同Erlang Cookie ###

   有些特殊的情况,比如已经运行一段时间的几个单个物理机,我们在之前没有设置过相同的Erlang Cookie值,现在我们要把单个的物理机部署成集群,实现我们需要同步Erlang的Cookie值.

   #### 1.为什么要配置相同的Erlang Cookie? ####

   因为RabbitMQ使用Erlang实现的,Erlang Cookie相当于不同节点之间相互通讯的秘钥,Erlang节点通过交换Erlang Cookie获得认证.

   #### 2.Erlang Cookie的位置 ####

   要想知道Erlang Cookie的位置,首先要取的RabbitMQ启动日志里面的home dir路径,作为根路径.可使用:

   ```shell
   docker logs 容器名称
   ```

   查看.

   #### 3.复制Erlang Cookie到其他RabbitMQ节点 ####

   获取到第一个RabbitMQ的Erlang Cookie之后,只需要把这个文件复制到其他RabbitMQ节点即可.

   物理机和容器之间复制命令如下:

   ​	容器复制文件到物理机: 

   ```shell
   docker cp 容器名称:容器目录 物理机目录
   ```

   ​	物理机复制文件到容器:

   ```shell
   docker cp 物理机目录 容器名称:容器目录
   ```

   设置Erlang Cookie文件权限:

   ```shell
   chmod 600 /var/lib/rabbitmq/.erlang.cookie
   ```





----



### 注意事项 ###

按照以上步骤搭建完成后,每个RabbitMQ服务器均需手动开启rabbitmq_management插件,方可在浏览器中输入[http://localhost:15672](http://localhost:15672)进入RabbitMQ管理界面,在其中可看到相关节点的信息. 

[如何开启插件](https://www.cnblogs.com/Alva-mu/p/9487459.html)

![RabbitMQ-Nodes](https://raw.githubusercontent.com/KimTae-mu/MarkdownPhotos/master/RabbitMQ-3/RabbitMQ-Nodes.png)