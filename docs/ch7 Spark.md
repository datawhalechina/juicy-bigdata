# 第七章：Spark

> 王嘉鹏，shenhao

## 7.0 引言
&emsp;&emsp;我们再次拿出5.1章节中辣椒酱的demo（没印象的同学移步[这里](https://shenhao-stu.github.io/Big-Data/#/ch5%20MapReduce)），来简单看下Spark和MapReduce在处理问题的方式上有什么区别。  
&emsp;&emsp;在介绍这个之前，必须要了解什么是内存和磁盘。**内存和磁盘两者都是存储设备**，但内存储存的是我们正在使用的资源，磁盘储存的是我们暂时用不到的资源。可以把磁盘理解为一个仓库，而内存是进出这个仓库的通道。仓库（磁盘）很大，而通道（内存）很小，通道就很容易塞满。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.0_1.png" style="zoom: 50%;" /></center>

&emsp;&emsp;假设把磁盘作为冰箱，内存为做饭时的操作台：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.0_2.png" style="zoom: 100%;" /></center>

&emsp;&emsp;Mapreduce每一个步骤发生在内存中，但产生的中间值（溢写文件）都会写入在磁盘里，下一步操作时又会将这个中间值`merge`到内存中，如此循环直到最终完成计算。  
&emsp;&emsp;而对于Spark，每个步骤也是发生在内存之中，但产生的中间值会直接进入下一个步骤，直到所有的步骤完成之后才会将最终结果保存进磁盘。所以在使用Spark做数据分析时，较少进行很多次相对没有意义的读写，节省大量的时间。当计算步骤很多时，Spark的优势就体现出来了。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.0_3.png" style="zoom: 100%;" /></center>

## 7.1 Spark概述

### 7.1.1 Spark诞生

&emsp;&emsp;在Hadoop出现之前，分布式计算都是**专用系统**，只能用来处理某一类的计算，比如进行大规模的排序。这样的系统无法复用到其他大数据计算场景。  
&emsp;&emsp;而Hadoop MapReduce出现后，使得大数据计算通用编程成为可能，只要遵循MapReduce编程模型编写业务处理代码，就可以运行在Hadoop分布式集群上，而无需关心分布式计算是怎样完成的。  
&emsp;&emsp;紧接着，我们经常看到的说法是：“MapReduce虽然已经可以满足大数据的应用场景，但是其执行速度和编程复杂度并不让人们满意。于是AMP lab的Spark应运而生”。  
&emsp;&emsp;从事后因果规律的分析上，往往容易**把结果当作了原因** ——觉得是因为MapReduce执行的很慢，所以才去发明和使用Spark。但事实上，在Spark出现之前，MapReduce并没有让人怨声载道。一方面，Hive这些工具将常用的MapReduce编程进行了封装，转化为了更易于编写的SQL形式；另一方面，MapReduce已经将分布式编程极大地进行了简化。  
&emsp;&emsp;而当Spark出现后，性能比MapReduce快了100多倍。因为有了Spark，才对MapReduce不满，才觉得MapReduce慢。而不是觉得MapReduce慢，所以诞生了Spark。真实世界中的因果关系并非是顺承的，**我们常常意识不到问题的存在，直到有大神解决了这些问题**。

&emsp;&emsp;附上Spark框架发展历史中**重要的时间点**：
<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.1.png" style="zoom: 80%;" /></center>

### 7.1.2 Spark与Hadoop、MapReduce、HDFS的关系

&emsp;&emsp;那接下来的问题是：Spark自己有自己的体系，那么其和Hadoop之间的关系是什么呢？  
&emsp;&emsp;我们先来回忆一下Hadoop处理大数据的流程：首先从**HDFS**读取输入数据；接着**在 Map 阶段**使用用户定义的`mapper function`；然后把结果写入磁盘；**在Reduce阶段**，从各个处于Map阶段的机器中读取Map计算的中间结果，使用用户定义的`reduce function`，最后**把结果写回HDFS**。  
&emsp;&emsp;在这个过程中， 至少进行了三次数据读写，Hadoop处理大数据的流程高度依赖磁盘读写，那么在数据处理上就出现了瓶颈，面对更复杂的计算逻辑的处理任务时，Hadoop存在很大局限性。  
&emsp;&emsp;Spark在这样的背景下产生，其不像Hadoop一样采取磁盘读写，而是**基于性能更高的内存存储来进行数据存储和读写**（这里说的是计算数据的存储，而非持久化的存储）。但是Spark并非完美，其缺乏对数据存储这一块的支持，即没有分布式文件系统，必须依赖外部的数据源，这个依赖可以是Hadoop系统的HDFS，也可以是其他的分布式文件系统，甚至可以是MySQL或本地文件系统。  
&emsp;&emsp;基于以上分析，我们可以得出**结论**：Hadoop和Spark两者都是大数据框架，但是各自存在的目的不同。Hadoop实质上是一个**分布式数据基础设施**，它将巨大的数据集分派到一个集群中的多个节点**进行存储**，也有**计算处理**的功能。Spark则是一个专门用来**对那些分布式存储的大数据进行处理的工具**，它并不会进行分布式数据的存储，可以部分看做是MapReduce的竞品（**准确的说是SparkCore**）。总结以上对比，下图所示：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.2_1.png" style="zoom: 100%;" /></center>

### 7.1.3 Spark生态体系

&emsp;&emsp;Spark是一个用来实现快速且通用的集群计算平台，主要表现在以下两个方面：  
1. 速度方面：Spark的一个主要特点是能够在内存中进行计算，因此，速度要比MapReduce计算模型更加高效，可以面向海量数据进行分析处理；
2. 通用方面：Spark框架可以针对任何业务类型分析进行处理，比如`SparkCore`离线批处理、`SparkSQL`交互式分析、`SparkStreaming`和`StructuredStreamig`流式处理及机器学习和图计算都可以完成；

&emsp;&emsp;以Spark为基础，有支持SQL语句的`SparkSQL`，有支持流计算的`Spark Streaming`，有支持机器学习的`MLlib`，还有支持图计算的`GraphX`。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.3_1.png" style="zoom: 100%;" /></center>

&emsp;&emsp;利用这些产品，Spark技术栈支撑了大数据分析、大数据机器学习等各种大数据应用场景。

## 7.2 Spark编程模型

### 7.2.1 RDD概述

&emsp;&emsp;RDD是Spark的核心概念，是弹性数据集（Resilient Distributed Datasets）的缩写。RDD既是Spark面向开发者的编程模型，又是Spark自身架构的核心元素。  
&emsp;&emsp;大数据计算就是在大规模的数据集上进行一系列的数据计算处理。类比MapReduce，针对输入数据，将计算过程分为两个阶段，Map阶段和Reduce阶段，可以理解成是**面向过程**的大数据计算。我们在用MapReduce编程的时候，思考的是，如何将计算逻辑用 Map和Reduce两个阶段实现，map和reduce函数的输入和输出是什么。  
&emsp;&emsp;而Spark则直接针对数据进行编程，将大规模数据集合抽象成一个RDD对象，然后在这个RDD上进行各种计算处理，得到一个新的RDD，并继续计算处理，直至得到最后的数据结果。所以，**Spark可以理解成是面向对象的大数据计算**。我们在进行Spark编程的时候，主要思考的是**一个RDD对象需要经过什么样的操作，转换成另一个RDD对象，思考的重心和落脚点都在RDD上**。

### 7.2.2 RDD定义

&emsp;&emsp;**RDD**是**分布式内存**的一个抽象概念，是只读的记录分区集合，能横跨集群所有节点进行并行计算。Spark建立在抽象的RDD上，可用统一的方式处理不同的大数据应用场景，把所有需要处理的数据转化为RDD，然后对RDD进行一系列的算子运算，通过丰富的API来操作数据，从而得到结果，

### 7.2.3 RDD五大特性

&emsp;&emsp;RDD共有五大特性，我们将对每一种特性进行介绍：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.2.4_1.jpg" style="zoom: 100%;" /></center>

**一、分区**

&emsp;&emsp;分区的含义是允许Spark将计算**以分区为单位**，分配到多个机器上并行计算。在某些情况下，比如从HDFS读取数据时，Spark会使用位置信息，将计算工作发给靠近数据的机器，减少跨网络传输的数据量。

**二、可并行计算**

&emsp;&emsp;RDD的每一个分区都会被一个计算任务（Task）处理，每个分区有计算函数（具体执行的计算算子），计算函数以分片为基本单位进行并行计算，**RDD的分区数决定着并行计算的数量**。

**三、依赖关系**

&emsp;&emsp;**依赖关系列表**会告诉Spark如何从必要的输入来构建RDD。当遇到错误需要重算时，Spark可以根据这些依赖关系重新执行操作，以此来重建RDD。依赖关系赋予了RDD**的容错机制**。

**四、Key-Value数据的RDD分区器**

&emsp;&emsp;想要理解分区器的概念，我们需要先来比较一下MapReduce的任务机制。MapReduce任务的Map阶段，处理结果会进行分片（也可以叫分区，这个分区不同于上面的分区），分片的数量就是Reduce Task的数量。而**具体分片的策略由分区器Partitioner**决定，Spark目前支持`Hash`分区（默认分区）和`Range`分区，用户也可以自定义分区。  
&emsp;&emsp;总结一下，Partitioner决定了RDD如何分区。通过Partitioner来决定下一步会产生并行的分片数，以及当前并行Shuffle输出的并行数据，使得Spark可以控制数据在不同节点上分区。  
&emsp;&emsp;值得注意的是，其本身**只针对于key-value的形式**（key-value形式的RDD才有Partitioner属性），Partitioner会从0到`numPartitions-1`区间内映射每一个`key`到`partition ID`上。

**五、每个分区都有一个优先位置列表**

&emsp;&emsp;大数据计算的基本思想是："移动计算而非移动数据"。Spark本身在进行任务调度时，需要尽可能的将任务分配到处理数据的数据块所在的具体位置。因此在具体计算前，就需要知道它运算的数据在什么地方。所以，分区位置列表会存储每个Partition的优先位置，如果读取的是HDFS文件，这个列表保存的就是每个分区所在的block块的位置。

### 7.2.4 RDD操作函数

&emsp;&emsp;RDD的操作函数包括两种：转换（transformation）函数和执行（action）函数。一种是转换（transformation）函数，这种函数的返回值还是RDD；另一种是执行（action）函数，这种函数不返回RDD。  
&emsp;&emsp;RDD中定义的转换操作函数有：用于计算的`map(func)`函数、用于过滤的`filter(func)`函数、用于合并数据集的`union(otherDataset)`函数、用于根据`key`聚合的`reduceByKey(func, [numPartitions])`函数、用于连接数据集的`join(otherDataset, [numPartitions])`函数、用于分组的`groupByKey([numPartitions])`函数等。

&emsp;&emsp;跟MapReduce一样，Spark也是**对大数据进行分片计算**，Spark分布式计算的数据分片、任务调度都是**以RDD为单位展开的**，每个RDD分片都会分配到一个执行进程中进行处理。RDD上的**转换操作分成两种**：  
1. 转换操作产生的RDD**不会出现新的分片**，比如`map`、`filter`等操作。一个RDD数据分片，经过`map`或者`filter`转换操作后，其结果还在当前的分片中。就像用`map`函数对每个数据加1，得到的还是这样一组数据，只是值不同。实际上，Spark并不是按照代码写的操作顺序生成RDD，比如`rdd2 = rdd1.map(func)`这样的代码并不会在物理上生成一个新的RDD。**物理上，Spark只有在产生新的RDD分片时候，才会真的生成一个RDD**，Spark的这种特性也被称作**惰性计算**；
2. 转换操作产生的RDD**会产生新的分片**，比如`reduceByKey`，来自不同分片的相同`key` 必须聚合在一起进行操作，这样就会产生新的RDD分片。实际执行过程中，**是否会产生新的RDD分片，并不是根据转换函数名就能判断出来的。**

## 7.3 Spark架构原理

&emsp;&emsp;Spark和MapReduce一样，也遵循着 **移动计算而非移动数据**这一大数据计算基本原则。MapReduce通过固定的Map与Reduce分阶段计算，而Spark的计算框架通过`DAG`来实现计算。

### 7.3.1 Spark计算阶段

&emsp;&emsp;MapReduce中，一个应用一次只运行一个`map`和一个`reduce`，而Spark可以根据应用的复杂程度，将过程分割成更多的计算阶段（stage），这些计算阶段组成一个有向无环图（DAG），Spark任务调度器根据**DAG的依赖关系**执行计算阶段（stage）。  
&emsp;&emsp;Spark比MapReduce快100 多倍。因为某些机器学习算法可能需要进行大量的迭代计算，产生数万个计算阶段，这些计算阶段在一个应用中处理完成，而不是像MapReduce那样需要启动数万个应用，因此极大地提高了运行效率。  
&emsp;&emsp;DAG是有向无环图，即是说**不同阶段的依赖关系是有向**的，计算过程只能沿着依赖关系方向执行，被依赖的阶段执行完成之前，依赖的阶段不能开始执行，同时，这个依赖关系不能是环形依赖，否则就造成死循环。下面这张图描述了一个典型的Spark运行DAG的不同阶段：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.1_1.png" style="zoom: 50%;" /></center>

&emsp;&emsp;从图上看，整个应用被切分成3个阶段，阶段3需要依赖阶段1和阶段2，阶段1和阶段2互不依赖。Spark在执行调度时，先执行阶段1和阶段2，完成以后再执行阶段3。如果有更多的阶段，Spark的策略是一样的。**Spark大数据应用的计算过程**为：Spark会根据程序初始化DAG，由DAG再建立依赖关系，根据依赖关系顺序执行各个计算阶段。  
&emsp;&emsp;**Spark 作业调度执行核心是DAG**，由DAG可以得出 **整个应用就被切分成哪些阶段**以及**每个阶段的依赖关系**。再根据每个阶段要处理的数据量生成相应的任务集合（TaskSet），每个任务都分配一个任务进程去处理。  
&emsp;&emsp;那DAG是怎么来生成的呢？在Spark中，`DAGScheduler`组件负责应用DAG的生成和管理，`DAGScheduler`会根据程序代码生成DAG，然后将程序分发到分布式计算集群，按计算阶段的先后关系调度执行。

### 7.3.2 如何划分计算阶段

&emsp;&emsp;上图的DAG对应Spark伪代码可以表示为：

```python
rddB = rddA.groupBy(key)
rddD = rddC.map(func)
rddF = rddD.union(rddE)
rddG = rddB.join(rddF)
```

&emsp;&emsp;可以看到，共有4个转换函数，但是只有3个阶段。看起来并不是RDD上的每个转换函数都会生成一个计算阶段。那**RDD的计算阶段是怎样来进行划分**的呢？

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.2_1.png" style="zoom: 50%;" /></center>

&emsp;&emsp;再看下上图，我们发现了一个规律，当 **RDD之间的转换连接线呈现多对多交叉连接**的时候，就会产生新的阶段。图中每个RDD里面都包含多个小块，每个小块都表示RDD的一个分片。  
&emsp;&emsp;**一个RDD表示一个数据集，一个数据集中的多个数据分片需要进行分区传输，写入到另一个数据集的不同分片中**。这种涉及到数据分区交叉传输的操作，是否在MapReduce中也有印象？我们来回忆下MapReduce的过程：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.2_2.png" style="zoom: 100%;" /></center>

&emsp;&emsp;MapReduce把这种从数据集跨越，由多个分区传输的过程，叫做**Shuffle**。同样，Spark也需要通过`Shuffle`将数据进行重新组合，把相同`key`的数据放一起。由于会进行新的聚合、关联等操作，所以Spark每次`Shuffle`都会产生新的计算阶段。而每次计算时，需要的数据都是由前面一个或多个计算阶段产生的，所以计算阶段需要依赖关系，必须等待前面的阶段执行完毕后，才能进行`Shuffle`。  
&emsp;&emsp;**Spark中计算阶段划分的依据是Shuffle**，而不是操作函数的类型，并不是所有的函数都有`Shuffle`过程。比如Spark计算阶段示例图中，RDD B和RDD F进行join后，得到RDD G。**RDD B不需要Shuffle**，因为RDD B在上一个阶段中，已经进行了数据分区，分区数和分区key不变，就不需要进行`Shuffle`。而RDD F的分区数不同，就需要进行`Shuffle`。Spark把**不需要Shuffle**的依赖，称为**窄依赖**。**需要Shuffle**的依赖，称为**宽依赖**。`Shuffle`是Spark最重要的一个环节，只有通过`Shuffle`，相关数据才能互相计算，从而构建起复杂的应用逻辑。  

&emsp;&emsp;那么Spark和MapReduce一样，都进行了`Shuffle`，为什么Spark会比MapReduce更高效呢？  我们从**本质和存储方式**两个方面，对Spark和MapReduce进行比较：

- **从本质上**：Spark可以算是一种MapReduce计算模型的不同实现，Hadoop MapReduce根据`Shuffle`将大数据计算分为Map和Reduce两个阶段。而Spark更流畅，将前一个的Reduce和后一个的Map进行连接，当作一个阶段进行计算，从而形成了一个更高效流畅的计算模型。其本质仍然是Map和Reduce。但是这种多个计算阶段依赖执行的方案可以有效减少对HDFS的访问（落盘），减少作业的调度执行次数，因此执行速度也更快。

- **从存储方式上**：MapReduce主要使用磁盘存储`Shuffle`过程的数据，而Spark优先使用内存进行数据存储（RDD也优先存于内存）。这也是Spark比Hadoop性能高的另一个原因。

### 7.3.3 Spark 作业管理

&emsp;&emsp;本小节主要说明 作业、计算阶段、任务的依赖和时间先后关系。  
&emsp;&emsp;Spark的RDD有两种函数：转换函数和`action`函数。`action`函数调用之后不再返回RDD。Spark的`DAGScheduler`遇到`Shuffle`时，会生成一个计算阶段，在遇到`action`函数时，会生成一个作业（Job）。RDD里的每个数据分片，Spark都会创建一个计算任务进行处理，所以，一个计算阶段会包含多个计算任务（Task）。  
&emsp;&emsp;一个作业至少包含一个计算阶段，每个计算阶段由多个任务组成，这些任务（Task）组成一个任务集合。  
&emsp;&emsp;`DAGScheduler`根据代码生成DAG图，Spark的任务调度以任务为单位进行分配，将任务分配到分布式集群的不同机器上进行执行。

### 7.3.4 Spark 执行过程

&emsp;&emsp;Spark支持多种部署方案（Standalone、Yarn、Mesos等），不同的部署方案核心功能和运行流程基本一样，只是不同组件角色命名不同。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.4_1.png" style="zoom: 100%;" /></center>

&emsp;&emsp;**首先**，Spark在自己的`JVM`进程里启动应用程序，即`Driver`进程。启动后，`Driver`调用`SparkContext`初始化执行配置和输入数据。再由`SparkContext`启动`DAGScheduler`构造执行的DAG图，切分成计算任务这样的最小执行单位。  
&emsp;&emsp;**接着**，`Driver`向`Cluster Manager`请求计算资源，用于`DAG`的分布式计算。`ClusterManager`收到请求以后，将`Driver`的主机地址等信息通知给集群的所有计算节点`Worker`。  
&emsp;&emsp;**最后**，`Worker`收到信息后，根据`Driver`的主机地址，向`Driver`通信并注册，然后根据自己的空闲资源向`Driver`通报可以领用的任务数。`Driver`根据DAG图向注册的`Worker`分配任务。     

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

&emsp;&emsp;进入`/opt/spark/conf`目录下，将`spark-env.sh.template`文件拷贝一份并命名为`spark-env.sh`，命令如下：  
```shell
cd /opt/spark/conf
cp ./spark-env.sh.template ./spark-env.sh
```

&emsp;&emsp;编辑`spark-env.sh`文件，命令如下：  
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

&emsp;&emsp;使用`Shift+:`，输入`wq`后回车，保存退出。运行如下命令使环境变量生效：
```shell
source /etc/profile
```

##### 5.检验Spark是否成功部署

&emsp;&emsp;通过运行Spark自带的示例，验证Spark是否安装成功，命令如下：  
```shell
cd /opt/spark
bin/run-example SparkPi
```

&emsp;&emsp;执行时会输出非常多的运行信息，输出结果不容易找到，可以通过`grep`命令进行过滤（命令中的`2>&1`可以将所有的信息都输出到`stdout`中，否则由于输出日志的性质，还是会输出到屏幕中），命令如下：  
```shell
cd /opt/spark
bin/run-example SparkPi 2>&1 | grep "Pi is"
```
&emsp;&emsp;过滤后的运行结果如下，可以得到$\pi$的5位小数近似值：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex1.2.png)

