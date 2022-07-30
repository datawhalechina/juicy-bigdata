# PySpark中的SQL
[TOC]
## 1. 实验目标
- 使用PySpark创建RDD，并学习PySpark中的SQL基本操作

## 2. 本次实验主要使用的 $Python$ 库

| 名称         | 版本     | 简介       |
| ------------ | -------- | ---------- |
| $Pandas$     | $0.25.0$ | 数据分析   |
| $PySpark$    | $2.4.5$  | 大数据处理 |
| $Matplotlib$ | $3.1.0$  | 数据可视化 |

## 3. 适用的对象

- 本课程假设您已经学习了 $Python$ 基础，具备数据可视化基础
- 学习对象：本科学生、研究生、人工智能、算法相关研究者、开发者
- 大数据分析与人工智能

## 4. 研究流程图

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611111836.png)

本实验将引入Spark功能，以结构化的方式处理数据。基本上，一切都围绕着*Data Frame*的概念，并使用*SQL语言*查询它们。
我们将看到在其他数据分析生态系统(例如R和Python/ panda)中非常流行的数据框架抽象在执行探索性数据分析时是如何非常强大的。
事实上，当与SQL语言一起使用时，表达数据查询非常容易。此外，Spark还透视地分布了这种基于列的数据结构，以使查询过程尽可能高效。

## 5. 实验步骤

### 步骤1 安装并引入必要的库

```python
# 安装第三方库
!pip install pyspark==2.4.5
!pip install numpy==1.16.0
!pip install pandas==0.25.0
```

```python 
import numpy as np
import pandas as pd
from time import time

from pyspark.sql import SQLContext
from pyspark.sql import Row

# 获取数据集
import zipfile
with zipfile.ZipFile('/resources/jupyter/pyspark/pyspark_dataset_kdd.zip') as z:
    z.extractall()
```

### 步骤2 获取数据并创建RDD

正如我们在之前的实验中所做的那样，我们将使用[KDD Cup 1999](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)提供的缩减数据集(10%)，其中包含近50万个互联网交互。该文件作为Gzip文件提供，我们将在下载到本地。

```python
data_file = "./kddcup.data_10_percent.gz"
raw_data = sc.textFile(data_file).cache()
```

### 步骤3 获取Data Frame
Spark`DataFrame`是一个分布式的数据集合，这些数据被组织到指定的列中。
它在概念上等价于关系数据库中的表、R或panda中的DataFrame。
它们可以由大量的源构建，比如我们的例子中已有的RDD。

Spark中所有SQL功能的入口点是`SQLContext`类。
要创建一个基本实例，我们只需要引入`SparkContext`。
由于我们在shell模式下运行Spark(使用pySpark)，因此可以使用全局上下文对象`sc`来实现此目的。

```python
sqlContext = SQLContext(sc)
```

#### 3.1 Inferring the schema 推断模式

使用`SQLContext`，我们可以从现有的RDD创建一个`DataFrame`。
但首先我们需要将数据中的模式告诉`Spark SQL`。

`Spark SQL`可以将`Row`对象的RDD转换为`DataFrame`。行是通过将键/值对列表作为*kwargs*传递给`Row`类来构造的。
键定义列名，类型通过查看第一行来推断。因此，为了正确地推断模式，在RDD的第一行中没有丢失数据是很重要的。

在我们的示例中，首先需要分割逗号分隔的数据，然后使用KDD 1999任务描述中的信息来获得[列名](http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names)。#### 3.1 Inferring the schema 推断模式

使用`SQLContext`，我们可以从现有的RDD创建一个`DataFrame`。
但首先我们需要将数据中的模式告诉`Spark SQL`。

`Spark SQL`可以将`Row`对象的RDD转换为`DataFrame`。行是通过将键/值对列表作为*kwargs*传递给`Row`类来构造的。
键定义列名，类型通过查看第一行来推断。因此，为了正确地推断模式，在RDD的第一行中没有丢失数据是很重要的。

在我们的示例中，首先需要分割逗号分隔的数据，然后使用KDD 1999任务描述中的信息来获得[列名](http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names)。

```python

csv_data = raw_data.map(lambda l: l.split(","))
row_data = csv_data.map(lambda p: Row(
    duration=int(p[0]), 
    protocol_type=p[1],
    service=p[2],
    flag=p[3],
    src_bytes=int(p[4]),
    dst_bytes=int(p[5])
    )
)
```

一旦我们有了`Row`的RDD，我们就可以推断并注册模式。

