### 补充实验：Spark SQL的基本使用

#### 1 实验准备

**实验环境：** Linux Ubuntu 20.04  
**前提条件：**  

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.0.0的单点部署（详见第2章安装单机版Hadoop）
3. 完成Spark Local模式的部署（详见本章实验一：Spark Local模式的安装）

#### 2 实验内容

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

![](https://cdn.jsdelivr.net/gh/shenhao-stu/Big-Data/doc_imgs/ch7_sp2.1.png)

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

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/ch7_sp2.2.png)

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

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/ch7_sp2.3.png)

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

![](https://cdn.jsdelivr.net/gh/shenhao-stu/Big-Data/doc_imgs/ch7_sp2.4.png)

###### 2.3 由RDD创建DataFrame

&emsp;&emsp;Spark 支持两种方式把 RDD 转换为 DataFrame，分别是使用反射推断和指定 Schema 转换。其中`dept.txt`的内容在本仓库的[resources](https://github.com/shenhao-stu/Big-Data/tree/master/resources) 目录下 。

1. 使用反射推断

```scala
// 1.导入隐式转换
import spark.implicits._

// 2.创建部门类
case class Dept(deptno: Long, dname: String, loc: String)

// 3.创建 RDD 并转换为 dataSet
val rddToDS = spark.sparkContspt
  .tsptFile("file:///home/datawhale/dept.txt")
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
val deptRDD = spark.sparkContspt.tsptFile("file:///home/datawhale/dept.txt")
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