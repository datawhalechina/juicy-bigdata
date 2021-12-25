# Chapter6 数据仓库Hive

> 王嘉鹏，shenhao

## 6.0 数据仓库

&emsp;&emsp;Hive是一个基于Hadoop的**数据仓库**工具，可以对存储在 Hadoop 文件中的数据集进行**数据整理、特殊查询和分析处理**。具体来说，它可以将结构化的数据文件映射成表，并提供类似于关系数据库 SQL 的查询语言—— **HiveQL** 。当采用 MapReduce 作为执行引擎时，Hive 自身可以将用于查询的 HiveQL 语句转换为 MapReduce 作业，然后提交到 Hadoop 上运行。

&emsp;&emsp;首先，我们先简单的引入一下数据仓库的概念！！

> ps：到了数据仓库啦，崭新的饱满的和知识相濡以沫的一天，又开始啦！！！！

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.0.png)

### 6.0.1 为什么要有数据仓库

&emsp;&emsp;在引入数据仓库之前，我们先来聊聊为什么会产生数据仓库呢！！

<img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.0.1.png" style="zoom:33%;" />

&emsp;&emsp;数据的作用有两个：操作型记录的保存和分析型决策的制定。
- 操作型记录的保存意味着企业通常不必维护历史数据，只需修改数据以反映最新的状态；
- 分析型决策意味着企业需要保存历史的数据，从而可以更精确的来评估现有状况进行决策。

&emsp;&emsp;基于后者分析型决策的优化，需要高性能地完成用户的查询，因此引出了数据仓库的概念。

### 6.0.2 数据仓库概念

&emsp;&emsp;数据仓库是一个**面向主题的**、**集成的**、**非易失的**、**随时间变化的**，用来**支持管理人员决策**的数据集合，数据仓库中包含了粒度化的企业数据。

&emsp;&emsp;随着信息技术的普及和企业信息化建设步伐的加快，企业逐步认识到建立企业范围内的统一数据存储的重要性，越来越多的企业已经建立或正在着手建立企业数据仓库。企业数据仓库有效集成了来自不同部门、不同地理位置、具有不同格式的数据，为企业管理决策者提供了企业范围内的单一数据视图，从而为综合分析和科学决策奠定了坚实的基础。

&emsp;&emsp;如下图所示，数据仓库的主要特征是：**主题性**、**集成性**、**非易失性**、**时变性**。

<img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.0.2_1.png" style="zoom:33%;" />

1. 主题性  
    &emsp;&emsp;各个业务系统的数据可能是相互分离的，但数据仓库则是**面向主题的**。数据仓库将不同的业务进行归类并分析，将数据抽象为主题，用于对应某一分析领域所涉及的分析对象。  
    &emsp;&emsp;而操作型记录（即传统数据）对数据的划分并不适用于决策分析。在数据仓库中，基于主题的数据被划分为各自独立的领域，每个领域有各自的逻辑内涵但互不交叉，在抽象层次上对数据进行完整的、一致的和准确的描述。  
    &emsp;&emsp;以零售业务的过程为例：将多个零售业务数据（杂货、冷冻食品、生活用品、肉类等），依据业务主题进行数据划分，可创建一个具有订单、库存和销售等多个业务领域的零售业务数仓。  
    
    <img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.0.2_2.png" style="zoom:50%;" />
    
2. 集成性  
    &emsp;&emsp;确定主题之后，就需要获取与主题相关的数据。这些数据会分布在不同的业务过程中，因此在数据进入数仓之前，需要对这些数据的口径进行统一。  
    &emsp;&emsp;口径统一是指，统一数据来源中的歧义、单位、字长等元素，并进行总和计算，来聚合成新的数据。  
    &emsp;&emsp;以上述零售业务过程中的订单主题为例，对于订单主题，通常会包括三个业务过程：订单、发货和发票。这些过程会产生一些新的指标，如：销售额、发票收入等。  
   
    <img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.0.2_3.png"  />
    
3. 非易失性  
    &emsp;&emsp;数据仓库的目的是分析数据中的规律，因此，添加到数据仓库中的数据，需要保证其稳定，不会轻易丢失和改变。  
    &emsp;&emsp;这里，与传统操作型数据库的区别在于：操作型数据库主要服务于日常的业务操作，产生的数据会实时更新到数据库中，以便业务应用能够迅速获得当前最新数据，不至于影响正常的业务运作。而数据仓库通常是保存历史业务数据，根据业务需要每隔一段时间将一批新的数据导入数据仓库。  

4. 时变性  
    &emsp;&emsp;数据仓库是根据业务需要来建立的，代表了一个业务过程。因此数据仓库分析的结果只能反映过去的业务情况，当业务变化后，数据仓库需要跟随业务的变化而改变，以适应分析决策的需要。  

