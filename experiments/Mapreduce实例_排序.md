<center><h1>Mapreduce实例——排序</h1></center>


[TOC]

## Mapreduce实例——排序

### 实验环境

1.Linux Centos 16.04

2.hadoop3.0.0

3.eclipse4.5.1

### 实验内容

在安装了Hadoop和eclipse的Linux系统服务器上，完成排序实验。

### 实验步骤

---

#### 1.启动Hadoop。

双击桌面命令行终端，打开命令行窗口

首先输入以下命令，回车，**进入Hadoop启动目录**

`cd /apps/hadoop/sbin`

首先输入以下命令，回车，**启动Hadoop**

`./start-all.sh`

如果启动成功，显示如下信息

```
WARNING: Attempting to start all Apache Hadoop daemons as dolphin in 10 seconds.
WARNING: This is not a recommended production deployment configuration.
WARNING: Use CTRL-C to abort.
Starting namenodes on [localhost]
localhost: Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
Starting datanodes
Starting secondary namenodes [tools.hadoop-mp.eclipse]
tools.hadoop-mp.eclipse: Warning: Permanently added 'tools.hadoop-mp.eclipse,172.30.0.2' (ECDSA) to the list of known hosts.
Starting resourcemanager
Starting nodemanagers
```

首先输入以下命令，回车，**查看Hadoop运行状态**

`jps`

显示信息如下

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414105217189.png)

运行状态中出现DataNode、NameNode、NodeManager、ResourceManager说明Hadoop启动运行正常

#### 2.环境搭建。

这里首先双击桌面eclipse图标，打开eclipse

中途会弹出如下窗口

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414105355475.png)

点击"ok"进入eclipse界面

进入eclipse界面后，如下图所示，点击window-->Preferences

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414105502062.png)

接着如下图所示，选择Hadoop Map/Reduce，点击图中图标2给出的相关内容，最后依次点击图标3，图标4

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414105613957.png)

进入eclipse界面后，点击window-->show view-->other-->mapreduce tools-->map/reduce locations，过程如下图所示

<img src="https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414105818799.png" style="zoom:50%;" />



上述操作完成后，界面下方会显示如下图标

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414110001131.png)

点击图上图标2，在新弹出的窗口中按如下内容填写

<img src="https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414110050768.png" style="zoom:67%;" />

填写完成后点击Finish

此时，点击界面右上方，如下图所示的图标

<img src="https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414111827945.png" style="zoom:50%;" />

如下图所示，选择Map/Reduce

<img src="https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414111856470.png" style="zoom:50%;" />

在界面左侧显示如下信息

<img src="https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414111908080.png" style="zoom:50%;" />

到此，基于 Eclipse 的 MapReduce 开发环境搭建完成

#### 3.普通排序实验

##### 1) 新建一个test项目

首先在eclipse界面当中，依次点击file-->new-->project进入以下界面

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414112018225.png)

双击Map/Reducer Project选项，弹出以下窗口，按下图所示，填写相关信息，创建一个test工程

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414112031285.png)

信息填写完成后，点击finish，完成创建，此时在eclipse界面左侧的Project Explorer下可以看到我们新建的工程，如下图所示

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414112040348.png)

这就是创建一个工程的方法，后期需要创建工程时，只需修改上方过程中的工程名

##### 2) 新建一个sort包

test工程创建完成后，右击该工程的src，依次点击new-->Package，弹出以下窗口，根据下图所示，填写包名。

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414112056636.png)



填写完成后点击"finish"，此时sort包创建完成，如下图所示在eclipse界面左上方的工程目录下的src下可以看到创建的sort包

<img src="https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414112147835.png" style="zoom:50%;" />

这就是创建一个包的方法，后期在某工程下需要创建包时，只需修改上方过程中的包名

##### 3) 新建一个Sort类并对其进行编辑

包创建完后，右击在sort包，依次点击new-->class弹出以下界面，按下图所示，填写类的名称

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414112202026.png)

类名填写完成后，点击finish，完成类的创建，如下图所示，在sort包下可以看到一个Sort类，同时eclipse主界面上弹出Sort类的编辑窗口

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414112218535.png)

