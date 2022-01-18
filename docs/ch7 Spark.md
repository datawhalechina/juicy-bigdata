# 第七章：Spark

> 王嘉鹏，shenhao

## 7.0 引言
我们再次拿出5.1章节中辣椒酱的demo（没印象的同学移步[这里]()），来简单看下Spark和MapReduce在处理问题的方式上有什么区别。

在了解这个之前，必须要了解什么是内存和磁盘。**内存和磁盘两者都是存储设备**，但内存储存的是我们正在使用的资源，磁盘储存的是我们暂时用不到的资源。
可以把磁盘理解为一个仓库，而内存是进出这个仓库的通道。仓库（磁盘）很大，而通道（内存）很小，通道就很容易塞满。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.0_1.png" style="zoom: 50%;" /></center>

假设把磁盘作为冰箱，内存为做饭时的操作台：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.0_2.png" style="zoom: 100%;" /></center>

Mapreduce每一个步骤发生在内存中但产生的中间值（溢写文件）都会写入在磁盘里，下一步操作时又会将这个中间值merge到内存中，如此循环，直到最终完成计算。

而对于Spark， Spark的每个步骤也是发生在内存之中，但产生的中间值会直接进入下一个步骤，直到所有的步骤完成之后才会将最终结果保存进磁盘。所以在使用Spark做数据分析能少进行很多次相对没有意义的读写，节省大量的时间。当步骤很多时，Spark的优势就体现出来了。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.0_3.png" style="zoom: 100%;" /></center>

## 7.1 Spark 概述

### 7.1.1 Spark 诞生
在Hadoop出现之前，分布式计算都是**专用系统**，只能用来处理某一类的计算，比如进行大规模的排序。这样的系统无法复用到其他大数据计算场景。

而Hadoop MapReduce出现后，使得大数据计算通用编程成为可能，只要遵循MapReduce编程模型编写业务处理代码，就可以运行在Hadoop分布式集群上，而无需关心分布式计算怎样完成。

紧接着，我们经常看到的说法是：`MapReduce 虽然已经可以满足大数据的应用场景，但是其执行速度和编程复杂度并不让人们满意。于是AMP lab的Spark应运而生`。

我们事后因果规律的分析上，往往容易**把结果当作了原因**  ---觉得是因为MapReduce执行的很慢，所以才去发明和使用Spark。

但事实上，在Spark出现之前，MapReduce并没有让人怨声载道，一方面Hive这些工具将常用的MapReduce编程进行了封装，转化为了更易于编写的SQL形式；一方面MR已经将分布式编程极大的进行了简化。

而当Spark出现后，性能比MapReduce快了100多倍。因为有了Spark，才对MapReduce不满，才觉得MapReduce慢。而不是觉得MapReduce慢，所以诞生了Spark。真实世界中的因果关系并非是顺承的，**我们常常意识不到问题的存在，直到有大神解决了这些问题**。


附上Spark框架发展历史中**重要的时间点**：
<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.1.png" style="zoom: 80%;" /></center>



### 7.1.2 Spark 与 Hadoop、MapReduce、HDFS的关系

那接下来的问题是，Spark自己有自己的体系，那么其和Hadoop之间的关系是什么呢？

我们先来回忆下Hadoop处理大数据的流程，Hadoop 来处理大数据，通常是这样的顺序：首先从 **HDFS** 读取输入数据；接着**在 Map 阶段**使用用户定义的 mapper function, 然后把结果写入磁盘；**在 Reduce 阶段**，从各个处于 Map 阶段的机器中读取 Map 计算的中间结果，使用用户定义的 reduce function, 通常最后**把结果写回 HDFS**。

而在这个过程中， 至少进行了三次数据读写，Hadoop处理大数据的流程高度依赖磁盘读写，那么在数据处理上就出现了瓶颈，面对更复杂的计算逻辑的处理任务时，Hadoop存在很大局限。

Spark在这样的背景下产生，其不像Hadoop一样采取磁盘读写，而是**基于性能更高的内存存储来进行数据存储和读写**（这里说的是计算数据的存储，而非持久化的存储）。但是Spark并非完美，其缺乏对数据存储这一块的支持--没有分布式文件系统，必须要依赖外部的数据源，这个依赖可以是Hadoop系统的HDFS，也可以是其他的分布式文件系统，也可以是mysql或本地文件系统。

