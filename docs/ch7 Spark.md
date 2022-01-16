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



### 7.2.6 RDD 宽窄依赖

待补充

### 7.2.7 RDD 的操作函数

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

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.1_1.png" style="zoom: 100%;" /></center>

从图上看，整个应用被切分成 3 个阶段，阶段 3 需要依赖阶段 1 和阶段 2，阶段 1 和阶段2 互不依赖。Spark 在执行调度的时候，先执行阶段 1 和阶段 2，完成以后，再执行阶段3。如果有更多的阶段，Spark 的策略也是一样的。**Spark 大数据应用的计算过程**为：Spark会根据程序初始化 DAG，由DAG再建立依赖关系，然后根据依赖关系顺序执行各个计算阶段。

**Spark 作业调度执行核心是 DAG**，由DAG可以得出 **整个应用就被切分成哪些阶段** 以及 **每个阶段的依赖关系**。之后再根据每个阶段要处理的数据量生成相应的任务集合（TaskSet），每个任务都分配一个任务进程去处理。

那DAG是怎么来生成的呢？在Spark中，DAGScheduler组件负责应用 DAG 的生成和管理，DAGScheduler 根据程序代码生成 DAG，然后将程序分发到分布式计算集群，按计算阶段的先后关系调度执行。

### 7.3.2 如何划分计算阶段

上图例子有4个转换函数，但是只有3个阶。看起来并不是RDD上的每个转换函数都会生成一个计算阶段。那RDD的计算阶段是怎样来进行划分的呢？

当 **RDD 之间的转换连接线呈现多对多交叉连接**的时候，就会产生新的阶段。

一个 RDD 代表一个数据集，图中每个 RDD 里面都包含多个小块，每个小块代表 RDD 的一个分片。

**一个数据集中的多个数据分片需要进行分区传输，写入到另一个数据集的不同分片中**。MapReduce的运行过程也有这种数据分区交叉传输的操作。

这种从数据集跨越，由多个分区传输的过程，就是**shuffle过程**，Spark需要通过shuffle将数据进行重新组合，把相同key的数据放一起，进行聚合、关联等操作，对于每次shuffle都会产生新的计算阶段。shuffle是spark最重要的一个环节，只有通过shuffle，相关数据才能互相计算，从而构建起复杂的应用逻辑。

不需要进行shuffle的依赖，叫做窄依赖。需要shuffle的依赖，叫做宽依赖。

现在再来看RDD计算阶段划分的问题，可以得出：计算阶段划分的依据是Shuffle，而不是转换函数的类型，有的函数有时有shuffle，有时没有。

**问题一**：为什么计算阶段会有依赖关系？

- 因为其需要的数据来源于前面一个或多个计算阶段产生的数据，必须等待前面的阶段执行完毕才能进行shuffle，并得到数据。

**问题二**：上图中RDD B 和 RDD F进行Join，得到了RDD G。B和F哪个RDD需要进行Shuffle？

- RDD B在前一个阶段，阶段1的shuffle过程中，已经进行了数据分区，分区数目和分区key不变，就不需要进行shuffle。

**问题三**：Spark进行了shuffle，为什么还可以更高效?

拿Spark和mr进行比较：

- 本质上：Spark可以算是一种MapReduce计算模型的不同实现，Hadoop MR根据Shuffle将大数据计算分为Map和Reduce两个阶段。而Spark 更流畅，将前一个的Reduce和后一个的Map做了连接，当作一个阶段持续来进行计算，从而形成了一个更高效流畅的计算模型。其本质仍然是Map和Reduce。但是这种多个计算阶段依赖执行的方案可以有效减少对HDFS的访问（落盘），减少作业的调度执行次数，因此执行速度也更快。

- 存储方式：MR主要使用磁盘存储shuffle过程的数据，而Spark优先使用内存进行数据存储（RDD也优先存于内存）。这也是Spark性能比Hadoop高的另一个原因。

### 7.3.3 Spark的作业管理

本小节主要来说明 作业、计算阶段、任务的依赖和时间先后关系。

Spark的RDD有两种函数：转换函数和action函数。action函数调用之后不再返回RDD。Spark的DAGScheduler 遇到shuffle时，会生成一个计算阶段，在遇到action函数时，会生成一个作业（job）。RDD里的每个数据分片，Spark都会创建一个计算任务去处理，故一个计算阶段会包含多个计算任务（task）。

一个作业至少包含一个计算阶段，每个计算阶段由多个任务组成，这些任务task组成一个任务集合。

DAGScheduler根据代码生成DAG图，Spark的任务调度以任务为单位进行分配，将任务分配到分布式集群的不同机器上进行执行。

