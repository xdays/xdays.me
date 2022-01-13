---
title: CCNA-WAN
date: 2010-11-17
author: admin
category: network
tags: ['ccna']
slug: ccna-wan
---

- WAN 基本概念
  - 基本概念
  - 接入方式
- PPP
  - 串行通信标准
  - 帧结构
  - 分层架构
  - LCP
  - NCP
  - 相关配置命令
  - 身份验证及相关配置
    - 密码验证协议 PAP
    - 配置 PAP
    - 挑战验证协议 CHAP
    - 配置 CHAP
- 帧中继（frame relay）
  - 基本概念
  - 帧结构
  - 执行过程
  - 基本配置
  - 子接口及相关配置

WAN 基本概念

基本概念

用户室内设备（customer premises equip，CPE）用户室内的设备和内部布线

数据通信设备（data communication
equipment）将用户连接到 WAN 网络云的通信链路，注意 DCE 还提供时钟频率

数据终端设备（data terminal
equipment）通过 WAN 传送来自客户网络或主机计算机的数据的客户设备

本地环路（local loop）用于连接 CPE 和中心局之间的介质，也叫最后一英里

分界点（demarcation point）客户设备和服务提供商设备的分隔点

中心局（central office）本地服务提供商的设备间和大楼

WAN 设备

调制解调器（modem）提供模拟信号和数字信号之间的转换

CSU/DSU（channel/data service
unit）将 CPE 的数字信号转换层服务提供商设备所能理解的信号的物理层设备

WAN 物理层标准

在 DCE 和 DTE 之间主要使用这几种通信标准：EIA/TIA-232，EIA/TIA-449/530，EIA/TIA-612/613，V.35 和 X.25

WAN 数据链路层协议

WAN 常用的数据链路层协议：HDLC，PPP，frame-relay，ATM

接入方式

WAN 接入方式如下图所示：

[![wan-link-options](/wp-content/uploads/2010/11/wan-link-options.jpg 'wan-link-options')](/wp-content/uploads/2010/11/wan-link-options.jpg)综合业务数字网络（ISDN）

一种电路交换网络，让 PSTN 的本地环路可以传送数字信号。有两种基本的 ISDN 接口，基本接口速率 BRI（base
rate
interface）提供一个 16kbit/s 的 D 信道和两个 64kbit/s 的 B 信道；基群速率接口 PRI（primary
rate
interface）可以提供相当于 T1 线路（1.544Mbit/s，23 个 B 信道和一个 D 信道）的速率，还可以提供相当于 E1 信道（2.048Mbit/s，30 个 B 信道和一个 D 信道）的速率。

异步传输模式（asynchronous transport mode）

基于信元的架构，信元长度固定为 53 字节，其中包括 5 字节的 ATM 头

PPP（point to point protocol）

串行通信标准

RS-232 通信接口通常为 9 针；V.35 连接到 T1 线路的接口标准；HSSI 高速串行接口，最高支持 52Mbit/s

帧结构

对比 HDLC 和 PPP 的帧结构如下（数字代表字节数）：

标准 HDLC

---

标志 1 地址 1 控制 2 数据 FCS2

---

其中控制字段根据信息帧，管理帧和无编号帧

cisco 的 HDLC

---

标志 1 地址 1 控制 2 协议 2 数据 FCS2

---

可以看出标准 HDLC 不支持多协议，而 cisco 版本的添加了协议字段支持多协议。

PPP 是基于 HDLC 的，帧结构如下

---

标志 1 地址 1 控制 2 协议 2 数据 FCS2

---

注意 LCP 协商可以修改 PPP 的帧结构，如有压缩选项的帧达成一致后可省略地址字段，控制字段变成一个字节

分层架构

LCP 链路控制协议

主要负责链路建立，维护和终止，还包括一些 PPP 特有选项的配置，如身份验证，压缩和多链路。LCP 分组封装于 PPP 帧的数据字段，主要字段如下：

---

编码 标识符 长度 数据

---

其中标识符用于匹配请求和应答，长度为 LCP 分组所有字段的总长度

NCP 网络控制协议

主要负责协调第三层协议，采用模块化模型，每种网络层协议都有相应的 NCP。IPCP 的两个选项是压缩和 IP 地址（用于拨号网络中）

相关配置命令

相关配置命令如下表：

---