基于以上分析，我们可以得出**结论**：Hadoop 和 Spark 两者都是大数据框架，但是各自存在的目的不尽相同。Hadoop 实质上更多是一个**分布式数据基础设施**，它将巨大的数据集分派到一个集群中的多个节点**进行存储**，也有**计算处理**的功能。Spark则是一个专门用来**对那些分布式存储的大数据进行处理的工具**，它并不会进行分布式数据的存储，可以部分看做是MapReduce的竞品（**准确的说是Spark Core**）。可以总结为下图：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.2_1.png" style="zoom: 100%;" /></center>

### 7.1.3 Spark 生态体系
spark是一个用来实现快速而通用的集群计算的平台。

1. 速度方面：spark的一个主要特点就是能在内存中进行计算，因此速度要比mapreduce计算模型要更加高效，可以面向海量数据进行分析处理；
2. 通用方面：Spark 框架可以针对任何业务类型分析进行处理，比如SparkCore离线批处理、SparkSQL交互式分析、SparkStreaming和StructuredStreamig流式处理及机器学习和图计算都可以完成；

以 Spark 为基础，有支持 SQL 语句的 Spark SQL，有支持流计算的 Spark Streaming，有支持机器学习的 MLlib，还有支持图计算的GraphX。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.3_1.png" style="zoom: 100%;" /></center>

利用这些产品，Spark 技术栈支撑起大数据分析、大数据机器学习等各种大数据应用场景。


## 7.2 Spark 编程模型
### 7.2.1 RDD 概述

RDD 是 Spark 的核心概念，是弹性数据集（Resilient Distributed Datasets）的缩写。RDD 既是 Spark 面向开发者的编程模型，又是 Spark 自身架构的核心元素。

大数据计算就是在大规模的数据集上进行一系列的数据计算处理。类比MapReduce，针对输入数据，R将计算过程分为两个阶段，一个 Map 阶段，一个 Reduce 阶段，可以理解成是**面向过程**的大数据计算。我们在用MapReduce 编程的时候，思考的是，如何将计算逻辑用 Map 和 Reduce 两个阶段实现，map 和 reduce 函数的输入和输出是什么。

而 Spark 则直接针对数据进行编程，将大规模数据集合抽象成一个 RDD 对象，然后在这个 RDD 上进行各种计算处理，得到一个新的 RDD，继续计算处理，直到得到最后的结果数据。所以 **Spark 可以理解成是面向对象的大数据计算**。我们在进行 Spark 编程的时候，思考的是**一个 RDD 对象需要经过什么样的操作，转换成另一个 RDD 对象，思考的重心和落脚点都在 RDD 上**。

### 7.2.2 RDD 定义

**RDD**是**分布式内存**的一个抽象概念，是只读的记录分区的集合，能横跨集群所有节点进行并行计算。

spark建立在抽象的RDD上，使得它可用一致的方式处理大数据不同的应用场景，把所有需要处理的数据转化为RDD，然后对RDD进行一系列的算子运算，从而得到结果，且提供了丰富的API来操作数据。

### 7.2.3 RDD 五大特性

RDD共有五大特性，我们将对每一种特性进行介绍：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.2.4_1.jpg" style="zoom: 100%;" /></center>

**一、分区**

​	    分区的含义是允许Spark将计算**以分区为单位**，分配到多个机器上进行并行计算。在某些情况下，比如从HDFS读取数据时，Spark会使用位置信息，将工作发给靠近数据的机器，减少了跨网络传输的数据量。

**二、可并行计算**

​        RDD的每一个分区都会被一个计算任务task处理，每个分区有计算函数（具体执行的计算算子），计算函数以分片为基本单位进行并行计算，**RDD的分区数决定着并行计算的数量**。

**三、依赖关系**

​	    首先**依赖关系列表**会告诉Spark如何从必要的输入来构建RDD。当遇到错误需要重算时，Spark可以根据这些依赖关系重新执行操作，以此来重建出RDD。依赖关系赋予了RDD**容错**的弹性。

**四、Key-Value数据的RDD分区器**

​	    想要理解分区器的概念，我们需要先来类比MapReduce任务。MR 任务的 map 阶段的处理结果会进行分片（也可以叫分区，这个分区不同于上面的分区），分片的数量就是 reduce task 的数量。而**具体分片的策略由分区器 Partitioner** 决定，Spark 目前支持 Hash 分区（默认分区）和 Range 分区，用户也可以自定义分区。

