---
title: CCNA-WLAN和IPv6
date: 2010-11-06
author: admin
category: network
tags: ['ccna']
slug: ccna-wlan和ipv6
---

- 无线局域网（wireless lan，WLAN）
  - IEEE802.11 无线标准
  - 无线技术相关机构
  - 无线拓扑
  - 无线关联过程
  - 无线安全
    - 开放访问
    - SSID，WEP 和 MAC 地址认证
    - WPA 和 WPA2 预共享密钥
- IPv6
  - 概述
    - 优点
    - 报头格式
    - 地址表示方式
  - 地址分类
  - 分配地址的方式
    - 手动配置
    - EUI-64 配置
    - 无状态自动配置
    - DHCPv6 配置
  - 路由协议配置
    - RIPng 配置
    - EIGRPv6 配置
    - OSPFv3 配置
  - 过渡技术
    - 双协议栈
    - 6to4 隧道
    - NAT-PT

## 无线局域网（WLAN）

### IEEE802.11 无线标准

无线标准以相关特点的对比如下表:

---

                   802.11a                       802.11b                       802.11g                               802.11n

频段（GHz） 5.7 2.4 2.4 2.4/5
信道 最多 23 3 3  
 调制技术 OFDM DSSS DSSS/OFDM MIMO-OFDM
速度（Mbit/s） 54 11 11/54 248
优点 距离 35m；速度快，不易受干扰 距离 35m；成本低，覆盖范围广 距离 35m；速度快，范围广，不易受阻挡 距离 70m；数据传输快；扩大的覆盖范围
缺点 成本高，范围小 速度慢，易干扰 易干扰

---

\*DSSS 表示直接序列扩频；OFDM 表示正交频分复用

\*\*MIMO-OFDM 多路输入多路输出正交频分复用

### 无线技术相关机构

无线技术相关机构及其职责如下表：

---

名称 职责
ITU-R 管理 RF 波段和卫星轨道分配
IEEE 规定如何调试射频来传送信息
Wi-Fi 联盟 确保供应商生产的设备可互操作

---

### 无线拓扑分类

无线拓扑如下表：

---

无线设备 拓扑模式 构成单位 覆盖区域
没有接入点 对等 独立基本服务集（IBSS） 基本服务区（BSA）
一个接入点 基本架构 基本服务集（BSS） 基本服务区（BSA）
一个以上接入点 基本架构 基本服务集（BSS） 扩展服务区（ESA）

---

### 无线关联过程

下面是无线关联的过程：

信标（beacon）无线网络通告其存在性的帧

探测（probe）信号 客户端用来检查网络的帧

身份验证（authenticate）通过某种验证机制对客户单进行验证

关联（associate）接入点和客户端建立链路的过程

特别注意以上术语

### 无线安全

#### 开放访问

开放访问就是不需要认证

#### WEP 共享密钥加密

其缺点在于加密数据所用算法容易被破解和可扩展性问题，因为 32 位密钥是人工管理必须手动输入密钥

#### WPA 和 WPA2 预共享密钥

802.11i 规定了两种加密机制分别是 TKIP 和 AES，他们分别被纳入到 Wi-Fi 联盟的 WPA 和 WPA2 认证中。另外，带 TKIP 的 PSK 或 PSK2 相当于 WPA，而带 AES 的 PSK 和 PSK2 相当于 WPA2

## IPv6

### 概述

#### 优点

优点如下所示：

- 改进的 ip 地址：更改了全局连接性和灵活性；更好的路由聚合的 ip 前缀；没有广播；多宿主主机提高连接的可靠性；自动配置；公有私有地址重新分配无需地址转换；简化了编址和修改机制
- 简化的报头：路由选择效率更高；无需处理校验和；扩展报头更简单；提供流标签无需检查传输层就可识别数据流
- 增强的移动性和安全性
- 丰富的过渡方式：双协议栈；6to4 隧道；NAT-PT

#### 报头格式

[![wan-ipv6-header](/wp-content/uploads/2010/11/wan-ipv6-header.jpg 'wan-ipv6-header')](/wp-content/uploads/2010/11/wan-ipv6-header.jpg)3 个基本字段和 5 个新增字段

#### 地址表示方式

IPv6 的地址是以分号分隔 16 位为一个字段以十六进制表示的，可以省略开头的 0 不写，连续为 0 的字段用“：：”简化，如地址 FF01:0034:5678:0000:0000:1234:0000：0001 可以简写成 FF01:34:5678::1234:0:01，注意多个连续 0 的字段只能有一个段简写

### 地址分类

地址分类如下表：

+--------------------------+--------------------------+--------------------------+
| 名称 | 作用 | 范围 |
+--------------------------+--------------------------+--------------------------+
| 单播地址 | 传送到单个网络接口，就是一对一的地址，又分为全球 | 全球单播地址 2000::/3 |
| | 单播地址，链路本地地址和本地唯一地址 | </p> |
| | | 本地唯一地址 FC00::/7 |
| | | |
| | | <p> |
| | | 链路本地单播地址 FE80::/10 |
+--------------------------+--------------------------+--------------------------+
| 组播地址 | 发送到由组播地址识别的所有接口，一对多的地址 | FF00::/8 |
+--------------------------+--------------------------+--------------------------+
| 任播地址 | 一对多个中的一个地址 | |
+--------------------------+--------------------------+--------------------------+
| 未指定地址 | 本机地址，用于自身地址未知时 | :: |
+--------------------------+--------------------------+--------------------------+
| 环回地址 | 相当于 Ipv4 中的 127.0.0.1 | ::0 |
+--------------------------+--------------------------+--------------------------+

### 分配地址的方式

#### 手动配置

就是直接通过 ipv6 addr 命令来指定

#### EUI-64 配置

知道那个 IPv6 地址前缀部分并派生接口 ID，64 位接口 ID 派生方法是在 MAC 地址的中间插入 16 位，为 FFFE

#### 无状态自动配置

过程开始从路由器学习到前缀信息，然后类似 EUI-64 配置在 MAC 地址中间插入 16 位的 FFFE，另外填充过程中会更改接口 ID 从左往右数第 7 位的值，如果是本地唯一地址则将其改为 0，如果是全球唯一地址则更改为 1，这样就完成了无状态的自动配置

#### DHCPv6 配置

类似 IPv4 中的 DHCP

### 路由协议的配置

需要指出的是所有路由协议都是在原先的基础上做了扩展，只是去掉了广播地址，使用组播地址发送更新。路由协议的配置都很类似，首先在全局配置 i 模式下开启路由协议，然后再接口配置模式下指定开启参与路由协议功能

#### RIPng 配置

- （config）\#ipv6 router rip process-number
- （config-if）\#ipv6 rip process-number enable

#### EIGRPv6 配置

- （config）\# ipv6  router eigrp process-number
- （config-rtr）\#no  shutdown
- （config-if）\#ipv6 eigrp process-number

#### OSPFv3 配置

- （config）\#ipv6routerospf process-number
- （config-rtr）\#router-id router--id
- （config-if）\#ipv6 ospf 10 area 0

### 过渡技术

#### 双协议栈

在路由器上同时运行两个版本的 ip 协议，全局开启 IPv6 然后在一个接口上既配上 IPv4 地址也配上 IPv6 地址

#### 6to4 隧道

在 IPv4 公共网络上传输 IPv6 的数据流，也就是将 IPv6 数据包封装到 IPv4 数据包中，只在 IPv6 网络的出口上做设置

#### NAT-PT（NAT-protocol translation）

类似 NAT 只是转换前的地址是 IPv6 地址，也可以做静态，动态和端口地址转化（PAT）
