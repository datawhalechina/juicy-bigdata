<center><h1>Mapreduce实例——WordCount</h1></center>


[TOC]

## Mapreduce实例——WordCount

### 实验环境

1.Linux Ubuntu 22.04

2.hadoop3.3.1

3.eclipse4.7.0

### 实验内容

在安装了Hadoop和eclipse的Linux系统服务器上，完成WordCount实验。

### 实验步骤

---

#### 1.在Eclipse中创建项目

首先，启动Eclipse，启动以后会弹出如下图所示界面，提示设置工作空间（workspace）。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117200805431.png" alt="image-20230117200805431" style="zoom: 67%;" />

可以直接采用默认的设置“/home/hadoop/workspace”，点击“OK”按钮。 Eclipse启动以后，呈现的界面如下图所示。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117200819950.png" alt="image-20230117200819950" style="zoom:80%;" />

选择“File–>New–>Java Project”菜单，开始创建一个Java工程，弹出如下图所示界面。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117200830364.png" alt="image-20230117200830364" style="zoom:80%;" />

  在“Project name”后面输入工程名称“WordCount”，选中“Use default location”，让这个Java工程的所有文件都保存到“/home/hadoop/workspace/WordCount”目录下。在“JRE”这个选项卡中，选择当前已经安装好的JDK：java。然后，点击界面底部的“Next>”按钮。

 

#### 2.为项目添加需要用到的JAR包

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117200838895.png" alt="image-20230117200838895" style="zoom: 80%;" />

在这个界面中加载该Java工程所需要用到的JAR包，这些JAR包中包含了与Hadoop相关的Java API。点击界面中的“Libraries”选项卡，然后，点击界面右侧的“Add External JARs…”按钮，弹出如下图所示界面。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117200849515.png" alt="image-20230117200849515" style="zoom:80%;" />

为了编写一个MapReduce程序，一般需要向Java工程中添加以下JAR包：

```
   1、“/usr/local/hadoop/share/hadoop/common”目录下的hadoop-common-3.1.3.jar和haoop-nfs-3.1.3.jar
   2、“/usr/local/hadoop/share/hadoop/common/lib”目录下的所有JAR包
   3、“/usr/local/hadoop/share/hadoop/mapreduce”目录下的所有JAR包
   4、“/usr/local/hadoop/share/hadoop/mapreduce/lib”目录下的所有JAR包
```

 全部添加完毕以后，就可以点击界面右下角的“Finish”按钮，完成Java工程WordCount的创建。具体如下图所示。 

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117200903526.png" alt="image-20230117200903526" style="zoom:80%;" />

#### 3.编写Java应用程序

下面编写一个Java应用程序，即WordCount.java。在Eclipse工作界面左侧的“Package Explorer”面板中（如下图所示），找到刚才创建好的工程名称“WordCount”，然后在该工程名称上点击鼠标右键，在弹出的菜单中选择“New–>Class”菜单，再选择“New–>Class”菜单以后会出现如下图所示界面。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201004151.png" alt="image-20230117201004151" style="zoom:80%;" />

在该界面中，只需要在“Name”后面输入新建的Java类文件的名称，这里采用名称“WordCount”，其他都可以采用默认设置。然后，点击界面右下角“Finish”按钮，出现如下图所示界面。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201012165.png" alt="image-20230117201012165" style="zoom:80%;" />

  可以看出，Eclipse自动创建了一个名为“WordCount.java”的源代码文件，清空该文件里面的代码，然后在该文件中输入完整的词频统计程序代码，具体如下：