​	    总结来说，Partitioner决定了RDD如何分区。通过Partitioner来决定下一步会产生多少并行的分片，及当前并行Shuffle输出的并行数据，来使得Spark可以控制数据在不同节点上分区。

​	    值得注意的是，其本身**只针对于key-value的形式**（k-v形式的RDD才有Partitioner属性），Partitioner会从0到numPartitions-1区间内映射每一个key到partition ID。

**五、每个分区都有一个优先位置列表**

​        大数据计算的基本思想是："移动计算而非移动数据"。Spark本身在进行任务调度时，需要尽可能的将任务分配到处理数据的数据块所在的具体位置。因此在具体计算前，就需要知道它运算的数据在什么地方。故分区位置列表会存储每个Partition的优先位置，如果读的时HDFS文件，这个列表保存的就是每个分区所在的block块的位置。

### 7.2.4 RDD 操作函数

RDD的操作函数包括两种：转换（transformation）函数 和 执行（action）函数。

一种是转换（transformation）函数，这种函数的返回值还是RDD；另一种是执行（action）函数，这种函数不再返回 RDD。

RDD 中定义的转换操作函数有：比如有计算map(func)、过滤filter(func)、合并数据集union(otherDataset)、根据 Key 聚合reduceByKey(func, [numPartitions])、连接数据集join(otherDataset, [numPartitions])、分组groupByKey([numPartitions]) 等十几个函数。

跟 MapReduce 一样，Spark 也是**对大数据进行分片计算**，Spark 分布式计算的数据分片、任务调度都是**以 RDD 为单位展开的**，每个 RDD 分片都会分配到一个执行进程去处理。

RDD 上的**转换操作分成两种**：一种转换操作产生的 RDD 不会出现新的分片，比如map、filter 等，也就是说一个 RDD 数据分片，经过 map 或者 filter 转换操作后，结果还在当前分片。就像你用 map 函数对每个数据加 1，得到的还是这样一组数据，只是值不同。实际上，Spark 并不是按照代码写的操作顺序去生成 RDD，比如rdd2 =rdd1.map(func)这样的代码并不会在物理上生成一个新的 RDD。物理上，Spark 只有在产生新的 RDD 分片时候，才会真的生成一个 RDD，Spark 的这种特性也被称作惰性计算

1. 一种转换操作产生的 RDD **不会出现新的分片**，比如map、filter 等。一个 RDD 数据分片，经过 map 或者 filter 转换操作后，其结果还在当前分片。就像你用 map 函数对每个数据加 1，得到的还是这样一组数据，只是值不同。实际上，Spark 并不是按照代码写的操作顺序去生成 RDD，比如rdd2 =rdd1.map(func)这样的代码并不会在物理上生成一个新的 RDD。**物理上，Spark 只有在产生新的 RDD 分片时候，才会真的生成一个 RDD**，Spark 的这种特性也被称作惰性计算。
2. 另一种转换操作产生的 RDD 则**会产生新的分片**，比如reduceByKey，来自不同分片的相同 Key 必须聚合在一起进行操作，这样就会产生新的 RDD 分片。实际执行过程中，**是否会产生新的 RDD 分片，并不是根据转换函数名就能判断出来的。**

Spark 应用程序代码中的 RDD 和 Spark 执行过程中生成的物理 RDD不是一一对应的。





## 7.3 Spark 架构原理

Spark同 MapReduce一样，遵循着 **移动计算而非移动数据** 这一大数据计算基本原则。MR是通过固定的Map 与 Reduce 分阶段计算，而Spark 的计算框架通过DAG来实现计算。

### 7.3.1 Spark 计算阶段

MapReduce中，一个应用一次只运行一个 map 和一个 reduce，而Spark 可以根据应用的复杂程度，将过程分割成更多的计算阶段（stage），这些计算阶段组成一个有向无环图 DAG，接着 Spark 任务调度器根据 **DAG 的依赖关系** 执行计算阶段（stage）。

Spark 比MapReduce 快 100 多倍。因为某些机器学习算法可能需要进行大量的迭代计算，产生数万个计算阶段，这些计算阶段在一个应用中处理完成，而不是像 MapReduce 那样需要启动数万个应用，因此极大地提高了运行效率。

