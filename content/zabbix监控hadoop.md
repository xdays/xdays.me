Title: Zabbix监控Hadoop
Date: 2014-03-06 23:17
Author: admin
Category: monitor
Tags: monitor, zabbix
Slug: zabbix监控hadoop

基础概念
========

JMX
---

JMX就是Java Management
Extentions，为Java程序提供管理功能的框架。看了几个介绍，感觉[这个说明](http://www.blogjava.net/chengang/archive/2006/03/07/34061.html)比较通俗易懂。一句话说就是JMX为你提供了一个通过特定协议管理应用程序的方案，而我们这里主要用其查询配置和监控数据的功能。

External Check
--------------

通过主动调用自定义脚本来获取监控数据，脚本的输出即为该监控项的监控值，这种方式有更强的定制化。因为下午在这里踩到了坑，走了不少弯路，所以这里要对配置方法做个特殊说明。配置监控项时选择external
chek，然后在key这一栏要指定运行脚本和参数。下边说下1.8和2.0之后的版本在key配置上的不同：  
\*
在1.8的版本里key的格式为`scriptname[arg1 arg2 ...]`，参数以空格，Zabbix实际执行的命令是`scriptname server_hostname arg1 arg2`，详见[这里](https://www.zabbix.com/documentation/1.8/manual/config/items#external_checks)  
\*
在2.0之后的版本key的格式为`scriptname[arg1, arg2 ...]`，参数以逗号分隔，Zabbix实际执行的命令是`scriptname arg1 arg2 ...`，详见[这里](https://www.zabbix.com/documentation/2.2/manual/config/items/itemtypes/external)  
​  
所以，拿1.8的模板倒入到2.0之后的的Zabbix
Server是有问题的，这点需要特别注意。

Trapper
-------

trapper也是Zabbix的一种获取监控数据的方式。我们知道常见的方式有agent，snmp和jmx，这些监控方式都是Zabbix
Server主动去问被监控设备要，而trapper是被动等着被监控设备把数据汇报（通过zabbix\_sender）上来，然后从汇报上来的数据中提取自己想要的。

**注意**
如果被监控端提供了接口可供外界获取其运行数据（不太安全），那么可配合external
check调用脚本远程获取数据，然后再用zabbix\_sender将获取的数据以trapper的形式发送给Zabbix
Server，这样既可以保证客户端零配置，而且能获取任意想要监控的数据。逻辑图如下：

    zabbix server --> external check-->script --> monitored device
    script--> zabbix_sender --> zabbx server

​

配置过程
========

1.  下载监控hadoop需要的模板和外挂脚本，链接在[这里](http://mikoomi.googlecode.com/svn/plugins/)
2.  在本地，通过浏览器将两个模板导入zabbix，**注意**两个模板有重复的监控项，如果需要对同一个设备监控需要删掉重复的hadoop
    version和hadoop status两个监控项
3.  在服务器端，将外挂脚本放到zabbix服务器的指定目录下，具体要看zabbix\_server.conf的ExternalScripts这个配置项，一般如果是编译安装的默认应该位于/usr/local/zabbix/share/zabbix/externalscripts目录下，也可修改配置文件自己指定，这里有两点需要注意：1)如果你的bash安装在/bin下，那么所有的脚本要修改第一行为\#!/bin/sh;
    2)确保脚本有可执行权限，且要注意脚本执行用户（即Zabbix
    Server的运行用户）具有所有的操作权限，如写文件等。
4.  修改zabbix\_server.conf去掉ExternalScripts这行的注释，重启zabbix\_server

参考链接
========

-   [JMX简单解释](http://www.blogjava.net/chengang/archive/2006/03/07/34061.html)
-   [1.8的外部脚本探测](https://www.zabbix.com/documentation/1.8/manual/config/items#external_checks)
-   [2.0后的外部脚本探测](https://www.zabbix.com/documentation/2.2/manual/config/items/itemtypes/external)
-   [Zabbix监控Hadoop的插件项目](https://code.google.com/p/mikoomi/)

