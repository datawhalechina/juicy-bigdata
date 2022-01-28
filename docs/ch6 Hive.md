# Chapter6 数据仓库Hive

> 王嘉鹏，shenhao

## 6.0 数据仓库
> ps：到了数据仓库啦，崭新的饱满的和知识相濡以沫的一天，又开始啦！！！！

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.0.png" style="zoom:67%;" /></center>

### 6.0.1 为什么要有数据仓库

&emsp;&emsp;在引入数据仓库之前，我们先来聊聊为什么会产生数据仓库呢！！

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.0.1.png" style="zoom:33%;" /></center>

&emsp;&emsp;数据的作用有两个：操作型记录的保存和分析型决策的制定。
- 操作型记录的保存意味着企业通常不必维护历史数据，只需修改数据以反映最新的状态；
- 分析型决策意味着企业需要保存历史的数据，从而可以更精确的来评估现有状况进行决策。

&emsp;&emsp;基于后者分析型决策的优化，需要高性能地完成用户的查询，因此引出了数据仓库的概念。

### 6.0.2 数据仓库概念

&emsp;&emsp;数据仓库是一个**面向主题的**、**集成的**、**非易失的**、**随时间变化的**，用来**支持管理人员决策**的数据集合，数据仓库中包含了粒度化的企业数据。  
&emsp;&emsp;随着信息技术的普及和企业信息化建设步伐的加快，企业逐步认识到建立企业范围内的统一数据存储的重要性，越来越多的企业已经建立或正在着手建立企业数据仓库。企业数据仓库有效集成了来自不同部门、不同地理位置、具有不同格式的数据，为企业管理决策者提供了企业范围内的单一数据视图，从而为综合分析和科学决策奠定了坚实的基础。  
&emsp;&emsp;如下图所示，数据仓库的主要特征是：**主题性**、**集成性**、**非易失性**、**时变性**。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.0.2_1.png" style="zoom:33%;" /></center>

1. 主题性  
   &emsp;&emsp;各个业务系统的数据可能是相互分离的，但数据仓库则是**面向主题的**。数据仓库将不同的业务进行归类并分析，将数据抽象为主题，用于对应某一分析领域所涉及的分析对象。  
   &emsp;&emsp;而操作型记录（即传统数据）对数据的划分并不适用于决策分析。在数据仓库中，基于主题的数据被划分为各自独立的领域，每个领域有各自的逻辑内涵但互不交叉，在抽象层次上对数据进行完整的、一致的和准确的描述。  
   &emsp;&emsp;以零售业务的过程为例：将多个零售业务数据（杂货、冷冻食品、生活用品、肉类等），依据业务主题进行数据划分，可创建一个具有订单、库存和销售等多个业务领域的零售业务数仓。  
   
<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.0.2_2.png" style="zoom:50%;" /></center>

2. 集成性  
   &emsp;&emsp;确定主题之后，就需要获取与主题相关的数据。这些数据会分布在不同的业务过程中，因此在数据进入数仓之前，需要对这些数据的口径进行统一。  
   &emsp;&emsp;口径统一是指，统一数据来源中的歧义、单位、字长等元素，并进行总和计算，来聚合成新的数据。  
   &emsp;&emsp;以上述零售业务过程中的订单主题为例，对于订单主题，通常会包括三个业务过程：订单、发货和发票。这些过程会产生一些新的指标，如：销售额、发票收入等。  

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.0.2_3.png"  /></center>

3. 非易失性  
   &emsp;&emsp;数据仓库的目的是分析数据中的规律，因此，添加到数据仓库中的数据，需要保证其稳定，不会轻易丢失和改变。  
   &emsp;&emsp;这里，与传统操作型数据库的区别在于：操作型数据库主要服务于日常的业务操作，产生的数据会实时更新到数据库中，以便业务应用能够迅速获得当前最新数据，不至于影响正常的业务运作。而数据仓库通常是保存历史业务数据，根据业务需要每隔一段时间将一批新的数据导入数据仓库。  

4. 时变性  
   &emsp;&emsp;数据仓库是根据业务需要来建立的，代表了一个业务过程。因此数据仓库分析的结果只能反映过去的业务情况，当业务变化后，数据仓库需要跟随业务的变化而改变，以适应分析决策的需要。  

### 6.0.3 数据仓库的体系结构

&emsp;&emsp;数据仓库的体系结构通常包含4个层次：数据源、数据存储和管理、数据服务以及数据应用。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.0.3.png" style="zoom:33%;" /></center>

- 数据源：数据仓库的数据来源，包括外部数据、现有业务系统和文档资料等。
- 数据存储和管理：为数据提供的存储和管理，包括数据仓库、数据集市、数据仓库监视、运行与维护工具和元数据管理等。
- 数据服务：为前端工具和应用提供数据服务，包括直接从数据仓库中获取数据提供给前端使用，或者通过`OLAP`服务器为前端应用提供更为复杂的数据服务。
- 数据应用：直接面向最终用户，包括数据工具、自由报表工具、数据分析工具、数据挖掘工具和各类应用系统。

### 6.0.4 面临的挑战

&emsp;&emsp;随着大数据时代的全面到来，传统数据仓库也面临了如下挑战：

- 无法满足快速增长的海量数据存储需求
- 无法有效处理不同类型的数据
- 计算和处理能力不足

## 6.1 Hive基本概念

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.1.png" style="zoom:33%;" /></center>

### 6.1.1 概述

&emsp;&emsp;**Hive是建立在Hadoop之上的一种数仓工具**。该工具的功能是将**结构化**、**半结构化**的数据文件映射为一张**数据库表**，基于数据库表，提供了一种类似`SQL`的查询模型（`HQL`），用于访问和分析存储在`Hadoop`文件中的大型数据集。  
&emsp;&emsp;`Hive`本身并不具备存储功能，其核心是将`HQL`转换为`MapReduce`程序，然后将程序提交到`Hadoop`集群中执行。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.1.1.png" style="zoom: 50%;" /></center>

**特点**：  
1. 简单、容易上手（提供了类似`SQL`的查询语言`HiveQL`），使得精通`SQL`却不了解`Java` 编程的人也能很好地进行大数据分析；
2. 灵活性高，可以自定义用户函数（UDF）和存储格式；
3. 为超大的数据集设计的计算和存储能力，集群扩展容易;
4. 统一的元数据管理，可与`presto`/`impala`/`sparksql`等共享数据；
5. 执行延迟高，不适合做数据的实时处理，但适合做海量数据的离线处理。