DAG 是有向无环图，即是说**不同阶段的依赖关系是有向**的，计算过程只能沿着依赖关系方向执行，被依赖的阶段执行完成之前，依赖的阶段不能开始执行，同时，这个依赖关系不能有环形依赖，否则就成为死循环了。下面这张图描述了一个典型的 Spark 运行DAG 的不同阶段：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.1_1.png" style="zoom: 50%;" /></center>

从图上看，整个应用被切分成 3 个阶段，阶段 3 需要依赖阶段 1 和阶段 2，阶段 1 和阶段2 互不依赖。Spark 在执行调度的时候，先执行阶段 1 和阶段 2，完成以后，再执行阶段3。如果有更多的阶段，Spark 的策略也是一样的。**Spark 大数据应用的计算过程**为：Spark会根据程序初始化 DAG，由DAG再建立依赖关系，然后根据依赖关系顺序执行各个计算阶段。

**Spark 作业调度执行核心是 DAG**，由DAG可以得出 **整个应用就被切分成哪些阶段** 以及 **每个阶段的依赖关系**。之后再根据每个阶段要处理的数据量生成相应的任务集合（TaskSet），每个任务都分配一个任务进程去处理。

那DAG是怎么来生成的呢？在Spark中，DAGScheduler组件负责应用 DAG 的生成和管理，DAGScheduler 根据程序代码生成 DAG，然后将程序分发到分布式计算集群，按计算阶段的先后关系调度执行。

### 7.3.2 如何划分计算阶段

图上这个DAG对应的Spark伪代码可以表示为：

```python
rddB = rddA.groupBy(key)
rddD = rddC.map(func)
rddF = rddD.union(rddE)
rddG = rddB.join(rddF)
```

可以看到例子有4个转换函数，但是只有3个阶。看起来并不是RDD上的每个转换函数都会生成一个计算阶段。那**RDD的计算阶段是怎样来进行划分**的呢？

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.2_1.png" style="zoom: 50%;" /></center>

再看下上图，我们发现了一个规律，当 **RDD 之间的转换连接线呈现多对多交叉连接**的时候，就会产生新的阶段。图中每个 RDD 里面都包含多个小块，每个小块 表示 RDD 的一个分片。

**一个RDD表示一个数据集，一个数据集中的多个数据分片需要进行分区传输，写入到另一个数据集的不同分片中**。这种涉及到数据分区交叉传输的操作，是否在MapReduce中也有印象？我们来回忆下MapReduce的过程：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.2_2.png" style="zoom: 100%;" /></center>

MR把这种从数据集跨越，由多个分区传输的过程，叫做**shuffle**。同样，Spark也需要通过shuffle将数据进行重新组合，把相同key的数据放一起。因为会进行新的聚合、关联等操作，所以Spark每次Shuffle都会产生新的计算阶段。而每次计算时，需要的数据来源于前面一个或多个计算阶段产生的数据，所以计算阶段需要依赖关系，必须等待前面的阶段执行完毕后，才能进行Shuffle。

**Spark中计算阶段划分的依据是Shuffle**，而不是操作函数的类型。有的函数有Shuffle，有时候没有。比如本小节第一张图中，RDD B和RDD F进行Join后，得到RDD G。**RDD B不需要Shuffle**，因为RDD B在上一个阶段中，已经进行了数据分区，分区数目和分区key不变，就不需要进行Shuffle。而RDD F得分区数目不同，就需要进行Shuffle。Spark把**不需要shuffle**的依赖，叫做**窄依赖**。**需要shuffle**的依赖，叫做**宽依赖**。shuffle是spark最重要的一个环节，只有通过shuffle，相关数据才能互相计算，从而构建起复杂的应用逻辑。

那么Spark和MapReduce一样，都进行了shuffle，为什么Spark会比MR更高效呢？

我们从**本质和存储方式**两个方面，对Spark和MR进行比较：

- **本质上**：Spark可以算是一种MapReduce计算模型的不同实现，Hadoop MR根据Shuffle将大数据计算分为Map和Reduce两个阶段。而Spark 更流畅，将前一个的Reduce和后一个的Map做了连接，当作一个阶段持续来进行计算，从而形成了一个更高效流畅的计算模型。其本质仍然是Map和Reduce。但是这种多个计算阶段依赖执行的方案可以有效减少对HDFS的访问（落盘），减少作业的调度执行次数，因此执行速度也更快。