```
import java.io.IOException;  
import java.util.Iterator;  
import java.util.StringTokenizer;  
import org.apache.hadoop.conf.Configuration;  
import org.apache.hadoop.fs.Path;  
import org.apache.hadoop.io.IntWritable;  
import org.apache.hadoop.io.Text;  
import org.apache.hadoop.mapreduce.Job;  
import org.apache.hadoop.mapreduce.Mapper;  
import org.apache.hadoop.mapreduce.Reducer;  
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;  
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;  
import org.apache.hadoop.util.GenericOptionsParser;  
public class WordCount {  
    public WordCount() {  
    }  
     public static void master(String[] args) throws Exception {  
        Configuration conf = new Configuration();  
        String[] otherArgs = (new GenericOptionsParser(conf, args)).getRemainingArgs();  
        if(otherArgs.length < 2) {  
            System.err.println("Usage: wordcount <in> [<in>...] <out>");  
            System.exit(2);  
        }  
        Job job = Job.getInstance(conf, "word count");  
        job.setJarByClass(WordCount.class);  
        job.setMapperClass(WordCount.TokenizerMapper.class);  
        job.setCombinerClass(WordCount.IntSumReducer.class);  
        job.setReducerClass(WordCount.IntSumReducer.class);  
        job.setOutputKeyClass(Text.class);  
        job.setOutputValueClass(IntWritable.class);   
        for(int i = 0; i < otherArgs.length - 1; ++i) {  
            FileInputFormat.addInputPath(job, new Path(otherArgs[i]));  
        }  
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[otherArgs.length - 1]));  
        System.exit(job.waitForCompletion(true)?0:1);  
    }  
    public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {  
        private static final IntWritable one = new IntWritable(1);  
        private Text word = new Text();  
        public TokenizerMapper() {  
        }  
        public void map(Object key, Text value, Mapper<Object, Text, Text, IntWritable>.Context context) throws IOException, InterruptedException {  
            StringTokenizer itr = new StringTokenizer(value.toString());   
            while(itr.hasMoreTokens()) {  
                this.word.set(itr.nextToken());  
                context.write(this.word, one);  
            }  
        }  
    }  
public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {  
        private IntWritable result = new IntWritable();  
        public IntSumReducer() {  
        }  
        public void reduce(Text key, Iterable<IntWritable> values, Reducer<Text, IntWritable, Text, IntWritable>.Context context) throws IOException, InterruptedException {  
            int sum = 0;  
            IntWritable val;  
            for(Iterator i$ = values.iterator(); i$.hasNext(); sum += val.get()) {  
                val = (IntWritable)i$.next();  
            }  
            this.result.set(sum);  
            context.write(key, this.result);  
        }  
    }  
} 

```

#### 4.编译打包程序

现在编译上面编写的代码。可以直接点击Eclipse工作界面上部的运行程序的快捷按钮，当把鼠标移动到该按钮上时，在弹出的菜单中选择“Run as”，继续在弹出来的菜单中选择“Java Application”，如下图所示。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201028788.png" alt="image-20230117201028788" style="zoom:80%;" />

然后，会弹出如下图所示界面。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201036533.png" alt="image-20230117201036533" style="zoom:67%;" />

点击界面右下角的“OK”按钮，开始运行程序。程序运行结束后，会在底部的“Console”面板中显示运行结果信息（如下图所示）。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201044062.png" alt="image-20230117201044062" style="zoom:67%;" />

下面把Java应用程序打包生成JAR包，部署到Hadoop平台上运行。现在可以把词频统计程序放在“/opt/hadoop/myapp”目录下。如果该目录不存在，可以使用如下命令创建：

```
cd /opt/hadoop 

mkdir myapp 
```

 

首先，请在Eclipse工作界面左侧的“Package Explorer”面板中，在工程名称“WordCount”上点击鼠标右键，在弹出的菜单中选择“Export”，然后，会弹出如下图所示界面。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201130324.png" alt="image-20230117201130324" style="zoom: 80%;" />

在该界面中，选择“Runnable JAR file”，然后，点击“Next>”按钮，弹出如下图所示界面。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201144602.png" alt="image-20230117201144602" style="zoom:80%;" />

