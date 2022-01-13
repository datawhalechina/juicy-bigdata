# 第七章：Spark

> 王嘉鹏

## 7.0 引言
我们再次拿出5.1章节中辣椒酱的demo（没印象的同学移步[这里]()），来简单看下Spark和MapReduce在处理问题的方式上有什么区别。

在了解这个之前，必须要了解什么是内存和磁盘。**内存和磁盘两者都是存储设备**，但内存储存的是我们正在使用的资源，磁盘储存的是我们暂时用不到的资源。
可以把磁盘理解为一个仓库，而内存是进出这个仓库的通道。仓库（磁盘）很大，而通道（内存）很小，通道就很容易塞满。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.0_1.png" style="zoom: 80%;" /></center>

假设把磁盘作为冰箱，内存为做饭时的操作台：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.0_2.png" style="zoom: 100%;" /></center>

Mapreduce每一个步骤发生在内存中但产生的中间值（溢写文件）都会写入在磁盘里，下一步操作时又会将这个中间值merge到内存中，如此循环，直到最终完成计算。

而对于Spark， Spark的每个步骤也是发生在内存之中，但产生的中间值会直接进入下一个步骤，直到所有的步骤完成之后才会将最终结果保存进磁盘。所以在使用Spark做数据分析能少进行很多次相对没有意义的读写，节省大量的时间。当步骤很多时，Spark的优势就体现出来了。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.0_3.png" style="zoom: 100%;" /></center>

## 7.1 Spark概述

### 7.1.1 Spark诞生
在Hadoop出现之前，分布式计算都是**专用系统**，只能用来处理某一类的计算，比如进行大规模的排序。这样的系统无法复用到其他大数据计算场景。

而Hadoop MapReduce出现后，使得大数据计算通用编程成为可能，只要遵循MapReduce编程模型编写业务处理代码，就可以运行在Hadoop分布式集群上，而无需关心分布式计算怎样完成。

紧接着，我们经常看到的说法是：**`MapReduce 虽然已经可以满足大数据的应用场景，但是其执行速度和编程复杂度并不让人们满意。于是AMP lab的Spark应运而生`。**

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

### 7.1.3 Spark生态体系
spark是一个用来实现快速而通用的集群计算的平台。

1. 速度方面：spark的一个主要特点就是能在内存中进行计算，因此速度要比mapreduce计算模型要更加高效，可以面向海量数据进行分析处理；
2. 通用方面：Spark 框架可以针对任何业务类型分析进行处理，比如SparkCore离线批处理、SparkSQL交互式分析、SparkStreaming和StructuredStreamig流式处理及机器学习和图计算都可以完成；

以 Spark 为基础，有支持 SQL 语句的 Spark SQL，有支持流计算的 Spark Streaming，有支持机器学习的 MLlib，还有支持图计算的GraphX。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.3_1.png" style="zoom: 100%;" /></center>

利用这些产品，Spark 技术栈支撑起大数据分析、大数据机器学习等各种大数据应用场景。


## 7.2 Spark编程模型
### 7.2.1 RDD概述

RDD 是 Spark 的核心概念，是弹性数据集（Resilient Distributed Datasets）的缩写。RDD 既是 Spark 面向开发者的编程模型，又是 Spark 自身架构的核心元素。

大数据计算就是在大规模的数据集上进行一系列的数据计算处理。类比MapReduce，针对输入数据，R将计算过程分为两个阶段，一个 Map 阶段，一个 Reduce 阶段，可以理解成是**面向过程**的大数据计算。我们在用MapReduce 编程的时候，思考的是，如何将计算逻辑用 Map 和 Reduce 两个阶段实现，map 和 reduce 函数的输入和输出是什么。

而 Spark 则直接针对数据进行编程，将大规模数据集合抽象成一个 RDD 对象，然后在这个 RDD 上进行各种计算处理，得到一个新的 RDD，继续计算处理，直到得到最后的结果数据。所以 **Spark 可以理解成是面向对象的大数据计算**。我们在进行 Spark 编程的时候，思考的是**一个 RDD 对象需要经过什么样的操作，转换成另一个 RDD 对象，思考的重心和落脚点都在 RDD 上**。

### 7.2.2 RDD定义

**RDD**是**分布式内存**的一个抽象概念，是只读的记录分区的集合，能横跨集群所有节点进行并行计算。

spark建立在抽象的RDD上，使得它可用一致的方式处理大数据不同的应用场景，把所有需要处理的数据转化为RDD，然后对RDD进行一系列的算子运算，从而得到结果，且提供了丰富的API来操作数据。

### 7.2.3 RDD底层存储原理

每个RDD的数据都以**Block**形式分布存储在多台机器上，RDD将分布在不同机器上的Block数据块聚集在一起。