- **存储方式**：MR主要使用磁盘存储shuffle过程的数据，而Spark优先使用内存进行数据存储（RDD也优先存于内存）。这也是Spark性能比Hadoop高的另一个原因。

### 7.3.3 Spark 作业管理

本小节主要来说明 作业、计算阶段、任务的依赖和时间先后关系。

Spark的RDD有两种函数：转换函数和action函数。action函数调用之后不再返回RDD。Spark的DAGScheduler 遇到shuffle时，会生成一个计算阶段，在遇到action函数时，会生成一个作业（job）。RDD里的每个数据分片，Spark都会创建一个计算任务去处理，故一个计算阶段会包含多个计算任务（task）。

一个作业至少包含一个计算阶段，每个计算阶段由多个任务组成，这些任务task组成一个任务集合。

DAGScheduler根据代码生成DAG图，Spark的任务调度以任务为单位进行分配，将任务分配到分布式集群的不同机器上进行执行。

### 7.3.4 Spark 执行过程

Spark支持多种部署方案（Standalone、Yarn、Mesos等），不同的部署方案核心功能和运行流程基本一样，只是不同组件角色命名不同。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.4_1.png" style="zoom: 100%;" /></center>

**首先**，Spark 在自己的 JVM 进程里启动应用程序，即 Driver 进程。启动后driver调用SparkContext 初始化执行配置和输入数据。再由SparkContext 启动 DAGScheduler 构造执行的 DAG 图，切分成计算任务这样的最小执行单位。

**接着**Driver 向 Cluster Manager 请求计算资源，用于 DAG 的分布式计算。ClusterManager 收到请求以后，将 Driver 的主机地址等信息通知给集群的所有计算节点Worker。

**最后**，Worker 收到信息以后，根据 Driver 的主机地址，跟 Driver 通信并注册，然后根据自己的空闲资源向 Driver 通报自己可以领用的任务数。Driver 根据 DAG 图开始向注册的Worker 分配任务。     

## 7.4 Spark 编程实战

### 7.4.1 实验一：Spark Local模式的安装

#### 7.4.1.1 实验准备

**实验环境：**Linux Ubuntu 20.04  
**前提条件：**  

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.0.0的单点部署（详见第2章安装单机版Hadoop）

#### 7.4.1.2 实验内容

&emsp;&emsp;基于上述前提条件，完成Spark Local模式的安装。

✅**厦门大学数据库实验室参考教程**：[GettingStarted](http://dblab.xmu.edu.cn/blog/2501-2/)

#### 7.4.1.3 实验步骤

##### 1.解压安装包

&emsp;&emsp;通过官网下载地址（✅**官网下载地址**：[Spark下载](https://spark.apache.org/downloads.html)），下载[spark-3.2.0-bin-without-hadoop.tgz](https://www.apache.org/dyn/closer.lua/spark/spark-3.2.0/spark-3.2.0-bin-without-hadoop.tgz)。

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex1.1.png)

&emsp;&emsp;将安装包放置本地指定目录，如`/data/hadoop/`下。解压安装包至`/opt`目录下，命令如下：  

```shell
sudo tar -zxvf /data/hadoop/spark-3.2.0-bin-without-hadoop.tgz -C /opt/
```

&emsp;&emsp;解压后，在`/opt`目录下会产生`spark-3.2.0-bin-without-hadoop`文件夹。

##### 2.更改文件夹名和所属用户

&emsp;&emsp;使用`mv`命令，将文件名改为`hive`，命令如下：  

```shell
sudo mv /opt/spark-3.2.0-bin-without-hadoop/ /opt/spark
```

&emsp;&emsp;使用`chown`命令，更改文件夹及其下级的所有文件的所属用户和用户组，将其改为`datawhale`用户和`datawhale`用户组，命令如下：  

```shell
sudo chown -R datawhale:datawhale /opt/spark/
```

##### 3.修改Spark的配置文件spark-env.sh

&emsp;&emsp;进入`/opt/spark/conf`目录下，将`spark-env.sh.template`文件拷贝一份命名为`spark-env.sh`，命令如下：  
```shell
cd /opt/spark/conf
cp ./spark-env.sh.template ./spark-env.sh
```

&emsp;&emsp;编辑spark-env.sh文件，命令如下：  
```shell
vim spark-env.sh
```

&emsp;&emsp;在第一行添加如下配置信息：  
```shell
export SPARK_DIST_CLASSPATH=$(/opt/hadoop/bin/hadoop classpath)
```

&emsp;&emsp;配置完成后就可以直接使用，不需要像Hadoop运行启动命令。

##### 4.设置Spark的环境变量

&emsp;&emsp;将`SPARK_HOME`环境变量设置为`/opt/spark`，作为工作目录，打开系统环境变量配置文件，命令如下：  

```shell
sudo vim /etc/profile
```

&emsp;&emsp;在文件末尾，添加如下内容：  

```shell
# spark
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin
```

&emsp;&emsp;使用`Shift+:`，输入`wq`后回车，保存退出。运行下面命令使环境变量生效：

```shell
source /etc/profile
```

##### 5.检验Spark是否成功部署

&emsp;&emsp;通过运行Spark自带的示例，验证Spark是否安装成功，命令如下：  
```shell
cd /opt/spark
bin/run-example SparkPi
```

&emsp;&emsp;执行时会输出非常多的运行信息，输出结果不容易找到，可以通过 grep 命令进行过滤（命令中的 2>&1 可以将所有的信息都输出到 stdout 中，否则由于输出日志的性质，还是会输出到屏幕中），命令如下：  
```shell
cd /opt/spark
bin/run-example SparkPi 2>&1 | grep "Pi is"
```
&emsp;&emsp;过滤后的运行结果如下图示，可以得到$\pi$的 5 位小数近似值：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex1.2.png)