### 6.1.2 产生背景

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.1.2.png" style="zoom: 50%;" /></center>

&emsp;&emsp;`Hive`的产生背景主要有两个：  

- **使用成本高**：使用`MapReduce`直接处理数据时，需要掌握`Java`等编程语言，学习成本较高，而且使用`MapReduce`不容易实现复杂查询；
- **建立分析型数仓的需求**：`Hive`支持类`SQL`的查询以及支持自定义函数，可以作为数据仓库的工具。

&emsp;&emsp;`Hive`利用`HDFS`存储数据，使用`MapReduce`查询分析数据。将`SQL`转换为`MapReduce`程序，从而完成对数据的分析决策。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.1.2_emoji.png" style="zoom:50%;" /></center>

### 6.1.3 Hive与Hadoop生态系统

&emsp;&emsp;下图描述了当采用`MapReduce`作为执行引擎时，`Hive`与`Hadoop`生态系统中其他组件的关系。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.1.3.png" alt="image-20211225161347381" style="zoom:33%;" /></center>

- **Hive与Hadoop生态的联系**

&emsp;&emsp;`HDFS`作为高可靠的底层存储方式，可以存储海量数据。`MapReduce`对这些海量数据进行批处理，实现高性能计算。`Hive`架构位于`MapReduce` 、`HDFS`之上，其自身并不存储和处理数据，而是分别借助于`HDFS`和`MapReduce`实现数据的存储和处理，用`HiveQL`语句编写的处理逻辑，最终都要转换成`MapReduce`任务来运行。`Pig`可以作为`Hive`的替代工具，它是一种数据流语言和运行环境，适用于在`Hadoop`平台上查询半结构化数据集，常用于数据抽取（`ETL`）部分，即将外部数据装载到`Hadoop`集群中，然后转换为用户需要的数据格式。  

- **Hive与HBase的区别**

&emsp;&emsp;`HBase`是一个面向列式存储、分布式、可伸缩的数据库，它可以提供数据的实时访问功能，而`Hive`只能处理静态数据，主要是`BI`报表数据。就设计初衷而言，在`Hadoop`上设计`Hive`，是为了减少复杂`MapReduce`应用程序的编写工作，在`Hadoop`上设计`HBase`是为了实现对数据的实时访问。所以，`HBase`与`Hive`的功能是互补的，它实现了`Hive`不能提供的功能。

### 6.1.4 Hive与传统数据库的对比

&emsp;&emsp;`Hive`在很多方面和传统数据库类似，但是，它的底层依赖的是`HDFS`和`MapReduce`（或`Tez`、`Spark`）。以下将从各个方面，对`Hive`和传统数据库进行对比分析。

| 对比内容 | Hive | 传统数据库 |
| :---: | :---: | :---: |
| 数据存储 | HDFS | 本地文件系统 |
| 索引 | 支持有限索引 | 支持复杂索引 |
| 分区 | 支持 | 支持 |
| 执行引擎 | MapReduce、Tez、Spark | 自身的执行引擎 |
| 执行延迟 | 高 | 低 |
| 扩展性 | 好 | 有限 |
| 数据规模 | 大 | 小 |


> ps：看完了Hive的特点后，一定很好奇这东西的内部构造是啥吧，小伙伴们，请跟我来，坚持学习，沉迷学习，忘我学习，冲冲冲！！！

### 6.1.5 模拟实现Hive

&emsp;&emsp;这里通过一个简单的需求，来帮助我们更好地理解`Hive`的原理。

- **需求**：在`HDFS`文件系统上有一个文件，其内容如下：

```
1,jingjing,26,hangzhou
2,wenrui,26,beijing
3,dapeng,26,beijing
4,tony,15,hebei
```

&emsp;&emsp;需要根据上述文本内容来设计`Hive`数仓，通过这个数仓，实现用户通过编写`SQL`语句，来处理位于`HDFS`文件系统上的结构化数据，从而统计**来自北京**的**年龄大于20**的人数。

- **分析**：写`SQL`的前提是对表进行操作，而不能是针对文件。那么需要记录文件和表之间的对应关系，关系示意图如下：

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.1.4.png" style="zoom:50%;" /></center>

&emsp;&emsp;要实现上图所示的文件和表的对应关系，关键在于**实现表和文件的映射**，那么需要记录的信息包括：  
- 表是对应于哪个文件的，即表的位置信息；
- 表的列是对应文件的哪一个字段，即字段的位置信息；
- 文件字段之间的分隔符是什么，即内容读取时的分隔操作；

&emsp;&emsp;完成了表和文件的映射后，`Hive`需要对用户编写的`SQL`语句进行语法校验，并且根据记录的元数据信息对`SQL`进行解析，制定执行计划，并将执行计划转化为`MapReduce`程序来执行，最终将执行的结果封装返回给用户。  
&emsp;&emsp;接下来，在`Hive`的核心概念中，我们进一步了解一下表和文件的映射信息。

## 6.2 Hive核心概念

### 6.2.1 Hive数据类型

- **基本数据类型**

&emsp;&emsp;`Hive`表中的列支持以下基本数据类型：

| 大类 | 类型 |
| :--- | :--- |
| Integers（整型） | TINYINT：1字节的有符号整数；<br>SMALLINT：2字节的有符号整数；<br>INT：4字节的有符号整数；<br>BIGINT：8字节的有符号整数 |
| Boolean（布尔型）| BOOLEAN：TRUE/FALSE |
| Floating point numbers（浮点型）| FLOAT：单精度浮点型；<br>DOUBLE：双精度浮点型 |
| Fixed point numbers（定点数）| DECIMAL：用户自定义精度定点数，比如 DECIMAL(7,2) |
| String types（字符串）| STRING：指定字符集的字符序列；<br>VARCHAR：具有最大长度限制的字符序列；<br>CHAR：固定长度的字符序列 |
| Date and time types（日期时间类型） | TIMESTAMP：时间戳；<br>TIMESTAMP WITH LOCAL TIME ZONE：时间戳，纳秒精度；<br>DATE：日期类型 |
| Binary types（二进制类型）| BINARY：字节序列 |