### 7.3.4 Spark 的执行过程

Spark支持多种部署方案（Standalone、Yarn、Mesos等），不同的部署方案核心功能和运行流程基本一样，只是不同组件角色命名不同。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.4_1.png" style="zoom: 100%;" /></center>

**首先**，Spark 在自己的 JVM 进程里启动应用程序，即 Driver 进程。启动后driver调用SparkContext 初始化执行配置和输入数据。再由SparkContext 启动 DAGScheduler 构造执行的 DAG 图，切分成计算任务这样的最小执行单位。

**接着**Driver 向 Cluster Manager 请求计算资源，用于 DAG 的分布式计算。ClusterManager 收到请求以后，将 Driver 的主机地址等信息通知给集群的所有计算节点Worker。

**最后**，Worker 收到信息以后，根据 Driver 的主机地址，跟 Driver 通信并注册，然后根据自己的空闲资源向 Driver 通报自己可以领用的任务数。Driver 根据 DAG 图开始向注册的Worker 分配任务。     

## 7.4 通过WordCount 看Spark RDD执行

   

## 7.5 Spark编程实战

### 7.5.1 实验一：Spark Local模式的安装

#### 7.5.1.1 实验准备

**实验环境：**Linux Ubuntu 20.04  
**前提条件：**  

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.0.0的单点部署（详见第2章安装单机版Hadoop）

#### 7.5.1.2 实验内容

&emsp;&emsp;基于上述前提条件，完成Spark Local模式的安装。

✅**厦门大学数据库实验室参考教程**：[GettingStarted](http://dblab.xmu.edu.cn/blog/2501-2/)

#### 7.5.1.3 实验步骤

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

### 7.5.2 实验二：Spark SQL的基本使用

#### 7.5.2.1 实验准备

**实验环境：**Linux Ubuntu 20.04  
**前提条件：**  

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.0.0的单点部署（详见第2章安装单机版Hadoop）
3. 完成Spark Local模式的部署（详见本章实验一：Spark Local模式的安装）

#### 7.5.2.2 实验内容

&emsp;&emsp;基于上述前提条件，完成基础的Spark SQL的使用：

- 创建DataFrame和Dataset
- Columns列操作
- 使用Structured API进行基本查询
- 使用Spark SQL进行基本查询

##### 1.启动Scala的Shell

&emsp;&emsp;在命令行终端中输入下面的命令即可启动Scala Shell

```shell
spark-shell
```

&emsp;&emsp;启动后终端显示如下：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex2.1.png)

&emsp;&emsp;如上出现了 Scala> 表明进入了Scala的Shell

##### 2.创建DataFrame和Dataset

###### 2.1 创建DataFrame

&emsp;&emsp;Spark 中所有功能的入口点是 `SparkSession`，可以使用 `SparkSession.builder()` 创建。创建后应用程序就可以从现有 RDD，Hive 表或 Spark 数据源创建 DataFrame。注意从hdfs文件系统导入时，需要先将本地文件emp.json导入到hdfs中再进行操作，同时hadoop服务也需要启动。创建DataFrame的示例如下：

```scala
// 建议在进行 spark SQL 编程前导入下面的隐式转换，因为 DataFrames 和 dataSets 中很多操作都依赖了隐式转换
import spark.implicits._

val spark = SparkSession.builder().appName("Spark-SQL").master("local[2]").getOrCreate()
//从hdfs文件系统导入
val df = spark.read.json("/home/datawhale/json/emp.json")
//从本地文件系统导入
val df = spark.read.json("file:///home/datawhale/emp.json")
df.show()
```

&emsp;&emsp;需要注意的是 `spark-shell` 启动后会自动创建一个名为 `spark` 的 `SparkSession`，在命令行中可以直接引用即可，结果显示如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex2.2.png)

&emsp;&emsp;其中`emp.json`的内容在本仓库的[resources](https://github.com/shenhao-stu/Big-Data/tree/master/resources) 目录下 。

###### 2.2 创建Dataset

&emsp;&emsp;Spark 支持由内部数据集和外部数据集来创建 Dataset，其创建方式分别如下：

1. 由外部数据集创建

```scala
// 1.需要导入隐式转换
import spark.implicits._

// 2.创建 case class,等价于 Java Bean
case class Emp(ename: String, comm: Double, deptno: Long, empno: Long, 
               hiredate: String, job: String, mgr: Long, sal: Double)

// 3.由外部数据集创建 Datasets
val ds = spark.read.json("file:///home/datawhale/emp.json").as[Emp]

//4.展示数据集
ds.show()
```

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex2.3.png)
2. 由内部数据集创建

