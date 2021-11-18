## HDFS API操作

#### 实验环境

  Linux Ubuntu 16.04
  前提条件：
  1）Java 运行环境部署完成
  2）Hadoop 的单点部署完成
  上述前提条件，我们已经为你准备就绪了。

#### 实验内容

  在上述前提条件下，学习使用HDFS Java API编程实验。

#### 实验步骤

- 1.点击桌面的"命令行终端"，打开新的命令行窗口

- 2.启动HDFS

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


- 3.查看HDFS相关进程

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


- 4.启动Eclipse

  点击桌面的Eclipse图标，打开Eclipse

  运行后，会弹出Workspace Launcher对话框，此时workspace我们默认就行，点击OK

- 5.创建项目

  进入Eclipse后，会默认进入Welcome标签页，点击标签的叉号，退出Welcome标签。

  点击左上角工具栏File，点击New下面的Java Project。

  此时弹出了New Java Project对话框，我们填写Project Name为 Example，再点击Finish后，项目创建完成。

- 6.创建Java类

  如下图所示，找到左上角Example项目下src目录后，右击，选择New，在点击Class。

  ![image-20210328215256838](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328215256838.png)

  此时会弹出New Java Class对话框，如下图，填写Package为com.dolphin，填写Name为Example，再点击右下角Finish。此时Example类已经创建完成。

  ![image-20210328215326942](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328215326942.png)

- 7.导入Hadoop Jar包

  右击左上角Example项目，找到Build Path，点击下面的Configure Build Path...

  点击后会弹出Properties for Example对话框，如下图所示，点击Libraries后，再点击Add External JARs... 此时弹出JAR Selection对话框，找到根目录下/apps/hadoop/share/hadoop/common目录，选中hadoop-common-3.0.0.jar后，再点击OK

  ![image-20210328215346700](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328215346700.png)

  

  再次点击Add External JARs...，此时弹出JAR Selection对话框，找到根目录下/apps/hadoop/share/hadoop/common/lib目录，按住Ctrl + A，选中该目录下所有jar包后，点击OK。

  

  再次点击Add External JARs...，此时弹出JAR Selection对话框，找到根目录下/apps/hadoop/share/hadoop/hdfs目录，选中hadoop-hdfs-client-3.0.0.jar后，再点击OK.

  再点击OK，此时Jar包已经导入完成。

- 8.编写代码

  右击桌面的Example.txt文件，使用编辑器打开，按住Ctrl + A，再按住Ctrl + C复制全部内容后，回到Eclipse，编辑Example.java文件，按住Ctrl + A，再按住Ctrl + V，粘贴代码，再按住Ctrl + S保存文件。

- 9.运行代码

  点击上方绿色的Run Example按钮，开始运行代码。运行后显示如下：

  ```
  hdfs://localhost:8020/mydir create success!
  Tape Scripts Test One I Understanding Basic Skill Directions: Listen to the following passage carefully and fill in the blanks with words and phrases or sentences you hear.
   ``(30 points) All big cities are quite similar. 
  Living in a modern Asian city is not very different from living in an American city.
  hdfs://localhost:8020/mydir delete success!
  ```

  ![image-20210328214901423](https://gitee.com/shenhao-stu/picgo/raw/master/Other/image-20210328214901423.png)

- 10.运行内容

  main函数运行了四个函数，分别是createDirectory、copyFromLocalFile、readFile、deleteFile。 首先创建HDFS目录，再上传本地文件到HDFS，再读取文件内容打印到控制台，再删除HDFS文件。

  至此，本实验结束啦。开始下一个实验吧。