> 注：`TIMESTAMP`和`TIMESTAMP WITH LOCAL TIME ZONE`的区别如下：  
> - **TIMESTAMP WITH LOCAL TIME ZONE**：用户提交`TIMESTAMP`给数据库时，会被转换成数据库所在的时区来保存。查询时，则按照查询客户端的不同，转换为查询客户端所在时区的时间。  
> - **TIMESTAMP** ：提交的时间按照原始时间保存，查询时，也不做任何转换。

- **隐式转换**

&emsp;&emsp;`Hive`中基本数据类型遵循以下的层次结构，按照这个层次结构，子类型到祖先类型允许隐式转换。例如`INT`类型的数据允许隐式转换为`BIGINT`类型。额外注意的是：按照类型层次结构，允许将`STRING`类型隐式转换为`DOUBLE`类型。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.2.1.png" style="zoom:33%;" /></center>

- **复杂类型**

| 类型 | 描述 | 示例 |
| --- | --- | --- |
| STRUCT | 类似于对象，是字段的集合，字段的类型可以不同，可以使用`名称.字段名`方式进行访问 | STRUCT('xiaoming', 12 , '2018-12-12') |
| MAP | 键值对的集合，可以使用`名称[key]`的方式访问对应的值 | map('a', 1, 'b', 2) |
| ARRAY | 数组是一组具有相同类型和名称的变量的集合，可以使用`名称[index]`访问对应的值 | ARRAY('a', 'b', 'c', 'd') |

- **示例**

&emsp;&emsp;下面是一个基本数据类型和复杂数据类型的使用示例：

```sql
CREATE TABLE students(
  name      STRING,   -- 姓名
  age       INT,      -- 年龄
  subject   ARRAY<STRING>,   -- 学科
  score     MAP<STRING,FLOAT>,  -- 各个学科考试成绩
  address   STRUCT<houseNumber:int, street:STRING, city:STRING, province:STRING>  -- 家庭居住地址
) ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";
```

### 6.2.2 Hive数据模型

&emsp;&emsp;`Hive`的数据都是存储在`HDFS`上的，默认有一个根目录，在`hive-site.xml`中可以进行配置数据的存储路径。`Hive`数据模型的含义是，描述`Hive`组织、管理和操作数据的方式。`Hive`包含如下4种数据模型：

1. **库**  
&emsp;&emsp;`MySQL`中默认数据库是`default`，用户可以创建不同的`database`，在`database`下也可以创建不同的表。`Hive`也可以分为不同的数据（仓）库，和传统数据库保持一致。在传统数仓中创建`database`。默认的数据库也是`default`。`Hive`中的库相当于关系数据库中的命名空间，它的作用是将用户和数据库的表进行隔离。  

2. **表**  
&emsp;&emsp;`Hive`中的表所对应的数据是存储在`HDFS`中，而表相关的元数据是存储在关系数据库中。Hive中的表分为内部表和外部表两种类型，两者的区别在于数据的访问和删除：  
- 内部表的加载数据和创建表的过程是分开的，在加载数据时，实际数据会被移动到数仓目录中，之后对数据的访问是在数仓目录实现。而外部表加载数据和创建表是同一个过程，对数据的访问是读取`HDFS`中的数据；
- 内部表删除时，因为数据移动到了数仓目录中，因此删除表时，表中数据和元数据会被同时删除。外部表因为数据还在`HDFS`中，删除表时并不影响数据。
- 创建表时不做任何指定，默认创建的就是内部表。想要创建外部表，则需要使用`External`进行修饰

| 对比内容 | 内部表 | 外部表 |
| :--- | :--- | :--- |
| 数据存储位置 | 内部表数据存储的位置由`hive.Metastore.warehouse.dir`参数指定，<br>默认情况下，表的数据存储在`HDFS`的`/user/hive/warehouse/数据库名.db/表名/`目录下 | 外部表数据的存储位置创建表时由`Location`参数指定 |
| 导入数据 | 在导入数据到内部表，内部表将数据移动到自己的数据仓库目录下，<br>数据的生命周期由`Hive`来进行管理 | 外部表不会将数据移动到自己的数据仓库目录下，<br>只是在元数据中存储了数据的位置 |
| 删除表 | 删除元数据（metadata）和文件 | 只删除元数据（metadata） |

3. **分区**  
&emsp;&emsp;分区是一个优化的手段，目的是**减少全表扫描**，提高查询效率。在`Hive`中存储的方式就是表的主目录文件夹下的子文件夹，子文件夹的名字表示所定义的分区列名字。
4. **分桶**  
&emsp;&emsp;分桶和分区的区别在于：分桶是针对数据文件本身进行拆分，根据表中字段（例如，编号ID）的值，经过`hash`计算规则，将数据文件划分成指定的若干个小文件。分桶后，`HDFS`中的数据文件会变为多个小文件。分桶的优点是**优化join查询**和**方便抽样查询**。

## 6.3 Hive系统结构

&emsp;&emsp;`Hive`主要由用户接口模块、驱动模型以及元数据存储模块3个模块组成，其系统架构如下图所示：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.3.png)

### 6.3.1 用户接口模块

&emsp;&emsp;用户接口模块包括`CLI`、`Hive`网页接口（Hive Web Interface，HWI）、`JDBC`、`ODBC`、`Thrift Server`等，主要实现外部应用对`Hive`的访问。用户可以使用以下两种方式来操作数据：

- **CLI**（command-line shell）：`Hive`自带的一个命令行客户端工具，用户可以通过`Hive`命令行的方式来操作数据；
- **HWI**（Thrift/JDBC）：`HWI`是`Hive`的一个简单网页，`JDBC`、`ODBS`和`Thrift Server`可以向用户提供编程访问的接口。用户可以按照标准的`JDBC`的方式，通过`Thrift`协议操作数据。

### 6.3.2 驱动模块

&emsp;&emsp;驱动模块（Driver）包括编译器、优化器、执行器等，所采用的执行引擎可以是 `MapReduce`、`Tez`或`Spark`等。当采用`MapReduce`作为执行引擎时，驱动模块负责把 `HiveQL`语句转换成一系列`MapReduce`作业，所有命令和查询都会进入驱动模块，通过该模块对输入进行解析编译，对计算过程进行优化，然后按照指定的步骤执行。

### 6.3.3 元数据存储模块