```scala
// 1.需要导入隐式转换
import spark.implicits._

// 2.创建 case class,等价于 Java Bean
case class Emp(ename: String, comm: Double, deptno: Long, empno: Long, 
               hiredate: String, job: String, mgr: Long, sal: Double)

// 3.由内部数据集创建 Datasets
val caseClassDS = Seq(Emp("ALLEN", 300.0, 30, 7499, "1981-02-20 00:00:00", "SALESMAN", 7698, 1600.0),Emp("JONES", 300.0, 30, 7499, "1981-02-20 00:00:00", "SALESMAN", 7698, 1600.0)).toDS()

//4.展示数据集
caseClassDS.show()
```

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex2.4.png)

###### 2.3 由RDD创建DataFrame

&emsp;&emsp;Spark 支持两种方式把 RDD 转换为 DataFrame，分别是使用反射推断和指定 Schema 转换。其中`dept.txt`的内容在本仓库的[resources](https://github.com/shenhao-stu/Big-Data/tree/master/resources) 目录下 。

1. 使用反射推断

```scala
// 1.导入隐式转换
import spark.implicits._

// 2.创建部门类
case class Dept(deptno: Long, dname: String, loc: String)

// 3.创建 RDD 并转换为 dataSet
val rddToDS = spark.sparkContext
  .textFile("file:///home/datawhale/dept.txt")
  .map(_.split("\t"))
  .map(line => Dept(line(0).trim.toLong, line(1), line(2)))
  .toDS()  // 如果调用 toDF() 则转换为 dataFrame

//4.展示数据集
rddToDS.show()
```

2. 以编程方式指定Schema

```scala
import org.apache.spark.sql.Row
import org.apache.spark.sql.types._


// 1.定义每个列的列类型
val fields = Array(StructField("deptno", LongType, nullable = true),
                   StructField("dname", StringType, nullable = true),
                   StructField("loc", StringType, nullable = true))

// 2.创建 schema
val schema = StructType(fields)

// 3.创建 RDD
val deptRDD = spark.sparkContext.textFile("file:///home/datawhale/dept.txt")
val rowRDD = deptRDD.map(_.split("\t")).map(line => Row(line(0).toLong, line(1), line(2)))


// 4.将 RDD 转换为 dataFrame
val deptDF = spark.createDataFrame(rowRDD, schema)

//5.展示数据集
deptDF.show()
```

###### 2.4 DataFrames与Datasets互相转换

&emsp;&emsp;Spark 提供了非常简单的转换方法用于 DataFrame 与 Dataset 间的互相转换，命令如下：  

```scala
//DataFrames转Datasets
df.as[Emp]

//Datasets转DataFrames
ds.toDF()
```

##### 3.Columns列操作

###### 3.1 引用列

```scala
//Spark 支持多种方法来构造和引用列，最简单的是使用 col() 或 column() 函数。
col("colName")
column("colName")

// 对于 Scala 语言而言，还可以使用$"myColumn"和'myColumn 这两种语法糖进行引用。
df.select($"ename", $"job").show()
df.select('ename, 'job).show()
```

###### 3.2 新增列

```scala
// 基于已有列值新增列
df.withColumn("upSal",$"sal"+1000)
// 基于固定值新增列
df.withColumn("intCol",lit(1000))
```

###### 3.3 删除列

```scala
// 支持删除多个列
df.drop("comm","job").show()
```

###### 3.4 重命名列

```scala
df.withColumnRenamed("comm", "common").show()
```

&emsp;&emsp;需要说明的是新增，删除，重命名列都会产生新的 DataFrame ，原来的 DataFrame 不会被改变。

##### 4.使用Structured API进行基本查询

```scala
// 1.查询员工姓名及工作
df.select($"ename", $"job").show()

// 2.filter 查询工资大于 2000 的员工信息
df.filter($"sal" > 2000).show()

// 3.orderBy 按照部门编号降序，工资升序进行查询
df.orderBy(desc("deptno"), asc("sal")).show()

// 4.limit 查询工资最高的 3 名员工的信息
df.orderBy(desc("sal")).limit(3).show()

// 5.distinct 查询所有部门编号
df.select("deptno").distinct().show()

// 6.groupBy 分组统计部门人数
df.groupBy("deptno").count().show()
```

##### 5.使用Spark SQL进行基本查询

```scala
// 1.首先需要将 DataFrame 注册为临时视图
df.createOrReplaceTempView("emp")

// 2.查询员工姓名及工作
spark.sql("SELECT ename,job FROM emp").show()

// 3.查询工资大于 2000 的员工信息
spark.sql("SELECT * FROM emp where sal > 2000").show()

// 4.orderBy 按照部门编号降序，工资升序进行查询
spark.sql("SELECT * FROM emp ORDER BY deptno DESC,sal ASC").show()

// 5.limit  查询工资最高的 3 名员工的信息
spark.sql("SELECT * FROM emp ORDER BY sal DESC LIMIT 3").show()

// 6.distinct 查询所有部门编号
spark.sql("SELECT DISTINCT(deptno) FROM emp").show()

// 7.分组统计部门人数
spark.sql("SELECT deptno,count(ename) FROM emp group by deptno").show()
```

&emsp;&emsp;至此，Spark SQL的基本命令介绍完成，本次实验结束啦！

### 7.5.3 实验三：Spark的Scala API的使用

#### 7.5.3.1 实验准备

**实验环境：**Linux Ubuntu 20.04  
**前提条件：**  

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.0.0的单点部署（详见第2章安装单机版Hadoop）
3. 完成Spark Local模式的部署（详见本章实验一：Spark Local模式的安装）

#### 7.5.3.2 实验内容

&emsp;&emsp;基于上述前提条件，完成Spark的Scala API的使用。

#### 7.5.3.3 实验步骤

##### 1.启动Scala的Shell

&emsp;&emsp;在命令行终端中输入下面的命令即可启动Scala Shell

```shell
spark-shell
```

&emsp;&emsp;启动后终端显示如下：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex2.1.png)

