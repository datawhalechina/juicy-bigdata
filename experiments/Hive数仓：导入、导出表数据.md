<center><h1>
Hive数仓：导入、导出表数据
</h1></center>

[TOC]

## Hive数仓：导入、导出表数据

### 实验环境

Linux Ubuntu 16.04

前提条件：
1）Java 运行环境部署完成
2）Hadoop2.7.6的单点部署完成
3) MySQL数据库安装完成
4) Hive单点部署完成
上述前提条件，我们已经为你准备就绪了。

### 实验内容

使用Hive完成以下实验：

1. 4种导入方式
2. 4种导出方式

现在开始我们的学习吧！

### 实验步骤

#### 1.点击"命令行终端"，打开新窗口

#### 2.启动MySQL

本实验平台已经提前安装好了MySql（账户名root，密码123456），这里只需要启动MySql服务即可

`sudo /etc/init.d/mysql start`

#### 3.指定元数据数据库类型并初始化Schema

`schematool -initSchema -dbType mysql`

#### 4.启动Hadoop

进入/apps/hadoop/bin目录

`cd /apps/hadoop/sbin`

执行启动脚本

`./start-all.sh`

注意，如果终端显示Are you sure you want to continue connecting (yes/no)? 提示，我们需要输入yes，再按回车即可。

检验hadoop是否启动成功

`jps`

如下，6个进程都出现了，表明Hadoop启动成功

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210511234649.png)

#### 5.启动hive

`hive`

启动成功后，显示效果如下