- **元数据：**  
	&emsp;&emsp;元数据（metadata）是**描述数据的数据**，对于`Hive`来说，元数据就是用来描述`HDFS`文件和表的各种对应关系（位置关系、顺序关系、分隔符）。`Hive`的元数据存储在**关系数据库**中（`Hive`内置的是`Derby`、第三方的是`MySQL`），`HDFS`中存储的是数据。在`Hive`中，所有的元数据默认存储在`Hive`内置的`Derby`数据库中，但由于`Derby`只能有一个实例，也就是说不能有多个命令行客户端同时访问，所以在实际生产环境中，通常使用` MySQL`代替`Derby`。  
	&emsp;&emsp;元数据存储模块（Metastore）是一个独立的关系数据库，通常是与`MySQL`数据库连接后创建的一个`MySQL`实例，也可以是`Hive`自带的`Derby`数据库实例，提供**元数据服务**。元数据存储模块中主要保存表模式和其他系统元数据，如表的名称、表的列及其属性、表的分区及其属性、表的属性、表中数据所在位置信息等。它提供给`Hive`操作管理访问元数据的一个服务，具体操作为`Metastore`对外提供一个服务地址，使客户端能够连接`Hive`，以此来对元数据进行访问。使用`Metastore`的好处如下：  
	- 元数据把数据保存在关系数据库中，`Hive`提供元数据服务，通过对外的服务地址，用户能够使用客户端连接`Hive`，访问并操作元数据；
	- 支持多个客户端的连接，而客户端无需关心数据的存储地址，实现了数据访问层面的解耦操作。
	- 因此如果你在`Hive`上创建了一张表，然后在`presto`/`impala`/`sparksql`中都是可以直接使用的，它们会从`Metastore`中获取统一的元数据信息，同样的你在`presto`/`impala`/`sparksql`中创建一张表，在`Hive`中也可以直接使用。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.3.3_1.png" style="zoom: 50%;" /></center>

- **`Metastore`管理元数据的方式：**

1. **内嵌模式**  
&emsp;&emsp;`Metastore`**默认的**部署模式是`Metastore`元数据服务和`Hive`服务融合在一起。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.3.3_2.png" style="zoom:50%;" /></center>

&emsp;&emsp;在这种模式下，`Hive`服务（即`Hive`驱动本身）、元数据服务`Metastore`，元数据`metadata`（用于存储映射信息）都在同一个`JVM`进程中，元数据存储在内置的**Derby数据库**。当启动`HiveServer`进程时，`Derby`和`Metastore`都会启动，不需要额外启动`Metastore`服务。但是，一次只能支持一个用户访问，适用于测试场景。  

2. **本地模式**  
&emsp;&emsp;本地模式与内嵌模式的区别在于：把元数据提取出来，让`Metastore`服务与`HiveServer`主进程在同一个`JVM`进程中运行，存储元数据的数据库在单独的进程中运行。元数据一般存储在`MySQL`关系型数据库中。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.3.3_3.png" style="zoom:50%;" /></center>

&emsp;&emsp;但是，每启动一个`Hive`服务，都会启动一个`Metastore`服务。多个人使用时，会启用多个`Metastore`服务。  

3. **远程模式**  
&emsp;&emsp;既然可以把元数据存储给提取出来，也可以考虑把`Metastore`给提取出来变为单独一个进程。把`Metastore`单独进行配置，并在单独的进程中运行，可以保证全局唯一，从而保证数据访问的安全性。（即不随`Hive`的启动而启动）

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.3.3_4.png" style="zoom:50%;" /></center>

&emsp;&emsp;其优点是把`Metastore`服务独立出来，可以安装到远程的服务器集群里，从而解耦`Hive`服务和`Metastore`服务，保证`Hive`的稳定运行。

### 6.3.4 HQL的执行流程

&emsp;&emsp;`Hive`在执行一条`HQL`语句时，会经过以下步骤：

1. 语法解析：`Antlr`定义`SQL`的语法规则，完成`SQL`词法，语法解析，将`SQL`转化为抽象语法树`AST Tree`；
2. 语义解析：遍历`AST Tree`，抽象出查询的基本组成单元`QueryBlock`；
3. 生成逻辑执行计划：遍历`QueryBlock`，翻译为执行操作树`OperatorTree`；
4. 优化逻辑执行计划：逻辑层优化器进行`OperatorTree`变换，合并不必要的`ReduceSinkOperator`，减少`shuffle`数据量；
5. 生成物理执行计划：遍历`OperatorTree`，翻译为`MapReduce`任务；
6. 优化物理执行计划：物理层优化器进行`MapReduce`任务的变换，生成最终的执行计划。

