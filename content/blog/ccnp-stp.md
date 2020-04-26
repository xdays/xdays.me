---
title: CCNP-STP
date: 2011-03-20
author: admin
category: network
tags: ['ccnp']
slug: ccnp-stp
---

注：本文档中桥和交换机为同义词，终端与主机为同义词，仅个人习惯而已。

- STP
  - 基本概述
  - 基本概念
    - 网桥 ID（BID）
    - 开销（cost）
  - 网桥协议数据单元（BPDU）
  - 端口角色
  - 端口状态
  - 计时器（timer）
  - 选举的标准
  - 执行的过程
  - 拓扑变更
  - STP 的衍生版本
- PVST+（per-vlan STP 中的 RID）
- RSTP（Rapid STP 快速生成树）
  - 端口角色
  - 端口状态
  - BPDU 中对 flag 的拓展
  - 分段收敛
  - keep-alive 机制
  - 拓扑更改
- RPVST+（per-vlan RSTP）
- MST（Multiple STP，多生成树）
  - 基本特征
  - RID 的再次扩展
  - MST 区域
  - MST 和 CST 共存
- STP 增强特性
  - 加快收敛的特性
  - BPDU 保护特性
  - STP 上避免环路

### STP（spanning tree protocol）

#### 基本概述

增加网络可靠性的方法就是提供冗余链路，然而如果没有有效的措施冗余就会造成环路。三层上的动态路由协议采用诸如水平分割，路由毒化等措施来避免环路，而二层上的环路主要是靠 STP（spanning
tree
protocol）来完成的。从总体上来说 STP 通过把一些端口置为阻塞状态最终要达到的一种如下图所示的状态。整个网络有一个根，然后向外发散构造的树状网络。此外由于从基本的 STP 向外扩展了很多衍生版本，使 STP 比较复杂。

#### 基本概念

网桥 ID（BID）

对于网络中的所有交换机都要有一个唯一的标识，功能类似于 OSPF 中的 RID。BID 由优先级（priority，2 字节）和 mac 地址（6 字节）两部分组成。

开销（cost）

因为 STP 要选最佳路径，所以 cost 确定到达根桥的最优路径。相应规定如下表：

---

链路速度 开销
10G 2
1G 4
100M 19
10M 100

---

#### 网桥协议数据单元（BPDU）

STP 的消息格式解释如下图所示：

#### 端口角色

因为最终 STP 要阻塞掉一些端口，端口角色就是来区分阻塞端口和正常转发端口。各种端口角色以及行为如下表：

---

端口角色 行为
根端口 除根桥以外的所有交换机到达根桥的最优端口
指定端口 每条链路上只能有一个指定端口，这句话也是 STP 核心
非指定端口 那些需要阻塞的端口

---

#### 端口状态

为确保网络的稳定性，端口不能在角色之间直接切换，这样就定义了端口状态来缓冲这个过程。端口状态及其行为如下表所示：

---

端口状态 行为
监听 仅接受 BPDU，执行选举过程
学习 接受 BPDU，并且学习 mac 地址
转发 接受 BPDU，转发数据
阻塞 仅接受 BPDU
禁用 不参与 STP

---

#### 计时器（timer）

STP 定义的在各种端口状态停留的时间也就是计时器如下表：

---

计时器 时间
Hello 时间 根桥发送 BPDU 的时间
失效时间 保存配置 BPDU 的最大时间
转发延迟 接口在监听和学习状态停留的时间

---

#### 选举的标准

从选举根桥到选举根接口再到选举指定接口 STP 一直遵循着同一个标准，按照如下顺序依次判定：1）最低的根桥 ID；2）最低的到达根桥的路径开销；3）最低的发送方的桥 ID；4）最低的端口优先级；5）最低的端口 ID。

#### 执行的过程

启动后各交换机都认为自己是根桥，当收到更优的 BPDU（RID 更小）时更改自己发送的 BPDU 的 RID；选举出根桥以后所有交换机确定到达根桥开销最小的端口作为根端口；所有网段上选举一个指定端口，根桥上的所有端口都是指定端口（designate
port，DP），因为与之相连的都是根端口；把所有剩余的端口 block 掉，设为非指定端口（NDP），这样网络就收敛了。

#### 拓扑变更

