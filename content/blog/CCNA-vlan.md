---
title: CCNA-VLAN
date: 2010-11-04
author: admin
category: network
tags: ['ccna']
slug: ccna-vlan
---

- 虚拟局域网（virtual lan，vlan）
  - 优点
  - vlan id 范围
  - vlan 类型
  - vlan 中继
- vlan 中继协议（vlan trunk protocol）
  - 基本概念
  - 操作过程
  - 配置和排错
- vlan 间路由
  - 每接口对应一个 vlan
  - 单臂路由（router on  a stick）
- 配置语音 vlan

## 虚拟局域网（vlan）

### 优点

虚拟局域网相对传统局域网的优点有如下几条：

1.  安全，实现了数据隔离
2.  成本降低
3.  性能提高
4.  广播控制
5.  简化应用管理和项目管理

### vlan id 范围

---

名称 普通 vlan（normal） 扩展 vlan（extend）
ID 范围 1-1005（其中 1 和 1002-1005 自动创建不能删除不能修改） 1006-4094
保存位置 Flash 中的 vlan.dat 数据库文件中 运行配置文件中
VTP 支持 支持 不支持（v3 支持）

---

### vlan 类型

---

名称 介绍
数据 vlan 传送用户数据
默认 vlan 所有接口默认所属 vlan，指 vlan1
黑洞 vlan 也叫哑 vlan，未使用端口分配的 vlan
本征（native）vlan 中继端口所属的 vlan
管理 vlan 用于访问交换机管理功能的 vlan，默认 vlan1
语音 vlan 用于传送语音的 vlan，需要专门配置

---

### vlan 中继

vlan 中继用于分配在不同交换机上相同 vlan 的主机间相互通信，有两种中继协议，ISL 和 802.1q。ISL（inter-switch
link）协议时再以太网帧的基础上加上 26 字节的报头和 4 字节的 FCS，基本不太常用。主要介绍 802.1q 协议，帧格式如下：

---

目的地址 6 源地址 6 Ethertype=0x8100 协议标识 2 用户优先级 3bit CFI 令牌网 1bit vlan-id 12bit 长度/类型 2 数据 pad 填充 FCS 4

---

其中，用户优先级用于服务质量，而 vlan-id 用来标识不同 vlan 的数据。还要强调的是本征 vlan，实际上它就是一个特殊的 vlan，只有中继链路的两个接口划分到这个 vlan。当交换机将不同 vlan 的数据发送到其他交换机的时候再中继链路的出口上打上相应的标签，通过中继链路传到其他交换机上时其他交换机根据根据标签转发数据，在转发到相应访问接口时会去掉相应的标签，也就是说只在中继链路上才能看到打了标签的帧。本征 vlan 另一个作用就是如果再中继端口上收到没有打标签的帧则发送给本征 vlan，这样就能保证像 CDP 的协议正常工作。

## vlan 中继协议（vlan trunk protocol）

vtp 是要完成在所有的交换机上实现 vlan 的统一管理的任务。vtp 要工作在一个 vtp 域中，两个不同域的交换机不能相互传递 vlan 信息，拥有共同域名的交换机构成一个 vtp 域

### 基本概念

vtp 消息封装于以太网帧（目的地址使用组播地址 0100-0ccc-cccc）中，然后打上标签通过中继链路上传播 vlan 信息

#### 服务器 server

这是 catalyst 交换机的默认模式，负责管理整个 vtp 域内的所有 vlan 信息，包括添加删除和修改。而且要注意服务器模式下的交换机 vlan 信息保存于 NVRAM 中

#### 客户端 client

只能接收服务器发来的 vlan 信息并更新自己的 vlan 信息，转发更新，但不能删除和修改 vlan

#### 透明 transparent

接收并转发 vtp 通告，但不会更新自己的 vlan 数据库，也不会把自己的 vlan 信息发送给其他交换机，仅能管理本地的 vlan 数据库。

#### vtp 修剪

达到仅将广播信息发送到需要该信息的中继链路上的目的

### 操作过程

交换机的默认配置如下：

---

名称 值
vtp 版本 1
vtp 域名 null
vtp 模式 server
配置修订版本 0
vlan vlan1

---

#### vtp 通告

总结通告

包括 vtp 配置的详细信息，由 vtp 服务器每 5 分钟发送一次，执行对 vlan 数据库配置后立即发送总结通告

子集通告

通告 vlan 具体信息

请求通告

请求 vlan 信息

注意：在以上几种通告中要注意配置修订版本号，它的值越大说明 vlan 信息越新,客户端通过比较配置修订版本号来决定是否更新本地 vlan 信息

### 配置和排错

#### 配置

- \#vtp mode server | transparent | client
- \#vtp domain name domain-name
- \#vtp pruning

#### 排错

版本不兼容，域名不一致，没有启用 vtp server

## vlan 间路由

### 每接口对应一个 vlan

每个 vlan 中的一个接入端口与路由器接口相连，对路由器屏蔽了 vlan 的概念，在路由器看来就是在路由两个不同网段

### 单臂路由（router on a stick）

通过配置中继和路由子接口，让路由器也参与到虚拟局域网中来，每个子接口对应于一个 vlan 接入接口，配置如下：

- \#intface f0/0.1
- \#encapsulation dot1q vlan 30
- \#ip addr xxx xxxx

## 配置语音 vlan

ip 电话就是一个特殊三端口的交换机，一个口接交换机的接入端口，一个接 pc，另一个供自身使用，它和交换机建立中继链路（通过 CDP）以承载 pc 发来的流量。需要注意的是这里交换机端口不再仅属于一个 vlan，出了接入 vlan 外还要在其开启服务质量后分配一个语音 vlan 以承载语音数据。配置具体步骤如下

- \#config t 进入全局配置模式
- \#mls qos 开启服务质量
- \#interface f/1 进入端口配置模式
- \#switchport priority extend trust
- \#mls qos trust cos
- \#switchport voicevlan dot1q
- \#switchport mode access
- \#switchport access vlan 3
- \#switchport   voice vlan 10