这就是创建一个类的方法，后期在创建类的时候，只需要修改上方过程中类的名称即可

类创建完成后，依次点击file-->open file-->Desktop-->Sort.txt，在eclipse中打开Sort.txt文件

将Sort.txt中的代码复制到刚才创建的类文件Sort.java中，并保存

到这里，Sort.java类编辑完成

##### 4) 配置代码运行所需文件

双击桌面命令行终端，打开桌面命令行终端，在命令行终端中输入以下命令，回车，将Hadoop相关文件复制到项目当中的src包下

`cp /apps/hadoop/etc/hadoop/{core-site.xml,hdfs-site.xml,log4j.properties} /home/dolphin/workspace/test/src`

##### 5) 创建并上传程序的输入文件

在命令行终端中输入以下命令，回车，进入/apps目录

`cd /apps`

输入以下命令，回车，创建，并编辑file1.txt文件

`leafpad file1.txt`

在文件中输入以下内容

```
2
32
654
32
15
756
65223
```


输入以下命令，回车，创建，并编辑file2.txt文件

`leafpad file2.txt`

在文件中输入以下内容

```
5956
22
650
92
```

输入以下命令，回车，创建，并编辑file3.txt文件

`leafpad file3.txt`

在文件中输入以下内容

```
26
54
6
```

本地创建完成后，通过eclipse在Hadoop上创建/sort/input/路径，存放输入文件

如下图如所示，在DFS locations下的myhadoop下的文件标志上右击，点击Create new directory，创建新路径

<img src="https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414112349128.png" style="zoom:50%;" />

如下图所示，输入创建的路径名称，然后点击"ok",完成创建

<img src="https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414112400302.png" style="zoom:50%;" />

右击myhadoop下的文件标志，点击Refresh,进行刷新

如下图所示，刷新后，在Hadoop上创建的目录就会显示出来

<img src="https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414112657724.png" style="zoom:50%;" />

输入以下命令，回车，将本地的file1.txt文件上传的/sort/input/目录下

`hadoop fs -put file1.txt /sort/input`

输入以下命令，回车，将本地的file2.txt文件上传的/sort/input/目录下

`hadoop fs -put file2.txt /sort/input`

输入以下命令，回车，将本地的file3.txt文件上传的/sort/input/目录下

`hadoop fs -put file3.txt /sort/input`

到这里，程序所需输入文件上传成功

##### 6) 执行程序

如下图所示，在eclipse中打开Sort.java类文件，右击界面，依次点击Run As-->Java Application,运行程序。

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414112823104.png)

如果运行成功，显示如下

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414112835891.png)

右击DFS locations下的mahadoop下的sort文件，点击Refresh,进行刷新，显示如下信息，双击打开part-r-00000文件，显示如下

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414113002895.png)

出现以上信息，说明排序成功

#### 4.二次排序实验

##### 1) 创建相关类

首先，创建一个IntPair类，右击sort包，依次点击new-->class弹出以下界面，按下图所示，填写类的名称

<img src="https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414113123227.png" style="zoom:67%;" />

再创建一个rank类，右击sort包，依次点击new-->class弹出以下界面，按下图所示，填写类的名称

<img src="https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414113159227.png" style="zoom:50%;" />

类创建完成后，依次点击file-->open file-->Desktop-->IntPair.txt，在eclipse中打开IntPair.txt文件

将IntPair.txt中的代码复制到刚才创建的类文件IntPair.java中，并保存

然后同上，依次点击file-->open file-->Desktop-->rank.txt，在eclipse中打开rank.txt文件

将rank.txt中的代码复制到刚才创建的类文件rank.java中，并保存

##### 2) 创建并上传实验输入数据

双击桌面命令行终端，打开桌面命令行终端，在命令行终端中输入以下命令，回车，首先进入/apps目录下

`cd /apps/`

在当前目录下创建一个rank文件作为实验的输入文件

`leafpad rank`

执行上边命令文件会自动打开，打开后，在文件中写入如下内容

```
40 20
40 10
40 30
40 5
30 30
30 20
30 10
30 40
50 20
50 50
50 10
50 60
```

内容写入完成后，进行保存并退出