当网络中链路出现中断以后，交换机会从自己的根接口发送 TC 置位的 BPDU，然后收到 BPDU 的交换机回复确认继续在自己的根接口上发出 TC 置位的 BPDU，直到到达根桥，根桥会修改配置 BPDU 以通知拓扑变更，持续时间为 35s，当其他交换机收到根桥发来的 TC
BPDU 后会将 CAM 寿命设为转发延迟（15s）以求快速更新地址表（经讨论认为，35s+15s 这恰好重新经历了一个 STP 收敛过程！）。

#### STP 的衍生版本

STP 有很多衍生版本，其名称以及对应的 IEEE 协议如下表：

---

名称 对应标准
CST 802.1d
RSTP 802.1w
PVST+ p-vlan 802.1d
RPVST+ p-vlan 802.1w
MSTP 802.1s

---

### PVST+（per-vlan STP 中的 RID）

因为 CST 是在所有 vlan 运行一个 STP 实例，而 PVST 是在每一个 vlan 独立运行一个实例，这样就可以在多条链路上实现负载均衡，有效利用带宽。但是可能一台交换机可能同时收到多个 vlan 的 BPDU，如何区分这些 BPDU 呢？这时就要对原先的 RID 进行拓展，从 2 个字节的优先级中拿出 12 位作为扩展 ID 来标志 vlan-id，这就是 PVST 和 CST 的区别。

### RSTP（Rapid STP 快速生成树）

#### 端口角色

根端口（RP）和指定端口（DP）：与 STP 一致

替代端口（alternative
port，AP）：两台交换机的 BPDU 比，次优的端口（发送次优 BPDU 的端口）作为替代端口；替代端口能在根端口失效的时候成为根端口。。

备份端口（backup
port）：同一台交换机上发送次优 BPDU 的端口作为备份端口（这种情况很少出现，如两个接口接到了 hub 上）

#### 端口状态

RSTP 把 STP 中的禁用，阻塞和监听都归为丢弃（discarding）状态，保留学习和转发状态，这样就缩短了过渡的时间。

#### BPDU 中对 flag 的拓展

STP 中只用了 flag 中的 2 位（TC 和 TCA），现在 RSTP 对其作了扩展，具体如下图所示：

#### 分段收敛

当交换机收到 proposal 置位的 BPDU 时就把所有其他接口置为 sync（同步，就是都 block 掉）状态，然后判断自己的端口角色，然后再向其他交换机发送 proposal 的 BPDU，继续这个过程。这是 RSTP 的核心内容，也是快速收敛的根源。

#### keep-alive 机制

每台交换机都向相邻交换机以 hello 时间为周期发送 BPDU，当 3 倍于 hello 时间没有收到对方的 BPDU 就认为拓扑更改了，这样检测链路故障的速度更快。

#### 拓扑更改

当拓扑发生更改是，交换机除了向根发送 BPDU 外也向其他交换机发送 BPDU，目的就是让大家尽快知道拓扑已经发生更改，以提高收敛速度。

### RPVST+（per-vlan RSTP）

就是在每个 vlan 中运行一个 RSTP。

### MST（Multiple STP，多生成树）

#### 基本特征

CST 是在所有 vlan 中运行一个 STP，PVST 是在每个 vlan 中运行个 STP，而 MST 就是这两种协议的折衷。MST 是将多个 vlan 映射到一个 STP 实例上，不仅能在多条链路上执行复杂均衡而且还能有效利用资源。此外 MST 还向后兼容，可以与其他版本的 STP 共存。

#### RID 的再次扩展

因为将多个 vlan 映射到一个实例上，那么 vlan-id 就不重要了，而 RID 的扩展 id 就变成了实例（instance）号，以此区分不同的实例。

#### MST 区域

具有相同 MST 配置的一系列交换机构成了 MST 区域，这里的配置包括了配置名称，配置版本号和 vlan 实例的映射关系三部分。

#### MST 和 CST 共存

共存时我们可以把 MST 的 IST（也就是 MSTI0，MST 的实例 0）当成一台虚拟的交换机，在外界看来它就是一台交换机。

### STP 的增强特性

#### 加快收敛的特性

portfast

由于接入层直接连终端，不会产生环路，所以配置 portfast 的端口启动后直接过渡到转发状态而不经过监听和学习。

uplinkfast

当交换机的上联链路 down 了，交换机能能直接把阻塞端口至于转发状态而不经过监听和学习，从而加快收敛速度。配置了 uplinkfast 的交换机为了防止自己变成根需要做如下修改：1）将自己的优先级改成 49152；2）到达根桥开销在原先基础增加 3000；3）标识 uplinkfast 开启。

