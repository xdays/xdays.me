---
title: Zabbix基本安装
date: 2013-11-15
author: admin
category: monitor
tags: ['monitor', 'zabbix']
slug: zabbix基本安装
---

# 简介

目前系统运维监控环节有 Cacti 和 Nagios 两大工具，分别用于监控中的作图和报警两个重要方面。而 Zabbix 可以集两工具的功能于一体并且具有一些额外的包括告警自动处理，资产管理等“福利”。官方称其为企业级的开源监控解决方案，其中含义可在学习研究中慢慢体会。

# 特性

- 数据采集，支持 SNMP，IPMI，JMX 和 agent 等多种模式
- 分析采集数据，问题探测
- 可视化，可做成牛掰的大屏幕模式
- 告警通知，自动处理
- 模板机制，简化操作
- 自动发现
- 支持 proxy 模式，可做分布是监控
- 资产管理

# 安装配置

## 安装需求

![zabbix hardware
reuqirement](/wp-content/uploads/2013/11/zabbix_requirement.jpg)

## 安装官方源

    rpm -ivh http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm

## 安装 Zabbix 组件

    yum install zabbix-server-mysql zabbix-web-mysql zabbix-agent

## 配置数据库

### 初始化数据库

    # mysql -uroot
    mysql> create database zabbix character set utf8;
    mysql> grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';
    mysql> exit
    # cd /usr/share/doc/zabbix-server-mysql-2.2.0/create
    # mysql -uroot zabbix < schema.sql
    # mysql -uroot zabbix < images.sql
    # mysql -uroot zabbix < data.sql

### 配置 zabbix_server.conf

    # vi /etc/zabbix/zabbix_server.conf
    DBHost=localhost
    DBName=zabbix
    DBUser=zabbix
    DBPassword=zabbix

### 启动 Zabbix

    service zabbix-server start
    service zabbix-agent start

## 解决中文字体问题

虽然 zabbix 的国际化做的不错，但是其自带的 web 字体是不支持汉字的，这导致作图时所有文字均为方框。解决办法是从系统上找个中文字体，然后覆盖 zabbix 的字体。

    cp font.ttf /etc/alternatives/zabbix-web-font

# 基本概念

- host groups,
  主机逻辑组，包括主机和模板，主机组下的主机和模板没有任何关系；这个概念主要用于权限控制
- template 模板，一些可以应用到主机的条目的集合，也是为了方便管理
  - application, 应用，就是一组 item 的集合
  - items, 项目，数据单元也是监控的基本单位
  - triggers, 触发器，就是对获取到的数据的逻辑计算表达式，可触发告警
  - graphs, 图形，即监控图
  - screen, 筛选，可以把多个监控图拼到一块
  - discovery rules, 自动发现规则
  - web scenarios，web 探测场景
- host,
  一个待监控的网络设备，从其包含的元素可看出来 host 可以通过 template 生成，注意 host 里没有 screens
  - application
  - items
  - triggers
  - graphs
  - discovery
  - web
- maintenance, 维护阶段，维护阶段内有问题不告警
- event，事件，一些事情发生了，trigger 状态变化，自动发现发生
- action, 动作，预先定义的对事件的响应
- slide shows, 简报片显示，平滑展示定期刷新的图表
- maps，拓扑图绘制
- discovery, 自动发现规则
- it service.， IT 服务，SLA

**注意：**
zabbix 对这些基本元素之间的管理定义的还不是很清楚，比如 template 里的 screens 的使用，这一点确实是其不足之处，这点还有待研究

# Zabbix Style

Zabbix 的使用有很多要说的，熟练使用 Zabbix 配置监控的前提是你得懂得**Zabbix
Style**，下面我基于我说下目前对这种 Style 的理解：首先，不同于 Cacti 为每种元素建立对应的模板（如图形模板，数据模板和主机模板），Zabbix 只用一种主机模板来整合所有的元素，一个主机模板会包括应用，监控项，触发器，图形，过滤，发现和 Web 元素，模板是 Zabbix 的核心之核心。所以配置监控项监控主机的流程基本上是定义模板，定义模板里的元素，将模板应用到主机；然后，对于监控数据的展示 Zabbix 有 screens，slide
shows，maps 和 IT
service 等多种方式来呈现；然后，由于 Zabbix 除了监控还有告警和自动处理的功能，告警就涉及 media
type 告警方式（短信，邮件等）的配置，自动处理就涉及动作的配置以便在事件发生的时候执行一系列的动作，这就是 action；此外，Zabbix 还有一个亮点是自动发现机制，比如自动发现你系统上的分区并采集其使用率，且完成画图等工作，这就是 discoverys；最后，资产管理也是 Zabbix 的一个附加功能，这就是 inventory。

# 参考链接

- [官方文档](https://www.zabbix.com/documentation/2.2/manual)
- [一些 zbbix 模板](https://github.com/jjmartres/Zabbix)
