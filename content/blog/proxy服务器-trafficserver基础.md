---
title: proxy服务器-trafficserver基础
date: 2013-11-07
author: admin
category: server
tags: ats, proxy, trafficserver
slug: proxy服务器-trafficserver基础
---

简介
====

Apache Traffic
Server（简称ATS）是新一代的缓存代理服务器，Yahoo买下Inktomi，经多年开发日渐成熟，2009年将其贡献给Apache基金会作为TLP。

特性
====

-   缓存，也是其最主要应用，功能和Squid一样；
-   代理，服务器端做反向代理，负载均衡，功能和nginx等类似；
-   快速，支持多核处理器，每秒并发支持到3w；
-   可扩展
    -   插件机制使其内部可扩展
    -   通过多级缓存和ICP互联工作模式使其外部可扩展

**注意：**在技术领域里会经常看到这种新技术创造的革命，如nginx

组件
====

TrafficServer缓存
-----------------

通过告诉对象数据库来缓存，索引为URL和相关header头。可以根据vary存多份；存储很大和很小的文件；能容忍磁盘的任何失效，盘坏完了就切换为纯代理模式；可以对缓存分区，不同条件存到不同的分区，可用于混合存储。

RAM缓存
-------

顾名思义，内存缓存。

Host数据库
----------

用于保存链接源服务器的DNS记录，包括DNS，HTTP版本信息。

DNS解析器
---------

回源解析，可实现根据条件使用不同的DNS服务器。

TrafficServer进程
-----------------

-   traffic\_server是事务处理引擎
-   traffic\_manager用来命令和控制ATS的进程，如配置，统计，集群管理和故障转移
-   traffic\_cop监控traffic\_server和traffic\_manager健康状况，可重启这俩进程。

安装
====

安装依赖
--------

对于CentOS：

    sudo yum install gcc gcc-c++ pkgconfig pcre-devel tcl-devel expat-devel openssl-devel perl-ExtUtils-MakeMaker libcap libcap-devel hwloc hwloc-devel autoconf automake libtool git

对于Ubuntu：

    sudo apt-get install g++ make pkg-config libssl-dev tcl-dev libexpat1-dev libpcre3-dev libmodule-install-perl

获取源码
--------

    git clone https://git-wip-us.apache.org/repos/asf/trafficserver.git

配置环境
--------

    cd trafficserver && autoreconf -if && ./configure --prefix=/usr/local/trafficserver

编译安装
--------

    make && make check && sudo make install

启动
----

    cd /usr/local/trafficserver/bin && ./traffic_server start

配置
====

由于ATS配置文件采用模块化管理，所以文件数目很多，配置文件对应的功能如下：

-   cache.config 控制如何存储对象
-   congestion.config 拥塞控制
-   hosting.config 为源站或者域名指定磁盘分区
-   icp.config 配置ICP服务
-   ip\_allow.config 访问控制
-   log\_hosts.config 为特定源站单独写log文件
-   log\_xml.config 自定义日志文件格式
-   parent.config 定义父缓存节点
-   plugin.config 插件配置
-   records.config 定义变量，可通过traffic\_line -x设置
-   remap.config URL映射规则
-   splitdns.config 自定义域名解析
-   ssl\_multicert.config 配置多SSL证书
-   storage.config 配置所有缓存存储
-   update.config 配置定时更新缓存
-   volume.config 配置volume

参考链接：
==========

-   [概要介绍](http://ostatic.com/blog/guest-post-yahoos-cloud-team-open-sources-traffic-server)
-   [官方文档](https://trafficserver.readthedocs.org/en/latest/reference/configuration/index.en.html)