backbonefast

（此处待插入图片后添加说明）

下面是对三种 fast 的总结：

---

特性 配置位置 节约时间
portfast 接入交换机 30s
uplinkfast 接入交换机 30s
backbonefast 所有交换机 20s

---

实验配置通过实验来验证三种特性：

[![stp-feathers](/wp-content/uploads/2011/03/stp-feathers.jpg 'stp-feathers')](/wp-content/uploads/2011/03/stp-feathers.jpg)

    sw1#sh spanning-tree

    VLAN1 is executing the ieee compatible Spanning Tree protocol

    Bridge Identifier has priority 32768, sysid 1, address 000d.29cf.1b80

    Configured hello time 2, max age 20, forward delay 15

    We are the root of the spanning tree

    Topology change flag not set, detected flag not set

    Number of topology changes 7 last change occurred 00:03:17 ago

    from FastEthernet0/2

    Times:  hold 1, topology change 35, notification 2

    hello 2, max age 20, forward delay 15

    Timers: hello 1, topology change 0, notification 0, aging 300

    Port 1 (FastEthernet0/1) of VLAN1 is forwarding

    Port path cost 19, Port priority 128, Port Identifier 128.1.

    Designated root has priority 32769, address 000d.29cf.1b80

    Designated bridge has priority 32769, address 000d.29cf.1b80

    Designated port id is 128.1, designated path cost 0

    Timers: message age 0, forward delay 0, hold 0

    Number of transitions to forwarding state: 1

    BPDU: sent 1519, received 9

    Port 2 (FastEthernet0/2) of VLAN1 is forwarding

    Port path cost 19, Port priority 128, Port Identifier 128.2.

    Designated root has priority 32769, address 000d.29cf.1b80

    Designated bridge has priority 32769, address 000d.29cf.1b80

    Designated port id is 128.2, designated path cost 0

    Timers: message age 0, forward delay 0, hold 0

    Number of transitions to forwarding state: 1

    BPDU: sent 188, received 0

    sw2#sh span

    VLAN0001

    Spanning tree enabled protocol ieee

    Root ID    Priority    32769

    Address     000d.29cf.1b80

    Cost        19

    Port        1 (FastEthernet0/1)

    Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

    Bridge ID  Priority    32769  (priority 32768 sys-id-ext 1)

    Address     000d.6548.c900

    Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

    Aging Time 300

    Interface        Role Sts Cost      Prio.Nbr Type

    ---------------- ---- --- --------- -------- --------------------------------

    Fa0/1            Root FWD 19        128.1    P2p

    Fa0/2            Desg FWD 19        128.2    P2p

    sw3#sh span

    VLAN0001

    Spanning tree enabled protocol ieee

    Root ID    Priority    32769

    Address     000d.29cf.1b80

    Cost        19

    Port        1 (FastEthernet0/1)

    Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

    Bridge ID  Priority    32769  (priority 32768 sys-id-ext 1)

    Address     0011.9234.7e80

    Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

    Aging Time 300

    Interface        Role Sts Cost      Prio.Nbr Type

    ---------------- ---- --- --------- -------- --------------------------------

    Fa0/1            Root FWD 19        128.1    P2p

    Fa0/2            Altn BLK 19        128.2    P2p

**portfast 特性**

1）不开启 portfast 的变化

    sw3#

    00:25:39: %LINK-3-UPDOWN: Interface FastEthernet0/3, changed state to up

    00:25:40: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/3, changed state to down

    sw3#

    00:25:40: set portid: VLAN0001 Fa0/3: new port id 8003

    00:25:40: STP: VLAN0001 Fa0/3 -> listening

    sw3#

    00:25:41: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/3, changed state to up

    sw3#

    00:25:55: STP: VLAN0001 Fa0/3 -> learning

    sw3#

    00:26:10: STP: VLAN0001 sent Topology Change Notice on Fa0/1

    00:26:10: STP: VLAN0001 Fa0/3 -> forwarding

计算时间差正好是 30s

2）开启 portfast 的变化

    sw3(config-if)#no shut

    sw3(config-if)#

    00:29:38: %LINK-3-UPDOWN: Interface FastEthernet0/3, changed state to down

    sw3(config-if)#

    00:29:40: %LINK-3-UPDOWN: Interface FastEthernet0/3, changed state to up

    00:29:41: set portid: VLAN0001 Fa0/3: new port id 8003

    00:29:41: STP: VLAN0001 Fa0/3 ->jump to forwarding from blocking

    sw3(config-if)#

    00:29:42: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/3, changed state to up

