# 第七章：Spark

> 王嘉鹏

概述；数据模型；实现原理；运行机制；编程实战

## 7.0 引言
我们再次拿出5.1章节中辣椒酱的demo（没印象的同学移步[这里]()），来简单看下Spark和MapReduce在处理问题的方式上有什么区别。

在了解这个之前，必须要了解什么是内存和磁盘。**内存和磁盘两者都是存储设备**，但内存储存的是我们正在使用的资源，磁盘储存的是我们暂时用不到的资源。
可以把磁盘理解为一个仓库，而内存是进出这个仓库的通道。仓库（磁盘）很大，而通道（内存）很小，通道就很容易塞满。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.0_1.png" style="zoom: 67%;" /></center>

假设把磁盘作为冰箱，内存为做饭时的操作台：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.0_2.png" style="zoom: 67%;" /></center>

Mapreduce每一个步骤发生在内存中但产生的中间值（溢写文件）都会写入在磁盘里，下一步操作时又会将这个中间值merge到内存中，如此循环，直到最终完成计算。

而对于Spark， Spark的每个步骤也是发生在内存之中，但产生的中间值会直接进入下一个步骤，直到所有的步骤完成之后才会将最终结果保存进磁盘。所以在使用Spark做数据分析能少进行很多次相对没有意义的读写，节省大量的时间。当步骤很多时，Spark的优势就体现出来了。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.0_3.png" style="zoom: 67%;" /></center>

## 7.1 Spark概述

### 7.1.1 Spark诞生
在Hadoop出现之前，分布式计算都是**专用系统**，只能用来处理某一类的计算，比如进行大规模的排序。这样的系统无法复用到其他大数据计算场景。

而Hadoop MapReduce出现后，使得大数据计算通用编程成为可能，只要遵循MapReduce编程模型编写业务处理代码，就可以运行在Hadoop分布式集群上，而无需关心分布式计算怎样完成。

紧接着，我们经常看到的说法是：**`MapReduce 虽然已经可以满足大数据的应用场景，但是其执行速度和编程复杂度并不让人们满意。于是AMP lab的Spark应运而生`。**

我们事后因果规律的分析上，往往容易**把结果当作了原因**  ---觉得是因为MapReduce执行的很慢，所以才去发明和使用Spark。

但事实上，在Spark出现之前，MapReduce并没有让人怨声载道，一方面Hive这些工具将常用的MapReduce编程进行了封装，转化为了更易于编写的SQL形式；一方面MR已经将分布式编程极大的进行了简化。

而当Spark出现后，性能比MapReduce快了100多倍。因为有了Spark，才对MapReduce不满，才觉得MapReduce慢。而不是觉得MapReduce慢，所以诞生了Spark。真实世界中的因果关系并非是顺承的，**我们常常意识不到问题的存在，直到有大神解决了这些问题**。


附上Spark框架发展历史中**重要的时间点**：
<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.1.png" style="zoom: 67%;" /></center>



### 7.1.2 Spark 与 Hadoop、MapReduce、HDFS的关系

那接下来的问题是，Spark自己有自己的体系，那么其和Hadoop之间的关系是什么呢？

我们先来回忆下Hadoop处理大数据的流程，Hadoop 来处理大数据，通常是这样的顺序：首先从 **HDFS** 读取输入数据；接着**在 Map 阶段**使用用户定义的 mapper function, 然后把结果写入磁盘；**在 Reduce 阶段**，从各个处于 Map 阶段的机器中读取 Map 计算的中间结果，使用用户定义的 reduce function, 通常最后**把结果写回 HDFS**。

而在这个过程中， 至少进行了三次数据读写，Hadoop处理大数据的流程高度依赖磁盘读写，那么在数据处理上就出现了瓶颈，面对更复杂的计算逻辑的处理任务时，Hadoop存在很大局限。

Spark在这样的背景下产生，其不像Hadoop一样采取磁盘读写，而是**基于性能更高的内存存储来进行数据存储和读写**（这里说的是计算数据的存储，而非持久化的存储）。但是Spark并非完美，其缺乏对数据存储这一块的支持--没有分布式文件系统，必须要依赖外部的数据源，这个依赖可以是Hadoop系统的HDFS，也可以是其他的分布式文件系统，也可以是mysql或本地文件系统。

基于以上分析，我们可以得出**结论**：Hadoop 和 Spark 两者都是大数据框架，但是各自存在的目的不尽相同。Hadoop 实质上更多是一个**分布式数据基础设施**，它将巨大的数据集分派到一个集群中的多个节点**进行存储**，也有**计算处理**的功能。Spark则是一个专门用来**对那些分布式存储的大数据进行处理的工具**，它并不会进行分布式数据的存储，可以部分看做是MapReduce的竞品（**准确的说是Spark Core**）。可以总结为下图：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.2_1.png" style="zoom: 67%;" /></center>

### 7.1.3 Spark生态体系
spark是一个用来实现快速而通用的集群计算的平台。

1. 速度方面：spark的一个主要特点就是能在内存中进行计算，因此速度要比mapreduce计算模型要更加高效，可以面向海量数据进行分析处理；
2. 通用方面：Spark 框架可以针对任何业务类型分析进行处理，比如SparkCore离线批处理、SparkSQL交互式分析、SparkStreaming和StructuredStreamig流式处理及机器学习和图计算都可以完成；

以 Spark 为基础，有支持 SQL 语句的 Spark SQL，有支持流计算的 Spark Streaming，有支持机器学习的 MLlib，还有支持图计算的GraphX。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.3_1.png" style="zoom: 67%;" /></center>

利用这些产品，Spark 技术栈支撑起大数据分析、大数据机器学习等各种大数据应用场景。





