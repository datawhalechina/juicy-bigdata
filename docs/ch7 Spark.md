# 第七章：Spark

> 王嘉鹏

概述；数据模型；实现原理；运行机制；编程实战
## 7.1 Spark概述

### 7.1.1 Spark诞生
在Hadoop出现之前，分布式计算都是**专用系统**，只能用来处理某一类的计算，比如进行大规模的排序。这样的系统无法复用到其他大数据计算场景。

而Hadoop MapReduce出现后，使得大数据计算通用编程成为可能，只要遵循MapReduce编程模型编写业务处理代码，就可以运行在Hadoop分布式集群上，而无需关心分布式计算怎样完成。

紧接着，我们经常看到的说法是：`MapReduce 虽然已经可以满足大数据的应用场景，但是其执行速度和编程复杂度并不让人们满意。于是AMP lab的Spark应运而生`。

我们事后因果规律的分析上，往往容易**把结果当作了原因**  ---觉得是因为MapReduce执行的很慢，所以才去发明和使用Spark。

但事实上，在Spark出现之前，MapReduce并没有让人怨声载道，一方面Hive这些工具将常用的MapReduce编程进行了封装，转化为了更易于编写的SQL形式；一方面MR已经将分布式编程极大的进行了简化。

而当Spark出现后，性能比MapReduce快了100多倍。因为有了Spark，才对MapReduce不满，才觉得MapReduce慢。而不是觉得MapReduce慢，所以诞生了Spark。真实世界中的因果关系并非是顺承的，**我们常常意识不到问题的存在，直到有大神解决了这些问题**。


Spark框架发展历史中**重要的时间点**：
<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.1.png" style="zoom: 67%;" /></center>



### 7.1.2 Spark 为什么比MapReduce快？ 

在了解这个之前，必须要了解什么是内存和磁盘。**内存和磁盘两者都是存储设备**，但内存储存的是我们正在使用的资源，磁盘储存的是我们暂时用不到的资源。
可以把磁盘理解为一个仓库，而内存是进出这个仓库的通道。仓库（磁盘）很大，而通道（内存）很小，通道就很容易塞满。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.2_1.png" style="zoom: 67%;" /></center>


再次拿出第五章中辣椒酱的小demo（没印象的同学移步[这里]()），来看Spark和MapReduce在处理问题的方式上有什么区别：


假设把磁盘作为冰箱，内存为做饭时的操作台：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.2_2.png" style="zoom: 67%;" /></center>

Mapreduce每一个步骤发生在内存中但产生的中间值（溢写文件）都会写入在磁盘里，下一步操作时又会将这个中间值merge到内存中，如此循环，直到最终完成计算。

而对于Spark， Spark的每个步骤也是发生在内存之中，但产生的中间值会直接进入下一个步骤，直到所有的步骤完成之后才会将最终结果保存进磁盘。所以在使用Spark做数据分析能少进行很多次相对没有意义的读写，节省大量的时间。当步骤很多时，Spark的优势就体现出来了。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.2_3.png" style="zoom: 67%;" /></center>





### 7.1.3 Hadoop、Spark、MapReduce、HDFS的关系