### 6.0.3 数据仓库的体系结构

&emsp;&emsp;数据仓库的体系结构通常包含4个层次：数据源、数据存储和管理、数据服务以及数据应用。

<img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.0.3.png" style="zoom:33%;" />

- 数据源：数据仓库的数据来源，包括外部数据、现有业务系统和文档资料等。
- 数据存储和管理：为数据提供的存储和管理，包括数据仓库、数据集市、数据仓库监视、运行于维护工具和元数据管理等。
- 数据服务：为前端工具和应用提供数据服务，包括直接从数据仓库中获取数据供前端使用，或者通过 OLAP 服务器为前端应用提供更为复杂的数据服务。
- 数据应用：直接面向最终用户，包括数据工具、自由报表工具、数据分析工具、数据挖掘工具和各类应用系统。

### 6.0.4 面临的挑战

&emsp;&emsp;随着大数据时代的全面到来，传统数据仓库也面临了如下几方面的挑战：

- 无法满足快速增长的海量数据存储需求
- 无法有效处理不同类型的数据
- 计算和处理能力不足

## 6.1 Hive 基本概念
<img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.1.png" style="zoom:33%;" />

### 6.1.1 概述

&emsp;&emsp;**Hive是建立在Hadoop之上的一种数仓工具**。该工具的功能是将**结构化**、**半结构化**的数据文件映射为一张**数据库表**，基于数据库表，提供了一种类似`SQL`的查询模型（`HQL`），用于访问和分析存储在`Hadoop`文件中的大型数据集。  
&emsp;&emsp;`Hive`本身并不具备存储功能，其核心是将`HQL`转换为`MapReduce`程序，然后将程序提交到`Hadoop`集群中执行。

<img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.1.1.png" style="zoom: 50%;" />

&emsp;&emsp;**特点**：

1. 简单、容易上手 (提供了类似 SQL 的查询语言 HiveQL) ，使得精通 SQL 但是不了解 Java 编程的人也能很好地进行大数据分析；
2. 灵活性高，可以自定义用户函数 (UDF) 和存储格式；
3. 为超大的数据集设计的计算和存储能力，集群扩展容易;
4. 统一的元数据管理，可与 presto／impala／sparksql 等共享数据；
5. 执行延迟高，不适合做数据的实时处理，但适合做海量数据的离线处理。

### 6.1.2 产生背景

<img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.1.2.png" style="zoom: 50%;" />

&emsp;&emsp;`Hive`的产生背景主要有两个：  

- **使用成本高**：使用`MapReduce`直接处理数据时，需要掌握`Java`等编程语言，学习成本较高，而且使用`MapReduce`不容易实现复杂查询；
- **建立分析型数仓的需求**：`Hive`支持类`SQL`的查询以及支持自定义函数，可以作为数据仓库的工具。

&emsp;&emsp;`Hive`利用`HDFS`存储数据，使用`MapReduce`查询分析数据。将`SQL`转换为`MapReduce`程序，从而完成对数据的分析决策。

<center><img src="D:/%E4%B8%8A%E8%B4%A2Courses/2020_%E5%A4%A7%E4%B8%89/Big-Data/doc_imgs/ch6.1.2_emoji.png" style="zoom:80%;" /></center>

### 6.1.3 Hive 与 Hadoop 生态系统

&emsp;&emsp;下图描述了当采用 MapReduce 作为执行引擎时，Hive 与 Hadoop 生态系统中其他组件的关系。

<img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.1.3.png" alt="image-20211225161347381" style="zoom:33%;" />

&emsp;&emsp;HDFS 作为高可靠的底层存储方式，可以存储海量数据。MapReduce 对这些海量数据进行批处理，实现高性能计算。Hive 架构在  MapReduce 、 HDFS 之上，其自身并不存储和处理数据，而是分别借助于 HDFS 和 MapReduce 实现数据的存储和处理，用 HiveQL 语句编写的处理逻辑，最终都要转换成 MapReduce 任务来运行。Pig 可以作为 Hive 的替代工具，它是一种数据流语言和运行环境，适用于在 Hadoop 平台上查询半结构化数据集，常用于 ETL 过程的部分，即将外部数据装载到 Hadoop 集群中，然后转换为用户需要的数据格式。HBase 是一个面向列的、分布式的、可伸缩的数据库，它可以提供数据的实时访问功能，而 Hive 只能处理静态数据，主要是 BI 报表数据。就设计初衷而言，在 Hadoop 上设计 Hive，是为了减少复杂 MapReduce 应用程序的编写工作，在 Hadoop 上设计 HBase 则是为了实现对数据的实时访问，所以，HBase 与 Hive 的功能是互补的，它实现了 Hive 不能提供的功能。