每个Block块由BlockManagerSlave来管理，但是Block的元数据由Driver节点的BlockManagerMaster来保存。BlockManagerSlave生成Block后向BlockManagerMaster**注册**该block，当rdd不再需要存储时，BlockManagerMaster将向BlockManagerSlave发送指令删除相应的Block。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.2.3_1.jpg" style="zoom: 100%;" /></center>

RDD本质上是**数据的一个元数据结构**，存储了数据分区及逻辑结构的映射。RDD的物理分区由BlockManager管理，通过Block存储在内存或磁盘上。而逻辑分区由Partition对应相应的物理块Block。

### 7.2.4 RDD 五大特性

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



### 7.2.5 RDD弹性解释

RDD是弹性数据集，那怎么来理解RDD的弹性？

RDD的弹性主要在如下六个方面体现：

**一、内存和磁盘数据自动交换**

spark优先把数据放内存，内存放不下得话，再放到磁盘。如果实际数据大于内存，要考虑数据放置策略。当应用程序内存不足时，spark应用程序将数据自动从内存存储切换到磁盘存储。**计算是在内存or磁盘进行？**

**二、基于血缘关系的高效容错机制**

为什么说基于血缘关系的容错比较高效？

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.2.5_1.jpg" style="zoom: 100%;" /></center>

首先我们想看下常规的容错方式是怎样的--常规容错的方式是通过 **数据检查点** 或者 **记录数据的更新**。

1. 数据检查点

   可以参考Hadoop 中 的 **SecondaryNameNode** 的机制，这个结点周期性的从 NameNode 结点上下载磁盘镜像和日志文件，在本地将日志合并到镜像中，产生新的镜像，上传到 NameNode，当 NameNode 结点重启时就会加载此最新的镜像文件。数据检查点每次的复制通过网络传输，对存储资源的消耗比较大。

2. 记录数据的更新

   就是每次数据变化了就记录一下，比如**MySQL中的LOG机制**。这种方式不需要重新复制一份数据。但是会比较复杂，消耗性能。

而RDD的容错，是由**血缘关系**实现的。血缘关系**基于RDD的依赖关系**完成（7.2.4小节介绍）。血缘关系记录粗粒度的的操作，（[粗细粒度介绍](https://spark.apache.org/docs/3.2.0/running-on-mesos.html#coarse-grained)）每个操作只关联父操作，各个分片的数据自己不受影响。当出现错误时，只要恢复单个split的特定部分即可。

**三、 Task 失败会自动进行特定次数的重试**

我们先考虑最底层的失败，即某一个 Task 执行失败了。我们先来简单看下task的执行过程，接下来的过程主要涉及五个概念：SparkContext、SchedulerBackend、DagScheduler、TaskScheduler和TaskSchedulerImpl，具体会在[7.3节]()进行介绍。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.2.5_2.png" style="zoom: 100%;" /></center>

①  [SparkContext](https://books.japila.pl/apache-spark-internals/scheduler/TaskSchedulerImpl/)是 Spark的主要入口点，用户与Spark交互，一般要首先创建SparkContext实例。当Spark应用启动时，就会创建具有**SchedulerBackend**和**Dagscheduler**。

② **DAGScheduler** 是高层调度，会计算每个job的stage的DAG，然后提交Stage，用tasksets的方式启动底层**TaskScheduler**调度在集群中运行；

③ **TaskSchedulerImpl**是底层的任务调度接口**TaskScheduler**的实现，这些Schedulers从每一个Stage中的**DAGScheduler**中获取taskset 来运行。如果有故障，会进行重试，**默认重试次数为4次**。



**四、 Stage 失败会自动进行特定次数的重试**

Stage是Spark job运行时具有相同逻辑功能和并行计算任务的一个基本单元。其执行失败后也会进行重试，默认是4次。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.2.5_3.png" style="zoom: 100%;" /></center>

**五、 数据调度弹性**

**Spark 将执行模型抽象有向无环图计划（ DAG ）**，这可以将多 Stage 的任务串联或并行执行，从而不需要将 Stage 中间结果输出到 HDFS 中，当发生节点运行故障时，可有其他可用节点代替该故障节点运行。

**六、数据分片的弹性**

Spark进行数据分片，默认将数据存到内存，内存放不下，则一部分会放到磁盘。在计算过程，会产生很多数据碎片，产生一个Partition可能很小，当一个Partition非常小时，又需要消耗一个线程处理，会降低处理效率。

因此需要考虑把小的Partition合并为一个大的处理，提高效率。每个Partition的数据Block比较大，考虑把Partition变成更小的数据分片，让Spark处理更多的批次，但是不会出现OOM。



### 7.2.4 RDD依赖关系



## 7.3 Spark DAG 逻辑视图





## 7.4 通过WordCount 看Spark RDD执行



## 7.5 实验