&emsp;&emsp;至此，`Spark`安装部署完成，本次实验结束啦！

### 7.4.2 实验二：通过WordCount观察Spark RDD执行流程

#### 7.4.2.1 实验准备

**实验环境：**Linux Ubuntu 20.04  
**前提条件：**  

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.0.0的单点部署（详见第2章安装单机版Hadoop）
3. 完成Spark Local模式的部署（详见本章Spark Local模式的安装）

#### 7.4.2.2 实验内容

&emsp;&emsp;基于上述前提条件，通过WordCount观察Spark RDD执行，进一步理解Spark RDD的执行逻辑。

#### 7.4.2.3 实验步骤

&emsp;&emsp;WordCount在MapReduce章节（第5章5.3节）已经提过。这里再次学习WordCount的案例（编写单词记数代码），从数据流动的角度来详细了解Spark RDD是如何进行数据处理的。

##### 1.文本数据准备

&emsp;&emsp;建立一个文本文件`hello_spark.txt`，将该文件放到文件目录` data/wordcount/`中，文本内容如下：  
```
Hello Spark Hello Scala
Hello Hadoop
Hello Flink
Spark is amazing
```

**待补图（cat文件即可）**

##### 2.配置Spark为本地模式运行

&emsp;&emsp;创建Spark的配置对象`SparkConf`，设置Spark程序运行时的配置信息，如：通过`setMaster`设置程序需要连接的Spark集群中的master的链接，如果设置为`local`，则代表Spark程序将采用本地模式运行，这里，配置为本地模式，具体代码如下：  
```scala
val conf = new SparkConf() // 创建SparkConf对象
conf.setAppName("First Spark App") //设置app应用名称，在程序运行的监控解面可以看到名称
conf.setMaster("local") //本地模式运行
```

