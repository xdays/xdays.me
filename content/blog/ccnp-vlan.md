---
title: CCNP-VLAN
date: 2011-03-22
author: admin
category: network
tags: ['ccnp']
slug: ccnp-vlan
---

- VLAN（虚拟局域网）
  - VLAN 概述
  - VLAN-id 范围
- VLAN trunk（中继）
  - VLAN trunk（中继）概述
  - 封装类型
  - 协商模式
  - native vlan（本征 vlan）
- VTP（vlan 中继协议）
  - VTP 概述
  - VTP 的工作模式
- VLAN 间路由
- 小特性

### VLAN（虚拟局域网）

#### VLAN 概述

虚拟局域网就是在物理网段上划分逻辑网段，一般是基于接口划分，它可以任意组合接口成为一个网段。由于不同的逻辑子网之间不能通信，VLAN 就分割广播域，安全性提高；可以把任意接口划分到任意 VLAN，这样增加了网络的灵活性；管理方便，易于维护。

#### VLAN-id 范围

VLAN 的范围为 0-4095，具体分配如下表：

---

范围 用途
0 和 4095 系统保留
1 所有接口默认所属的 vlan
2-1001 正常使用 vlan
1002-1005 保留给特殊网络使用（令牌网等）
1006-4094 扩展 vlan

---

注意：扩展 vlan 只能在部分机型上配置，而且交换机必须处在 VTP 的透明模式下才可以。

### VLAN trunk（中继）

#### VLAN trunk（中继）概述

当在一条链路上承载多个 vlan 的数据是，这条链路就是 trunk 链路。关于 trunk 链路有两方面重要内容：封装和协商模式。

#### 封装类型

封装主要有 ISL 和 802.1Q，ISL 是思科专有协议，它是在以太网帧的外面继续封装，添加 30 个字节的信息；802.1Q 是开放协议，它是在帧内部打上一个 4 字节的标签，分别是 2 字节以太网标识，3 位的优先级，1 位的 token-ring 标记，和 12 位的 vlan-id。

#### 协商模式

交换机接口通过 DTP 协议来协商建立 trunk 链路，链路的模式以及其工作状态如下表：

---

模式 特点
access 无条件 access 模式，不发也不收
trunk 无条件 trunk 模式，既发又收
dynamic auto 只发送不接收
dynamic desirable 既发送又接收
nonegotiate 无条件 trunk 模式，既不发也不收

---

而当两交换机工作在这几种模式下最终达到的状态如下表：

---

access trunk auto desirable
access access \* access access
trunk \* trunk trunk trunk
auto access trunk access trunk
desirable access trunk trunk trunk

---

注意打\*表示不建议这样配置。

#### native vlan（本征 vlan）

就是通过 trunk 链路却不打标签的 vlan，当交换机收到不打标签的 vlan 时就发给本征 vlan，所以 trunk 链路两边的接口的本征 vlan 必须一致，否则不能正常通信。

### VTP（vlan 中继协议）

#### VTP 概述

相当于是 vlan 分发协议，只在一台交换机（vtp
server）上配置 vlan 信息，然后哦通过 vtp 协议发给其他交换机，最终所有在 vtp 域内的交换机的 vlan 信息一致（透明模式交换机例外）。关于 vtp 需要注意一下几点：1）vtp 工作的前提是链路必须工作在 trunk 模式下；vtp 的域名和密码必须一致；3）server 和 client 都跟着配置版本号大的学习 vlan 信息，并且会丢弃自己的信息，所以配置 vtp 要慎重。

#### VTP 的工作模式

vtp 有三种工作模式，名称及状态如下表：

---

模式 特点
server 增删改 vlan 信息，发送转发 vlan 信息，同步 vlan，信息保存于 NVRAM
client 发送和转发 vlan 信息，同步 vlan 信息，不保存
transparent（透明） 不同步，不发送自己的 vlan，只转发收到的，信息保存于 NVRAM

---

### VLAN 间路由

vlan 间路由主要有三种方式：

1）三层交换：交换机通过开启 SVI 接口和路由功能来转发（CEF 方式）不同 vlan 之间的流量。

2）交换机路由接口：因为三层交换机的每一个接口都可以配成路由接口，这样交换机就可以看作是一台路由器。

3）单臂路由（route on a
stick）：通过给路由器配置子接口以承载不同 vlan 之间的流量，再加上路由器的路由功能实现 vlan 间的转发，需要注意的是：与路由器建立 trunk 链路的交换机上要有相应的 vlan，否则 vlan 间不能通信。

### 小特性

1）ARP 表的老化时间是 300s

2）在 trunk 链路配置 vtp pruning 可以过滤不必要的流量通过交换机。