```
dolphin@tools:~$ hive
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

#### 6.创建名为dolphin的数据库

`create database if not exists dolphin;`

显示并使用新建的dolphin数据库

`show databases;`

`use dolphin;`

#### 7.创建表

创建用于测试的两张表格testA和testB

```
CREATE TABLE testA ( 
  id INT, 
  name string, 
  area string 
) PARTITIONED BY (create_time string) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;
```

```
CREATE TABLE testB (  
    id INT,  
    name string,  
    area string,  
    code string  
) PARTITIONED BY (create_time string) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;
```

查看当前数据库的表格

`show tables;`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210511235116.png)

#### 8.导入方式一：本地文件导入到Hive表

我们已经在桌面为大家准备好数据集sourceA.txt和sourceB.txt，打开文件观察数据

将数据导入testA，并将分区设置为'2015-07-08'

`LOAD DATA LOCAL INPATH '/home/dolphin/Desktop/sourceA.txt' INTO TABLE testA PARTITION(create_time='2015-07-08');`

将数据导入testB，并将分区设置为'2015-07-09'

`LOAD DATA LOCAL INPATH '/home/dolphin/Desktop/sourceB.txt' INTO TABLE testB PARTITION(create_time='2015-07-09');`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210511235211.png)

#### 9.查看数据

查看testA表的数据

`select * from testA;`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210511235306.png)

查看testB表的数据

`select * from testB;`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210511235319.png)

#### 10.导入方式二：Hive表导入到Hive表

这里我将testB的数据导入到testA表

说明：将testB中id=1的行，导入到testA，分区为2015-07-11

`INSERT INTO TABLE testA PARTITION(create_time='2015-07-11') select id, name, area from testB where id = 1;`

执行后部分日志显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210511235434.png)

动态导入分区表数据，需要开启hive设置

`set hive.exec.dynamic.partition.mode=nonstrict;`

说明：将testB中id=2的行，导入到testA，分区create_time为id=2行的code值。

`INSERT INTO TABLE testA PARTITION(create_time) select id, name, area, code from testB where id = 2;`

执行后部分日志显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210511235638.png)

#### 11.查看此时testA表的信息

查看testA的全部数据

`select * from testA;`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210511235757.png)

查看testA的分区信息

`SHOW PARTITIONS testA;`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210511235846.png)

#### 12.导入方式三：HDFS文件导入到Hive表

将sourceA.txt传到HDFS中，路径是/home/hadoop/sourceA.txt

上传数据，输入如下命令：

`hadoop fs -mkdir /home`

`hadoop fs -put /home/dolphin/Desktop/sourceA.txt /home/`

查看文件是否上传成功

`hadoop fs -ls /home`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512000212.png)

导入HDFS上的数据，这里相当于给testA添加了一个新的分区数据

`LOAD DATA INPATH '/home/sourceA.txt' INTO TABLE testA PARTITION(create_time='2015-07-13');`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512000401.png)

查看testA的数据

`select * from testA;`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512000428.png)

#### 13.导入方式四：创建表的过程中从其他表导入

创建testC表

`create table testC as select name, code from testB;`

执行后部分日志显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512000512.png)

查看testC的数据

`select * from testC;`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512000535.png)

#### 14.导出方式一：导出到本地文件系统

通过INSERT OVERWRITE LOCAL DIRECTORY将hive表testA数据导入到指定目录
HQL会启动Mapreduce完成，这里的/home/dolphin/Desktop/output就是Mapreduce输出路径，产生的结果存放在文件名为：000000_0

`INSERT OVERWRITE LOCAL DIRECTORY '/home/dolphin/Desktop/output' ROW FORMAT DELIMITED FIELDS TERMINATED by ',' select * from testA;`

执行后部分日志显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512000805.png)

注意：hive导出数据到指定的文件夹，会覆盖原文件内容，若不存在就创建文件夹和文件

查看导出数据，重新打开一个命令行终端，输入如下命令：

`cat /home/dolphin/Desktop/output/000000_0`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512001048.png)

#### 15.导出方式二：导出到HDFS

导入到HDFS和导入本地文件类似，去掉HQL语句的LOCAL就可以了
但是需要指定分隔符

`INSERT OVERWRITE DIRECTORY '/output' row format delimited fields terminated by '\t'select * from testB;`

执行后部分日志显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512000954.png)

在命令行终端下输入如下命令，查看导出的数据

`hadoop fs -cat /output/000000_0`

执行后显示如下：

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512001108.png)

#### 16.导出方式三：采用hive的-e参数来导出数据。

参数为： -e 的使用方式，后面接SQL语句。>>后面为输出文件路径

在命令行终端输入输入如下指令

`hive -e "select * from dolphin.testA" >> /home/dolphin/Desktop/testA_output.txt`

查看导出的testA_output.txt数据

`cat /home/dolphin/Desktop/testA_output.txt`

如下下图所示

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512001210.png)

#### 17.导出方式四：采用hive的-f参数来导出数据。

参数为： -f 的使用方式，后面接存放sql语句的文件 >> 后面为输出文件路径

在命令行终端输入输入如下指令

`vim /home/dolphin/Desktop/sql.sql`

在弹出的文件框中输入如下代码，保存退出

`select * from dolphin.testB;`

在命令行终端输入如下指令

`hive -f /home/dolphin/Desktop/sql.sql >> /home/dolphin/Desktop/testB_output.txt`

执行后部分日志显示如下：

`OKTime taken: 1.864 seconds, Fetched: 5 row(s)`

查看导出的testB_output.txt数据

`cat /home/dolphin/Desktop/testB_output.txt`

如下下图所示

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512001259.png)



#### 小实验

- data3为外部表通过insert一个内部表的数据
- data2为外部表直接load文件（内部表也是直接load同样的文件）

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512011206.png)

内部表删除的时候，user/hive/warehouse/dolphin.db/内部表目录也删除了

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512011143.png)

外部表删除的时候，目录和文件都没有删除。

如果外部表是用内部表的data进行insert的，即使内部表被删除了，user/hive/warehouse/dolphin.db/外部表数据依旧存在。

![](https://github.com/shenhao-stu/picgo/raw/master/DataWhale/20210512011158.png)

所以外部表应该也是移动了一份数据到user/hive/warehouse/dolphin.db/外部表目录中。