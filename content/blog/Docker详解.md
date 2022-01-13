---
title: Docker详解
date: 2014-08-16
author: admin
category: container
tags: ['docker']
slug: docker详解
---

<iframe width="100%" height="500px" frameborder="0" src="https://x.xdays.me/slide/docker.html"></iframe>

**说明** 本文档来自前段时间写的一个[slide](https://x.xdays.me/slide/docker.html)，由于 remark 没有很好的支持嵌入到 HTML 中，只能把 markdown 搬过来了。

# Docker

#### by 张向军

---

# Agenda

- ##简介
- ##概念
- ##基础
- ##高级
- ##扩展

---

# 简介

- 针对可移植的应用的简单轻量虚拟环境
- 基于容器提供沙箱，基于 cgroup 和 namespace 做到资源的隔离
- 快速，启动容器就是启动进程
- 轻量，只需要应用运行的依赖
- 容器即目录，故传输方便
- 使用 aufs 或者 devicemapper 等技术作为存储引擎，节省空间
- 仓库机制，可相互分享，搜索等

---

# 概念

- ##cgroups
- ##lxc
- ##aufs
- ##devicemapper
- ##namespace

---

# 概念-cgroups

cgroups 全称 control groups，是 linux 内核提供的一种限制、记录和隔离进程组所使用物理资源的一种机制。在 2.6.24 之后的内核中都已经支持 cgroups。详细的介绍请参考[cgroups 详解](http://files.cnblogs.com/lisperl/cgroups%E4%BB%8B%E7%BB%8D.pdf)和[cgroups 官方文档](https://www.kernel.org/doc/Documentation/cgroups/cgroups.txt)。

应用场景：

- 进程隔离
- 资源统计
- 进程控制

基本概念：

- task，被 cgoups 管理的进程
- control group，分配资源的基本单位
- hierarchy，层级，也就是限制的继承关系
- subsystem，资源控制器

---

#概念-lxc

lxc 全称是 linux container，是基于 cgroups 和 chroot 等内核特性的一组工具，用于构建虚拟环境。通过一系列的命令行工具可以创建，修改，删除虚拟环境。具体用法可参考[ubuntu 官方文档](http://manpages.ubuntu.com/manpages/lucid/man7/lxc.7.html)和[LXC 官方文档](https://linuxcontainers.org/)。

---

#概念-aufs

aufs 全称是 advance(another) union file system，是一种联合文件系统。这种文件系统最重要的一个特性就是有一个层的概念和复制时拷贝，可以做到当文件系统改变时只影响其中一层，其他层保持不变。举个例子，整个文件系统就像由一层一层的玻璃组成的，你从上往下看能看到所有的图案（如果上下层的玻璃完全重合则只能看见上层的玻璃对应的图案），而当你需要新增或者修改图案时就只能在最上层的玻璃上操作。具体的一些操作例子可参考[geekstuff 的 aufs 演示](http://www.thegeekstuff.com/2013/05/linux-aufs/)和[aufs 官方文档](http://aufs.sourceforge.net/aufs3/man.html)

---

#概念-devicemapper

官方说，使用了 LVM 的镜像功能的高级变种作为一种存储引擎。简单来说，devicemapper 是内核的逻辑卷管理框架，它可以做到将多个设备的块映射到一个逻辑卷上，然后对外提供 IO 服务。具体可参考[Linux 内核中的 Device Mapper 机制](http://www.ibm.com/developerworks/cn/linux/l-devmapper/)

---

#概念-namespace

内核级别的资源隔离方案，PID 和 Network 等不再是全局性的而是属于特定的 Namespace，每个 Namespace 对其他的 Namespace 都是透明的。具体可参考[Linux Namespaces 机制](http://www.cnblogs.com/lisperl/archive/2012/05/03/2480316.html)

---

# 基础

- ##安装
- ##拉取
- ##运行
- ##提交
- ##再运行

---

# 基础-安装

## 依赖

内核需要 3.8 以上, ubuntu-12.04 以上，centos-6.5 最新内核

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

从 Docker 官方的 index 上拉取仓库

**注意** 其实拉取的过程就是复制的过程

---

# 基础-运行

## 命令

    docker run -i -t ubuntu /bin/bash

## 解释

从 ubuntu 这个镜像运行一个 container，container 里的进程为 bash

---

# 基础-提交

## 命令

    docker  commit id user/name
    docker push user/name

## 解释

在容器里执行一些改动之后，将这些改动提交到仓库里去，也就是添加了一个新的镜像；然后把这个新的镜像推送到 Docker 的 index 上去。

---

# 基础-再运行

## 命令

    docker pull user/name
    docker run -i -t user/name /bin/bash

## 解释

再次从 index 上拉取镜像，然后从新的镜像启动 container。

---

# 高级

- ##Dockerfile
- ##Link
- ##端口映射

---

# 高级-Dockerfile-简介

## 简介

描述了一个 image 应该是什么样的，然后通过 `docker build` 来生成 image

---

# 高级-Dockerfile-指令参考

## 指令参考

- FROM 当前镜像基于哪个镜像生成
- AUTHOR 镜像作者
- ADD 向镜像里添加文件
- RUN 运行一些安装和命令或者脚本
- EXPOSE 指定链接时暴漏给其他容器的端口
- CMD 启动容器时默认执行的命令
- ENTRYPOINT 启动容器时运行的程序

## CMD 和 ENTRYPOINT 的区别

就是命令和选项的区别，ENTRYPOINT 是命令，CMD 是选项

---

# 高级-Dockerfile-演示

## 演示

### 命令

    docker build -t image_name /path/to/dockerfile_dir

### 解释

通过指定 Dockerfile 所在路径，docker 自动构建 image

---

# 高级-link-简介

## 简介

一种让 Container 之间相互通信更友好的方式，被链接的 container 的信息直接在其他 container 的环境变量里得以体现。

---

# 高级-link-演示

## 演示

### 命令

    docker run -d --name redis redis
    docker run -d --name consumer --link redis:redis ubuntu /bin/bash

### 解释

首先启动一个 redis 的 container，然后将该 container 链接到 consumer 这个 container 上，然后我们可以从这个容器里通过环境变量访问到 redis 的相关信息。

---

# 高级-端口映射-简介

## 简介

一种让 container 提供公网服务的技术，底层为 iptables 的 DNAT 技术实现。

---

# 高级-端口映射-演示

## 演示

### 命令

    docker run -d --name redis -p 6379 redis

### 解释

将物理机的 6379 端口映射到 redis 这个 container 的 6379 端口上。

---

# 扩展

- ##网络相关
- ##开机启动

---

# 扩展-网络相关-简介

## 简介

传统上，Docker 的网络技术其实就是基于网桥和 iptables 的技术，0.11 版本引入 host 模式的网络模式，允许 container 完全共享物理机的网络，不再需要 iptables 做映射。

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

1. 关闭 Docker 的自动启动特性`-r=false`
2. 配合 upstart 或者 systemd 的配置文件，调用 Docker 命令来开机启动

## 内部

也就是如何在启动容器时再其内部自动启动进程。很遗憾，目前 Docker 容器和 systemd 还不兼容。目前我用的方案是 supervisor 来管理容器内的进程。详见[upops 项目的 Dockerfile](http://gitlab.widget-inc.com/xdays/docker-upops)

---

# 资源

1. [Official Document](http://docs.docker.io/en/latest/)
2. [Docker Weekly](http://blog.docker.io/docker-weekly-archives/)
3. [Docker Book](http://www.dockerbook.com)
4. [User Group](https://groups.google.com/forum/#!forum/docker-user)

---

# Q&A
