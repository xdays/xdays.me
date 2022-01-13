---
title: Zabbix监控Hadoop
date: 2014-03-06
author: admin
category: monitor
tags: ['monitor', 'zabbix']
slug: zabbix监控hadoop
---

# 基础概念

## JMX

JMX 就是 Java Management
Extentions，为 Java 程序提供管理功能的框架。看了几个介绍，感觉[这个说明](http://www.blogjava.net/chengang/archive/2006/03/07/34061.html)比较通俗易懂。一句话说就是 JMX 为你提供了一个通过特定协议管理应用程序的方案，而我们这里主要用其查询配置和监控数据的功能。

## External Check

通过主动调用自定义脚本来获取监控数据，脚本的输出即为该监控项的监控值，这种方式有更强的定制化。因为下午在这里踩到了坑，走了不少弯路，所以这里要对配置方法做个特殊说明。配置监控项时选择 external
chek，然后在 key 这一栏要指定运行脚本和参数。下边说下 1.8 和 2.0 之后的版本在 key 配置上的不同：  
\*
在 1.8 的版本里 key 的格式为`scriptname[arg1 arg2 ...]`，参数以空格，Zabbix 实际执行的命令是`scriptname server_hostname arg1 arg2`，详见[这里](https://www.zabbix.com/documentation/1.8/manual/config/items#external_checks)  
\*
在 2.0 之后的版本 key 的格式为`scriptname[arg1, arg2 ...]`，参数以逗号分隔，Zabbix 实际执行的命令是`scriptname arg1 arg2 ...`，详见[这里](https://www.zabbix.com/documentation/2.2/manual/config/items/itemtypes/external)  
​  
所以，拿 1.8 的模板倒入到 2.0 之后的的 Zabbix
Server 是有问题的，这点需要特别注意。

## Trapper

trapper 也是 Zabbix 的一种获取监控数据的方式。我们知道常见的方式有 agent，snmp 和 jmx，这些监控方式都是 Zabbix
Server 主动去问被监控设备要，而 trapper 是被动等着被监控设备把数据汇报（通过 zabbix_sender）上来，然后从汇报上来的数据中提取自己想要的。

**注意**
如果被监控端提供了接口可供外界获取其运行数据（不太安全），那么可配合 external
check 调用脚本远程获取数据，然后再用 zabbix_sender 将获取的数据以 trapper 的形式发送给 Zabbix
Server，这样既可以保证客户端零配置，而且能获取任意想要监控的数据。逻辑图如下：

    zabbix server --> external check-->script --> monitored device
    script--> zabbix_sender --> zabbx server

​

# 配置过程

1.  下载监控 hadoop 需要的模板和外挂脚本，链接在[这里](http://mikoomi.googlecode.com/svn/plugins/)
2.  在本地，通过浏览器将两个模板导入 zabbix，**注意**两个模板有重复的监控项，如果需要对同一个设备监控需要删掉重复的 hadoop
    version 和 hadoop status 两个监控项
3.  在服务器端，将外挂脚本放到 zabbix 服务器的指定目录下，具体要看 zabbix_server.conf 的 ExternalScripts 这个配置项，一般如果是编译安装的默认应该位于/usr/local/zabbix/share/zabbix/externalscripts 目录下，也可修改配置文件自己指定，这里有两点需要注意：1)如果你的 bash 安装在/bin 下，那么所有的脚本要修改第一行为\#!/bin/sh; 2)确保脚本有可执行权限，且要注意脚本执行用户（即 Zabbix
    Server 的运行用户）具有所有的操作权限，如写文件等。
4.  修改 zabbix_server.conf 去掉 ExternalScripts 这行的注释，重启 zabbix_server

# 参考链接

- [JMX 简单解释](http://www.blogjava.net/chengang/archive/2006/03/07/34061.html)
- [1.8 的外部脚本探测](https://www.zabbix.com/documentation/1.8/manual/config/items#external_checks)
- [2.0 后的外部脚本探测](https://www.zabbix.com/documentation/2.2/manual/config/items/itemtypes/external)
- [Zabbix 监控 Hadoop 的插件项目](https://code.google.com/p/mikoomi/)
