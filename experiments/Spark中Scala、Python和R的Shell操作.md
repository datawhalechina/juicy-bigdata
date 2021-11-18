# Spark中Scala、Python和R的Shell操作

[TOC]

### 实验环境

Linux Ubuntu 16.04
前提条件：
1) Java 运行环境部署完成
2) R语言运行环境部署完成
3) Spark Local模式部署完成
上述前提条件，我们已经为你准备就绪了。

### 实验内容

在上述前提条件下，完成Spark中Scala、Python和R的Shell操作

### 实验步骤

#### 1.点击"命令行终端"，打开新窗口

#### 2.启动Scala的Shell

Scala是Spark默认的语言，在命令行终端中输入下面的命令即可启动Scala Shell

`spark-shell`

启动后终端显示如下：

![image-20210610124835335](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210610124835.png)

如上出现了 Scala> 表明进入了Scala的Shell

#### 3.使用Scala shell完成单词统计案例

在Scala shell中输入下面的Scala语句

`sc.textFile("file:///home/dolphin/words.txt").flatMap(_.split(" ")).map((_,1)).reduceByKey(_+_).saveAsTextFile("file:///home/dolphin/output")`

此时，在/home/dolphin/output目录下产生了结果文件。我们下载Scala命令行下输入下面命令来退出Scala命令行

`:quit`

此时又返回了命令行终端
输入下面的命令，来查看结果

`cat ~/output/part-*`

执行后显示如下，表明单词统计案例完成。

![image-20210610133415236](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210610133415.png)

![image-20210610125549021](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210610125549.png)

> 关于代码的说明：
> sc是SparkContext对象，该对象是提交Spark程序的入口
> textFile("file:///home/dolphin/words.txt")是在本地读取数据
> flatMap(_.split(" "))先map在压平
> map((_,1))将单词和1构成元组
> reduceByKey(_+_)按照key进行reduce，并将value累加
> saveAsTextFile("file:///home/dolphin/output")将结果写入到本地中

#### 4.启动Python的Shell

在命令行终端中输入下面的命令即可启动Python Shell

`pyspark`

启动后显示如下

![](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210610134049.png)


如上出现了 >>> 表明进入了Python的Shell

#### 5.使用Spark Python实现单词筛选的案例

在python的命令行中执行下面的代码
```
lines = sc.textFile("file:///apps/spark/README.md")
pythonLines = lines.filter(lambda line: "Python" in line)
pythonLines.count()
pythonLines.collect()
```

执行后显示如下：

![image-20210610140148643](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210610140148.png)

关于代码的说明：

> sc是SparkContext对象，该对象是提交Spark程序的入口
> textFile("file:///apps/spark/README.md")是hdfs中读取数据
> filter(lambda line: "Python" in line)是**过滤**掉不含"Python"的所有行
> **count()**是统计数量
> **collect()**是列出所有结果

退出Python shell，执行下面的命令

`exit()`

#### 6.使用R语言的Shell

在命令行终端中输入下面的命令即可启动R Shell

`sparkR`

执行后显示如下：

![image-20210610140334065](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210610140334.png)

如上显示 > 表明进入了R语言的Shell

#### 7.使用R操作SparkDataFrame

创建一个SparkDataFrame

`people <- read.df("/apps/spark/examples/src/main/resources/people.json", "json")`

显示df中的数据

`head(people)`

执行后显示如下

![image-20210610140501522](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210610140501.png)

只显示某一列数据

`head(select(people, "name"))`

执行后显示如下

![image-20210610140550468](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210610140550.png)

过滤数据

`head(filter(people, people$age > 20))`

执行后显示如下

![image-20210610140625909](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210610140625.png)


至此，本次实验结束啦

