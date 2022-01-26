# Chapter2 大数据处理架构Hadoop

> 王洲烽，shenhao

## 2.0 Hadoop的前世今生 

&emsp;&emsp;本部分为先导内容，主要介绍Hadoop的发展历程与各大互联网巨头的爱恨情仇，各位小伙伴不用担心，至少这一部分是轻松愉快的，哈哈哈，帮助大家了解大数据处理架构**Hadoop**！！！  

### 在很久很久以前\~\~\~\~ {docsify-ignore}

> &emsp;&emsp;谈到大数据，就不得不提一嘴全球最大的搜索引擎公司：**Google**

&emsp;&emsp;“Google来源于”“Googol”一词。“Googol”指的是10的100次幂（方），代表互联网上的海量资源。公司创建之初，肖恩·安德森在搜索该名字是否已经被注册时，将“Googol”误打成了“Google”。Google搜索引擎主要的搜索服务，包括网页、图片、音乐、视频、地图、新闻、问答，另外尖端科技还有谷歌火星、谷歌月球、谷歌自动驾驶汽车、智能家居、生物科技、生命科学、元宇宙等。  
&emsp;&emsp;作为一个码农，必须得承认，Google的伟大是目前国内多家互联网公司无法比拟的，至少在学术研究方面。Google可以说是在分布式系统方面的领军企业。Google在2004年提出MapReduce框架，颠覆了整个计算机界，以至于后来的风靡一时、目前在国内使用的Hadoop系统，也是以此为基础发展而来。**在接下来几年的时间，Google陆续发表了各种先进的操作系统，引领着整个世界的分布式系统发展，能够达到处理每秒PB级的数据。**  
&emsp;&emsp;数据不会说谎，这家1998年才成立的高科技公司，用了十几年，做出了几十年的成绩。伟大需要用时间去评判，需要影响力的积累，Google现在可能不能被称之为伟大。**但是我们有理由相信，如果Google一直坚持不作恶的原则，未来一定会在人类科技及生活的发展历史上画下浓墨重彩的一笔。**

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.0.1.png" style="zoom:67%;" /></center>

------

> &emsp;&emsp;无独有偶，一位名叫**Doug Cutting**的美国工程师，也迷上了搜索引擎。他做了一个用于文本搜索的函数库（姑且理解为软件的功能组件），命名为**Lucene**。

&emsp;&emsp;Lucene的目的是为软件开发人员提供一个简单易用的工具包，以方便在目标系统中实现全文检索的功能，或者是以此为基础，建立起完整的全文检索引擎。Lucene在全文检索领域是一个经典的祖先，现在很多检索引擎都是在其基础上创建的，思想是相通的。  

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.0.2.png" style="zoom:67%;">
<br/><div style="color:orange; border-bottom: 1px solid #d9d9d9;display: inline-block;color: #000;padding: 2px; text-align: center;">左为Doug Cutting，右为Lucene的LOGO</div></center>

&emsp;&emsp;**Lucene**是用**JAVA**写成的，目标是为各种中小型应用软件加入全文检索功能。因为好用而且开源（代码公开），非常受程序员们的欢迎。  
&emsp;&emsp;早期的时候，这个项目被发布在**Doug Cutting**的个人网站和**SourceForge**（一个开源软件网站）。后来，**2001**年底，**Lucene**成为**Apache**软件基金会**jakarta**项目的一个子项目。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.0.3.png" style="zoom:67%;" />
<br/><div style="color:orange; border-bottom: 1px solid #d9d9d9;display: inline-block;color: #000;padding: 2px; text-align: center;">Apache软件基金会的LOGO，搞IT的应该都认识</div></center>

> &emsp;&emsp;**Apache**软件基金会是专门为支持开源软件项目而办的一个非盈利性组织。它作为一个群体（或者社区）交流技术、维护软件的媒介，把代码重写与维护的工作有效组织起来。这些开发者们逐渐地把他们这个群体称为“Apache组织”，把这个经过不断修正并改善的服务器软件命名为Apache服务器。

&emsp;&emsp;这个命名是根据北美当地的一支**印第安部落**而来，这支部落以高超的军事素养和超人的忍耐力著称，19世纪后半期对侵占他们领土的入侵者进行了反抗。为了对这支印第安部落表示敬仰之意，取该部落名称（Apache）作为服务器名。但一提到这个命名，这里还有一段广为流传的故事。因为这个服务器是在NCSA HTTPd服务器的基础之上，通过众人努力，不断地修正、打补丁**（Patchy）**的产物，被戏称为“*A Patchy Server*”（一个补丁服务器）。在这里，因为“A Patchy”与“Apache”是谐音，故最后正式命名为“Apache Server”。  

------

> &emsp;&emsp;**2004**年，**Doug Cutting**再接再励，在**Lucene**的基础上，和**Apache**开源伙伴**Mike Cafarella**合作，开发了一款可以代替当时的主流搜索的开源搜索引擎，命名为**Nutch**。

&emsp;&emsp;**Nutch**是一个建立在**Lucene**核心之上的网页搜索应用程序，可以开箱即用。它在**Lucene**的基础上加了网络爬虫和一些网页相关的功能，目的就是从一个简单的站内检索推广到全球网络的搜索上，就像**Google**一样。**Nutch**在业界的影响力比**Lucene**更大。  

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.0.4.png" style="zoom:67%;" /></center>

