---
title: CCNA-ACL和NAT
date: 2010-11-05
author: admin
category: network
tags: ['ccna']
slug: ccna-acl和nat
---

- 访问控制表（access control list，ACL）
  - 配置 acl 的原则（3p 原则）
  - 执行过程
  - 分类
    - 标准 acl
    - 扩展 acl
    - 命名 acl
  - acl 的放置位置
  - 配置过程和排错
    - 标准 acl 配置
    - 扩展 acl 配置
    - 命名 acl 配置
    - 排错
  - 复杂 acl
    - 动态 acl
    - 自反 acl
    - 基于时间的 acl
- 网络地址转换（network address translation）
  - 基本概念
    - 内部本地地址
    - 内部全局地址
    - 外部本地地址
    - 外部全局地址
  - 类型及其执行过程
    - 静态 nat
    - 动态 nat
    - 端口地址转换 pat（nat 重载）
  - nat 的优点和缺点
  - 配置和排错
    - 静态 nat 配置
    - 动态 nat 配置
    - 端口地址转换 pat 配置-单地址
    - 端口地址转换 pat 配置-nat 池
    - 排错

## 访问控制表（access control list，ACL）

### 配置 acl 的原则（3p 原则）

每个接口（per port），每个协议（per protocol），每个方向（per
direction）只能配置一条 acl

### 执行过程

[![acl-process](/wp-content/uploads/2010/11/acl-process.jpg 'acl-process')](/wp-content/uploads/2010/11/acl-process.jpg)需要注意的是如果在一个接口的一个方向如果所有 acl 规则都不匹配，默认路由器会丢弃该数据包

### 分类

从根本上来说 acl 分为两类，他们的区别如下表：

---

名称 标准 acl 扩展 acl
acl 编号 1-99；1300-1999 100-199；2000-2699
控制条件 仅用源 ip 协议类型，源 ip 和端口，目的 ip 和端口

---

另外两种 acl 都可以配置成命名 acl，命名 acl 的好处是直观，并且可以根据编号调整控制表各条语句的相互顺序

### acl 放置位置

为了提高网络的工作效率，也更精确的控制流量，需要把 acl 放置的合理的位置。标准访问控制表只能通过源 ip 地址来决定数据包的通过与否，所以要将其放置到尽可能接近目的网络的位置；扩展访问控制表可以通过源和目的 ip 以及源和目的端口来控制数据包，所以要把 acl 放置到尽可能接近源网络的位置

### 配置和排错

访问控制表建立是在全局模式下而控制表的应用是在接口模式下

#### 标准 acl 配置

- \#access-list access-list-id permit | deny | remark
  source-ip-address wildmask 其中 remark 用于注释控制表
- \#ip access-group access-list-id in | out

#### 扩展 acl 配置

- \#access-list access-list-id permit | deny | remark protocol-type
  source-ip wildcard operator port-numb dest-ip wildcard operator
  port-numb 这里只是列举了部分规则，具体规则根据协议的类型而变化
- \#ip access-group access-list-id in | out

#### 命名 acl 配置

如上所说命名 acl 是可以直接通过编号进行编辑控制语句的前后顺序，具体如下

- \#ip access-list standard | extended name
- \#sequence-number permit \*\* 下面的就和标准和扩展的配置规则一样了

#### 排错

关于排错需要注意的是网络规划和通配符子网掩码的分配，另外明确路由器的隐式拒绝规则，排错命令有 sh
ip access-list，注释信息需要在 running-config 下才能看到

### 复杂 acl

复杂 acl 通过其他策略实现的访问控制，如验证后自动添加一条 acl，自反 acl 也就是只允许由内部发起连接的返回数据流通过的 acl，还有基于时间的 acl 允许数据特定时间段内通过

#### 动态（锁和钥匙）acl

默认使用一条 acl 阻止所有数据通过，当用户通过 telnet 登陆并通过身份验证时 telnet 断开，自动建立一条动态 acl 允许数据通过，还可以设置超时时间

#### 自反 acl

只允许响应内部网络发起的连接的外部数据通过，而拒绝其他的数据

#### 基于时间的 acl

相关配置如下：

\#time-range acl-name

\#periodic Weekday 7:00 to 8:00

\#创建 acl 时就是在扩展 acl 之后加上一个 time-range acl-name

## 网络地址转换（network address translation）

### 基本概念

---

名称 含义
内部本地地址 内部网络分配给主机的地址
内部全局地址 数据包离开 nat 路由器是的公网 ip 地址
外部全局地址 分配给外部主机的公网地址
外部本地地址 通常认为和外部全局地址相同

---

### 类型和执行过程

#### 静态 nat

当数据包从 nat 路由器发送出去时仅源 ip 地址被更改，并且 nat 路由器是参考 nat 表来更改地址，一个内部地址对应一个外部地址

#### 动态 nat

nat 路由器上指定一个地址池，由路由器自动分配内部地址对应的外部地址，并且在通信过程中一直保存着这种对应关系

#### 端口地址转换（pat，或者 nat 重载）

nat 路由器同时修改数据包的源 ip 地址和端口号（合成 socket）都更改掉，并且维护着这种对应关系。这里又根据转换后的数据包的源 ip 地址又有两种情况，单公有 ip 地址的重载（overload）和公有 ip 地址池的重载。实际上我们可以把这两种情况想象成灾静态 nat 和动态 nat 的基础上加上了重载的特性

### nat 的优点和缺点

如下表所示

---

优点 缺点
节省了公有 ip 地址；提高了连接到公网的灵活性；提供了一致的内部网络编址方案；提供了网络安全性 影响性能，重新封装；影响端到端的功能；无法跟踪端到端的 ip 地址；一些协议无法工作

---

### 配置和排错

#### 静态 nat 配置

\#ip nat inside source inside-address global-address
定义一条 nat 规则使内网地址和外网地址建立联系

\#ip nat inside 设置需要转换的接口

\#ip nat outside 转换后的送出接口

#### 动态 nat 配置

\#ip nat pool pool-name start-addr end-addr netmask
net-netmask 定义一个 nat 池

\#access-list access-list-id permit net-addr
net-netmask 定义一个访问控制表来控制需要 nat 的范围

\#ip nat inside source list  access-list-id pool
pool-name 定义一条 nat 规则把需要 nat 的网段范围和供 nat 用的 nat 池联系起来

\#ip nat inside

\#ip nat outside

#### 端口地址转换（pat）配置-单地址

\#access-list access-list-id permit net-addr net-netmask

\#ip nat inside source list access-list-id interface interface-id
overload 定义一条 nat 规则建立一个网段和一个接口的端口地址转换规则

\#ip nat inside

\#ip nat outside

#### 端口地址转换（pat）配置-nat 池

\#access-list access-list-id permit net-addr net-netmask

\#ip nat pool pool-name start-addr end-addr netmask net-netmask

\#ip nat inside list access-list-id pool pool-name overload
定义一条规则建立一个网段和一个 nat 池的端口地址转换规则

\#ip nat inside

\#ip nat outside

#### 排错

可以从以下角度分析问题所在：

- 检查访问控制表的 ip 范围
- 检查 nat 地址池的范围
- 确定内部和外部接口分配正确

还有 sh ip nat translations 查看 nat 表
