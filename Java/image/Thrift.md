# Thrift

## Thrift简介

Thrift是一个跨语言的服务部署框架,最初由Facebook于2007年开发,2008年进入Apache开源项目.Thrift通过一个中间语言(IDL,接口定义语言)来定义RPC的接口和数据类型,然后通过一个编译器生成不同语言的代码,***并由生成的代码负责RPC协议层和传输层的实现***.

## Thrift协议栈

![Thrift架构](https://upload.wikimedia.org/wikipedia/commons/d/df/Apache_Thrift_architecture.png)

### Transport

Transport层提供了一个简单的网络读写抽象层.这使得Thrift底层的Transport从系统其它部分(如:序列化/反序列化)解耦.

Thrift支持如下几种Transport:

> - TIOStreamTransport和TSocket这两个类的结构对应着阻塞同步IO, TSocket封装了Socket接口
> - TNonblockingTrasnsort，TNonblockingSocket这两个类对应着非阻塞IO
> - TMemoryInputTransport封装了一个字节数组byte[]来做输入流的封装
> - TMemoryBuffer使用字节数组输出流ByteArrayOutputStream做输出流的封装
> - TFramedTransport则封装了TMemoryInputTransport做输入流，封装了TByteArryOutPutStream做输出流，作为内存读写缓冲区的一个封装。TFramedTransport的flush方法时，会先写4个字节的输出流的长度作为消息头，然后写消息体。和FrameBuffer的读消息对应起来。FrameBuffer对消息时，先读4个字节的长度，再读消息体
> - TFastFramedTransport是内存利用率更高的一个内存读写缓存区，它使用自动增长的byte[]\(不够长度才new)，而不是每次都new一个byte[]，提高了内存的使用率。其他和TFramedTransport一样，flush时也会写4个字节的消息头表示消息长度。

### Protocol

Protocol抽象层定义了一种将内存中数据结构映射成可传输格式的机制.换句话说,Protocol定义了dataType怎样使用底层的Transport对自己进行编解码.因此,Protocol的实现要给出编码机制并负责对数据进行序列化.

Thrift支持如下几种Protocol:

> - TBinaryProtocol : 二进制格式.
> - TCompactProtocol : 压缩格式
> - TJSONProtocol : JSON格式
> - TSimpleJSONProtocol : 提供JSON只写协议, 生成的文件很容易通过脚本语言解析
> - 等等

### Processor

与服务相关的processor实现由编译器产生.

Processor主要工作流程如下:

从连接中读取数据(使用输入Protocol),将处理授权给handler(由用户实现),最后将结果写到连接上(使用输出Protocol).

### Server

***Server将以上所有特性集成在一起***,Server实现的几个步骤如下:

> （1）  创建一个transport对象
>
> （2）  为transport对象创建输入输出protocol
>
> （3）  基于输入输出protocol创建processor
>
> （4）  等待连接请求并将之交给processor处理

## Thrift类型系统

Thrift类型系统包括预定义的基本类型(如bool,byte,double,string),特殊类型(如binary),用户自定义结构体,容器类型(如list,set,map)以及异常和服务定义.

### 基本类型(Base Type)

> bool    ： 布尔类型(true or value)，占一个字节
> byte/i8 ： 有符号字节
> i16     :  16位有符号整型
> i32     :  32位有符号整型
> i64     :  64位有符号整型
> double  ： 64位浮点数
> string  ： 未知编码或者二进制的字符串

### 特殊类型(Special type)

> ```txt
> binary   ： 未经过编码的字节流
> ```

### 容器(Container)

Thrift容器与类型密切相关,它与当前流行编程语言提供的容器类型相对应,Thrift提供了3中容器类型.

> ```t
> List<t1>   ：一系列t1类型的元素组成的有序表，元素可以重复
>  
> Set<t1>    ：一系列t1类型的元素组成的无序表，元素唯一
> 
> Map<t1,t2> ：key/value对（key的类型是t1且key唯一，value类型是t2)
> ```
>
> **注意:容器中的元素类型可以是除了Service之外的任何合法Thrift类型(包括结构体和异常)**

### 结构(struct)

Thrift结构体在概念上同C语言结构体类型——**一种将相关属性聚集(封装)在一起的方式.在面向对象语言中,Thrift结构体被转换成类,在Java语言中,这等价于JavaBean的概念**.

### 异常(Exception)

异常在语法和功能上类似于结构体,只不过异常使用关键字exception而不是struct关键字声明.但它在语义上不同于结构体——当定义一个RPC服务时,开发者可能需要声明一个远程方法抛出一个异常.

### 服务(Service)

一个服务包含一系列命名函数,每个函数包含一系列的参数以及一个返回类型.

***在语法上,服务等价于定义一个借口或者纯虚抽象类***

## 其他语法参考

### Tpedefs

Thrift支持C/C++风格的typedef,如:

```c
typedef i32 MyInteger
```

> 说明:
>
> 1. 末尾没有逗号
> 2. struct可以使用typedef

### 枚举Enums

可以像C/C++那样定义枚举类型,如:

```C++
enum Gender{
    MALE,
    FEMALE,
    UNKONWN
}
```

### 注释Comments

Thrift支持shell注释风格,C/C++语言中单行或者多行注释风格

### 命名空间Namespace

Thrift中的命名空间同C++中的namespace和Java中的package类似,它们均提供了一种组织(隔离)代码的方式.因为每种语言均有自己的命名空间定义方式(如Python中有module),Thrift允许开发者针对特定语言定义namespace:

```C++
namespace cpp com.example.project
namespace java com.example.project
```

### includes

Thrift允许Thrift文件包含,用户需要使用Thrift文件名作为前缀访问被包含的对象,如:

```c++
include "user.thrift"
```

> 说明:
>
> 1. Thrift文件名要用双引号包含,末尾没有逗号或者分号
> 2. 注意user前缀

### 常量Constants

Thrift允许用户定义常量,复杂的类型和结构体可使用JSON形式表示.

```c++
const i32 INT_CONST = 1234;    // a
 
const map<string,string> MAP_CONST = {"hello": "world", "goodnight": "moon"}
```

