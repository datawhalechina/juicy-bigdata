# 第七章：Spark

## 7.1 大数据技术框架综述

已经到了第七章，我们已经对一些大数据的基本组件有所了解。实际上，一套大数据的解决方案通常会包含有多个重要的组件，从存储计算，到数据处理，再到利用统计计算方法，进行可视化分析。这里我们对大数据常用的技术框架做个简要的综述总结，再来引出本章的Spark内容。

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.1.png)

前面涉及到的大数据技术大致可以分为两个模块：**存储引擎**和**分析引擎**。

存储引擎通常用来存储海量数据，而分析引擎通常用来分析海量数据。

## 7.2 Spark概述

Spark框架发展的时间顺序：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.2_1.png)

spark是一个用来实现快速而通用的集群计算的平台。--《spark 快速大数据分析》

1. 速度方面：spark的一个主要特点就是能在内存中进行计算，因此速度要比mapreduce计算模型要更加高效，可以面向海量数据进行分析处理；
2. 通用方面：Spark 框架可以针对任何业务类型分析进行处理，比如SparkCore离线批处理、SparkSQL交互式分析、SparkStreaming和StructuredStreamig流式处理及机器学习和图计算都可以完成；

Spark框架核心数据结构：==RDD（弹性分布式数据集）==

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.2_2.png)

Spark 处理数据时，将数据封装到集合RDD，<font color=red>RDD中有很多分区Partition，每个分区数据被1个Task处理</font>。

对于Spark和Flink框架来说，每个Task任务以线程Thread方式运行，但是MapReduce中每个Task（MapTask或ReduceTask）以进程Process方式运行。线程运行 要快于进程运行。

Spark 框架仅仅就是处理分析数据，计算引擎：

- 数据来源
  - 任意地方都可以，Spark应用程序可以从任意地方读取数据，Spark 1.3开始提供一套外部数据源接口
  - 比如HDFS、JSON、CSV、Parquet、RDBMs、ES、Redis、Kafka等等
- 应用程序运行在哪
  - 本地模式Local，开发测试及小数据量
  - 集群模式：==YARN==、Standalone、Mesos
  - 容器中：K8s（Spark 2.3支持），Spark 1.x中支持Docker

整个Spark 框架模块包含：Spark Coke、 Spark SQL、 Spark Streaming、 Spark GraphX、Spark MLlib，而后四项的能力都是建立在核心引擎之上 。整个Spark 框架模块包含：Spark Coke、 Spark SQL、 Spark Streaming、 Spark GraphX、Spark MLlib，而后四项的能力都是建立在核心引擎之上 。

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.2_3.png)

本章内容主要对两个模块进行讲解，使用Scala语言开发

- SparkCore：RDD
- SparkSQL：DataFrame/Dataset = RDD + Schema



spark运行模式

本地模式（Local Mode）：启动1个JVM 进程，运行所有Task任务，每个Task运行需要1Core CPU。

并行度parallelism：同时运行几个Task任务

所以本地模式运行时，最好设置2个CPU Core，此时可以同时运行2个Task任务，相当并行计算。

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.2_4.png)

集群模式（Cluster Mode）：运行应用在YARN集群或者框架自身集群Standalone，启动多个JVM进程，运行Task程序。

- 管理者：AppMaster（MR）、Driver Program（Spark）、JobManager(Flink)
- 干活的：JVM进程中运行Task任务，MapTask和ReduceTask（MR）、Executor（Spark）、TaskManager（Flink）。

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.2_5.png)

## 7.3 Spark本地模式

本节根据已经提供好的虚拟机进行导入，并通过spark-shell交互，计算wordcount及圆周率的求算。

### 7.3.1 导入虚拟机

#### 步骤一：设置VMWare 网段地址

> 【编辑】->【虚拟网络编辑器】

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.1_1.png)

更改设置：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.1_2.png)



#### 步骤二：导入虚拟机至VMWare

> 注意：VMWare 虚拟化软件版本：==12.5.5+==

选择虚拟机中**vmx**文件

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.1_3.png)



#### 步骤三：启动虚拟机

> 当启动虚拟机时，弹出如下对话框，选择【我已移动改虚拟机】

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.1_4.png)

#### 步骤四：配置主机名和IP地址映射

