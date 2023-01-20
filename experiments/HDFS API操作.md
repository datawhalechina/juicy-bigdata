## HDFS API操作

#### 实验环境

  Linux Ubuntu 22.04
  前提条件：
  1）Java 运行环境部署完成
  2）Hadoop 的单点部署或集群部署完成
  上述前提条件，我们已经为你准备就绪了。

#### 实验内容

  在上述前提条件下，学习使用HDFS Java API编程实验。

#### 实验步骤


- 1.安装并启动Eclipse

  下载压缩包后安装

  ```
  sudo tar -zxvf /data/hadoop/eclipse-4.7.0-linux.gtk.x86_64.tar.gz -C /opt
  ```

  ```
  cd /opt/eclipse
  ```

  ```
  ./eclipse
  ```

  （此处也可以在Ubuntu自带的软件园中，下载Eclipse，点击桌面的Eclipse图标，打开Eclipse）

  运行后，会弹出Workspace Launcher对话框，此时workspace我们默认就行，点击OK

- 2.创建项目

  进入Eclipse后，会默认进入Welcome标签页，点击标签的叉号，退出Welcome标签。

  点击左上角工具栏File，点击New下面的Java Project。

  此时弹出了New Java Project对话框（没有的话在other里面找），我们填写Project Name为 HDFSExample，选中“Use default location”，让这个Java工程的所有文件都保存到“/home/datawhale/workspace/HDFSExample”目录下。在“JRE”这个选项卡中，可以选择当前的Linux系统中已经安装好的JDK，即java。然后，点击界面底部的“Next>”按钮，进入下一步的设置。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114163412703.png"  style="zoom: 67%;" />

- 3.导入JAR包

  进入下一步的设置以后，点击界面中的“Libraries”选项卡，然后，点击界面右侧的“Add External JARs…”按钮。为了编写一个能够与HDFS交互的Java应用程序，一般需要向Java工程中添加以下JAR包：（可以使用“Ctrl+A”组合键进行全选操作）

  ```
  （1）"/usr/local/hadoop/share/hadoop/common”目录下的所有JAR包；
  （2）/usr/local/hadoop/share/hadoop/common/lib”目录下的所有JAR包；
  （3）“/usr/local/hadoop/share/hadoop/hdfs”目录下的所有JAR包；
  （4）“/usr/local/hadoop/share/hadoop/hdfs/lib”目录下的所有JAR包。
  ```

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114163538758.png" alt="image-20230114163538758" style="zoom:67%;" />

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114163557311.png" alt="image-20230114163557311" style="zoom:67%;" />



下面编写一个Java应用程序，用来检测HDFS中是否存在一个文件。

- 4.创建class

  请在Eclipse工作界面左侧的“Package Explorer”面板中，找到刚才创建好的工程名称“HDFSExample”，然后在该工程名称上点击鼠标右键，在弹出的菜单中选择“New->Class”菜单。

  在该界面中，只需要在“Name”后面输入新建的Java类文件的名称，这里采用名称“HDFSFileIfExist”，其他都可以采用默认设置，然后，点击界面右下角“Finish”按钮。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114163719382.png" alt="image-20230114163719382" style="zoom:67%;" />

之后，Eclipse会自动创建了一个名为“HDFSFileIfExist.java”的源代码文件，请在该文件中输入以下代码：

    import org.apache.hadoop.conf.Configuration;
    import org.apache.hadoop.fs.FileSystem;
    import org.apache.hadoop.fs.Path;
    public class HDFSFileIfExist {
        public static void master(String[] args){
            try{
                String fileName = "test";
                Configuration conf = new Configuration();
                conf.set("fs.defaultFS", "hdfs://localhost:9000");
                conf.set("fs.hdfs.impl", "org.apache.hadoop.hdfs.DistributedFileSystem");
                FileSystem fs = FileSystem.get(conf);
                if(fs.exists(new Path(fileName))){
                    System.out.println("文件存在");
                }else{
                    System.out.println("文件不存在");
                }
     
            }catch (Exception e){
                e.printStackTrace();
            }
        }
    }
