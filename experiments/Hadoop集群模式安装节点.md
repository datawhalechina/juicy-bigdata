## Hadoop集群模式安装

### 集群搭建-节点1

#### 1.Java环境配置

```
sudo mv /tmp/java /opt/
```

jdk安装完配置环境变量，编辑/etc/profile：

```
sudo leafpad /etc/profile
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

`java -version`

正常结果显示如下

```
java version "1.8.0_161"
Java(TM) SE Runtime Environment (build 1.8.0_161-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.161-b12, mixed mode)
```

#### 2.修改hosts文件

查看master ip地址

```
ifconfig eth0|sed -n '2p'|awk -F " " '{print $2}'|awk -F ":" '{print $2}'
```

记录下显示的ip，例：172.18.0.4

打开slave1 节点，做如上操作，记录下显示的ip，例：172.18.0.3

打开slave2 节点，做如上操作，记录下显示的ip，例：172.18.0.2

编辑/etc/hosts文件：

```
sudo leafpad /etc/hosts
```

添加master IP地址对应本机映射名和其它节点IP地址对应映射名(如下只是样式，请写入实验时您的正确IP)：

```
172.18.0.4 master
172.18.0.3 slave1
172.18.0.2 slave2
```

#### 3.创建公钥

在dolphin用户下创建公钥：

```
ssh-keygen -t rsa
```

出现如下内容：

Enter file in which to save the key (/home/dolphin/.ssh/id_rsa):

回车即可，出现如下内容：

Enter passphrase (empty for no passphrase):
直接回车，出现内容：
Enter same passphrase again:
直接回车，创建完成，结果内容如下：

#### 4.拷贝公钥

提示：命令执行过程中需要输入“yes”和密码“dolphin”。三台节点请依次执行完成。

```
ssh-copy-id master
ssh-copy-id slave1
ssh-copy-id slave2
```

测试连接是否正常：

```
ssh master
```

#### 5.Hadoop环境配置

```
sudo mv /tmp/hadoop /opt/
```

下面来修改环境变量

```
sudo leafpad /etc/profile
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

`hadoop version`

正常结果显示如下

```
Hadoop 3.0.0
Source code repository https://git-wip-us.apache.org/repos/asf/hadoop.git -r c25427ceca461ee979d30edd7a4b0f50718e6533
Compiled by andrew on 2017-12-08T19:16Z
Compiled with protoc 2.5.0
From source with checksum 397832cb5529187dc8cd74ad54ff22
This command was run using /opt/hadoop/share/hadoop/common/hadoop-common-3.0.0.jar
```