&emsp;&emsp;如上出现了 Scala> 表明进入了Scala的Shell

##### 2.RDD的创建方法

&emsp;&emsp;1） 由一个已经存在的Scala集合创建。

```scala
val rdd1 = sc.parallelize(Array(1,2,3,4,5,6,7,8))
```

&emsp;&emsp;2） 由外部存储系统的数据集创建，包括本地的文件系统，还有所有Hadoop支持的数据集，比如HDFS、Cassandra、HBase等

```scala
val rdd2 = sc.textFile("file:///opt/spark/README.md")
```

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex3.1.png)

##### 3.Transformation转换

&emsp;&emsp;RDD中的所有转换都是***延迟加载***的，也就是说，它们并不会直接计算结果。相反的，它们只是***记住这些应用到基础数据集***（例如一个文件）上的转换动作。只有当发生一个==**要求返回结果给Driver的动作时，这些转换才会真正运行**==。这种设计让Spark更加有效率地运行。

&emsp;&emsp;**常用的Transformation**

- **map(func)**
  返回一个新的RDD，该RDD由每一个输入元素经过func函数转换后组成

- **filter(func)**
  返回一个新的RDD，该RDD由经过func函数计算后返回值为true的输入元素组成
- **flatMap(func)**
  类似于map，但是每一个输入元素可以被映射为0或**多个输出**元素（所以func应该返回一个序列，而不是单一元素）
- **union(otherDataset)**
  对源RDD和参数RDD求并集后返回一个新的RDD
- **intersection(otherDataset)**
  对源RDD和参数RDD求交集后返回一个新的RDD
- **groupByKey([numTasks])**
  在一个(K,V)的RDD上调用，返回一个(K, Iterator[V])的RDD
- **reduceByKey(func, [numTasks])**
  在一个(K,V)的RDD上调用，返回一个(K,V)的RDD，使用指定的reduce函数，将相同key的值聚合到一起，与groupByKey类似，reduce任务的个数可以通过第二个可选的参数来设
- **sortByKey([ascending], [numTasks])**
  在一个(K,V)的RDD上调用，K必须实现Ordered接口，返回一个按照key进行排序的(K,V)的RDD
- **join(otherDataset, [numTasks])**
  在类型为(K,V)和(K,W)的RDD上调用，返回一个相同key对应的所有元素对在一起的(K,(V,W))的RDD

##### 4.Action动作

&emsp;&emsp;**常用的Action**

- **reduce(func)**
  通过func函数聚集RDD中的所有元素，这个功能必须是可交换且可并联的

- **collect()**
  在驱动程序中，以数组的形式返回数据集的所有元素

- **count()**
  返回RDD的元素个数

- **first()**
  返回RDD的第一个元素（类似于take(1)）
- **take(n)**
  返回一个由数据集的前n个元素组成的数组
- **takeSample(withReplacement,num, [seed])**
  返回一个数组，该数组由从数据集中随机采样的num个元素组成，可以选择是否用随机数替换不足的部分，seed用于指定随机数生成器种子
