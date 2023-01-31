# Chapter6 期中大作业

> 边圣陶，蒋志政，王洲烽

> &emsp;&emsp;本章节对前五章的内容掌握程度进行一个小小的测试，包括一些面向企业的面试题，和两道基础的实战编程题。学了理论知识这么久了，也该好好动动手喽，相信大作业的学习对小伙伴们有很大的提高！！

## 6. 1 面试题

### 6.1.1 简述Hadoop小文件弊端

1）HDFS 上每个文件都要在 NameNode 上创建对应的元数据，这个元数据的大小约为150byte，这样当小文件比较多的时候，就会产生很多的元数据文件，一方面会大量占用NameNode 的内存空间，另一方面就是元数据文件过多，使得寻址索引速度变慢。

2）小文件过多，在进行 MR 计算时，会生成过多切片，需要启动过多个 MapTask。每个MapTask 处理的数据量小，导致 MapTask 的处理时间比启动时间还小，白白消耗资源。

### 6.1.2 HDFS中DataNode挂掉如何处理？

1）副本冗余策略
  可以指定数据文件的副本数量，默认是3；
  保证所有的数据块都有副本，不至于在一个DataNode宕机后，数据出现丢失现象。

2）机架感知策略
  集群的机器一般处于不同机架上，机架间带宽要比机架内带宽要小；
  HDFS具有“机架感知”能力，它能自动实现在本机架上存放一个副本，然后在其它机架再存放另一副本，这样可以防止机架失效时数据丢失，也可以提高带宽利用率。

3）心跳策略
  NameNode周期性从DataNode接收心跳信号和块报告，NameNode根据块报告验证元数据；
  NameNode对没有按时发送心跳的DataNode会被标记为宕机，不会再给它任何I/O请求；
  DataNode失效造成副本数量下降，并且低于预先设置的阈值；NameNode会检测出这些数据块，并在合适的时机迕行重新复制；
  引发重新复制的原因还包括数据副本本身损坏、磁盘错误，复制因子被增大等。

### 6.1.3 HDFS中DataNode挂掉如何处理？

1）主备切换
  集群一般会有俩个NameNode，一个处于active状态，一个处于睡眠状态，当第一个Name Node挂掉，集群中睡眠状态的NameNode就会启动。

2）镜像文件和操作日志磁盘存储
  当集群启动的时候，在NameNode启动的时候，如果是集群格式化后，或者说是第一次启动，会创建一个空的(fsimage)镜像空间和(edits)日志文件；否则的话会产生一个新的fsimage和edits，并加载上一次的fsimage和edits到这次的fsimage中。

3）镜像文件和操作日志可以存储多分，多磁盘存储

### 6.1.4 HBase读写流程？

**读流程：**

1）HRegionServer保存着meta表以及表数据，要访问表数据，首先Client先去访问zookeeper，从zookeeper里面获取meta表所在的位置信息，即找到这个meta表在哪个HRegionServer上保存着

2）接着Client通过刚才获取到的HRegionServer的IP来访问Meta表所在的HRegionServer，从而读取到Meta，进而获取到Meta表中存放的元数据

3）Client通过元数据中存储的信息，访问对应的HRegionServer，然后扫描所在HRegionServer的Memstore和Storefile来查询数据

4）最后HRegionServer把查询到的数据响应给Client

**写流程：**

1）Client先访问zookeeper，找到Meta表，并获取Meta表元数据

2）确定当前将要写入的数据所对应的HRegion和HRegionServer服务器

3）Client向该HRegionServer服务器发起写入数据请求，然后HRegionServer收到请求并响应

4）Client先把数据写入到HLog，以防止数据丢失

5）然后将数据写入到Memstore

6）如果HLog和Memstore均写入成功，则这条数据写入成功

7）如果Memstore达到阈值，会把Memstore中的数据flush到Storefile中

8）当Storefile越来越多，会触发Compact合并操作，把过多的Storefile合并成一个大的Storefile

9）当Storefile越来越大，Region也会越来越大，达到阈值后，会触发Split操作，将Region一分为二

### 6.1.5 MapReduce为什么一定要有Shuffle过程

因为不同的 Map 可能输出相同的 Key，相同的 Key 必须发送到同一个 Reduce 端处理，因此需要Shuffle进行排序分区，减少跨节点数据传输的资源消耗。将数据完整的从map task端拉取数据到reduce task端减少磁盘IO对task的影响。

### 6.1.6 MapReduce中的三次排序

mr在Map任务和Reduce任务的过程中，一共发生了3次排序

1）当map函数产生输出时，会首先写入内存的环形缓冲区，当达到设定的阀值，在刷写磁盘之前，后台线程会将缓冲区的数据划分成相应的分区。在每个分区中，后台线程按键进行内排序

2）在Map任务完成之前，磁盘上存在多个已经分好区，并排好序的，大小和缓冲区一样的溢写文件，这时溢写文件将被合并成一个已分区且已排序的输出文件。由于溢写文件已经经过第一次排序，所有合并文件只需要再做一次排序即可使输出文件整体有序。

3）在reduce阶段，需要将多个Map任务的输出文件copy到ReduceTask中后合并，由于经过第二次排序，所以合并文件时只需再做一次排序即可使输出文件整体有序

在这3次排序中第一次是内存缓冲区做的内排序，使用的算法使快速排序，第二次排序和第三次排序都是在文件合并阶段发生的，使用的是归并排序。

### 6.1.7 MapReduce为什么不能产生过多小文件

**Hadoop小文件弊端**

1）HDFS 上每个文件都要在 NameNode 上创建对应的元数据，这个元数据的大小约为150byte，这样当小文件比较多的时候，就会产生很多的元数据文件，一方面会大量占用NameNode 的内存空间，另一方面就是元数据文件过多，使得寻址索引速度变慢。

2）小文件过多，在进行 MR 计算时，会生成过多切片，需要启动过多个 MapTask。每个MapTask 处理的数据量小，导致 MapTask 的处理时间比启动时间还小，白白消耗资源。

**小文件优化的方向**

1）在数据采集的时候，就将小文件或小批数据合成大文件再上传 HDFS。

2）在业务处理之前，在 HDFS 上使用 MapReduce 程序对小文件进行合并。

3）在 MapReduce 处理时，可采用 CombineTextInputFormat 提高效率

4）开启 uber 模式，实现 jvm 重用

## 6.2 实战

### 6.2.1 xxxxx



### 6.2.2 xxxxx





> 实战了第五章大内容，是不是感觉意犹未尽，放心吧，后边的内容更精彩！！！！！希望大家带着轻松愉快的态度去学习，积极面对困难，持久化学习！！！