该段代码用来测试在HDFS中对应的用户目录下是否存在名为“test”的文件

- 5.编译运行程序

在开始编译运行程序之前，请一定确保Hadoop已经启动运行，如果还没有启动，需要打开一个Linux终端，输入以下命令启动Hadoop：

```
/opt/hadoop/sbin/start-all.sh
```

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114164300131.png" alt="image-20230114164300131" style="zoom:67%;" />

此时有7个进程，还有eclipse程序在运行

现在就可以编译运行上面编写的代码。可以直接点击Eclipse工作界面上部的运行程序的快捷按钮，当把鼠标移动到该按钮上时，在弹出的菜单中选择“Run As”，继续在弹出来的菜单中选择“Java Application”。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114164434325.png" alt="image-20230114164434325" style="zoom:67%;" />

点击界面右下角的“OK”按钮，开始运行程序

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114165233579.png" alt="image-20230114165233579" style="zoom:67%;" />

程序运行结束后，会在底部的“Console”面板中显示运行结果信息。由于目前HDFS的目录下还没有test文件，因此，程序运行结果是“文件不存在”。同时，“Console”面板中还会显示一些类似“log4j:WARN…”的警告信息，可以不用理会。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114165331883.png" alt="image-20230114165331883" style="zoom:80%;" />

- 6.应用程序的部署

  下面介绍如何把Java应用程序生成JAR包，部署到Hadoop平台上运行。首先，在Hadoop安装目录下新建一个名称为myapp的目录，用来存放我们自己编写的Hadoop应用程序，可以在Linux的终端中执行如下命令：

  ```
  cd /opt/hadoop
  sudo mkdir myapp
  ```

  然后，请在Eclipse工作界面左侧的“Package Explorer”面板中，在工程名称“HDFSExample”上点击鼠标右键，在弹出的菜单中选择“Export”.

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114165846461.png" alt="image-20230114165846461" style="zoom:67%;" />

然后，会弹出下图所示界面，在该界面中，选择“Runnable JAR file”，然后，点击“Next>”按钮。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114165934091.png" alt="image-20230114165934091" style="zoom:67%;" />

在该界面中，“Launch configuration”用于设置生成的JAR包被部署启动时运行的主类，需要在下拉列表中选择刚才配置的类“HDFSFileIfExist-HDFSExample”。在“Export destination”中需要设置JAR包要输出保存到哪个目录，比如，这里设置为“/opt/hadoop/myapp/HDFSExample.jar”。在“Library handling”下面选择“Extract required libraries into generated JAR”。然后，点击“Finish”按钮。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114170115552.png" alt="image-20230114170115552" style="zoom:67%;" />

可以忽略该界面的信息，直接点击界面右下角的“OK”按钮，启动打包过程。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114170149517.png" alt="image-20230114170149517" style="zoom:67%;" />

打包过程结束后，会出现一个警告信息界面，可以忽略该界面的信息，直接点击界面右下角的“OK”按钮。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114171008717.png" alt="image-20230114171008717" style="zoom:67%;" />

至此，已经顺利把HDFSExample工程打包生成了HDFSExample.jar。可以到Linux系统中查看一下生成的HDFSExample.jar文件，可以在Linux的终端中执行如下命令：

```
cd /opt/hadoop/myapp
ls
```

![image-20230114171044288](https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114171044288.png)

可以看到，“/opt/hadoop/myapp”目录下已经存在一个HDFSExample.jar文件。现在，就可以在Linux系统中，使用hadoop jar命令运行程序，命令如下：

```
cd /opt/hadoop
java -jar ./myapp/HDFSExample.jar
```

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230114174446255.png" alt="image-20230114174446255" style="zoom: 80%;" />

命令执行结束后，会在屏幕上显示执行结果“文件不存在”，检测HDFS文件是否存在的程序，就顺利部署完成了。

至此，本实验结束啦。开始下一个实验吧。