### 6.1.3 Hive 与传统数据库的对比分析

&emsp;&emsp;Hive 在很多方面和传统数据库类似，但是，它的底层依赖的是 HDFS 和 MapReduce （或Tez、Spark），所以，在很多方面又有别于传统数据。以下将从各个方面，对 Hive 和传统数据库进行对比分析。

| 对比内容 |         Hive          |   传统数据库   |
| :------: | :-------------------: | :------------: |
| 数据存储 |         HDFS          |  本地文件系统  |
|   索引   |     支持有限索引      |  支持复杂索引  |
|   分区   |         支持          |      支持      |
| 执行引擎 | MapReduce、Tez、Spark | 自身的执行引擎 |
| 执行延迟 |          高           |       低       |
|  扩展性  |          好           |      有限      |
| 数据规模 |          大           |       小       |


> ps：看完了Hive的特点后，一定很好奇这东西的内部构造是啥吧，小伙伴们，请跟我来
> 坚持学习，沉迷学习，忘我学习，冲冲冲！！！
### 6.1.4 模拟实现Hive

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

<img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.1.4.png" style="zoom:50%;" />

&emsp;&emsp;要实现上图所示的文件和表的对应关系，关键在于**实现表和文件的映射**，那么需要记录的信息包括：  
- 表是对应于哪个文件的，即表的位置信息；
- 表的列是对应文件的哪一个字段，即字段的位置信息；
- 文件字段之间的分隔符是什么，即内容读取时的分隔操作；

&emsp;&emsp;完成了表和文件的映射后，`Hive`需要对用户编写的`SQL`语句进行语法校验，并且根据记录的元数据信息对`SQL`进行解析，制定执行计划，并将执行计划转化为`MapReduce`程序来执行，最终将执行的结果封装返回给用户。  
&emsp;&emsp;接下来，在`Hive`的核心概念中，我们进一步了解一下表和文件的映射信息。

## 6.2 Hive 核心概念

### 6.2.1 元数据

- **metadata**  
&emsp;&emsp;上面所介绍的`Hive`表和文件的映射信息，被称为**元数据**。元数据表示**描述数据的数据**，对于`Hive`来说，元数据就是用来描述`HDFS`文件和表的各种对应关系（位置关系、顺序关系、分隔符）。`Hive`的元数据存储在**关系数据库**中（`Hive`内置的是`Derby`、第三方的是`MySQL`），`HDFS`中存储的是数据。

- **metastore**  
&emsp;&emsp;`metastore`是**元数据服务**：表示`Hive`操作管理访问元数据的一个服务。用于访问元数据，`metastore`对外提供一个服务地址，使客户端能够连接`Hive`。使用`metastore`的好处如下：
- 元数据把数据保存在关系数据库中，`Hive`提供元数据服务，通过对外的服务地址，用户能够使用客户端连接Hive，访问并操作元数据；
- 支持多个客户端的连接，而客户端无需关心数据的存储地址，实现了数据访问层面的解耦操作。

<img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.2.1_1.png" style="zoom: 50%;" />

- `metastore`管理元数据的方式
1. **内嵌模式**  
&emsp;&emsp;`metastore`**默认的**部署模式是`metastore`元数据服务和`Hive`服务融合在一起。

<img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.2.1_2.png" style="zoom:50%;" />

&emsp;&emsp;在这种模式下，`Hive`服务（即`Hive`驱动本身）、元数据服务`Metastore`，元数据`metadata`（用于存储映射信息）都在同一个`JVM`进程中，元数据存储在内置的**Derby数据库**。当启动`HiveServer`进程时，`Derby`和`metastore`都会启动，不需要额外启动`metastore`服务。但是，一次只能支持一个用户访问，适用于测试场景。
    
2. **本地模式**  
&emsp;&emsp;本地模式与内嵌模式的区别在于：把元数据提取出来，让`metastore`服务与`HiveServer`主进程在同一个`JVM`进程中运行，存储元数据的数据库在单独的进程中运行。元数据一般存储在`MySQL`关系型数据库中。

<img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.2.1_3.png" style="zoom:50%;" />

&emsp;&emsp;但是，每启动一个`Hive`服务，都会启动一个`metastore`服务。多个人使用时，会启用多个`metastore`服务。
    
3. **远程模式**  
&emsp;&emsp;既然可以把元数据存储给提取出来，也可以考虑把`metastore`给提取出来变为单独一个进程。把`metastore`单独进行配置，并在单独的进程中运行，可以保证全局唯一，从而保证数据访问的安全性。（即不随`Hive`的启动而启动）

<img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.2.1_4.png" style="zoom:50%;" />

