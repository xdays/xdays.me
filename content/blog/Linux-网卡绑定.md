---
title: Linux网卡绑定
date: 2012-09-03
author: admin
category: linux
tags: ['linux']
slug: linux网卡绑定
---

### 简介

端口绑定就是将多个物理网卡绑定为一个逻辑网卡；根据模式不同可以网卡绑定的作用可分为提升吞吐量和热备份两个主要作用，一般都是提升吞吐量。另外需要 bonding 内核模块的支持。

### 配置

#### 挂载模块

修改模块挂载配置文件 vim /etc/modprobe.conf

    alias bond0 bonding
    options bond0 mode=balance-alb miimon=100 use_carrier=0

#### 修改网卡参数

添加 bond0 配置 vim /etc/sysconfig/network-script/ifcfg-bond0

    DEVICE=bond0
    USERCTL=no
    BOOTPROTO=none
    ONBOOT=yes
    IPADDR=192.168.110.2
    NETWORK=192.168.110.0
    NETMASK=255.255.255.0
    GATEWAY=192.168.110.1

添加 slave 配置 vim /etc/sysconfig/network-script/ifcfg-eth1

    DEVICE=eth1
    USERCTL=no
    ONBOOT=yes
    MASTER=bond0
    SLAVE=yes
    BOOTPROTO=none

#### 重启网络

    service network restart

### 参考链接

官方文档，内容全面，特别有用：<http://www.kernel.org/doc/Documentation/networking/bonding.txt>

Mini 文档：<http://www.kernel.org/pub/linux/kernel/people/marcelo/linux-2.4/Documentation/networking/bonding.txt>

一点感想

基础的东西越全面越好，上层应用的技术够用就行，过多的纠结于实战技术的细节往往影响事情的效率；具体来说，我不需要看完常常的官方文档，因为实际上不会用到所有的参数，需要的时候去查就好了。
