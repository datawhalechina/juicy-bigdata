<center><h1>
实验报告
</h1></center>
<center><h4>
沈豪 2018111177 金融学院 金融三班
</h4></center>

## HDFS 的使用和管理

#### 实验环境

Linux Centos 6

#### 实验内容

  前提条件：

  1）Hadoop 3.0.0 的单点部署完成

  2）Java 运行环境部署完成

  上述前提条件，我们已经为你准备就绪了。

#### 实验步骤

##### 1. 启动hadoop的hdfs相关进程

  `cd /opt/hadoop/sbin/`

  `./start-dfs.sh`

  ![image-20210326122222326](https://i.loli.net/2021/03/26/jyqps8vO1GWxdc4.png)

##### 2. 用jps查看HDFS是否启动

`jps`

![image-20210326122736762](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210326122736762.png)

我们可以看到相关进程，都已经启动。

##### 3. 验证HDFS运行状态

先在HDFS上创建一个目录, 看是否能够成功

`hadoop fs -mkdir /myhadoop1`

如果成功，查询hdfs文件系统根目录，将看到 /myhadoop1 目录。

`hadoop fs -ls /`

![image-20210326123127674](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210326123127674.png)

##### 4. ls 命令

列出hdfs文件系统根目录下的目录和文件。

`hadoop fs -ls /` 

<p style="color:red">列出hdfs文件系统所有的目录和文件。</p>

`hadoop fs -ls -R /`

![image-20210326124327389](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210326124327389.png)

##### 5. put 命令

1）拷贝文件：**hadoop fs -put < local file > < hdfs file >**

其中< hdfs file >的父目录一定要存在，否则命令不会执行, 比如：

`hadoop fs -put /opt/hadoop/README.txt /`

2）拷贝目录：**hadoop fs -put < local dir > < hdfs dir >**

其中< hdfs dir >的父目录一定要存在，否则命令不会执行。

3）查询是否拷贝成功：

`hadoop fs -ls /`

![image-20210326125840807](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210326125840807.png)

如果拷贝文件和目录成功，你将会看到 /logs 和 /REAME.txt

##### 6. moveFromLocal 命令

1) 拷贝文件或目录：

**hadoop fs -moveFromLocal < local src > < hdfs dst >**

与put相类似，命令执行后源文件 local src 被删除

`hadoop fs -moveFromLocal /opt/hadoop/NOTICE.txt /myhadoop1`

`hadoop fs -moveFromLocal /opt/hadoop/logs /myhadoop1`

2）查询是否拷贝成功：

`hadoop fs -ls /myhadoop1`

如果拷贝文件和目录成功，你将会看到 /logs 和 /NOTICE.txt

![image-20210326130117258](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210326130117258.png)

##### 7. get 命令

1) 拷贝文件或目录到本地：

**hadoop fs -get < hdfs file or dir > < local file or dir>**

local file不能和 hdfs file名字不能相同，否则会提示文件已存在，没有重名的文件会复制到本地

`hadoop fs -get /myhadoop1/NOTICE.txt /opt/hadoop/`

`hadoop fs -get /myhadoop1/logs /opt/hadoop/`

拷贝多个文件或目录到本地时，本地要为文件夹路径

**注意：如果用户不是root， local 路径要为用户文件夹下的路径，否则会出现权限问题**

2）查询是否拷贝得到本地成功：

`cd /opt/hadoop`

`ls -l`

![image-20210326130225990](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210326130225990.png)

如果拷贝文件和目录成功，你将会看到 logs 和 NOTICE.txt

##### 8. rm 命令

1) 删除一个或多个文件

**hadoop fs -rm < hdfs file > ...**

`hadoop fs -rm /README.txt`

2) 删除一个或多个目录

**hadoop fs -rm -r < hdfs dir > ...**

`hadoop fs -rm -r /logs`

3）查询是否删除成功：

`hadoop fs -ls /`

如果删除文件和目录成功，你将不会看到 /logs 和 /NOTICE.txt

##### 9. mkdir 命令

1) 创建一个新目录：

**hadoop fs -mkdir < hdfs path >**

只能一级一级的建目录，父目录不存在则这个命令会报错

**hadoop fs -mkdir -p < hdfs dir > ...**

所创建的目录如果父目录不存在就创建该父目录

`hadoop fs -mkdir /myhadoop1/test`

`hadoop fs -mkdir -p /myhadoop2/test`

2）查询目录：

`hadoop fs -ls /`

`hadoop fs -ls /myhadoop1`

`hadoop fs -ls /myhadoop2`

![image-20210326130527696](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210326130527696.png)

如果创建目录成功，你将会看到 /myhadoop1/test 和 /myhadoop2/test

##### 10. cp 命令

完成HDFS 上文件或目录的拷贝

**hadoop fs -cp < hdfs file > < hdfs file >**

目标文件不能存在，否则命令不能执行，相当于给文件重命名并保存，源文件还存在

**hadoop fs -cp < hdfs file or dir >... < hdfs dir >**

目标文件夹要存在，否则命令不能执行

1）拷贝一个本地文件到 HDFS 的根目录下

`hadoop fs -put /opt/hadoop/LICENSE.txt /`