&emsp;&emsp;其优点是把`metaStore`服务独立出来，可以安装到远程的服务器集群里，从而解耦`Hive`服务和`metaStore`服务，保证`Hive`的稳定运行。

### 6.2.2 Hive数据模型

&emsp;&emsp;`Hive`的数据都是存储在`HDFS`上的，默认有一个根目录，在`hive-site.xml`中可以进行配置数据的存储路径。`Hive`数据模型的含义是，描述`Hive`组织、管理和操作数据的方式。`Hive`包含如下4种数据模型：

1. **库**  
&emsp;&emsp;`MySQL`中默认数据库是`default`，用户可以创建不同的`database`，在`database`下也可以创建不同的表。`Hive`也可以分为不同的数据（仓）库，和传统数据库保持一致。在传统数仓中创建`database`。默认的数据库也是`default`。`Hive`中的库相当于关系数据库中的命名空间，它的作用是将用户和数据库的表进行隔离。  

2. **表**  
&emsp;&emsp;`Hive`中的表所对应的数据是存储在`HDFS`中，而表相关的元数据是存储在关系数据库中。Hive中的表分为内部表和外部表两种类型，两者的区别在于数据的访问和删除：  
- 内部表的加载数据和创建表的过程是分开的，在加载数据时，实际数据会被移动到数仓目录中，之后对数据的访问是在数仓目录实现。而外部表加载数据和创建表是同一个过程，对数据的访问是读取`HDFS`中的数据；
- 内部表删除时，因为数据移动到了数仓目录中，因此删除表时，表中数据和元数据会被同时删除。外部表因为数据还在`HDFS`中，删除表时并不影响数据。
- 创建表时不做任何指定，默认创建的就是内部表。想要创建外部表，则需要使用`External`进行修饰

| 对比内容     |                            内部表                            |                            外部表                            |
| ------------ | :----------------------------------------------------------: | :----------------------------------------------------------: |
| 数据存储位置 | 内部表数据存储的位置由 hive.metastore.warehouse.dir 参数指定，默认情况下表的数据存储在 HDFS 的 `/user/hive/warehouse/数据库名.db/表名/` 目录下 |     外部表数据的存储位置创建表时由 `Location` 参数指定；     |
| 导入数据     | 在导入数据到内部表，内部表将数据移动到自己的数据仓库目录下，数据的生命周期由 Hive 来进行管理 | 外部表不会将数据移动到自己的数据仓库目录下，只是在元数据中存储了数据的位置 |
| 删除表       |                 删除元数据（metadata）和文件                 |                   只删除元数据（metadata）                   |

3. **分区**  
&emsp;&emsp;分区是一个优化的手段，目的是**减少全表扫描**，提高查询效率。在`Hive`中存储的方式就是表的主目录文件夹下的子文件夹，子文件夹的名字表示所定义的分区列名字。
4. **分桶**  
&emsp;&emsp;分桶和分区的区别在于：分桶是针对数据文件本身进行拆分，根据表中字段（例如，编号ID）的值，经过`hash`计算规则，将数据文件划分成指定的若干个小文件。分桶后，`HDFS`中的数据文件会变为多个小文件。分桶的优点是**优化join查询**和**方便抽样查询**。

## 6.3 Hive 系统结构

&emsp;&emsp;Hive 主要由用户接口模块、驱动模型以及元数据存储模块3个模块组成，其系统架构如下图所示：

![](https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.3.png)



### 6.3.1 用户接口模块

&emsp;&emsp;用户接口模块包括 CLI、Hive 网页接口（Hive Web Interface，HWI）、JDBC、ODBC、Thrift Server等，用来实现外部应用对 Hive 的访问。

&emsp;&emsp;用户可以使用以下两种方式来操作数据：
- **CLI**（command-line shell）：Hive 自带的一个命令行客户端工具，用户可以通过 Hive 命令行的方式来操作数据；
- **HWI**（Thrift/JDBC）：HWI 是 Hive 的一个简单网页，JDBC、ODBS 和 Thrift Server 可以向用户提供进行编程访问的接口。用户可以通过 Thrift 协议按照标准的 JDBC 的方式操作数据。

### 6.3.2 驱动模块

&emsp;&emsp;驱动模块（Driver）包括编译器、优化器、执行器等，所采用的执行引擎可以是 MapReduce、Tez 或 Spark 等。当采用 MapReduce 作为执行引擎时，驱动模块负责把 HiveQL 语句转换成一系列 MapReduce 作业，所有命令和查询都会进入驱动模块，通过该模块对输入进行解析编译，对计算过程进行优化，然后按照指定的步骤执行。

### 6.3.3 元数据存储模块

