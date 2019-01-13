---
title: CCNP-OSPF
date: 2011-03-17
author: admin
category: ccnp
tags: ccnp, cisco, ospf
slug: ccnp-ospf
---

-   基本特征
-   术语解释
    -   自制系统（AS）
    -   邻居表
    -   拓扑表
    -   路由器标志符（RID）
    -   划分区域
    -   指定路由器（DR）和备份指定路由器（BDR）
    -   区域边界路由器（ABR）
    -   自治系统边界路由器（ASBR）
-   分组类型
-   邻接关系
-   度量计算
-   LSAs类型总结
-   汇总路由
-   默认路由
-   网络类型
-   特殊区域
    -   末节（stub）区域
    -   绝对末节区域（totally stub）区域
    -   NSSA（not so stub area）区域
    -   绝对NSSA（totally NSSA）区域
    -   不规则区域
-   身份验证

### 基本特征

开放最短路径优先（OSPF）协议是一种链路状态路由协议，封装于ip数据包中协议号为89，采用组播地址224.0.0.5（所有路由器）和224.0.0.6（DR和BDR）。链路状态路由协议与距离矢量路由协议最大的区别就是他可以了解到整个网络的拓扑结构，然后利用SPF算法根据这个链路状态数据库计算最优路径，而距离矢量路由协议总是相信邻居传来的路由信息。关于链路状态协议最好的解释是商场的地图，每一个地点都有一张已改点为中心到达商场其他地点的最佳路径，这种结构形象地体现了OSPF构建的SPF树。另外OSPF发送限定更新，且只将更新发往受影响的路由器，以较低的频率发送更新（每30min，老化时间为1h）。

### 术语解释

#### 自治系统（AS）

所有运行OSPF的路由器构成了一个自治系统。

#### 邻居表

记录了路由器和相邻路由器建立邻接关系过程的状态，这里区别于EIGRP，并不是所有存在于邻居表中的条目都和本地路由器建立了邻接关系，具体见邻接关系。

#### 拓扑表

也就是链路状态数据库，他记录了OSPF的AS所有链路的状态，是生成路由表的基础。

#### 路由器标志符（RID）

代表每个路由器在OSPF协议中的身份，并且是唯一的。每台路由器发送更新时都要打上自己的RID。RID的确定原则是：1）通过router-id命令来指定；2）选择所有换回接口最大的地址；3）选择所有接口最大的地址。

#### 划分区域

OSPF适合于大型网络，当网络很大时庞大的链路状态数据库以及不断的进行SPF计算会拖慢OSPF收敛。划分区域的优点主要有：由于在区域之间执行路由汇总可以减小路由表的条目；限制拓扑变化的影响范围；减小LSA的泛洪。区域分为骨干区域（area
0）和非骨干区域（area n）

#### 指定路由器（DR）和备份指定路由器（BDR）

在多路访问网络中如果每台路由器都与其他路由器建立邻接关系那么拓扑结构变得很复杂，这时可以在网络中选出一个代表来代表其他路由器，与其他网络上的路由器通信，这个路由器就叫做DR，另外BDR是做备份用的，当DR失效时BDR升级为DR。选DR原则：优先选择接口优先级高（数字大）的，如果优先级相同就选择RID最大的。关于DR也有一个比喻：一群人坐在一间屋子开会，如果大家你一句我一句就会很混乱，这时大家选一名代表，谁有事就告诉代表，然后代表把事情传递给大家，这样可以很好的提高效率。

#### 区域边界路由器（ABR）

连接OSPF的不同区域的路由器，ABR让两个区域可以了解彼此的网络。

#### 自治系统边界路由器（ASBR）

连接OSPF自治系统和其他网络的路由器，在ASBR上可以通过重定向把其他路由导入到OSPF中。

### 分组类型

OSPF的分组类型有5种，它们的名称和功能如下表：

  ------ ----------------- -------------------------------------------
  类型   名称              说明
  1      hello             用于建立邻接关系
  2      DBD数据库描述     检查数据库是否同步
  3      LSR链路状态请求   向邻居请求链路状态记录
  4      LSU链路状态更新   响应请求的链路状态记录，包含一个或多个LSA
  5      LSack             对其他数据包的确认
  ------ ----------------- -------------------------------------------

### 邻接关系

OSPF中两台路由器相互交换链路信息要先建立邻接关系，这里的邻接关系要区别于邻居关系：当两台路由器相互交换hello包就建立了邻居关系，而只有交换了LSA才算是建立了邻接关系。下面是建立邻接关系的详细过程：AB两台路由器开启OSPF，当AB收到的hello包中包含自己时连台路由器相当于建立邻居关系，称作为2way状态；然后下一步因为要交换DBD包所以要协调一个主从关系，这时进入Exstart状态，RID大的作为主路由器小的作为从路由器；然后进入Exchange状态交换DBD，DBD是链路状态信息的简要概述，可以类比书的目录；接着双方根据收到的LSR包响应响应的链路信息，这一阶段称为loading；最后链路状态数据库达到收敛也就是full状态。

注意：1）在建邻接关系时如果网络是MA网络则要进行选DR和BDR过程，选举完成后的状态是，所有路由器都与DR和BDR建立邻接关系（full）而与其他路由器保持2way状态。2）建立邻居要满足的条件：hello和dead时间一致；AS号一致；身份验证，stub区域标记一致

### 度量计算

OSPF的度量称作cost，仅考虑带宽，计算公式：10E8/bw（bitps）