##### 3.创建SparkContext对象

&emsp;&emsp;SparkContext是Spark程序所有功能的唯一入口。不管是使用`scala`，还是`python`语言编程，都必须有一个SparkContext，具体代码如下：  
```scala
val sc = new SparkContext(conf) // 创建SparkContext对象，通过传入SparkConf实例来定制Spark运行的具体参数和配置信息
```

&emsp;&emsp;**SparkContext的核心作用**：初始化Spark应用程序，运行所需要的核心组件，包括`DAGScheduler`、`TaskScheduler`、`SchedulerBackend`，同时还会负责Spark向Master注册等，SparkContext是整个Spark应用程序中至关重要的一个对象。

##### 4.创建RDD

&emsp;&emsp;根据具体的数据来源，如HDFS，通过SparkContext来创建RDD。创建的方式有三种：根据外部数据源、根据Scala集合、由其他的RDD操作转换。数据会被RDD划分为一系列的Partitions，分配到每个Partition的数据属于一个Task的处理范畴，具体代码如下：  
```scala
val lines = sc.textFile("dataq/helloSpark.txt", 1) // 读取本地文件并设置为一个Partition
```

##### 5.对数据进行转换处理

&emsp;&emsp;对初始的RDD进行`transformation`级别的处理，如通过`map`、`filter`等高阶函数编程，进行具体的数据计算。  