&emsp;&emsp;元数据存储模块（Metastore）是一个独立的关系数据库，通常是与 MySQL 数据库连接后创建的一个 MySQL 实例，也可以是 Hive 自带的 derby 数据库实例。元数据存储模块中主要保存表模式和其他系统元数据，如表的名称、表的列及其属性、表的分区及其属性、表的属性、表中数据所在位置信息等。

&emsp;&emsp;在 Hive 中，所有的元数据默认存储在 Hive 内置的 derby 数据库中，但由于 derby 只能有一个实例，也就是说不能有多个命令行客户端同时访问，所以在实际生产环境中，通常使用 MySQL 代替 derby。

&emsp;&emsp;Hive 进行的是统一的元数据管理，就是说你在 Hive 上创建了一张表，然后在 presto／impala／sparksql 中都是可以直接使用的，它们会从 Metastore 中获取统一的元数据信息，同样的你在 presto／impala／sparksql 中创建一张表，在 Hive 中也可以直接使用。

### 6.3.4 HQL的执行流程

&emsp;&emsp;Hive 在执行一条 HQL 的时候，会经过以下步骤：

1. 语法解析：Antlr 定义 SQL 的语法规则，完成 SQL 词法，语法解析，将 SQL 转化为抽象语法树 AST Tree；
2. 语义解析：遍历 AST Tree，抽象出查询的基本组成单元 QueryBlock；
3. 生成逻辑执行计划：遍历 QueryBlock，翻译为执行操作树 OperatorTree；
4. 优化逻辑执行计划：逻辑层优化器进行 OperatorTree 变换，合并不必要的 ReduceSinkOperator，减少 shuffle 数据量；
5. 生成物理执行计划：遍历 OperatorTree，翻译为 MapReduce 任务；
6. 优化物理执行计划：物理层优化器进行 MapReduce 任务的变换，生成最终的执行计划。

