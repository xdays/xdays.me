---
title: Zabbix自动发现
date: 2013-11-28
author: admin
category: monitor
tags: ['monitor', 'zabbix']
slug: zabbix自动发现
---

# 简介

通过近段时间对 Zabbix 的研究，我认为实现批量监控设备的方式有两种：一种是封装 API，通过调用函数传递主机信息来新增设备；另一种是通过自动发现并新增设备。本文主要讨论自动发现，因为它功能强大且操作简单。自动发现可分为网络发现，自动注册和底层发现。一言以蔽之，通过自动发现你只需要配置一个网段和发现规则即可自动完成设备的监控。

# 底层发现

## 原理

底层发现的原理大致如下：当 Zabbix 被告知需要监控一台设备时，会主动去探测设备上一些信息来作为 item，然后可以为这些 item 创建 trigger 和 graph；目前这种去探测设备的常见方式有 agent 和 snmp 等；探测来的信息实际上是一个个 key，需要通过正则表达式来筛选，然后拿筛选后的 key 来获取实际想要的信息；item，trigger 和 graph 在发现里叫做 prototype，即原型。

## 配置流程

底层发现的创建流程如下：

1.  进入模板配置，点击 discovery
2.  点击 create discovery rule
3.  填写 discovery 的相关信息
4.  点击 items prototypes
5.  点击 trigger prototypes
6.  点击 graph prototypes
7.  检查配置

**注意：**
以上每个步骤的具体细节请参考[官方文档](https://www.zabbix.com/documentation/2.2)，我只写思路。

## 实例 1 通过 SNMP 自动发现 DiskIO

由于 Net-SNMP 已经包含了磁盘 IO 的相关信息，所以只需要添加一个模板即可，考参照[zabbix_snmp_linux_templates 模板](https://gist.github.com/xdays/7689567)学习。

## 实例 2 通过 agent 自动发现 DiskIO

由于 agent 目前仅包含基于设备（如/dev/sda1）的磁盘 IO 的信息，而却不支持对设备的自动发现（是的，vfs.fs.discovery 只能发现挂载点，不能发现设备），所以我们需要自己配置 UserParameter 来读取/proc/diskstats 来实现

### zabbix_agentd.conf 配置

需要添加的配置如下：

    # disk io not filesystem!
    UserParameter=vfs.fs.io.read.ops[*],dev=`mount | grep "$1 " | awk '{print $$1}' | awk -F'/' '{print $$3}'` && cat /proc/diskstats | grep $dev | head -1 | awk '{print $$4}'
    UserParameter=vfs.fs.io.read.ms[*],dev=`mount | grep "$1 " | awk '{print $$1}' | awk -F'/' '{print $$3}'` && cat /proc/diskstats | grep $dev | head -1 | awk '{print $$7}'
    UserParameter=vfs.fs.io.write.ops[*],dev=`mount | grep "$1 " | awk '{print $$1}' | awk -F'/' '{print $$3}'` && cat /proc/diskstats | grep $dev | head -1 | awk '{print $$8}'
    UserParameter=vfs.fs.io.write.ms[*],dev=`mount | grep "$1 " | awk '{print $$1}' | awk -F'/' '{print $$3}'` && cat /proc/diskstats | grep $dev | head -1 | awk '{print $$11}'
    UserParameter=vfs.fs.io.active[*],dev=`mount | grep "$1 " | awk '{print $$1}' | awk -F'/' '{print $$3}'` && cat /proc/diskstats | grep $dev | head -1 | awk '{print $$12}'
    UserParameter=vfs.fs.io.ms[*],dev=`mount | grep "$1 " | awk '{print $$1}' | awk -F'/' '{print $$3}'` && cat /proc/diskstats | grep $dev | head -1 | awk '{print $$13}'
    UserParameter=vfs.fs.io.read.sectors[*],dev=`mount | grep "$1 " | awk '{print $$1}' | awk -F'/' '{print $$3}'` && cat /proc/diskstats | grep $dev | head -1 | awk '{print $$6}'
    UserParameter=vfs.fs.io.write.sectors[*],dev=`mount | grep "$1 " | awk '{print $$1}' | awk -F'/' '{print $$3}'` && cat /proc/diskstats | grep $dev | head -1 | awk '{print $$10}'

然后添加[zabbix_agent_linux_templates 模板](https://gist.github.com/xdays/7689550)学习。

# 动作

## 原理

在介绍网络发现和自动注册前不得不先说下动作 action 这个概念，它是自动化监控的执行者。顾名思义，动作就是在一个事件发生的时候再满足一定条件下执行一系列的操作。比如在一个监控值的触发器被触发的时候发邮件告警（即告警），比如从一个网络中发现合法的设备时创建主机并关联相关模板（网络发现），再比如当一个 agent 向 server 汇报信息时，获取相关信息，然后创建主机并关联相关模板（自动注册）。

## 配置流程

动作的创建流程如下：

1.  进入 action 配置页面，选择事件源
2.  点击 create action
3.  填写名称等 action 描述信息
4.  创建执行条件
5.  创建操作动作

**注意：** 以上每个步骤的具体细节请参考官方文档，我只写思路。

# 网络发现

## 原理

Zabbix 通过一个 IP 地址范围和发现规则（如通过 agent 获取一个 key 或者通过 snmp 获取一个 OID）来发现合法的目标设备，如果满足条件则触发一个动作，来完成相关操作。

**坑：**
我实践中发现，网络发现设备后 action 只能创建 host 不能给 host 添加 interface，这样就导致不能给设备关联 SNMP 相关的模板。

## 配置流程

网络发现的配置流程如下：

1.  点击配置，进入 discovery 页面
2.  点击 create discovery rule
3.  填写相关信息
4.  按照 action 创建流程配置这个发现对应的 action

**注意：** 以上每个步骤的具体细节请参考官方文档，我只写思路。

# 自动注册

## 原理

通过配置 zabbix_agentd.conf 指定 ServerActive 配置项让 agent 在启动的时候主动去向 server 汇报信息，具体汇报的信息由 HostMetadataItem 配置项指定，然后触发一个动作，来完成相关操作。

## 配置流程

自动注册配置流程如下：

1.  配置 agent
2.  按照 action 创建流程配置这个发现对应的 action

# 参考链接

[官方文档](https://www.zabbix.com/documentation/2.2)
