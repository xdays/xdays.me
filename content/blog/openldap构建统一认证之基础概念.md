---
title: OpenLDAP构建统一认证之基础概念
date: 2014-05-15
author: admin
category: server
tags: server, ldap
slug: openldap构建统一认证之基础概念
---

目录服务与关系数据库
====================

目录数据库系统和关系数据库系统都是用来保存数据的，但是他们有两个主要的不同点：

-   数据结构，目录服务只有树形结构，不像关系数据库有复杂的数据结构。
-   查询速度与写入速度，目录服务适合查询，不适合写入。

基本概念
========

在浏览LDAP相关文档时经常会遇见一些概念，下面是常见概念的简单解释：

-   DIT，目录信息树，近似相当于一个表
-   Entry，条目，也叫记录项
-   DN，是无歧义标识一个条目的名字，如"cn=alair,dc=account,dc=xdays,dc=info"，相当于主键
-   属性，一个条目可以有多个属性，常见的属性有CN，O，OU，DC等
-   ObjectClass，对象类，决定了一个条目能具备哪些属性，以及属性对应值的类型
-   Schema，Schema是对象类的集合
-   baseDN，基本DN，baseDN执行绑定查询时的根目录
-   RootDN，根目录，也就是绑定了OpenLDAProotDSE这个类的条目。
-   O，组织，是一个对象类，用于组织记录项
-   OU，组织单元，也是一个对象类，用于组织记录项，比O小一个等级。
-   RDN，RDN是相对DN，类比于相对路径
-   CN，CN是通用名称类似于别名，与RDN没有关系
-   DC，域名成分

LDIF
====

简介
----

LDIF是LDAP的数据交换格式，就像json，xml等一样。其格式可以大体描述如下：

-   第一行指定LDIF的版本号
-   整个文件是以记录（record）来组织的，不同的记录间用空行分隔
-   记录分为数据记录和操作记录，数据记录就是保存实际的数据的，而操作记录用于修改数据
-   文件中非ASCII的数据存储这里不研究了

数据记录
--------

数据记录很简单，就是一组属性值对，如果行太长可以以空格开头来续行，一个数据记录的实例如下：

    dn: ou=user,dc=xdays,dc=info
    objectClass: organizationalUnit
    ou: user
    dn: ou=group,dc=xdays,dc=info
    objectClass: organizationalUnit
    ou: group
    dn: ou=hosts,dc=xdays,dc=info
    objectClass: organizationalUnit
    ou: hosts

操作记录
--------

操作记录稍复杂一点。一个操作记录是由一个或者多个操作组成的，每个操作以"-"开头的行隔开；可用的操作包括add,
delete, replace等操作。如下是一个操作记录的实例：

    dn: cn=config
    replace: olcTLSCertificateFile
    olcTLSCertificateFile: /etc/ldap/certs/ldap.crt
    -
    replace: olcTLSCertificateKeyFile
    olcTLSCertificateKeyFile: /etc/ldap/certs/ldap.key

参考资料
========

-   http://schnell18.iteye.com/blog/39208
-   http://blog.csdn.net/wuyupengwoaini/article/details/12855927
-   http://yunfeng.blog.51cto.com/202525/281009

