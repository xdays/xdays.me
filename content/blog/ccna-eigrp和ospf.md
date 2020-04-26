---
title: CCNA-EIGRP和OSPF
date: 2010-10-31
author: admin
category: network
tags: ['ccna']
slug: ccna-eigrp和ospf
---

增强内部网关路由协议 EIGRP

- 概述
  - 消息格式
  - 消息类型
  - 可靠传输协议
- 邻居关系建立
- 度量计算
- DUAL 算法相关概念
  - 可行距离
  - 报告（通告）距离
  - 后继路由器
  - 可行后继路由器
- 配置和排错

开放最短路径优先协议 OSPF

- 概述
  - 消息格式
  - 消息类型
  - 路由 ID
- 邻接关系建立
- 度量计算
- 迪科斯特拉算法（Dijkstra，或称 SPF）
- 多路访问网络中 DR 和 BDR 选择
- 配置和排错

## 增强内部网关路由协议 EIGRP

### 概述

#### 消息格式

EIGRP 的一大特性是通过协议相关模块（protocol
dependentmodules，PDM）支持多种协议，有 IP，IPv6，IPX，AppleTalk 四种，此处我们只学习 IP 协议相关的。EIGRP 封装于 IP 数据包中，协议类型字段为 0x58，采用三层组播地址 224.0.0.10，二层组播地址为 0100.5e00.000a。下表是数据包格式：

---

帧头 IP 数据包 EIGRP 数据包包头 类型/长度/值（TLV）

---

EIGRP 数据包包头

<table style="text-align: center;" border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td width="189" valign="top">
版本

</td>
<td width="189" valign="top">
操作码

</td>
<td width="189" valign="top">
校验和

</td>
</tr>
<tr>
<td colspan="3" width="568" valign="top">
标志

</td>
</tr>
<tr>
<td colspan="3" width="568" valign="top">
序列号

</td>
</tr>
<tr>
<td colspan="3" width="568" valign="top">
确认

</td>
</tr>
<tr>
<td colspan="3" width="568" valign="top">
自治系统号

</td>
</tr>
<tr>
<td colspan="3" width="568" valign="top">
TLVs

</td>
</tr>
</tbody>
</table>
其中TLVs又分参数TLV，内部路由TLV，外部路由TLV

#### 消息类型

EIGRP 共有 5 种数据包类型，分别是：Hello，更新，查询，响应，确认。这些数据包由协议数据包包头的操作码（opcode）字段来决定

#### 可靠传输协议

因为传输层采用实时传输协议（real time
protocol，RTP），EIGRP 支持可靠和不可靠传输。Hello 数据包采用不可靠传输，其他几种数据包都采用可靠传输，即收到数据包后要进行确认

### 邻居关系建立

邻居关系的建立和维持是通过不断发送 Hello 数据包维持的，一般网络每 5 秒发送一次，dead 时间是 15 秒，对于非广播多路访问网络（NBMA）的发送时间间隔为 60 秒，dead 时间为 180 秒。邻居关系建立的条件有如下三个：

1.  发送和收到 Hello 数据包
2.  具有相同的 AS 号
3.  具有相同的度量（K 值）

### 度量计算

EIGRP 的度量有带宽（bandwidth），延迟（delay），负载（load），可靠性（reliability），虽然最大传输单元（maximum
transport
unit，MTU）不是度量，但是在设置 K 值和路由重定向时需要指定，度量计算公式如下：

---

Metric = （10000000/bandwidth + delay-of-sum/10）\* 256

---

### DUAL 算法

DUAL 的核心是保证了到达目的网络不会出现路由环路

#### 可行距离（feasible distance，FD）

到达目的网络的所有路径中的最佳度量，这条路径会添加到路由表中

#### 报告距离（reported/advertised distance，RD/AD）

只是从不同路由器角度对同一度量的不同称呼，比如路由器 A 发送通告给路由器 B，这个度量对于 A 来说是可行距离，对于 B 来说是通告距离

#### 可行性条件（feasible condition，FD）

当邻居通向特定网络的报告距离比本地路由通向相同网络的可行距离短时，即满足可行性条件

#### 后继路由器（successor）

用于转发数据包的邻居路由，具有到达目的网络最小的开销，它会显示在路由表中

#### 可行后继路由器（feasible successor）

满足可行性条件，但是没有当前的后继路由器的报告距离小的邻居路由器

### 配置和排错