注意带宽是除接口带宽，单位是bitps

### LSAs类型总结

由于OSPF有不同的区域，而且区域内还有不同角色的路由器，要让这些路由器通信就要构建不同种类的LSAs以达到特定目的，下表是对六种LSA的总结（主要包括通告路由器，传播范围，包含内容三部分）：

  ------ ------------------ ------------ -------------- ----------------------
  种类   名称               通告路由器   传播范围       内容
  1      router lsa         RID          本区域内       拓扑信息和路由
  2      network lsa        DR           本区域内       本网络内的拓扑信息
  3      summary lsa        ABR\*        整个自治系统   域间路由
  4      summary ASB lsa    ABR\*        整个自治系统   到达ASBR的路由
  5      external lsa       ASBR         整个自治系统   域外路由（重定向）
  7      NSSA lsa（暂时）   ASBR         整个自治系统   在NSSA区域传域外路由
  ------ ------------------ ------------ -------------- ----------------------

注意：1）在通告路由器一栏凡是打\*的表示通告路由器随区域改变而改变；2）135分别用于传播域内，域间和域外路由；3）关于NSSA留待特殊区域解释。

### 汇总路由

汇总可以减少传播的路由条目，减轻CPU负载等。默认OSPF不执行任何的自动汇总，所以要手工汇总。可以汇总的地方有两个：一个是区域边界路由器ABR，汇总一个区域内的路由；一个是自治系统边界路由器ASBR，汇总外部路由。

### 默认路由

OSPF配默认路由的步骤：1）确保本地路由器有默认路由；2）在进程中通告默认路由：default-information
originate

### 网络类型

首先要搞清楚网络类型的作用，OSPF不仅要考虑网络的结构还要考虑二层链路的特性，不同的网络类型就是满足不同的二层链路介质需求而设计的。下表列举了六种OSPF网络类型，以及工作在这些网络类型下的行为：

  --------------------- --------------------- ----------- ------ ------------- ----------------
  网络类型              默认接口              hello时间   选DR   邻接关系      适用类型
  loopback              loopback              无          否     无            loopback（32）
  point-to-point        serial/FR’s p2p sub   10          否     hello包自动   串口/子接口
  broadcast             ethernet              10          是     hello包自动   以太口
  non-broadcast         FR’s phy/sub          30          是     手工指定      帧中继
  point-to-multipoint   -----\*               30          否     hello包自动   广播星形拓扑
  p2mp nonbroadcast     -----\*               30          否     手工指定      非广播星形
  --------------------- --------------------- ----------- ------ ------------- ----------------

注意：1）point-to-multipoint和point-to-multipoint
non-broadcast两种网络默认不对应任何接口；2）凡是非广播的网络类型都需要手工指定邻居，指定方法是在进程下配neighbour
ipaddr；3）可以通过修改hello-interval让工作在不同网络类型的接口建邻居4）帧中继点到点子接口默认网络类型是point-to-point，点到多点的类型是non-broadcast，物理接口的网络类型是non-broadcast，所以默认OSPF不能工作在帧中继网络中，所以要修改网络类型，最简单有效的方式是在支持broadcast的链路上配point-to-multipoint网络类型，既不需要手工配邻居也不需要选举DR。

### 特殊区域

#### 末节（stub）区域

如果一个区域只与主干区域相连且没有ASBR那么这个区域内就不需要有外部路由，仅有一条默认路由就可以了。

#### 绝对末节区域（totally stub）区域

在末节区域的基础上再去掉域间路由，也用一条指向ABR的默认路由代替，这样更精简了路由表。配置时no-summary参数只需要加在ABR上。

#### NSSA（not so stub area）区域

NSSA区域与stub区域的唯一不同是它可以包括ASBR也就是这个区域内可以传播外部路由，那么问题就出现了，你还不能传播5类LSA还需要传播外部路由给其他区域，解决办法就是再添加7类路由这样既传递了外部路由也保持着NSSA区域的规则，7类路由就用在这种特定的场合而且在NSSA的ABR上7类被转换成5类法非其他区域，也就是7类LSA仅存在于NSSA网络中。

#### 绝对NSSA（totally NSSA）区域

与stub和绝对stub区域的关系一样，绝对NSSA不传播域间路由，直接用默认路由代替。

#### 不规则区域

区域不与主干区域相连或者主干区域被其他区域分割开的解决办法有如下三种：1）多进程双向重分布；2）通过打隧道（tunnel）来延长主干区域的范围实现区域连接；3）虚链路，通过ABR之间建立虚链路来连接区域。

### 身份验证

从密钥的角度讲有明文认证和md5认证，从认证的对象来讲有接口认证，区域认证和虚链路认证。可以理解为区域认证就是批量接口认证，所有归到特定区域内的接口都被认证。如果配置了区域认证，那么虚链路也包含在内被认证，所以在另一端也要配置认证才能保持虚链路的畅通。

 

### 小特性（feathers）

1）
E1和E2外部路由的区别：就在metric值的计算上，E2类型的外部路由被重定向到自治系统内后metric值不再增加，而E1类型继续累加自治系统内的metric，另外重定向到OSPF的外部路由的默认metric（seed
metric）值也可以修改。

2）
因为有些链路带宽已经超过了100M，这时计算的metric就不那么准确（100M和1000M的metric都是1）可以修改参考带宽以修改metric值，也可以直接修改链路的cost值。

3）
当在OSPF中通告换回口时其子网掩码总是32位，确保最佳路由，因为逻辑接口就这一个地址。

 