&emsp;&emsp;相对于那些商用的搜索引擎，Nutch作为开放源代码的搜索引擎，会更加透明，更值得大家信赖。所有主流的搜索引擎都采用私有的排序算法，而不会解释为什么一个网页会排在一个特定的位置。除此之外，有的搜索引擎依照网站所付的费用，而不是根据它们本身的价值进行排序。与它们不同，Nutch没有什么需要隐瞒，也没有动机去扭曲搜索的结果。Nutch将尽自己最大的努力为用户提供最好的搜索结果。（比如百度搜索，有时候前几条全是广告QAQ哈哈哈哈）  
&emsp;&emsp;大批网站采用了**Nutch**平台，大大降低了技术门槛，使低成本的普通计算机取代高价的**Web**服务器成为可能。甚至有一段时间，在硅谷有了一股用**Nutch**低成本创业的潮流。  
&emsp;&emsp;随着时间的推移，无论是**Google**还是**Nutch**，都面临搜索对象“体积”不断增大的问题。尤其是**Google**，作为互联网搜索引擎，需要存储大量的网页，并不断优化自己的搜索算法，提升搜索效率。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.0.5.png" style="zoom:67%;" /></center>

### 后来的后来\~\~\~\~ {docsify-ignore}

> &emsp;&emsp;在这个过程中，**Google**确实找到了不少好办法，并且无私地分享了出来。

&emsp;&emsp;**2003**年，**Google**发表了一篇技术学术论文，公开介绍了自己的谷歌文件系统**GFS**（**Google File System**）。这是**Google**公司为了存储海量搜索数据而设计的专用文件系统。  
&emsp;&emsp;第二年，也就是**2004**年，**Doug Cutting**基于**Google**的**GFS**论文，实现了**分布式文件存储系统**，并将它命名为**NDFS**（**Nutch Distributed File System**）。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.0.6.png" style="zoom:67%;" /></center>

&emsp;&emsp;还是**2004**年，**Google**又发表了一篇技术学术论文，介绍自己的**MapReduce**编程模型，主要用于大规模数据集（大于**1TB**）的并行分析运算。  
&emsp;&emsp;第二年（**2005**年），**Doug Cutting**又基于**MapReduce**，在**Nutch**搜索引擎实现了上述功能。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.0.7.png" style="zoom:67%;" /></center>

&emsp;&emsp;**2006**年，当时依然很厉害的**Yahoo**（雅虎）公司，招安了**Doug Cutting**。  
&emsp;&emsp;雅虎这个名字对于现在的年轻人来说可能并不熟悉，但是它在70、80后一代中可是家喻户晓。雅虎创始人杨致远是那个时代年轻人心中的偶像，是中国互联网的领路人，马云的贵人和好友。雅虎是门户网站形式的创造者，搜索引擎的开拓者，它引领了世界互联网行业的发展！

> &emsp;&emsp;一些学者曾做出评价：“Internet有朝一日将改变整个世界，但若没有Yahoo，恐怕连门还摸不着呢”，这句评价雅虎当之无愧！

&emsp;&emsp;这里要补充说明一下雅虎招安**Doug**的背景：在**2004**年之前，作为互联网开拓者的雅虎，是使用**Google**搜索引擎作为自家搜索服务的。在**2004**年开始，雅虎放弃了**Google**，开始自己研发搜索引擎。所以......  

### Hadoop的诞生！！！{docsify-ignore}

&emsp;&emsp;或许是为了给新上任的自己先冲点业绩，加盟**Yahoo**之后，**Doug Cutting**将**NDFS**和**MapReduce**进行了升级改造，并重新命名为**Hadoop**（**NDFS**也改名为**HDFS**，全称是**Hadoop Distributed File System**）。  
&emsp;&emsp;这就是后来大名鼎鼎的大数据框架系统**Hadoop**的由来。而**Doug Cutting**，则被人们称为**Hadoop**之父。  

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.0.8.png" /></center>

&emsp;&emsp;**Hadoop**这个名字，实际上是**Doug Cutting**他儿子的黄色玩具大象的名字。所以，**Hadoop**的**Logo**，就是一只奔跑的黄色大象。突然感觉到技术大牛的生活就是如此的枯燥且朴实。  

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.0.9.png" style="zoom:67%;" /></center>

------

&emsp;&emsp;我们继续往下说，还是**2006**年，Google又发论文了。这次，介绍了自己的**BigTable**。这是一种分布式数据存储系统，一种用来处理海量数据的非关系型数据库。  
&emsp;&emsp;**Doug Cutting**当然没有放过，在自己的**Hadoop**系统里面，引入了**BigTable**，并命名为**HBase**。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.0.10.png" style="zoom: 80%;" /></center>

&emsp;&emsp;好吧，反正就是紧跟**Google**时代步伐，你出什么，我学什么。所以，**Hadoop**的核心部分，基本上都有**Google**的影子。  

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.0.11.png" style="zoom:80%;" /></center>

