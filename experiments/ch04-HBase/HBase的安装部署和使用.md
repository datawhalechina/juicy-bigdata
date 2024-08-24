<center><h1>HBase的安装部署和使用</h1></center>


[TOC]
## HBase的安装部署和使用

### 实验环境

Linux Ubuntu 16.04 前提条件：
1）Java 运行环境部署完成
2）Hadoop 3.0.0 的单点部署完成
上述前提条件，我们已经为你准备就绪了。

### 实验内容

在上述前提条件下，安装HBase和HBase Shell的简单使用。

### 实验步骤

#### 1.点击"命令行终端"，打开新的命令行窗口

#### 2.解压安装包

我们已为您预先下载了hbase的安装包，可直接运行下面的命令，解压安装包 。

`sudo tar -zxvf /data/hadoop/ hbase-2.3.5-bin.tar.gz -C /opt/`

#### 3.更改文件夹名和所属用户

安装包解压成功后，在“/opt”目录下将会产生"hbase-2.3.5"目录。

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210423132920566.png)

运行下面命令，将hbase-2.3.5目录更名为hbase

`sudo mv /opt/hbase-2.3.5/ /opt/hbase`

运行下面命令，改变hbase目录所属用户和用户组

`sudo chown -R dolphin:dolphin /opt/hbase/`

#### 4.设置HBASE_HOME环境变量

将"/opt/hbase"设置到HBASE_HOME环境变量，做为工作目录。

`sudo vim /etc/profile`

在新弹出的记事本窗口的最底部添加如下内容，再保存退出。

```
export HBASE_HOME=/opt/hbase/
export PATH=$PATH:$HBASE_HOME/bin
```

运行下面命令使环境变量生效

`source /etc/profile`

#### 5.修改hbase-site.xml配置文件

`sudo vim /opt/hbase/conf/hbase-site.xml`

在新弹出的记事本窗口找到<configuration>标签，在<configuration>和</configuration>之间添加以下内容：

其余的内容删掉。

```
<property>
<name>hbase.cluster.distributed</name>
<value>true</value>
</property>
<property>
<name>hbase.rootdir</name>
<value>hdfs://localhost:8020/hbase</value>
</property>
```

  添加后保存退出编辑器即可

#### 6.修改hbase-env.sh配置文件

`sudo vim /opt/hbase/conf/hbase-env.sh`

在新弹出的记事本窗口找到 # export JAVA_HOME=/usr/java/jdk1.6.0/一行，并改为以下内容：

`export JAVA_HOME=/opt/java/`

#### 7.启动hadoop

运行下面的命令，进入hadoop目录下的sbin目录

`cd /opt/hadoop/sbin/`

运行下面的命令，启动Hadoop集群

`./start-all.sh`

检验hadoop是否启动成功

`jps`

执行上述命令后，显示如下：

```
dolphin@tools:/opt/hadoop/sbin$ jps
2261 Jps
1317 DataNode
2086 NodeManager
1788 ResourceManager
1550 SecondaryNameNode
1199 NameNode
```

如上所示出现了6个进程，表明hadoop启动成功

#### 8.启动HBase

运行下面的命令，启动HBase

`start-hbase.sh`

检验HBase是否启动成功

`jps`

执行上述命令后，显示如下：

```
dolphin@tools:~$ jps
1552 NodeManager
1010 SecondaryNameNode
659 NameNode
2759 Jps
2215 HQuorumPeer
810 DataNode
2284 HMaster
2444 HRegionServer
```

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210424184916381.png)

如果HMaster、HRegionServer和HQuorumPeer进程都出现了，说明HBase安装成功。

#### 9.启动HBase Shell

运行下面的命令，启动HBase Shell

```
    cd /opt/hbase/bin
    hbase shell
```

启动后，进入hbase命令行模式，显示如下

```
dolphin@tools:~$ hbase shell
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/opt/hbase/lib/slf4j-log4j12-1.7.5.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/opt/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
HBase Shell; enter 'help' for list of supported commands.
Type "exit" to leave the HBase Shell
Version 1.2.6, rUnknown, Mon May 29 02:25:32 CDT 2017
 
hbase(main):001:0>
```

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210424185145181.png)

#### 10.创建表

在hbase的命令行模式下，输入下面的语句，用于创建一个"student"表，"info"和"addr"为该表的两个列族

`create 'student','info','addr'`

创建后显示如下

```
    hbase(main):009:0> create 'student','info','addr'
0 row(s) in 2.2840 seconds
 
=> Hbase::Table - student
```

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210424204131514.png)

#### 11.put添加数据

hbase中的put命令用于向表中添加数据，下面我们向student表中添加数据

`put 'student','1','info:name','zeno'`

`put 'student','1','info:age','22'`

`put 'student','1','addr:city','hefei'`

`put 'student','2','info:sex','man'`

执行后显示如下：![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210424204210160.png)

#### 12.查看表内容

hbase中的scan命令用于扫描表内容，下面我们看看student表有哪些数据

`scan 'student'`

执行后显示如下：

```
hbase(main):014:0> scan 'student'
ROW                   COLUMN+CELL
1                    column=addr:city, timestamp=1531207679298, value=hefei
1                    column=info:age, timestamp=1531207651174, value=22
1                    column=info:name, timestamp=1531207642229, value=zeno
2                    column=info:sex, timestamp=1531207752067, value=man
2 row(s) in 0.0200 seconds
```

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210424204236526.png)

#### 13.查询

hbase中的get命令用于查询数据，下面我们查询一下student表中rowkey为1的一条数据

`get 'student','1'`

执行后显示如下：

```
hbase(main):015:0> get 'student','1'
COLUMN                CELL
addr:city            timestamp=1531207679298, value=hefei
info:age             timestamp=1531207651174, value=22
info:name            timestamp=1531207642229, value=zeno
3 row(s) in 0.0480 seconds
```

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210424204259759.png)

#### 14.修改内容

hbase中严格来说，没有修改数据的概念，只有覆盖数据，也是用put命令

我们先插入数据

`put 'student','1','info:age','18'`

执行后显示如下：

```
hbase(main):016:0> put 'student','1','info:age','18'
```

再查询一下，查看修改结果

```
hbase(main):017:0> get 'student','1'
COLUMN                CELL
addr:city            timestamp=1531207679298, value=hefei
info:age             timestamp=1531207651183, value=18
info:name            timestamp=1531207642229, value=zeno
3 row(s) in 0.0520 seconds
```

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210424204339528.png)

#### 15.添加列族

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210424203357381.png)
**这里可以指定NAME => 'nation' or 'NAME' => 'nation'**

#### 16.删除列族

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210424203434915.png)

#### 17.删除表

hbase中的表不能直接删除，需要禁用(disable 命令)后，才能删除(drop)，下面我们删除student表

`disable 'student'`

执行后显示如下：

```
hbase(main):018:0> disable 'student'
0 row(s) in 2.2950 seconds
```

`drop 'student'`

执行后显示如下：

```
hbase(main):019:0> drop 'student'
0 row(s) in 2.2770 seconds
```

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210424204432165.png)

