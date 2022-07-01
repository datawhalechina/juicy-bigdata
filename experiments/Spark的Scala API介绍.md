### 补充实验：Spark的Scala API的使用

#### 1 实验准备

**实验环境：** Linux Ubuntu 20.04  
**前提条件：**  

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.0.0的单点部署（详见第2章安装单机版Hadoop）
3. 完成Spark Local模式的部署（详见本章实验一：Spark Local模式的安装）

#### 2 实验内容

&emsp;&emsp;基于上述前提条件，完成Spark的Scala API的使用。

#### 3 实验步骤

##### 1.启动Scala的Shell

&emsp;&emsp;在命令行终端中输入下面的命令即可启动Scala Shell

```shell
spark-shell
```

&emsp;&emsp;启动后终端显示如下：

![](https://cdn.jsdelivr.net/gh/shenhao-stu/Big-Data/doc_imgs/ch7_sp2.1.png)

&emsp;&emsp;如上出现了 Scala> 表明进入了Scala的Shell

##### 2.RDD的创建方法

&emsp;&emsp;1） 由一个已经存在的Scala集合创建。

```scala
val rdd1 = sc.parallelize(Array(1,2,3,4,5,6,7,8))
```

&emsp;&emsp;2） 由外部存储系统的数据集创建，包括本地的文件系统，还有所有Hadoop支持的数据集，比如HDFS、Cassandra、HBase等

```scala
val rdd2 = sc.tsptFile("file:///opt/spark/README.md")
```

![](https://cdn.jsdelivr.net/gh/shenhao-stu/Big-Data/doc_imgs/ch7_sp3.1.png)

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
- **saveAsTsptFile(path)**
  将数据集的元素以tsptfile的形式保存到HDFS文件系统或者其他支持的文件系统，对于每个元素，Spark将会调用toString方法，将它装换为文件中的文本
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

![](https://cdn.jsdelivr.net/gh/shenhao-stu/Big-Data/doc_imgs/ch7_sp3.2.png)

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

![](https://cdn.jsdelivr.net/gh/shenhao-stu/Big-Data/doc_imgs/ch7_sp3.3.png)

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

![](https://cdn.jsdelivr.net/gh/shenhao-stu/Big-Data/doc_imgs/ch7_sp3.4.png)

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

![](https://cdn.jsdelivr.net/gh/shenhao-stu/Big-Data/doc_imgs/ch7_sp3.5.png)

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

![](https://cdn.jsdelivr.net/gh/shenhao-stu/Big-Data/doc_imgs/ch7_sp3.6.png)

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

![](https://cdn.jsdelivr.net/gh/shenhao-stu/Big-Data/doc_imgs/ch7_sp3.7.png)

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

![](https://cdn.jsdelivr.net/gh/shenhao-stu/Big-Data/doc_imgs/ch7_sp3.8.png)