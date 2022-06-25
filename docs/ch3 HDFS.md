# 第3章 Hadoop分布式文件系统

> shenhao

## 3.0 产生的背景

&emsp;&emsp;随着数据量越来越大，一台独立的物理计算机逐渐已经存不下所有的数据。如何解决这一问题呢？直观的解决办法就是：当一台机器存不下时，那就用上百上千万台机器一起存储大规模的数据，但是管理和维护会极其不方便，十分低效。而这也是大数据时代必须解决的**海量数据的高效存储问题**！！为此，**分布式文件系统**孕育而生！  
&emsp;&emsp;**分布式文件系统是管理网络中跨多台计算机存储的文件系统**。该系统架构于网络之上，势必会引入了网络编程的复杂性。因此，分布式文件系统比普通磁盘文件系统更为复杂。例如，如何使文件系统能够容忍节点故障的同时，不会丢失任何数据；在单一节点数据更新的同时如何通知整个文件系统进行同步更新等等。  
&emsp;&emsp;谷歌公司开发了**第一个大规模商业化应用的分布式文件系统GFS**，而Hadoop分布式文件系统是针对GFS的开源实现，它就是Hadoop两大核心组成部分之一的**HDFS**！！由于其良好的容错能力，使得用户能在廉价服务器集群中存储大规模数据，实现大流量和大数据量的读写。

> ps：这一部分可是重点哈，敲黑板敲黑板！！！！都支棱起来支棱起来，好好学习冲冲冲~~~

<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.0.png" style="zoom: 67%;" /></center>

## 3.1 概述

### 3.1.1 分布式文件系统简介

