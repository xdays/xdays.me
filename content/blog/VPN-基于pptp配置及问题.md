---
title: VPN-基于pptp配置及问题
date: 2011-04-16
author: admin
category: server
tags: ['pptpd', 'server', 'vpn']
slug: vpn-基于pptp配置及问题
---

先说下应用场景：学校里是用硬件集中认证的的方式来控制学生公寓上网的，如果不通过认证仅能通过 IP 访问校园网的资源。原先的应对方案是在机房（无需通过认证即可访问外网）用 squid 假设 proxy 服务器，既然是代理限制也很明显，有些不支持代理的应用就不能用了，比如一些游戏和网络电视等。自接触 VPN 以来感受其强大特性，宿舍通过拨 VPN 到机房网络，既然已经属于机房的网络了访问外网也就不是问题了。

实施步骤：

1）目前优先选取的是 pptp
VPN，因为它配置简单，况且仅需要几个连接，对性能也没什么要求。

2）配置步骤见另一篇文章[VPN-基于 pptp 的简单配置](/vpn-%E5%9F%BA%E4%BA%8Epptp%E7%9A%84%E7%AE%80%E5%8D%95%E9%85%8D%E7%BD%AE.html)

拓扑图如下：

[![pptpd-vpn-top](/wp-content/uploads/2011/03/pptpd-vpn-top.jpg 'pptpd-vpn-top')](/wp-content/uploads/2011/03/pptpd-vpn-top.jpg)

出现的问题：

按照上述步骤配置完成，客户端可以拨到 VPN
Server 获取地址，但仅可以访问部分网站，校园网内的网站可以，百度谷歌可以，新浪人人等不可以。

自己的尝试：因为之前用的是 proxy，这次就想到把 proxy 和 VPN 结合起来，不让 VPN
Server 去执行 nat 而仅仅是做为代理用，下面是测试结果

- 不拨 VPN 直接用 proxy 可以正常访问外网
- 拨 VPN 不用 proxy 可以访问部分网站
- 拨 VPN，然后去掉 Server 的 nat 功能，用 proxy，仅能访问部分网站，貌似 proxy 在 VPN 没有起作用

这个问题比较困扰我，前后总共也得折腾了三四天了，关于 pptp 协议原理的介绍也都很含糊，只好作罢，留待以后继续研究了。
