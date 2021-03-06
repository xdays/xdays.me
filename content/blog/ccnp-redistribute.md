---
title: CCNP-Redistribute
date: 2011-03-18
author: admin
category: network
tags: ['ccnp']
slug: ccnp-redistribute
---

- 基本特征
- 管理距离
- 种子度量值（seed metric）
- 重分布命令
- 前缀列表（prefix list）
- 分发列表（distribute list）
- 路由映射表（route map）
- 列表总结
- 两点双向重分布问题

### 基本特征

随着网络的扩展，一个网络中可能要运行多种网络协议。要让运行不同网络协议的路由器之间获悉各自的路由信息，就要在边界路由器上执行重定向，就是两种路由协议相互导入各自的路由条目。需要考虑的因素包括不同路由协议的管理距离以及度量值不同，以及如何控制重分布的路由条目等。

### 管理距离

不同路由协议的管理距离如下表所示：

---

路由协议 管理距离
直连接口 0
送出接口的静态路由 0
下一跳的静态路由 1
EIGRP 汇总路由 5
外部 BGP 20
内部 EIGRP 90
OSPF 110
IS-IS 115
RIP 120
外部网关协议（EGP） 140
按需路由协议（ODR） 160
外部 EIGRP 170
内部 BGP 200
未知 255

---

### 种子度量值（seed metric）

当在不同路由协议之间执行重分布时，重分布而来的路由在新的路由协议中要有一个新的度量值基数，这个度量值如下表：

---

重分布到该路由协议中 种子度量值
RIP 对于静态和直连路由为 1，其他的为无穷大
IGRP/EIGRP 对于静态和直连路由为 1，其他的为无穷大
OSPF 20，类型为 E2
IS-IS 0
BGP IGP 的度量值

---

注意：除了默认的度量值外还有两种方法修改充分发的度量值：1）在配置重分布时带上 metric 参数；2）在进程模式下执行 default-metric 命令。

### 重分布命令

重分布命令统一用 redistribute，只是在参数上有区别。需要注意的是：1）重分布到 RIP 一定要制定 metric 值，要不然重分布不成功；2）EIGRP 也要指定 metric 值，而且 EIGRP 有五个 metric 需要按提示分别制定，建议取值为 1500，100，255，1，1500；3）OSPF 默认不会重分布子网，所以执行重分布时必家参数 subnets

### 前缀列表（prefix list）

前缀列表也属于一种控制列表，只是这种控制类表不能用来控制数据表而是控制路由。但与防控控制表相比前缀列表可以更精准的控制路由，具体用法如下举例：

    ip prefix-list 1 permit 2.2.2.0/24 掩码为24位

    ip prefix-list 1 permit 2.2.2.0/24  le 32  掩码为24-32位

    ip prefix-list 1 permit 2.2.2.0/24  ge 26  掩码为26-32位

    ip prefix-list 1 permit 2.2.2.0/24  gr 26 le 30  掩码为26-30位

    ip prefix-list 1 permit 0.0.0.0/0

### 分发列表（distribute list）

分发列表是控制重分布路由的方式之一，它是通过调用访问控制表来限制发往某个接口或者针对某种路由协议的路由。两种限制方式的不同之处在于：限制接口是在出方向上过滤掉路由，使其发不出去，而限制路由协议是在重定向之前就过滤掉路由，相比后者的执行效率更高。

### 路由映射表（route map）

路由映射表有脚本语言的一些特性：通过字符命名方便调用，自上而下执行，可以通过方便很方便的插入和删除，采用 match（匹配）set（设置）方式执行。可以把通过路由映射表控制的重分布路由理解为两个层面：1）是否重分布相应路由；2）对重分布的路由作何种修改（比如更改默认的 metric 值，更改 OSPF 的外部路由类型）

### 列表总结

到目前为止我们学习了那么多的列表，这些列表有什么关系，如何从更深层次上看待这些列表。从控制和数据层面上来列举如下图所示：

![list-framework](/wp-content/uploads/2011/03/list-framework.jpg 'list-framework')
</a>  
</a>

### 两点双向重分布问题

当两种路由协议有两个重分布点时由于管理距离的问题会产生次优路由问题。解决办法就是更改管理距离（distance 指定的 ip 地址是指只更改从该路由器接收到的路由的管理距离），这个问题需要单独用一个实验来总结，实验拓扑如下图：（待完善）