1. 将每一行的字符串拆分为单个单词
```scala
val words = lines.flatMap{line => line.split(" ")} // 把每行字符串进行单词拆分，把拆分结果通过flat合并为一个大的单词集合
```

2. 在单词拆分的基础上对每个单词实例计数为1，也就是word ->（word, 1）
```scala
val pairs = words.map{word => (word, 1)}
```

3. 在每个单词实例计数为1基础之上统计每个单词在文件中出现的总次数
```scala
val wordCountOdered = pairs.reduceByKey(_+_).map(pair=>(pair._2, pair._1)).sortByKey(false).map(pair => (pair._2, pair._1))
```

##### 6.打印数据

&emsp;&emsp;打印每个单词在文件中出现的次数，具体代码如下：  
```scala
wordCountsOrdered.collect.foreach(wordNumberPair => println(wordNumberPair._1 + "：" + wordNumberPair._2))
```

&emsp;&emsp;执行结果如下：

**（图待补）**

#### 7.4.2.4 WordCount在RDD的运行原理

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.4.3_1.jpg" style="zoom: 100%;" /></center>

## 7.5 本章小结

&emsp;&emsp;在本章的学习中，主要介绍`Spark`的编程模型：`RDD`的定义、特性和操作函数，接着从`Spark`的架构原理出发，简述了`Spark`的计算阶段、作业管理和执行过程。最后通过实验，介绍了`Spark`的安装、并通过`WordCount`实例观察`RDD`的数据流向。如果想要更多的了解Spark SQL和Scala API的内容，可以参考本仓库[experiments](https://github.com/shenhao-stu/Big-Data/tree/master/experiments)目录下的笔记[Spark SQL的基本使用](https://github.com/shenhao-stu/Big-Data/blob/master/experiments/Spark%20SQL的基本使用.md)以及[Spark的Scala API介绍](https://github.com/shenhao-stu/Big-Data/blob/master/experiments/Spark的Scala%20API介绍.md)（✅**Gitee地址**：[Spark SQL的基本使用](https://gitee.com/shenhao-stu/Big-Data/blob/master/experiments/Spark%20SQL的基本使用.md)以及[Spark的Scala API介绍](https://gitee.com/shenhao-stu/Big-Data/blob/master/experiments/Spark的Scala%20API介绍.md)）。