- **saveAsTextFile(path)**
  将数据集的元素以textfile的形式保存到HDFS文件系统或者其他支持的文件系统，对于每个元素，Spark将会调用toString方法，将它装换为文件中的文本
- **saveAsSequenceFile(path)**
  将数据集中的元素以Hadoop sequencefile的格式保存到指定的目录下，可以使HDFS或者其他Hadoop支持的文件系统。
- **foreach(func)**
  在数据集的每一个元素上，运行函数func进行更新。

##### 5.练习1

&emsp;&emsp;在Scala命令行中运行下面的代码：  

```scala
//通过并行化生成rdd
val rdd1 = sc.parallelize(List(5, 6, 4, 7, 3, 8, 2, 9, 1, 10))

//对rdd1里的每一个元素乘2然后排序
val rdd2 = rdd1.map(_ * 2).sortBy(x => x, true)

//过滤出大于等于十的元素
val rdd3 = rdd2.filter(_ >= 10)

//将元素以数组的方式在客户端显示
rdd3.collect
```

&emsp;&emsp;运行上述代码后，显示如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex3.2.png)

##### 6.练习2

&emsp;&emsp;在Scala命令行中运行下面的代码：  

```scala
//通过并行化生成rdd
val rdd1 = sc.parallelize(Array("a b c", "d e f", "h i j"))

//将rdd1里面的每一个元素先切分在压平
val rdd2 = rdd1.flatMap(_.split(' '))
rdd2.collect
```

&emsp;&emsp;运行上述代码后，显示如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex3.3.png)

##### 7.练习3

&emsp;&emsp;在Scala命令行中运行下面的代码：  

```scala
//通过并行化生成rdd
val rdd1 = sc.parallelize(List(5, 6, 4, 3))
val rdd2 = sc.parallelize(List(1, 2, 3, 4))

//求并集
val rdd3 = rdd1.union(rdd2)

//求交集
val rdd4 = rdd1.intersection(rdd2)

//去重
rdd3.distinct.collect
rdd4.collect
```

&emsp;&emsp;运行上述代码后，显示如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex3.4.png)

##### 8.练习4

&emsp;&emsp;在Scala命令行中运行下面的代码：  

```scala
//通过并行化生成rdd
val rdd1 = sc.parallelize(List(("tom", 1), ("jerry", 3), ("kitty", 2)))
val rdd2 = sc.parallelize(List(("jerry", 2), ("tom", 1), ("shuke", 2)))

//求jion
val rdd3 = rdd1.join(rdd2)
rdd3.collect

//求并集
val rdd4 = rdd1 union rdd2
rdd4.collect

//按key进行分组
val rdd5 = rdd4.groupByKey().map(t => (t._1, t._2.sum))
rdd5.collect
```

&emsp;&emsp;运行上述代码后，显示如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex3.5.png)

##### 9.练习5

&emsp;&emsp;在Scala命令行中运行下面的代码：  

```scala
//通过并行化生成rdd
val rdd1 = sc.parallelize(List(("tom", 1), ("tom", 2), ("jerry", 3), ("kitty", 2)))
val rdd2 = sc.parallelize(List(("jerry", 2), ("tom", 1), ("shuke", 2)))

//cogroup, 注意cogroup与groupByKey的区别
val rdd3 = rdd1.cogroup(rdd2)
rdd3.collect
```

&emsp;&emsp;运行上述代码后，显示如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex3.6.png)

##### 10.练习6

&emsp;&emsp;在Scala命令行中运行下面的代码：  

```scala
//通过并行化生成rdd
val rdd1 = sc.parallelize(List(1, 2, 3, 4, 5))

//reduce聚合
val rdd2 = rdd1.reduce(_ + _)
rdd2
```

&emsp;&emsp;运行上述代码后，显示如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex3.7.png)

##### 11.练习7

&emsp;&emsp;在Scala命令行中运行下面的代码：  

```scala
//通过并行化生成rdd
val rdd1 = sc.parallelize(List(("tom", 1), ("jerry", 3), ("kitty", 2),  ("shuke", 1)))
val rdd2 = sc.parallelize(List(("jerry", 2), ("tom", 3), ("shuke", 2), ("kitty", 5)))
val rdd3 = rdd1.union(rdd2)

//按key进行聚合
val rdd4 = rdd3.reduceByKey(_ + _)
rdd4.collect

//按value的降序排序
val rdd5 = rdd4.map(t => (t._2, t._1)).sortByKey(false).map(t => (t._2, t._1))
rdd5.collect
```

&emsp;&emsp;运行上述代码后，显示如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7_ex3.8.png)

&emsp;&emsp;至此，Spark的Scala API介绍完成，本次实验结束啦！