&emsp;&emsp;时间来到**2008**年**1**月，**Hadoop**成功上位，正式成为**Apache**基金会的顶级项目。  
&emsp;&emsp;同年**2**月，**Yahoo**宣布建成了一个拥有**1**万个内核的**Hadoop**集群，并将自己的搜索引擎产品部署在上面。  
&emsp;&emsp;**7**月，**Hadoop**打破世界纪录，成为最快排序**1TB**数据的系统，用时**209**秒。此后，**Hadoop**便进入了高速发展期，直至现在。  

> &emsp;&emsp;以上就是Hadoop的先导内容，看完大家应该会对我们即将要学习的内容有一个不错的历史了解，接下来的知识就很硬核啦，大家冲冲冲冲冲冲！！！！！
> &emsp;&emsp;其他的关于Hadoop的版本、历程、花边故事等等凑字数行为就不多介绍了，废话少说，直接上干货。

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.0.12.png" style="zoom: 50%;" /></center>


## 2.1 概述

### 2.1.1 Hadoop简介

&emsp;&emsp;**Hadoop是Apache软件基金会旗下的一个开源分布式计算平台，为用户提供了系统底层细节透明的分布式基础架构。**Hadoop是基于**Java**语言开发的，具有很好的**跨平台特性**，并且可以**部署在廉价的计算机集群**中。  
&emsp;&emsp;Hadoop的核心是**分布式文件系统HDFS**（Hadoop Distributed File System）和 **MapReduce**。HDFS是对谷歌文件系统(Google File System，GFS）的开源实现，是面向普通硬件环境的分布式文件系统，具有较高的读写速度、很好的容错性和可伸缩性，支持大规模数据的分布式存储，其冗余数据存储的方式，很好地保证了数据的安全性。MapReduce是针对谷歌MapReduce的开源实现，允许用户在不了解分布式系统底层细节的情况下开发并行应用程序，采用MapReduce来整合分布式文件系统上的数据，可保证分析和处理数据的高效性。借助于Hadoop，程序员可以轻松地编写分布式并行程序，可将其运行于廉价计算机集群上，完成海量数据的存储与计算。  
&emsp;&emsp;Hadoop被公认为行业大数据标准开源软件，在分布式环境下提供了海量数据的处理能力。几乎所有主流厂商都围绕Hadoop提供开发工具、开源软件、商业化工具和技术服务，如谷歌、雅虎、微软、思科和淘宝等都支持Hadoop。  

### 2.1.2 Hadoop的特性

&emsp;&emsp;Hadoop是一个能够对大量数据进行分布式处理的软件框架，并且是以一种可靠、高效、可伸缩的方式进行数据处理，它具有以下几个方面的特性：

- **高可靠性：**采用冗余数据存储方式，即使一个副本发生故障，其他副本也可以保证正常对外提供服务。Hadoop按位存储和处理数据的能力，值得人们信赖。
- **高效性：**作为并行分布式计算平台，Hadoop采用分布式存储和分布式处理两大核心技术，能够高效地处理PB级数据。Hadoop能够在节点之间动态地移动数据，并保证各个节点的动态平衡，因此处理速度非常快。
- **高可扩展性：**Hadoop的设计目标是可以高效稳定地运行在廉价的计算机集群上，可以扩展到数以千计的计算机节点。
- **高容错性：**采用冗余数据存储方式，自动保存数据的多个副本，并且能够自动将失败的任务进行重新分配。
- **成本低：**Hadoop采用廉价的计算机集群，成本较低，普通用户也很容易用自己的PC上搭建Hadoop运行环境。与一体机、商用数据仓库以及QlikView、Yonghong Z-Suite等数据集市相比，Hadoop是开源的，项目的软件成本因此会大大降低。
- **运行在Linux平台上：**Hadoop是基于Java语言开发的，可以较好地运行在Linux平台上。
- **支持多种编程语言：**Hadoop上的应用程序也可以使用其他语言编写，如C++。

### 2.1.3 Hadoop的应用现状

- 在国外：  
    &emsp;&emsp;**Yahoo**是Hadoop的最大支持者，截至2012年，Yahoo的Hadoop机器总节点数目超过**42000**个，有超过**10万**的核心CPU在运行Hadoop。最大的一个单Master节点集群有**4500**个节点（**每个节点双路4核心CPUboxesw，4×1TB磁盘，16GBRAM**）。总的集群存储容量大于**350PB**，每月提交的作业数目超过**1000万**个，在Pig（大规模数据分析平台）中超过60%的Hadoop作业是使用该平台编写提交的。  
    &emsp;&emsp;**Facebook**使用Hadoop存储内部日志与多维数据，并以此作为报告、分析和机器学习的数据源。目前Hadoop集群的机器节点超过**1400**台，共计**11200**个核心CPU，超过**15PB**原始存储容量，每个商用机器节点配置了**8**核CPU，**12TB**数据存储，主要使用StreamingAPI和JavaAPI编程接口。Facebook同时在Hadoop基础上建立了一个名为Hive的高级数据仓库框架，Hive已经正式成为基于Hadoop的Apache一级项目。此外，还开发了HDFS上的FUSE实现。

- 在国内：  
    &emsp;&emsp;**百度**在2006年就开始关注Hadoop并开始调研和使用，在2012年其总的集群规模达到近十个，单集群超过**2800**台机器节点，Hadoop机器总数有上万台机器，总的存储容量超过**100PB**，已经使用的超过**74PB**，每天提交的作业数目有数千个之多，每天的输入数据量已经超过**7500TB**，输出超过**1700TB**。百度的Hadoop集群为整个公司的数据团队、大搜索团队、社区产品团队、广告团队，以及LBS团体提供统一的计算和存储服务。  
    &emsp;&emsp;**阿里巴巴**的Hadoop集群截至2012年大约有**3200**台服务器，大约**30000**个物理CPU核心，总内存**100TB**，总的存储容量超过**60PB**，每天的作业数目超过**150000**个，每天hivequery查询大于**6000**个，每天扫描数据量约为**7.5PB**，每天扫描文件数约为**4亿**，存储利用率大约为80%，CPU利用率平均为65%，峰值可以达到80%。阿里巴巴的Hadoop集群拥有**150个用户组、4500个集群用户**，为淘宝、天猫、一淘、聚划算、CBU、支付宝提供底层的基础计算和存储服务。  
    &emsp;&emsp;**腾讯**也是使用Hadoop最早的中国互联网公司之一，截至2012年年底，腾讯的Hadoop集群机器总量超过**5000**台，最大单集群约为**2000**个节点，并利用Hadoop-Hive构建了自己的数据仓库系统TDW，同时还开发了自己的TDW-IDE基础开发环境。腾讯的Hadoop为腾讯各个产品线提供基础云计算和云存储服务。  
    &emsp;&emsp;**华为**公司也是Hadoop主要做出贡献的公司之一，排在Google和Cisco的前面，华为对Hadoop的HA方案，以及HBase领域有深入研究，并已经向业界推出了自己的基于Hadoop的大数据解决方案。  

## 2.2 Hadoop的项目架构

&emsp;&emsp;经过多年发展，Hadoop项目不断完善和成熟，目前已经包含多个子项目，逐渐形成一个丰富的Hadoop生态系统。  

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.2.png" style="zoom:50%;" /></center>

- Common  
    &emsp;&emsp;Common是为Hadoop其他子项目提供支持的常用工具，它主要包括**FileSystem、RPC和串行化库**，它们为在廉价的硬件上搭建云计算环境提供了基本的服务，并为运行在该平台上的软件开发提供了所需的API。

- Avro  
    &emsp;&emsp;用于数据库序列化的系统，它提供了丰富的数据结构类型、快速可压缩的二进制数据格式、存储持久性数据的文件集、远程调用RPC的功能和简单的动态语言集成功能，其中代码生成器即不需要读写文件数据，也不需要使用或者实现RPC协议，它只是一个**可选的对静态类型语言的实现**。Hadoop的其他子项目（如HBase和Hive）的客户端与服务端之间的数据传输都采用了Avro。  
    &emsp;&emsp;**Avro系统依赖于模式**，数据的读和写是在模式之下完成的，这样可以减少写入数据的开销，提高序列化的速度并缩减其大小，同时也可以方便动态脚本语言的使用，因为数据连同其模式都是自描述的。  
    &emsp;&emsp;在RPC中，Avro系统客户端和服务器端通过握手协议进行模式交换，因此当客户端和服务器拥有彼此所有的模式时，不同模式下相同命名字段、丢失字段和附加字段等信息的一致性问题得以解决。

- HDFS  
    &emsp;&emsp;Hadoop分布式文件系统（Hadoop Distributed File System，HDFS），它是针对谷歌文件系统（Google File System，GFS）的开源实现。HDFS具有**处理超大数据、流式处理、可以运行在廉价商用服务器上**等优点。它可以通过提供高吞吐率来访问应用程序的数据，适合那些具有超大数据集的应用程序，HDFS放宽了可移植操作系统接口的要求，这样可以**通过流的形式访问文件系统中的数据**，HDFS原本是开源的Apache项目Nutch的基础结构，最后它却成为了Hadoop基础架构之一。

- HBase  
    &emsp;&emsp;HBase是一个**提供高可靠性、高性能、可伸缩、实时读写和分布式的列式数据库**，一般采用HDFS作为其底层数据存储。HBase是针对谷歌BigTable的开源实现。HBase不同于一般的数据库，原因有两个：其一、HBase是一个**适合于非结构化数据存储的数据库**；其二，HBase是**基于列而不是基于行**的存储模式，HBase和BigTable使用相同的数据模型，用户将数据存储在一个表里，一个数据行拥有一个可选择的键和任务数量的列，由于HBase表是疏松的，用户可以给行定义各种不同类型的列，HBase主要用于需要随机访问、实时读写的大数据（Big Data）。

- Pig  
    &emsp;&emsp;Pig是一种数据流语言和运行环境，适合于使用Hadoop和MapReduce的平台来**查询大型半结构化数据集**。虽然MapReduce应用程序的编写不是十分复杂，但毕竟也是需要一定的开发经验。Pig的出现大大简化了Hadoop常见的工作任务，它在MapReduce的基础上创建了更简单的过程语言抽象，为Hadoop应用程序提供了一种更加**接近结构化查询语言(SQL)的接口**。  
    &emsp;&emsp;Pig是一个相对简单的语言，它可以执行语句，因此，当我们需要从大型数据集中搜索满足某个给定搜索条件的记录时，采用Pig要比MapReduce具有明显的优势，前者只需要编写一个简单的脚本在集群中自动并行处理与分发，而后者则需要编写一个单独的MapReduce应用程序。  
    &emsp;&emsp;Pig是一个对大型数据集进行分析、评估的平台，最突出的优势是**它的结构能够经受住高度并行化的检验**，这个特性使得它能够处理大型的数据集。**Pig的底层由编译器组成**，运行的时候会产生一些MapReduce程序序列。

- Sqoop   
    &emsp;&emsp;**Sqoop可以改进数据的互操作性，主要用来在Hadoop和关系数据库之间交换数据。**通过Sqoop，我们可以方便地将数据从MySQL、Oracle、PostgreSQL等关系数据库中导入Hadoop（可以导人 HDFS、HBase或 Hive）、或者将数据从Hadoop导出到关系数据库，使得两者之间的数据迁移变得非常方便。**Sqoop主要通过JDBC（Java DataBase Connectivity）与关系数据库进行交互**，理论上，支持JDBC的关系数据库都可以用Sqoop与Hadoop进行数据交互。Sqoop是专门为大数据集设计的，支持增量更新，可以将新记录添加到最近一次导出的数据源上，或者指定上次修改的时间戳。

- Chukwa  
    &emsp;&emsp;Chukwa是开源的**数据收集系统**，用于**监控和分析**大型分布式系统的数据，Chukwa是在Hadoop的HDFS和MapReduce框架之上搭建的，集成了Hadoop的可扩展性和健壮性，通过HDFS来存储数据，并依赖MapReduce任务处理数据。Chukwa中也附带了灵活且强大的工具，用于显示、监视和分析数据结果，以便更好地利用已收集的数据。

- Zookeeper  
    &emsp;&emsp;Zookeeper是一个为分布式应用所涉及的开源协调服务，主要为用户**提供同步、配置管理、分组和命名等服务**，减轻分布式应用程序所承担的协调任务，Zookeeper的文件系统使用了我们所熟悉的**目录树结构**，Zookeeper是主要使用Java语言编写，同时支持C语言。

## 2.3 Hadoop的安装与应用

> 学了这么多理论，终于要实操了吗，大伙儿冲冲冲啊！！！！

<center><img src="https://gitee.com/shenhao-stu/Big-Data/raw/master/doc_imgs/ch2.3.png" /></center>

### 2.3.1 实验准备

&emsp;&emsp;在开始具体操作之前，首先需要选择一个合适的操作系统。尽管Hadoop本身可以运行在Linux、Windows以及其他一些类UNIX系统（如FreeBSD、OpenBSD、Solaris等）之上，但是，**Hadoop官方真正支持的运行平台只有Linux**。这就导致其他平台在运行Hadoop时，往往需要安装很多其他的包来提供一些Linux操作系统的功能，以配合Hadoop的执行。例如，Windows在运行Hadoop时，需要安装Cygwin等软件。  
&emsp;&emsp;我们这里选择Linux作为Hadoop的运行平台，用于演示在计算机上如何安装Hadoop、运行程序并得到最终结果。当然，其他平台仍然可以作为开发平台使用。对于正在使用Windows操作系统的小伙伴，可以通过在Windows操作系统中安装Linux虚拟机的方式完成实验。  
&emsp;&emsp;在Linux发行版的选择上，我们倾向于使用企业级、稳定的操作系统作为实验的系统环境，同时，考虑到易用性以及是否免费等方面的问题，我们排除了OpenSUSE和RedHat等发行版，最终选择免费的Ubuntu发行版作为推荐的操作系统，大家可以到网络上下载Ubuntu系统镜像文件进行安装（系统镜像下载地址：https://ubuntu.com/download/desktop/thank-you?version=20.04.3&architecture=amd64），✅参考教程：[2020最新版VMware安装Ubuntu20.04教程(巨细)！](https://zhuanlan.zhihu.com/p/141033713)

### 2.3.2 实验内容

**实验环境：**Linux Ubuntu 20.04  
**实验要求：**在Linux系统的虚拟机上安装Hadoop软件，基本安装配置主要包括以下几个步骤：

1. 创建Hadoop用户
2. 安装Java
3. 设置SSH登录权限。
4. 单机安装配置。
5. 伪分布式安装配置。

### 2.3.3 实验步骤

#### 2.3.3.1 创建Hadoop用户

&emsp;&emsp;为方便操作，我们创建一个名为`datawhale`的用户来运行程序，这样可以使不同用户之间有明确的权限区别。同时，也可以防止Hadoop的配置操作影响到其他用户的使用。对于一些大的软件（如 MySQL)，在企业中也常常为其单独创建一个用户。  
&emsp;&emsp;创建用户的命令是`adduser`：会自动为创建的用户指定主目录、系统shell版本，会在创建时输入用户密码。

