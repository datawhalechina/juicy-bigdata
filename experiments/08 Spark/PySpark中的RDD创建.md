# PySpark中的RDD创建

[TOC]

## 1. 实验目标

- 学习使用PySpark创建RDD
- 了解PySpark中的数据存储读取模式

## 2. 本次实验主要使用的 $Python$ 库

| 名称         | 版本     | 简介       |
| ------------ | -------- | ---------- |
| $requests$   | $2.20.0$ | 线性代数   |
| $Pandas$     | $0.25.0$ | 数据分析   |
| $PySpark$    | $2.4.3$  | 大数据处理 |
| $Matplotlib$ | $3.0.1$  | 数据可视化 |

## 3. 适用的对象

- 本课程假设您已经学习了 $Python$ 基础，具备数据可视化基础
- 学习对象：本科学生、研究生、人工智能、算法相关研究者、开发者
- 大数据分析与人工智能

## 4. 研究流程图

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210610145017.png)

## 5. 实验步骤

### 步骤1 安装并引入必要的库

```python
# 安装第三方库
!pip install pyspark==2.4.5
```

```python 
# 获取数据集
import zipfile
with zipfile.ZipFile('/resources/jupyter/pyspark/pyspark_dataset_kdd.zip') as z:
    z.extractall()
```

在本实验中，我们将介绍***两种不同的方法***来将数据导入基本的Spark数据结构，即**Resilient Distributed Dataset**或**RDD**。RDD是元素的分布式集合。Spark中的所有工作都表示为创建新的RDDs，转换现有的RDDs或调用RDDs上的操作来计算结果。Spark自动将RDDs中包含的数据分布到集群中，并并行化对其执行的操作。

<font size = 4>**获取数据文件**</font>

1999年KDD杯比赛数据集的详细描述[KDDCUP1999](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99)。

在本实验中，我们将使用为1999年KDD杯提供的缩减数据集(10%)，其中包含近50万个网络交互。该文件作为*Gzip*文件提供，我们将在下载到本地。


### 步骤2 从文件创建RDD

创建RDD最常见的方法是从文件中加载它。注意，Spark的“textFile”可以直接处理压缩文件。

```python 
data_file = "./kddcup.data_10_percent.gz"
raw_data = sc.textFile(data_file)
```

现在我们将数据文件加载到 `raw_data` RDD中。

在不涉及 Spark *transformation* 和 *actions* 的情况下，我们可以做的最基本的检查RDD内容是否正确的事情是`count()`从文件加载到RDD中的数据行数。

```python 
raw_data.count()
```

<img src="https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210610145234.png" style="zoom: 67%;" />

我们还可以检查数据中的前几个条目。

```python 
raw_data.take(5)
```

<img src="https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210610145323.png" style="zoom:67%;" />

在接下来的实验中，我们将使用这些原始数据来了解不同的Spark转换和操作。****

### 步骤3 使用 `parallelize` 创建RDD

创建RDD的另一种方法是并行化已经存在的列表。

```python 
a = range(100)
data = sc.parallelize(a)
```

和前面一样，我们可以`count()`RDD中的元素数量。

```python 
data.count()
```

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210610145510.png)

和上面一样，我们可以访问RDD上的前几个元素。

```python 
data.take(5)
```

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210610145537.png)