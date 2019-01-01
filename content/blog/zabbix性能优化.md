---
title: Zabbix性能优化
date: 2013-12-12
author: admin
category: monitor
tags: monitor, zabbix
slug: zabbix性能优化
---

概述
====

关于优化，我个人观点是这样的：首先，优化的前提是完善的监控，因为你有完善的监控才能发现确定问题所在，才能看到优化后的效果；然后，不要过度优化，时间很宝贵，视需求来决定优化的程度，够用即可；最后优化不是一件容易的事情，需要对方方面面有深入的理解。

性能评估
========

Zabbix自带了对自身的监控，包括繁忙worker进程的比例，缓存使用情况等，也有相应的触发器。

配置调整
========

    #采集进程的数量，这个值是关键，当监控数目较多时需增大此值
    StartPollers=100
    #对不可达设备的采集进程数量，适当增加
    StartPollersUnreachable=100
    #缓存大小，用于存储主机，项目和触发器的数据
    CacheSize=256M
    #历史数据值缓存
    ValueCacheSize=64M
    #认为agent不可达的时间
    Timeout=10
    #数据库慢查询
    LogSlowQueries=1000

**吐槽：** 官方文档对配置文件的描述太简单了，只能知其然不能知其所以然。

参考链接  
[zabbix performance
tuning](http://www.slideshare.net/xsbr/alexei-vladishev-zabbixperformancetuning)
