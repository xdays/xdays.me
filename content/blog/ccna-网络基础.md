---
title: CCNA-网络基础
date: 2010-10-25
author: admin
category: network
tags: ['ccna']
slug: ccna-网络基础
---

目录

- [OSI 模型，名称，职责，包括的协议](#osi)
- [TCP/IP 模型](#tcp/ip)
- [应用层：http,ftp,tftp,dhcp,smb,telnet](#application)
- [传输层：tcp/udp](#transport)
- [网络层：ip，icmp，arp，rarp,proxy-arp](#network)
- [数据链路层：IEEE802.2/802.3,ethernetii](#datalink)
- [物理层：线缆类型](#physical)
- [以太网：帧格式，csma/cd，类型](#ethernet)
- [ip 寻址：地址类型，广播地址，子网划分，cidr，vlsm](#ipaddr)

### <a name="osi"></a>

**OSI 模型**

全称开放系统互联模型（open system interconnection
model）主要层次，各层作用以及相关协议如下表所示：

---

名称 作用 相关协议
应用层（application） 为用户提供应用程序服务 http,ftp,tftp,dhcp,smb,telnet
表示层（presentation） 表示，处理数据  
 会话层（session） 在不同程序间管理会话  
 传输层（transport） 提供可靠和不可靠数据传输，重传前执行错误纠正 tcp/udp
网络层（network） 提供逻辑寻址路由选择 ip,icmp,arp,rarp,proxy-arp
数据链路层（data link） 将数据组合成帧，控制介质访问，错误检测但不纠正 IEEE802.2/802.3
物理层（physical） 设备间传输比特，电压大小，线路速率和接口引脚

---

### <a name="tcp/ip"></a>

**TCP/IP 模型**

现在因特网实际应用中的协议栈，也成为 DoD 模型。它一共分四层，各层名称以及与 OSI 对应的层次如下表所示：

---

名称 对应 OSI 层
过程/应用层协议（process/application） 应用层，表示层，会话层
主机到主机协议（host-to-host） 传输层
网际层（internet） 网络层
网络接入层（network access） 数据链路层，物理层

---

#### 协议数据单元 pdu

每一层对应的协议数据单元的称呼

---

名称 协议数据单元
application data
transport segment
network package
data link frame
physical bit

---

### <a name="application"></a>

**应用层协议**

#### http 协议

用于 web 服务的协议，主要特点可概括如下：

1.支持客户/服务器模式。

2.简单快速：客户向服务器请求服务时，只需传送请求方法和路径。请求方法常用的有
get、head、post。每种方法规定了客户与服务器联系的类型不同。由于 http
协议简单，使得 http 服务器的程序规模小，因而通信速度很快。

3.灵活：http 允许传输任意类型的数据对象。正在传输的类型由 content-type
加以标记。

4.无连接：无连接的含义是限制每次连接只处理一个请求。服务器处理完客户的请求，并收到客户的应答后，即断开连接。采用这种方式可以节省传输时间。

5.无状态：http
协议是无状态协议。无状态是指协议对于事务处理没有记忆能力。缺少状态意味着如果后续处理需要前面的信息，则它必须重传，这样可能导致每次连接传送的数据量增大。另一方面，在服务器不需要先前信息时它的应答就较快。

参考文档：<http://wenku.baidu.com/view/9fc10d6c1eb91a37f1115c86.html>

#### ftp 协议

用于文件传输的协议，具体可参考</?p=101>

#### dhcp 协议

用于局域网内自动分配 ip 地址的协议，具体可参考</?p=179>

### <a name="transport"></a>

**传输层协议**

#### tcp/udp 协议

传输层通过顺序和确认号提供可靠传输，通过窗口来实现流量和拥塞控制，具体参考</?p=105>

### <a name="network"></a>

**网络层协议**

#### ip 协议

[![ip-headers](/wp-content/uploads/2010/10/ip-headers.jpg 'ip-headers')](/wp-content/uploads/2010/10/ip-headers.jpg)

字段依次代表：版本，包头长度，服务类型，数据包长度，标识（标识同一数据包），标志和分片偏移量（重组数据包依据），ttl 生存时间，协议类型（上层协议），校验和（如果出错只是丢弃而不重传），源地址，目的地址，其他选项，填充（以满足 32 位）

#### icmp 协议

虽然是网络层协议，但是它是封装在 ip 包内的，具体类型主要有

[![icmp-type](/wp-content/uploads/2010/10/icmp-type.jpg 'icmp-type')](/wp-content/uploads/2010/10/icmp-type.jpg)

#### arp 协议

提供通过广播由 ip 地址到 mac 地址的解析过程的协议，关于 arp 欺骗参考</?p=109>

#### rarp 协议

对于无盘工作站，只知道自己 mac 地址的情况下请求自己 ip 地址的情况。

#### proxy-arp 协议

arp 请求由路由器代理，从而实现不同网段之间的二层通信（基于 arp 和 mac 地址）。

#### 广播域与冲突域，点到点与端到端

广播域就是一个网段内的所有主机，冲突域是共享相同介质的所有主机，广播域大于等于冲突域。点到点是指的设备通过第二层地址通信，端到端是指的通过第三层设备通信。

### <a name="datalink"></a>

**数据链路层**

IEEE 把数据链路层分成两层分别是 802.2 逻辑链路控制（logical link
control）和 802.3 介质访问控制（media access
control），前者负责协调上层协议，后者负责控制介质访问；而更常见的是以太网的数据链路层，两者区别如下：

802.3 帧

---

前导码 8 源地址 6 目的地址 6 长度 2 数据 FCS 校验和

---

ethernetII 帧

---

前导码 8 源地址 6 目的地址 6 类型 2 数据 FCS 校验和

---

总之，以太网可以直接区分上层协议。

### <a name="physical"></a>

**物理层**

主要有三个方面介质（铜介质有采用 rj-45 接口的非屏蔽双绞线 utp 和同轴电缆 coaxial
cable，光纤，无线），编码（不归零码，曼侧斯特码），信号（电压大小）

线缆类型

直通线（straight-through），交叉线（crossover），全反线（rolled）：其中直通线用于不同设备间，交叉线用于相同设备间，全反线用于连接思科设备的 console 口。注意：路由器按做 PC 处理，而集线器按做交换机处理。

### <a name="ethernet"></a>

**以太网**

数据链路层上面已经介绍了，下表是物理层上以太网的类型

[![ethernet-type](/wp-content/uploads/2010/10/ethernet-type.jpg 'ethernet-type')](/wp-content/uploads/2010/10/ethernet-type.jpg)

CSMA/CD 载波监听多路访问/冲突检测（carrier sense multiple
access/collision
detect）是用于总线型拓扑下的一种通信方式在现在交换式网络中已经不再使用，参考文档<http://baike.baidu.com/view/54303.htm>

### <a name="ipaddr"></a>

**IP 寻址**

#### 有类地址划分

---

类型 起始位 子网掩码
A 0 255.0.0.0
B 10 255.255.0.0
C 110 255.255.255.0
D 1110 组播
E 1111 实验

---

#### 无类地址划分

CIDR 无类域间路由（classless inter-domain routing）和 VLSM（variable
length subnet
masks）,，通过 VLSM 把 ip 地址更灵活的划分，通过 CIDR 将划分的地址块汇总聚合。

私有地址

---

地址类 范围
A 类 10.0.0.0—10.255.255.255
B 类 172.16.0.0—172.31.255.255
C 类 192.168.0.0—192.168.255.255

---

#### 保留地址

---

地址 功能
网络地址全为 0 这个网络分段
网络地址全为 1 全部网络
127.0.0.1 操作系统环回测试
结点地址全 0 网络中任意主机
结点地址全 1 网络上所有结点
整个 ip 地址为 0 默认路由
整个 ip 地址为 1 对网络上所有结点广播，受限广播

---