> 关于 Hive SQL 的详细工作原理可以参考美团技术团队的文章：[HiveQL编译过程](https://tech.meituan.com/2014/02/12/hive-sql-to-mapreduce.html)

## 6.4 Hive编程实战

### 6.4.1 实验一：Hive的安装部署和管理

#### 6.4.1.1 实验准备

**实验环境：**Linux Ubuntu 20.04  
**前提条件：**  

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.0.0的单点部署（详见第2章安装单机版Hadoop）

#### 6.4.1.2 实验内容

&emsp;&emsp;基于上述前提条件，学习并掌握Hive的安装部署和管理。

✅**官网参考教程**：[GettingStarted](https://cwiki.apache.org/confluence/display/Hive/GettingStarted)

#### 6.4.1.3 实验步骤

##### 1.解压安装包

&emsp;&emsp;通过官网下载地址（✅**官网下载地址**：[Hive下载](https://dlcdn.apache.org/hive/)），下载hive 2.3.9的安装包到本地指定目录，如`/data/hadoop/`下。解压安装包至`/opt`目录下，命令如下：
```shell
sudo tar -zxvf /data/hadoop/apache-hive-2.3.9-bin.tar.gz -C /opt/
```

&emsp;&emsp;解压后，在`/opt`目录下会产生`apache-hive-2.3.9-bin`文件夹。

##### 2.更改文件夹名和所属用户

&emsp;&emsp;使用`mv`命令，将文件名改为`hive`，命令如下：  
```shell
sudo mv /opt/apache-hive-2.3.9-bin/ /opt/hive
```

&emsp;&emsp;使用`chown`命令，更改文件夹及其下级的所有文件的所属用户和用户组，将其改为`datawhale`用户和`datawhale`用户组，命令如下：  
```shell
sudo chown -R datawhale:datawhale /opt/hive/
```

##### 3.设置HIVE_HOME环境变量

&emsp;&emsp;将`HIVE_HOME`环境变量设置为`/opt/hive`，作为工作目录，打开系统环境变量配置文件，命令如下：  
```shell
sudo vim /etc/profile
```

&emsp;&emsp;在文件末尾，添加如下内容：  
```shell
# hive
export HIVE_HOME=/opt/hive
export PATH=$PATH:$HIVE_HOME/bin
```

&emsp;&emsp;使用`Shift+:`，输入`wq`后回车，保存退出。运行下面命令使环境变量生效：
```shell
source /etc/profile
```

##### 4.安装MySQL

&emsp;&emsp;在Ubuntu 20.04版本中，源仓库中`MySQL`的默认版本已经更新到8.0，因此可以直接安装，命令如下：  
```shell
sudo apt-get update  #更新软件源
sudo apt-get install mysql-server  #安装mysql
```

&emsp;&emsp;默认情况下，MySQL是已经启动的，可以通过`netstat -tap|grep mysql`或`systemctl status mysql`命令查看（下面给出开启，关闭，重启命令），具体命令如下：  
```shell
sudo netstat -tap | grep mysql    #mysql节点处于LISTEN状态表示启动成功
sudo service mysql start    #开启
sudo service mysql stop     #关闭
sudo service mysql restart  #重启
```

&emsp;&emsp;执行结果如下：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex1.1.png)

**注意**：安装时没有提示输入root账户密码，默认是空，可以执行以下命令设置密码为`123456`：  

```shell
sudo mysql -u root -p  #密码按Enter即可进入mysql shell，空格也可以，普通用户一定sudo
```

##### 5.创建MySQL hive用户

&emsp;&emsp;登录mysql shell界面，请先确认已经启动，命令如下：  
```shell
mysql -u root -p
```

&emsp;&emsp;创建`datawhale`用户，密码是`123456`，必须与`hive-site.xml`配置的`user`、`password`相同，并赋予权限，命令如下：
```sql
create user 'datawhale'@'localhost' identified by '123456'; -- 创建用户
grant all on *.* to 'datawhale'@'localhost'; -- 将所有数据库的所有表的所有权限赋给datawhale
flush privileges;  -- 刷新mysql系统权限关系表
```

##### 6.下载安装MySQL JDBC

✅**官网下载地址**：[MySQL JDBC下载](https://dev.mysql.com/downloads/connector/j/)

&emsp;&emsp;选择合适的系统以及系统版本，会自动出现最新的安装包，注意下载的是`deb`格式的，可以使用`cpkg`命令安装。这里选择`Ubuntu Linux 20.04`版本的`Connector/J 8.0.27`。  

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex1.2.png" style="zoom: 33%;" /></center>

&emsp;&emsp;下载`MySQL JDBC`到本地的目录（如`~/Download`目录）下，并使用`cpkg`命令安装，命令如下：

```shell
cd ~/Download  #切换到你的文件所在目录下
sudo dpkg -i mysql-connector-java_8.0.27-1ubuntu20.04_all.deb  #安装mysql-connector-java
```

##### 7.导入MySQL JDBC jar包到`hive/lib`目录下

&emsp;&emsp;使用`cp`命令，将`jar`包到`/opt/hive/lib`目录下，命令如下：  
```shell
sudo cp /usr/share/java/mysql-connector-java-8.0.27.jar /opt/hive/lib/
```

> **注意**：
>
> &emsp;&emsp;你可能不知道安装到哪里了，别急，在`/usr/share/java/`下面，会存在该`jar`包。  
> &emsp;&emsp;验证路径的方法：打开`deb`文件，提取文件，看到`.tar.xz`文件，使用`xz -d`命令解压，并使用`tar -xvf`解包，解压出来的文件目录路径就是在系统中的路径。

&emsp;&emsp;使用`chown`命令，更改`jar`包的所属用户和用户组，将其改为`datawhale`用户和`datawhale`用户组，命令如下：  
```shell
sudo chown datawhale:datawhale /opt/hive/lib/mysql-connector-8.0.27.jar
```

##### 8.修改hive配置文件

&emsp;&emsp;进入`/opt/hive/conf`目录下，将`hive-default.xml.template`文件重命名为`hive-default.xml`，命令如下：  
```shell
cd /opt/hive/conf
sudo mv hive-default.xml.template hive-default.xml
```

&emsp;&emsp;在当前目录（`/opt/hive/conf`）下，创建`hive-site.xml`文件，命令如下：  
```shell
sudo touch hive-site.xml
```

&emsp;&emsp;使用`vim`命令，打开`hive-site.xml`文件，命令如下：  
```shell
sudo vim hive-site.xml
```

&emsp;&emsp;添加内容如下：  
```html
<configuration>
    <property>
        <name>javax.jdo.option.ConnectionURL</name>
        <value>jdbc:mysql://localhost:3306/hive_metadata?createDatabaseIfNotExist=true</value>
        <description>JDBC connect string for a JDBC Metastore</description>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionDriverName</name>
        <value>com.mysql.cj.jdbc.Driver</value>
        <description>Driver class name for a JDBC Metastore</description>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionUserName</name>
        <value>datawhale</value>
        <description>username to use against Metastore database</description>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionPassword</name>
        <value>123456</value>
        <description>password to use against Metastore database</description>
    </property>
</configuration>
```

&emsp;&emsp;至此，`Hive`的配置已经完成了。

##### 9.启动MySQL

&emsp;&emsp;使用`service`命令，启动`MySQL`，命令如下：  
```shell
sudo service mysql start
```

&emsp;&emsp;使用`systemctl`命令，查看`MySQL`是否正常启动，命令如下：  
```shell
systemctl status mysql
```

&emsp;&emsp;执行结果如下：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex1.1.png)

##### 10.指定元数据数据库类型并初始化Schema

&emsp;&emsp;使用`schematool`命令，初始化`Hive`在`MySQL`上的`Schema`，命令如下：  
```shell
schematool -initSchema -dbType mysql
```

&emsp;&emsp;初始化成功后，执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex1.3.png)

&emsp;&emsp;如果运行此步时报错，`schematool:未找到命令...`，需要重新`source`一下全局变量：

```shell
source /etc/profile
```


##### 8.启动Hadoop

&emsp;&emsp;进入/opt/hadoop/bin目录，启动`Hadoop`，命令如下：  
```shell
cd /opt/hadoop/sbin
./start-all.sh
```

&emsp;&emsp;使用`jps`命令检验hadoop是否启动成功，如果6个进程都启动，表示启动成功，执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex1.4.png)

