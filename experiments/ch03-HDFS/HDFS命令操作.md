<center><h1>
HDFS命令操作
</h1></center>

#### 实验环境

  Linux Ubuntu 16.04
  前提条件：
  1）Java 运行环境部署完成
  2）Hadoop 的单点部署完成
  上述前提条件，我们已经为你准备就绪了。

#### 实验内容

  在上述前提条件下，这个实验学习HDFS其它未遇到过的命令。

#### 实验步骤

##### 1.点击桌面的"命令行终端"，打开新的命令行窗口

##### 2.启动HDFS

  启动HDFS，在命令行窗口输入下面的命令：

  `/apps/hadoop/sbin/start-dfs.sh`

  运行后显示如下，根据日志显示，分别启动了NameNode、DataNode、Secondary NameNode：

```
dolphin@tools:~$ /apps/hadoop/sbin/start-dfs.sh 
Starting namenodes on [localhost]
localhost: Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
Starting datanodes
Starting secondary namenodes [tools.hadoop.fs.init]
tools.hadoop.fs.init: Warning: Permanently added 'tools.hadoop.fs.init,172.22.0.2' (ECDSA) to the list of known hosts.
```

##### 3.查看HDFS相关进程

  在命令行窗口输入下面的命令：

  `jps`

  运行后显示如下，表明NameNode、DataNode、Secondary NameNode已经成功启动

```
dolphin@tools:~$ jps
484 DataNode
663 SecondaryNameNode
375 NameNode
861 Jps
```

##### 4.准备要上传的文件

  在命令行窗口输入下面的命令：

  `hadoop fs -put ./test.txt /`

  运行后，已经本地的test.txt文件上传到HDFS的根目录下

##### 5.统计文件数和大小

  在命令行窗口输入下面的命令：

  `hadoop fs -count -h /`

  运行后显示如下，1 1 306 分别是根目录下文件数、目录数、和文件的大小

```
dolphin@tools:~$ hadoop fs -count -h /
	1      1        306
```

##### 6.查找文件

  在命令行窗口输入下面的命令，用于查找根目录下所有以txt结尾的文件

  `hadoop fs -find / -name *.txt`

  运行后如下：

```
dolphin@tools:~$ hadoop fs -find / -name *.txt
/test.txt
```

##### 7.改变文件的副本数

  默认HDFS是有3个副本的，若想改变某文件的副本数，使用setrep命令即可。在命令行窗口输入下面的命令

  `hadoop fs -setrep -w 1 /test.txt`

  运行后显示如下：

```
dolphin@tools:~$ hadoop fs -setrep -w 1 /test.txt
Replication 1 set: /test.txt
Waiting for /test.txt ... done
```

##### 8.test命令

  检查文件是否存在。如果存在则返回0，否则返回1
  在命令行窗口输入下面的命令

  `hadoop fs -test -e /zeno.txt`

  在命令行窗口输入下面的命令

  `echo $?`

  运行后显示如下，返回1表明不存在zeno.txt文件：

```
dolphin@tools:~$ echo $?
1
```

##### 9.stat命令

  在命令行窗口输入下面的命令，返回指定路径的统计信息：

  `hadoop fs -stat /test.txt`

  运行后显示如下：

```
dolphin@tools:~$ hadoop fs -stat /test.txt
2019-11-28 16:20:30
```

##### 10.清理回收站

  当用户或应用程序删除某个文件时，这个文件并没有立刻从HDFS中删除。实际上，HDFS会将这个文件重命名转移到/trash目录。只要文件还在/trash目录中，该文件就可以被迅速地恢复。文件在/trash中保存的时间是可配置的，当超过这个时间时，Namenode就会将该文件从名字空间中删除。删除文件会使得该文件相关的数据块被释放。 在命令行窗口输入下面的命令，清理回收站的所有文件：

  `hadoop fs -expunge`

  至此，本实验结束啦。开始下一个实验吧。