&emsp;&emsp;至此，`Spark`安装部署完成，本次实验结束啦！

### 7.4.2 实验二：通过 WordCount 看Spark RDD执行流程

#### 7.4.2.1 实验准备

**实验环境：**Linux Ubuntu 20.04  
**前提条件：**  

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.0.0的单点部署（详见第2章安装单机版Hadoop）
3. 完成Spark Local模式的部署（详见本章实验一：Spark Local模式的安装）

#### 7.4.2.2 实验内容

&emsp;&emsp;基于上述前提条件，通过 WordCount 看Spark RDD执行，进一步理解Spark RDD执行的逻辑。

#### 7.4.2.3 实验步骤

WordCount在MapReduce章节已经提过。这里再次通过WordCount的案例：编写单词记数代码，从数据流动的角度来详细看Spark RDD是如何进行数据处理的。

##### 1.文本数据准备

首先建立一个文本文件helloSpark ，将文本文件放到文件目录 data/wordcount/中。helloSpark 。txt文本内容如下：

```
Hello Spark Hello Scala
Hello Hadoop
Hello Flink
Spark is amazing
```

**待补图**

##### 2.代码步骤

**第一步**：创建Spark的配置对象SparkConf，设置Spark程序运行时的配置信息，如：通过setMaster设置程序要链接的Spark集群的master的url，如果设置为local，则代表Spark程序在本地运行。

```scala
val conf = new SparkConf() // 创建SparkConf对象
conf.setAppName("First Spark App") //设置app应用名称，在程序运行的监控解面可以看到名称
conf.setMaster("local") //本地模式运行
```

第二步：创建SparkContext对象，SparkContext是Spark程序所有功能的唯一入口。不管是使用scala，py都必须有一个SparkContext。

```scala
val sc = new SparkContext(conf) // 创建SparkContext对象，通过传入SparkConf实例来定制Spark运行的具体参数和配置信息
```

**SparkContext的核心作用**：初始化Spark应用程序，运行所需要的核心组件，包括DAGScheduler，TaskScheduler，SchedulerBackend，同时还会负责Spark程序往Master注册程序等，SparkContext是整个Spark应用程序中至关重要的一个对象。

**第三步**：根据具体的数据来源，如HDFS，通过SparkContext来创建RDD。创建的方式有三种：根据外部数据来源，根据Scala集合，由其他的rdd操作转换。数据会被rdd划分为一系列的partitions，分配到每个Partition的数据属于一个task的处理范畴。

```scala
val lines = sc.textFile("dataq/helloSpark.txt", 1) // 读取本地文件并设置为一个Partition
```

**第四步**：对初始的rdd进行transformation级别的处理，如通过map，filter等高阶函数等的编程，进行具体的数据计算。

