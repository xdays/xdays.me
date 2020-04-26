---
title: freeradius&mysql简单配置一例
date: 2011-01-20
author: admin
category: server
slug: freeradiusmysql-简单配置
---

总体说下：

我用的是 ubuntu
server，因为他的强大方便的包管理系统，省了好多脑细胞。总体环境是 lamp +
phpmyadmin +
freeradius，lamp 提供给 freeradius 数据库和 phpmyadmin 运行的环境。这里我仅仅实现了基本的功能就是认证，拿的思科交换机开启 aaa 功能测试，也就是客户端登录交换机先通过 freeradius 的认证，通过即可操作交换机否则拒绝。

引用一张图：

[![aaacs](/wp-content/uploads/2011/01/AAAbs-1024x804.jpg 'aaacs')](/wp-content/uploads/2011/01/AAAbs.jpg)

基于 C/S 架构，只是这里数据库和 freeradius 放一台上了。

开始安装：

1）安装 lamp

安装系统的时候直接选上 lamp 环境就行了，需要设置一个 mysql 密码（这里是 thinkin）

2）安装 phpmyadmin

apt-get install
phpmyadmin，安装过程时让设置个管理 phpmyadmin 自身数据库的密码（还是 thinkin，其实也没大用处，没考虑安全，直接用的 root）

3）安装 freeradius

apt-get intall freeradius
freeradius-sql（数据库模块），默认安装没什么问题

开始配置：

首先列举下需要配置的文件 radiusd.conf（主配置文件，其他文件都是通过@INCLUDE 包含进来的），client.conf（NAS 网络接入服务器，对于 freeradius 来说是客户端的配置文件），sql.conf（数据库相关的配置文件），sites-available/default（默认虚拟主机的配置文件），再者就是 mysql 数据库中的数据了下面是具体每个文件需要修改的地方：

1）radiusd.conf：找到\$INCLUDE
sql.conf 这一行去掉前面的注释，把 sql.conf 的相关配置包含进来

2）sql.conf：找到如下两行：

login = "radius"

password = "radpass"修改为：

login = "root"

password = "thinkin"其他的默认

3）sites-available/default：去掉 authorize {}（授权）和 accounting
{}（记账）中的 sql 一行前的\#，对于认证 authenticate
（认证）{}字段中 sql 已经开启

4）创建导入 mysql 数据库

\#mysql –u root –p

\#create database
radius（也可用 phpmyadmin，但是这里的数据库名必须是 radius，和 sql.conf 对应的）

\#mysql –u root –p \<
/etc/freeradius/sql/mysql/schema.sql（导入数据库模板）

\#insert into radius  (username,attribute,op,value)  values (0,’test’,’
User-Password’,’ :=’,’test’);（添加一个测试用户）后续的添加类似。