成功后，即可以查询到此文件

`hadoop fs -ls /`

2）然后将此文件拷贝到 /myhadoop1 下

`hadoop fs -cp /LICENSE.txt /myhadoop1`

3）查询 /myhadoop1 目录：

`hadoop fs -ls /myhadoop1`

![image-20210328120303473](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328120303473.png)

如果拷贝成功，你将会看到 LICENSE.txt 文件

##### 11. mv 命令

完成HDFS 上文件或目录的移动

**hadoop fs -mv < hdfs file > < hdfs file >**

目标文件不能存在，否则命令不能执行，相当于给文件重命名并保存，源文件不存在

**hadoop fs -mv < hdfs file or dir >... < hdfs dir >**

源路径有多个时，目标路径必须为目录，且必须存在

**注意：跨文件系统的移动（local到hdfs或者反过来）都是不允许的**

1) 移动一个 HDFS 文件

`hadoop fs -mv /myhadoop1/LICENSE.txt /myhadoop2`

2) 查询 /myhadoop2 目录

`hadoop fs -ls /myhadoop2`

如果拷贝成功，你将会看到 /myhadoop2/LICENSE.txt 文件

![image-20210328120539882](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328120539882.png)

##### 12. count 命令

统计hdfs对应路径下的目录个数，文件个数，文件总计大小

**hadoop fs -count < hdfs path >**

`hadoop fs -count /myhadoop1/logs`

显示为目录个数，文件个数，文件总计大小，输入路径， 如下：

`1 8 128199 /myhadoop1/logs`

![image-20210328120715221](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328120715221.png)

![image-20210328122017712](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328122017712.png)

##### 13. du 命令

**hadoop fs -du < hdsf path>**

显示hdfs对应路径下每个文件夹和文件的大小

**hadoop fs -du -s < hdsf path>**

显示hdfs对应路径下所有文件总和的大小

**hadoop fs -du -h < hdsf path>**

显示hdfs对应路径下每个文件夹和文件的大小,文件的大小用方便阅读的形式表示，例如用64M代替67108864

`hadoop fs -du /myhadoop2`

`hadoop fs -du -s /myhadoop2`

`hadoop fs -du -h /myhadoop2`

`hadoop fs -du -s -h /myhadoop2`

![image-20210328122230795](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328122230795.png)

>第一列标示该目录下总文件大小
>
>第二列标示该目录下所有文件在集群上的总存储大小和你的副本数相关，我的副本数是3 ，所以第二列的是第一列的三倍 （第二列内容=文件大小*副本数）
>
>第三列标示你查询的目录

![image-20210328124349144](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328124349144.png)

##### 14. setrep 命令

**hadoop fs -setrep -R 3 < hdfs path >**

改变一个文件在hdfs中的副本个数，上述命令中数字3为所设置的副本个数

-R选项可以对一个人目录下的所有目录+文件递归执行改变副本个数的操作

`hadoop fs -setrep -R 3 /myhadoop1`

![image-20210328122422486](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328122422486.png)

##### 15. stat 命令

**hdoop fs -stat [format] < hdfs path >**

返回对应路径的状态信息

[format]可选参数有：

%b（文件大小）

%o（Block大小）

%n（文件名）

%r（副本个数）

%y（最后一次修改日期和时间）

`hadoop fs -stat %b /myhadoop2/LICENSE.txt`

显示为文件大小， 如下：

![image-20210328122533216](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328122533216.png)

##### 16. balancer 命令

**hdfs balancer**

如果管理员发现某些DataNode保存数据过多，某些DataNode保存数据相对较少，可以使用上述命令手动启动内部的均衡过程

`hadoop balancer`

`hdfs balancer`

##### 17. dfsadmin 命令

**hdfs dfsadmin -help**

管理员可以通过dfsadmin管理HDFS，用法可以通过上述命令查看

`hdfs dfsadmin -help`

**hdfs dfsadmin -report**

显示文件系统的基本数据

`hdfs dfsadmin -report`

![image-20210328123146369](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328123146369.png)

**hdfs dfsadmin -safemode < enter | leave | get | wait >**

enter：进入安全模式；

leave：离开安全模式；

get：获知是否开启安全模式；

wait：等待离开安全模式

`hdfs dfsadmin -safemode enter`

![image-20210328123230322](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328123230322.png)

##### 18. 其他 命令

![image-20210328124810316](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328124810316.png)

###### 18.1 cat 命令

查看hdfs中的文本文件内容

```
 hadoop fs -cat /demo.txt
 hadoop fs -tail -f /demo.txt
```

> hadoop fs -tail -f **根据文件描述符进行追踪，当文件改名或被删除，追踪停止**

![image-20210328125119748](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328125119748.png)

###### 18.2 appendToFile 命令

追加内容到已存在的文件

   ```
hadoop fs -appendToFile /本地文件 /hdfs中的文件
   ```

![image-20210328125642993](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328125642993.png)

###### 18.3 chown 命令

修改文件的权限

   ```
hadoop fs -chown user:group /shenhao
hadoop fs -chmod 777 /shenhao
   ```

- `chown`定义谁拥有文件。
- `chmod`定义谁可以做什么。