```shell
sudo adduser datawhale # 创建datawhale用户
```

&emsp;&emsp;切换用户为`datawhale`用户，在该用户环境下进行操作。
```shell
su datawhale # 切换到datawhale用户
```

#### 2.3.3.2 Java的安装

&emsp;&emsp;由于Hadoop本身是使用Java语言编写的，因此Hadoop的开发和运行都需要Java的支持，一般要求Java 6或者更新的版本。对于Ubuntu 20.04本身，系统上可能已经预装了Java 7，JDK版本为openjdk，路径为`/usr/lib/jvm/java-1.7.0-openjdk`，后文中需要配置的 `JAVA_HOME` 环境变量就可以设置为这个值。  
&emsp;&emsp;对于Hadoop而言，采用更为广泛应用的Oracle公司的Java版本，在功能上可能会更稳定一些，因此用户也可以根据自己的爱好安装Oracle版本的Java。在安装过程中，请记住JDK的文件路径，即`JAVA_HOME`的位置，这个路径的设置将用在后文Hadoop的配置文件中，目的是让Hadoop程序可以找到相关的Java工具。  
&emsp;&emsp;比如我们在`/data/hadoop`目录中下载了`jdk-8u161-linux-x64.tar.gz`。

##### 1.安装jdk

&emsp;&emsp;将`/data/hadoop`目录下`jdk-8u161-linux-x64.tar.gz`解压缩到`/opt`目录下。
```shell
sudo tar -xzvf /data/hadoop/jdk-8u161-linux-x64.tar.gz -C /opt
```