**uplinkfast 特性**

1）不开启 uplinkfast 特性

    sw3(config)#int f0/1

    sw3(config-if)#shut

    sw3(config-if)#

    00:31:17: STP: VLAN0001 new root port Fa0/2, cost 38

    00:31:17: STP: VLAN0001 Fa0/2 -> listening

    sw3(config-if)#

    00:31:19: %LINK-5-CHANGED: Interface FastEthernet0/1, changed state to administratively down

    sw3(config-if)#

    00:31:19: STP: VLAN0001 sent Topology Change Notice on Fa0/2

    sw3(config-if)#

    00:31:20: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/1, changed state to down

    sw3(config-if)#

    00:31:32: STP: VLAN0001 Fa0/2 -> learning

    sw3(config-if)#

    00:31:47: STP: VLAN0001 sent Topology Change Notice on Fa0/2

    00:31:47: STP: VLAN0001 Fa0/2 -> forwarding

2）开启 uplinkfast 特性

开启后变化

    sw3(config)#spanning-tree uplinkfast

    sw3(config)#

    00:35:29: setting bridge id (which=1) prio 49153 prio cfg 49152 sysid 1 (on) id C001.0011.9234.7e80
    （优先级变成49152）

    sw3#sh spanning-tree

    VLAN0001

    Spanning tree enabled protocol ieee

    Root ID    Priority    32769

    Address     000d.29cf.1b80

    Cost        3038

    Port        2 (FastEthernet0/2)

    Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

    Bridge ID  Priority    49153  (priority 49152 sys-id-ext 1)

    Address     0011.9234.7e80

    Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

    Aging Time 300

    Uplinkfast enabled

    Interface        Role Sts Cost      Prio.Nbr Type

    ---------------- ---- --- --------- -------- --------------------------------

    Fa0/2            Root FWD 3019      128.2    P2p

    Fa0/3            Desg FWD 3100      128.3    Edge Shr

    注意观察三处的变化。

    sw3(config)#int f0/1

    sw3(config-if)#shut

    sw3(config-if)#

    00:40:15: STP: VLAN0001 new root port Fa0/2, cost 3038

    00:40:15: %SPANTREE_FAST-7-PORT_FWD_UPLINK: VLAN0001 FastEthernet0/2 moved to Forwarding (UplinkFast).

    sw3(config-if)#

    00:40:17: %LINK-5-CHANGED: Interface FastEthernet0/1, changed state to administratively down

    sw3(config-if)#

    00:40:17: STP: VLAN0001 sent Topology Change Notice on Fa0/2

    sw3(config-if)#

    00:40:18: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/1, changed state to down

可以看到 F0/2 直接进入转发状态不经过 30s 延迟了。

**backbonefast 特性**

1）不开启 backbonefast 特性

    sw3#

    01:56:48: STP: VLAN0001 heard root 32769-000d.6548.c900 on Fa0/2

    sw3#收到次优的root BPDU

    01:56:50: STP: VLAN0001 heard root 32769-000d.6548.c900 on Fa0/2

    sw3#

    01:56:52: STP: VLAN0001 heard root 32769-000d.6548.c900 on Fa0/2

    sw3#

    01:56:54: STP: VLAN0001 heard root 32769-000d.6548.c900 on Fa0/2

    sw3#

    01:56:56: STP: VLAN0001 heard root 32769-000d.6548.c900 on Fa0/2

    sw3#

    01:56:58: STP: VLAN0001 heard root 32769-000d.6548.c900 on Fa0/2

    sw3#

    01:57:00: STP: VLAN0001 heard root 32769-000d.6548.c900 on Fa0/2

    01:57:00: STP: VLAN0001 Fa0/2 -> listening超时之后进入listening状态

    sw3#

    01:57:01: STP: VLAN0001 Topology Change rcvd on Fa0/2

    01:57:01: STP: VLAN0001 sent Topology Change Notice on Fa0/1

    sw3#

    01:57:15: STP: VLAN0001 Fa0/2 -> learning

    sw3#

    01:57:30: STP: VLAN0001 sent Topology Change Notice on Fa0/1

    01:57:30: STP: VLAN0001 Fa0/2 -> forwarding

    sw3#