#### 配置命令

1.  \#router  eigrp xx  开启 EIGRP，xx 为自治系统号
2.  \#network 192.168.1.0
    0.0.0.255 设置参与路由协议的网络（通配符子网掩码可以表示一个范围的网段，其中 0 表示必须匹配 1 表示不需要匹配）
3.  \#passive-interface
    interface-id 设置不参与路由协议的接口（设置被动接口的接口将也不会发送 Hello 数据包，这一点与 RIP 区分开）
4.  \#no auto-summary 不自动汇总

#### 排错命令

- \#sh ip eigrp neighbour
- \#sh ip eigrp topology
  [all-links]查看拓扑结构，加上 all-links 时不符合可行性条件的条目也会列举出来
- \#debug ip eigrp \*\*查看 eigrp 产生的一些日志信息

## 开放最短路径优先协议 OSPF

### 概述

#### 消息格式

OSPF 包封装于 IP 数据包中，协议代号为 0x59,；采用组播地址 224.0.0.5 和 224.0.0.6，前者代表所有路由器，后者代表 DR 和 BDR

OSPF 分组

---

帧头 IP 数据包 OSPF 数据包包头 数据

---

OSPF 数据包包头

---

版本 类型 分组长度 路由器 ID 区域 ID 校验和 身份验证类型 身份验证

---

#### 消息类型

---

类型 作用
Hello 发现邻居并在他们之间建立邻接（adjacency）关系
数据库描述（DBD） 检查数据库之间是否同步
链路状态请求（LSR） 向另一台路由器请求特定的链路状态
链路状态更新（LSU） 发送请求的链路转台更新
确认（LSAck） 对其他类型的分组确认

---

#### 路由 ID

用来表示路由器的 IP 的地址，有环回接口的用最高环回接口作为 RID，如果没有用所有接口中最高的 IP 地址作为 RID，路由 ID 还用于多路访问网络中 DR 和 BDR 的选择。

### 邻接关系的建立

邻接关系的建立和维持是通过不断发送 Hello 数据包维持的，一般网络每 10 秒发送一次，dead 时间是 40 秒，对于非广播多路访问网络（NBMA）的发送时间间隔为 30 秒，dead 时间为 120 秒。邻居关系建立的条件有如下三个：

1.  具有相同的 Hello 发送和失效时间
2.  区域 ID 相同
3.  末节区域标记相同

### 度量计算

计算公式如下：

---

Metric = 100000000 / bandwidth 或者自己通过 ip ospf cost 命令自己设定

---

### 迪科斯特拉（Dijkstra）算法

Dijkstra 算法的核心思想是让每台路由器通过泛洪得到的链路状态数据库构建一个以自己为根的全网目录树。大体过程是这样的：路由器启动起来自后，首先了解自身的直连网络，然后向邻居发送 Hello 数据包建立邻接关系，接着每个路由器建立链路状态数据包并泛洪给邻接路由器，邻居收到后继续泛洪给除接受接口的其他接口知道所有路由器保存了全网链路状态数据库，最后路由器执行 SPF 算法构建自己的 SPF 树同时计算最短路径并将相应条目添加到路由表中，由此完成了收敛

### 多路访问网络中 DR 和 BDR 的选择

多路访问网络中的 OSPF 问题是每两台路由器间都要创建邻接关系导致大量的邻接关系，而且由于 OSPF 初始化采用泛洪方式会导致流量很大。为了解决这一问题，采用选举指定路由器（designate
router）然后通过 DR 做代表来减小避免上述问题的方法。一个有趣的类比是：多个人之间相互介绍肯定要比选一个人做代表然后一一向大家介绍每一个人所用的时间要多，这就是 DR 的作用，而 BDR 主要是用作备份。选举的方式如下：先比较路由器优先级，选择拥有最高优先级（优先级数字越大说明优先级越高）做 DR，第二高的作为 BDR，如果优先级相同则通过路由器 ID 来比较。

### 配置和排错

#### 配置命令

1.  \#router ospf  xx 开启 OSPF，xx 为进程号，本地有效
2.  \#network 192.168.1.0 0.0.0.255 area
    0 参与路由协议的接口或者说网段并且制定区域 ID
3.  \#passive-interface 不参与路由协议的接口
4.  \#router-id 10.1.1.1 手动指定 RID

#### 排错命令

- \#sh ip ospf neighbor | database | interface
- \#debug ip ospf  \*
