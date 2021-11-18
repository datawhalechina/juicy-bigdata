<center><h1>Hive的安装部署和管理</h1></center>
[TOC]

## Hive的安装部署和管理

#### 实验环境

Linux Ubuntu 16.04
前提条件：
1）Java 运行环境部署完成
2）Hadoop 3.0.0 的单点部署完成
3) MySQL数据库安装完成
上述前提条件，我们已经为你准备就绪了。

#### 实验内容

在上述前提条件下，完成hive的安装部署和管理

#### 实验步骤

##### 1.点击"命令行终端"，打开新窗口

##### 2.解压安装包

我们已为您预先下载了Hive的安装包，可直接运行下面的命令，解压安装包 。

`sudo tar -zxvf /data/hadoop/apache-hive-2.3.2-bin.tar.gz -C /opt/`

解压后，在/opt目录下产生了apache-hive-2.3.2-bin文件夹

##### 3.更改文件夹名和所属用户

更改文件夹名

`sudo mv /opt/apache-hive-2.3.2-bin/ /opt/hive`

更改所属用户和用户组

`sudo chown -R dolphin:dolphin /opt/hive/`

##### 4.设置HIVE_HOME环境变量

将"/opt/hive"设置到HIVE_HOME环境变量，作为工作目录

`sudo vim ~/.bashrc`

在新弹出的编辑器的最下面添加以下内容：

```
export HIVE_HOME=/opt/hive
export PATH=$PATH:$HIVE_HOME/bin
```

运行下面命令使环境变量生效

`source ~/.bashrc`

##### 5.导入MySql jdbc jar包到hive/lib目录下

复制jar包到/app/hive/lib目录下

`sudo cp /data/hadoop/mysql-connector-java-5.1.7-bin.jar /opt/hive/lib/`

更改jar包所属用户和用户组

`sudo chown dolphin:dolphin /opt/hive/lib/mysql-connector-java-5.1.7-bin.jar`

##### 6.修改hive配置文件

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

##### 7.启动MySQL

hive的元数据需要存储在关系型数据库中，这里我们选择了Mysql
本实验平台已经提前安装好了MySql（账户名root，密码123456），这里只需要启动MySql服务即可

`sudo /etc/init.d/mysql start`

启动成功显示如下

```
dolphin@tools:~$ sudo /etc/init.d/mysql start
* Starting MySQL database server mysqld
No directory, logging in with HOME=/
[ OK ]
```



##### 8.指定元数据数据库类型并初始化Schema

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

##### 9.启动Hadoop

进入/opt/hadoop/bin目录

`cd /opt/hadoop/sbin`

执行启动脚本

`./start-all.sh`

检验hadoop是否启动成功

`jps`

```
dolphin@tools:/opt/hadoop/sbin$ jps
2258 ResourceManager
2020 SecondaryNameNode
1669 NameNode
1787 DataNode
2731 Jps
2556 NodeManager
```

如上6个进程都启动，表明Hadoop启动成功

##### 10.启动hive

`hive`

启动成功后，显示效果如下

```
dolphin@tools:/opt/hadoop/sbin$ hive
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/opt/hive/lib/log4j-slf4j-impl-2.6.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/opt/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
 
Logging initialized using configuration in jar:file:/opt/hive/lib/hive-common-2.3.3.jar!/hive-log4j2.properties Async: true
Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. spark, tez) or using Hive 1.X releases.
hive>
```

##### 11.检验hive能否使用

在hive命令行下执行show databases;命令，用于显示有哪些数据库，显示效果如下

```
hive> show databases;
OK
default
Time taken: 3.06 seconds, Fetched: 1 row(s)
```

如上表明hive安装部署成功，本次实验结束啦

