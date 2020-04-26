---
title: CCNA-交换基础和STP
date: 2010-11-02
author: admin
category: network
tags: ['ccna']
slug: ccna-交换基础和stp
---

- 交换基础
  - 分层网络中交换机的功能
  - 转发数据包方式
  - 第二层交换的 3 个功能
  - 端口安全
- 生成树协议（spanning tree protocol，STP）
  - 基本概念
    - 桥 ID
    - 根桥
    - 网桥协议数据单元（bridge protocol data unit）
    - 根端口
    - 指定端口
    - 端口状态
- STP 协议执行过程（820.1D）
- 其他生成树协议
- 拓展特性
  - portfast
  - BPDU guard
  - BPDU filtering
  - uplinkfast
  - backbonefast

## 交换基础

### 分层网络中交换机的功能

LAN 体系结构分为三层，包括接入层（access），分发层（distribute）和核心层（core），每一层对交换机的功能都有不同要求，具体如下表：

---

层次 功能要求
接入层 端口安全；VLAN；快速以太网/千兆以太网；以太网供电（PoE）；链路聚合（Etherchannel）；服务质量（QoS）
分布层 第 3 层支持；很高的转发速率；千兆以太网/万兆以太网；冗余组件；安全策略/访问控制列表；链路聚合；服务质量
核心层 第 3 层支持；极高转发速度；千兆以太网/万兆以太网；冗余组件；链路聚合；服务质量

---

### 转发数据包的方式

交换机转发数据的方式有存储转发和快速转发，其中快速转发又可分为快速转发和免分片转发（fragment-free），快速转发只查看目的地址就开始转发，免分片转发转发之前存储前 64 个字符。

### 第二层交换的 3 个功能

地址学习，转发/过滤（控制冲突域），避免环路（STP）

### 端口安全

端口安全包括两方面内容：安全规则和违规模式。安全规则包括允许特定 MAC 地址访问，允许特定数量的 MAC 地址访问；违规模式包括保护（仅不转发流量），限制（不转发流量，发出 SNMP 陷阱和 syslog 消息，增加违规计数器），关闭（限制的所有动作，关闭端口）。注意：MAC 地址的获取方式包括静态，动态和粘滞（sticky），粘滞方式会把学习到的 MAC 地址添加到运行配置文件中。下表为相关配置命令：

---

\#switchport port-security [ mac-address | maximum | violation]
\#switchport port-security mac-address [ x.x.x.x | sticky ]
\#switchport port-security maximum x
\#switchport port-security violation protect | restrict | shutdown

---

## 生成树协议（spanning tree protocol，STP）

### 基本概念

#### 桥 ID

用来标识广播域内的每一个交换机，它主要由如下三部分组成：

---

桥优先级 4 位 扩展系统 ID 12 位 MAC 地址 48 位

---

#### 根桥

实施 STP 的第一步就是选根桥，因为一些行为都是相对根桥来操作的，可以把根桥想象成最终形成的 STP 树的根。选举根桥的标准时最高的网桥优先级，特别注意这里的最高网桥优先级是指的最小的桥 ID，也就是说在选举根桥的时候数字越小越好

#### 网桥协议数据单元（spanning tree protocol，STP）

下图是通过 wireshark 抓到的 STP 消息：

[![switch-stp-bpdu](/wp-content/uploads/2010/11/switch-stp-bpdu.jpg 'switch-stp-bpdu')](/wp-content/uploads/2010/11/switch-stp-bpdu.jpg)注意消息类型字段是区分 BPDU 类型：0x00 表示配置 BPDU，0x80 表示 TCN 用于拓扑发生变化时通告，另外链路开销如下表：

---

链路速度 开销
10Gbit/s 2
1Gbit/s 4
100Mbit/s 19
10Mbit/s 100

---

#### 根端口

所有的非根网桥都要选举根端口，就是到达根桥开销最小的端口。首先明确一点就是在生成树协议中数字越小优先级越大，然后确定根端口的标准先后顺序是：路径开销--上一跳交换机的桥 ID--链路另一端端口优先级--链路另一端端口号

#### 指定端口（designate port）

每一条二层链路上都要选举，也就是连接交换机的链路两端要有一个是指定端口。确定知道那个端口的标准有限顺序和确定根端口的一样。这时候我们想想根端口和指定端口恰好完美的实现了无环拓扑的构建，根端口确保了每个网桥到达根的路径只有一条且开销最小，而指定端口在根端口的基础上确保每条链路到达根桥的路径只有一条且开销最小，最终便实现了一种逻辑上星型的拓扑

#### 端口状态

下表为 802.1D 规定的端口状态：

---

端口状态 动作
阻塞（blocking） 丢弃收到数据帧；不转发数据帧；不获取地址；接收处理 BPDU
侦听（listening） 丢弃收到数据帧；不转发数据帧；不获取地址；接收处理并传输 BPDU
学习（learning） 丢弃收到数据帧；不转发数据帧；获取地址；接收处理并传输 BPDU
转发（forwarding） 接收转发收到数据帧；转发数据帧；获取地址；接收处理传输 BPDU
禁用（disabled） 相当于 down 状态

---

### STP 执行过程

