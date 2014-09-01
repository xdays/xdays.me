Title: Docker初识
Date: 2014-01-12 22:44
Author: admin
Category: cloud
Tags: cloud, docker
Slug: docker初识

简介
====

如官方文档所说，docker是一个自动将应用打包成轻量可移植自包涵的容器的引擎。开发者构建的应用可以一次构建全平台运行，包括本地开发机，生产环境，虚拟机和云等。目前处于开发阶段，不可用于生产环境。在你启动一条命令时docker会调用lcx等其他一个组建为这条命令构建一个container，包含了进程运行的所有资源。但是官方文档以说明，docker处于开发阶段目前还不能用于生产环境。

特性
====

-   Go语言编写
-   基于lxc的进程级隔离，而lxc基于cgroup，轻量级
-   通过cgroup做到文件系统，网络和资源的隔离
-   使用aufs文件系统存储，写时复制，相同数据只保存一份，节省空间
-   源机制，可相互分享，搜索等

概念
====

cgroups
-------

cgroups全称control
groups，是linux内核提供的一种限制、记录和隔离进程组所使用物理资源的一种机制。在2.6.24之后的内核中都已经支持cgroups。详细的介绍请参考[cgroups详解](https://www.kernel.org/doc/Documentation/cgroups/cgroups.txt)。

lxc
---

lxc全称是linux
container，是基于cgroups和chroot等内核特性的一组工具，用于构建虚拟环境。通过一系列的命令行工具可以创建，修改，删除虚拟环境。具体用法可参考[ubuntu官方文档](http://www.unionfs.org/)。

aufs
----

aufs全称是advance(another) union file
system，是一种联合文件系统。这种文件系统最重要的一个特性就是有一个层的概念和复制时拷贝，可以做到当文件系统改变时只影响其中一层，其他层保持不变。举个例子，整个文件系统就像由一层一层的玻璃组成的，你从上往下看能看到所有的图案（如果上下层的玻璃完全重合则只能看见上层的玻璃对应的图案），而当你需要新增或者修改图案时就只能在最上层的玻璃上操作。具体的一些操作例子可参考[geekstuff的aufs演示](http://aufs.sourceforge.net/aufs3/man.html)

安装
====

**注意：** docker要求内核在3.8以上，所以建议的安装系统为ubuntu。

ubuntu
------

    curl -s https://get.docker.io/ubuntu/ | sudo sh

centos
------

1.  安装epel rpm -ivh
    http://dl.fedoraproject.org/pub/epel/6/x86\_64/epel-release-6-8.noarch.rpm

2.  安装docker yum install -y docker-io

3.  启动 service docker start chkconfig docker on

使用
====

命令行
------

### 获取base image

    docker pull ubuntu   

这条命令会从docker index上获取ubuntu镜像，它是运行其他进程的基础。

### 运行命令

    docker run -i -t ubuntu yum install -y vim

### 提交改变

    docker images
    docker commit id user/name
    docker push user/name

### 再次运行

    docker pull user/name
    docker run -i -t image vim

*注意：*
这里的再次运行是指你所构建的环境可以再其他任何平台上运行起来，不需要额外的配置，没有依赖。

Dockerfile
----------

dockerfile通过一些指令来描述了一个image的方方面面。

    # Memcached
    #
    # VERSION       2.2
    # use the ubuntu base image provided by dotCloud
    FROM ubuntu
    MAINTAINER Victor Coisne victor.coisne@dotcloud.com
    # make sure the package repository is up to date
    RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
    RUN apt-get update
    # install memcached
    RUN apt-get install -y memcached
    # Launch memcached when launching the container
    ENTRYPOINT ["memcached"]
    # run memcached as the daemon user
    USER daemon
    # expose memcached port
    EXPOSE 11211

其中的一些指令解释：

-   FROM指定此image的base image
-   MAINTAINER指定image的维护者
-   RUN指定在当前的image下运行的命令，相当于`docker run image command`
-   ENTRYPOINT指定在运行image时触发的命令
-   USER指定运行出发命令的用户名
-   EXPOSE指定对外提供的端口号

参考链接
========

-   [cgroup的官方文档](https://www.kernel.org/doc/Documentation/cgroups/cgroups.txt)
-   [aufs比unionfs好在哪里](http://www.unionfs.org/)
-   [aufs的官方文档](http://aufs.sourceforge.net/aufs3/man.html)
-   [docker官方文档](http://docs.docker.io/en/latest/)