配置 命令
启用 ppp encapsulation ppp
压缩 compress predictor | stac
链路质量监控，低于设定值自动关闭 ppp quality 80
负载均衡多链路 ppp multilink

---

身份验证及相关配置

密码验证协议 PAP

基本的身份验证协议，本地路由器以 LCP 包发送用户名和密码，信息已明文传送，只进行一次身份验证，远程节点验证身份回应接收还是拒绝。

PAP 配置

---

步骤 命令
添加本地保存的用来验证的用户信息 username router password passwd
LCP 发送的信息 ppp pap sent-username ruoter password passwd
启用 PAP 身份验证 ppp authentication pap

---

挑战握手验证协议 CHAP

相比 PAP，CHAP 的优点在定时验证和加密（md5 加密算法）具体执行过程：路由器 A 向路由器 B 发送挑战消息包括 ID，随机数和用户名 A，然后 B 查找自身数据库加上接收到的 ID，随机数来计算一个散列值，并将这个值，ID 以及用户名返回给 A，A 再查找自身数据库计算一个散列值与接收到的散列值对比如果一只则返回接受建立连接

CHAP 配置

---

步骤 命令
添加保存本地用来验证的用户信息 username router password passwd
启用 CHAP 身份验证 ppp authentication chap

---

帧中继（frame relay）

帧结构

---

标志 地址 数据 FCS

---

地址字段如下（数字表示位数）

---

DLCI 6 C/R 1 EA 1 DLCI 4 FECN 1 BECN 1 DE 1 EA 1

---

C/R 为保留字段；EA 为扩展地址，当该位为 1 时为 DLCI 的最后一个字节；F/BECN 用于拥塞控制的位；DE 可丢弃位，也就是当网络拥塞时可以丢弃的位；DLCI 为虚电路的标识符，其保留的部分分配具体如下表：

---

VC 标识符 VC 类型
0 LMI（ANSI，ITU）
1-15 提供以后使用
992-1007 CLLM
1008-1022 提供以后使用
1019-1020 多播（cisco）
1023 LMI（cisco）

---

基本概念

虚电路

虚电路为两台 DTE 提供一条双向通信路径，用 DLCI（数据链路连接标识符）标识。称为虚电路是因为并没有真实的电路连接设备，而是通过服务提供商的帧中继交换机来实现一种逻辑上的电路，所有用户共享带宽

本地管理接口（local manage interface，LMI）

DTE 和它连接的第一个帧中继交换机之间的信令标准，用于传递有关服务提供商网络和 DTE 之间的操作和状态信息。其中 LMI 扩展包括保持激活（每 10s 轮训网络一次），虚电路状态，组播（DLCI 号 1019-1022 用于组播），全局地址和简单流量控制

接口速度或者端口速度

就是接入电路可以传输的最大速度

承诺信息速率（CIR）

服务提供商承诺的最大传输速率

突发速率

突发速率包括承诺突发信息速率（CBIR）和超额突发量（BE），前者指超过承诺信息速率的突发量，而后者是超过 CBIR 的那部分流量

可达性问题

当路由器的一个接口连接多条帧中继虚电路时，由于路由协议的水平分割机制，导致无法广播路由信息到其他网络。解决这个问题的方法有两个：禁用水平分割和配置子接口

流量控制

帧中继通过 F/BECN 来实现简单的拥塞控制，对于从拥塞链路接收到的帧将其 BECN（后向显式拥塞通知）置位，对于发往拥塞链路的帧将其 FECN（前向显式拥塞通知）置位

配置帧中继

基本配置

基本配置命令如下表：

---

配置 命令
启用帧中继 encapsulation frame-relay cisco | ietf
静态映射 frame-relay map protocol addr dlci [broadcast][cisco | ietf ]
本地管理接口类型 frame-relay lmi cisco | ansi |q933a

---

配置子接口

子接口旨在解决 NBMA（非广播多路访问网络）的不可达问题，为每个 PVC 分配单独的接口，只是这种接口是虚拟的并不是真实的物理接口，但实现的功能是一样的，配置不收如下：

---

步骤 命令
创建子接口 interface serial id.subid point-to-point
为子接口关联本地 DLCI frame-relay interface-dlci dlci-id

---

注意其中 subid 通常是本地的 dlci 号

检验相关命令

show frame-relay lmi | pvc dlci-id | map
