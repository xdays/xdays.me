---
title: Cobbler自动化安装Linux系统
date: 2013-08-09
author: admin
category: server
tags: ['pxe', 'server']
slug: cobbler自动化安装linux系统
---

# 简介

根据官方文档的定位，Cobbler 首要的是快速设置网络安装环境的 Linux 安装服务器；但其功能不限于此，它还可以管理配置，管理 DNS，HDCP，TFTP 和 rsync，软件包升级和电源管理等；个人感觉有些乱，作为一个开源项目明白自己想要解决什么问题并把这个问题解决到极致就够了。

# 说明

血与泪的经历：

- Cobbler2.2（来自 CentOS5.5）
  安装 CentOS5.5 和 CentOS6.4 没有问题，安装 Ubuntu12.04 失败
- Cobbler2.4（来自 CentOS6.4）
  安装 CentOS5.5 和 CentOS6.4 没有问题，安装 Ubuntu12.04 没问题

# 基本概念

## PXE 原理

![PXE原理](/wp-content/uploads/2013/08/pxe-flow.png)

1.  客户端发起 Discover 包，通过 flag 说明自身的 PXE 拓展信息；
2.  服务器响应 Offer 包，告知客户端下边去找哪台服务器；
3.  客户端发送 Request 包
4.  服务器发送 ACK 包
5.  客户端通过 TFTP 协议请求 pxelinux.0 等文件
6.  客户端加载并启动系统

## Cobbler 模型

![Cobbler模型](/wp-content/uploads/2013/08/how-we-do.png)

这张图画出了 Cobbler 的模型，越往上的对象越基础越通用，自上而下不断的添加一些新的东西进来让其满足个性化的需求。这里我们需要重点关注的是 distro 和 profile 这两个概念。

# 安装

## 安装 EPEL 或者 rpmforge

- CentOS5

      rpm -ivh http://mirrors.yun-idc.com/epel/5/x86_64/epel-release-5-4.noarch.rpm #坑，此源安装的cobbler不可用
      rpm -ivh http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el5.rf.x86_64.rpm

- CentOS6

      rpm -ivh http://mirrors.yun-idc.com/epel/6/x86_64/epel-release-6-8.noarch.rpm

## 安装 Cobbler

    yum install -y dhcp cobbler cobbler-web

# 配置

## 配置 Cobbler

    vim /etc/cobbler/settings

修改如下：

    next-server: 本机IP
    server: 本机IP
    manage_dhcp: 1

## 配置 Cobbler_web

    sed -i 's/authn_denyall/authn_configfile/g' /etc/cobbler/modules.conf
    htdigest /etc/cobbler/users.digest "Cobbler" cobbler

## 配置 dhcp

    vim /etc/cobbler/dhcp.template

修改如下：

    subnet 192.168.110.0 netmask 255.255.255.0 {
         option routers             192.168.110.1;
         option domain-name-servers 8.8.8.8;
         option subnet-mask         255.255.255.0;
         range dynamic-bootp        192.168.110.100 192.168.110.254;
         filename                   "/pxelinux.0";
         default-lease-time         21600;
         max-lease-time             43200;
         next-server                $next_server;
    }

## 配置 xinetd

    vim /etc/xinet.d/{rsync,tftp}

修改如下：

    disable = no

# 检查并处理问题

## 检查

    cobbler check

## 处理问题

一些根据提示就能解决的问题，这里不再赘述了。

# 导入版本

**注意：目前可以在不折腾的情况下自动安装 CentOS 和 Ubuntu**

## 挂载镜像

    mount -t auto -o loop distro.iso /mnt

## 导入版本

    cobbler import --path=/mnt --name=distro-name

# 同步配置

    cobbler sync

# 参考链接

[运维自动化之 Cobbler 系统安装详解](http://os.51cto.com/art/201109/288604.htm)  
[利用 Cobbler 批量布署 CentOS](http://kerry.blog.51cto.com/172631/648430)  
[官方文档](http://www.cobblerd.org/manuals/2.4.0/)