> 文件路径：`C:\Windows\System32\drivers\etc\hosts`
>
> 内容如下：

192.168.88.100    node1.datawhale.cn    node1
192.168.88.101    node2.datawhale.cn    node2
192.168.88.102    node3.datawhale.cn    node3

### 7.3.2 运行spark-shell

> 启动HDFS集群以后，运行Spark框架自带交互式命令：`spark-shell`
>
> cd /export/server/spark
>
> bin/spark-shell

1、每个Spark Application运行时，提供WEB UI监控页面，端口号为4040

​	Spark context Web UI available at http://node1.itcast.cn:4040

2、每个SparkApplication程序入口为：**SparkContext**

​	Spark context available as 'sc' (master = local[2], app id = local-1599711246803).

SparkContext用于加载数据，封装到RDD集合中；调度每个Job执行

​		在启动spark-shell时，自动创建SparkContext对象，变量名称为：==sc==，提供给用户读取数据

3、从Spark 2.x开始，官方提供新的程序入口：SparkSession，底层还是SparkContext

​		Spark session available as 'spark'

​		在启动spark-shell时，自动创建SparkSession对象，变量名称为：==spark==，以供用户使用读取数据。

### 7.3.3 词频统计WordCount

> 在Spark框架中，进行词频统计WordCount：
>
> - 第一步、读取数据，封装数据至RDD集合
> - 第二步、分析数据，调用RDD中函数（高阶函数，很多函数与Scala集合中高阶函数类似，比如flatMap、map、filter、。。。。。）
> - 第三步、保存数据，将最终RDD结果数据保存至外部存储系统

在Spark数据结构RDD中reduceByKey函数，相当于MapReduce中shuffle和reduce函数合在一起：按照Key分组，将相同Value放在迭代器中，再使用reduce函数对迭代器中数据聚合。  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.3_1.png)



1. 准备数据文件： wordcount.data，内容如下，上传HDFS目录【/datas/】  

```scala
## 创建文件
vim wordcount.data
## 内容如下
spark spark hive hive spark hive
hadoop sprk spark
## 上传HDFS
hdfs dfs -put wordcount.data /datas/
```

2. 编写代码进行词频统计：  

```scala
## 读取HDFS文本数据，封装到RDD集合中，文本中每条数据就是集合中每条数据
val inputRDD = sc.textFile("/datas/wordcount.data")
## 将集合中每条数据按照分隔符分割，使用正则： https://www.runoob.com/regexp/regexp-syntax.html
val wordsRDD = inputRDD.flatMap(line => line.split("\\s+"))
## 转换为二元组，表示每个单词出现一次
val tuplesRDD = wordsRDD.map(word => (word, 1))
# 按照Key分组，对Value进行聚合操作， scala中二元组就是Java中Key/Value对
## reduceByKey：先分组，再聚合
val wordcountsRDD = tuplesRDD.reduceByKey((tmp, item) => tmp + item)
## 查看结果
wordcountsRDD.take(5)
## 保存结果数据到HDFs中
wordcountsRDD.saveAsTextFile("/datas/spark-wc")
## 查结果数据
hdfs dfs -text /datas/spark-wc/par*
```

![](E:\big-data-书\pic\ch7.3.3_2.png)

3. 结果如下

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.3_3.png)

### 7.3.4 运行圆周率PI

> 使用`spark-submit`提交运行自带圆周率PI，在本地模式运行。
>

1. 自带案例jar包：【/export/server/spark/examples/jars/spark-examples_2.11-2.4.5.jar】  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.4_1.png)

2. 使用spark-submit来提交运行PI程序

```scala
SPARK_HOME=/export/server/spark
${SPARK_HOME}/bin/spark-submit \
--master local[2] \
--class org.apache.spark.examples.SparkPi \
${SPARK_HOME}/examples/jars/spark-examples_2.11-2.4.5.jar \
10
```

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch7.3.4_2.png)



## 7.4 Spark Standalone集群

### 7.4.1 standalone 架构

Standalone集群使用了分布式计算中的master-slave模型， master是集群中含有Master进程的节点， slave是集群中的Worker节点含有Executor进程。  

Spark Standalone集群，类似Hadoop YARN，管理集群资源和调度资源。