##### 9.启动Hive

&emsp;&emsp;执行`hive`命令，启动`Hive`，执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex1.5.png)

##### 10.检验Hive是否成功部署

&emsp;&emsp;在`hive shell`命令行下，执行`show databases;`命令，显示已有的数据库，执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex1.6.png)

&emsp;&emsp;至此，`Hive`安装部署完成，本次实验结束啦！

### 6.4.2 实验二：Hive常用的DDL操作

#### 6.4.2.1 实验准备

**实验环境：**Linux Ubuntu 20.04  
**前提条件：**  

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.0.0的单点部署，并**正常启动**（详见第2章安装单机版Hadoop）
3. MySQL数据库安装完成，并**正常启动**（详见实验一）
4. Hive单点部署完成，并**正常启动**（详见实验一）

#### 6.4.2.2 实验内容

&emsp;&emsp;基于上述前提条件， 在`hive shell`命令行下，完成一些常见的`DDL`操作。（✅**官方参考内容**：[LanguageManual DDL](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL)）

#### 6.4.2.3 实验步骤

&emsp;&emsp;正常启动`hive`之后，可进入`hive shell`命令行，以下所有命令将在该环境下执行。

##### 1.数据库操作

###### 1.1 查看数据列表

&emsp;&emsp;使用如下命令，查看已有数据库：  
```sql
show databases;
```

&emsp;&emsp;执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.1.png)

###### 1.2 使用数据库

&emsp;&emsp;使用`use`命令，指定要使用的数据库，命令格式如下：  
```sql
use <database_name>;
```

&emsp;&emsp;使用`datawhale`数据库，执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.2.png)

###### 1.3 新建数据库

&emsp;&emsp;使用`create database`命令，新建数据库，命令格式如下：  
```sql
CREATE (DATABASE|SCHEMA) [IF NOT EXISTS] database_name   -- DATABASE|SCHEMA 是等价的
  [COMMENT database_comment] -- 数据库注释
  [LOCATION hdfs_path] -- 存储在HDFS上的位置
  [WITH DBPROPERTIES (property_name=property_value, ...)]; -- 指定额外属性
```

&emsp;&emsp;创建`hive_test`数据库，命令如下：  
```sql
CREATE DATABASE IF NOT EXISTS hive_test
  COMMENT 'hive database for test'
  WITH DBPROPERTIES ('create'='datawhale');
```

&emsp;&emsp;执行结果如下：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.3.png)

###### 1.4 查看数据库信息

&emsp;&emsp;使用`desc database`命令，查看数据库信息，命令格式如下：  
```sql
DESC DATABASE [EXTENDED] db_name; -- EXTENDED 表示是否显示额外属性
```

&emsp;&emsp;查看`hive_test`数据库信息，命令如下：  
```sql
DESC DATABASE EXTENDED hive_test;
```

&emsp;&emsp;执行结果如下：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.4.png)

###### 1.5 删除数据库

&emsp;&emsp;使用`drop database`命令，删除数据库，命令格式如下：  
```sql
DROP (DATABASE|SCHEMA) [IF EXISTS] database_name [RESTRICT|CASCADE];
```
**注**：默认行为是`RESTRICT`，如果数据库中存在该表，则删除失败。要想删除库及其中的表，可以使用`CASCADE`级联删除。

&emsp;&emsp;删除`hive_test`数据库，命令如下：  
```sql
DROP DATABASE IF EXISTS hive_test CASCADE;
```

&emsp;&emsp;执行结果如下：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.5.png)

##### 2.创建表

###### 2.1 建表语法

&emsp;&emsp;使用`create table`命令，创建表，命令格式如下：  
```sql
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name     -- 表名
  [(col_name data_type [COMMENT col_comment],
    ... [constraint_specification])]  -- 列名 列数据类型
  [COMMENT table_comment]   -- 表描述
  [PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)]  -- 分区表分区规则
  [
    CLUSTERED BY (col_name, col_name, ...) 
   [SORTED BY (col_name [ASC|DESC], ...)] INTO num_buckets BUCKETS
  ]  -- 分桶表分桶规则
  [SKEWED BY (col_name, col_name, ...) ON ((col_value, col_value, ...), (col_value, col_value, ...), ...)  
   [STORED AS DIRECTORIES] 
  ]  -- 指定倾斜列和值
  [
   [ROW FORMAT row_format]    
   [STORED AS file_format]
     | STORED BY 'storage.handler.class.name' [WITH SERDEPROPERTIES (...)]  
  ]  -- 指定行分隔符、存储文件格式或采用自定义存储格式
  [LOCATION hdfs_path]  -- 指定表的存储位置
  [TBLPROPERTIES (property_name=property_value, ...)]  -- 指定表的属性
  [AS select_statement];   -- 从查询结果创建表
```

###### 2.2 内部表

&emsp;&emsp;使用以下雇员表`emp`的字段信息，在`Hive`中创建内部表：  

| 字段名称 | 字段类型 | 说明 |
| :---: | :---: | :---: |
| empno | INT | 员工编号 |
| ename | STRING | 员工姓名 |
| job | STRING | 员工工作 |
| mgr | INT | 领导编号 |
| hiredate | TIMESTAMP | 入职日期 |
| sal | DECIMAL(7,2) | 月薪 |
| comm | DECIMAL(7,2) | 奖金 |
| deptno | INT | 部门编号 |

&emsp;&emsp;使用`create table`创建`emp`内部表，命令如下：  
```sql
CREATE TABLE emp(
  empno INT,
  empname STRING,
  job STRING,
  mgr INT,
  hiredate TIMESTAMP,
  sal DECIMAL(7,2),
  comm DECIMAL(7,2),
  deptno INT)
  ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";
```

&emsp;&emsp;执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.6.png)

&emsp;&emsp;hdfs文件系统中的存储位置如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.7.png)

###### 2.3 外部表

&emsp;&emsp;使用`create external table`创建`emp_external`外部表，命令如下：  
```sql
CREATE EXTERNAL TABLE emp_external(
  empno INT,
  ename STRING,
  job STRING,
  mgr INT,
  hiredate TIMESTAMP,
  sal DECIMAL(7,2),
  comm DECIMAL(7,2),
  deptno INT)
  ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t"
  LOCATION '/datawhale/emp_external';
```

