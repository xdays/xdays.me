---
title: Zabbix编译安装
date: 2013-11-20
author: admin
category: monitor
tags: monitor, zabbix
slug: zabbix编译安装
---

安装依赖
========

由于自带的PHP版本为5.1，而Zabbix2.2对PHP版本需要是不低于5.3，故而卸载系统自带的版本安装5.3：

    rpm -e php-common php-cli php
    yum install httpd yum install php53 php53-cli php53-common php53-pdo php53-mysql php53-gd php53-bcmath php53-xml php53-mbstring mysql mysql-server mysql-devel net-snmp net-snmp-utils net-snmp-devel

下载解压
========

    wget -SO zabbix-2.2.0.tar.gz "http://sourceforge.net/projects/zabbix/files/ZABBIX%20Latest%20Stable/2.2.0/zabbix-2.2.0.tar.gz/download" && tar xzf zabbix-2.2.0.tar.gz && cd zabbix-2.2.0

配置
====

    ./configure --enable-server --enable-agent --with-mysql --enable-ipv6 --with-net-snmp --with-libcurl --with-libxml2 --prefix=/usr/local/zabbix-2.2.0

安装主程序
==========

    make install
    ln -s /usr/local/zabbix-2.2.0 /usr/local/zabbix

配置zabbix\_server.conf
=======================

修改zabbix server配置文件

    vim /usr/local/zabbix/etc/zabbix_server.conf

内容如下：

    LogFile=/tmp/zabbix_server.log
    DBHost= ip
    DBName=zabbix
    DBUser=zabbix
    DBPassword=passwd

创建用户
========

    groupadd zabbix
    useradd -g zabbix -M -s /sbin/nologin zabbix

启动
====

    cd /usr/local/zabbix/sbin && ./zabbix_server && ./zabbix_agentd

安装fontend
===========

程序文件
--------

cp -a frontend/php /user/local/zabbix-web

配置Web服务器
-------------

修改zabbix对应的配置文件

    vim /etc/httpd/conf.d/zabbix-web.conf

<p>
内容如下：  

<script src="https://gist.github.com/xdays/7564955.js"></script>
</p>
然后重启apache

    service httpd restart

Web安装
-------

访问http://zabbix\_server/zabbix/，然后按照安装向导操作即可。