输入以下命令，回车，在Hadoop上创建输入数据存放目录

`hadoop fs -mkdir -p /rank/input`

输入以下命令，回车，将本地的输入数据上传到Hadoop上

`hadoop fs -put /apps/rank /rank/input`

到这里，实验输入数据上传成功

##### 3) 执行程序

如下图所示，打开rank.java类文件，右击文件编辑区，依次点击Run As-->Java Application,运行程序

如果运行成功，控制台显示如下信息

```
BAD_ID=0
        CONNECTION=0
        IO_ERROR=0
        WRONG_LENGTH=0
        WRONG_MAP=0
        WRONG_REDUCE=0
    File Input Format Counters 
        Bytes Read=70
    File Output Format Counters 
        Bytes Written=71
```

右击DFS locations下的myhadoop下的rank文件，点击Refresh,进行刷新，显示如下信息，双击打开part-r-00000文件，显示如下。

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414113734312.png)


出现以上信息，说明排序成功

#### 5.倒排索引实验

##### 1) 创建相关类

首先，创建一个rank1类，右击sort包，依次点击new-->class弹出以下界面，按下图所示，填写类的名称

<img src="https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414113938828.png" style="zoom:67%;" />

类创建完成后，依次点击file-->open file-->Desktop-->rank1.txt，在eclipse中打开rank1.txt文件

将rank1.txt中的代码复制到刚才创建的类文件rank1.java中，并保存

##### 2) 创建并上传实验输入数据

双击桌面命令行终端，打开桌面命令行终端，在命令行终端中输入以下命令，回车，首先进入/apps目录下

`cd` `/apps/`

在当前目录下创建一个text1和text12文件作为实验的输入文件

输入以下命令，回车，创建并打开text1文件

`leafpad text1`

打开后，在文件中写入如下内容

```
I Love Hadoop
I like ZhouSiYuan
I love me
```

内容写入完成后，进行保存并退出

输入以下命令，回车，创建并打开text2文件

`leafpad text2`

打开后，在文件中写入如下内容

```
I Love MapReduce
I like NBA
I love Hadoop
```

内容写入完成后，进行保存并退出

输入以下命令，回车，在Hadoop上创建输入数据存放目录

`hadoop fs -mkdir -p /rank1/input`

输入以下命令，回车，将本地的text1文件上传到Hadoop上

`hadoop fs -put /apps/text1 /rank1/input`

输入以下命令，回车，将本地的text2文件上传到Hadoop上

`hadoop fs -put /apps/text2 /rank1/input`

到这里，实验输入数据上传成功

##### 3) 执行程序

打开rank1.java类文件，右击文件编辑区，依次点击Run As-->Java Application,运行程序

如果运行成功，控制台显示如下信息

```
WRONG_LENGTH=0
        WRONG_MAP=0
        WRONG_REDUCE=0
    File Input Format Counters 
        Bytes Read=82
    File Output Format Counters 
        Bytes Written=649
```

右击DFS locations下的myhadoop下的rank1文件，点击Refresh,进行刷新，显示如下信息

![](https://github.com/shenhao-stu/picgo/raw/master/Others/image-20210414114147467.png)

双击打开part-r-00000文件，显示如下

```
Hadoop    hdfs://localhost:8020/rank1/input/text2:1;hdfs://localhost:8020/rank1/input/text1:1;
I   hdfs://localhost:8020/rank1/input/text1:3;hdfs://localhost:8020/rank1/input/text2:3;
Love    hdfs://localhost:8020/rank1/input/text2:1;hdfs://localhost:8020/rank1/input/text1:1;
MapReduce   hdfs://localhost:8020/rank1/input/text2:1;
NBA hdfs://localhost:8020/rank1/input/text2:1;
ZhouSiYuan  hdfs://localhost:8020/rank1/input/text1:1;
like    hdfs://localhost:8020/rank1/input/text1:1;hdfs://localhost:8020/rank1/input/text2:1;
love    hdfs://localhost:8020/rank1/input/text2:1;hdfs://localhost:8020/rank1/input/text1:1;
me  hdfs://localhost:8020/rank1/input/text1:1;
```

出现以上信息，说明排序成功