&emsp;&emsp;使用 `desc emp_external` 命令，查看`emp_external`表的详细信息，执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.8.png)

&emsp;&emsp;hdfs文件系统中的存储位置如下所示：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.9.png)

###### 2.4 分区表

&emsp;&emsp;使用 `partitioned`语句，创建`emp_partition`分区表，命令如下：  
```sql
CREATE EXTERNAL TABLE emp_partition(
  empno INT,
  ename STRING,
  job STRING,
  mgr INT,
  hiredate TIMESTAMP,
  sal DECIMAL(7,2),
  comm DECIMAL(7,2)
  )
  PARTITIONED BY (deptno INT)   -- 按照部门编号进行分区
  ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t"
  LOCATION '/datawhale/emp_partition';
```

&emsp;&emsp;hdfs文件系统中的存储位置如下所示：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.10.png)

###### 2.5 分桶表

&emsp;&emsp;使用`clustered sorted into`语句，创建`emp_bucket`分桶表，命令如下：  
```sql
CREATE EXTERNAL TABLE emp_bucket(
  empno INT,
  ename STRING,
  job STRING,
  mgr INT,
  hiredate TIMESTAMP,
  sal DECIMAL(7,2),
  comm DECIMAL(7,2),
  deptno INT)
  CLUSTERED BY(empno) SORTED BY(empno ASC) INTO 4 BUCKETS  -- 按照员工编号散列到四个 bucket 中
  ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t"
  LOCATION '/datawhale/emp_bucket';
```

&emsp;&emsp;hdfs文件系统中的存储位置如下所示：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.10.png)

###### 2.6 倾斜表

&emsp;&emsp;通过指定一个或者多个列经常出现的值（严重偏斜），`Hive`会自动将涉及到这些值的数据拆分为单独的文件。在查询时，如果涉及到倾斜值，它就直接从独立文件中获取数据，而不是扫描所有文件，这使得查询性能得到提升。  
&emsp;&emsp;使用`skewed`语句，创建`emp_skewed`倾斜表，命令如下：  
```sql
CREATE EXTERNAL TABLE emp_skewed(
  empno INT,
  ename STRING,
  job STRING,
  mgr INT,
  hiredate TIMESTAMP,
  sal DECIMAL(7,2),
  comm DECIMAL(7,2)
  )
  SKEWED BY (empno) ON (66,88,100)  -- 指定 empno 的倾斜值 66,88,100
  ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t"
  LOCATION '/datawhale/emp_skewed';   
```

&emsp;&emsp;hdfs文件系统中的存储位置如下所示：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.10.png)

###### 2.7 临时表

&emsp;&emsp;临时表仅对当前`session`可见，临时表的数据将存储在用户的暂存目录中，并在会话结束后删除。如果临时表与永久表表名相同，则对该表名的任何引用都将解析为临时表，而不是永久表。临时表还具有以下两个限制：

- 不支持分区列；
- 不支持创建索引。

&emsp;&emsp;使用`create temporary table`命令，创建`emp_temp`临时表，命令如下：  
```sql
CREATE TEMPORARY TABLE emp_temp(
  empno INT,
  ename STRING,
  job STRING,
  mgr INT,
  hiredate TIMESTAMP,
  sal DECIMAL(7,2),
  comm DECIMAL(7,2)
  )
  ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t";
```

###### 2.8 CTAS创建表

&emsp;&emsp;使用`create table as select`语句形式，从查询语句的结果中创建表：  
```sql
CREATE TABLE emp_copy AS SELECT * FROM emp WHERE deptno='20';
```

&emsp;&emsp;执行命令如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.11.png)

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.12.png)

&emsp;&emsp;hdfs文件系统中的存储位置如下所示：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.13.png)

###### 2.9 复制表结构

&emsp;&emsp;使用`create like`语句形式，复制一个表的表结构，命令格式如下：  
```sql
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name  -- 创建表表名
   LIKE existing_table_or_view_name  -- 被复制表的表名
   [LOCATION hdfs_path]; -- 存储位置
```

&emsp;&emsp;通过复制`emp`表，创建`emp_co`表，命令如下：  
```sql
CREATE TEMPORARY EXTERNAL TABLE IF NOT EXISTS emp_co LIKE emp
```

&emsp;&emsp;执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.14.png)

> **注**：临时表不存储在hdfs中。

###### 2.10 加载数据到表

&emsp;&emsp;加载数据到表中属于`DML`操作，这里为了方便大家测试，先简单介绍一下加载本地数据到表中的命令，命令如下：  
```sql
-- 加载数据到 emp 表中
load data local inpath "/home/datawhale/emp.txt" into table emp;
```

&emsp;&emsp;其中`emp.txt`的内容在本仓库的[resources](https://github.com/shenhao-stu/Big-Data/tree/master/resources) 目录下，具体内容如下：  
```
7369	SMITH	CLERK	7902	1980-12-17 00:00:00	800.00		20
7499	ALLEN	SALESMAN	7698	1981-02-20 00:00:00	1600.00	300.00	30
7521	WARD	SALESMAN	7698	1981-02-22 00:00:00	1250.00	500.00	30
7566	JONES	MANAGER	7839	1981-04-02 00:00:00	2975.00		20
7654	MARTIN	SALESMAN	7698	1981-09-28 00:00:00	1250.00	1400.00	30
7698	BLAKE	MANAGER	7839	1981-05-01 00:00:00	2850.00		30
7782	CLARK	MANAGER	7839	1981-06-09 00:00:00	2450.00		10
7788	SCOTT	ANALYST	7566	1987-04-19 00:00:00	1500.00		20
7839	KING	PRESIDENT		1981-11-17 00:00:00	5000.00		10
7844	TURNER	SALESMAN	7698	1981-09-08 00:00:00	1500.00	0.00	30
7876	ADAMS	CLERK	7788	1987-05-23 00:00:00	1100.00		20
7900	JAMES	CLERK	7698	1981-12-03 00:00:00	950.00		30
7902	FORD	ANALYST	7566	1981-12-03 00:00:00	3000.00		20
7934	MILLER	CLERK	7782	1982-01-23 00:00:00	1300.00		10
```

&emsp;&emsp;加载后可使用`select * from emp`查询该表的数据，执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.15.png)