&emsp;&emsp;其中，`tar -xzvf` 对文件进行解压缩，-C 指定解压后，将文件放到/opt目录下。  

> **注意：**如果`sudo`命令无法使用，请直接切换到`root`用户，`su root`或`sudo -i`。但要注意，以下步骤需要切换到`datawhale`用户下进行操作：
> - ssh登录权限设置
> - Hadoop伪分布安装中的5、6、7、8、9步骤。

&emsp;&emsp;下面将`jdk1.8.0_161`目录重命名为`java`，执行如下命令：
```shell
sudo mv /opt/jdk1.8.0_161/ /opt/java
```

&emsp;&emsp;修改`java`目录的所属用户：
```shell
sudo chown -R datawhale:datawhale /opt/java
```

##### 2.修改系统环境变量

&emsp;&emsp;打开`/etc/profile`文件，命令如下：
```shell
sudo vim /etc/profile
```

&emsp;&emsp;在该文件末尾，添加如下内容：
```shell
#java
export JAVA_HOME=/opt/java
export PATH=$JAVA_HOME/bin:$PATH
```
&emsp;&emsp;使用`Shift+:`，输入`wq`后回车，保存并关闭编辑器。

&emsp;&emsp;输入以下命令，使得环境变量生效：
```shell
source /etc/profile
```