2）开启 backbonefast 特性

    sw3#（没有超时过程，直接进入listening）

    02:03:32: STP: VLAN0001 heard root 32769-000d.6548.c900 on Fa0/2

    02:03:32: STP: VLAN0001 Fa0/2 -> listening

    02:03:33: STP: VLAN0001 Topology Change rcvd on Fa0/2

    02:03:33: STP: VLAN0001 sent Topology Change Notice on Fa0/1

    sw3#

    02:03:47: STP: VLAN0001 Fa0/2 -> learning

    sw3#

    02:04:02: STP: VLAN0001 sent Topology Change Notice on Fa0/1

    02:04:02: STP: VLAN0001 Fa0/2 -> forwarding

#### BPDU 的保护特性

基本原理

BPDU
guard：当从 portfast 接口收到 BPDU 时交换机将接口置于 err-disable 的状态，相当于关闭状态，全局启动。

BPDU
filter：这个尤其要注意接口模式和全局模式下配置的不同之处：接口模式下配就不发送任何 BPDU 且丢弃任何接受到的 BPDU；全局模式下配如果收到 BPDU 就将相应接口改回正常的 STP 操作。

Root
guard：当交换机收到更好的 BPDU 时将相应的接口置于 inconsistent 状态，相当于监听状态，经过一定时间自动恢复。

实验配置

1）BPDU guard 特性

在 S1 上配置：

    S1(config)#int f0/23

    S1(config-if)#spanning-tree portfast

    S1(config-if)#spanning-tree bpduguard enable

把 S2 连接到 S1 上

    00:06:45: %LINK-3-UPDOWN: Interface FastEthernet0/24, changed state to up

    S1#

    00:06:46: set portid: VLAN0001 Fa0/24: new port id 8018

    00:06:46: STP: VLAN0001 Fa0/24 -> listening

    00:06:47: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/24, changed state to up

    S1#

    00:06:48: %SPANTREE-2-BLOCK_BPDUGUARD: Received BPDU on port FastEthernet0/24 with BPDU Guard enabled. Disabling port.

    S1#

    00:06:48: %PM-4-ERR_DISABLE: bpduguard error detected on Fa0/24, putting Fa0/24 in err-disable state

    00:06:49: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/24, changed state to down

    S1#

2）BPDU filter 特性

在 S1 上配置

    S1(config)#int f0/23

    S1(config-if)#spanning-tree portfast

    S1(config-if)#spanning-tree bpdufilter enable

把 S2 连接到 S1 上，如下提示：

    S1#

    00:09:14: %LINK-3-UPDOWN: Interface FastEthernet0/24, changed state to up

    00:09:15: set portid: VLAN0001 Fa0/24: new port id 8018

    00:09:15: STP: VLAN0001 Fa0/24 -> listening

    S1#

    00:09:16: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/24, changed state to up

    S1#

    00:09:30: STP: VLAN0001 Fa0/24 -> learning

    S1#

    00:09:45: STP: VLAN0001 sent Topology Change Notice on Fa0/2

    00:09:45: STP: VLAN0001 Fa0/24 -> forwarding可以进入正常的转发状态

3）root guard 特性

在 S1 上配置

    S1(config)#int f0/24

    S1(config-if)#spanning-tree guard root

把 S3 接到 S1 上，如下提示：

    00:14:23: %LINK-3-UPDOWN: Interface FastEthernet0/24, changed state to up

    S1#

    00:14:25: set portid: VLAN0001 Fa0/24: new port id 8018

    00:14:25: STP: VLAN0001 Fa0/24 -> listening

    00:14:26: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/24, changed state to up

    S1#

    00:14:26: STP: VLAN0001 heard root 32769-000d.29cf.1b80 on Fa0/24

    00:14:26:     supersedes 32769-000d.6548.c900

    00:14:26: %SPANTREE-2-ROOTGUARD_BLOCK: Root guard blocking port FastEthernet0/24 on VLAN0001.

    S1#

    00:14:26: STP: VLAN0001 Fa0/24 -> blocking

    00:14:27: STP: VLAN0001 heard root 32769-000d.29cf.1b80 on Fa0/24

    00:14:27:     supersedes 32769-000d.6548.c90

#### STP 上避免环路

有 loopguard 和 udld 两种方式，避免单向故障造成的环路。（烦了，不想总结了，待定吧）