```python
interactions_df = sqlContext.createDataFrame(row_data)
interactions_df.registerTempTable("interactions")
```

现在，我们可以在已注册为表的数据框架上运行SQL查询。

```python
# 选择持续时间超过1秒且不从目标传输的tcp网络交互
tcp_interactions = sqlContext.sql("""
    SELECT duration, dst_bytes FROM interactions WHERE protocol_type = 'tcp' AND duration > 1000 AND dst_bytes = 0
""")
tcp_interactions.show()
```

 ![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611112315.png)

SQL查询的结果是RDDs并支持所有正常的RDD操作。

```python
# 输出持续时间和dst_bytes
tcp_interactions_out = tcp_interactions.rdd.map(
    lambda p: "Duration: {}, Dest. bytes: {}".format(p.duration, p.dst_bytes))
for ti_out in tcp_interactions_out.collect():
    print(ti_out)
```

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611112340.png)

我们可以很容易地使用`printSchema`查看我们的数据结构。

```python
interactions_df.printSchema()
```

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611112416.png)

### 步骤4 查询作为`DataFrame`操作

Spark `DataFrame`为结构化数据操作提供了一种特定于域的语言。
该语言包含了我们可以连接的方法，以便进行选择、过滤、分组等。
例如，假设我们想要计算每种协议类型有多少交互。我们可以这样进行。

```python

t0 = time()
interactions_df.select("protocol_type", "duration",
                       "dst_bytes").groupBy("protocol_type").count().show()
tt = time() - t0

print("Query performed in {} seconds".format(round(tt, 3)))
```

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611112449.png)

现在，假设我们想要计算有多少交互持续时间超过1秒，没有从目的地传输数据，按协议类型分组。我们可以只添加到前面的过滤器调用。

```python
t0 = time()
interactions_df.select(
    "protocol_type", "duration",
    "dst_bytes").filter(interactions_df.duration > 1000).filter(
        interactions_df.dst_bytes == 0).groupBy(
            "protocol_type").count().show()
tt = time() - t0

print("Query performed in {} seconds".format(round(tt, 3)))
```

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611112517.png)

我们可以使用它来执行一些[探索性数据分析](http://en.wikipedia.org/wiki/Exploratory_data_analysis)。
让我们来计算一下我们有多少攻击和正常的交互。首先，我们需要将label列添加到数据中。

```python
def get_label_type(label):
    if label!="normal.":
        return "attack"
    else:
        return "normal"
    
row_labeled_data = csv_data.map(lambda p: Row(
    duration=int(p[0]), 
    protocol_type=p[1],
    service=p[2],
    flag=p[3],
    src_bytes=int(p[4]),
    dst_bytes=int(p[5]),
    label=get_label_type(p[41])
    )
)
interactions_labeled_df = sqlContext.createDataFrame(row_labeled_data)
```

这次我们不需要注册模式，因为我们将使用OO查询接口。

让我们通过计算DataFrame中的攻击和正常数据来检查前面的方法是否有效。

```python
t0 = time()
interactions_labeled_df.select("label").groupBy("label").count().show()
tt = time() - t0

print("Query performed in {} seconds".format(round(tt, 3)))
```

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611112609.png)

现在，我们要根据标签和协议类型对它们进行计数，以便了解协议类型在检测交互是否为攻击时有多重要。

```python
t0 = time()
interactions_labeled_df.select("label", "protocol_type").groupBy(
    "label", "protocol_type").count().show()
tt = time() - t0

print("Query performed in {} seconds".format(round(tt, 3)))
```

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611112651.png)

乍一看，与其他协议类型相比，*udp*交互在网络攻击中所占的比例较低。

我们可以做更复杂的分组。例如，根据来自目标的数据传输添加到前面的“分割”。

```python
t0 = time()
interactions_labeled_df.select("label", "protocol_type", "dst_bytes").groupBy(
    "label", "protocol_type",
    interactions_labeled_df.dst_bytes == 0).count().show()
tt = time() - t0

print("Query performed in {} seconds".format(round(tt, 3)))
```

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210611112725.png)

我们将看到这个新的分割与确定网络交互是否为攻击有多么相关。

我们将在这里停止实验，但是我们可以看到为了研究我们的数据，这种类型的查询是多么强大。
实际上，当我们引入分类树时，只需选择、摸索和过滤我们的Dataframe，就可以复制我们在以前的实验中看到的所有分割。
有关Spark的`DataFrame`操作和数据源的更详细列表，请查看官方文档[此处](https://spark.apache.org/docs/latest/sql-programming-guide.html#dataframe-operations)。