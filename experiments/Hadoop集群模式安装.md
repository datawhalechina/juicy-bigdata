## Hadoop集群模式安装

### 实验环境

Linux Ubuntu 16.04

### 实验内容

在Linux系统的服务器上，安装Hadoop3.0.0集群模式。

![](https://github.com/shenhao-stu/picgo/raw/master/Other/image-20210324200229210.png)

#### 1.安装jdk

将/data/hadoop目录下jdk-8u161-linux-x64.tar.gz 解压缩到/opt目录下。

```
sudo tar -xzvf /data/hadoop/jdk-8u161-linux-x64.tar.gz -C /opt
```

其中，tar -xzvf 对文件进行解压缩，-C 指定解压后，将文件放到/opt目录下。

下面将jdk1.8.0_161目录重命名为java，执行：

```
sudo mv /opt/jdk1.8.0_161/ /opt/java
```

修改java目录的所属用户和所属组：

```
sudo chown -R datawhale.datawhale /opt/java
```

#### 2.下面来修改环境变量

![](https://github.com/shenhao-stu/picgo/raw/master/Other/image-20210324200407803.png)

```
sudo vim /etc/profile
```

末端添加如下内容：

```
#java
export JAVA_HOME=/opt/java
export PATH=$JAVA_HOME/bin:$PATH
```

保存并关闭编辑器

让环境变量生效。

```
source /etc/profile
```

刷新环境变量后，可以通过java的家目录找到java可使用的命令。 利用java查看版本号命令验证是否安装成功：

```
java -version
```

正常结果显示如下

![](https://github.com/shenhao-stu/picgo/raw/master/Other/image-20210324200646610.png)

```
java version "1.8.0_161"
Java(TM) SE Runtime Environment (build 1.8.0_161-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.161-b12, mixed mode)
```

#### 3.安装hadoop

将hadoop-3.0.0.tar.gz解压缩到/opt目录下。

```
sudo tar -xzvf /data/hadoop/hadoop-3.0.0.tar.gz -C /opt/
```

为了便于操作，我们也将hadoop-3.0.0重命名为hadoop。

```
sudo mv /opt/hadoop-3.0.0/ /opt/hadoop
```

修改hadoop目录的所属用户和所属组：

```
sudo chown -R datawhale.datawhale /opt/hadoop
```



#### 4.下面来修改环境变量

```
sudo vim /etc/profile
```

末端添加如下内容：

```
#hadoop
export HADOOP_HOME=/opt/hadoop
export PATH=$HADOOP_HOME/bin:$PATH
```

保存并关闭编辑器

让环境变量生效。

```
source /etc/profile
```

利用hadoop查看版本号命令验证是否安装成功：

```
hadoop version
```

正常结果显示如下

![](https://github.com/shenhao-stu/picgo/raw/master/Other/image-20210324200549213.png)

```
Hadoop 3.0.0
Source code repository https://git-wip-us.apache.org/repos/asf/hadoop.git -r c25427ceca461ee979d30edd7a4b0f50718e6533
Compiled by andrew on 2017-12-08T19:16Z
Compiled with protoc 2.5.0
From source with checksum 397832cb5529187dc8cd74ad54ff22
This command was run using /opt/hadoop/share/hadoop/common/hadoop-common-3.0.0.jar
```

#### 5.修改hadoop hadoop-env.sh文件配置

```
vim /opt/hadoop/etc/hadoop/hadoop-env.sh
```

末端添加如下内容：

```
export JAVA_HOME=/opt/java/
```

保存并关闭编辑器

#### 6.修改hadoop core-site.xml文件配置

```
vim /opt/hadoop/etc/hadoop/core-site.xml
```

添加下面配置到`<configuration>与</configuration>`标签之间。

```
<property>
    <name>fs.defaultFS</name>
    <value>hdfs://master:9000</value>
</property>
```

保存并关闭编辑器

#### 7.修改hadoop hdfs-site.xml文件配置

```
vim /opt/hadoop/etc/hadoop/hdfs-site.xml
```

添加下面配置到`<configuration>与</configuration>`标签之间。

```
<property>
    <name>dfs.replication</name>
    <value>3</value>
</property>
```

保存并关闭编辑器

#### 8.修改hadoop yarn-site.xml文件配置

```
vim /opt/hadoop/etc/hadoop/yarn-site.xml
```

添加下面配置到`<configuration>与</configuration>`标签之间。

```
<property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
</property>
<property>
    <name>yarn.nodemanager.env-whitelist</name>
   <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
</property>
```

保存并关闭编辑器

#### 9.mapred-site.xml文件配置

```
vim /opt/hadoop/etc/hadoop/mapred-site.xml
```

添加下面配置到`<configuration>与</configuration>`标签之间。

```
<property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
</property>
```

保存并关闭编辑器

#### 10.修改hadoop workers文件配置

```
vim /opt/hadoop/etc/hadoop/workers
```

覆盖写入主节点映射名和从节点映射名：

```
master
slave1
slave2
```

保存并关闭编辑器

#### 11.修改hosts文件

查看master ip地址

```
ip addr    
```

记录下显示的ip，例：172.18.0.4

打开slave1 节点，做如上操作，记录下显示的ip，例：172.18.0.3

打开slave2 节点，做如上操作，记录下显示的ip，例：172.18.0.2

编辑/etc/hosts文件：

```
sudo vim /etc/hosts
```

添加master IP地址对应本机映射名和其它节点IP地址对应映射名(如下只是样式，请写入实验时您的正确IP)：

```
172.18.0.4 master
172.18.0.3 slave1
172.18.0.2 slave2
```

#### 12.创建公钥

在datawhale用户下创建公钥：

```
ssh-keygen -t rsa
```

出现如下内容：

Enter file in which to save the key (/home/datawhale/.ssh/id_rsa):

回车即可，出现如下内容：

Enter passphrase (empty for no passphrase):

直接回车，出现内容：

Enter same passphrase again:

直接回车，创建完成。

#### 13.拷贝公钥

提示：命令执行过程中需要输入“yes”和密码“datawhale”。三台节点请依次执行完成。

```
ssh-copy-id master
```

```
ssh-copy-id slave1
```

```
ssh-copy-id slave2
```

修改文件权限：（master和slave均需修改）

```
chmod 700 /home/datawhale/.ssh
```

```
chmod 700 /home/datawhale/.ssh/*
```

测试连接是否正常：

```
ssh master
```

#### 14.拷贝文件到所有从节点

```
scp -r /opt/java/ /opt/hadoop/ slave1:/tmp/
```

```
scp -r /opt/java/ /opt/hadoop/ slave2:/tmp/
```

至此，主节点配置完成。

现在，请去slave1和slave2依次完成节点配置。

以下内容在所有从节点配置完成之后回来继续进行!

#### 15.格式化分布式文件系统

```
hdfs namenode -format
```

#### 16.启动Hadoop

```
/opt/hadoop/sbin/start-all.sh
```

重新启动前记得要先关闭

```
/opt/hadoop/sbin/stop-all.sh
```

#### 17.查看Hadoop进程

在hadoop主节点执行：

`jps`

输出结果必须包含6个进程，结果如下：

```
2529 DataNode
2756 SecondaryNameNode
3269 NodeManager
3449 Jps
2986 ResourceManager
2412 NameNode
```

在hadoop从节点执行同样的操作：

`jps`

输出结果必须包含3个进程，具体如下：

```
2529 DataNode
3449 Jps
2412 NameNode
```

#### 18.在命令行中输入以下代码，打开Hadoop WebUI管理界面：

```
firefox http://master:8088
```

#### 19.测试HDFS集群以及MapReduce任务程序

利用Hadoop自带的WordCount示例程序进行检查集群；在主节点进行如下操作，创建HDFS目录：

```
hadoop fs -mkdir /datawhale/
```

```
hadoop fs -mkdir /datawhale/input
```

创建测试文件

```
vim /home/datawhale/test
```

添加下面文字

`datawhale`

保存并关闭编辑器

将测试文件上传到到Hadoop HDFS集群目录：

```
hadoop fs -put /home/datawhale/test /datawhale/input
```

执行wordcount程序：

```
hadoop jar /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar wordcount /datawhale/input/ /datawhale/out/
```

查看执行结果：

```
hadoop fs -ls /datawhale/out/
```

如果列表中结果包含”_SUCCESS“文件，代码集群运行成功。

![](https://github.com/shenhao-stu/picgo/raw/master/Other/image-20210324202518121.png)

查看具体的执行结果，可以用如下命令：

```
hadoop fs -text /datawhale/out/part-r-00000
```

![](https://github.com/shenhao-stu/picgo/raw/master/Other/image-20210324202554101.png)

到此，集群安装完成。



