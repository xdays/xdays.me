---
title: iptables 防火墙及nat
date: 2010-08-02
author: admin
category: server
tags: iptables, server, 防火墙
slug: iptables-防火墙及nat
---

什么是iptables？

iptables是用来配置linux内核自带的包过滤系统的命令行工具，它主要是面向系统管理员。

什么是规则，链，表？

规则（rule）：包过滤条件及处理方式，这是过滤系统的基本单位。比如规则可以指定源地址，目的地址，源端口，目的端口等，如果匹配规则就按照相关处理方式处理数据包。  

链（chain）：链是数据包的传播路径，是规则的集合，包括一条或者多条规则。数据包到达某条链时，iptables依次按规则处理数据包。  

表（table）：提供特定功能的一组链，常见的主要有filter表（INPUT,FORWARD,OUTPUT链），nat表
（PREROUTING,POSTROUTING,OUTPUT链），mangle表
（PREROUTING,POSTROUTING,INPUT,FORWARD,OUTPUT链）。

数据包有怎样的传输过程（链之间的关系）？

[![iptables](/wp-content/uploads/2010/08/iptables.png "iptables")](/wp-content/uploads/2010/08/iptables.png)

(图片转自鸟哥私房菜)

iptables的语法？

iptables [-t 表(默认filter)] [命令选项]   {链} [ 匹配选项(默认所有) ] [
操作选项]

命令选项：-A 添加 -D 删除 -I 插入，加序号 -L 查看 -P 默认规则 -F
清除规则 -N 创建新链 -X删除指定链 -Z 清零计数器

匹配选项：（很多，具体查看手册，这里列举常用的）  
接口号：-i 指定从哪个接口收到的包  
协议类型：-p {tcp | udp | icmp} 指定协议类型  
源地址：-s ip/netmask，可以指定ip地址和网段  
目的地址：-d/netmask，同上  
源端口号：--sport n1:n2，特定范围端口  
目的端口：--dport n1:n2，同上  
icmp类型：--icmp-type n 指定icmp类型号  
状态模块：-m [mac | state]，--mac-source源mac地址，--state
包括INVALID，ESTABLISHED，NEW，RELATED

操作选项：-j
指定匹配数据包的处理方式，有ACCEPT，DROP，SNAT，DNAT，还可以传递给其他的自定义链。

怎样操作规则？

主要是如何保存和恢复，以及如何开机启动规则。  
保存规则：iptables-save \> filename  
恢复规则：iptables-restore \< filename  
注意：redhat系统可以执行service iptables save或者iptables-save \>
/etc/sysconfig/iptables来保存规则并开机启动。

什么是nat？

nat（network address
translation）是一种将私有地址转换成公有地址的技术，优点主要是解决ip地址不足以及增强网络安全等问题。

如何通过iptables配置nat服务器？

首先打开内核的路由功能：echo "1" \> /proc/sys/net/ipv4/ip\_forward  
然后再nat表的POSTROUTING链中添加规则：iptables -t nate -A POSTROUTING 
-o eth1 -j SNAT --to A.B.C.D  
最后设定客户端的网关为nat服务器面向lan的接口地址。

使用nat时有哪些控制方式？

因为nat服务器是作为客户端的网关，在其上做控制显得尤为必要了。从iptables内建表格相关性(如图)可以看出，其实控制就是通过编辑nat表的FORWARD和PREROUTING链来实现的，命令选项也与其他链一样。

还有一个有意思的控制，强制重定向到特定站点。

\#iptables -t nat -A PREROUTING -i eth0 -p tcp -dport 80 -j DNAT --to
192.168.1.250:80

参考资料：

《鸟哥的linux私房菜--服务器架设篇》

Iptables 指南
1.1.19<http://www.frozentux.net/iptables-tutorial/cn/iptables-tutorial-cn-1.1.19.html#TRAVERSINGGENERAL>

Iptables Tutorial 1.1.19<http://www.faqs.org/docs/iptables/>

[](http://www.faqs.org/docs/iptables/)（一篇详细介绍iptables的文档，把文档写的如此详细，不得不佩服也感谢译者。）
