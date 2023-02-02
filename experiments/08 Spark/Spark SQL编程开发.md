## Spark SQL编程开发

[TOC]

### 实验环境

Linux Ubuntu 16.04
1) Java 运行环境部署完成
2) Spark Local模式部署完成
上述前提条件，我们已经为你准备就绪了。

### 实验内容

在上述前提条件下，完成Spark SQL的基本开发

### 实验步骤

#### 1.点击"命令行终端"，打开新窗口

#### 2.启动Scala的Shell

在命令行终端中输入下面的命令即可启动Scala Shell

`spark-shell`

启动后终端显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611110343.png)

如上出现了 Scala> 表明进入了Scala的Shell

#### 3.了解Datasets 和 DataFrames

一个 Dataset 是一个分布式的数据集合。Dataset 是在 Spark 1.6 中被添加的新接口，它提供了 RDD 的优点（强类型化，能够使用强大的 lambda 函数）与 Spark SQL 优化的执行引擎的好处。一个 Dataset 可以从 JVM 对象来构造并且使用转换功能（map，flatMap，filter，等等）。Dataset API 在 Scala 和 Java 中是可用的。Python 不支持 Dataset API。但是由于 Python 的动态特性，许多 Dataset API 的有点已经可用了（也就是说，你可能通过 name 天生的 row.columnName 属性访问一行中的字段）。这种情况和 R 相似。

一个 DataFrame 是一个 Dataset 组织成的指定列。它的概念与一个在关系型数据库或者在 R/Python 中的表是相等的，但是有更多的优化。DataFrame 可以从大量的 Source 中构造出来，像 : 结构化的数据文件，Hive 中的表，外部的数据库，或者已存在的 RDD。DataFrame API 在 Scala，Java，Python 和 R 中是可用的。在 Scala 和 Java 中，一个 DataFrame 所代表的是一个多个 Row（行）的 Dataset。在 Scala API 中，DataFrame 仅仅是一个 Dataset[Row] 类型的别名 。然而，在 Java API 中，用户需要去使用 Dataset\<Row\> 来表示 DataFrame。

#### 4.RDD转换为DataFrame

读取本地infos.txt文件来创建RDD

`val infoRDD = spark.sparkContext.textFile("file:///home/dolphin/infos.txt")`

创建Info类

`case class Info(id:Int, name:String, age:Int)`

导入隐式转换

`import spark.implicits._`

RDD转化为DataFrame

`val infoDF = infoRDD.map(_.split(",")).map(line => Info(line(0).toInt, line(1), line(2).toInt)).toDF`

显示前20条数据

`infoDF.show()`

执行后，显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611110624.png)

#### 5.使用sql方式查询数据

先将DataFrame注册成一个infos表

`infoDF.createOrReplaceTempView("infos")`

使用sql语句查询数据

`spark.sql("select * from infos where age > 23").show()`

查询结果如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611110947.png)

#### 6.读取文件

spark的安装包中有测试文件，这里我们使用people.json文件来实验
在scala命令行中运行下面的文件，用于读取json文件，将json文件加载成DataFrame

`val peopleDF = spark.read.json("file:///apps/spark/examples/src/main/resources/people.json")`

打印Schema

`peopleDF.printSchema()`

执行后显示如下

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611111037.png)

#### 7.查询

打印数据集的前20条记录（这里只有三条记录）

`peopleDF.show`

执行后显示如下

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611111058.png)

查询某列所有数据，相当于sql中的select name from table

`peopleDF.select("name").show()`

执行后显示如下

![](C:\Users\56550\AppData\Roaming\Typora\typora-user-images\image-20210611111132507.png)

查询某几列所有的数据，并对列进行计算，相当于sql中的 select name, age + 10 from table

`peopleDF.select(peopleDF.col("name"), peopleDF.col("age") + 10).show()`

执行后显示如下：

<img src="https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611111213.png"/>

#### 8.条件过滤

根据某一列的值进行过滤，相当于sql中的 select * from table where age > 19

`peopleDF.filter(peopleDF.col("age") > 19).show()`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611111357.png)

#### 9.聚合

根据某一列进行分组再聚合，相当于sql中的 select age, count(1) from table group by age

`peopleDF.groupBy("age").count().show()`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611111421.png)

#### 10.存储文件

Spark SQL支持将数据存储为很多格式，如csv，json，text，parquet等等，这里我们将刚才处理的DataFrame存储为csv文件

`peopleDF.select("name", "age").write.format("csv").save("/home/dolphin/namesAndAges.csv")`

此时已经在/home/dolphin/目录下产生了namesAndAges.csv文件夹，我们先退出Scala命令行

`:quit`

显示存储的csv文件

`cat /home/dolphin/namesAndAges.csv/*.csv`

执行后显示如下

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611111507.png)


至此，本次实验结束啦。
