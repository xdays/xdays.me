---
title: CCNP-Switch-Security
date: 2011-03-26
author: admin
category: network
tags: ['ccnp']
slug: ccnp-switch-security
---

- 交换机安全的知识框架
  - MAC 层的攻击及解决方案
  - MAC 扩散
  - 解决方案
- Vlan 层攻击及解决方案
  - vlan 跳跃攻击
  - 解决方案
  - vlan 流量控制
  - Pvlan 部署
  - 隔离端口
- 欺骗攻击
  - DHCP 欺骗（DHCP spoofing）
  - 解决方案
  - 盗地址
  - 解决方案
  - ARP 欺骗
  - 解决方案

### 交换机安全的知识框架

<table border="1" cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td colspan="2" width="253" valign="top">
威胁类型

</td>
<td width="315" valign="top">
应对措施

</td>
</tr>
<tr>
<td colspan="2" width="253" valign="top">
MAC层攻击

</td>
<td width="315" valign="top">
端口安全（基于mac允许和拒绝，阻止单播扩散）

</td>
</tr>
<tr>
<td rowspan="3" width="111" valign="top">
vlan攻击

</td>
<td width="142" valign="top">
vlan跳跃

</td>
<td width="315" valign="top">
所有非trunk置于access

</td>
</tr>
<tr>
<td width="142" valign="top">
vlan流量控制

</td>
<td width="315" valign="top">
RACL，VACL和PACL

</td>
</tr>
<tr>
<td width="142" valign="top">
Pvlan和隔离端口

</td>
<td width="315" valign="top">
限制相同网段主机之间访问

</td>
</tr>
<tr>
<td rowspan="3" width="111" valign="top">
spoofing（欺骗）攻击

</td>
<td width="142" valign="top">
DHCP spoofing

</td>
<td width="315" valign="top">
DHCP snoop（监听）

</td>
</tr>
<tr>
<td width="142" valign="top">
盗地址

</td>
<td width="315" valign="top">
IPSG（ip source guard）源防护结合DHCP snoop

</td>
</tr>
<tr>
<td width="142" valign="top">
arp spoofing

</td>
<td width="315" valign="top">
DAI动态ARP检测结合DHCP snoop

</td>
</tr>
</tbody>
</table>
 

### MAC 层的攻击及解决方案

#### MAC 扩散

主机更改 MAC 地址发送大量帧，交换机的 CAM 表被填充满了就会泛洪接下来接收到的帧，这样就影响了网络的性能。

#### 解决方案

端口安全：包括限制方法和违规行为两方面的内容；限制方法包括允许特定数量的 mac 地址的数据通过和如何学习这些 MAC 地址（静态配置和 sticky 粘滞）；当超过时则发生违规，违规包括关闭（也就是 err-disable 状态），限制（发送 SNMP 警告信息）和保护。

基于 mac 阻止流量：显示的配置命令组织特定 MAC 地址的帧通过接口。

阻止单播帧扩散：不需要从配有端口安全的端口扩散出单播帧，所以通过命令显示丢弃。

### vlan 攻击及解决方案

#### vlan 跳跃攻击

1）通过发送 DTP 报文和交换机建立 trunk，非法主机能看到发往不同 vlan 的流量。

2）给帧打两层标签，并且两层标签的 vlan 不同，交换机去掉第一层标签后会把帧发往另一个 vlan。

#### 解决方案

避免建立 trunk 的机会因为实现 vlan 跳跃都用到了 trunk 链路，所以务必把 trunk 端口之外的端口配成 access 端口。

#### vlan 流量控制

有三种控制表可以应用于 vlan：RACL 是传统访问控制表；VACL 可以控制通过 SVI 的流量，除了转发和丢弃外还可以重定向以用作监控流量，具体见配置实验部分。

#### Pvlan 部署

Pvlan 可以更灵活的控制接入端口之间的流量，可以做到同在一个网段内的终端那些可以相互访问，哪些不能相互访问的关系。由于现在没有支持 Pvlan 的设备，此部分略去。

#### 隔离端口

隔离端口实现了 Pvlan 的一个功能就是，让同在一个网段的终端之间不能互访，可以通过命令达到要求。

### 欺骗攻击

#### DHCP 欺骗（DHCP spoofing）

因为配置有自动获取地址的终端会采纳先接收到的 DHCP 响应报文（offer），而且这个过程没有什么验证机制。那么非法接入的 DHCP 服务器就可以随意的分配地址扰乱正常网络的进行，这中攻击叫 DHCP 欺骗。

#### 解决方案

采用 DHCP
snoop 窥探技术，基本原理是：在交换机上设置信任端口和非信任端口，信任端口可以收发 DHCP 报文，而非信任端口仅仅能接收 DHCP 请求报文丢弃其他的；可以在非信任端口上配置限制流量，防止发生 DOS 攻击；交换机建立 DHCP 绑定表，记录的 IP，MAC，端口，vlan 信息等信息。

#### 盗地址

如果仅开启了 DHCP
snoop 特性，那么如果非法主机直接填地址而不通过 DHCP 获取仍然可以访问网络。

#### 解决方案

结合 HDCP snoop 窥探，IPSG（ip source
guard，ip 源防护）可以通过拿主机的二层和三层地址和 HDCP 绑定表对比来决定是否转发流量。

#### ARP 欺骗

主机总是把最后一次接受的 ARP 信息加入到自己的 ARP 表中，这是产生 ARP 欺骗的根本原因。参考下图，非法主机 C 通过发送 ARP 让主机 A 和 B 的 ARP 表中相互之间的三层地址对应的 MAC 地址指向 C 的 MAC 地址，这成为中间人攻击。

#### 解决方案

DAI（dynamic arp inspection，动态 ARP 检测）结合 DHCP
snoop，其原理是：配置信任端口和非信任端口，非信任端口不能发出 request，心热端口可以收发 ARP 报文；收到数据包和 DHCP 绑定表对比，一致则为合法流量转发，否则属于违规采取相应的措施；可以在非信任端口上配置限制流量，防止发生 DOS 攻击。
