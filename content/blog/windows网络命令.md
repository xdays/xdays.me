---
title: windows网络命令
date: 2010-06-05
author: admin
category: windows
tags: ['windows']
slug: windows网络命令
---

ping

ping 命令用法和功能比较简单，主要总结 ping 不通的原因：  
1.最常见的就是对方开防火墙给过滤掉了。

2.错误的 ip 地址设置，如果两个接口设置的 ip 地址在同一个网段，主机不知道从哪个接口发出数据包。

ipconfig

比较常用的选项有/all（所有配置信息）
/release（释放通过 dhcp 获得地址参数） /renew
（从新获取地址）。另外还可以查看 dns 缓存的一些信息。

route

帮助文件就差不多了：

    ROUTE [-f] [-p] [command [destination]
    [MASK netmask] [gateway] [METRIC metric] [IF interface]

    -f           Clears the routing tables of all gateway entries. If this is
    used in conjunction with one of the commands, the tables are
    cleared prior to running the command.
    -p           When used with the ADD command, makes a route persistent across
    boots of the system. By default, routes are not preserved
    when the system is restarted. Ignored for all other commands,
    which always affect the appropriate persistent routes. This
    option is not supported in Windows 95.
    command      One of these:
    PRINT     Prints a route
    ADD       Adds    a route
    DELETE    Deletes a route
    CHANGE    Modifies an existing route
    destination Specifies the host.
    MASK         Specifies that the next parameter is the 'netmask' value.
    netmask      Specifies a subnet mask value for this route entry.
    If not specified, it defaults to 255.255.255.255.
    gateway      Specifies gateway.
    interface    the interface number for the specified route.
    METRIC       specifies the metric, ie. cost for the destination.

从打印的路由表中可以看出，本网段内和回环网段的默认网关就是本地地址，也就是自己充当网关。

tracert

一个比 ping 强大的工具，基本原理是 tracert 发送包含目的地址的数据包，只是生存时间 ttl 从 1 一直增大到能到达目的地址为止。从而收到沿途经过的路由器们的地址，打印显示。有个参数
-d 不解析 ip 地址。
