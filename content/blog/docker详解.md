---
title: Docker详解
date: 2014-08-16
author: admin
category: container
tags: docker
slug: docker详解
---

<iframe width="100%" height="500px" frameborder="0" src="http://x.xdays.me/slide/docker.html"></iframe>

**说明** 本文档来自前段时间写的一个[slide](https://x.xdays.me/slide/docker.html)，由于remark没有很好的支持嵌入到HTML中，只能把markdown搬过来了。

# Docker
#### by 张向军

---

# Agenda

* ##简介
* ##概念
* ##基础
* ##高级
* ##扩展

---

# 简介

* 针对可移植的应用的简单轻量虚拟环境
* 基于容器提供沙箱，基于cgroup和namespace做到资源的隔离
* 快速，启动容器就是启动进程
* 轻量，只需要应用运行的依赖
* 容器即目录，故传输方便
* 使用aufs或者devicemapper等技术作为存储引擎，节省空间
* 仓库机制，可相互分享，搜索等

---

# 概念

* ##cgroups
* ##lxc
* ##aufs
* ##devicemapper
* ##namespace

---

# 概念-cgroups

cgroups全称control groups，是linux内核提供的一种限制、记录和隔离进程组所使用物理资源的一种机制。在2.6.24之后的内核中都已经支持cgroups。详细的介绍请参考[cgroups详解](http://files.cnblogs.com/lisperl/cgroups%E4%BB%8B%E7%BB%8D.pdf)和[cgroups官方文档](https://www.kernel.org/doc/Documentation/cgroups/cgroups.txt)。

应用场景：
* 进程隔离
* 资源统计
* 进程控制

基本概念：
* task，被cgoups管理的进程
* control group，分配资源的基本单位
* hierarchy，层级，也就是限制的继承关系
* subsystem，资源控制器

---

#概念-lxc

lxc全称是linux container，是基于cgroups和chroot等内核特性的一组工具，用于构建虚拟环境。通过一系列的命令行工具可以创建，修改，删除虚拟环境。具体用法可参考[ubuntu官方文档](http://manpages.ubuntu.com/manpages/lucid/man7/lxc.7.html)和[LXC官方文档](https://linuxcontainers.org/)。

---

#概念-aufs

aufs全称是advance(another) union file system，是一种联合文件系统。这种文件系统最重要的一个特性就是有一个层的概念和复制时拷贝，可以做到当文件系统改变时只影响其中一层，其他层保持不变。举个例子，整个文件系统就像由一层一层的玻璃组成的，你从上往下看能看到所有的图案（如果上下层的玻璃完全重合则只能看见上层的玻璃对应的图案），而当你需要新增或者修改图案时就只能在最上层的玻璃上操作。具体的一些操作例子可参考[geekstuff的aufs演示](http://www.thegeekstuff.com/2013/05/linux-aufs/)和[aufs官方文档](http://aufs.sourceforge.net/aufs3/man.html)

---

#概念-devicemapper

官方说，使用了LVM的镜像功能的高级变种作为一种存储引擎。简单来说，devicemapper是内核的逻辑卷管理框架，它可以做到将多个设备的块映射到一个逻辑卷上，然后对外提供IO服务。具体可参考[Linux 内核中的 Device Mapper 机制](http://www.ibm.com/developerworks/cn/linux/l-devmapper/)

---

#概念-namespace

内核级别的资源隔离方案，PID和Network等不再是全局性的而是属于特定的Namespace，每个Namespace对其他的Namespace都是透明的。具体可参考[Linux Namespaces机制](http://www.cnblogs.com/lisperl/archive/2012/05/03/2480316.html)

---

# 基础

* ##安装
* ##拉取
* ##运行
* ##提交
* ##再运行

---

# 基础-安装

## 依赖
内核需要3.8以上, ubuntu-12.04以上，centos-6.5最新内核

## ubuntu
    curl -s https://get.docker.io/ubuntu/ | sudo sh

## centos
    rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    yum install -y docker-io

---

# 基础-拉取

## 命令

    docker pull ubuntu

## 解释

从Docker官方的index上拉取仓库

**注意** 其实拉取的过程就是复制的过程

---

# 基础-运行

## 命令

    docker run -i -t ubuntu /bin/bash

## 解释

从ubuntu这个镜像运行一个container，container里的进程为bash

---

# 基础-提交

## 命令

    docker  commit id user/name
    docker push user/name

## 解释

在容器里执行一些改动之后，将这些改动提交到仓库里去，也就是添加了一个新的镜像；然后把这个新的镜像推送到Docker的index上去。

---

# 基础-再运行

## 命令

    docker pull user/name
    docker run -i -t user/name /bin/bash

## 解释

再次从index上拉取镜像，然后从新的镜像启动container。

---

# 高级

* ##Dockerfile
* ##Link
* ##端口映射

---

# 高级-Dockerfile-简介

## 简介
描述了一个image应该是什么样的，然后通过 `docker build` 来生成image

---

# 高级-Dockerfile-指令参考

## 指令参考

* FROM 当前镜像基于哪个镜像生成
* AUTHOR 镜像作者
* ADD 向镜像里添加文件
* RUN 运行一些安装和命令或者脚本
* EXPOSE 指定链接时暴漏给其他容器的端口
* CMD 启动容器时默认执行的命令
* ENTRYPOINT 启动容器时运行的程序

## CMD和ENTRYPOINT的区别

就是命令和选项的区别，ENTRYPOINT是命令，CMD是选项

---

# 高级-Dockerfile-演示

## 演示
### 命令
    docker build -t image_name /path/to/dockerfile_dir

### 解释
通过指定Dockerfile所在路径，docker自动构建image

---

# 高级-link-简介

## 简介
一种让Container之间相互通信更友好的方式，被链接的container的信息直接在其他container的环境变量里得以体现。

---

# 高级-link-演示

## 演示
### 命令
    docker run -d --name redis redis
    docker run -d --name consumer --link redis:redis ubuntu /bin/bash

### 解释
首先启动一个redis的container，然后将该container链接到consumer这个container上，然后我们可以从这个容器里通过环境变量访问到redis的相关信息。

---

# 高级-端口映射-简介

## 简介
一种让container提供公网服务的技术，底层为iptables的DNAT技术实现。

---

# 高级-端口映射-演示
## 演示
### 命令
    docker run -d --name redis -p 6379 redis

### 解释
将物理机的6379端口映射到redis这个container的6379端口上。

---

# 扩展

* ##网络相关
* ##开机启动

---

# 扩展-网络相关-简介

## 简介
传统上，Docker的网络技术其实就是基于网桥和iptables的技术，0.11版本引入host模式的网络模式，允许container完全共享物理机的网络，不再需要iptables做映射。

---

# 扩展-网络相关-演示

## 演示
### 命令
    docker run -d --name redis --net host redis /sbin/ip addr
### 解释
直接使用物理机的网络

---

# 扩展-开机启动

## 外部
也就是如何开机启动对应的容器，主要有两步操作：
1. 关闭Docker的自动启动特性`-r=false`
2. 配合upstart或者systemd的配置文件，调用Docker命令来开机启动

## 内部
也就是如何在启动容器时再其内部自动启动进程。很遗憾，目前Docker容器和systemd还不兼容。目前我用的方案是supervisor来管理容器内的进程。详见[upops项目的Dockerfile](http://gitlab.widget-inc.com/xdays/docker-upops)

---

# 资源
1. [Official Document](http://docs.docker.io/en/latest/)
2. [Docker Weekly](http://blog.docker.io/docker-weekly-archives/)
3. [Docker Book](http://www.dockerbook.com)
4. [User Group](https://groups.google.com/forum/#!forum/docker-user)

---

# Q&A