在该界面中，“Launch configuration”用于设置生成的JAR包被部署启动时运行的主类，需要在下拉列表中选择刚才配置的类“WordCount-WordCount”。在“Export destination”中需要设置JAR包要输出保存到哪个目录，这里设置为“/usr/local/hadoop/myapp/WordCount.jar”。在“Library handling”下面选择“Extract required libraries into generated JAR”。然后，点击“Finish”按钮，会出现如下图所示界面。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201153013.png" alt="image-20230117201153013" style="zoom:67%;" />

  可以忽略该界面的信息，直接点击界面右下角的“OK”按钮，启动打包过程。打包过程结束后，会出现一个警告信息界面，如下图所示。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201159270.png" alt="image-20230117201159270" style="zoom:67%;" />

  可以忽略该界面的信息，直接点击界面右下角的“OK”按钮。至此，已经顺利把WordCount工程打包生成了WordCount.jar。

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201206005.png" alt="image-20230117201206005" style="zoom:80%;" />

#### 5.运行程序

在运行程序之前，需要启动Hadoop，命令如下：

```
cd /opt/hadoop/sbin 

./start-all.sh 
```

 

在启动Hadoop之后，需要首先删除HDFS中与当前Linux用户datawhale对应的input和output目录（即HDFS中的“/user/datawhale/input”和“/user/datawhale/output”目录），这样确保后面程序运行不会出现问题，具体命令如下：

```
cd /opt/hadoop 

./bin/hdfs dfs -rm -r /input 

./bin/hdfs dfs -rm -r /output
```

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201232946.png" alt="image-20230117201232946" style="zoom:67%;" />

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201238052.png" alt="image-20230117201238052" style="zoom:67%;" />

然后，再在HDFS中新建与当前Linux用户datawhale对应的input目录，即“/user/ datawhale /input”目录，具体命令如下：

```
./bin/hdfs dfs -mkdir /input 
```

然后，把之前在第7.1节中在Linux本地文件系统中新建的两个文件wordfile1.txt和wordfile2.txt（假设这两个文件位于“/opt/hadoop/mytext”目录下，并且里面包含了一些英文语句），上传到HDFS中的“/user/datawhale/input”目录下，命令如下：

```
./bin/hdfs dfs -put /opt/hadoop/mytext/wordfile1.txt /input 

./bin/hdfs dfs -put /opt/hadoop/mytext/wordfile2.txt /input 
```

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201341148.png" alt="image-20230117201341148" style="zoom: 67%;" />

如果HDFS中已经存在目录“/user/hadoop/output”，则使用如下命令删除该目录：

```
./bin/hdfs dfs -rm -r /user/hadoop/output 
```

现在，就可以在Linux系统中，使用hadoop jar命令运行程序，命令如下：

```
./bin/hadoop jar ./myapp/WordCount.jar /input /output
```

上面命令执行以后，当运行顺利结束时，屏幕上会显示类似如下的信息：

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201504791.png" alt="image-20230117201504791" style="zoom:80%;" />

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201517246.png" alt="image-20230117201517246" style="zoom:80%;" />

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201527189.png" alt="image-20230117201527189" style="zoom:80%;" />

词频统计结果已经被写入了HDFS的“/user/datawhale/output”目录中，可以执行如下命令查看词频统计结果：

```
./bin/hdfs dfs -cat /output/* 
```

上面命令执行后，会在屏幕上显示如下词频统计结果：

<img src="https://github.com/wzfer/picgo/raw/master/juicy-bigdata/experiments_imgs/image-20230117201621438.png" alt="image-20230117201621438" style="zoom:80%;" />

至此，词频统计程序顺利运行结束。需要注意的是，如果要再次运行WordCount.jar，需要首先删除HDFS中的output目录，否则会报错。

 

#### 6.问题与讨论

1、理解Hadoop中MapReduce模块的处理逻辑。编写MapReduce程序，实现单词出现次数统计。统计结果保存到hdfs的output文件夹，并获取统计结果。

2、注意到程序编写时要留意外界的文件是否清空干净，有时程序正确也会因冲突而产生报错

3、编写MapReduce的Java程序时困难重重，整体编写结束后收获颇丰，对整个MapReduce的架构有了更深刻的认识

4、要检查工程文件是否移入相应的位置，内容是否有误写

5、程序崩溃后强制退出程序，删除之前的输出文件，重新执行