&emsp;&emsp;如果使用分区表加载数据，需要增加字段`partition(deptno=30)`，或者可以修改`hive`的默认配置配置为动态分区，可以**参考**[Hive数仓：操作分区表](https://github.com/shenhao-stu/Big-Data/tree/master/experiments/Hive数仓：操作分区表.md)。  
&emsp;&emsp;使用分区表加载`emp.txt`数据，命令如下：  
```sql
load data local inpath "/home/datawhale/emp.txt" into table emp_partition partition(deptno=30);
```

&emsp;&emsp;hdfs文件系统中的存储位置如下所示：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.16.png)

##### 3.修改表

###### 3.1 重命名表

&emsp;&emsp;使用`alter table rename`语句，对表进行重命名，命令格式如下：  
```sql
ALTER TABLE table_name RENAME TO new_table_name;
```

&emsp;&emsp;将`emp_temp`表重命名为`new_emp`表，命令如下：  
```sql
ALTER TABLE emp_temp RENAME TO new_emp;
```

&emsp;&emsp;执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.17.png)

###### 3.2 修改列

&emsp;&emsp;使用`alter table change column`语句，修改列的属性，命令格式如下：  
```sql
ALTER TABLE table_name [PARTITION partition_spec] CHANGE [COLUMN] col_old_name col_new_name column_type
  [COMMENT col_comment] [FIRST|AFTER column_name] [CASCADE|RESTRICT];
```

&emsp;&emsp;修改`new_emp`表中的`empno`、`sal`、`mgr`字段属性，命令分别如下：
```sql
-- 修改字段名和类型
ALTER TABLE new_emp CHANGE empno empno_new INT;

-- 修改字段 sal 的名称 并将其放置到 empno 字段后
ALTER TABLE new_emp CHANGE sal sal_new decimal(7,2) AFTER ename;

-- 为字段增加注释
ALTER TABLE new_emp CHANGE mgr mgr_new INT COMMENT 'this is column mgr';
```

###### 3.3 新增列

&emsp;&emsp;使用`alter table add columns`语句形式，在`new_emp`表中新增`address`列，命令如下：
```sql
ALTER TABLE new_emp ADD COLUMNS (address STRING COMMENT 'home address');
```

##### 4.清空表/删除表

###### 4.1 清空表

&emsp;&emsp;使用`truncate table`命令，清空整个表或表指定分区中的数据，命令格式如下：  
```sql
-- 清空整个表或表指定分区中的数据
TRUNCATE TABLE table_name [PARTITION (partition_column = partition_col_value,  ...)];
```

&emsp;&emsp;目前只有内部表才能执行`TRUNCATE`操作，外部表执行时会抛出异常`Cannot truncate non-managed table`。

&emsp;&emsp;清空`emp_partition`分区表，命令如下：  
```sql
TRUNCATE TABLE emp_partition PARTITION (deptno=30);
```

###### 4.2 删除表

&emsp;&emsp;使用`drop table`命令，删除表，命令格式如下：  
```sql
DROP TABLE [IF EXISTS] table_name [PURGE]; 
```

**注**：  
- 内部表：不仅会删除表的元数据，同时会删除`HDFS`上的数据；
- 外部表：只会删除表的元数据，不会删除`HDFS`上的数据；
- 删除视图引用的表时，不会给出警告（但视图已经无效了，必须由用户删除或重新创建）。

##### 5.其他命令

###### 5.1 describe

&emsp;&emsp;使用`describe`命令，查看数据库属性，命令格式如下：  
```sql
DESCRIBE|Desc DATABASE [EXTENDED] db_name;  -- EXTENDED 是否显示额外属性
```

&emsp;&emsp;查看`datawhale`库的属性，执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.18.png)


&emsp;&emsp;也可用于查看表的属性，命令格式如下：
```sql
DESCRIBE|Desc [EXTENDED|FORMATTED] table_name -- FORMATTED 以友好的展现方式查看表详情
```

&emsp;&emsp;查看`emp`表的属性，命令如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.19.png)

###### 5.2 show

1. **查看数据库列表**  

```sql
-- 语法
SHOW (DATABASES|SCHEMAS) [LIKE 'identifier_with_wildcards'];
```

&emsp;&emsp;以列表形式展示符合`datawhale*`规则的所有数据库，命令如下：  
```sql
SHOW DATABASES like 'datawhale*';
```

&emsp;&emsp;`LIKE`子句允许使用正则表达式进行过滤，但是`SHOW`语句当中的`LIKE`子句只支持 `*`（通配符）和 `|`（条件或）两个符号。例如 `employees`，`emp *`，`emp * | * ees`，所有这些都将匹配名为`employees`的数据库。

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.20.png)

2. **查看表的列表**  

&emsp;&emsp;使用`show tables`命令，查看数据库下的所有表，命令格式如下：  
```sql
-- 语法
SHOW TABLES [IN database_name] ['identifier_with_wildcards'];
```

&emsp;&emsp;展示`datawhale`库下的所有表，命令如下：
```sql
SHOW TABLES IN 'datawhale';
```

&emsp;&emsp;执行结果如下：  

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6_ex2.21.png)

3. **查看视图列表**  

&emsp;&emsp;使用`show views`命令，查看数据库下的所有视图，命令格式如下：  
```sql
SHOW VIEWS [IN/FROM database_name] [LIKE 'pattern_with_wildcards'];  -- 仅支持 Hive 2.2.0 +
```

4. **查看表的分区列表**

&emsp;&emsp;使用`show partitions`命令，查看表的所有分区表，命令格式如下：  
```sql
SHOW PARTITIONS table_name;
```

5. **查看表/视图的创建语句**

&emsp;&emsp;使用`show create table`命令，查看表/视图的创建语句，命令格式如下：  
```sql
SHOW CREATE TABLE ([db_name.]table_name|view_name);
```

## 6.5 本章小结

&emsp;&emsp;在本章的学习中，主要介绍了数据仓库和`Hive`的基本概念，并通过一个小示例，模拟实现`Hive`；还介绍了`Hive`的核心概念，主要包括7大类的`Hive`的数据类型和4个数据模型；通过讲解`Hive`的系统结构，结合之前学习过的`MapReduce`，介绍了`HQL`语句的执行流程；最后通过两个实验，分别介绍了`Hive`的安装和常用的DDL操作。

> ps：多用脑，多思考，这一章内容很干，希望大家足够肝。  
> 保护眼睛，保护头发，好好学习，天天向上

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.5.png" style="zoom:80%;" /></center>