&emsp;&emsp;执行完上述命令之后，可以通过`JAVA_HOME`目录找到`java`可使用的命令。 通过查看版本号的命令验证是否安装成功，命令如下：
```shell
java -version
```

&emsp;&emsp;执行结果如下：
```shell
java version "1.8.0_161"
Java(TM) SE Runtime Environment (build 1.8.0_161-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.161-b12, mixed mode)
```

#### 2.3.3.3 SSH登录权限设置

**注意：**需要切换为datawhale用户，命令如下：
```shell
su datawhale # 切换为datawhale用户
```

&emsp;&emsp;对于Hadoop的伪分布和全分布而言，Hadoop名称节点（NameNode）需要启动集群中所有机器的Hadoop守护进程，这个过程可以通过SSH登录来实现。Hadoop并没有提供SSH输入密码登录的形式，因此，为了能够顺利登录每台机器，需要将所有机器配置为名称节点，可以通过SSH无密码的方式登录它们。  
&emsp;&emsp;为了实现SSH无密码登录方式，首先需要让`NameNode`生成自己的`SSH`密钥，命令如下：

```shell
ssh-keygen -t rsa # 执行该命令后，遇到提示信息，一直按回车就可以
```

&emsp;&emsp;`NameNode`生成密钥之后，需要将它的公共密钥发送给集群中的其他机器。我们可以将`id_dsa.pub`中的内容添加到需要SSH无密码登录的机器的`~/ssh/authorized_keys`目录下，然后就可以无密码登录这台机器了。对于无密码登录本机而言，可以执行以下命令：  
```shell
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

&emsp;&emsp;或者执行以下命令：  
```shell
cat /home/datawhale/.ssh/id_rsa.pub >> /home/datawhale/.ssh/authorized_keys
```

&emsp;&emsp;这时可以通过`ssh localhost`命令来检测一下是否需要输入密码。 测试ssh连接，看到“sucessful login”，则配置成功，命令如下：  
```shell
ssh localhost
```

#### 2.3.3.4 安装单机版Hadoop

&emsp;&emsp;这里使用的Hadoop版本为3.3.1。下载地址为http://archive.apache.org/dist/hadoop/core/hadoop-3.3.1/hadoop-3.3.1.tar.gz  
&emsp;&emsp;将该文件夹解压后，可以放置到自己喜欢的位置，如`/data/hadoop`文件夹下，注意，文件夹的用户和组必须都为hadoop。

##### 1.安装Hadoop

&emsp;&emsp;将`hadoop-3.3.1.tar.gz`解压缩到`/opt`目录下，命令如下：
```shell
sudo tar -xzvf /data/hadoop/hadoop-3.3.1.tar.gz -C /opt/
```

&emsp;&emsp;为了便于操作，我们也将`hadoop-3.3.1`重命名为`hadoop`，命令如下：
```shell
sudo mv /opt/hadoop-3.3.1/ /opt/hadoop
```

&emsp;&emsp;修改hadoop目录的所属用户和所属组，命令如下
```shell
sudo chown -R datawhale:datawhale /opt/hadoop
```

##### 2.修改系统环境变量

&emsp;&emsp;打开`/etc/profile`文件，命令如下：
```shell
sudo vim /etc/profile
```

&emsp;&emsp;在文件末尾，添加如下内容：
```shell
#hadoop
export HADOOP_HOME=/opt/hadoop
export PATH=$HADOOP_HOME/bin:$PATH
```
&emsp;&emsp;使用`Shift+:`，输入`wq`后回车，保存并关闭编辑器。

&emsp;&emsp;输入以下命令，使得环境变量生效：
```shell
source /etc/profile
```

&emsp;&emsp;通过查看版本号命令验证是否安装成功，命令如下：
```shell
hadoop version
```

&emsp;&emsp;执行结果如下：
```log
Hadoop 3.3.1
Source code repository https://git-wip-us.apache.org/repos/asf/hadoop.git -r c25427ceca461ee979d30edd7a4b0f50718e6533
Compiled by andrew on 2017-12-08T19:16Z
Compiled with protoc 2.5.0
From source with checksum 397832cb5529187dc8cd74ad54ff22
This command was run using /opt/hadoop/share/hadoop/common/hadoop-common-3.3.1.jar
```

##### 3.修改hadoop-env.sh文件配置

&emsp;&emsp;对于单机安装，首先需要更改`hadoop-env.sh`文件，用于配置Hadoop运行的环境变量，命令如下：
```shell
cd /opt/hadoop/
vim etc/hadoop/hadoop-env.sh
```

&emsp;&emsp;在文件末尾，添加如下内容：
```shell
export JAVA_HOME=/opt/java/
```
&emsp;&emsp;使用`Shift+:`，输入`wq`后回车，保存并关闭编辑器。

&emsp;&emsp;Hadoop文档中还附带了一些例子来供我们测试，可以运行`WordCount`的示例，检测一下Hadoop安装是否成功。运行示例的步骤如下：  
1. 在`/opt/hadoop/`目录下新建`input`文件夹，用来存放输入数据；
2. 将`etc/hadoop/`文件夹下的配置文件拷贝至`input`文件夹中；
3. 在`hadoop`目录下新建`output`文件夹，用于存放输出数据；
4. 运行`wordCount`示例
4. 查看输出数据的内容。

&emsp;&emsp;执行命令如下：
```shell
mkdir input
cp etc/hadoop/*.xml input
bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar grep input output 'dfs[a-z.]+'
cat output/*
```

&emsp;&emsp;输出数据结果：
```log
1    dfsadmin
```

&emsp;&emsp;这意味着，在所有的配置文件中，只有一个符合正则表达式`dfs[a-z.]+`的单词，输出结果正确。

#### 2.3.3.5 Hadoop伪分布式安装

&emsp;&emsp;伪分布式安装是指在一台机器上模拟一个小的集群。当Hadoop应用于集群时，不论是伪分布式还是真正的分布式运行，都需要通过配置文件对各组件的协同工作进行设置。  
&emsp;&emsp;对于伪分布式配置，我们需要修改`core-site.xml`、`hdfs-site.xml`、`mapred-site.xml`和`yarn-site.xml`这4个文件。

##### 1.修改core-site.xml文件配置

&emsp;&emsp;打开`core-site.xml`文件，命令如下：
```shell
vim /opt/hadoop/etc/hadoop/core-site.xml
```

&emsp;&emsp;添加下面配置到`<configuration>与</configuration>`标签之间，添加内容如下：
```html
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```
&emsp;&emsp;使用`Shift+:`，输入`wq`后回车，保存并关闭编辑器。		

&emsp;&emsp;可以看出，`core-site.xml`配置文件的格式十分简单，`<name>`标签代表了配置项的名字，`<value>`项设置的是配置的值。对于该文件，我们只需要在其中指定HDFS的地址和端口号，端口号按照官方文档设置为9000即可。

##### 2.修改hdfs-site.xml文件配置

&emsp;&emsp;打开`hdfs-site.xml`文件，命令如下：
```shell
vim /opt/hadoop/etc/hadoop/hdfs-site.xml
```

&emsp;&emsp;添加下面配置到`<configuration>与</configuration>`标签之间，添加内容如下：
```html
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```
&emsp;&emsp;使用`Shift+:`，输入`wq`后回车，保存并关闭编辑器。	

&emsp;&emsp;对于`hdfs-site.xml`文件，我们设置`replication`值为1，这也是Hadoop运行的默认最小值，用于设置HDFS文件系统中同一份数据的副本数量。

##### 3.修改mapred-site.xml文件配置

&emsp;&emsp;打开`mapred-site.xml`文件，命令如下：
```shell
vim /opt/hadoop/etc/hadoop/mapred-site.xml
```

&emsp;&emsp;添加下面配置到`<configuration>与</configuration>`标签之间，修改后的`mapred-site.xml`文件内容如下：
```html
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>mapreduce.application.classpath</name>
        <value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
    </property>
</configuration>
```
保存并关闭编辑器修改。

##### 4.修改yarn-site.xml文件配置

```shell
vim /opt/hadoop/etc/hadoop/yarn-site.xml
```

添加下面配置到`<configuration>与</configuration>`标签之间。

```html
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
    </property>
</configuration>
```
&emsp;&emsp;使用`Shift+:`，输入`wq`后回车，保存并关闭编辑器。	

&emsp;&emsp;对于本书的实验，通过上述配置后，就已经满足运行要求了。这里再给出一个官方文档的详细地址，感兴趣的小伙伴可以查看文档配置的其他项（网址如下：https://hadoop.apache.org/docs/stable ）

##### 5.格式化分布式文件系统

**注意：**需要切换为datawhale用户，命令如下：
```shell
su datawhale
```

&emsp;&emsp;在配置完成后，首先需要初始化文件系统，由于Hadoop的很多工作是在自带的 HDFS文件系统上完成的，因此，需要将文件系统初始化之后才能进一步执行计算任务。执行初始化的命令如下：
```shell
hdfs namenode -format
```

&emsp;&emsp;在看到运行结果中出现“successfully formatted”之后，则说明初始化成功。

##### 6.启动Hadoop
&emsp;&emsp;使用如下命令启动Hadoop的所有进程，可以通过提示信息得知，所有的启动信息都写入到对应的日志文件。如果出现启动错误，则可以查看相应的错误日志。
```shell
/opt/hadoop/sbin/start-all.sh
```

##### 7.查看Hadoop进程

&emsp;&emsp;运行之后，输入`jps`命令可以查看所有的`Java`进程。正常启动后，可以得到如下类似结果：
```log
2072524 SecondaryNameNode
2073019 ResourceManager
2072169 NameNode
2073158 NodeManager
2072291 DataNode
2073923 Jps
```

##### 8.Hadoop WebUI管理界面

&emsp;&emsp;此时，可以通过`http://localhost:8088`访问Web界面，查看Hadoop的信息。

##### 9.测试HDFS集群以及MapReduce任务程序

&emsp;&emsp;利用Hadoop自带的`WordCount`示例程序进行检查集群，并在主节点上进行如下操作，创建执行MapReduce任务所需的HDFS目录：
```shell
hadoop fs -mkdir /user
hadoop fs -mkdir /user/datawhale
hadoop fs -mkdir /input
```

&emsp;&emsp;创建测试文件，命令如下：
```shell
vim /home/datawhale/test
```

&emsp;&emsp;在`test`文件中，添加以下内容：
```log
Hello world!
```
&emsp;&emsp;使用`Shift+:`，输入`wq`后回车，保存并关闭编辑器。	

&emsp;&emsp;将测试文件上传到Hadoop HDFS集群目录，命令如下：
```shell
hadoop fs -put /home/datawhale/test /input
```

&emsp;&emsp;执行wordcount程序，命令如下：
```shell
hadoop jar /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar wordcount /input /out
```

&emsp;&emsp;通过以下命令，查看执行结果：
```shell
hadoop fs -ls /out
```

&emsp;&emsp;执行结果如下：
```log
Found 2 items
-rw-r--r--    1 root supergroup       0 time /out/_SUCCESS
-rw-r--r--    1 root supergroup      17 time /out/part-r-00000 
```
&emsp;&emsp;可以看到，结果中包含`_SUCCESS`文件，表示Hadoop集群运行成功。

&emsp;&emsp;查看具体的输出结果，命令如下：
```shell
hadoop fs -text /out/part-r-00000
```
&emsp;&emsp;输出结果如下：
```log
Hello   1
world!  1
```

### 2.3.4 Tips

✅ **Hadoop3.3.1集群模式**安装请参考： [Hadoop集群模式安装.md](https://gitee.com/shenhao-stu/Big-Data/blob/master/experiments/Hadoop集群模式安装.md) 和 [Hadoop集群模式安装节点.md](https://gitee.com/shenhao-stu/Big-Data/blob/master/experiments/Hadoop集群模式安装节点.md)。	

✅ **官网安装**请参考：[Hadoop单节点集群安装](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html#Execution)

✅ **安装问题**：[Hadoop中DataNode没有启动](https://www.cnblogs.com/mtime2004/p/10008325.html)  

>`VERSION`参考查询目录：`tmp/hadoop-datawhale/dfs/data/current/VERSION`

## 2.4 本章小结

&emsp;&emsp;Hadoop被视为事实上的大数据处理标准，本章主要介绍了Hadoop的发展历程，并阐述了Hadoop的高可靠性、高效性、高可扩展性、高容错性、成本低、运行在Linux平台上、支持多种编程语言等特性。  
&emsp;&emsp;Hadoop目前已经在各个领域得到了广泛的应用，如雅虎、Facebook、百度、淘宝、网易等公司都建立了自己的Hadoop集群。  
&emsp;&emsp;经过多年发展，Hadoop项目已经变得非常成熟和完善，包括Common、Avro、Zookeeper、HDFS、MapReduce、HBase、Hive、Chukwa、Pig等子项目。其中，HDFS和 MapReduce是Hadoop的两大核心组件。  
&emsp;&emsp;本章最后通过一个实验，讲解了如何在Linux系统下安装和配置Hadoop，并通过`WordCount`程序验证已部署的Hadoop集群，这个部分是后续章节实践环节的基础。