1. 将每一行的字符串拆分为单个单词

```scala
val words = lines.flatMap{line => line.split(" ")} // 把每行字符串进行单词拆分，把拆分结果通过flat合并为一个大的单词集合
```

2. 在单词拆分的基础上对每个单词实例计数为1，也就是word ->（word, 1）

```scala
val pairs = words.map{word => (word, 1)}
```

3. 在每个单词实例计数为1基础之上统计每个单词在文件中出现的总次数。

```scala
val wordCountOdered = pairs.reduceByKey(_+_).map(pair=>(pair._2, pair._1)).sortByKey(false).map(pair => (pair._2, pair._1))
```

**第五步**：展示数据

```scala
wordCountsOrdered.collect.foreach(wordNumberPair => println(wordNumberPair._1 + "：" + wordNumberPair._2))
```

运行程序，结果如下：

**（图待补）**

#### 7.4.2.4 WordCount在RDD的运行原理

ch7.4.2.4_1.png

一、 **textFile**

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.4.2.4_1.png" style="zoom: 100%;" /></center>

textFile：在textFile 操作产生了两个 RDD：**HadoopRDD** 和 **MapPartitionRDD**。

1. **HadoopRDD** 

在这里之所以会先产生 HadoopRDD，是因为处理数据的第一步：我们当然是先要从 HDFS 中抓取数据了，所以会先产生 HadoopRDD。HadoopRDD 会从 HDFS 上读取分布式文件，并将输入文件以数据分片的方式存在于集群中。数据分片就是把要处理的数据分成不同的部分。

假如我们集群现在有 4 个节点，于是我们将数据分成 4 个数据分片 (当然，这是一种粗略的划分)，Hello Spark在第一台机器，Hello Hadoop在第二台机器，Hello Flink在第三台机器，Spark is amazing在第四台机器。HadoopRDD 会帮助我们从磁盘上读取数据，在计算的时候会将数据放在内存中，并且会以分布式的方式放在内存中。

在默认情况下，Spark 分片的策略，分片的大小与存储数据的 block 块的大小是相同的。假设我们现在有 4 个数据分片 (partition)，每个数据分片有 128M 左右。这里描述为"左右"的原因是，分片记录可能会跨越两个Block来存储，如果最后一条数据跨了两个Block，那么分片的时候会把最后一条数据都放在前面的一个分片中，此时分片大小会大于128M（Block块大小）。

2. **MapPartitionsRDD**

MapPartitionsRDD 是基于 HadoopRDD 产生的 RDD，MapPartitionsRDD 将 HadoopRDD 产生的数据分片 (partition) 去掉相应行的 key，只留 value。

产生RDD的个数与操作并不一一对应。在textFile 操作产生了 2 个 RDD，Spark 中一个操作可以产生一个或多个 RDD。

二、 **flatMap**

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.4.2.4_2.png" style="zoom: 100%;" /></center>

flatMap 操作产生了一个 MapPartitionsRDD，MapPartitionsRDD 在这里面的作用：是对每个 Partition 中的每一行内容进行单词切分并合并成一个大的单词实例的集合。

三、 **Map**

四、 **reduceByKey**

五、 **输出**



## 7.5 本章小结

&emsp;&emsp;在本章的学习中，主要介绍`Spark`的编程模型：`RDD`的定义、特性和操作函数，接着从`Spark`的架构原理出发，简述了`Spark`的计算阶段、作业管理和执行过程。最后通过实验，介绍了`Spark`的安装和`WordCount`实例在`RDD`的数据流向。如果想要更多的了解Spark SQL和Scala API的内容，可以参考本仓库[experiments](https://github.com/shenhao-stu/Big-Data/tree/master/experiments)目录下的笔记[Spark SQL的基本使用](https://github.com/shenhao-stu/Big-Data/blob/master/experiments/Spark%20SQL的基本使用.md)以及[Spark的Scala API介绍](https://github.com/shenhao-stu/Big-Data/blob/master/experiments/Spark的Scala%20API介绍.md)（✅**Gitee地址**：[Spark SQL的基本使用](https://gitee.com/shenhao-stu/Big-Data/blob/master/experiments/Spark%20SQL的基本使用.md)以及[Spark的Scala API介绍](https://gitee.com/shenhao-stu/Big-Data/blob/master/experiments/Spark的Scala%20API介绍.md)）。