> **块的概念：普通文件系统 VS 分布式文件系统**  
> - **普通文件系统：**一般会把磁盘空间划分为每512字节一组，称为“[磁盘块](https://zhuanlan.zhihu.com/p/117375905)”，它是文件系统读写操作的最小单位，文件系统的块（Block）通常是磁盘块的整数倍，即每次读写的数据量必须是磁盘块大小的整数倍；  
> - **分布式文件系统：**也采用了块的概念，文件被分成若干个块进行存储，块是数据读写的基本单元，只不过分布式文件系统的块要比普通文件系统中的块大很多，比如，HDFS默认的一个块的大小是64MB，而且与普通文件系统不同的是，在分布式文件系统中，如果一个文件小于一个数据块的大小，它不会占用整个数据块的储存空间。设计一个比较大的块，是为了**最小化**寻址开销（HDFS寻址开销包括：磁盘的寻道开销和数据块的定位开销）；但是块的大小也不能太大，会导致MapReduce中的Map任务一次只处理一个块中的数据，如果启动的任务太少，反而会影响并行的速度。

&emsp;&emsp;分布式文件系统的设计一般采用**“客户机/服务器”（Client/Server）**，客户端以特定的通信协议通过网络与服务器建立连接，提出文件访问请求，客户端和服务器可以通过设置访问权，来限制请求方对底层数据存储块的访问。  
&emsp;&emsp;分布式文件系统在**物理结构**上是由计算机集群中的多个节点构成的，如下图所示，这些节点分为两类：一类叫“**主节点**”（Master Node），或者也被称为“**名称节点**"（NameNode）；另一类叫“**从节点**"（Worker Node），或者也被称为“**数据节点**"（DataNode）：

<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.1.1.png" style="zoom:50%;" /></center>

- **名称节点：**负责文件和目录的创建、删除和重命名等，同时管理着数据节点和文件块的映射关系，因此客户端只有访问名称节点才能找到请求的文件块所在的位置，从而到相应位置读取所需的文件块；

<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.1.1_namenode.png" style="zoom:50%;" /></center>

- **数据节点：**负责数据的存储和读取。在存储时，由名称节点分配存储位置，然后由客户端把数据直接写入相应数据节点；在读取时，客户端从名称节点获得数据节点和文件块的映射关系，然后就可以到相应位置访问文件块。数据节点也要根据名称节点的命令创建、删除数据块和冗余复制。

&emsp;&emsp;计算机集群中的节点可能发生故障，因此为了保证**数据的完整性**，分布式文件系统通常采用**多副本存储**。文件块会被复制为多个副本，存储在不同的节点上，而且存储同一文件块不同副本的各个节点会分布在不同的机器上。  
&emsp;&emsp;这样在单个节点出现故障时，就可以快速调用副本重启单个节点上的计算过程，而不用重启整个计算过程，整个机器出现故障时也不会丢失所有文件块。文件块的大小和副本个数通常可以由用户指定。  
&emsp;&emsp;分布式文件系统是针对大规模数据存储而设计的，主要用于处理大规模文件，如TB级文件，处理过小的文件不仅无法充分发挥其优势，而且会严重影响到系统的扩展和性能。

### 3.1.2 HDFS简介

&emsp;&emsp;**HDFS（Hadoop Distribute File System）**是大数据领域一种非常可靠的存储系统，它以分布式方式存储超大数据量文件，但它并不适合存储大量的小数据量文件。同时HDFS是Hadoop和其他组件的数据存储层，运行在由价格廉价的商用机器组成的集群上的，而价格低廉的机器发生故障的几率比较高，因此HDFS在设计上采取了多种机制，在硬件故障的情况下保障数据的完整性。

&emsp;&emsp;总体而言，HDFS要实现以下目标：  

- **兼容廉价的硬件设备：**实现在硬件故障的情况下也能保障数据的完整性
- **流数据读写：**不支持随机读写的操作
- **大数据集：**数据量一般在GB、TB以上的级别
- **简单的文件模型：**一次写入、多次读取
- **强大的跨平台兼容性：**采用`Java`语言实现

&emsp;&emsp;但是，HDFS也有如下局限性：  

- **不适合低延迟数据访问：**HDFS主要是**面向大规模数据批量处理而设计**的，采用**流式数据读取**，具有**很高的数据吞吐率**，但是，这也意味着**较高的延迟**，因此，HDFS不适合用在需要较低延迟（如数十毫秒）的应用场合。对于低延迟要求的应用程序而言，HBase是一个更好的选择；
- **无法高效存储大量小文件：**小文件是指文件大小小于一个块的文件，HDFS无法高效存储和处理大量的小文件，过多小文件会给系统扩展性和性能带来诸多问题：
  1. HDFS采用名称节点（NameNode）来管理文件系统的元数据，这些元数据被保存在内存中，使客户端可以快速获取文件实际存储位置。通常，每个文件、目录和块大约占150字节，如果有1000万个文件，每个文件对应一个块，那么，名称节点至少要消耗3GB的内存来保存这些元数据信息。很显然，这时元数据检索的效率就比较低了，需要花费较多的时间找到一个文件的实际存储位置。而且，如果继续扩展到数十亿个文件时，名称节点保存元数据所需要的内存空间就会大大增加，以现有的硬件水平，是无法在内存中保存如此大量的元数据；
  2. 用MapReduce处理大量小文件时，会产生过多的Map任务，线程管理开销会大大增加，因此处理大量小文件的速度远远低于处理同等大小的大文件的速度；
  3. 访问大量小文件的速度远远低于访问大文件的速度，因为访问大量小文件，需要不断从一个数据节点跳到另一个数据节点，严重影响性能。
- **不支持多用户写入及任意修改文件**：HDFS只允许一个文件有一个写入者，不允许多个用户对同一个文件执行写操作，而且只允许对文件执行追加操作，不能执行随机写操作。

## 3.2 HDFS的体系结构

&emsp;&emsp;HDFS采用了主从（Master/Slave）结构模型，一个HDFS集群包括**一个名称节点（NameNode）**和**若干个数据节点（DataNode）**。  
- **名称节点**作为中心服务器，负责管理文件系统的命名空间及客户端对文件的访问。
- **数据节点**负责处理文件系统客户端的读/写请求，在名称节点的统一调度下进行数据块的创建、删除和复制等操作。
- 每个数据节点会周期性地向名称节点发送**“心跳"信息**，报告自己的状态，没有按时发送心跳信息的数据节点会被标记为“宕机”，不会再给它分配任何I/O请求。

&emsp;&emsp;用户在使用HDFS时，仍然可以像在普通文件系统中那样，使用文件名去存储和访问文件。

<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.2.png" style="zoom: 50%;" /></center>

&emsp;&emsp;实际上，在系统内部，一个文件会被切分成若干个数据块，这些数据块被分布存储到若干个数据节点上。当客户端需要访问一个文件时，首先把文件名发送给名称节点，名称节点根据文件名找到对应的数据块（一个文件可能包括多个数据块），再根据每个数据块信息找到实际存储在各个数据块的数据节点的位置，并把数据节点位置发送给客户端，最后客户端直接访问这些数据节点获取数据。在整个访问过程中，名称节点并不参与数据的传输。这种设计方式，使得各个文件的数据能够在不同的数据节点上实现并发访问，大大提高了数据访问速度。


## 3.3 HDFS的存储原理

### 3.3.1 数据的冗余存储

&emsp;&emsp;为了保证系统的**容错性**和**可用性**，HDFS采用了**多副本方式**对数据进行冗余存储，通常**一个数据块的多个副本会被分布到不同的数据节点上**。

<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.3.1.png" style="zoom: 67%;" /></center>

&emsp;&emsp;这种多副本方式具有以下 3 个优点：  
- **加快数据传输速度：**当多个客户端需要同时访问同一个文件时，可以让各个客户端分别从不同的数据块副本中读取数据，这就大大加快了数据传输速度，实现了并行操作。
- **容易检查数据错误：**HDFS的数据节点之间通过网络传输数据，采用多个副本可以很容易判断数据传输是否出错。
- **保证数据的可靠性：**即使某个数据节点出现故障失效，也不会造成数据丢失。

### 3.3.2 数据存取策略

&emsp;&emsp;数据存取策略包括**数据存放**、**数据读取**和**数据复制**。

#### 3.3.2.1 数据存放

&emsp;&emsp;HDFS采用了以机架（Rack）为基础的数据存放策略。一个HDFS集群通常包含多个机架，不同机架之间的数据通信需要经过交换机或路由器，同一机架的不同机器之间数据通信不需要交换机或路由器，因此同一机架中不同机器之间的通信要比不同机架之间机器的通信带宽大。  
&emsp;&emsp;HDFS默认每个数据节点都是在不同机架上的，这样有一个缺点：**写入数据的时候不能充分利用同一机架内部机器之间的带宽**。这种方法同时也带来了更多显著的优点： 
- 可以**获得很高的数据可靠性**，即使一个机架发生故障，位于其他机架上的数据副本仍然可用。
- 在读数据的时候，可以在多个机架上并行读取数据，大大**提高了数据读取速度**。
- 可以更容易**实现系统内部负载均衡和错误纠正**。
  

&emsp;&emsp;**HDFS默认的冗余复制因子是 3**，每一个文件会被同时保存到 3 个地方，其中两份副本放在同一个机架的不同机器上面，第三个副本放在不同机架的机器上面。

<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.3.2.png" style="zoom:50%;" /></center>

HDFS副本的存放策略是：
1. 如果是在集群内发起写操作请求，则把第1个副本放置在发起写操作请求的数据节点上，实现就近写入数据。如果是来自集群外部的写操作，则从集群内部挑选一台磁盘空间较为充足、CPU不太忙的数据节点，作为第1个副本的存放地。
2. 第2个副本会被放置在与第1个副本不同的机架的数据节点上。
3. 第3个副本会被放置在与第1个副本相同的机架的其他节点上。
4. 如果还有更多的副本，则继续从集群中随机选择数据节点进行存放。

#### 3.3.2.2 数据读取

&emsp;&emsp;HDFS提供了一个API，用于确定一个数据节点所属的机架的ID，客户端可以调用该API获取自己所属机架的ID。  
&emsp;&emsp;当客户端读取数据时，从名称节点获取数据块不同副本的存放位置的列表，列表中包含了副本所在的数据节点，可以调用API确定客户端和这些数据节点所属的机架ID。当发现某个数据块副本对应的机架ID和客户端对应的机架的ID相同时，则优先选择该副本读取数据；如果没有发现，则随机选择一个副本读取数据。

#### 3.3.2.3 数据复制

&emsp;&emsp;HDFS的数据复制采用了 **流水线复制** 的策略，大大提高了数据复制过程的效率。

> **补充：流水线复制**
> &emsp;&emsp;当客户端要向HDFS中写入一个文件时，这个文件会首先被写入本地，并被切分成若干个块，每个块的大小是由HDFS的设定值来决定。每个块都向HDFS集群中的名称节点发起写请求，名称节点会根据系统中各个数据节点的使用情况，选择一个数据节点列表返回给客户端，然后客户端就把数据首先写入列表中的第1个数据节点，同时把列表传给第1个数据节点，当第1个数据节点接收到一个块的数据的时候，将其写入本地，并且向列表中的第2个数据节点发起连接请求，把自己已经接收到的数据和列表传给第2个数据节点，当第2个数据节点接收到数据的时候，将其写入本地，并且向列表中的第3个数据节点发起连接请求，依次类推，列表中的多个数据节点形成一条数据复制的流水线。最后，当文件写完的时候，数据复制也同时完成。

### 3.3.3 数据错误与恢复

#### 3.3.3.1 名称节点出错

&emsp;&emsp;Hadoop采用两种机制来确保名称节点的安全：  
- 把名称节点上的元数据信息同步存储到其他文件系统中；
- 运行一个第二名称节点，当名称节点宕机以后，利用第二名称节点中的元数据信息进行系统恢复。

&emsp;&emsp;但是用第二种方法恢复数据，仍然会丢失部分数据。 因此，一般会把上述两种方法结合使用，当名称节点宕机时，首先到远程挂载的网络文件系统中获取备份的元数据信息，放到第二名称节点上进行恢复，并把第二名称节点作为名称节点来使用。

#### 3.3.3.2 数据节点出错

&emsp;&emsp;每个数据节点会定期向名称节点发送“心跳”信息，向名称节点报告自己的状态。当数据节点发生故障，或者网络发生断网时，名称节点就无法收到来自这些节点的“心跳”信息，这时，这些节点就会被标记为“宕机”，节点上面的数据都会被标记为“不可读”，名称节点不会再给它们发送任何I/O请求。
&emsp;&emsp;当名称节点检查发现，某个数据的副本数量小于冗余因子，就会启动数据冗余复制，为它生成新的副本。

#### 3.3.3.3 数据出错

&emsp;&emsp;**网络传输**和**磁盘错误**等因素都会造成数据错误。客户端在读取到数据后，会采用`md5`和`sha1`对数据块进行校验，以确保读取到正确的数据。在文件被创建时，客户端会对每一个文件块进行信息摘录，并把这些信息写入到同一个路径的隐藏文件里面。
&emsp;&emsp;当客户端读取文件的时候，会先读取该信息文件，然后，利用该信息文件对每个读取的数据块进行校验。如果校验出错，客户端就会请求到另外一个数据节点读取该文件块，并且向名称节点报告这个文件块有错误，名称节点会定期检查并且重新复制这个块。

## 3.4 HDFS的数据读写过程

> ps：读写过程很重要哟，大家注意点又到重点啦，敲黑板✖2

<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.4.1_emoij.png" style="zoom:80%;" /></center>

> 说明：以下图片引用自博客：[翻译经典 HDFS原理讲解漫画](https://blog.csdn.net/hudiefenmu/article/details/37655491)

### 3.4.1 读数据的过程

<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.4.1_read.png" style="zoom:33%;" /></center>

![img](https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.4.1.png)

**具体流程：**
1. 客户端通过 `FileSystem.open()` 打开文件，相应地，在HDFS文件系统中，`DistributedFileSystem`具体实现了`FileSystem`。因此，调用`open()`方法后，`DistributedFileSystem`会创建输入流`FSDataInputStream`，对于HDFS而言，具体的输入流就是`DFSInputStream`。
2. 在`DFSInputStream`的构造函数中，输入流通过`ClientProtocal.getBlockLocations()` 远程调用名称节点，获得文件开始部分的数据块保存位置。对于该数据块，名称节点返回保存该数据块的所有数据节点的地址，同时，根据距离客户端的远近对数据节点进行排序；然后，`DistributedFileSystem`会利用`DFSInputStream`来实例化`FSDataInputStream`，返回给客户端，同时返回了数据块的数据节点地址。
3. 获得输入流`FSDataInputStream`后，客户端调用`read()`函数读取数据。输入流根据前面的排序结果，选择距离客户端最近的数据节点建立连接并读取数据。
4. 数据从该数据节点读到客户端；当该数据块读取完毕时，`FSDataInputStream`关闭与该数据节点的连接。
5. 输入流通过`getBlockLocations()`方法查找下一个数据块（如果客户端缓存中已经包含了该数据块的位置信息，就不需要调用该方法）。
6. 找到该数据块的最佳数据节点，读取数据。
7. 当客户端读取完毕数据的时候，调用`FSDataInputStream`的`close()`函数，关闭输入流。需要注意的是，在读取数据的过程中，如果客户端与数据节点通信时出现错误，就会尝试连接包含此数据块的下一个数据节点。

### 3.4.2 写数据的过程

<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.4.2_write.png" style="zoom:33%;" /></center>

![](https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.4.2.png)

**具体流程：**
1. 客户端通过 `FileSystem.create()` 创建文件。相应地，在HDFS文件系统中， `DistributedFile System`具体实现了`FileSystem`。因此，调用`create()`方法后，`DistributedFileSystem`会创建输出流对象`FSDataOutputStream`，对于`HDFS`而言，具体的输出流就是`DFSOutputStream`。
2. 然后，`DistributedFileSystem`通过RPC远程调用名称节点，在文件系统的命名空间中创建一个新的文件。名称节点会执行一些检查，比如文件是否已经存在，客户端是否有权限创建文件等。检查通过之后，名称节点会构造一个新文件，并添加文件信息。远程方法调用结束后，`DistributedFileSystem`会利用`DFSOutputStream`来实例化`FSDataOutputStream`，返回给客户端，客户端使用这个输出流写入数据。
3. 获得输出流`FSDataOutputStream`以后，客户端调用输出流的`write()`方法向HDFS对应的文件写入数据。
4. 客户端向输出流`FSDataOutputStream`中写入的数据，会首先被分成一个个的分包，这些分包被放入`DFSOutputStream`对象的内部队列。输出流`FSDataOutputStream`会向名称节点申请保存文件和副本数据块的若干个数据节点，这些数据节点形成一个数据流管道。队列中的分包最后被打包成数据包，发往数据流管道中的第一个数据节点，第一个数据节点将数据包发送给第二个数据节点，第二个数据节点将数据包发送给第三个数据节点，这样，数据包会流经管道上的各个数据节点（即**流水线复制策略**）。
5. 因为各个数据节点位于不同机器上，数据需要通过网络发送，因此，为了保证所有数据节点的数据都是准确的，接收到数据的数据节点要向发送者发送“确认包”（ACK Packet）。确认包沿着数据流管道逆流而上，从数据流管道依次经过各个数据节点并最终发往客户端，当客户端收到应答时，它将对应的分包从内部队列移除。不断执行第3~5步，直到数据全部写完。
6. 客户端调用`close()`方法关闭输出流，此时开始，客户端不会再向输出流中写入数据，所以，当`DFSOutputStream`对象内部队列中的分包都收到应答以后，就可以使用`ClientProtocol.complete()`方法通知名称节点关闭文件，完成一次正常的写文件过程。

### 3.4.3 HDFS故障类型和其检测方法

![](https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.4.3_1.png)

#### 3.4.3.1 读写故障的处理

![](https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.4.3_2.png)

#### 3.4.3.2 DataNode 故障处理

![](https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.4.3_3.png)

#### 3.4.3.3 副本布局策略

![](https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.4.3_4.png)

## 3.5 HDFS编程实战

### 3.5.1 实验一：HDFS的使用和管理

#### 3.5.1.1 实验准备

**实验环境：**Linux Ubuntu 20.04    
**前提条件：**

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.3.1的单点部署（详见第2章安装单机版Hadoop）  

#### 3.5.1.2 实验内容

&emsp;&emsp;基于上述前提条件，学习并掌握HDFS的使用和基本命令。

#### 3.5.1.3 实验步骤

##### 1.启动Hadoop的HDFS相关进程

&emsp;&emsp;启动Hadoop的HDFS服务，使用**root用户**执行如下命令：
```shell
cd /opt/hadoop/sbin/
./start-dfs.sh
```

&emsp;&emsp;执行结果如下：
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.1.png" style="zoom:50%;" /></center>

##### 2.查看HDFS进程
&emsp;&emsp;输入`jps`命令可以查看所有的`Java`进程，正常启动后，可以得到如下类似结果：
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.2.png" style="zoom:50%;" /></center>

##### 3.验证HDFS运行状态

&emsp;&emsp;在hdfs上创建一个目录，执行如下命令，验证能够创建成功：
```shell
hadoop fs -mkdir /myhadoop1
```

&emsp;&emsp;如果创建成功，执行如下命令，可查询hdfs文件系统根目录，将看到`/myhadoop1`目录：
```shell
hadoop fs -ls /
```
&emsp;&emsp;执行结果如下：
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.3.png" style="zoom:50%;" /></center>

##### 4.`ls`命令

&emsp;&emsp;列出hdfs文件系统根目录下的目录和文件，执行命令如下：
```shell
hadoop fs -ls /
```

&emsp;&emsp;列出hdfs文件系统所有的目录和文件，执行命令如下：
```shell
hadoop fs -ls -R /
```
&emsp;&emsp;执行结果如下：
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.4.png" style="zoom:50%;" /></center>

##### 5.`put`命令

1）拷贝文件   
&emsp;&emsp;将本地文件上传到hdfs上，命令格式如下：  
```shell
hadoop fs -put <local file> <hdfs file>
```
&emsp;&emsp;其中`<hdfs file>`的父目录必须存在，否则命令执行失败，例如将`/opt/hadoop`的`README.txt`文件上传到hdfs文件系统根目录，命令如下：  
```shell
hadoop fs -put /opt/hadoop/README.txt /
```

2）拷贝目录   
&emsp;&emsp;将本地文件夹上传到hdfs的文件夹中，命令格式如下：  
```shell
hadoop fs -put <local dir> <hdfs dir>
```
&emsp;&emsp;其中`<hdfs dir>`的父目录必须存在，否则命令执行失败。例如将`/opt/hadoop/`的`log`文件夹上传到hdfs文件系统根目录，命令如下：
```shell
hadoop fs -put /opt/hadoop/logs / 
```

3）查看是否拷贝成功   
&emsp;&emsp;查看上传文件或目录是否成功，执行如下命令：  
```shell
hadoop fs -ls <hdfs file/hdfs dir>
```
&emsp;&emsp;例如，查看刚刚上传的`README.txt`文件和`log`目录是否在hdfs根目录下存在，命令如下：  
```shell
hadoop fs -ls /
```
&emsp;&emsp;执行结果如下：  
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.5.png" style="zoom:50%;" /></center>

##### 6.`moveFromLocal`命令

1）拷贝文件或目录  
&emsp;&emsp;将本地文件/文件夹上传到hdfs中，但本地文件/文件夹会被删除，命令格式如下：  
```shell
hadoop fs -moveFromLocal <local src> <hdfs dst>
```

&emsp;&emsp;例如，执行如下命令，上传本地文件/文件夹至hdfs中：
```shell
hadoop fs -moveFromLocal /opt/hadoop/NOTICE.txt /myhadoop1
hadoop fs -moveFromLocal /opt/hadoop/logs /myhadoop1
```

2）查看是否拷贝成功  
&emsp;&emsp;查看上传文件或目录是否成功，执行如下命令：  
```shell
hadoop fs -ls <hdfs file/hdfs dir>
```
&emsp;&emsp;例如，查看刚刚上传的`NOTICE.txt`文件和`log`目录是否在hdfs文件系统的`/myhadoop1`目录下存在，命令如下：  
```shell
hadoop fs -ls /myhadoop1
```
&emsp;&emsp;执行结果如下：  
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.6.png" style="zoom:50%;" /></center>

##### 7.`get`命令

1）拷贝文件或目录到本地  
&emsp;&emsp;将hdfs文件系统中的文件/文件夹下载到本地，命令格式如下：
```shell
hadoop fs -get < hdfs file or dir > < local file or dir>
```
&emsp;&emsp;例如，将hdfs文件系统中`/myhadoop1`目录下的`NOTICE.txt`和`logs`分别下载到本地路径`/opt/hadoop`目录，执行命令如下：
```shell
hadoop fs -get /myhadoop1/NOTICE.txt /opt/hadoop/
hadoop fs -get /myhadoop1/logs /opt/hadoop/
```
**注意：**  
1. 拷贝多个文件或目录到本地时，本地要为文件夹路径
2. `local file`不能和`hdfs file`名字不能相同，否则会提示文件已存在。
3. 如果用户不是**root用户**， `local`路径要使用该用户文件夹下的路径，否则会出现权限问题

2）查看是否成功拷贝到本地  
&emsp;&emsp;查看本地是否在`/opt/hadoop`目录下存在已拷贝完毕的`NOTICE`文件或`logs`目录，执行如下命令：  
```shell
cd /opt/hadoop
ls -l
```
&emsp;&emsp;执行结果如下：  
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.7.png" style="zoom:50%;" /></center>

##### 8. `rm`命令

1）删除一个或多个文件  
&emsp;&emsp;在hdfs文件系统中，删除一个或多个文件，命令格式如下：  
```shell
hadoop fs -rm <hdfs file> ...
```

&emsp;&emsp;例如，删除hdfs文件系统中根目录下的`README.txt`文件，命令如下：  
```shell
hadoop fs -rm /README.txt
```

2）删除一个或多个目录  
&emsp;&emsp;在hdfs文件系统中，删除一个或多个目录，命令格式如下：  
```shell
hadoop fs -rm -r <hdfs dir> ...
```

&emsp;&emsp;例如，删除hdfs文件系统中根目录下的`logs`目录，命令如下：  
```shell
hadoop fs -rm -r /logs
```

3）查看是否删除成功  
&emsp;&emsp;查看刚刚删除的`README.txt`文件和`log`目录是否在hdfs根目录下存在，命令如下：   

```shell
hadoop fs -ls /
```
&emsp;&emsp;如果删除成功，将不会看到`/logs`和`/NOTICE.txt`。

##### 9.`mkdir`命令

1）创建一个新目录  
&emsp;&emsp;使用如下命令，在hdfs文件系统中创建一个目录，该命令只能一级一级的创建目录，如果父目录不存在，则会报错：  
```shell
hadoop fs -mkdir <hdfs path>
```

&emsp;&emsp;例如，在hdfs文件系统的`/myhadoop1`目录下创建`test`目录，命令如下：  
```shell
hadoop fs -mkdir /myhadoop1/test
```

2）创建一个新目录（`-p`选项）  
&emsp;&emsp;使用如下命令，在hdfs文件系统中创建一个目录，如果父目录不存在，则创建该父目录：  
```shell
hadoop fs -mkdir -p <hdfs dir> ...
```

&emsp;&emsp;例如，在hdfs文件系统创建`/myhadoop1/test`目录，命令如下：  
```shell
hadoop fs -mkdir -p /myhadoop2/test
```

3）查询目录  
&emsp;&emsp;查看刚刚创建的`/myhadoop1/test`和`/myhadoop2/test`目录是否存在，命令如下：   

```shell
hadoop fs -ls /
hadoop fs -ls /myhadoop1
hadoop fs -ls /myhadoop2
```
&emsp;&emsp;执行结果如下：  
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.8.png" style="zoom:50%;" /></center>

> ps:命令好多，不过都很硬核，嘤嘤嘤，各位看官，要坚持看下去哟

<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.8_emoji.png" style="zoom:80%;" /></center>

##### 10.`cp`命令

&emsp;&emsp;使用如下命令，在hdfs文件系统上进行文件或目录的拷贝，如果目标文件不存在，则命令执行失败，相当于给文件重命名并保存，源文件还存在：
```shell
hadoop fs -cp <hdfs file or dir>... <hdfs dir>
```

&emsp;&emsp;按照下面的步骤，使用`cp`命令，将`/LICENSE.txt`拷贝到`/myhadoop1`目录下：  
1） 拷贝一个本地文件到HDFS的根目录下  
&emsp;&emsp;将本地`/opt/hadoop`目录下的`LICENSE.txt`文件上传到hdfs文件系统的根目录下，命令如下：  
```shell
hadoop fs -put /opt/hadoop/LICENSE.txt /
```
&emsp;&emsp;查看hdfs文件系统的根目录下的`LICENSE.txt`是否存在，命令如下：
```shell
hadoop fs -ls /
```

2）将此文件拷贝到`/myhadoop1`目录下  
&emsp;&emsp;使用`cp`命令，将hdfs文件系统中根目录下的`LICENSE.txt`文件拷贝到`/myhadoop1`目录下，命令如下：  
```shell
hadoop fs -cp /LICENSE.txt /myhadoop1
```

3）查看`/myhadoop1`目录  
&emsp;&emsp;使用如下命令，查看hdfs文件系统的`/myhadoop1`目录下是否存在`LICENSE.txt`文件：  
```shell
hadoop fs -ls /myhadoop1
```
&emsp;&emsp;执行结果如下：  
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.9.png" style="zoom:50%;" /></center>

##### 11. `mv`命令

&emsp;&emsp;使用如下命令，在hdfs文件系统上进行文件或目录的移动，如果目标文件不存在，则命令执行失败，相当于给文件重命名并保存，源文件不存在；源路径有多个时，目标路径必须为目录，且必须存在：  
```shell
hadoop fs -mv <hdfs file or dir>... <hdfs dir>
```
**注意：**跨文件系统的移动（local到hdfs或者反过来）都是不允许的。  

&emsp;&emsp;按照下面的步骤，使用`mv`命令，将`/myhadoop1/LICENSE.txt`移动到`/myhadoop2`目录下：  
1）移动一个 HDFS文件  
&emsp;&emsp;使用`mv`命令，将hdfs文件系统的`/myhadoop1`目录下的`LICENSE.txt`文件移动到`/myhadoop2`目录下，命令如下：  
```shell
hadoop fs -mv /myhadoop1/LICENSE.txt /myhadoop2
```

2）查询`/myhadoop2`目录  
&emsp;&emsp;使用如下命令，查看hdfs文件系统的`/myhadoop2`目录下是否存在`LICENSE.txt`文件：  
```shell
hadoop fs -ls /myhadoop2
```
&emsp;&emsp;执行结果如下：  
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.10.png" style="zoom:50%;" /></center>

##### 12.`count`命令

&emsp;&emsp;使用如下命令，统计hdfs对应路径下的目录个数，文件个数，文件总计大小：   
```shell
hadoop fs -count <hdfs path>
```

&emsp;&emsp;例如，查看`/myhadoop1/logs`目录下的目录个数，文件个数，文件总计大小，命令如下：  
```shell
hadoop fs -count /myhadoop1/logs
```
&emsp;&emsp;执行结果如下：  
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.12.png" style="zoom:50%;" /></center>

##### 13. `du`命令

- 显示hdfs对应路径下每个文件夹和文件的大小
```shell
hadoop fs -du <hdsf path>
```

- 显示hdfs对应路径下所有文件大小的总和
```shll
hadoop fs -du -s <hdsf path>
```

- 显示hdfs对应路径下每个文件夹和文件的大小，文件的大小用方便阅读的形式表示，例如用64M代替67108864
```shell
hadoop fs -du -h <hdsf path>
```

&emsp;&emsp;例如，执行如下命令，可以查看hdfs文件系统`/myhadoop2`目录下的每个文件夹和文件的大小、所有文件大小的总和：  
```shell
hadoop fs -du /myhadoop2
hadoop fs -du -s /myhadoop2
hadoop fs -du -h /myhadoop2
hadoop fs -du -s -h /myhadoop2
```
&emsp;&emsp;执行结果如下：  
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.13.png" style="zoom:50%;" /></center>

&emsp;&emsp;**执行结果说明：**  
- 第一列：表示该目录下总文件大小
- 第二列：表示该目录下所有文件在集群上的总存储大小，该大小和副本数相关，设置的默认副本数为3 ，所以第二列的是第一列的三倍 （第二列内容 = 文件大小 $\times$ 副本数）
- 第三列：表示查询的目录

<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.14.png" style="zoom:50%;" /></center>

##### 14.`setrep`命令

&emsp;&emsp;使用如下命令，改变一个文件在hdfs文件系统中的副本个数，数字3表示所设置的副本个数，其中，`-R`选项可以对一个目录下的所有目录和文件递归执行改变副本个数的操作：  
```shell
hadoop fs -setrep -R 3 <hdfs path>
```

&emsp;&emsp;例如，对hdfs文件系统中`/myhadoop1`目录下的所有目录和文件递归执行，设置为3个副本，命令如下：  
```shell
hadoop fs -setrep -R 3 /myhadoop1
```
&emsp;&emsp;执行结果如下：  
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.15.png" style="zoom:50%;" /></center>

##### 15. `stat`命令
&emsp;&emsp;使用如下命令，查看对应路径的状态信息： 
```shell
hdoop fs -stat [format] < hdfs path >
```
&emsp;&emsp;其中，`[format]`可选参数有：
- `%b`：文件大小
- `%o`：Block大小
- `%n`：文件名
- `%r`：副本个数
- `%y`：最后一次修改日期和时间

&emsp;&emsp;例如，查看hdfs文件系统中`/myhadoop2/LICENSE.txt`文件的大小，命令如下：  
```shell
hadoop fs -stat %b /myhadoop2/LICENSE.txt
```
&emsp;&emsp;执行结果如下：
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.16.png" style="zoom:50%;" /></center>

##### 16.`balancer`命令

&emsp;&emsp;该命令主要用于，当管理员发现某些`DataNode`保存数据过多，某些`DataNode`保存数据相对较少，可以使用如下命令手动启动内部的均衡过程：
```shell
hadoop balancer
或
hdfs balancer
```

##### 17. `dfsadmin`命令

&emsp;&emsp;该命令主要用于管理员通过`dfsadmin`管理HDFS：  

1）使用`-help`参数，查看相关的帮助：  
```shell
hdfs dfsadmin -help
```

2） 使用`-report`参数，查看文件系统的基本数据：  
```shell
hdfs dfsadmin -report
```

&emsp;&emsp;执行结果如下：
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.17.png" style="zoom:50%;" /></center>

3） 使用`-safemode`参数，操作安全模式：  
```shell
hdfs dfsadmin -safemode <enter | leave | get | wait>
```
其中：
- `enter`：进入[安全模式](https://blog.csdn.net/u012538609/article/details/109356665)
- `leave`：离开安全模式
- `get`：查看是否开启安全模式
- `wait`：等待离开安全模式

&emsp;&emsp;例如，进入安全模式，执行命令如下：  
```shell
hdfs dfsadmin -safemode enter
```
&emsp;&emsp;执行结果如下：
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.18.png" style="zoom:50%;" /></center>

##### 18. 其他命令

![](https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.19.png)

###### 18.1 `cat`命令

&emsp;&emsp;使用`cat`命令，查看hdfs文件系统中文本文件的内容，例如，查看根目录下的`deom.txt`文件内容：
```shell
 hadoop fs -cat /demo.txt
 hadoop fs -tail -f /demo.txt
```

&emsp;&emsp;当使用`hadoop fs -tail -f`命令后，终端会根据文件描述符进行追踪，当文件改名或被删除，追踪停止。终端操作如下：
- 此时要想暂停刷新，使用`Ctrl+S`暂停终端，`S`表示`sleep`
- 若想要继续刷新终端，使用`Ctrl+Q`，`Q`表示`quiet`
- 若想退出`tail`命令，直接使用`Ctrl+C`，也可以使用`Ctrl+Z`
  `Ctrl+C`和`Ctrl+Z`都是中断命令，当他们的作用却不一样的：
  1. `Ctrl+C`比较暴力，就是发送`Terminal`到当前的程序，比如正在运行一个查找功能，文件正在查找中，使用`Ctrl+C`会强制结束当前这个进程
  2. `Ctrl+Z`则会将当前程序挂起，暂停执行这个程序，比如`mysql`终端下，需要跳出来执行其他的文件操作，又不想退出`mysql`终端（因为下次还需要输入用户名密码进入，很麻烦），于是可以使用`Ctrl+Z`将`mysql`挂起，然后进行其他操作，输入`fg`回车可以回到`mysql`终端，担任也可以挂起很多进程到后台，执行`fg <编号>`就能将挂起的进程返回到当前的终端。配合`bg`和`fg`命令能更方便的进行前后台切换

###### 18.2 `appendToFile`命令

&emsp;&emsp;将本地文件内容追加到hdfs文件系统中的文本文件里，命令格式如下：  
```shell
hadoop fs -appendToFile <local file> <hdfs file>
```

&emsp;&emsp;执行示例如下：  
<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3_ex1.21.png" style="zoom:50%;" /></center>

###### 18.3 `chown`命令
&emsp;&emsp;使用`chown`命令，修改hdfs文件系统中文件的读、写、执行的权限，命令示例如下：  
```shell
hadoop fs -chown user:group /datawhale
hadoop fs -chmod 777 /datawhale
```
其中，参数说明如下：
- `chown`：定义谁拥有文件
- `chmod`：定义可以对该文件做什么

## 3.5 本章小结

&emsp;&emsp;HDFS原来是Apache Nutch搜索引擎的一部分，后来独立出来作为一个Apache子项目，并和MapReduce一起成为Hadoop的核心组成部分。本章介绍了分布式文件系统的概念，并从分布式文件系统出发，引入了HDFS。作为Hadoop和其他组件的数据存储层，HDFS提供了强大可靠的数据容错处理、自动恢复的机制以及多副本策略。  
&emsp;&emsp;本章通过实验，讲解了在Linux系统中的HDFS文件系统基本命令，通过这些命令可以进一步熟悉HDFS分布式文件系统的使用。  

> ps：看到内容量，大家应该也知道这节课很硬核了，对吧！的确如此，HDFS是Hadoop的基石之一，希望大家能够好好理解其中的理论知识，并在此基础上进行编程实践，好记性不如烂笔头，好好敲代码做编程才是正道！！！也希望大家别怕命令多，多敲敲就会了。
>
> 嘿嘿，这边又有一个看网课敲代码学傻的人\~\~\~\~

<center><img src="https://github.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch3.5.png" style="zoom:80%;" /></center>