> 关于 Hive SQL 的详细工作原理可以参考美团技术团队的文章：[HiveQL编译过程](https://tech.meituan.com/2014/02/12/hive-sql-to-mapreduce.html)

## 6.4 Hive 编程实战

### 6.4.1 实验一：Hive的安装部署和管理

#### 6.4.1.1 实验准备

**实验环境：**Linux CentOS 7  
**前提条件：**  

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.0.0的单点部署（详见第2章安装单机版Hadoop）
3. MySQL数据库安装完成

#### 6.4.1.2 实验内容

基于上述前提条件，完成hive的安装部署和管理。

✅**官网参考教程**：[GettingStarted](https://cwiki.apache.org/confluence/display/Hive/GettingStarted)

#### 6.4.1.3 实验步骤

##### 1.解压安装包

&emsp;通过官网下载地址（✅**官网下载地址**：[Hive下载](https://dlcdn.apache.org/hive/)），下载hive 2.3.2的安装包到本地指定目录，如/data/hadoop/下。运行下面的命令，解压安装包至`/opt`目录下：

`sudo tar -zxvf /data/hadoop/apache-hive-2.3.2-bin.tar.gz -C /opt/`

解压后，在/opt目录下产生了apache-hive-2.3.2-bin文件夹

##### 2.更改文件夹名和所属用户

更改文件夹名

`sudo mv /opt/apache-hive-2.3.2-bin/ /opt/hive`

更改所属用户和用户组

`sudo chown -R datawhale:datawhale /opt/hive/`

##### 3.设置HIVE_HOME环境变量

将"/opt/hive"设置到HIVE_HOME环境变量，作为工作目录

`sudo vim ~/.bashrc`

在新弹出的编辑器的最下面添加以下内容：

```
export HIVE_HOME=/opt/hive
export PATH=$PATH:$HIVE_HOME/bin
```

运行下面命令使环境变量生效

`source ~/.bashrc`

##### 4.导入MySql jdbc jar包到hive/lib目录下

复制jar包到/app/hive/lib目录下

https://dev.mysql.com/downloads/connector/j/

`sudo cp /data/hadoop/mysql-connector-java-5.1.7-bin.jar /opt/hive/lib/`

更改jar包所属用户和用户组

`sudo chown datawhale:datawhale /opt/hive/lib/mysql-connector-java-5.1.7-bin.jar`

##### 5.修改hive配置文件

进入/opt/hive/conf目录下

`cd /opt/hive/conf`

将hive-default.xml.template文件重命名为hive-default.xml

`sudo mv hive-default.xml.template hive-default.xml`

创建hive-site.xml文件

`sudo touch hive-site.xml`

执行后，会在/opt/hive/conf/下产生hive-site.xml文件

修改hive-site.xml文件

`sudo vim hive-site.xml`

在弹出的编辑器中添加以下内容：
（提示：可以将桌面上的hive-site.txt中的内容复制到hive-site.xml文件中）

```
<configuration>
<property>
<name>javax.jdo.option.ConnectionURL</name>
<value>jdbc:mysql://localhost:3306/hive_metadata?createDatabaseIfNotExist=true</value>
</property>
<property>
<name>javax.jdo.option.ConnectionDriverName</name>
<value>com.mysql.jdbc.Driver</value>
</property>
<property>
<name>javax.jdo.option.ConnectionUserName</name>
<value>root</value>
</property>
<property>
<name>javax.jdo.option.ConnectionPassword</name>
<value>123456</value>
</property>
</configuration>
```

至此，hive的配置已经完成

##### 6.启动MySQL

hive的元数据需要存储在关系型数据库中，这里我们选择了Mysql
本实验平台已经提前安装好了MySql（账户名root，密码123456），这里只需要启动MySql服务即可

`sudo /etc/init.d/mysql start`

启动成功显示如下

```
datawhale@tools:~$ sudo /etc/init.d/mysql start
* Starting MySQL database server mysqld
No directory, logging in with HOME=/
[ OK ]
```

##### 7.指定元数据数据库类型并初始化Schema

`schematool -initSchema -dbType mysql`

初始化成功后，效果如下：

```dolphin@tools:/opt/hive/conf$ schematool -initSchema -dbType mysql
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/opt/hive/lib/log4j-slf4j-impl-2.6.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/opt/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
Metastore connection URL:    jdbc:mysql://localhost:3306/hive_metadata?createDatabaseIfNotExist=true
Metastore Connection Driver :    com.mysql.jdbc.Driver
Metastore connection User:   root
Starting metastore schema initialization to 2.3.0
Initialization script hive-schema-2.3.0.mysql.sql
Initialization script completed
schemaTool completed
```

##### 8.启动Hadoop

进入/opt/hadoop/bin目录

`cd /opt/hadoop/sbin`

执行启动脚本

`./start-all.sh`

检验hadoop是否启动成功

`jps`

```
datawhale@tools:/opt/hadoop/sbin$ jps
2258 ResourceManager
2020 SecondaryNameNode
1669 NameNode
1787 DataNode
2731 Jps
2556 NodeManager
```

如上6个进程都启动，表明Hadoop启动成功

##### 9.启动hive

`hive`

启动成功后，显示效果如下

```
datawhale@tools:/opt/hadoop/sbin$ hive
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/opt/hive/lib/log4j-slf4j-impl-2.6.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/opt/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
 
Logging initialized using configuration in jar:file:/opt/hive/lib/hive-common-2.3.3.jar!/hive-log4j2.properties Async: true
Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. spark, tez) or using Hive 1.X releases.
hive>
```

##### 10.检验hive能否使用

在hive命令行下执行show databases;命令，用于显示有哪些数据库，显示效果如下

```
hive> show databases;
OK
default
Time taken: 3.06 seconds, Fetched: 1 row(s)
```

如上表明hive安装部署成功，本次实验结束啦！

### 6.4.2 实验二：操作分区表

#### 6.4.2.1 实验准备

**实验环境：**Linux CentOS 7  
**前提条件：**  

1. 完成Java运行环境部署（详见第2章Java安装）
2. 完成Hadoop 3.0.0的单点部署（详见第2章安装单机版Hadoop）
3. MySQL数据库安装完成
4. Hive单点部署完成

#### 6.4.2.2 实验内容

基于上述前提条件， 使用Hive完成以下实验：

1. 创建数据库

2. 创建内、外分区表，并导入数据

3. 创建动态分区表
4. 删除分区表

#### 6.4.2.3 实验步骤

##### 1.启动MySQL

本实验平台已经提前安装好了MySql（账户名root，密码123456），这里只需要启动MySql服务即可

`sudo /etc/init.d/mysql start`

启动成功显示如下

![](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210507113111.png)

##### 2.指定元数据数据库类型并初始化Schema

`schematool -initSchema -dbType mysql`

初始化成功后，效果如下：

```
datawhale@tools:~$ schematool -initSchema -dbType mysql
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/apps/hive/lib/log4j-slf4j-impl-2.6.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/apps/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
Metastore connection URL:    jdbc:mysql://localhost:3306/hive_metadata?createDatabaseIfNotExist=true
Metastore Connection Driver :    com.mysql.jdbc.Driver
Metastore connection User:   root
Starting metastore schema initialization to 2.3.0
Initialization script hive-schema-2.3.0.mysql.sql
Initialization script completed
schemaTool completed
```

##### 3.启动Hadoop

进入/apps/hadoop/bin目录

`cd /apps/hadoop/sbin`

执行启动脚本

`./start-all.sh`

注意，如果终端显示Are you sure you want to continue connecting (yes/no)? 提示，我们需要输入yes，再按回车即可。

检验hadoop是否启动成功

`jps`

如下，6个进程都出现了，表明Hadoop启动成功

![image-20210507113338055](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210507113338.png)

##### 4.启动hive

`hive`

启动成功后，显示效果如下

```
datawhale@tools:~$ hive
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/apps/hive/lib/log4j-slf4j-impl-2.6.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/apps/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
 
Logging initialized using configuration in jar:file:/apps/hive/lib/hive-common-2.3.3.jar!/hive-log4j2.properties Async: true
Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. spark, tez) or using Hive 1.X releases.
hive>
```

此时，终端显示hive>，表明已经进入hive的命令行模式。

##### 5.创建名为datawhale的数据库

`create database if not exists datawhale;`

执行后显示如下：

![image-20210507113505481](C:/Users/56550/AppData/Roaming/Typora/typora-user-images/image-20210507113505481.png)

##### 6.查看已有的数据库,并使用datawhale数据库

`show databases;`

执行后显示如下：

![image-20210507113547926](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/image-20210507113547926.png)

`use datawhale;`

执行后显示如下：

```
hive> use datawhale;
OK
Time taken: 0.101 seconds
```

##### 7.创建内部静态分区表

**partition_table**表中一共有3个字段id，name，city，并以","为分割符

```
create table partition_table(id int,name string)
partitioned by(city string)
row format delimited
fields terminated by ',';
```

![image-20210511190445268](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511190448.png)

##### 8.向分区表partition_table导入数据

我们已经在本地准备好数据集dome1.txt，输入以下命令，回车

![image-20210511190711419](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511190711.png)

`load data local inpath '/home/datawhale/Desktop/dome1.txt' into table partition_table partition(city="beijing");`

执行后显示如下：

![image-20210511190820190](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511190820.png)

查看partition_table表中的数据，输入以下命令，回车

`select * from partition_table;`

执行后显示如下：

![image-20210511190936935](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511190936.png)

##### 9.增加分区

给partition_table增加一个分区，以字段值city="hangzhou"为新增分区

`alter table partition_table add partition(city="hangzhou");`

查看partition_table的分区，输入以下命令，回车

`show partitions partition_table;`

执行后显示如下：

![image-20210511191110704](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511191202.png)

导入**新增**的分区数据，输入以下命令，回车，如果没导入数据执行select * from partition_table不会出现hangzhou，和原先的一样。

![image-20210511230227815](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511230227.png)

![image-20210511191308382](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511191308.png)

`load data local inpath '/home/datawhale/Desktop/dome2.txt' into table partition_table partition(city="hangzhou");`

`select * from partition_table;`

执行后显示如下：

![image-20210511191558304](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511191558.png)

##### 10.创建名为partition_table1的动态分区表

首先，修改hive的默认配置，开启动态分区，输入以下命令，回车

`set hive.exec.dynamici.partition=true; #开启动态分区，默认是false`

`set hive.exec.dynamic.partition.mode=nonstrict; #开启允许所有分区都是动态的，否则必须要有静态分区才能使用。`

创建动态分区表partition_table1

```
create table partition_table1(id int,name string)
partitioned by(city string)
row format delimited
fields terminated by ',';
```

执行后显示如下：

![image-20210511192724689](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511192724.png)

查看此时partition_table1的分区，输入以下命令，回车

`show partitions partition_table1;`

执行后显示如下：

![image-20210511192855681](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511192855.png)

向表partition_table1导入数据

`insert into table partition_table1 partition (city) select id,name,city from partition_table;`

注意：hive此时会执行Mapreduce任务，等待任务结束。 部分日志如下

![image-20210511193043986](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511193044.png)

##### 11.查看动态分区表partition_table1

查看partition_table1分区

`show partitions partition_table1;`

执行后显示如下：

![image-20210511193117701](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511193117.png)

查看partition_table1的数据

`select * from partition_table1;`

执行后显示如下：

![image-20210511193143435](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511193143.png)

##### 12.在HDFS上查看partition_table1的数据

新打开一个命令终端，输入如下命令，回车

`hadoop fs -ls /user/hive/warehouse/datawhale.db`

执行后显示如下：

![image-20210511193351558](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511193351.png)

查看**hive的分区数据**在HDFS上的状态

`hadoop fs -ls /user/hive/warehouse/datawhale.db/partition_table1`

执行后显示如下：

![image-20210511193510586](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511193510.png)

查看**partition_table1表在“beijing”分区**的数据

`hadoop fs -cat /user/hive/warehouse/datawhale.db/partition_table1/city=beijing/000000_0`

执行后显示如下：

![image-20210511193618044](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511193618.png)

##### 13.创建一个外部分区表partition_table2

```
create external table partition_table2(id int,name string)
partitioned by(city string)
row format delimited
fields terminated by ',';
```

执行后显示如下：

![image-20210511194123431](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511194123.png)

导入数据：

`insert into table partition_table2 partition (country) select * from partition_table;`

BUG的问题：插入分区字段名必须跟创建表分区字段名相同。

**修改为以下两种都可以：**

`insert into table partition_table2 partition (city) select * from partition_table;`

`insert into table partition_table2 partition (city) select id,name,city from partition_table;`

执行后部分日志显示如下：

![image-20210511194650192](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511194650.png)

查看数据：

`select * from partition_table2;`

执行后显示如下：

![image-20210511194738708](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511194738.png)

##### 14.删除内部分区表和外部分区表

```
alter table partition_table1 drop partition(city="beijing");
alter table partition_table2 drop partition(city="beijing");
```

执行后显示如下：

![image-20210511194957908](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511194957.png)

##### 15.查看表的数据

`select * from partition_table1;`

`select * from partition_table2;`

执行后显示如下：

![image-20210511195114927](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511195114.png)

##### 16.查看表的分区信息

更新表的信息，输入如下命令

`msck repair table partition_table1;`

`msck repair table partition_table2;`

执行后显示如下：

![image-20210511195219306](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511195219.png)

查看表分区信息

`show partitions partition_table1;`

`show partitions partition_table2;` （如果不更新表的信息，不将原始数据重写会metastore那么只是显示hangzhou）

执行后显示如下：

![image-20210511195449248](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511195449.png)

`select * from partition_table2;`

![image-20210511233510771](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511233510.png)

##### 14-16总结操作

![image-20210511233433242](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511233433.png)

##### 17.在HDFS查看两张表格的数据

```
hadoop fs -ls /user/hive/warehouse/datawhale.db/partition_table1/
hadoop fs -ls /user/hive/warehouse/datawhale.db/partition_table2/
```

执行后显示如下：

![image-20210511195614791](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511195614.png)

`hadoop fs -cat /user/hive/warehouse/datawhale.db/partition_table2/city=beijing/000000_0`

执行后显示如下：

![image-20210511195705559](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210511195705.png)

##### 结论

对比partition_table1和partition_table2两种表，我们发现在进行内部表和外部表的修改时，如果我们进行的操作时删除分区，那么对于外部表而言并没有删除数据源的内容，即hdfs文件系统中的数据源，只是删除了元数据中的分区内容，导致在hive中，分区被删除，但是在hdfs文件系统中，分区依旧存在。

##### 个人思考

**Q**：问题是partition_table2的数据是从partition_table中导入的，相当于table2 load hdfs文件系统中/user/hive/warehouse/datawhale.db/partition_table/目录下的数据。那么出现在/user/hive/warehouse/datawhale.db/partition_table2/目录下的数据是否和定义一样时前者目录文件的链接呢？

**A**：应该不是，是复制/移动了一份到warehouse/datawhale.db/partition_table2/中。

**Q**：即修改partition_table的内容是否会导致partition_table2的内容改变。结果是不会的，Why？

**A**：因为table和table2没有联系，在hive中进行的操作不会影响warehouse/datawhale.db/partition_table2/下的数据，只会改变metastore。如果执行`msck repair table partition_table2;`，那么**metastore（元数据）**会恢复到warehouse下的状态。


##### 小实验

- data3为外部表通过insert一个内部表的数据
- data2为外部表直接load文件（内部表也是直接load同样的文件）

![image-20210512011049832](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210512011206.png)

内部表删除的时候，user/hive/warehouse/datawhale.db/内部表目录也删除了

![image-20210512011143487](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210512011143.png)

外部表删除的时候，目录和文件都没有删除。

如果外部表是用内部表的data进行insert的，即使内部表被删除了，user/hive/warehouse/datawhale.db/外部表数据依旧存在。

![image-20210512011158613](https://gitee.com/shenhao-stu/picgo/raw/master/DataWhale/20210512011158.png)

所以外部表应该也是移动了一份数据到user/hive/warehouse/datawhale.db/外部表目录中。



## 6.5 本章小结

&emsp;&emsp;在本章的学习中，主要介绍了数据仓库的主要特征，通过大学教育的数仓建模讲解了维度建模方法；基于建立于`Hadoop`之上的`Hive`工具，主要介绍了`Hive`的基本概念，包括`HQL`执行流程和产生背景，并通过一个小示例，模拟实现`Hive`；还介绍了`Hive`的核心概念，主要有`metadata`、`metastore`、`metastore`管理元数据的方式（内嵌模式、本地模式和远程模式）以及`Hive`的数据模型（库、表、分区和分桶）。

> ps：多用脑，多思考，这一章内容很干，希望大家足够肝。  
> 保护眼睛，保护头发，好好学习，天天向上

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch6.5.png" style="zoom:80%;" /></center>