总体上来说是选举根桥--选举根端口--选举指定端口--把非指定端口 block 掉，完成收敛。下面用转自[china-ccie](http://www.china-ccie.com/ccie/lilun/switching/switching.html#6)上的例子来说明

[![switch-stp-converge](/wp-content/uploads/2010/11/switch-stp-converge.jpg 'switch-stp-converge')](/wp-content/uploads/2010/11/switch-stp-converge.jpg)  
上图的网络环境中，运行 STP 后，则选举如下角色：（所有链路为 100
Mb/s，即 Path Cost 值为 19）

根交换机（Root）

因为 4 台交换机的优先级分别为 SW1（4096）
，SW2（24576），SW3（32768），SW4（32768），选举优先级最高的（数字最低的）为根交换机，所以 SW1 被选为根交换机，如果优先级相同，则比较 MAC 地址。

根端口（Root Port）

根端口需要在除 SW1 外的非根交换机上选举。SW2 上从端口 F0/23 到达根的 Path
Cost 值为 19，从 F0/19 和 F0/20 到达根的 Path
Cost 值都为 19×3=57。因此，F0/23 被选为根端口。SW3 上从端口 F0/19 到达根的 Path
Cost 值为 19，从 F0/23 和 F0/24 到达根的 Path
Cost 值都为 19×3=57。因此，F0/19 被选为根端口。SW4 上从所有端口到达根的 Path
Cost 值都为 19×2=38，所以从比较 Path
Cost 值，无法选出根端口，接下来比较上一跳交换机 Bridge-ID，也就是比较 SW2 与 SW3 的 Bridge-ID，所以选择往 SW2 的方向，然而通过端口 F0/19 和 F0/20 都可以从 SW2 到达根交换机，所以接下来比较端口 F0/19 和 F0/20 对端交换机端口的优先级，因为 SW2 的 F0/19 端口优先级为 128，而 F0/20 的端口优先级为 112，所以 SW4 选择连接 SW2 的 F0/20 的端口为根端口，即 SW4 的 F0/20 为根端口，如果此步还选不出，SW4 将根据
对端端口号做出决定，也就是 F0/19 和 F0/20，数字小的为根端口，也就是 F0/19。

指定端口(Designated Port)

每个网段（每个冲突域），或理解为每条线路都要选举指定端口。在根交换机 SW1 连接 SW2 的网段与连接 SW3 的网段中，当然是根自己的端口离自己最近，所以这两个网段中，选举根交换机上的端口为指定端口，因此，根交换机上所有的端口都应该是指定端口。在 SW3 连接 SW4 的两个网段中，同样也是 SW3 上的两个端口离根交换机最近，所以在这两个网段中，选举 SW3 上的端口为指定端口。在 SW2 连接 SW4 的两个网段中，同样也是 SW2 上的两个端口离根交换机最近，所以在这两个网段中，选举 SW2 上的端口为指定端口。

注：根交换机上所有的端口最终都为指定端口。

其它既不是根端口，也不是指定端口的落选的端口，就是 SW4 上的 F0/19，F0/23，F0/24，都将被 STP 放入 Blocking 状态，不为用户提供数据转发，以此来防止环路。最终的网络，构建出了任何两点之间，都是单链路的环境，不会有环路，当使用中的链路失效时，Blocking 的端口可以代替原端口。上图的 STP 选举结果如下：

根交换机（Root）

SW1

根端口（Root Port）

SW2：F0/23 SW3：F0/19 SW4：F0/20

指定端口(Designated Port)

SW1：F0/19，F0/23 SW2：F0/19，F0/20 SW3：F0/23，F0/24

Blocking 端口

SW4：F0/19，F0/23，F0/24

### 其他生成树协议

#### 快速生成树协议（rapid STP，RSTP,也就是 802.1w）

因为阻塞，侦听和禁用都不转发数据，将其统一为丢弃（discarding）状态，RSTP 端口有丢弃，学习和转发 3 种状态。在 STP 中链路失效要经过一个最大失效时间和两个转发延迟才能启用 block 端口这样需要进过 50 秒，而 RSTP 经过 3 个 Hello 时间就认为与根交换机失去联系，立即将丢弃状态的转为启用状态。

#### PVST（思科专有 ISL 协议），PVST+（pervlan 802.1d）和 Rapid PVST+（pervlan 802.1w）

这三种协议都支持 vlan，在每个 vlan 上构建独立的生成树，PVST 只支持 ISL 中继协议，PVST+和 Rapid
PVST+分别是基于 STP（802.1D）和 RSTP（802.1w）并添加了 vlan 的支持，而且添加了一些拓展特性，关于这些拓展特性下面会有讨论。注意：以上协议为思科转悠协议

#### MSTP(802.1s)

多个 vlan 可映射到相同的生成树实例，由 802.1s 规定

### 拓展特性

#### portfast

因为对于接入层的交换机接口一般不会形成环路，所以端口启动时可以跳过 STP 计算过程直接过渡到转发状态，这就是 portfast

#### BPDU guard

如果启用了 portfast 的端口连接了会收到 BPDU 消息这种情况下 portfast 是个错误的配置，为了避免这个问题可以添加 BPDU
guard 特性，也就是当收到 BPDU 消息时执行 shutdown 或者 error-disable 状态。全局启动的 bpduguard 只会影响启用了 portfast 的端口，而接口上的启动的 bpduguard 会对所有接口有效不管它是否开启了 portfast

#### BPDU filtering

过滤掉接口上发送和接收的 BPDU，相当于关闭了 STP 功能。如果 BPDU
Filtering 是全局开启的，则只能在开启了 portfast 的接口上过滤 BPDU，并且只能过滤掉发出的 BPDU，并不能过滤收到的 BPDU；如果是在接口模式下开启的，则可以过滤掉任何接口收到和发出的 BPDU

#### uplinkfast

接入层交换机检测到自身的链路断开时立即开启 blocking 的端口而不去等待 Hello 超时和转发延迟，且只支持全局开启。

#### backbonefast

具体参考一下<http://www.china-ccie.com/ccie/lilun/switching/switching.html#17>
