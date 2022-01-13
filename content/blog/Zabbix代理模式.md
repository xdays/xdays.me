---
title: Zabbix代理模式
date: 2015-06-13
author: admin
category: monitor
tags: ['monitor', 'zabbix']
slug: zabbix代理模式
---

#简介
Proxy 模式用于监控服务器无法直接访问被监控机器的情况，如内网监控。

#安装 ##安装源
rpm -ivh http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm

##安装 proxy 及依赖
yum install -y zabbix-proxy-mysql mysql-server

##mysql 初始化
/usr/bin/mysql_secure_installation

#配置 ##创建数据库

```
CREATE DATABASE zabbix CHARACTER SET utf8;
GRANT ALL ON zabbix.* TO zabbix@'localhost' IDENTIFIED BY 'zabbixpass';
```

##导入数据
mysql -uzabbix -pzabbixpass zabbix < /usr/share/doc/zabbix-proxy-mysql-2.2.2/create/schema.sql

##配置 proxy

```
Server= 服务器IP
Hostname= 主机名
DBName=zabbix 数据库名
DBUser=zabbix 用户名
DBPassword=zabbixpass 密码
```

##配置 server

###添加 Proxy
在 administration->DM 下选择 Proxy，创建 Proxy。

- 选择被动模式，注意这里的被动模式是指 Proxy 不主动向 Server 汇报监控数据，Server 要什么 Proxy 就问 Agent 要什么
- 连接 IP 和端口号，填写 Proxy 的监听地址和端口

###添加 host
在 Server 的 web 界面上创建 host 的时候在 Monitored by proxy 选择要使用的 proxy 即可。

##配置 agent
主要的配置向包括如下：

    Server= 配置为Proxy的地址

**注意** 如果不需要开启主动探测，保持 ServerActive 配置项为空即可
